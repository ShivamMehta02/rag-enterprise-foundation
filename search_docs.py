from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# connect to qdrant
client = QdrantClient(host="localhost", port=6333)

# load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

print("\n==============================")
print(" Enterprise Vector Search")
print("==============================\n")

# ---------------------------------------
# show available organisations
# ---------------------------------------

orgs = set()

scroll = client.scroll(
    collection_name="enterprise_docs",
    limit=200
)

points = scroll[0]

for p in points:
    orgs.add(p.payload.get("org_id"))

print("Available Organisations:")
for o in sorted(orgs):
    print(f"  - {o}")

print("\nAvailable Filters:")
print("  org_id  → organisation isolation")
print("  brand   → product brand")
print("  price   → max price filter")

print("\nExample query:")
print("  org_id = org_2")
print("  query  = router")
print("  brand  = NetLink")
print("  price  = 6000\n")

# ---------------------------------------
# user inputs
# ---------------------------------------

org_id = input("Enter organisation id: ").strip()

query = input("Enter search query: ").strip()

brand = input("Filter by brand (press enter to skip): ").strip()

price_limit = input("Max price filter (press enter to skip): ").strip()

# ---------------------------------------
# embedding
# ---------------------------------------

query_vector = model.encode(query)

# ---------------------------------------
# build filters
# ---------------------------------------

must_filters = [
    {
        "key": "org_id",
        "match": {"value": org_id}
    }
]

if brand:
    must_filters.append({
        "key": "brand",
        "match": {"value": brand}
    })

if price_limit:
    must_filters.append({
        "key": "price",
        "range": {"lte": int(price_limit)}
    })

# ---------------------------------------
# search
# ---------------------------------------

results = client.search(
    collection_name="enterprise_docs",
    query_vector=query_vector.tolist(),
    limit=5,
    query_filter={
        "must": must_filters
    }
)

# ---------------------------------------
# show results
# ---------------------------------------

print("\nResults:\n")

if not results:
    print("No matching records found.")
else:
    for r in results:
        payload = r.payload
        print(
            f"{payload['text']} "
            f"(org: {payload['org_id']}, brand: {payload['brand']}, price: {payload['price']})"
        )