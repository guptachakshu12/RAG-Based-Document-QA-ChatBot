import os
import time
import streamlit as st
from load_documents import load_documents, add_documents_to_index, retrieve_relevant_documents
from gemini import generate_response
from utils import load_env
from document_manager import add_document, list_documents, remove_document
from chat_history import save_chat, show_chat, export_chat

load_env()

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="RAG Based Document Q&A",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
body, .stApp { background: #121212; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; }
h1 { background: linear-gradient(90deg, #1e90ff, #00c6ff, #8a2be2, #ff69b4);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: gradient 5s ease infinite; }
@keyframes gradient { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
.sidebar .sidebar-content { background: linear-gradient(180deg, #1f1f1f, #2c2c2c); padding: 25px; border-radius: 12px; }
.stFileUploader > div { background-color: #2a2a2a; border-radius: 10px; padding: 10px; color: #e0e0e0; }
.stTextInput input { background-color: #1e1e1e; color: #ffffff; border-radius: 12px; padding: 12px; font-size: 16px; border: 1px solid #444; }
.stTextInput input::placeholder { color: #bbbbbb; }
.stButton button { background: linear-gradient(90deg, #1e90ff, #00c6ff); color: #ffffff; font-weight: bold; border-radius: 12px; padding: 10px 25px; border: none; transition: all 0.3s ease; }
.stButton button:hover { background: linear-gradient(90deg, #00c6ff, #1e90ff); transform: scale(1.05); }
.chat-container { border-radius: 15px; padding: 15px; margin-bottom: 12px; box-shadow: 0px 3px 8px rgba(0,0,0,0.4); max-width: 80%; }
.chat-user { background-color: #2a2a2a; border-left: 5px solid #1e90ff; margin-left: auto; text-align: right; }
.chat-bot { background-color: #333333; border-left: 5px solid #00c6ff; margin-right: auto; text-align: left; }
.loading-dots::after { content: '...'; animation: dots 1s steps(5, end) infinite; }
@keyframes dots { 0%, 20% { content: ''; } 40% { content: '.'; } 60% { content: '..'; } 80%, 100% { content: '...'; } }
a { color: #1e90ff; text-decoration: none; }
</style>
""", unsafe_allow_html=True)


def main():
    st.title("RAG Based Document Q&A ChatBot 🤖")

    # --- SIDEBAR: Document Upload ---
    st.sidebar.header("Upload Documents 📄")
    uploaded_files = st.sidebar.file_uploader(
        "Upload .txt, .pdf, .docx, .xlsx files",
        type=["txt", "pdf", "docx", "xlsx"],
        accept_multiple_files=True
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            temp_path = f"temp/{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.read())

            load_documents(temp_path)
            add_document(uploaded_file.name)

        add_documents_to_index()
        st.sidebar.success(f"{len(uploaded_files)} file(s) processed and indexed!")

    # --- SIDEBAR: Document Manager ---
    st.sidebar.subheader("📂 Your Documents")
    for i, doc in enumerate(list_documents()):
        ext = doc.split('.')[-1].upper()
        st.sidebar.write(f"📄 {doc} ({ext})")
        remove_key = f"remove_{i}_{doc}"  # unique key
        if st.sidebar.button(f"❌ Remove {doc}", key=remove_key):
            remove_document(doc)
            st.experimental_rerun()

    # --- EXPORT DOCUMENT LIST ---
    if st.sidebar.button("📤 Export Document List"):
        doc_list = "\n".join(list_documents())
        st.sidebar.download_button("Download Docs", doc_list, "documents_list.txt")

    # --- CHAT HISTORY ---
    if "history" not in st.session_state:
        st.session_state.history = []

    # --- CHAT INTERFACE ---
    st.header("Chat 💬")
    user_query = st.chat_input("Ask something about your documents...")

    if user_query:
        st.session_state.history.append({"user": user_query})
        with st.spinner("Chatbot is typing..."):
            time.sleep(1)
            retrieved_docs = retrieve_relevant_documents(user_query)
            bot_response = generate_response(user_query, retrieved_docs, st.session_state.history)

        st.session_state.history.append({"bot": bot_response})
        save_chat(user_query, bot_response)

    # --- DISPLAY CHAT HISTORY ---
    for chat in st.session_state.history:
        if "user" in chat:
            st.markdown(
                f'<div class="chat-container chat-user"><strong>You:</strong> {chat["user"]}</div>',
                unsafe_allow_html=True
            )
        elif "bot" in chat:
            st.markdown(
                f'<div class="chat-container chat-bot"><strong>Chatbot:</strong> {chat["bot"]}</div>',
                unsafe_allow_html=True
            )

    # --- SHOW SAVED CHAT HISTORY IN SIDEBAR ---
    st.sidebar.subheader("🗂 Chat History")
    show_chat()

    # --- SEARCH CHAT HISTORY ---
    search_term = st.sidebar.text_input("🔍 Search Chat History")
    if search_term and "chat_history" in st.session_state:
        for i, chat in enumerate(st.session_state.chat_history):
            if search_term.lower() in chat["query"].lower() or search_term.lower() in chat["answer"].lower():
                st.sidebar.markdown(f"**Q{i+1}: {chat['query']}**")
                st.sidebar.write(chat["answer"])

    # --- EXPORT CHAT HISTORY ---
    if st.sidebar.button("📤 Export Chat"):
        exported_text = export_chat()
        st.sidebar.download_button("Download Chat", exported_text, "chat_history.txt")

# --- CLEAR CHAT BUTTON ---
if st.button("Clear Chat"):
    st.session_state.history = []
    if "user_query" in st.session_state:
        del st.session_state.user_query

if __name__ == "__main__":
    if not os.path.exists("temp"):
        os.makedirs("temp")
    main()
