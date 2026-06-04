from rag.builder_code import expand_section_modules, recherche_hybride, expand_section_modules, expand_context, COLLECTION, embed_model
import os
from groq import Groq

# --- Clients ---
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
GEN_MODEL  = "llama-3.3-70b-versatile"

while True:

    # --- Question ---
    question = input("What do you want to code?")

    # embed la question directement (pas de HyDE)
    query_vector = embed_model.encode(question).tolist()

    # ordre de lecture du manuel
    hits, chunks_by_id = recherche_hybride(question, query_vector, COLLECTION, limit=3)
    hits = expand_context(hits, chunks_by_id, window=2)
    hits = expand_section_modules(hits, chunks_by_id, list(chunks_by_id.values()), n_sections=2)
    hits.sort(key=lambda h: h.id)

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
    prompt = f"""You are an expert Maude programmer. Your task is to write Maude code that
implements the concept requested by the user.

You have two distinct sources of knowledge, and you MUST keep them separate:

1. GENERAL KNOWLEDGE (your own): use this ONLY to understand WHAT the user is
   asking for — the mathematical or computational concept itself (e.g., what
   Peano numbers are, what a stack is, how Euclid's algorithm works).

2. THE MAUDE MANUAL EXCERPTS (provided below): this is your ONLY authority for
   HOW to write it in Maude — the syntax, the keywords (fmod, op, eq, ceq,
   sort, subsort, ...), the operator declaration conventions, the attributes
   ([ctor], assoc, comm, ...), and every Maude-specific construct.

STRICT RULES:
- Every piece of Maude syntax you produce MUST be grounded in the manual
  excerpts below. Do NOT invent operators, attributes, keywords, or notation
  that do not appear in the excerpts.
- If the excerpts do not contain a construct you would need, do NOT guess or
  borrow syntax from other languages (no Haskell, ML, or generic functional
  notation). Instead, state explicitly which construct is missing from the
  excerpts.
- Do NOT use general knowledge to write Maude syntax — only to understand the
  concept. The manual is the single source of truth for the language.
- After the code, briefly cite which excerpt sections justify the main syntactic
  choices you made.

MAUDE MANUAL EXCERPTS:
{context}

USER REQUEST: {question}

Write the Maude code now, following the rules above."""

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