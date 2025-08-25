import os
import pdfplumber
import docx
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Initialize model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize FAISS index
dimension = 384  # embedding size of all-MiniLM-L6-v2
index = faiss.IndexFlatL2(dimension)

# Store documents (will now hold chunks)
documents = []

# ----------------- File Loaders -----------------

def load_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def load_pdf(file_path):
    pdf_text = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pdf_text.append(text.strip())
    return pdf_text

def load_docx(file_path):
    doc = docx.Document(file_path)
    return [para.text.strip() for para in doc.paragraphs if para.text.strip()]

def load_xlsx(file_path):
    excel_text = []
    df = pd.read_excel(file_path)
    for col in df.columns:
        excel_text.extend([str(cell).strip() for cell in df[col] if pd.notnull(cell)])
    return excel_text

# ----------------- Chunking -----------------

def chunk_text(text, chunk_size=1000, overlap=100):
    """Split text into overlapping chunks for better embeddings."""
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

# ----------------- Main Document Loader -----------------

def load_documents(file_path):
    global documents
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".txt":
        raw_doc = load_txt(file_path)
    elif ext == ".pdf":
        raw_doc = load_pdf(file_path)
    elif ext == ".docx":
        raw_doc = load_docx(file_path)
    elif ext == ".xlsx":
        raw_doc = load_xlsx(file_path)
    else:
        print(f"Unsupported file type: {ext}")
        return

    # Join lines/pages into a single string for chunking
    full_text = " ".join(raw_doc)
    chunks = chunk_text(full_text)
    documents.extend(chunks)

# ----------------- FAISS Indexing -----------------

def add_documents_to_index():
    global documents, index
    if not documents:
        print("No documents loaded to index.")
        return
    embeddings = model.encode(documents)
    index.add(np.array(embeddings, dtype=np.float32))
    print(f"Indexed {len(documents)} document chunks.")

# ----------------- Retrieval -----------------

def retrieve_relevant_documents(query, top_k=5):
    global documents, index, model
    if not documents:
        print("No documents loaded.")
        return []

    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding, dtype=np.float32), top_k)
    valid_indices = [i for i in indices[0] if 0 <= i < len(documents)]
    retrieved_docs = [documents[i] for i in valid_indices]
    return retrieved_docs
