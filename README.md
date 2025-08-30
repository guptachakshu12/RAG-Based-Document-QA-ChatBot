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

<img width="796" height="342" alt="image" src="https://github.com/user-attachments/assets/aa95d23a-f5e3-47c1-b7a8-3a049e233fb2" />
ADDING MULTIPLE DOCUMENTS

<img width="744" height="568" alt="image" src="https://github.com/user-attachments/assets/9a10d14d-2519-4ead-945e-c7abcfab271f" />
Main Interface

<img width="1275" height="729" alt="image" src="https://github.com/user-attachments/assets/7be25210-e4c0-4844-ac4e-cf61d6d96c42" />
Chat History



