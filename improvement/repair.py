"""Boucle compile-and-repair pour l'amelioration de code Maude par LLM.

Motivation (issue de l'analyse des resultats rag-gemini-2.5-flash) :
- 4/19 echecs etaient des erreurs de PARSING (when, Unicode, --, = vs ==)
- 2/19 compilaient mais etaient FAUX (pattern non-lineaire, matching Nat)
Tous detectables en local : le paquet `maude` parse et reduit les termes.
La boucle reinjecte le diagnostic (linter + parseur + cas de test en echec)
et redemande une correction, au plus --max-iters fois.

Usage :
    python repair.py tests/original/maudec/maude/pow.maude -m gemini-2.5-flash
    python repair.py <fichier> -m scripted:responses.json --rag none   # tests

Le RAG est configurable (--rag ../rag-system | ../maude-rag-hybrid |
../maude-rag-sections | none) : la boucle sert aussi a comparer les RAG.
"""
import argparse
import json
import os
import random
import re
import subprocess
import sys
import tempfile
try:
    import tomllib
except ImportError:                      # Python < 3.11
    import tomli as tomllib
from pathlib import Path

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linter import autofix, lint, fatals, format_issues
from check import make_tests, MaudeDriver

HERE = Path(__file__).parent
EVAL_TIMEOUT = 60

# Cles API : .env local (improvement/) puis celui de rag-system —
# GEMINI_API_KEY et EDENAI_API_KEY y sont cherchees sans export manuel.
# load_dotenv n'ecrase pas une variable deja exportee dans le shell.
try:
    from dotenv import load_dotenv
    load_dotenv()
    load_dotenv(HERE.parent / 'rag-system' / '.env')
except ImportError:
    pass


# ---------------------------------------------------------------------------
# Evaluation Maude (sous-processus isole)
# ---------------------------------------------------------------------------

def evaluer(code, termes):
    """Charge `code` dans Maude et reduit `termes`.
    Retourne (loaded, results, stderr)."""
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "candidate.maude"
        src.write_text(code)
        tj = Path(tmp) / "termes.json"
        tj.write_text(json.dumps(termes))

        try:
            proc = subprocess.run(
                (sys.executable, str(HERE / "maude_eval.py"), str(src), str(tj)),
                capture_output=True, text=True, timeout=EVAL_TIMEOUT,
            )
        except subprocess.TimeoutExpired:
            return False, {}, "timeout : la reduction ne termine pas (boucle infinie probable)"

        # stderr avant ===TERMES=== : chargement ; apres : parsing des termes
        stderr_load, _, stderr_terms = proc.stderr.partition("===TERMES===")
        stderr_load = stderr_load.strip()

        if proc.returncode != 0:
            return False, {}, stderr_load or f"le processus Maude a echoue (code {proc.returncode})"

        try:
            data = json.loads(proc.stdout)
        except json.JSONDecodeError:
            return False, {}, stderr_load or "sortie illisible de l'evaluateur"

        # comme check.py : des warnings au CHARGEMENT = build error
        if not data["loaded"] or "Warning" in stderr_load or "Error" in stderr_load:
            return False, data.get("results", {}), stderr_load

        return True, data["results"], stderr_load


# ---------------------------------------------------------------------------
# Connecteurs LLM
# ---------------------------------------------------------------------------

MAIN_SCHEMA = {
    'type': 'object',
    'properties': {
        'comment': {'type': 'string',
                    'description': 'The model reply except for the modified code'},
        'code': {'type': 'string',
                 'description': 'The modified code (a multiline string)'},
    },
    'required': ['comment', 'code'],
}


class Gemini:
    """Connecteur Gemini (meme API que rag-gemini.py)."""

    API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent'
    SCHEMA = {'responseMimeType': 'application/json', 'responseJsonSchema': MAIN_SCHEMA}

    def __init__(self, model):
        self.session = requests.Session()
        self.model = model
        self.session.headers.update({'x-goog-api-key': os.environ['GEMINI_API_KEY']})

    def ask(self, message):
        answer = self.session.post(
            self.API_URL.format(model=self.model),
            json={'contents': [{'parts': [{'text': message}]}],
                  'generationConfig': self.SCHEMA},
        )
        if answer.status_code != 200:
            raise ValueError(f'API error: {answer.content}')
        return json.loads(answer.json()['candidates'][0]['content']['parts'][0]['text'])


