from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

COLLECTION_NAME = "enterprise_docs"

model = SentenceTransformer("all-MiniLM-L6-v2")
client = QdrantClient(host="localhost", port=6333)


# ----------------------------------------
# Test dataset
# ----------------------------------------

test_queries = [
    {
        "query": "device used for typing",
        "expected_keyword": "Keyboard"
    },
    {
        "query": "gaming keyboard",
        "expected_keyword": "Keyboard"
    },
    {
        "query": "external storage device",
        "expected_keyword": "SSD"
    },
    {
        "query": "computer display screen",
        "expected_keyword": "Monitor"
    }
]


# ----------------------------------------
# Retrieval function
# ----------------------------------------

def retrieve(query, k=5):

    query_vector = model.encode(query).tolist()

    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=k
    )

    docs = [r.payload["text"] for r in results]

    return docs


# ----------------------------------------
# Evaluation
# ----------------------------------------

def evaluate():

    total = len(test_queries)

    recall_hits = 0
    precision_total = 0
    mrr_total = 0

    for item in test_queries:

        query = item["query"]
        expected = item["expected_keyword"]

        docs = retrieve(query)

        print("\nQuery:", query)

        found = False

        for i, doc in enumerate(docs):

            print(f"{i+1}. {doc}")

            if expected.lower() in doc.lower():

                if not found:
                    recall_hits += 1
                    mrr_total += 1 / (i + 1)
                    found = True

                precision_total += 1

        print("Expected keyword:", expected)

    recall = recall_hits / total
    precision = precision_total / (total * 5)
    mrr = mrr_total / total

    print("\n==============================")
    print("Evaluation Results")
    print("==============================")

    print("Recall@5:", recall)
    print("Precision@5:", precision)
    print("MRR:", mrr)


if __name__ == "__main__":
    evaluate()