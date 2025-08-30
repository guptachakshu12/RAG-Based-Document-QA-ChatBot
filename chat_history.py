import streamlit as st

def save_chat(query, answer):
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    st.session_state.chat_history.append({"query": query, "answer": answer})

def show_chat():
    if "chat_history" in st.session_state:
        for i, chat in enumerate(st.session_state.chat_history):
            with st.expander(f"Q{i+1}: {chat['query']}"):
                st.write(chat["answer"])

def export_chat():
    if "chat_history" not in st.session_state:
        return ""
    text = ""
    for chat in st.session_state.chat_history:
        text += f"Q: {chat['query']}\nA: {chat['answer']}\n\n"
    return text
