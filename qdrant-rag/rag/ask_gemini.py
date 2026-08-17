import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from rag.builder_ask import recherche_hybride, expand_context, COLLECTION, embed_model

# --- Config ---
load_dotenv()
GEN_MODEL = "gemini-2.5-flash"

# --- Clients ---
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# --- Question ---
question = input("Ta question sur Qdrant : ")

# embed la question directement (pas de HyDE)
query_vector = embed_model.encode(question).tolist()

hits, chunks_by_id = recherche_hybride(question, query_vector, COLLECTION, limit=3)
hits = expand_context(hits, chunks_by_id, window=2)
hits.sort(key=lambda h: h.id)       # ordre de lecture de la doc

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
    f"[{h.payload['section']} - {h.payload['type']}]\n{h.payload['text']}"
    for h in hits
)

# --- Prompt final ---
prompt = f"""Reponds uniquement a partir des extraits fournis.
Si l'information n'y figure pas, dis-le clairement
(« La documentation ne couvre pas ce point dans les extraits disponibles »).
Tu ne peux citer QUE les sections listees dans les extraits ci-dessus.
Il t'est interdit de mentionner toute autre section ou page de la
documentation Qdrant, ou tout exemple qui n'apparait pas litteralement
dans les extraits.

EXTRAITS DE LA DOCUMENTATION QDRANT :
{context}

QUESTION : {question}

REPONSE :"""

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
