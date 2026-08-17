# maude-rag-hybrid — variante "hybride natif Qdrant"

Variante du RAG Maude (`rag-system`) pour comparaison. **Une seule variable
change** : la methode de ranking. Corpus, chunking, embeddings dense et
expansions de contexte sont identiques au baseline.

| | baseline (`rag-system`) | cette variante |
|---|---|---|
| lexical | scan Python du corpus entier, symboles x10 | BM25 sparse, IDF serveur |
| fusion | conditionnelle (lexical d'abord si symboles) | RRF cote serveur |
| symboles `:=` `~>` ... | substring match direct | tokens sentinelles (`symassign`...) proteges avant BM25 |
| latence | O(corpus) par requete | O(log n), index sparse |

Le pari teste : BM25+RRF est l'etat de l'art standard — fait-il mieux que
l'heuristique maison calibree sur le domaine ? Pas gagne d'avance : la fusion
conditionnelle du baseline est une forme de connaissance du domaine que RRF
ne possede pas.

## Installation / indexation

```bash
pip install -r requirements.txt   # ajoute fastembed (telecharge Qdrant/bm25 au 1er run)
cp ../rag-system/.env .env        # ou creer avec GEMINI_API_KEY
python -m indexation.index_html   # collection maude_manual_hybrid (~5 min)
python -m rag.test_retrieve       # verif retrieval sans LLM
```

## Branchement dans improvement/

Dans `improvement/rag-gemini.py`, remplacer la ligne 6 :

```python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'maude-rag-hybrid'))
```

`retrieve_maude_context(code)` a la meme signature et le meme format de
sortie que le baseline. Un seul RAG a la fois dans le path (les paquets
s'appellent tous `rag`).
