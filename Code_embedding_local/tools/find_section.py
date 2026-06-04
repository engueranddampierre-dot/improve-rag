from dotenv import load_dotenv
from qdrant_client import QdrantClient

# This tool allows you to find all chunks from a section
# Be careful with the limit in qdrant.scroll as well as with the type condition, set for text by default but you can change it to code or remove it to get all types of chunks.

# --- Config ---
load_dotenv()
COLLECTION = "maude_manual"

# --- Clients ---
qdrant      = QdrantClient(url="http://localhost:6333")

# --- Finding ---
section = input("Indicate the section you want to find (e.g., '4.3'): ")

r = [c for c in qdrant.scroll(collection_name=COLLECTION, limit=10000, with_payload=True, with_vectors=False)[0]
     if c.payload['section'].startswith(section)]
print(len(r), f"chunks en {section}")
for c in r: 
    print(c.payload['section'], '|', c.payload['text'])