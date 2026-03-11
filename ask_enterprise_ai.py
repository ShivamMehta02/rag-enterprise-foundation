from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
import ollama

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
        limit=5,
        query_filter={"must": must_filters}
    )

    context = ""

    for r in results:
        context += r.payload["text"] + "\n"

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

    # show orgs
    valid_orgs = show_available_orgs()

    org_id = input("\nEnter your organisation id: ").strip()

    while org_id not in valid_orgs:
        print("Invalid organisation id.")
        org_id = input("Enter a valid organisation id: ").strip()

    print("\nOptional filters available:")
    print(" - brand")
    print(" - max price")

    while True:

        query = input("\nAsk about inventory (type 'exit' to quit): ").strip()

        if query.lower() == "exit":
            print("\nGoodbye.")
            break

        brand = input("Brand filter (press Enter to skip): ").strip()
        price_limit = input("Max price filter (press Enter to skip): ").strip()

        if brand == "":
            brand = None

        if price_limit == "":
            price_limit = None

        context = retrieve_context(query, org_id, brand, price_limit)

        if context.strip() == "":
            print("\nNo matching records found.\n")
            continue

        # Debug (optional)
        # print("\nRetrieved Context:\n", context)

        answer = ask_llama(query, context)

        print("\nAI Answer:\n")
        print(answer)


# ----------------------------------------

if __name__ == "__main__":
    main()