import os
from dotenv import load_dotenv
from groq import Groq
from google import genai
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import re

# --- Config ---
load_dotenv()
COLLECTION = "maude_manual"

# --- Clients ---
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
qdrant      = QdrantClient(url="http://localhost:6333")

def recherche_hybride(question, query_vector, collection, limit=3):
    # --- Semantic search ---
    hits_semantique = qdrant.query_points(
        collection_name=collection,
        query=query_vector,
        limit=limit * 2,
        with_payload=True,
    ).points

    # --- Tokens : we distinguish special symbols (:=) from common words ---
    tokens = re.findall(r'[:\w]+=|[^\w\s]{2,}|\b\w{4,}\b', question)
    # retire guillemets/apostrophes/backticks qui collent au symbole
    tokens = [t.strip('"\'`') for t in tokens]
    tokens = [t for t in tokens if t]   # vire les tokens devenus vides
    tokens_speciaux = [t for t in tokens if re.search(r'[^\w]', t)]
    tokens_mots     = [t.lower() for t in tokens if not re.search(r'[^\w]', t)]

    # --- Complete search in the corpus ---
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

    # --- Lexical scoring: special matches (symbols) are more valuable than normal ones ---
    def score_lexical(chunk):
        texte = chunk.payload['text'].lower()
        score = 0
        for t in tokens_speciaux:
            if t.lower() in texte:
                score += 10
        for t in tokens_mots:
            if t in texte:
                score += 1
        return score

    hits_lexicaux = [c for c in tous_les_chunks if score_lexical(c) > 0]
    hits_lexicaux.sort(key=score_lexical, reverse=True)

    # --- Conditional fusion ---
    if tokens_speciaux:
        # requête symbolique : lexical prioritaire
        ids_lexicaux = {h.id for h in hits_lexicaux[:limit]}
        prioritaires = hits_lexicaux[:limit]
        complement   = [h for h in hits_semantique if h.id not in ids_lexicaux][:limit]
        # marquage selon la voie réellement empruntée
        for h in prioritaires:
            h.payload['_origine'] = 'lexical'
        for h in complement:
            h.payload['_origine'] = 'sémantique'
        fusion = prioritaires + complement
    else:
        # requête conceptuelle : sémantique prioritaire
        ids_sem = {h.id for h in hits_semantique[:limit]}
        prioritaires = hits_semantique[:limit]
        complement   = [h for h in hits_lexicaux if h.id not in ids_sem][:limit]
        for h in prioritaires:
            h.payload['_origine'] = 'sémantique'
        for h in complement:
            h.payload['_origine'] = 'lexical'
        fusion = prioritaires + complement

    chunks_by_id = {c.id: c for c in tous_les_chunks}
    return fusion[:limit * 2], chunks_by_id

def expand_context(hits, all_chunks_by_id, window=2, window_search=5):
    ids_presents = {h.id for h in hits}
    ajouts = []
    hits_originaux = list(hits)   # on n'expand que ceux-ci, pas les ajouts

    for h in hits_originaux:
        section = h.payload['section']

        if h.payload.get('type') == 'code':
            # --- expansion ciblée : prose la plus proche, avant ET après ---
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
            # --- expansion classique : fenêtre ±window, même section ---
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

def expand_section_modules(hits, all_chunks_by_id, all_chunks_list,
                            n_sections=2):
    """Pour les sections des meilleurs hits, ajoute les blocs de code de type
    'module' (fmod/mod/fth/th) de la même section, en écartant les sessions Maude>."""
    ids_presents = {h.id for h in hits}

    # sections des n meilleurs hits (en gardant l'ordre de pertinence)
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
        # écarter les sessions interactives
        texte = c.payload['text']
        # écarter les sessions interactives et transcriptions LaTeX
        if 'Maude>' in texte or 'Welcome to Maude' in texte:
            continue
        if any(sym in texte for sym in ('→', '⇝', '⇒', '∧')):
            continue
        # garder ce qui ressemble à une déclaration de module / définitions
        if any(kw in texte for kw in ('fmod ', 'mod ', 'fth ', 'th ', '\neq ', '\nop ')):
            c.payload['_origine'] = 'module-section'
            ajouts.append(c)
            ids_presents.add(c.id)

    return hits + ajouts

# mots-clés trop fréquents dans le manuel pour discriminer une section pertinente
# (ils apparaissent dans presque tous les modules → bruit en requête lexicale)
MOTS_TROP_FREQUENTS = {
    'fmod', 'mod', 'fth', 'th', 'sort', 'op', 'ops', 'var', 'vars',
    'ctor', 'assoc', 'comm', 'id', 'protecting', 'including', 'extending',
    'eq', 'subsort',
}

def extraire_constructions(code):
    """Extrait du code Maude les constructions discriminantes pour piloter
    la recherche lexicale. Les mots-clés trop fréquents sont écartés car ils
    ramènent des sections hors-sujet (ils sont présents dans presque tous les modules)."""
    constructions = set()

    # attributs entre crochets : on garde les rares (owise, iter, ditto, variant...)
    for attr in re.findall(r'\[([^\]]+)\]', code):
        for mot in attr.split():
            if mot.isalpha() and mot.lower() not in MOTS_TROP_FREQUENTS:
                constructions.add(mot)

    # mots-clés structurels rares uniquement (les fréquents sont écartés)
    for kw in ('ceq', 'cmb', 'crl', 'rl', 'mb', 'owise', 'frozen', 'strat', 'variant'):
        if re.search(rf'\b{kw}\b', code):
            constructions.add(kw)

    # symboles/opérateurs spéciaux notables (toujours discriminants)
    for sym in (':=', '~>', '=>', '/\\'):
        if sym in code:
            constructions.add(sym)

    return constructions


def retrieve_maude_context(code, limit=3):
    """Construit le contexte RAG pour AMÉLIORER un bloc de code Maude.
    La requête est dérivée du code lui-même (constructions + contenu)."""
    # requête textuelle = les constructions trouvées, pour piloter le lexical
    constructions = extraire_constructions(code)
    question = " ".join(constructions)

    # requête sémantique = le code lui-même (tronqué par MiniLM, mais le début porte le signal)
    query_vector = embed_model.encode(code).tolist()

    hits, chunks_by_id = recherche_hybride(question, query_vector, COLLECTION, limit=limit)
    hits = expand_context(hits, chunks_by_id, window=2)
    hits = expand_section_modules(hits, chunks_by_id, list(chunks_by_id.values()), n_sections=2)
    hits.sort(key=lambda h: h.id)

    # bloc de contexte formaté pour le prompt
    context = "\n\n---\n\n".join(
        f"[{h.payload['section']} - {h.payload['type']}]\n{h.payload['text']}"
        for h in hits
    )
    return context