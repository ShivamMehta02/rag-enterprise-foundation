from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection


class MilvusVectorStore:

    def __init__(self, collection_name="rag_collection", dim=384):

        connections.connect(
            alias="default",
            host="localhost",
            port="19530"
        )

        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dim)
        ]

        schema = CollectionSchema(fields)

        self.collection = Collection(
            name=collection_name,
            schema=schema
        )

    def insert(self, embeddings):
        data = [embeddings]
        self.collection.insert(data)

    def search(self, query_embedding, top_k=3):

        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}

        results = self.collection.search(
            data=[query_embedding],
            anns_field="embedding",
            param=search_params,
            limit=top_k
        )

        return results