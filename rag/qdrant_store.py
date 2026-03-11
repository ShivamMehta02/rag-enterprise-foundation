from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


class QdrantVectorStore:

    def __init__(self, collection_name="enterprise_docs", dim=384):

        # connect to running docker qdrant
        self.client = QdrantClient(host="localhost", port=6333)

        self.collection_name = collection_name

        # create collection only if it does not exist
        if not self.client.collection_exists(collection_name):

            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=dim,
                    distance=Distance.COSINE
                ),
            )

    def insert(self, embeddings, payloads):

        points = []

        for i, emb in enumerate(embeddings):

            points.append({
                "id": i,
                "vector": emb,
                "payload": payloads[i]
            })

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def search(self, query_vector, org_id, top_k=3):

        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k,
            query_filter={
                "must": [
                    {
                        "key": "org_id",
                        "match": {"value": org_id}
                    }
                ]
            }
        )

        return results