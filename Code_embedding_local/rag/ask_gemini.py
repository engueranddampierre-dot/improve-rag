from wsgiref import types

from rag.builder_ask import recherche_hybride, expand_context, COLLECTION, GEN_MODEL, embed_model, qdrant
import os
from dotenv import load_dotenv
from google import genai
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# --- Clients ---
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
qdrant      = QdrantClient(url="http://localhost:6333")

# --- Question ---
question = input("Ta question sur Maude : ")

# embed la question directement (pas de HyDE)
query_vector = embed_model.encode(question).tolist()

hits, chunks_by_id = recherche_hybride(question, query_vector, COLLECTION, limit=3)
hits = expand_context(hits, chunks_by_id, window=2)
hits.sort(key=lambda h: h.id)       # ordre de lecture du manuel

# --- Affichage debug ---
print("🔍 Top chunks pertinents :")
for h in hits:
    score = getattr(h, "score", None)
    if score is not None:
        score_str = f"{score:.3f}"
    else:
        score_str = h.payload.get('_origine', '?')   # else filet de sécurité
    print(f"  [{h.payload['type']}] section: {h.payload['section']} (score: {score_str})")
    print(f"  {h.payload['text'][:120]}...")
    print()

# --- Construire le contexte ---
context = "\n\n---\n\n".join(
    f"[{h.payload['section']} - {h.payload['type']}]\n{h.payload['text']}"
    for h in hits
)

# --- Prompt final ---
prompt = f"""Réponds uniquement à partir des extraits fournis.
Si l'information n'y figure pas, dis-le clairement
(« Le manuel ne couvre pas ce point dans les extraits disponibles »).
Tu ne peux citer QUE les sections listées dans les extraits ci-dessus.
Il t'est interdit de mentionner toute autre section (ex: « voir Section X »)
ou tout exemple qui n'apparaît pas littéralement dans les extraits.

EXTRAITS DU MANUEL :
{context}

QUESTION : {question}

RÉPONSE :"""

# --- Générer avec Gemini ---
print("\n" + "=" * 60)
print("💬 RÉPONSE FINALE :")
response = gemini_client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config=types.GenerateContentConfig(temperature=0.3),
)
print(response.text)
print("=" * 60)