import os
import time
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams, SparseVectorParams, Distance, Modifier, PointStruct,
    SparseVector,
)
from sentence_transformers import SentenceTransformer
from fastembed import SparseTextEmbedding
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

## VARIANTE "HYBRID NATIF" DU RAG MAUDE.
## Meme corpus, meme extraction, meme decoupage que rag-system.
## Ce qui change : chaque point porte DEUX vecteurs nommes —
##   dense  : all-MiniLM-L6-v2 (comme le baseline)
##   bm25   : vecteur sparse BM25 (fastembed), IDF calcule par le serveur
## La fusion lexical/semantique se fait cote Qdrant (RRF), plus de scan
## Python du corpus a chaque requete.
##
## ASTUCE SYMBOLES : BM25 tokenise en mots et detruirait `:=`, `~>`, etc.
## — or en Maude la syntaxe EST le sens (l'insight du baseline, pondere 10x).
## On remplace donc les symboles par des tokens sentinelles AVANT l'encodage
## BM25, a l'indexation comme a la requete. Le payload reste le texte pur.

# --- Config ---
load_dotenv()
COLLECTION = "maude_manual_hybrid"
EMBED_DIM  = 384
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")

# --- Clients ---
embed_model  = SentenceTransformer("all-MiniLM-L6-v2")
sparse_model = SparseTextEmbedding("Qdrant/bm25")
qdrant       = QdrantClient(url=QDRANT_URL)

BASE_URL = "https://maude.lcc.uma.es/maude-manual/"

CHAPTER_FILES = [
    *[f"maude-manualch{i}.html" for i in range(1, 22)],
    "maude-manualap1.html",
    "maude-manualap2.html",
]

# --- Protection des symboles Maude pour BM25 (ordre : du plus long au plus court) ---
SYMBOLES_MAUDE = [
    ("=/=", "symnoteq"),
    (":=",  "symassign"),
    ("=>",  "symruleto"),
    ("~>",  "symsquig"),
    ("->",  "symarrow"),
    ("/\\", "symconj"),
    ("\\/", "symdisj"),
    ("<=",  "symleq"),
    (">=",  "symgeq"),
    ("==",  "symeqeq"),
]

def proteger_symboles(text):
    for sym, token in SYMBOLES_MAUDE:
        text = text.replace(sym, f" {token} ")
    return text

# --- Tokenizer & parametres de decoupage (identiques au baseline) ---
tokenizer  = embed_model.tokenizer
MAX_TOKENS = 200
OVERLAP    = 30


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
                    chunks.append({"source": url, "section": current_section,
                                   "type": "text", "text": texte})
            current_section = elem.get_text(separator=" ", strip=True)
            current_texts = []

        elif elem.name == 'pre':
            code = elem.get_text()
            code = "\n".join(l.rstrip() for l in code.splitlines() if l.strip())
            if any(sym in code for sym in ('::=', '⟨', '⟩', '∣')):
                continue
            if len(code) > 20:
                chunks.append({"source": url, "section": current_section,
                               "type": "code", "text": code})

        elif elem.name == 'p':
            texte = elem.get_text(separator=" ", strip=True)
            if texte:
                current_texts.append(texte)

    if current_texts:
        texte = "\n".join(current_texts).strip()
        if len(texte) > 100:
            chunks.append({"source": url, "section": current_section,
                           "type": "text", "text": texte})

    return chunks


def split_by_tokens(text, max_tokens=MAX_TOKENS, overlap=OVERLAP):
    if n_tokens(text) <= max_tokens:
        return [text]

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

    final = []
    for b in blocs:
        ids = tokenizer.encode(b, add_special_tokens=False)
        if len(ids) <= max_tokens:
            final.append(b)
        else:
            pas = max_tokens - overlap
            for start in range(0, len(ids), pas):
                final.append(tokenizer.decode(ids[start:start + max_tokens]))
    return final


def texte_a_embedder(c):
    pur = c["text"]
    if not c["section"]:
        return pur
    if c["type"] == "code" or n_tokens(pur) < 120:
        return f"{c['section']}\n{pur}"
    return pur


if __name__ == "__main__":
    # --- 1. Extraction ---
    all_chunks = []
    for filename in CHAPTER_FILES:
        url = BASE_URL + filename
        print(f"Scraping {filename}...")
        try:
            soup = scraper_page(url)
            all_chunks.extend(extraire_chunks_html(soup, url))
            time.sleep(0.5)
        except Exception as e:
            print(f"Erreur sur {filename} : {e}")

    print(f"{len(all_chunks)} chunks bruts extraits.")

    # --- 2. Decoupage ---
    all_chunks = [
        {**c, "text": t}
        for c in all_chunks
        for t in split_by_tokens(c["text"])
    ]

    # --- 3. Numerotation (ids consecutifs = ordre de lecture) ---
    for i, chunk in enumerate(all_chunks):
        chunk["id"] = i
    print(f"{len(all_chunks)} chunks apres decoupage.")

    # --- 4. Embeddings dense ---
    texts = [texte_a_embedder(c) for c in all_chunks]
    over = sum(n_tokens(t) > 256 for t in texts)
    assert over == 0, "Des chunks depassent 256 tokens"
    print("Embeddings dense...")
    dense = embed_model.encode(texts, batch_size=64, show_progress_bar=True,
                               convert_to_numpy=True)

    # --- 5. Embeddings sparse BM25 (symboles proteges) ---
    print("Embeddings sparse BM25...")
    textes_bm25 = [proteger_symboles(t) for t in texts]
    sparse = list(sparse_model.embed(textes_bm25, batch_size=64))

    # --- 6. Collection a deux vecteurs nommes ---
    if qdrant.collection_exists(COLLECTION):
        qdrant.delete_collection(COLLECTION)
    qdrant.create_collection(
        collection_name=COLLECTION,
        vectors_config={"dense": VectorParams(size=EMBED_DIM, distance=Distance.COSINE)},
        sparse_vectors_config={"bm25": SparseVectorParams(modifier=Modifier.IDF)},
    )

    # --- 7. Upload ---
    print("Upload dans Qdrant...")
    BATCH_SIZE = 100
    points = [
        PointStruct(
            id=c["id"],
            vector={
                "dense": dense[i].tolist(),
                "bm25": SparseVector(
                    indices=sparse[i].indices.tolist(),
                    values=sparse[i].values.tolist(),
                ),
            },
            payload={"source": c["source"], "section": c["section"],
                     "type": c["type"], "text": c["text"]},
        )
        for i, c in enumerate(all_chunks)
    ]
    for i in range(0, len(points), BATCH_SIZE):
        qdrant.upsert(collection_name=COLLECTION, points=points[i:i + BATCH_SIZE])
        print(f"  {min(i + BATCH_SIZE, len(points))}/{len(points)}")

    nb_code = sum(1 for c in all_chunks if c["type"] == "code")
    print(f"OK — {len(points)} chunks indexes dans '{COLLECTION}' "
          f"({nb_code} code / {len(points) - nb_code} texte).")
