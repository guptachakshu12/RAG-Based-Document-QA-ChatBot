import os
import time
import streamlit as st

from load_documents import (
    load_documents,
    add_documents_to_index,
    retrieve_relevant_documents,
)

from gemini import generate_response
from utils import load_env

from document_manager import (
    add_document,
    list_documents,
    remove_document,
)

from chat_history import (
    save_chat,
    show_chat,
    export_chat,
)


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_env()


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="RAG Based Document Q&A",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    body, .stApp {
        background: #121212;
        color: #e0e0e0;
        font-family: 'Segoe UI', sans-serif;
    }

    h1 {
        background: linear-gradient(
            90deg,
            #1e90ff,
            #00c6ff,
            #8a2be2,
            #ff69b4
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .stFileUploader > div {
        background-color: #2a2a2a;
        border-radius: 10px;
        padding: 10px;
        color: #e0e0e0;
    }

    .stTextInput input {
    background-color: #1e1e1e !important;
    color: #ffffff !important;
    border-radius: 12px;
    padding: 12px;
    font-size: 16px;
    border: 1px solid #444;
}

/* Chat input */

[data-testid="stChatInput"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

[data-testid="stChatInput"] > div {
    background-color: #1e1e1e !important;
    border: 1px solid #444 !important;
    border-radius: 14px !important;
}

[data-testid="stChatInput"] textarea {
    background-color: transparent !important;
    color: #ffffff !important;
    font-size: 16px !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #999999 !important;
    opacity: 1 !important;
}

[data-testid="stChatInput"] textarea:focus {
    color: #ffffff !important;
}

    .stButton button {
        background: linear-gradient(
            90deg,
            #1e90ff,
            #00c6ff
        );
        color: white;
        font-weight: bold;
        border-radius: 12px;
        padding: 10px 25px;
        border: none;
    }

    .chat-container {
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 12px;
        box-shadow: 0px 3px 8px rgba(0,0,0,0.4);
        max-width: 80%;
    }

    .chat-user {
        background-color: #2a2a2a;
        border-left: 5px solid #1e90ff;
        margin-left: auto;
        text-align: right;
    }

    .chat-bot {
        background-color: #333333;
        border-left: 5px solid #00c6ff;
        margin-right: auto;
        text-align: left;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

def initialize_session_state():

    if "history" not in st.session_state:
        st.session_state.history = []

    if "doc_list" not in st.session_state:
        st.session_state.doc_list = []

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "processed_files" not in st.session_state:
        st.session_state.processed_files = set()

    if "removed_files" not in st.session_state:
        st.session_state.removed_files = set()

    if "uploader_key" not in st.session_state:
        st.session_state.uploader_key = 0


# ============================================================
# MAIN
# ============================================================

def main():

    initialize_session_state()

    st.title("RAG Based Document Q&A ChatBot 🤖")


    # ========================================================
    # SIDEBAR - UPLOAD
    # ========================================================

    st.sidebar.header("Upload Documents 📄")

    uploaded_files = st.sidebar.file_uploader(
        "Upload .txt, .pdf, .docx, .xlsx files",
        type=["txt", "pdf", "docx", "xlsx"],
        accept_multiple_files=True,
        key=f"document_uploader_{st.session_state.uploader_key}",
    )


    # ========================================================
    # PROCESS NEW FILES
    # ========================================================

    if uploaded_files:

        new_files = []

        for uploaded_file in uploaded_files:

            filename = uploaded_file.name

            # Don't process files that were already processed
            # Don't immediately re-add a file that was removed
            if (
                filename not in st.session_state.processed_files
                and filename not in st.session_state.removed_files
            ):
                new_files.append(uploaded_file)


        if new_files:

            for uploaded_file in new_files:

                filename = uploaded_file.name

                temp_path = os.path.join(
                    "temp",
                    filename
                )


                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())


                # Load document
                load_documents(temp_path)


                # Add filename
                add_document(filename)


                # Mark as processed
                st.session_state.processed_files.add(
                    filename
                )


                # Make sure it isn't marked removed
                st.session_state.removed_files.discard(
                    filename
                )


            # Build index
            add_documents_to_index()


            st.sidebar.success(
                f"{len(new_files)} new file(s) processed and indexed!"
            )


    # ========================================================
    # DOCUMENT MANAGER
    # ========================================================

    st.sidebar.subheader("📂 Your Documents")

    current_documents = list_documents()


    if current_documents:

        for i, doc in enumerate(current_documents):

            ext = doc.split(".")[-1].upper()

            st.sidebar.write(
                f"📄 {doc} ({ext})"
            )


            remove_key = f"remove_{i}_{doc}"


            if st.sidebar.button(
                f"❌ Remove {doc}",
                key=remove_key,
            ):

                # Remove from document list
                remove_document(doc)

                # Mark it as removed so uploader
                # doesn't immediately add it again
                st.session_state.removed_files.add(doc)

                # Remove from processed files
                st.session_state.processed_files.discard(doc)

                # Reset uploader
                st.session_state.uploader_key += 1

                # Rerun app
                st.rerun()


    else:

        st.sidebar.info(
            "No documents uploaded yet."
        )


    # ========================================================
    # EXPORT DOCUMENT LIST
    # ========================================================

    if st.sidebar.button("📤 Export Document List"):

        doc_list = "\n".join(
            list_documents()
        )

        st.sidebar.download_button(
            "Download Docs",
            doc_list,
            "documents_list.txt",
            mime="text/plain",
        )


    # ========================================================
    # CHAT
    # ========================================================

    st.header("Chat 💬")

    user_query = st.chat_input(
        "Ask something about your documents..."
    )


    if user_query:

        st.session_state.history.append(
            {
                "user": user_query
            }
        )


        with st.spinner("Chatbot is typing..."):

            time.sleep(0.5)

            retrieved_docs = retrieve_relevant_documents(
                user_query
            )


            bot_response = generate_response(
                user_query,
                retrieved_docs,
                st.session_state.history,
            )


        st.session_state.history.append(
            {
                "bot": bot_response
            }
        )


        save_chat(
            user_query,
            bot_response
        )


    # ========================================================
    # DISPLAY CHAT
    # ========================================================

    for chat in st.session_state.history:

        if "user" in chat:

            st.markdown(
                f"""
                <div class="chat-container chat-user">
                    <strong>You:</strong>
                    {chat["user"]}
                </div>
                """,
                unsafe_allow_html=True,
            )


        elif "bot" in chat:

            st.markdown(
                f"""
                <div class="chat-container chat-bot">
                    <strong>Chatbot:</strong>
                    {chat["bot"]}
                </div>
                """,
                unsafe_allow_html=True,
            )


    # ========================================================
    # CHAT HISTORY
    # ========================================================

    st.sidebar.subheader("🗂 Chat History")

    show_chat()


    # ========================================================
    # SEARCH CHAT HISTORY
    # ========================================================

    search_term = st.sidebar.text_input(
        "🔍 Search Chat History"
    )


    if search_term and "chat_history" in st.session_state:

        for i, chat in enumerate(
            st.session_state.chat_history
        ):

            if (
                search_term.lower()
                in chat["query"].lower()
                or
                search_term.lower()
                in chat["answer"].lower()
            ):

                st.sidebar.markdown(
                    f"**Q{i + 1}: {chat['query']}**"
                )

                st.sidebar.write(
                    chat["answer"]
                )


    # ========================================================
    # EXPORT CHAT
    # ========================================================

    if st.sidebar.button("📤 Export Chat"):

        exported_text = export_chat()

        st.sidebar.download_button(
            "Download Chat",
            exported_text,
            "chat_history.txt",
            mime="text/plain",
        )


    # ========================================================
    # CLEAR CHAT
    # ========================================================

    st.divider()

    if st.button("🗑️ Clear Chat"):

        st.session_state.history = []

        st.rerun()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    if not os.path.exists("temp"):
        os.makedirs("temp")

    main()