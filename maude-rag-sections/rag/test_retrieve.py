"""Verification rapide du retrieval sans appel LLM.
Usage : python -m rag.test_retrieve [fichier.maude]
Necessite la collection maude_manual du baseline (rag-system) deja indexee.
"""
import sys
from pathlib import Path

from rag.builder_code import retrieve_maude_context

if len(sys.argv) > 1:
    code = Path(sys.argv[1]).read_text()
else:
    code = """fmod PEANO is
  sort Nat .
  op 0 : -> Nat [ctor] .
  op s_ : Nat -> Nat [ctor] .
  op _+_ : Nat Nat -> Nat .
  vars N M : Nat .
  eq 0 + N = N .
  eq s(N) + M = s(N + M) .
endfm"""

print(retrieve_maude_context(code))
