"""Verification rapide du retrieval sans appel LLM.
Usage : python -m rag.test_retrieve "ma question"
"""
import sys

from rag.builder_ask import recherche_hybride, expand_context, COLLECTION, embed_model
from rag.builder_code import expand_section_snippets

question = sys.argv[1] if len(sys.argv) > 1 else "How do I create a collection with hnsw_config?"

query_vector = embed_model.encode(question).tolist()
hits, chunks_by_id = recherche_hybride(question, query_vector, COLLECTION, limit=3)
hits = expand_context(hits, chunks_by_id, window=2)
hits = expand_section_snippets(hits, chunks_by_id, list(chunks_by_id.values()), n_sections=2)
hits.sort(key=lambda h: h.id)

print(f"Question : {question}\n")
for h in hits:
    score = getattr(h, "score", None)
    score_str = f"{score:.3f}" if score is not None else h.payload.get('_origine', '?')
    lang = f" ({h.payload['lang']})" if h.payload.get('lang') else ""
    print(f"[{h.payload['type']}{lang}] {h.payload['section']} — {score_str}")
    print(f"  {h.payload['text'][:150].replace(chr(10), ' ')}")
    print()