class Scripted:
    """Connecteur scripte pour les tests : rejoue des reponses depuis un JSON.
    Format : [{"comment": ..., "code": ...}, ...] servies dans l'ordre."""

    def __init__(self, path):
        with open(path) as f:
            self.responses = json.load(f)
        self.calls = []

    def ask(self, message):
        self.calls.append(message)
        if not self.responses:
            raise RuntimeError("plus de reponses scriptees")
        return self.responses.pop(0)


class EdenAI:
    """Connecteur OpenAI-compatible (EdenAI, cf. mail d'Adrian).
    Usage : -m edenai:deepseek/deepseek-v4-flash
    Cle API dans EDENAI_API_KEY. Les modeles n'ayant pas tous un mode JSON
    fiable, on demande du texte et on extrait le code des blocs ``` (meme
    technique que la classe Gemma de rag-gemini.py)."""

    BASE_URL = os.environ.get('EDENAI_BASE_URL', 'https://api.edenai.run/v3')

    def __init__(self, model):
        self.session = requests.Session()
        self.model = model
        self.session.headers.update(
            {'Authorization': f"Bearer {os.environ['EDENAI_API_KEY']}"})

    @staticmethod
    def _separate_code(text):
        """Separe commentaire et code (blocs ```)."""
        buckets = ([], [])
        current = 0
        for line in text.split('\n'):
            if line.startswith('```'):
                current = 1 - current
            else:
                buckets[current].append(line)
        return {'comment': '\n'.join(buckets[0]).strip(),
                'code': '\n'.join(buckets[1]).strip() + '\n'}

    def ask(self, message):
        answer = self.session.post(
            f'{self.BASE_URL}/chat/completions',
            json={'model': self.model,
                  'messages': [{'role': 'user', 'content': message}],
                  'temperature': 0.3},
            timeout=180,
        )
        if answer.status_code != 200:
            raise ValueError(f'API error: {answer.content}')
        text = answer.json()['choices'][0]['message']['content']
        rep = self._separate_code(text)
        if not rep['code'].strip():
            # pas de bloc ``` : tout le texte est peut-etre du code brut
            rep = {'comment': '', 'code': text.strip() + '\n'}
        return rep


def get_connector(name):
    if name.startswith('scripted:'):
        return Scripted(name.split(':', 1)[1])
    if name.startswith('edenai:'):
        return EdenAI(name.split(':', 1)[1])
    if name.startswith('gemini'):
        return Gemini(name)
    raise ValueError(f'modele inconnu : {name}')


# ---------------------------------------------------------------------------
# RAG configurable + exemplaire similaire
# ---------------------------------------------------------------------------

def charger_rag(rag_path):
    """Importe retrieve_maude_context depuis le RAG demande, ou None."""
    if rag_path in (None, 'none'):
        return None
    sys.path.insert(0, str((HERE / rag_path).resolve()))
    try:
        from rag.builder_code import retrieve_maude_context
        return retrieve_maude_context
    except Exception as e:
        print(f"RAG indisponible ({e}) - generation sans contexte manuel")
        return None


def _tokens_code(code):
    return set(re.findall(r"[A-Za-z][\w'-]*|:=|=>|~>|/\\", code))


def exemplaire_similaire(code, exclude, originals_dir=HERE / 'tests/original/maudec/maude'):
    """Programme original le plus proche (Jaccard sur tokens) comme few-shot.
    Volontairement simple et sans dependance ; un embedding ferait mieux,
    mais l'exemplaire n'a besoin que d'etre 'du meme genre'."""
    ref = _tokens_code(code)
    best, best_score = None, 0.0
    for f in sorted(originals_dir.glob('*.maude')):
        if f.name == exclude:
            continue
        toks = _tokens_code(f.read_text())
        score = len(ref & toks) / len(ref | toks) if ref | toks else 0
        if score > best_score:
            best, best_score = f, score
    return best


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

