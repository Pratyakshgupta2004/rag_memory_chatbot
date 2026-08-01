import os
import uuid
import streamlit as st
from dotenv import load_dotenv
from google import genai

from database import save_memory, search_memory

st.set_page_config(
    page_title="Long-Term Memory Chatbot",
    page_icon="🤖",
)

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY not found in .env file")
    st.stop()

client = genai.Client(api_key=api_key)

st.title("🤖 Long-Term Memory Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("Type your message...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.write(question)

    memories = search_memory(question)
    memory_text = "\n".join(memories) if isinstance(memories, list) else str(memories)

    prompt = f"""
You are a helpful AI assistant.

Long-Term Memory:
{memory_text}

Conversation:
"""

    for msg in st.session_state.messages:
        prompt += f"{msg['role']}: {msg['content']}\n"

    try:
        response = client.models.generate_content(
            model="models/gemini-3.6-flash",
            contents=prompt,
        )
        answer = response.text

        st.session_state.messages.append({"role": "assistant", "content": answer})

        with st.chat_message("assistant"):
            st.write(answer)

        memory_prompt = f"""
Extract only useful long-term information from the user's message.

Examples:
- Name
- Age
- Profession
- Goals
- Preferences
- Skills
- Interests

If nothing is important return ONLY:

NONE

Message:
{question}
"""

        extracted_response = client.models.generate_content(
            model="models/gemini-3.6-flash",
            contents=memory_prompt,
        )
        extracted = (extracted_response.text or "NONE").strip()

        if extracted.upper() != "NONE":
            save_memory(extracted, str(uuid.uuid4()))

    except Exception as error:
        st.error(f"Error: {error}")
