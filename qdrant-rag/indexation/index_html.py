import os
import re
import time
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer

## MEME APPROCHE QUE LE RAG MAUDE : scraping HTML (structure fiable pour
## separer code / texte / titres), chunks purs + section dans le payload.
## Difference principale : les pages sont decouvertes via le sitemap au lieu
## d'une liste de chapitres codee en dur, et les blocs de code portent un
## champ "lang" (la doc Qdrant donne chaque exemple en plusieurs langages).

# --- Config ---
load_dotenv()
COLLECTION = "qdrant_docs"
EMBED_DIM  = 384
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")

BASE       = "https://qdrant.tech"
SITEMAP    = f"{BASE}/sitemap.xml"
DOC_PREFIX = f"{BASE}/documentation/"

# sous-arbres a ecarter (peu utiles pour un RAG technique local)
EXCLUDE_PATTERNS = (
    "/documentation/examples/",        # notebooks externes, peu de contenu inline
    "/documentation/release-notes",
)

# --- Clients ---
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
qdrant      = QdrantClient(url=QDRANT_URL)

# --- Tokenizer & parametres de decoupage ---
tokenizer  = embed_model.tokenizer
MAX_TOKENS = 200   # marge sous 256 : le tokenizer ajoute [CLS]/[SEP]
OVERLAP    = 30    # chevauchement pour ne pas couper une idee net


def n_tokens(text):
    return len(tokenizer.encode(text, add_special_tokens=True))


