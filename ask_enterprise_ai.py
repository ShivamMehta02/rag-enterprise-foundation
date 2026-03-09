from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
import ollama

# embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# connect to qdrant
client = QdrantClient(host="localhost", port=6333)

COLLECTION_NAME = "enterprise_docs"


def retrieve_context(query):

    query_vector = model.encode(query).tolist()

    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=3
    )

    context = ""

    for r in results:
        context += r.payload["text"] + "\n"

    return context


def ask_llama(query, context):

    prompt = f"""
You are an enterprise inventory assistant.

Use the following context to answer the question.

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


def main():

    print("Enterprise AI Assistant Ready")

    while True:

        query = input("\nAsk about inventory: ")

        context = retrieve_context(query)

        answer = ask_llama(query, context)

        print("\nAI Answer:\n")
        print(answer)


if __name__ == "__main__":
    main()