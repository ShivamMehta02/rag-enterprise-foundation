# Enterprise RAG Inventory Assistant

This project implements an **Enterprise Retrieval-Augmented Generation (RAG) AI assistant** capable of answering inventory questions using semantic search and a local LLM.

The system retrieves relevant enterprise inventory data from a vector database and uses an LLM to generate grounded answers.

---

## Architecture

User Query
↓
Query Parser
↓
Embedding Model (Sentence Transformers)
↓
Vector Search (Qdrant)
↓
Metadata Filtering
↓
Reranker
↓
LLM (Llama3 via Ollama)
↓
Final Response

---

## Features

- Semantic search over enterprise inventory
- Multi-tenant organization isolation
- Metadata filtering (brand, price)
- Reranked retrieval results
- Local LLM reasoning
- FastAPI backend
- Web chat interface

---

## Tech Stack

Backend:
- Python
- FastAPI

AI / ML:
- Sentence Transformers
- CrossEncoder reranker
- Llama3 via Ollama

Vector Database:
- Qdrant

Frontend:
- HTML + JavaScript

---

## Project Structure
rag_system
│
├── api_server.py
├── ask_enterprise_ai.py
├── query_parser.py
├── reranker.py
├── ingest_mock_data.py
├── search_docs.py
│
├── rag/
│ ├── vector_store.py
│ ├── qdrant_store.py
│ └── milvus_store.py
│
├── static/
│ └── index.html
│
└── README.md
## Example Queries


keyboard
device used for typing
gaming input hardware
cheap device for typing from technova


---

## Running the System

Start Qdrant


docker run -p 6333:6333 qdrant/qdrant


Start API server


uvicorn api_server:app --reload


Open chat UI


http://127.0.0.1:8000


---

## Example Response

Query:


cheap device for typing from technova


Response:


The Gaming Keyboard MK87 from Technova costs 3499 rupees.


---

## Future Improvements

- Hybrid search (vector + keyword)
- Query understanding improvements
- Better metadata ranking
- Authentication and multi-org login
- Deployment with Docker

---

## Author

Shivam Mehta