def scraper_page(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def decouvrir_pages():
    """Liste des pages de doc via le sitemap (plus robuste qu'une liste en dur :
    la doc Qdrant bouge souvent)."""
    r = requests.get(SITEMAP, timeout=30)
    r.raise_for_status()
    urls = re.findall(r"<loc>(.*?)</loc>", r.text)
    pages = [
        u for u in urls
        if u.startswith(DOC_PREFIX)
        and not any(p in u for p in EXCLUDE_PATTERNS)
    ]
    return sorted(set(pages))


def detecter_langage(pre):
    """Langage d'un bloc <pre> via les classes CSS (language-python, etc.)."""
    for node in [pre] + pre.find_all("code"):
        for cls in node.get("class") or []:
            if cls.startswith("language-"):
                return cls[len("language-"):]
    return ""


def zone_contenu(soup):
    """Isole le contenu principal : la doc Qdrant est generee par Hugo,
    le contenu vit dans <article> ; sinon <main> ; sinon body nettoye."""
    zone = soup.find("article") or soup.find("main") or soup.body
    if zone is None:
        return None
    for tag in zone.find_all(["nav", "aside", "header", "footer", "script", "style", "form"]):
        tag.decompose()
    return zone


def extraire_chunks_html(soup, url):
    chunks = []
    zone = zone_contenu(soup)
    if zone is None:
        return chunks

    # titre de page (h1) comme section par defaut
    h1 = zone.find("h1")
    current_section = h1.get_text(separator=" ", strip=True) if h1 else ""
    current_texts = []

    def flush_texts():
        nonlocal current_texts
        if current_texts:
            texte = "\n".join(current_texts).strip()
            if len(texte) > 100:
                chunks.append({
                    "source": url,
                    "section": current_section,
                    "type": "text",
                    "lang": "",
                    "text": texte,      # contenu PUR, titre dans "section"
                })
            current_texts = []

    for elem in zone.find_all(["h2", "h3", "h4", "p", "pre", "li", "table"]):
        if elem.name in ["h2", "h3", "h4"]:
            flush_texts()
            current_section = elem.get_text(separator=" ", strip=True)

        elif elem.name == "pre":
            code = elem.get_text()   # pas de separator -> respecte espaces/\n
            code = "\n".join(l.rstrip() for l in code.splitlines() if l.strip())
            if len(code) > 20:
                chunks.append({
                    "source": url,
                    "section": current_section,
                    "type": "code",
                    "lang": detecter_langage(elem),
                    "text": code,   # code PUR
                })

        elif elem.name == "li":
            # ne garder que les <li> hors nav, sans sous-blocs deja traites
            if elem.find("pre") or elem.find("li"):
                continue
            texte = elem.get_text(separator=" ", strip=True)
            if texte:
                current_texts.append(f"- {texte}")

        elif elem.name == "table":
            lignes = []
            for tr in elem.find_all("tr"):
                cells = [td.get_text(separator=" ", strip=True) for td in tr.find_all(["td", "th"])]
                if any(cells):
                    lignes.append(" | ".join(cells))
            if lignes:
                current_texts.append("\n".join(lignes))

        elif elem.name == "p":
            # eviter les <p> imbriques dans des <li> deja captures
            if elem.find_parent("li"):
                continue
            texte = elem.get_text(separator=" ", strip=True)
            if texte:
                current_texts.append(texte)

    flush_texts()
    return chunks


def split_by_tokens(text, max_tokens=MAX_TOKENS, overlap=OVERLAP):
    """Decoupe en respectant d'abord les lignes, puis par fenetre de tokens."""
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
    """Texte envoye a l'embedding : enrichi du titre pour le code et les
    chunks courts, brut sinon."""
    pur = c["text"]
    if not c["section"]:
        return pur
    if c["type"] == "code" or n_tokens(pur) < 120:
        return f"{c['section']}\n{pur}"
    return pur


if __name__ == "__main__":
    # --- 1. Extraction ---
    pages = decouvrir_pages()
    print(f"{len(pages)} pages de documentation trouvees dans le sitemap.")

    all_chunks = []
    for url in pages:
        print(f"Scraping {url.removeprefix(DOC_PREFIX) or 'index'}...")
        try:
            soup = scraper_page(url)
            all_chunks.extend(extraire_chunks_html(soup, url))
            time.sleep(0.5)  # politesse
        except Exception as e:
            print(f"Erreur sur {url} : {e}")

    print(f"{len(all_chunks)} chunks bruts extraits.")

    # --- 2. Decoupage sous la fenetre du modele ---
    chunks_decoupes = []
    for c in all_chunks:
        for sous_texte in split_by_tokens(c["text"]):
            chunks_decoupes.append({**c, "text": sous_texte})
    all_chunks = chunks_decoupes

    # --- 3. Numerotation (APRES decoupage : ids consecutifs = ordre de lecture) ---
    for i, chunk in enumerate(all_chunks):
        chunk["id"] = i

    print(f"{len(all_chunks)} chunks apres decoupage.")

    # --- 4. Textes a embedder + controle AVANT encode ---
    texts = [texte_a_embedder(c) for c in all_chunks]
    over = sum(n_tokens(t) > 256 for t in texts)
    print(f"Controle longueur — max={max(n_tokens(t) for t in texts)}, >256: {over}/{len(texts)}")
    assert over == 0, "Des chunks depassent 256 apres ajout du titre — baisse MAX_TOKENS"

    # --- 5. Embedding ---
    print("Generation des embeddings (local)...")
    vectors = embed_model.encode(
        texts,
        batch_size=64,
        show_progress_bar=True,
        convert_to_numpy=True,
    )
    print(f"Embeddings generes : {vectors.shape}")

    # --- 6. Creation de la collection ---
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
            id=c["id"],
            vector=vectors[i].tolist(),
            payload={
                "source":  c["source"],
                "section": c["section"],
                "type":    c["type"],
                "lang":    c["lang"],
                "text":    c["text"],
            },
        )
        for i, c in enumerate(all_chunks)
    ]
    for i in range(0, len(points), BATCH_SIZE):
        qdrant.upsert(collection_name=COLLECTION, points=points[i:i + BATCH_SIZE])
        print(f"  {min(i + BATCH_SIZE, len(points))}/{len(points)} points uploades")

    nb_code = sum(1 for c in all_chunks if c["type"] == "code")
    nb_text = sum(1 for c in all_chunks if c["type"] == "text")
    print(f"OK — {len(points)} chunks indexes dans '{COLLECTION}'.")
    print(f"   dont {nb_code} blocs de code et {nb_text} paragraphes texte.")
