from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from sentence_transformers import SentenceTransformer

# connect to qdrant
client = QdrantClient(host="localhost", port=6333)

# load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# mock enterprise documents
documents = [
    "Zoho inventory sales order for March includes laptops",
    "April sales increased by 20 percent",
    "Customer invoice generated for order 1452",
    "Warehouse inventory updated after shipment",
    "Purchase order created for supplier electronics"
]

# convert documents into embeddings
embeddings = model.encode(documents)

# prepare vector points
points = []

for i, vector in enumerate(embeddings):
    points.append(
        PointStruct(
            id=i,
            vector=vector.tolist(),
            payload={"text": documents[i]}
        )
    )

# insert into vector database
client.upsert(
    collection_name="enterprise_docs",
    points=points
)

print("Documents inserted successfully")