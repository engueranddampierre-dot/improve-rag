"""Tests de proprietes (metamorphiques) pour programmes Maude.

Complement des tests par points de check.py : au lieu de comparer le candidat
a l'original terme par terme, on verifie des identites ALGEBRIQUES internes
au candidat, instanciees sur des valeurs aleatoires. Exemple (free-tuples) :
first(h(F1, B1, F2, B2)) == F1 pour TOUTES les combinaisons — c'est
exactement ce que le bug reel du pattern non-lineaire violait (il ne matchait
que si B1 == B2), et que 25 points aleatoires sur une seule expression
pouvaient rater.

Specs : inputs/props/maudec/maude/<nom>.toml
    [[prop]]
    name  = "first_h"
    left  = "first(h({F1}, {B1}, {F2}, {B2}))"
    right = "{F1}"
    count = 8                     # instances aleatoires (defaut 10)
    [prop.vars]
    F1 = "float"
    B1 = "bool"
    F2 = "float"
    B2 = "bool"

Usage : python props.py <fichier.maude> [--spec ...] [--seed 0] [-v]
Sortie : code retour 0 si toutes les proprietes passent.
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

from local_eval import evaluer_rw

HERE = Path(__file__).parent


def valeur(ty, rng):
    match ty:
        case 'nat':   return str(rng.randint(0, 12))
        case 'int':   return str(rng.randint(-12, 12))
        case 'bool':  return rng.choice(['true', 'false'])
        case 'float': return f"{rng.uniform(-50, 50):.1f}"
        case _:       raise ValueError(f'type inconnu : {ty}')


def instances(prop, rng):
    """Genere les paires (gauche, droite) instanciees."""
    n = prop.get('count', 10)
    vars_ = prop.get('vars', {})
    for _ in range(n):
        subst = {k: valeur(t, rng) for k, t in vars_.items()}
        yield prop['left'].format(**subst), prop['right'].format(**subst)


def verifier_proprietes(code, spec_path, seed=0):
    """-> (ok, echecs) ; echecs = liste de messages."""
    with open(spec_path, 'rb') as f:
        spec = tomllib.load(f)
    rng = random.Random(seed)

    paires, appartient = [], []
    for prop in spec.get('prop', ()):
        for g, d in instances(prop, rng):
            paires.append((g, d))
            appartient.append(prop.get('name', '?'))

    termes = sorted({t for paire in paires for t in paire})
    loaded, results, _, stderr = evaluer_rw(code, termes)
    if not loaded:
        return False, [f'le module ne charge pas : {stderr[:300]}']

    echecs = []
    for (g, d), nom in zip(paires, appartient):
        rg, rd = results.get(g), results.get(d)
        if rg is None or rd is None or rg != rd:
            echecs.append(f'propriete `{nom}` violee : `{g}` -> `{rg}` mais `{d}` -> `{rd}`')
        if len(echecs) >= 5:
            break
    return not echecs, echecs


def spec_pour(source: Path):
    return HERE / 'inputs/props/maudec/maude' / source.with_suffix('.toml').name


def main():
    ap = argparse.ArgumentParser(description='Tests de proprietes Maude')
    ap.add_argument('input', type=Path)
    ap.add_argument('--spec', type=Path)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('-v', action='store_true')
    args = ap.parse_args()

    spec = args.spec or spec_pour(args.input)
    if not spec.is_file():
        print(f'pas de spec de proprietes : {spec}')
        sys.exit(2)

    ok, echecs = verifier_proprietes(args.input.read_text(), spec, seed=args.seed)
    if ok:
        print(f'OK — proprietes respectees ({args.input.name})')
    else:
        print(f'ECHEC ({args.input.name}) :')
        for e in echecs:
            print(' ', e)
        sys.exit(1)


if __name__ == '__main__':
    main()
