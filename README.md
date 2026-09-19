# 🧠 RAG-Based Document QA Chatbot

A production-style AI application that allows users to upload documents and ask natural language questions using **Retrieval-Augmented Generation (RAG)** to deliver accurate, context-aware answers.

> Built to demonstrate real-world RAG pipelines used in AI-powered document search and knowledge systems.

---

## 🚀 Problem Statement
Large Language Models (LLMs) cannot reliably answer questions from **private or long documents** and often hallucinate.  
This project solves that by retrieving only the **most relevant document context** before generating answers.

---

## ✨ Key Features
- 📄 Upload and process multiple documents (PDF, DOCX, TXT)
- 🔍 Semantic search using vector embeddings
- 🧠 FAISS-based vector indexing for fast retrieval
- 🤖 Context-aware responses using LLMs
- 🖥 Interactive Streamlit user interface
- 🔐 Secure API key handling with environment variables

---

## 🛠 Tech Stack
- **Language:** Python  
- **Frontend:** Streamlit  
- **Backend:** FastAPI  
- **LLM:** OpenAI API  
- **Vector Database:** FAISS  
- **Embeddings:** OpenAI Embeddings  
- **Document Parsing:** PyPDF, LangChain  

---

## 🧩 System Architecture
Document Upload
↓
Text Chunking
↓
Embedding Generation
↓
FAISS Vector Store
↓
User Query
↓
Relevant Context Retrieval
↓
LLM Answer Generation

<img width="1901" height="915" alt="Screenshot 2026-09-19 142329" src="https://github.com/user-attachments/assets/1989c9af-608d-4e34-90ab-afb135079394" />


ADDING MULTIPLE DOCUMENTS




<img width="744" height="568" alt="image" src="https://github.com/user-attachments/assets/9a10d14d-2519-4ead-945e-c7abcfab271f" />
Main Interface





<img width="1275" height="729" alt="image" src="https://github.com/user-attachments/assets/7be25210-e4c0-4844-ac4e-cf61d6d96c42" />
Chat History


⚙️ How to Run Locally
1️⃣ Clone the repository
git clone https://github.com/guptachakshu12/RAG-Based-Document-QA-ChatBot
cd RAG-Based-Document-QA-ChatBot

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Set environment variables

Create a .env file in the root directory:

OPENAI_API_KEY=your_api_key_here

4️⃣ Run the application
streamlit run streamlit_app.py

📌 Use Cases

📑 Legal document analysis

🏥 Medical report question answering

📚 Academic research papers

🏢 Internal company knowledge bases

🔮 Future Improvements

User authentication & role-based access

Persistent vector storage (Pinecone / ChromaDB)

Chat history & conversation memory

Cloud deployment with scalable backend

Multi-document comparison support

👨‍💻 Author

Chakshu Gupta
B.Tech Artificial Intelligence & Machine Learning
Aspiring Software Engineer | Full-Stack & AI Developer

🔗 LinkedIn: https://linkedin.com/in/chakshugupta1

📫 Email: chakshugupta05@gmail.com



