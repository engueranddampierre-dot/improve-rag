import maude
maude.init()

from pathlib import Path

dossier = Path(__file__).parent          # le dossier où est test_code.py
chemin = dossier / "peano_gemini.txt"

with open(chemin, "r", encoding="utf-8") as f:
    code = f.read()

maude.input(code)
mod = maude.getModule("PEANO-INTEGERS")   # le vrai nom du module de Gemini
print("Échec" if mod is None else f"Chargé : {mod}")

mod = maude.getModule("PEANO-INTEGERS")
t = mod.parseTerm("(s 0) + (s 0)")   # devrait donner int(s s 0, 0), soit "2"
t.reduce()
print(t)
t2 = mod.parseTerm("- (s 0)")        # devrait donner int(0, s 0), soit "-1"
t2.reduce()
print(t2)