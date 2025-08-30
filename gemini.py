import google.generativeai as genai
import os
from utils import load_env

# Load environment variables
load_env()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Configure Gemini model
generation_config = {
    "temperature": 0.2,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 1024,
    "response_mime_type": "text/plain",
}

gemini_model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

def generate_response(query, retrieved_docs, chat_history=None, top_k=5):
    if not retrieved_docs:
        return "No relevant documents found for your query."

    # Format chat history
    formatted_history = ""
    if chat_history:
        for turn in chat_history:
            if "user" in turn:
                formatted_history += f"User: {turn['user']}\n"
            if "bot" in turn:
                formatted_history += f"Bot: {turn['bot']}\n"

    # Safely extract chunks (handle dict or string)
    context_chunks = []
    for doc in retrieved_docs[:top_k]:
        if isinstance(doc, dict) and "chunk" in doc:
            context_chunks.append(doc["chunk"])
        else:
            context_chunks.append(str(doc))
    context = "\n".join(context_chunks)

    prompt = f"""
You are an intelligent assistant. Use the context below to answer the user's query concisely.

Context:
{context}

Conversation History:
{formatted_history}

User Query:
{query}

Answer:
"""

    chat_session = gemini_model.start_chat(history=[])
    try:
        response = chat_session.send_message(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, I couldn't generate a response."
