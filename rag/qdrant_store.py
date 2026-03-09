from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


class QdrantVectorStore:

    def __init__(self, collection_name="rag_collection", dim=384):

        self.client = QdrantClient(":memory:")

        self.collection_name = collection_name

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=dim,
                distance=Distance.COSINE
            ),
        )

    def insert(self, embeddings):

        points = []

        for i, emb in enumerate(embeddings):
            points.append({
                "id": i,
                "vector": emb
            })

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def search(self, query_vector, top_k=3):

        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k
        )

        return results