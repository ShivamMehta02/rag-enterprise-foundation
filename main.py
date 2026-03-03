from core.embedding_client import EmbeddingClient
from rag.vector_store import VectorStore

if __name__ == "__main__":
    print("Program started")

    embedder = EmbeddingClient()

    documents = [
        "Sales order for March includes laptops and monitors.",
        "Inventory report shows low stock for keyboards.",
        "Customer placed order for 50 units of printers.",
        "April sales increased by 20 percent."
    ]

    print("Generating document embeddings...")
    doc_embeddings = embedder.embed_batch(documents)

    store = VectorStore(dimension=len(doc_embeddings[0]))
    store.add_documents(doc_embeddings, documents)

    query = "Show me March sales"
    print("Embedding query...")
    query_embedding = embedder.embed_text(query)

    results = store.search(query_embedding, k=2)

    print("\nTop Results:")
    for r in results:
        print("-", r)