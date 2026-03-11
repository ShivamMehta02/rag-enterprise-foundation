from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
import ollama

from query_parser import extract_filters
from reranker import rerank

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

    query_vector = model.encode(query).tolist()

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

    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=10,
        query_filter={"must": must_filters}
    )

    # collect documents
    documents = [r.payload["text"] for r in results]

    if len(documents) == 0:
        return ""

    # rerank documents
    top_docs = rerank(query, documents)

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

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

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

        # automatic filter extraction
        query, brand, price_limit = extract_filters(user_query)

        print("\nDetected Filters:")
        print("Query:", query)
        print("Brand:", brand)
        print("Price Limit:", price_limit)

        context = retrieve_context(query, org_id, brand, price_limit)

        if context.strip() == "":
            print("\nNo matching records found.\n")
            continue

        answer = ask_llama(query, context)

        print("\nAI Answer:\n")
        print(answer)


# ----------------------------------------

if __name__ == "__main__":
    main()