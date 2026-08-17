"""Selection best-of-N : alternative a la boucle de reparation.

Genere N candidats (temperature du modele), verifie chacun LOCALEMENT
(linter + chargement + tests differentiels contre l'original + proprietes si
une spec existe), puis choisit parmi les candidats corrects le plus RAPIDE
(somme des temps de reduction des termes de test, via maude_eval_rw).

Meme infrastructure de verification que repair.py, autre strategie de
depense : N appels independants vs 1 appel + reparations. Le comparatif
boucle vs best-of-N est une des questions ouvertes du projet.

Usage :
    python best_of.py tests/original/maudec/maude/pow.maude -m gemini-2.5-flash -n 3
    python best_of.py <fichier> -m scripted:candidats.json -n 3 --rag none   # test
"""
import argparse
import json
import random
import sys
try:
    import tomllib
except ImportError:
    import tomli as tomllib
from pathlib import Path

# reutilise sans les modifier : connecteurs, RAG, prompts, linter
from repair import (get_connector, charger_rag, exemplaire_similaire,
                    BASE, RAG_BLOCK, EXAMPLE_BLOCK)
from linter import autofix, lint, fatals, format_issues
from local_eval import evaluer_rw
from check import make_tests, MaudeDriver
import props as props_mod

HERE = Path(__file__).parent


def verifier_candidat(code, termes, reference, props_spec, seed):
    """-> (ok, temps_total, details)"""
    issues = fatals(lint(code))
    if issues:
        return False, None, "linter : " + format_issues(issues).replace("\n", " ; ")

    loaded, results, times, stderr = evaluer_rw(code, termes)
    if not loaded:
        return False, None, f"chargement : {(stderr or '?')[:200]}"

    for terme, attendu in reference.items():
        if results.get(terme) != attendu:
            return False, None, f"diff : `{terme}` -> `{results.get(terme)}` (attendu `{attendu}`)"

    if props_spec and props_spec.is_file():
        ok, echecs = props_mod.verifier_proprietes(code, props_spec, seed=seed)
        if not ok:
            return False, None, "propriete : " + echecs[0][:200]

    return True, sum(times.get(t, 0.0) for t in reference), None


def best_of(source: Path, model_name, rag_path, n, max_var, seed, spec=None, use_example=False):
    random.seed(seed)
    original = source.read_text()

    if spec is None:
        spec = HERE / 'inputs/spec/maudec/maude' / source.with_suffix('.toml').name
    with open(spec, 'rb') as f:
        tests = make_tests(tomllib.load(f), MaudeDriver())
    termes = [t.expr for t in tests]

    loaded, reference, ref_times, stderr = evaluer_rw(original, termes)
    assert loaded, f"l'ORIGINAL ne charge pas : {stderr[:300]}"
    reference = {t: r for t, r in reference.items() if r is not None}
    termes = list(reference)
    temps_original = sum(ref_times.get(t, 0.0) for t in reference)

    retrieve = charger_rag(rag_path)
    connector = get_connector(model_name)
    props_spec = props_mod.spec_pour(source)

    rag_block = RAG_BLOCK.format(context=retrieve(original)) if retrieve else ''
    example_block = ''
    if use_example:
        ex = exemplaire_similaire(original, exclude=source.name)
        if ex:
            example_block = EXAMPLE_BLOCK.format(example=ex.read_text())
    message = f'{BASE}{rag_block}{example_block}\n```\n{original}\n```\n'

    rapport = {'file': str(source), 'model': model_name, 'rag': rag_path, 'n': n,
               'temps_original': temps_original, 'candidats': []}

    meilleurs = []
    for k in range(n):
        try:
            response = connector.ask(message)
        except Exception as e:
            rapport['candidats'].append({'k': k, 'ok': False, 'raison': f'API : {e}'})
            continue
        code, fixes = autofix(response['code'])
        ok, temps, raison = verifier_candidat(code, termes, reference, props_spec, seed)
        rapport['candidats'].append({'k': k, 'ok': ok, 'temps': temps,
                                     'raison': raison, 'autofixes': fixes})
        print(f"  candidat {k}: {'OK' if ok else 'X'}"
              + (f" (temps={temps:.4f}s)" if ok else f" - {raison[:80]}"))
        if ok:
            meilleurs.append((temps, k, code, response.get('comment', '')))

    if not meilleurs:
        rapport['choix'] = None
        return None, None, rapport

    meilleurs.sort(key=lambda x: x[0])
    temps, k, code, comment = meilleurs[0]
    rapport['choix'] = {'k': k, 'temps': temps,
                        'speedup_vs_original': (temps_original / temps) if temps else None}
    return code, comment, rapport


def main():
    ap = argparse.ArgumentParser(description='Best-of-N pour code Maude')
    ap.add_argument('input', type=Path)
    ap.add_argument('-m', '--model', default='gemini-2.5-flash')
    ap.add_argument('-n', type=int, default=3)
    ap.add_argument('--rag', default='../rag-system')
    ap.add_argument('--example', action='store_true')
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--spec', type=Path)
    ap.add_argument('-o', type=Path)
    ap.add_argument('--rapport', type=Path)
    args = ap.parse_args()

    code, comment, rapport = best_of(args.input, args.model, args.rag, args.n,
                                     None, args.seed, spec=args.spec,
                                     use_example=args.example)
    if args.rapport:
        args.rapport.write_text(json.dumps(rapport, indent=1))

    if code is None:
        print(f"ECHEC : aucun des {args.n} candidats ne passe")
        sys.exit(1)

    output = args.o or args.input.with_stem(f'{args.input.stem}-bestof')
    with open(output, 'w') as out:
        out.write(f'***\n***\t<comment from="{args.model}" via="best-of-{args.n}">\n')
        for line in (comment or '').split('\n'):
            out.write(f'***\t{line}'.rstrip() + '\n')
        out.write('***\t</comment>\n***\n\n')
        out.write(code)
    ch = rapport['choix']
    print(f"choisi : candidat {ch['k']} (temps {ch['temps']:.4f}s, "
          f"speedup x{ch['speedup_vs_original']:.2f} vs original) -> {output}")


if __name__ == '__main__':
    main()
