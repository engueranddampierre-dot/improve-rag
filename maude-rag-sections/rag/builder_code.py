import os
import re
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

## VARIANTE "PARENT-SECTION" DU RAG MAUDE.
## Meme collection que rag-system (maude_manual : PAS de re-indexation),
## meme recherche hybride Python (semantique + lexicale ponderee 10x).
## Ce qui change : l'assemblage du contexte. Au lieu des heuristiques
## d'expansion (voisins ±2, prose-de-code, modules de section), on remonte
## les SECTIONS ENTIERES des meilleurs hits — prose et code dans l'ordre du
## manuel — sous un budget global de tokens. Pari teste : pour ameliorer du
## code, le LLM profite plus d'une section coherente et complete que de
## fragments selectionnes par heuristiques.

# --- Config ---
load_dotenv()
COLLECTION = "maude_manual"          # collection du baseline, reutilisee
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
BUDGET_TOKENS = 3000                 # plafond du contexte assemble

# --- Clients ---
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
qdrant      = QdrantClient(url=QDRANT_URL)

tokenizer = embed_model.tokenizer

def n_tokens(text):
    return len(tokenizer.encode(text, add_special_tokens=False))


# ---------------------------------------------------------------------------
# Recherche hybride : copie conforme du baseline rag-system/rag/builder_code.py
# ---------------------------------------------------------------------------

def recherche_hybride(question, query_vector, collection, limit=3):
    hits_semantique = qdrant.query_points(
        collection_name=collection,
        query=query_vector,
        limit=limit * 2,
        with_payload=True,
    ).points

    tokens = re.findall(r'[:\w]+=|[^\w\s]{2,}|\b\w{4,}\b', question)
    tokens = [t.strip('"\'`') for t in tokens]
    tokens = [t for t in tokens if t]
    tokens_speciaux = [t for t in tokens if re.search(r'[^\w]', t)]
    tokens_mots     = [t.lower() for t in tokens if not re.search(r'[^\w]', t)]

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

    if tokens_speciaux:
        ids_lexicaux = {h.id for h in hits_lexicaux[:limit]}
        prioritaires = hits_lexicaux[:limit]
        complement   = [h for h in hits_semantique if h.id not in ids_lexicaux][:limit]
    else:
        ids_sem = {h.id for h in hits_semantique[:limit]}
        prioritaires = hits_semantique[:limit]
        complement   = [h for h in hits_lexicaux if h.id not in ids_sem][:limit]

    fusion = prioritaires + complement
    chunks_by_id = {c.id: c for c in tous_les_chunks}
    return fusion[:limit * 2], chunks_by_id


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


# ---------------------------------------------------------------------------
# Assemblage parent-section (ce qui differe du baseline)
# ---------------------------------------------------------------------------

def _bruit(payload):
    """Chunks a ecarter dans une section : sessions interactives et
    transcriptions LaTeX (memes filtres que le baseline)."""
    texte = payload['text']
    if 'Maude>' in texte or 'Welcome to Maude' in texte:
        return True
    if any(sym in texte for sym in ('→', '⇝', '⇒', '∧')):
        return True
    return False


def reconstruire_section(hit, all_chunks_by_id):
    """Remonte la section entiere d'un hit en marchant sur les ids
    consecutifs (= ordre de lecture du manuel, garanti par l'indexation)."""
    section = hit.payload['section']
    membres = [hit]

    for direction in (-1, +1):
        step = 1
        while True:
            vid = hit.id + direction * step
            voisin = all_chunks_by_id.get(vid)
            if voisin is None or voisin.payload['section'] != section:
                break
            membres.append(voisin)
            step += 1

    membres.sort(key=lambda c: c.id)
    return [m for m in membres if not _bruit(m.payload)]


def assembler_contexte(hits, all_chunks_by_id, budget=BUDGET_TOKENS):
    """Sections entieres des hits, par ordre de pertinence, sous budget.
    La section d'un hit mieux classe passe d'abord ; une section n'entre que
    si elle tient entierement dans le budget restant (pas de section coupee,
    sauf la premiere si elle depasse a elle seule le budget)."""
    sections_vues = set()
    blocs = []
    restant = budget

    for h in hits:
        section = h.payload['section']
        if section in sections_vues:
            continue
        sections_vues.add(section)

        membres = reconstruire_section(h, all_chunks_by_id)
        texte_section = "\n\n".join(
            f"[{m.payload['type']}]\n{m.payload['text']}" for m in membres
        )
        cout = n_tokens(texte_section)

        if cout > restant:
            if not blocs:
                # premiere section trop grosse : on tronque par chunks entiers
                partiel, cumul = [], 0
                for m in membres:
                    t = f"[{m.payload['type']}]\n{m.payload['text']}"
                    c = n_tokens(t)
                    if cumul + c > budget:
                        break
                    partiel.append(t)
                    cumul += c
                if partiel:
                    blocs.append((section, "\n\n".join(partiel)))
                    restant = budget - cumul
            continue

        blocs.append((section, texte_section))
        restant -= cout

    return "\n\n---\n\n".join(
        f"=== SECTION : {titre} ===\n\n{contenu}" for titre, contenu in blocs
    )


def retrieve_maude_context(code, limit=3):
    """Contexte RAG pour AMELIORER un bloc de code Maude — meme signature
    que le baseline ; seul l'assemblage du contexte change."""
    constructions = extraire_constructions(code)
    question = " ".join(constructions)

    query_vector = embed_model.encode(code).tolist()

    hits, chunks_by_id = recherche_hybride(question, query_vector, COLLECTION, limit=limit)
    return assembler_contexte(hits, chunks_by_id)
