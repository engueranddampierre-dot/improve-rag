from dotenv import load_dotenv
from qdrant_client import QdrantClient

# Allows the user to retrieve chunks from the collection by their IDs, and print the full payload (text, page, type) for each chunk.

# --- Config ---
load_dotenv()
COLLECTION = "maude_manual"

# --- Clients ---
qdrant      = QdrantClient(url="http://localhost:6333")

# --- Retrieval ---
numeros = input("Indicate in the form: integer,integer,... the list of chunks you want to retrieve: ")
liste = [int(x) for x in numeros.split(",")]

points = qdrant.retrieve(
    collection_name=COLLECTION,
    ids=liste,
    with_payload=True,
    with_vectors=False,
)

# --- Display ---
for e in points:
    print(e, "\n\n")