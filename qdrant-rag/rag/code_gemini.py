import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from rag.builder_ask import recherche_hybride, expand_context, COLLECTION, embed_model
from rag.builder_code import expand_section_snippets

# --- Config ---
load_dotenv()
GEN_MODEL   = "gemini-2.5-flash"
LANG_CIBLE  = "Python (client qdrant-client)"   # adapte si besoin

# --- Clients ---
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

while True:

    # --- Question ---
    question = input("What do you want to code with Qdrant? ")

    # embed la question directement (pas de HyDE)
    query_vector = embed_model.encode(question).tolist()

    hits, chunks_by_id = recherche_hybride(question, query_vector, COLLECTION, limit=3)
    hits = expand_context(hits, chunks_by_id, window=2)
    hits = expand_section_snippets(hits, chunks_by_id, list(chunks_by_id.values()), n_sections=2)
    hits.sort(key=lambda h: h.id)   # ordre de lecture de la doc

    # --- Affichage debug ---
    print("Top chunks pertinents :")
    for h in hits:
        score = getattr(h, "score", None)
        score_str = f"{score:.3f}" if score is not None else h.payload.get('_origine', '?')
        print(f"  [{h.payload['type']}] section: {h.payload['section']} (score: {score_str})")
        print(f"  {h.payload['text'][:120]}...")
        print()

    # --- Construire le contexte ---
    context = "\n\n---\n\n".join(
        f"[{h.payload['section']} - {h.payload['type']}"
        + (f" ({h.payload['lang']})" if h.payload.get('lang') else "")
        + f"]\n{h.payload['text']}"
        for h in hits
    )

    # --- Prompt final ---
    prompt = f"""You are an expert Qdrant engineer. Your task is to write {LANG_CIBLE}
code that implements what the user requests, using the Qdrant vector database.

You have two distinct sources of knowledge, and you MUST keep them separate:

1. GENERAL KNOWLEDGE (your own): use this ONLY to understand WHAT the user is
   asking for — the retrieval or data-management concept itself (e.g., what
   hybrid search is, what a payload filter does conceptually, what
   quantization means).

2. THE QDRANT DOCUMENTATION EXCERPTS (provided below): this is your ONLY
   authority for HOW to write it — the client API (method names, parameters),
   the models classes (Filter, VectorParams, PointStruct, ...), the REST
   routes, the JSON shapes, the configuration keys (hnsw_config, ef_construct,
   on_disk, ...), and every Qdrant-specific construct.

STRICT RULES:
- Every Qdrant API call, parameter name, model class, and configuration key
  you produce MUST be grounded in the documentation excerpts below. Do NOT
  invent methods, parameters, or fields that do not appear in the excerpts.
- If the excerpts do not contain a construct you would need, do NOT guess or
  borrow from other vector databases (no Pinecone, Weaviate, or generic
  pseudo-API). Instead, state explicitly which construct is missing from the
  excerpts.
- Do NOT use general knowledge to write Qdrant API calls — only to understand
  the concept. The documentation is the single source of truth for the API.
- After the code, briefly cite which excerpt sections justify the main API
  choices you made.

QDRANT DOCUMENTATION EXCERPTS:
{context}

USER REQUEST: {question}

Write the code now, following the rules above."""

    # --- Generer avec Gemini ---
    print("\n" + "=" * 60)
    print("REPONSE FINALE :")
    response = gemini_client.models.generate_content(
        model=GEN_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.3),
    )
    print(response.text)
    print("=" * 60)
    print(f"\nSections utilisees : {[h.payload['section'] for h in hits]}")