BASE = ('Please, simplify and improve the efficiency of the following Maude code '
        'while preserving the semantics. Keep the original function signatures, '
        'but change the implementation as needed.')

RAG_BLOCK = ('\n\nThe following excerpts from the Maude manual document the constructs '
             'used. Use them as the authoritative reference for Maude syntax. Do NOT '
             'introduce notation that does not appear in these excerpts or the '
             'original code.\n\nMAUDE MANUAL EXCERPTS:\n{context}')

EXAMPLE_BLOCK = ('\n\nHere is a complete, valid Maude program of a similar kind, as a '
                 'reference for correct Maude style and syntax (do not copy its '
                 'content, only its idioms):\n```\n{example}\n```')

REPAIR = ('Your previous Maude code was checked mechanically and REJECTED. '
          'Fix it. Do not apologize, return the corrected full program.\n'
          '\nYOUR PREVIOUS CODE:\n```\n{code}\n```\n'
          '\nWHAT THE CHECKER FOUND:\n{feedback}\n'
          '{rag_block}'
          '\nReminder: preserve the semantics and signatures of the original '
          'program:\n```\n{original}\n```\n'
          'If you cannot make an optimization work, prefer returning a minimal '
          'correct variant of the original over an incorrect optimization.')


def verifier(code, termes, reference):
    """Lint + compile + tests. Retourne (ok, feedback)."""
    issues = lint(code)
    problemes_fatals = fatals(issues)
    if problemes_fatals:
        return False, "Static check (linter):\n" + format_issues(problemes_fatals)

    loaded, results, stderr = evaluer(code, termes)
    if not loaded:
        fb = f"Maude failed to load the module. Parser output:\n{stderr or '(vide)'}"
        if issues:
            fb += "\n\nLinter warnings (possibly related):\n" + format_issues(issues)
        return False, fb

    echecs = []
    signature_changee = False
    for terme, attendu in reference.items():
        obtenu = results.get(terme)
        if obtenu != attendu:
            if obtenu is None:
                echecs.append(f'- term `{terme}` does NOT PARSE in your module, while the '
                              f'original computes `{attendu}`. You changed the declared '
                              f'operators or sorts. RESTORE the original signatures '
                              f'(same sort names, same operator syntax, same constructors).')
                signature_changee = True
            else:
                echecs.append(f'- term `{terme}` : expected `{attendu}`, got `{obtenu}`'
                              + (' (did not reduce - an equation probably does not match)'
                                 if terme.split("(")[0] in obtenu else ''))
        if len(echecs) >= 3:
            break
    if signature_changee:
        echecs.append('- REMINDER: the test terms use the original syntax; your module '
                      'must keep it. Do not re-parameterize or rename anything declared '
                      'in the original.')
    if echecs:
        fb = "The module loads, but differential tests FAILED:\n" + "\n".join(echecs)
        if issues:
            fb += "\n\nLinter warnings (check them, one may be the cause):\n" + format_issues(issues)
        return False, fb

    return True, None


# ---------------------------------------------------------------------------
# Boucle principale
# ---------------------------------------------------------------------------

