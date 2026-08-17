import os
import re
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# --- Config ---
load_dotenv()
COLLECTION = "qdrant_docs"
GEN_MODEL  = "gemini-2.5-flash"
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")

# --- Clients ---
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
qdrant      = QdrantClient(url=QDRANT_URL)


def recherche_hybride(question, query_vector, collection, limit=3):
    # --- Recherche semantique ---
    hits_semantique = qdrant.query_points(
        collection_name=collection,
        query=query_vector,
        limit=limit * 2,
        with_payload=True,
    ).points

    # --- Tokens : on distingue les identifiants techniques des mots communs.
    # En doc Qdrant, l'equivalent des symboles Maude, ce sont les noms de
    # parametres (hnsw_config, ef_construct), les routes API (/collections/...)
    # et les champs JSON ("must", "should"...). La regex capte les chemins,
    # le snake_case et les symboles ; le tri special/mot se fait apres.
    tokens = re.findall(r'/[\w/{}.-]+|[:\w]+=|[^\w\s]{2,}|\b\w{4,}\b', question)
    tokens = [t.strip('"\'`') for t in tokens]
    tokens = [t for t in tokens if t]
    # "special" = contient un caractere non-mot (/, {, =, ...) OU un underscore
    # (les parametres snake_case sont tres discriminants dans la doc Qdrant)
    tokens_speciaux = [t for t in tokens if re.search(r'[^\w]|_', t)]
    tokens_mots     = [t.lower() for t in tokens if t not in tokens_speciaux]

    # --- Parcours complet du corpus ---
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

    # --- Score lexical : un match "special" vaut 10x un mot normal ---
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

    # --- Fusion conditionnelle ---
    if tokens_speciaux:
        # requete technique : lexical prioritaire
        ids_lexicaux = {h.id for h in hits_lexicaux[:limit]}
        prioritaires = hits_lexicaux[:limit]
        complement   = [h for h in hits_semantique if h.id not in ids_lexicaux][:limit]
        for h in prioritaires:
            h.payload['_origine'] = 'lexical'
        for h in complement:
            h.payload['_origine'] = 'semantique'
        fusion = prioritaires + complement
    else:
        # requete conceptuelle : semantique prioritaire
        ids_sem = {h.id for h in hits_semantique[:limit]}
        prioritaires = hits_semantique[:limit]
        complement   = [h for h in hits_lexicaux if h.id not in ids_sem][:limit]
        for h in prioritaires:
            h.payload['_origine'] = 'semantique'
        for h in complement:
            h.payload['_origine'] = 'lexical'
        fusion = prioritaires + complement

    chunks_by_id = {c.id: c for c in tous_les_chunks}
    return fusion[:limit * 2], chunks_by_id


def expand_context(hits, all_chunks_by_id, window=2, window_search=5):
    """Ajoute les voisins de meme section : les ids sont consecutifs dans
    l'ordre de lecture de la doc (numerotation post-decoupage a l'indexation)."""
    ids_presents = {h.id for h in hits}
    ajouts = []
    hits_originaux = list(hits)   # on n'expand que ceux-ci, pas les ajouts

    for h in hits_originaux:
        section = h.payload['section']

        if h.payload.get('type') == 'code':
            # --- expansion ciblee : prose la plus proche, avant ET apres ---
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
            # --- expansion classique : fenetre ±window, meme section ---
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
