from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import random

# connect to qdrant
client = QdrantClient(host="localhost", port=6333)

# embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

collection_name = "enterprise_docs"

brands = [
    "Technova", "PrintCorp", "NetLink",
    "DisplayTech", "DataPro", "UltraSys",
    "NextGen", "LogicWorks", "CloudTech", "CoreSystems"
]

products = [
    "SSD", "Keyboard", "Mouse", "Router", "Printer",
    "Monitor", "Server", "Dock", "GPU", "Laptop"
]

points = []
point_id = 1000

for org in range(1, 11):  # 10 organisations

    org_id = f"org_{org}"

    for item in range(1, 11):  # 10 records per org

        brand = random.choice(brands)
        product = random.choice(products)

        sku = f"{brand[:2].upper()}-{product[:2].upper()}-{org}{item}"

        price = random.randint(2000, 20000)

        text = f"{product} from brand {brand} with SKU {sku} costs {price} rupees."

        embedding = model.encode(text).tolist()

        payload = {
            "text": text,
            "org_id": org_id,
            "brand": brand,
            "sku": sku,
            "price": price
        }

        points.append({
            "id": point_id,
            "vector": embedding,
            "payload": payload
        })

        point_id += 1


client.upsert(
    collection_name=collection_name,
    points=points
)

print(f"Inserted {len(points)} records into Qdrant.")