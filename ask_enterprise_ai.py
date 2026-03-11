from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
import ollama

from query_parser import extract_filters
from reranker import rerank
from metrics import Metrics

# ----------------------------------------
# Metrics
# ----------------------------------------

metrics = Metrics()

# ----------------------------------------
# Configuration
# ----------------------------------------

COLLECTION_NAME = "enterprise_docs"

# embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# connect to qdrant
client = QdrantClient(host="localhost", port=6333)


# ----------------------------------------
# Show available organisations
# ----------------------------------------

def show_available_orgs():

    orgs = set()

    scroll = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=200
    )

    points = scroll[0]

    for p in points:
        orgs.add(p.payload.get("org_id"))

    print("\nAvailable Organisations:\n")

    for o in sorted(orgs):
        print(" -", o)

    return orgs


# ----------------------------------------
# Retrieve context from vector DB
# ----------------------------------------

def retrieve_context(query, org_id, brand=None, price_limit=None):

    # ----------------------------------------
    # Embedding
    # ----------------------------------------

    metrics.start("embedding")

    query_vector = model.encode(query).tolist()

    metrics.end("embedding")

    # ----------------------------------------
    # Build Filters
    # ----------------------------------------

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

    # ----------------------------------------
    # Vector Search
    # ----------------------------------------

    metrics.start("vector_search")

    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=10,
        query_filter={"must": must_filters}
    )

    metrics.end("vector_search")

    # ----------------------------------------
    # Collect documents
    # ----------------------------------------

    documents = [r.payload["text"] for r in results]

    if len(documents) == 0:
        return ""

    # ----------------------------------------
    # Reranking
    # ----------------------------------------

    metrics.start("reranking")

    top_docs = rerank(query, documents)

    metrics.end("reranking")

    # ----------------------------------------
    # Build Context
    # ----------------------------------------

    context = ""

    for doc in top_docs:
        context += doc + "\n"

    return context


# ----------------------------------------
# Ask Llama3
# ----------------------------------------

def ask_llama(query, context):

    prompt = f"""
You are an enterprise inventory assistant.

Use ONLY the information in the context to answer the question.

If the answer is not in the context say:
"I could not find that information in the inventory database."

Context:
{context}

Question:
{query}

Answer clearly and concisely.
"""

    # ----------------------------------------
    # LLM Inference Metrics
    # ----------------------------------------

    metrics.start("llm_inference")

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    metrics.end("llm_inference")

    return response["message"]["content"]


# ----------------------------------------
# Main chatbot loop
# ----------------------------------------

def main():

    print("\n==============================")
    print(" Enterprise AI Assistant")
    print("==============================")

    # show organisations
    valid_orgs = show_available_orgs()

    org_id = input("\nEnter your organisation id: ").strip()

    while org_id not in valid_orgs:
        print("Invalid organisation id.")
        org_id = input("Enter a valid organisation id: ").strip()

    print("\nYou can ask naturally like:")
    print("show NetLink routers under 6000")
    print("gaming keyboard")
    print("cheap monitor\n")

    while True:

        user_query = input("\nAsk about inventory (type 'exit' to quit): ").strip()

        if user_query.lower() == "exit":
            print("\nGoodbye.")
            break

        # ----------------------------------------
        # Query Parsing
        # ----------------------------------------

        query, brand, price_limit = extract_filters(user_query)

        print("\nDetected Filters:")
        print("Query:", query)
        print("Brand:", brand)
        print("Price Limit:", price_limit)

        # ----------------------------------------
        # Retrieval
        # ----------------------------------------

        context = retrieve_context(query, org_id, brand, price_limit)

        if context.strip() == "":
            print("\nNo matching records found.\n")
            continue

        # ----------------------------------------
        # LLM Answer
        # ----------------------------------------

        answer = ask_llama(query, context)

        print("\nAI Answer:\n")
        print(answer)


# ----------------------------------------

if __name__ == "__main__":
    main()