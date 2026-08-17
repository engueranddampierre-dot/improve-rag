"""Generation de code Maude depuis une specification en langage naturel,
avec verification locale et boucle de reparation.

Reutilise :
- le prompt anti-hallucination de rag-system/rag/code_gemini.py (concept =
  connaissance generale, syntaxe Maude = extraits du manuel uniquement) ;
- la mecanique de repair.py : connecteurs (Gemini, EdenAI, scripted), RAG
  configurable, linter+autofix, evaluateur Maude isole, tests differentiels.

Le programme de REFERENCE (tests/original) sert uniquement d'oracle pour le
differential testing : il n'est JAMAIS montre au modele. La spec inclut la
signature exacte des operateurs, sans quoi les termes de test ne peuvent pas
parser (lecon de simple-list).

Usage :
    python generate.py specs/maudec/maude/pow.txt -m edenai:deepseek/deepseek-v4-flash
    python generate.py specs/maudec/maude/pow.txt -m scripted:reponses.json --rag none
"""
import argparse
import json
import random
import sys
try:
    import tomllib
except ImportError:                      # Python < 3.11
    import tomli as tomllib
from pathlib import Path

from linter import autofix
from repair import evaluer, verifier, charger_rag, get_connector
from check import make_tests, MaudeDriver

HERE = Path(__file__).parent


# ---------------------------------------------------------------------------
# Prompts (adaptes de rag-system/rag/code_gemini.py)
# ---------------------------------------------------------------------------

GEN_PROMPT = """You are an expert Maude programmer. Your task is to write a complete,
self-contained Maude program implementing the specification below.

You have two distinct sources of knowledge, and you MUST keep them separate:

1. GENERAL KNOWLEDGE (your own): use this ONLY to understand WHAT the
   specification asks for — the mathematical or computational concept itself.

2. THE MAUDE MANUAL EXCERPTS (when provided below): your ONLY authority for
   HOW to write it in Maude — the syntax, the keywords (fmod, mod, op, eq,
   ceq, rl, sort, subsort, ...), operator declaration conventions, and the
   attributes ([ctor], assoc, comm, id:, owise, frozen, ...).

STRICT RULES:
- Do NOT invent operators, attributes, keywords, or notation that do not
  appear in the excerpts or in the specification.
- Do NOT borrow syntax from other languages (no Haskell, ML, or generic
  functional notation).
- Respect the required interface EXACTLY: same operator names, same
  argument sorts, same notation. The test terms below must parse.
- Output the complete program, nothing else.
{rag_block}
SPECIFICATION:
{spec}

Your program MUST parse and correctly reduce terms of this exact form:
{exemples}

Write the Maude program now."""

RAG_BLOCK = """
MAUDE MANUAL EXCERPTS:
{context}
"""

GEN_REPAIR = """Your previous Maude program was checked mechanically against the
specification and REJECTED. Fix it. Do not apologize, return the corrected
full program.

THE SPECIFICATION (unchanged):
{spec}

YOUR PREVIOUS PROGRAM:
```
{code}
```

WHAT THE CHECKER FOUND:
{feedback}
{rag_block}
Remember: the required interface (operator names, sorts, notation) is part
of the specification and must be respected exactly."""


# ---------------------------------------------------------------------------
# Boucle de generation
# ---------------------------------------------------------------------------

def gen_loop(spec_path: Path, model_name, rag_path, max_iters, seed,
             reference=None, spec_toml=None):
    random.seed(seed)   # memes termes de test a chaque iteration

    spec = spec_path.read_text()
    nom = spec_path.stem

    # oracle : le programme de reference (jamais montre au modele)
    if reference is None:
        reference = HERE / 'tests/original/maudec/maude' / f'{nom}.maude'
    code_ref = Path(reference).read_text()

    if spec_toml is None:
        spec_toml = HERE / 'inputs/spec/maudec/maude' / f'{nom}.toml'
    with open(spec_toml, 'rb') as f:
        tests = make_tests(tomllib.load(f), MaudeDriver())
    termes = [t.expr for t in tests]

    loaded, oracle, stderr = evaluer(code_ref, termes)
    assert loaded, f"la REFERENCE ne charge pas : {stderr[:400]}"
    invalides = [t for t, r in oracle.items() if r is None]
    if invalides:
        print(f"! {len(invalides)}/{len(termes)} termes de la spec TOML ignores "
              f"(ne parsent pas dans la reference)")
        oracle = {t: r for t, r in oracle.items() if r is not None}
        termes = list(oracle)

    retrieve = charger_rag(rag_path)
    connector = get_connector(model_name)

    # requete RAG = la spec elle-meme (semantique) ; les builders acceptent
    # n'importe quel texte comme "code"
    rag_block = RAG_BLOCK.format(context=retrieve(spec)) if retrieve else ''
    exemples = ', '.join(f'`{t}`' for t in termes[:6]) or '(aucun)'

    message = GEN_PROMPT.format(rag_block=rag_block, spec=spec, exemples=exemples)

    trace = {'spec': str(spec_path), 'model': model_name, 'rag': rag_path,
             'n_tests': len(termes), 'iterations': []}

    response = connector.ask(message)
    for it in range(1, max_iters + 1):
        code, fixes = autofix(response['code'])
        ok, feedback = verifier(code, termes, oracle)

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

        rag_block = RAG_BLOCK.format(context=retrieve(code)) if retrieve else ''
        message = GEN_REPAIR.format(spec=spec, code=code, feedback=feedback,
                                    rag_block=rag_block)
        response = connector.ask(message)

    trace['final'] = 'failed'
    return None, None, trace


def main():
    parser = argparse.ArgumentParser(description='Generation Maude depuis spec NL')
    parser.add_argument('input', type=Path, help='Fichier spec .txt (specs/maudec/maude/x.txt)')
    parser.add_argument('-m', '--model', default='gemini-2.5-flash',
                        help='gemini-*, edenai:<provider/model>, scripted:<json>')
    parser.add_argument('--rag', default='../rag-system',
                        help='../rag-system | ../maude-rag-hybrid | ../maude-rag-sections | none')
    parser.add_argument('--max-iters', type=int, default=3)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--reference', type=Path, help='programme oracle (defaut : tests/original)')
    parser.add_argument('--spec-toml', type=Path, help='tests TOML (defaut : inputs/spec)')
    parser.add_argument('-o', type=Path, help='fichier de sortie')
    parser.add_argument('--trace', type=Path, help='trace JSON')
    args = parser.parse_args()

    code, comment, trace = gen_loop(args.input, args.model, args.rag,
                                    args.max_iters, args.seed,
                                    reference=args.reference,
                                    spec_toml=args.spec_toml)
    if args.trace:
        args.trace.write_text(json.dumps(trace, indent=1))

    if code is None:
        print(f"ECHEC apres {args.max_iters} iterations")
        sys.exit(1)

    output = args.o or args.input.with_suffix('.maude')
    with open(output, 'w') as out:
        out.write(f'***\n***\t<comment from="{args.model}" via="generate-loop">\n')
        for line in (comment or '').split('\n'):
            out.write(f'***\t{line}'.rstrip() + '\n')
        out.write('***\t</comment>\n***\n\n')
        out.write(code)
    print(f"ecrit dans {output} ({len(trace['iterations'])} iteration(s))")


if __name__ == '__main__':
    main()
