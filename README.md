RAG-Based Document Q&A System

A Retrieval-Augmented Generation (RAG) system that allows users to upload documents (PDFs, text files, etc.) and interact with them through natural language queries. The system uses the Gemini API for generating responses and integrates document retrieval for context-aware answers.

Features:

Upload and index documents (PDF, TXT, etc.)
Retrieve relevant document chunks for queries
Generate context-aware answers using Gemini LLM
Store and manage chat history
Easy to run with Streamlit frontend

📂 Project Structure

├── app.py                # Main Streamlit app
├── chat_history.py       # Handles saving & retrieving chat history
├── document_manager.py   # Document indexing and management
├── gemini.py             # Gemini API integration
├── load_documents.py     # Loading and preprocessing documents
├── utils.py              # Helper functions
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (API keys, etc.)
├── README.md             # Project documentation
└── temp/                 # Temporary file storage


📖 Usage
Upload documents (PDF/TXT).
Ask questions in natural language.
The system retrieves relevant context and generates accurate answers.
Previous conversations are stored in chat history.

✅ Requirements
Python 3.9+
Streamlit
pdfplumber
dotenv
Gemini API access
(All dependencies are listed in requirements.txt)

🔮 Future Scope
Support for more document types (DOCX, CSV)
Advanced vector databases (e.g., FAISS, Pinecone)
User authentication
Multi-user chat history management
