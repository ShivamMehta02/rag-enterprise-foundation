from registry.zoho_etl import fetch_zoho_documents
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

# embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# connect to qdrant
client = QdrantClient(host="localhost", port=6333)

COLLECTION_NAME = "enterprise_docs"

def ingest():

    docs = fetch_zoho_documents()

    print(f"Fetched {len(docs)} documents from Zoho")

    points = []

    for i, doc in enumerate(docs):

        text = doc["text"]
        metadata = doc["metadata"]

        vector = model.encode(text)

        points.append(
            PointStruct(
                id=i,
                vector=vector.tolist(),
                payload={
                    "text": text,
                    **metadata
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print("Documents inserted into Qdrant")

if __name__ == "__main__":
    ingest()