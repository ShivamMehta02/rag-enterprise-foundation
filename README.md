Enterprise AI Assistant (RAG System)

An Enterprise Retrieval-Augmented Generation (RAG) assistant that allows users to query enterprise inventory data using natural language.

The system retrieves relevant business records from a vector database (Qdrant) and uses a local LLM (Llama3 via Ollama) to generate accurate answers grounded in enterprise data.

Features

Semantic search over enterprise inventory

Multi-tenant architecture (organization isolation)

Metadata filtering (brand, price)

Vector database using Qdrant

Local LLM inference using Ollama + Llama3

Interactive enterprise chatbot

Hybrid search (semantic + structured filters)

System Architecture
User Query
    ↓
SentenceTransformer Embedding
    ↓
Vector Search (Qdrant)
    ↓
Metadata Filtering
(org_id, brand, price)
    ↓
Context Retrieval
    ↓
Prompt Construction
    ↓
Llama3 (Ollama)
    ↓
Final AI Answer
Technologies Used

Python

SentenceTransformers

Qdrant Vector Database

Ollama (Llama3)

Docker

FAISS (initial experimentation)

Project Structure
rag_system
│
├── ask_enterprise_ai.py        # Enterprise chatbot
├── search_docs.py              # Vector search testing
├── ingest_mock_data.py         # Mock data generator
├── create_collection.py        # Qdrant collection creation
│
├── rag/
│   ├── qdrant_store.py
│   ├── milvus_store.py
│   └── vector_store.py
│
├── core/
│   ├── embedding_client.py
│   └── llm_client.py
│
├── registry/
│   └── zoho_etl.py
│
└── README.md
Mock Data Setup

The system generates enterprise-like mock data to simulate multiple organizations.

Configuration:

10 Organizations
10 Records per Organization
Total = 100 Vector Documents

Each stored document contains:

text
org_id
brand
sku
price
embedding vector (384 dimensions)
Setup Instructions
1. Start Qdrant

Run the vector database using Docker:

docker run -p 6333:6333 qdrant/qdrant

Open dashboard:

http://localhost:6333/dashboard
2. Activate Python Environment
venv\Scripts\activate
3. Insert Mock Data
python ingest_mock_data.py

This creates 100 vector records across 10 organizations.

4. Run the Enterprise AI Assistant
python ask_enterprise_ai.py
Example Interaction
Enterprise AI Assistant

Available Organisations:
- org_1
- org_2
- org_3
...

Enter your organisation id:
org_3

Ask about inventory:
router

Brand filter:
NetLink

Max price filter:
6000

AI Response:

The NetLink router with SKU NL-RT-21 costs 5400 rupees.
Key Capabilities
Semantic Search

Users can query inventory using natural language.

Example:

gaming keyboard
wireless router
cheap monitor
Multi-Tenant Data Isolation

Each organization only sees its own data.

org_1 → only org_1 inventory
org_2 → only org_2 inventory
Hybrid Filtering

Search combines:

vector similarity
+
metadata filters

Filters supported:

brand
price
organization
Future Improvements

Automatic filter extraction from natural language

Support additional enterprise entities:

orders

customers

invoices

Reranking models for better retrieval

Web dashboard UI

API integration with Zoho ERP

Author

Shivam
AI / ML Engineer (AIML)

License

MIT License

Repository Purpose

This repository demonstrates a production-style Retrieval-Augmented Generation system for enterprise AI assistants, combining vector databases, semantic search, and LLM reasoning.