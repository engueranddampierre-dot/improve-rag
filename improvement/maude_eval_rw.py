"""Evaluateur Maude etendu (nouveau fichier — maude_eval.py reste intact).

Ajouts par rapport a maude_eval.py :
- convention rlapp/arlapp pour tester les REGLES de reecriture :
    rlapp_<Sort>(t)  -> resultat de UNE reecriture (t.rewrite(1)), strategie
                        par defaut de Maude, deterministe
    arlapp_<Sort>(t) -> ensemble TRIE de tous les successeurs a un pas
                        (search =>1 avec le motif X:<Sort>), independant de
                        l'ordre des regles
  NB : c'est une INTERPRETATION de la convention esquissee par collatz.toml
  (rlapp_Nat / arlapp_Nat, jamais implementee dans check.py) ; elle rend les
  modules a regles comparables entre original et candidat.
- chronometrage de chaque terme (pour le classement best-of-N)

Usage : python maude_eval_rw.py <fichier.maude> <termes.json>
Sortie : {"loaded": bool, "module": str|null, "results": {...}, "times": {...}}
"""
import json
import re
import sys
import time

RLAPP = re.compile(r'^(a?)rlapp_(\w+)\((.*)\)$', re.DOTALL)


def main():
    fichier, termes_json = sys.argv[1], sys.argv[2]
    with open(termes_json) as f:
        termes = json.load(f)

    import maude
    maude.init()
    maude.load(fichier)
    m = maude.getCurrentModule()

    print("===TERMES===", file=sys.stderr, flush=True)

    if m is None:
        print(json.dumps({"loaded": False, "module": None, "results": {}, "times": {}}))
        return

    results, times = {}, {}
    for terme in termes:
        debut = time.perf_counter()
        mrl = RLAPP.match(terme.strip())
        try:
            if mrl:
                tous, sorte, inner = mrl.group(1) == 'a', mrl.group(2), mrl.group(3)
                t = m.parseTerm(inner)
                if t is None:
                    results[terme] = None
                elif tous:
                    pat = m.parseTerm(f'X:{sorte}')
                    if pat is None:
                        results[terme] = None
                    else:
                        succ = set()
                        for sol in t.search(maude.ONE_STEP, pat):
                            succ.add(sol[0].prettyPrint(0))
                            if len(succ) >= 64:     # garde-fou
                                break
                        results[terme] = "{ " + ", ".join(sorted(succ)) + " }"
                else:
                    t.rewrite(1)
                    results[terme] = t.prettyPrint(0)
            else:
                t = m.parseTerm(terme)
                if t is None:
                    results[terme] = None
                else:
                    t.reduce()
                    results[terme] = t.prettyPrint(0)
        except Exception as e:
            results[terme] = None
        times[terme] = time.perf_counter() - debut

    print(json.dumps({"loaded": True, "module": str(m), "results": results, "times": times}))


if __name__ == "__main__":
    main()
