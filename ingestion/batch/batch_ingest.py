import random
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from ingestion.etl.transform_inventory import transform_inventory_record

model = SentenceTransformer("all-MiniLM-L6-v2")
client = QdrantClient(host="localhost", port=6333)

COLLECTION = "enterprise_docs"

brands = ["Technova","NetLink","DisplayTech","CoreSystems"]
products = ["Keyboard","Monitor","SSD","Router","Laptop"]


def generate_records():

    data = []

    for org in range(1,11):

        for i in range(10):

            record = {
                "org_id": f"org_{org}",
                "sku": f"SKU-{org}-{i}",
                "brand": random.choice(brands),
                "product": random.choice(products),
                "price": random.randint(2000,20000)
            }

            data.append(record)

    return data


def run_batch_ingestion():

    records = generate_records()

    points = []

    for i,record in enumerate(records):

        text,metadata = transform_inventory_record(record)

        vector = model.encode(text).tolist()

        points.append({
            "id": i,
            "vector": vector,
            "payload": {
                "text": text,
                **metadata
            }
        })

    client.upsert(
        collection_name=COLLECTION,
        points=points
    )

    print("Batch ingestion completed")
    print("Documents indexed:",len(points))


if __name__ == "__main__":
    run_batch_ingestion()