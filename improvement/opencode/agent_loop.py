"""Boucle "Ralph Wiggum" autour d'OpenCode (cf. mail de Juan) : l'agent lit
la spec et les erreurs de test dans des fichiers, genere le programme, notre
evaluateur Maude regenere le fichier d'erreurs, et on recommence jusqu'a
zero erreur ou --max-turns.

NON TESTE : ce script exige opencode installe et connecte (EdenAI), le
reseau, et Maude en local. Premiere execution a faire a la main, tour par
tour, avec -v.

Difference avec ../generate.py : ici le retrieval est TIRE par l'agent (il
interroge le serveur MCP qdrant-maude quand il le juge utile) au lieu d'etre
pousse dans le prompt. Comparer les deux sur les memes specs est l'un des
objectifs.

Usage :
    python agent_loop.py ../specs/maudec/maude/pow.txt \
        --model edenai/deepseek/deepseek-v4-flash --max-turns 4 -v
"""
import argparse
import json
import random
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
IMPROVEMENT = HERE.parent
sys.path.insert(0, str(IMPROVEMENT))

try:
    import tomllib
except ImportError:
    import tomli as tomllib

from repair import evaluer, verifier          # noqa: E402
from linter import autofix                     # noqa: E402
from check import make_tests, MaudeDriver      # noqa: E402

PROMPT_TURN = """Read the specification in {spec_file} and the current test
errors in {errors_file} (empty file = first attempt, no errors yet).

Write a complete Maude program satisfying the specification into
{output_file} (overwrite it entirely). The required interface in the
specification must be respected exactly. You can query the qdrant-maude
tool to look up Maude syntax in the reference manual. Do not modify any
other file."""


def extraire_code(path: Path):
    """Le fichier ecrit par l'agent, nettoye des eventuels blocs ```."""
    txt = path.read_text()
    if '```' in txt:
        lignes, dedans, code = txt.split('\n'), False, []
        for l in lignes:
            if l.startswith('```'):
                dedans = not dedans
            elif dedans:
                code.append(l)
        if code:
            return '\n'.join(code) + '\n'
    return txt


def main():
    ap = argparse.ArgumentParser(description='Boucle agent OpenCode + verification Maude')
    ap.add_argument('spec', type=Path)
    ap.add_argument('--model', default='edenai/deepseek/deepseek-v4-flash')
    ap.add_argument('--max-turns', type=int, default=4)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--workdir', type=Path, default=Path('agent-work'))
    ap.add_argument('-v', action='store_true')
    args = ap.parse_args()

    random.seed(args.seed)
    nom = args.spec.stem
    wd = args.workdir; wd.mkdir(exist_ok=True)
    spec_file = wd / f'{nom}-spec.txt'
    errors_file = wd / f'{nom}-errors.txt'
    output_file = wd / f'{nom}.maude'
    spec_file.write_text(args.spec.read_text())
    errors_file.write_text('')
    output_file.write_text('')

    # oracle (jamais montre a l'agent) + termes de test
    reference = IMPROVEMENT / 'tests/original/maudec/maude' / f'{nom}.maude'
    with open(IMPROVEMENT / 'inputs/spec/maudec/maude' / f'{nom}.toml', 'rb') as f:
        tests = make_tests(tomllib.load(f), MaudeDriver())
    termes = [t.expr for t in tests]
    loaded, oracle, stderr = evaluer(reference.read_text(), termes)
    assert loaded, f'reference invalide : {stderr[:300]}'
    oracle = {t: r for t, r in oracle.items() if r is not None}
    termes = list(oracle)

    prompt = PROMPT_TURN.format(spec_file=spec_file, errors_file=errors_file,
                                output_file=output_file)

    for turn in range(1, args.max_turns + 1):
        print(f'--- tour {turn} : opencode run ---')
        ret = subprocess.run(
            ['opencode', 'run', '--model', args.model, prompt],
            capture_output=True, text=True, timeout=600,
        )
        if args.v:
            print(ret.stdout[-2000:])
            if ret.returncode != 0:
                print('STDERR:', ret.stderr[-1000:])

        code = extraire_code(output_file)
        if not code.strip():
            errors_file.write_text('You did not write any program into the output file.')
            continue

        code, _ = autofix(code)
        ok, feedback = verifier(code, termes, oracle)
        if ok:
            print(f'OK au tour {turn} -> {output_file}')
            return
        errors_file.write_text(feedback)
        print(f'  X : {feedback.splitlines()[0][:90]}')

    print(f'ECHEC apres {args.max_turns} tours (erreurs dans {errors_file})')
    sys.exit(1)


if __name__ == '__main__':
    main()
