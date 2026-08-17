import re

from rag.builder_ask import (
    recherche_hybride, expand_context, COLLECTION, embed_model, qdrant,
)

# Langage cible par defaut pour les extraits de code ajoutes au contexte.
# La doc Qdrant duplique chaque exemple en http/python/typescript/rust/java...
# On privilegie un langage pour ne pas noyer le prompt, http garde en second
# (la requete REST est la reference canonique de l'API).
LANG_PREFEREES = ("python", "http", "bash", "json", "")


def expand_section_snippets(hits, all_chunks_by_id, all_chunks_list,
                            n_sections=2, langs=LANG_PREFEREES):
    """Equivalent de expand_section_modules du RAG Maude : pour les sections
    des meilleurs hits, ajoute les blocs de code de la meme section, mais
    filtres par langage prefere (sinon le contexte serait sature par les
    5 variantes de chaque exemple)."""
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
        if c.payload.get('lang', '') not in langs:
            continue
        texte = c.payload['text']
        # ecarter les sorties de console / logs (equivalent des sessions Maude>)
        if texte.lstrip().startswith(('$', '>>>', '#')) and '\n' not in texte:
            continue
        c.payload['_origine'] = 'snippet-section'
        ajouts.append(c)
        ids_presents.add(c.id)

    return hits + ajouts


# Mots-cles trop frequents dans la doc Qdrant pour discriminer une section
# (presents presque partout -> bruit en requete lexicale)
MOTS_TROP_FREQUENTS = {
    'client', 'qdrant', 'collection', 'collections', 'points', 'point',
    'vector', 'vectors', 'import', 'from', 'print', 'result', 'name',
    'models', 'http', 'localhost',
}


def extraire_constructions(code):
    """Extrait d'un code client Qdrant les constructions discriminantes pour
    piloter la recherche lexicale : noms de parametres snake_case, methodes
    du client, routes API. Les mots trop frequents sont ecartes."""
    constructions = set()

    # parametres nommes : xxx_yyy= ou "xxx_yyy":
    for m in re.findall(r'\b([a-z]+(?:_[a-z0-9]+)+)\s*[=:]', code):
        if m not in MOTS_TROP_FREQUENTS:
            constructions.add(m)

    # appels de methode du client : client.upsert(, client.query_points(...
    for m in re.findall(r'\.\s*([a-z_]{4,})\s*\(', code):
        if m not in MOTS_TROP_FREQUENTS:
            constructions.add(m)

    # classes de models : models.Filter, models.VectorParams...
    for m in re.findall(r'models\.([A-Za-z]+)', code):
        constructions.add(m)

    # routes API REST
    for m in re.findall(r'(/collections/[\w/{}.-]*)', code):
        constructions.add(m)

    return constructions


def retrieve_qdrant_context(code, limit=3):
    """Construit le contexte RAG pour AMELIORER un bloc de code utilisant
    Qdrant. La requete est derivee du code lui-meme (constructions + contenu)."""
    constructions = extraire_constructions(code)
    question = " ".join(constructions)

    # requete semantique = le code lui-meme (tronque par MiniLM, le debut porte le signal)
    query_vector = embed_model.encode(code).tolist()

    hits, chunks_by_id = recherche_hybride(question, query_vector, COLLECTION, limit=limit)
    hits = expand_context(hits, chunks_by_id, window=2)
    hits = expand_section_snippets(hits, chunks_by_id, list(chunks_by_id.values()), n_sections=2)
    hits.sort(key=lambda h: h.id)

    context = "\n\n---\n\n".join(
        f"[{h.payload['section']} - {h.payload['type']}"
        + (f" ({h.payload['lang']})" if h.payload.get('lang') else "")
        + f"]\n{h.payload['text']}"
        for h in hits
    )
    return context
