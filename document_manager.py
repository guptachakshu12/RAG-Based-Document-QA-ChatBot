import streamlit as st
from load_documents import add_documents_to_index, model
import numpy as np
import faiss

# ----------------- Manage Documents -----------------
def add_document(doc_name):
    """Add document name to session list if not already present."""
    if "doc_list" not in st.session_state:
        st.session_state.doc_list = []
    if doc_name not in st.session_state.doc_list:
        st.session_state.doc_list.append(doc_name)

def list_documents():
    """Return the list of document names."""
    return st.session_state.get("doc_list", [])

def remove_document(doc_name):
    """
    Remove a document name and its chunks from session_state,
    then rebuild FAISS index if documents remain.
    """
    # Remove from document list
    if "doc_list" in st.session_state and doc_name in st.session_state.doc_list:
        st.session_state.doc_list.remove(doc_name)

    # Remove document chunks
    if "documents" in st.session_state:
        st.session_state.documents = [
            d for d in st.session_state.documents if d["doc_name"] != doc_name
        ]

    # Rebuild FAISS index
    if st.session_state.documents:
        embeddings = model.encode([d["chunk"] for d in st.session_state.documents])
        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(np.array(embeddings, dtype=np.float32))
        st.session_state.index = index
    else:
        st.session_state.index = None
