\# 🚀 RAG Enterprise Foundation



A modular Retrieval-Augmented Generation (RAG) backbone designed for enterprise systems.



---



\## 🧠 Architecture Overview



User Query  

↓  

Embedding Layer (MiniLM - Hugging Face)  

↓  

FAISS Vector Store (Semantic Retrieval)  

↓  

Context Assembly  

↓  

LLM (Flan-T5)  

↓  

Final Answer  



---



\## 📂 Project Structure



```

rag\_system/

│

├── core/

│   ├── embedding\_client.py

│   ├── llm\_client.py

│

├── rag/

│   ├── vector\_store.py

│

├── main.py

├── .gitignore

```



---



\## 🔧 Setup Instructions



\### 1️⃣ Create Virtual Environment



```bash

python -m venv venv

venv\\Scripts\\activate

```



\### 2️⃣ Install Dependencies



```bash

pip install sentence-transformers torch transformers faiss-cpu

```



\### 3️⃣ Run the System



```bash

python main.py

```



---



\## ⚙️ Components



\### 🔹 Embedding Layer

\- Model: `all-MiniLM-L6-v2`

\- Converts text into 384-dimensional semantic vectors.



\### 🔹 Vector Store

\- FAISS (IndexFlatL2)

\- Stores embeddings

\- Performs top-k similarity search



\### 🔹 LLM Layer

\- Model: `google/flan-t5-base`

\- Generates answers using retrieved context



---



\## 🎯 Current Status



✅ Local Embedding Layer  

✅ FAISS Retrieval Backbone  

✅ End-to-End RAG Flow  

⬜ Registry Layer (Next)  

⬜ Canonical DB Integration (Next)  



---



\## 📌 Future Enhancements



\- Intent Classification (Registry Layer)

\- Structured JSON Output

\- Database Integration

\- Model Provider Abstraction

\- Scalable Vector DB (Pinecone / Weaviate)



---



\## 👨‍💻 Author



Shivam Mehta

