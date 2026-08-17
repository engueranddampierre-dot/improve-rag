# maude-rag-sections — variante "parent-section"

Variante du RAG Maude (`rag-system`) pour comparaison. **Une seule variable
change** : l'assemblage du contexte. La recherche hybride (semantique +
lexicale ponderee x10) est une copie conforme du baseline, et la collection
`maude_manual` du baseline est reutilisee telle quelle — **aucune
re-indexation necessaire**.

| | baseline (`rag-system`) | cette variante |
|---|---|---|
| contexte | fragments : voisins ±2, prose-de-code, modules de la section | sections ENTIERES des meilleurs hits, ordre du manuel |
| taille | variable, non plafonnee | budget global 3000 tokens, sections completes uniquement |
| filtres | sessions `Maude>`, LaTeX (sur les modules ajoutes) | memes filtres, appliques a toute la section |

Le pari teste : pour ameliorer du code, une section coherente et complete
(la prose ET tous ses exemples, dans l'ordre pedagogique du manuel) sert plus
au LLM que des fragments choisis par heuristiques. Cout : contexte plus long,
donc plus cher et potentiellement plus dilue — c'est exactement ce que la
comparaison doit trancher.

## Installation

Rien a indexer. Memes dependances que `rag-system`, collection `maude_manual`
deja en place. Verification :

```bash
python -m rag.test_retrieve       # depuis maude-rag-sections/
```

## Branchement dans improvement/

Dans `improvement/rag-gemini.py`, remplacer la ligne 6 :

```python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'maude-rag-sections'))
```

## Protocole de comparaison suggere (3 systemes)

1. Meme jeu de fichiers `.maude` d'entree pour les trois RAG
   (baseline, hybrid, sections), meme modele, meme temperature.
2. Mesures via ton harnais existant : compilation (`results-compile`),
   equivalence semantique (`results-diff`), benchs (`results-bench`).
3. Ajouter le cout : nombre de tokens de contexte par requete (les sections
   entieres en consomment plus — l'efficacite se juge a resultat/cout).
4. Au moins ~20 fichiers de test : sur 5 cas, le bruit domine.
