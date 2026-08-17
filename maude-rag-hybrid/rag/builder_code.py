import os
import re
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Prefetch, FusionQuery, Fusion, SparseVector
from sentence_transformers import SentenceTransformer
from fastembed import SparseTextEmbedding

## VARIANTE "HYBRID NATIF" : la fusion lexical/semantique est faite par
## Qdrant (RRF sur prefetch dense + BM25) au lieu du scan Python du corpus.
## Les expansions de contexte (voisins, prose-de-code, modules de section)
## sont IDENTIQUES au baseline rag-system : seule la methode de ranking
## change, pour que la comparaison mesure bien ca et rien d'autre.

# --- Config ---
load_dotenv()
COLLECTION = "maude_manual_hybrid"
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")

# --- Clients ---
embed_model  = SentenceTransformer("all-MiniLM-L6-v2")
sparse_model = SparseTextEmbedding("Qdrant/bm25")
qdrant       = QdrantClient(url=QDRANT_URL)

# --- Protection des symboles (meme table qu'a l'indexation) ---
SYMBOLES_MAUDE = [
    ("=/=", "symnoteq"),
    (":=",  "symassign"),
    ("=>",  "symruleto"),
    ("~>",  "symsquig"),
    ("->",  "symarrow"),
    ("/\\", "symconj"),
    ("\\/", "symdisj"),
    ("<=",  "symleq"),
    (">=",  "symgeq"),
    ("==",  "symeqeq"),
]

def proteger_symboles(text):
    for sym, token in SYMBOLES_MAUDE:
        text = text.replace(sym, f" {token} ")
    return text


def recherche_hybride(question, query_vector, collection, limit=3):
    """Fusion RRF cote serveur : prefetch dense + prefetch BM25.
    Retourne (hits, chunks_by_id) — meme contrat que le baseline."""
    q_sparse = next(iter(sparse_model.query_embed(proteger_symboles(question))))

    hits = qdrant.query_points(
        collection_name=collection,
        prefetch=[
            Prefetch(query=query_vector, using="dense", limit=limit * 5),
            Prefetch(
                query=SparseVector(indices=q_sparse.indices.tolist(),
                                   values=q_sparse.values.tolist()),
                using="bm25",
                limit=limit * 5,
            ),
        ],
        query=FusionQuery(fusion=Fusion.RRF),
        limit=limit * 2,
        with_payload=True,
    ).points

    for h in hits:
        h.payload['_origine'] = 'rrf'

    # meme besoin qu'au baseline : acces aux voisins par id pour l'expansion
    tous_les_chunks = []
    offset = None
    while True:
        batch, offset = qdrant.scroll(
            collection_name=collection,
            limit=256,
            offset=offset,
            with_payload=True,
            with_vectors=False,
        )
        tous_les_chunks.extend(batch)
        if offset is None:
            break

    chunks_by_id = {c.id: c for c in tous_les_chunks}
    return hits, chunks_by_id


# ---------------------------------------------------------------------------
# Expansions : copie conforme du baseline rag-system/rag/builder_code.py
# ---------------------------------------------------------------------------

def expand_context(hits, all_chunks_by_id, window=2, window_search=5):
    ids_presents = {h.id for h in hits}
    ajouts = []
    hits_originaux = list(hits)

    for h in hits_originaux:
        section = h.payload['section']

        if h.payload.get('type') == 'code':
            for direction in (+1, -1):
                for step in range(1, window_search + 1):
                    vid = h.id + direction * step
                    voisin = all_chunks_by_id.get(vid)
                    if voisin is None or voisin.payload['section'] != section:
                        break
                    if voisin.payload.get('type') == 'text' and vid not in ids_presents:
                        voisin.payload['_origine'] = 'prose-de-code'
                        ajouts.append(voisin)
                        ids_presents.add(vid)
                        break
        else:
            for delta in range(-window, window + 1):
                if delta == 0:
                    continue
                vid = h.id + delta
                voisin = all_chunks_by_id.get(vid)
                if voisin is None or voisin.payload['section'] != section:
                    continue
                if vid not in ids_presents:
                    voisin.payload['_origine'] = 'voisin'
                    ajouts.append(voisin)
                    ids_presents.add(vid)

    return hits + ajouts


def expand_section_modules(hits, all_chunks_by_id, all_chunks_list, n_sections=2):
    ids_presents = {h.id for h in hits}

    sections_cibles = []
    for h in hits:
        s = h.payload['section']
        if s not in sections_cibles:
            sections_cibles.append(s)
        if len(sections_cibles) >= n_sections:
            break

    ajouts = []
    for c in all_chunks_list:
        if c.id in ids_presents:
            continue
        if c.payload.get('type') != 'code':
            continue
        if c.payload['section'] not in sections_cibles:
            continue
        texte = c.payload['text']
        if 'Maude>' in texte or 'Welcome to Maude' in texte:
            continue
        if any(sym in texte for sym in ('→', '⇝', '⇒', '∧')):
            continue
        if any(kw in texte for kw in ('fmod ', 'mod ', 'fth ', 'th ', '\neq ', '\nop ')):
            c.payload['_origine'] = 'module-section'
            ajouts.append(c)
            ids_presents.add(c.id)

    return hits + ajouts


MOTS_TROP_FREQUENTS = {
    'fmod', 'mod', 'fth', 'th', 'sort', 'op', 'ops', 'var', 'vars',
    'ctor', 'assoc', 'comm', 'id', 'protecting', 'including', 'extending',
    'eq', 'subsort',
}


def extraire_constructions(code):
    constructions = set()

    for attr in re.findall(r'\[([^\]]+)\]', code):
        for mot in attr.split():
            if mot.isalpha() and mot.lower() not in MOTS_TROP_FREQUENTS:
                constructions.add(mot)

    for kw in ('ceq', 'cmb', 'crl', 'rl', 'mb', 'owise', 'frozen', 'strat', 'variant'):
        if re.search(rf'\b{kw}\b', code):
            constructions.add(kw)

    for sym in (':=', '~>', '=>', '/\\'):
        if sym in code:
            constructions.add(sym)

    return constructions


def retrieve_maude_context(code, limit=3):
    """Contexte RAG pour AMELIORER un bloc de code Maude — meme signature
    et meme format de sortie que le baseline, seul le ranking change."""
    constructions = extraire_constructions(code)
    question = " ".join(constructions) if constructions else code[:200]

    query_vector = embed_model.encode(code).tolist()

    hits, chunks_by_id = recherche_hybride(question, query_vector, COLLECTION, limit=limit)
    hits = expand_context(hits, chunks_by_id, window=2)
    hits = expand_section_modules(hits, chunks_by_id, list(chunks_by_id.values()), n_sections=2)
    hits.sort(key=lambda h: h.id)

    context = "\n\n---\n\n".join(
        f"[{h.payload['section']} - {h.payload['type']}]\n{h.payload['text']}"
        for h in hits
    )
    return context
