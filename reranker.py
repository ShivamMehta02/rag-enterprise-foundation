from sentence_transformers import CrossEncoder

# Cross encoder reranker
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank(query, documents, top_k=3):

    pairs = [[query, doc] for doc in documents]

    scores = reranker.predict(pairs)

    ranked = sorted(
        zip(documents, scores),
        key=lambda x: x[1],
        reverse=True
    )

    top_docs = [doc for doc, score in ranked[:top_k]]

    return top_docs