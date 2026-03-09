from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# connect to qdrant
client = QdrantClient(host="localhost", port=6333)

# load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# query
query = "sales order for March"

# convert query into embedding
query_vector = model.encode(query)

# search in vector database
results = client.search(
    collection_name="enterprise_docs",
    query_vector=query_vector.tolist(),
    limit=3
)

# print results
for r in results:
    print(r.payload["text"])