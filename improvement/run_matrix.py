"""Orchestrateur de la matrice de comparaison RAG x methode x modele.

Enchaine repair.repair_loop sur un ensemble de fichiers pour chaque
configuration, agrege les traces et imprime un tableau comparatif.
N'ecrit RIEN dans tests/ : les sorties vont dans un dossier dedie.

Configuration : un JSON, liste d'objets
    [{"label": "baseline+boucle", "rag": "../rag-system",
      "model": "gemini-2.5-flash", "max_iters": 3, "example": false},
     {"label": "baseline-sans-boucle", "rag": "../rag-system",
      "model": "gemini-2.5-flash", "max_iters": 1}]
max_iters = 1 <=> pas de boucle (une seule generation, verdict sec).

Modele special "echo" : renvoie l'original tel quel (aucun appel API) —
verifie la mecanique de la matrice et que chaque original passe ses
propres tests. Utile avant de payer de vrais tokens.

Usage :
    python run_matrix.py --config matrix.json -o results-matrix.json
    python run_matrix.py --config matrix.json --files "tests/original/maudec/maude/p*.maude"
"""
import argparse
import json
import tempfile
import time
import traceback
from pathlib import Path

import repair

HERE = Path(__file__).parent


def connecteur_pour(cfg, original, max_iters, tmpdir):
    """Nom de modele a passer a repair_loop ; 'echo' devient un scripted
    qui renvoie l'original a chaque tour."""
    model = cfg['model']
    if model != 'echo':
        return model
    p = Path(tmpdir) / f"echo-{time.time_ns()}.json"
    p.write_text(json.dumps([{'comment': 'echo', 'code': original}] * max_iters))
    return f'scripted:{p}'


def run(config_path, files_glob, out_path, outdir):
    with open(config_path) as f:
        configs = json.load(f)

    fichiers = sorted(HERE.glob(files_glob))
    assert fichiers, f'aucun fichier ne correspond a {files_glob}'
    outdir.mkdir(parents=True, exist_ok=True)

    resultats = {}
    with tempfile.TemporaryDirectory() as tmpdir:
        for cfg in configs:
            label = cfg['label']
            max_iters = cfg.get('max_iters', 3)
            print(f"=== {label} (rag={cfg.get('rag', 'none')}, model={cfg['model']}, "
                  f"iters<={max_iters}) ===")
            entree = resultats[label] = {'config': cfg, 'files': {}}

            for f in fichiers:
                original = f.read_text()
                model = connecteur_pour(cfg, original, max_iters, tmpdir)
                try:
                    code, comment, trace = repair.repair_loop(
                        f, model, cfg.get('rag', 'none'), max_iters,
                        cfg.get('example', False), cfg.get('seed', 0),
                    )
                    ok = trace['final'] == 'ok'
                    iters = len(trace['iterations'])
                    entree['files'][f.name] = {'ok': ok, 'iterations': iters,
                                               'trace': trace['iterations']}
                    if ok and code is not None:
                        dest = outdir / label.replace(' ', '_') / f.name
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        dest.write_text(code)
                    print(f"  {'OK' if ok else 'X '} {f.name} ({iters} iter)")
                except Exception as e:
                    entree['files'][f.name] = {'ok': False, 'erreur': str(e)}
                    print(f"  !! {f.name} : {e}")
                    if '--debug' in str(e):
                        traceback.print_exc()

    # --- tableau recapitulatif ---
    print()
    print(f"{'configuration':<28} {'reussite':>10} {'iters moy.':>10}")
    print('-' * 52)
    for label, entree in resultats.items():
        fs = entree['files']
        n_ok = sum(1 for v in fs.values() if v.get('ok'))
        iters = [v['iterations'] for v in fs.values() if 'iterations' in v]
        moy = sum(iters) / len(iters) if iters else float('nan')
        print(f"{label:<28} {n_ok:>4}/{len(fs):<5} {moy:>10.2f}")

    with open(out_path, 'w') as out:
        json.dump(resultats, out, indent=1)
    print(f"\ndetails -> {out_path}, codes acceptes -> {outdir}/")


def main():
    ap = argparse.ArgumentParser(description='Matrice de comparaison RAG/methodes')
    ap.add_argument('--config', type=Path, required=True)
    ap.add_argument('--files', default='tests/original/maudec/maude/*.maude')
    ap.add_argument('-o', type=Path, default=Path('results-matrix.json'))
    ap.add_argument('--outdir', type=Path, default=Path('matrix-out'))
    args = ap.parse_args()
    run(args.config, args.files, args.o, args.outdir)


if __name__ == '__main__':
    main()
