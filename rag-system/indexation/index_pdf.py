import re
from pathlib import Path
from dotenv import load_dotenv
import fitz
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer

## THIS DOESN'T WORK AS WELL AS WITH THE HTML DOCUMENT

# --- Config ---
load_dotenv()
PDF_PATH   = Path(__file__).parent / "Manuel_Maude.pdf"
COLLECTION = "maude_manual"
EMBED_DIM  = 384

# --- Clients ---
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
qdrant      = QdrantClient(url="http://localhost:6333")

# --- Fonctions de découpage ---
def est_texte_lisible(text):
    mots = text.split()
    if len(mots) < 5:
        return False
    mots_un_char = sum(1 for m in mots if len(m) == 1)
    return (mots_un_char / len(mots)) < 0.4

def extraire_chunks(text, page_num):
    chunks = []

    # 1. Détecte les blocs de code Maude
    blocs_code = re.findall(
        r'((?:fmod|mod|fth|th)\s+\w+.*?(?:endfm|endm|endfth|endth))',
        text,
        re.DOTALL | re.IGNORECASE
    )

    for bloc in blocs_code:
        if len(bloc) > 50:
            chunks.append({
                "page": page_num,
                "type": "code",
                "text": bloc.strip(),
            })

    # 2. Supprime les blocs de code du texte pour ne pas les doubler
    texte_sans_code = re.sub(
        r'(?:fmod|mod|fth|th)\s+\w+.*?(?:endfm|endm|endfth|endth)',
        '',
        text,
        flags=re.DOTALL | re.IGNORECASE
    )

    # 3. Découpe le reste en paragraphes
    for para in re.split(r'\n\s*\n', texte_sans_code):
        para = para.strip()
        if len(para) > 80 and est_texte_lisible(para):
            chunks.append({
                "page": page_num,
                "type": "text",
                "text": para,
            })

    return chunks

# --- 1. Lire le PDF ---
print(f"Lecture de {PDF_PATH.name}...")
doc = fitz.open(str(PDF_PATH))

all_chunks = []
for page_num, page in enumerate(doc):
    text = page.get_text()
    if not text:
        continue
    all_chunks.extend(extraire_chunks(text, page_num + 1))

# numérotation globale des ids
for i, chunk in enumerate(all_chunks):
    chunk["id"] = i

if any(":=" in chunk for chunk in all_chunks):
    print("oui ça a marché sa mère")
else:
    print("euh, nique ta mère")

print(all_chunks[29:32])

# stats
nb_code = sum(1 for c in all_chunks if c["type"] == "code")
nb_text = sum(1 for c in all_chunks if c["type"] == "text")
print(f"{len(all_chunks)} chunks extraits : {nb_text} texte, {nb_code} code.")

# --- 2. Embedder en batch ---
print("Génération des embeddings (local)...")
texts   = [c["text"] for c in all_chunks]
vectors = embed_model.encode(
    texts,
    batch_size=64,
    show_progress_bar=True,
    convert_to_numpy=True,
)
print(f"Embeddings générés : {vectors.shape}")

# --- 3. Créer la collection Qdrant ---
if qdrant.collection_exists(COLLECTION):
    qdrant.delete_collection(COLLECTION)

qdrant.create_collection(
    collection_name=COLLECTION,
    vectors_config=VectorParams(size=EMBED_DIM, distance=Distance.COSINE),
)

# --- 4. Uploader par batch ---
print("Upload dans Qdrant...")
BATCH_SIZE = 100
points = [
    PointStruct(
        id=chunk["id"],
        vector=vectors[i].tolist(),
        payload={
            "page": chunk["page"],
            "type": chunk["type"],
            "text": chunk["text"],
        }
    )
    for i, chunk in enumerate(all_chunks)
]

for i in range(0, len(points), BATCH_SIZE):
    batch = points[i:i + BATCH_SIZE]
    qdrant.upsert(collection_name=COLLECTION, points=batch)
    print(f"  {min(i + BATCH_SIZE, len(points))}/{len(points)} points uploadés")

print(f"✅ {len(points)} chunks indexés dans '{COLLECTION}'.")
print(f"   dont {nb_code} blocs de code et {nb_text} paragraphes texte.")