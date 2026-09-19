import streamlit as st


def add_document(doc_name):
    """Add document name to the session document list."""
    if "doc_list" not in st.session_state:
        st.session_state.doc_list = []

    if doc_name not in st.session_state.doc_list:
        st.session_state.doc_list.append(doc_name)


def list_documents():
    """Return uploaded document names."""
    return st.session_state.get("doc_list", [])


def remove_document(doc_name):
    """
    Remove a document from the displayed document list.

    The actual FAISS index is rebuilt by load_documents.py.
    """
    if "doc_list" in st.session_state:
        if doc_name in st.session_state.doc_list:
            st.session_state.doc_list.remove(doc_name)