def repair_loop(source: Path, model_name, rag_path, max_iters, use_example, seed, spec=None):
    random.seed(seed)   # memes termes de test a chaque iteration

    original = source.read_text()

    # tests depuis la spec TOML (meme convention que check.py)
    if spec is None:
        spec = HERE / 'inputs/spec/maudec/maude' / source.with_suffix('.toml').name
    with open(spec, 'rb') as f:
        tests = make_tests(tomllib.load(f), MaudeDriver())
    termes = [t.expr for t in tests]

    # reference : sorties du programme original
    loaded, reference, stderr = evaluer(original, termes)
    assert loaded, f"le programme ORIGINAL ne charge pas : {stderr[:500]}"

    # termes que l'original lui-meme ne parse pas : spec inutilisable pour eux
    # (cas reel : collatz.toml reference rlapp_Nat/arlapp_Nat, definis nulle part)
    invalides = [t for t, r in reference.items() if r is None]
    if invalides:
        if len(invalides) == len(termes):
            print(f"! {len(invalides)}/{len(termes)} termes de la spec ne parsent pas "
                  f"dans l'ORIGINAL (ex: {invalides[0]!r}) - verification limitee a la compilation")
        else:
            print(f"! {len(invalides)}/{len(termes)} termes de la spec ignores "
                  f"(ne parsent pas dans l'original)")
        reference = {t: r for t, r in reference.items() if r is not None}
        termes = list(reference)

    retrieve = charger_rag(rag_path)
    connector = get_connector(model_name)

    # --- prompt initial (identique a rag-gemini.py, + exemplaire optionnel) ---
    rag_block = RAG_BLOCK.format(context=retrieve(original)) if retrieve else ''
    example_block = ''
    if use_example:
        ex = exemplaire_similaire(original, exclude=source.name)
        if ex:
            example_block = EXAMPLE_BLOCK.format(example=ex.read_text())

    exemples_termes = ', '.join(f'`{t}`' for t in termes[:5])
    interface_block = (f'\n\nYour module MUST still parse and correctly reduce terms written '
                       f'in the original syntax, e.g.: {exemples_termes}. Keep every declared '
                       f'sort and operator unchanged.') if termes else ''
    message = f'{BASE}{rag_block}{example_block}{interface_block}\n```\n{original}\n```\n'

    trace = {'file': str(source), 'model': model_name, 'rag': rag_path,
             'n_tests': len(termes), 'iterations': []}

    response = connector.ask(message)
    for it in range(1, max_iters + 1):
        code, fixes = autofix(response['code'])
        ok, feedback = verifier(code, termes, reference)

        trace['iterations'].append({
            'iter': it, 'ok': ok, 'autofixes': fixes,
            'feedback': feedback[:2000] if feedback else None,
        })
        print(f"  iter {it}: {'OK' if ok else 'X'}"
              + (f" - {feedback.splitlines()[0][:90]}" if feedback else ""))

        if ok:
            trace['final'] = 'ok'
            return code, response.get('comment', ''), trace

        if it == max_iters:
            break

        # --- prompt de reparation ---
        rag_block = RAG_BLOCK.format(context=retrieve(code)) if retrieve else ''
        message = REPAIR.format(code=code, feedback=feedback,
                                rag_block=rag_block, original=original)
        response = connector.ask(message)

    trace['final'] = 'failed'
    return None, None, trace


def main():
    parser = argparse.ArgumentParser(description='Boucle compile-and-repair Maude')
    parser.add_argument('input', type=Path, help='Fichier .maude original')
    parser.add_argument('-m', '--model', default='gemini-2.5-flash',
                        help='gemini-* ou scripted:<fichier.json>')
    parser.add_argument('--rag', default='../rag-system',
                        help='chemin du RAG (../rag-system, ../maude-rag-hybrid, '
                             '../maude-rag-sections) ou none')
    parser.add_argument('--max-iters', type=int, default=3)
    parser.add_argument('--example', action='store_true',
                        help='ajoute le programme original le plus similaire en few-shot')
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--spec', type=Path, help='spec TOML (defaut : deduite du chemin)')
    parser.add_argument('-o', type=Path, help='fichier de sortie')
    parser.add_argument('--trace', type=Path, help='trace JSON de la session')
    args = parser.parse_args()

    code, comment, trace = repair_loop(args.input, args.model, args.rag,
                                       args.max_iters, args.example, args.seed,
                                       spec=args.spec)

    if args.trace:
        args.trace.write_text(json.dumps(trace, indent=1))

    if code is None:
        print(f"ECHEC apres {args.max_iters} iterations")
        sys.exit(1)

    output = args.o or args.input.with_stem(f'{args.input.stem}-repaired')
    with open(output, 'w') as out:
        out.write(f'***\n***\t<comment from="{args.model}" via="repair-loop">\n')
        for line in (comment or '').split('\n'):
            out.write(f'***\t{line}'.rstrip() + '\n')
        out.write('***\t</comment>\n***\n\n')
        out.write(code)
    print(f"ecrit dans {output} ({len(trace['iterations'])} iteration(s))")


if __name__ == '__main__':
    main()
