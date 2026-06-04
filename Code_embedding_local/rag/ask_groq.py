from rag.builder_ask import recherche_hybride, expand_context, COLLECTION, GEN_MODEL, embed_model
import os
from groq import Groq

# --- Clients ---
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

while True:

    # --- Question ---
    question = input("Your question about Maude: ")

    # embedding the question
    query_vector = embed_model.encode(question).tolist()

    hits, chunks_by_id = recherche_hybride(question, query_vector, COLLECTION, limit=3)
    hits = expand_context(hits, chunks_by_id, window=2)
    hits.sort(key=lambda h: h.id)        # ordre de lecture du manuel

    # --- Displaying debug ---
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

    # --- Building the context ---
    context = "\n\n---\n\n".join(
        f"[{h.payload['section']} - {h.payload['type']}]\n{h.payload['text']}"
        for h in hits
    )

    # --- Final prompt ---
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

    # --- Generating with Groq ---
    print("\n" + "=" * 60)
    print("💬 RÉPONSE FINALE :")
    response = groq_client.chat.completions.create(
        model=GEN_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    print(response.choices[0].message.content)
    print("=" * 60)
    print(f"\n📚 Sections utilisées : {[h.payload['section'] for h in hits]}")