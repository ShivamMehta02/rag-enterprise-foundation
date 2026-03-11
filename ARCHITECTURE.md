Enterprise RAG Data Pipeline



Data Sources

-------------

ERP Systems

Inventory Databases

Customer Records

Product Catalog



Ingestion Layer

---------------

Batch ingestion jobs

Kafka streaming events



ETL Layer

---------

Transform raw structured data

Convert to semantic documents



Embedding Layer

---------------

SentenceTransformers model

384 dimensional embeddings



Vector Database

---------------

Qdrant



Stores:

\- vectors

\- metadata

\- document text



Retrieval Pipeline

------------------

Query embedding

Vector search

Metadata filtering

Reranking



LLM Layer

---------

Llama3 via Ollama



API Layer

---------

FastAPI



UI Layer

--------

Web chat interface



Future Improvements

-------------------

Hybrid retrieval

Distributed vector DB

Kafka streaming ingestion

Role based access

