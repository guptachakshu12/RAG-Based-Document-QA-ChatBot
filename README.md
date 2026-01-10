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


<img width="796" height="342" alt="image" src="https://github.com/user-attachments/assets/aa95d23a-f5e3-47c1-b7a8-3a049e233fb2" />
ADDING MULTIPLE DOCUMENTS




<img width="744" height="568" alt="image" src="https://github.com/user-attachments/assets/9a10d14d-2519-4ead-945e-c7abcfab271f" />
Main Interface





<img width="1275" height="729" alt="image" src="https://github.com/user-attachments/assets/7be25210-e4c0-4844-ac4e-cf61d6d96c42" />
Chat History



