# qdrant-rag — RAG sur la documentation Qdrant

Meme architecture que `rag-system` (RAG Maude), adaptee a la doc officielle
Qdrant (https://qdrant.tech/documentation/).

## Pipeline

1. **Indexation** (`indexation/index_html.py`)
   - decouverte des pages via `sitemap.xml` (filtre `/documentation/`, la doc bouge souvent)
   - extraction HTML scopee sur `<article>` (site Hugo), nav/footer ecartes
   - separation prose / blocs de code ; les blocs portent un champ `lang`
     (`python`, `http`, `bash`, ...) car chaque exemple existe en ~5 langages
   - listes `<li>` et tableaux inclus dans la prose (la doc Qdrant en est pleine)
   - chunks < 200 tokens avec chevauchement, embeddings `all-MiniLM-L6-v2` (384 dim)
   - collection `qdrant_docs`, ids consecutifs = ordre de lecture

2. **Recherche hybride** (`rag/builder_ask.py`, `rag/builder_code.py`)
   - semantique (vecteurs) + lexicale ; un match "special" vaut 10x un mot normal
   - "special" adapte au domaine : parametres snake_case (`ef_construct`),
     routes REST (`/collections/{name}/points`), symboles — l'equivalent des
     `:=` du RAG Maude
   - expansion de contexte par section (voisins, prose-de-code)
   - `expand_section_snippets` : equivalent de `expand_section_modules`, mais
     filtre par langage prefere (sinon les 5 variantes de chaque exemple
     saturent le prompt)

3. **Generation** (`rag/ask_gemini.py`, `rag/code_gemini.py`)
   - mode "ask" : repond uniquement depuis les extraits, refus explicite sinon
   - mode "code" : concept = connaissance generale, API Qdrant = extraits
     uniquement (meme discipline anti-hallucination que pour Maude)

## Installation

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
cp .env.example .env   # renseigner GEMINI_API_KEY
sudo docker start qdrant
```

## Usage

```bash
python -m indexation.index_html     # depuis qdrant-rag/ (une fois, ~10 min)
python -m rag.test_retrieve "How do I filter by payload?"   # retrieval seul
python -m rag.ask_gemini            # questions
python -m rag.code_gemini           # generation de code
```

## Sources d'enrichissement possibles

- **API Reference OpenAPI** : https://api.qdrant.tech est genere depuis la spec
  OpenAPI (`qdrant/qdrant` sur GitHub, `docs/redoc/master/openapi.json`).
  L'indexer donnerait la liste exhaustive des parametres avec types et
  defauts — exactement ce que le mode "code" exige. C'est la source la plus
  rentable a ajouter.
- **Docstrings du client Python** : le paquet `qdrant-client` lui-meme
  (`help(QdrantClient.query_points)`), extractibles par introspection.
  Elimine le decalage doc web / version reelle installee.
- **Depot d'exemples** : `qdrant/examples` et `qdrant/qdrant_demo` sur GitHub —
  du code complet qui marche, la ou la doc ne donne que des fragments.
- **FAQ + articles techniques du blog Qdrant** (qdrant.tech/articles/) : bonnes
  reponses "pourquoi" (choix de quantization, tuning HNSW) absentes du manuel.

## Idees d'amelioration (valables aussi pour rag-system)

- **Filtrage par langage au retrieval** : le champ `lang` est indexe mais la
  recherche semantique ne filtre pas encore dessus ; un `Filter` Qdrant sur
  `lang in (python, http)` reduirait le bruit avant meme la fusion.
- **Ironie utile : utiliser les features de Qdrant documentees ici.** Le score
  lexical actuel re-scanne tout le corpus en Python a chaque requete
  (herite du RAG Maude). Qdrant sait faire ca nativement : index full-text sur
  `text` + `models.Filter` avec `MatchText`, ou vecteurs sparse BM25. Meme
  resultat, sans scroll complet — et ca scale.
- **Versionner le corpus** : stocker la date de scrape et le hash de chaque
  page dans le payload, pour re-indexer seulement ce qui a change.
- **Benchmark type `improvement/`** : reutiliser ton harnais existant en
  remplacant le test de compilation Maude par l'execution des snippets Python
  generes contre un Qdrant jetable (`:memory:`), pour mesurer le taux de code
  qui tourne du premier coup.
