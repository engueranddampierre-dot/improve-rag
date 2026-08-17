"""Evaluateur Maude isole, lance en sous-processus par repair.py.

Usage : python maude_eval.py <fichier.maude> <termes.json>
Sortie stdout : JSON {"loaded": bool, "module": str|null, "results": {terme: str|null}}
Les erreurs/warnings du parseur Maude partent sur stderr (captures par le parent).
Processus separe : un fichier pathologique ne tue pas la boucle de reparation.
"""
import json
import sys


def main():
    fichier, termes_json = sys.argv[1], sys.argv[2]
    with open(termes_json) as f:
        termes = json.load(f)

    import maude
    maude.init()
    maude.load(fichier)
    m = maude.getCurrentModule()

    # separe les warnings du CHARGEMENT de ceux du parsing des termes :
    # seuls les premiers signifient que le module est invalide
    print("===TERMES===", file=sys.stderr, flush=True)

    if m is None:
        print(json.dumps({"loaded": False, "module": None, "results": {}}))
        return

    results = {}
    for terme in termes:
        t = m.parseTerm(terme)
        if t is None:
            results[terme] = None
        else:
            t.reduce()
            results[terme] = t.prettyPrint(0)

    print(json.dumps({"loaded": True, "module": str(m), "results": results}))


if __name__ == "__main__":
    main()
