import requests
import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

## WORKS WAY BETTER THAN WITH THE PDF PROBABLY BECAUSE THE HTML STRUCTURE HELPS A LOT TO SEPARATE CODE / TEXT AND TITLES


# --- Config ---
load_dotenv()
COLLECTION = "maude_manual"
EMBED_DIM  = 384

# --- Clients ---
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
qdrant      = QdrantClient(url="http://localhost:6333")

BASE_URL = "https://maude.lcc.uma.es/maude-manual/"

CHAPTER_FILES = [
    "maude-manualch1.html",
    "maude-manualch2.html",
    "maude-manualch3.html",
    "maude-manualch4.html",
    "maude-manualch5.html",
    "maude-manualch6.html",
    "maude-manualch7.html",
    "maude-manualch8.html",
    "maude-manualch9.html",
    "maude-manualch10.html",
    "maude-manualch11.html",
    "maude-manualch12.html",
    "maude-manualch13.html",
    "maude-manualch14.html",
    "maude-manualch15.html",
    "maude-manualch16.html",
    "maude-manualch17.html",
    "maude-manualch18.html",
    "maude-manualch19.html",
    "maude-manualch20.html",
    "maude-manualch21.html",
    "maude-manualap1.html",
    "maude-manualap2.html",
]

# --- Tokenizer & paramètres de découpage ---
tokenizer  = embed_model.tokenizer
MAX_TOKENS = 200 # marge sous 256 : le tokenizer ajoute [CLS]/[SEP]
OVERLAP    = 30    # chevauchement pour ne pas couper une idée net


def n_tokens(text):
    return len(tokenizer.encode(text, add_special_tokens=True))


def scraper_page(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')


def extraire_chunks_html(soup, url):
    chunks = []
    current_section = ""
    current_texts = []

    for elem in soup.find_all(['h2', 'h3', 'h4', 'p', 'pre']):
        if elem.name in ['h2', 'h3', 'h4']:
            if current_texts:
                texte = "\n".join(current_texts).strip()
                if len(texte) > 100:
                    chunks.append({
                        "source": url,
                        "section": current_section,
                        "type": "text",
                        "text": texte,          # contenu PUR, titre dans "section"
                    })
            current_section = elem.get_text(separator=" ", strip=True)
            current_texts = []

        elif elem.name == 'pre':
            code = elem.get_text()  # pas de separator -> respecte espaces/\n de la source
            code = "\n".join(line.rstrip() for line in code.splitlines() if line.strip())
            if any(sym in code for sym in ('::=', '⟨', '⟩', '∣')):
                continue
            if len(code) > 20:
                chunks.append({
                    "source": url,
                    "section": current_section,
                    "type": "code",
                    "text": code,               # code PUR
                })

        elif elem.name == 'p':
            texte = elem.get_text(separator=" ", strip=True)
            if texte:
                current_texts.append(texte)

    # dernier bloc de texte en fin de page
    if current_texts:
        texte = "\n".join(current_texts).strip()
        if len(texte) > 100:
            chunks.append({
                "source": url,
                "section": current_section,
                "type": "text",
                "text": texte,
            })

    return chunks


def split_by_tokens(text, max_tokens=MAX_TOKENS, overlap=OVERLAP):
    """Découpe en respectant d'abord les lignes, puis par fenêtre de tokens si besoin."""
    if n_tokens(text) <= max_tokens:
        return [text]

    # 1) regrouper par lignes (paragraphes / lignes de code)
    lines = text.split("\n")
    blocs, courant = [], []
    for ligne in lines:
        test = "\n".join(courant + [ligne])
        if n_tokens(test) > max_tokens and courant:
            blocs.append("\n".join(courant))
            courant = [ligne]
        else:
            courant.append(ligne)
    if courant:
        blocs.append("\n".join(courant))

    # 2) si un bloc unique dépasse encore (longue ligne), fenêtre de tokens brute
    final = []
    for b in blocs:
        ids = tokenizer.encode(b, add_special_tokens=False)
        if len(ids) <= max_tokens:
            final.append(b)
        else:
            pas = max_tokens - overlap
            for start in range(0, len(ids), pas):
                morceau = tokenizer.decode(ids[start:start + max_tokens])
                final.append(morceau)
    return final


def texte_a_embedder(c):
    """Texte réellement envoyé à l'embedding : enrichi du titre pour le code
    et les chunks courts, brut sinon."""
    pur = c["text"]
    if not c["section"]:
        return pur
    if c["type"] == "code" or n_tokens(pur) < 120:
        return f"{c['section']}\n{pur}"
    return pur


# --- 1. Extraction ---
all_chunks = []
for filename in CHAPTER_FILES:
    url = BASE_URL + filename
    print(f"Scraping {filename}...")
    try:
        soup = scraper_page(url)
        chunks = extraire_chunks_html(soup, url)
        all_chunks.extend(chunks)
        time.sleep(0.5)  # politesse
    except Exception as e:
        print(f"Erreur sur {filename} : {e}")

print(f"{len(all_chunks)} chunks bruts extraits.")

# --- 2. Découpage sous la fenêtre du modèle ---
chunks_decoupes = []
for c in all_chunks:
    for sous_texte in split_by_tokens(c["text"]):
        chunks_decoupes.append({
            "source":  c["source"],
            "section": c["section"],
            "type":    c["type"],
            "text":    sous_texte,
        })
all_chunks = chunks_decoupes

# --- 3. Numérotation (APRÈS découpage) ---
for i, chunk in enumerate(all_chunks):
    chunk["id"] = i

print(f"{len(all_chunks)} chunks après découpage.")

# --- 4. Construction des textes à embedder + vérification AVANT encode ---
texts = [texte_a_embedder(c) for c in all_chunks]

over = sum(n_tokens(t) > 256 for t in texts)
print(f"Contrôle longueur — max={max(n_tokens(t) for t in texts)}, >256: {over}/{len(texts)}")
assert over == 0, "Des chunks dépassent encore 256 après ajout du titre — baisse MAX_TOKENS"

# --- 5. Embedding ---
print("Génération des embeddings (local)...")
vectors = embed_model.encode(
    texts,
    batch_size=64,
    show_progress_bar=True,
    convert_to_numpy=True,
)
print(f"Embeddings générés : {vectors.shape}")

# --- 6. Création de la collection ---
if qdrant.collection_exists(COLLECTION):
    qdrant.delete_collection(COLLECTION)

qdrant.create_collection(
    collection_name=COLLECTION,
    vectors_config=VectorParams(size=EMBED_DIM, distance=Distance.COSINE),
)

# --- 7. Upload par batch (payload["text"] = contenu PUR) ---
print("Upload dans Qdrant...")
BATCH_SIZE = 100
points = [
    PointStruct(
        id=chunk["id"],
        vector=vectors[i].tolist(),
        payload={
            "source":  chunk["source"],
            "section": chunk["section"],
            "type":    chunk["type"],
            "text":    chunk["text"],
        }
    )
    for i, chunk in enumerate(all_chunks)
]

for i in range(0, len(points), BATCH_SIZE):
    batch = points[i:i + BATCH_SIZE]
    qdrant.upsert(collection_name=COLLECTION, points=batch)
    print(f"  {min(i + BATCH_SIZE, len(points))}/{len(points)} points uploadés")

nb_code = sum(1 for c in all_chunks if c["type"] == "code")
nb_text = sum(1 for c in all_chunks if c["type"] == "text")
print(f"OK — {len(points)} chunks indexés dans '{COLLECTION}'.")
print(f"   dont {nb_code} blocs de code et {nb_text} paragraphes texte.")