# Long-Term Memory Chatbot

This is a small Streamlit chatbot that can remember useful details from earlier chats. Instead of only using the messages visible in the current session, it stores important information in a local vector database and brings it back when it is relevant.

For example, if someone says that their name is Pratyaksh Gupta and they are interested in RAG, the chatbot can use that information later when asked about the user's name or interests.

## What it uses

- **Streamlit** for the chat interface
- **Gemini API** for generating replies and identifying useful facts
- **ChromaDB** for saving memories locally
- **Sentence Transformers** to convert text into embeddings for similarity search

## How it works

1. The user sends a message through the Streamlit page.
2. The app searches ChromaDB for older memories related to that message.
3. Relevant memories and the recent conversation are sent to Gemini.
4. Gemini generates a context-aware reply.
5. A second Gemini request checks whether the user's message includes a useful long-term fact, such as a name, preference, goal, skill, or interest.
6. If a useful fact is found, it is embedded and saved in `memory_db/`.

The saved database remains on disk, so memories can still be found after restarting the app.

## Project files

```text
rag_memory_chatbot/
├── app.py              # Streamlit app and Gemini calls
├── database.py         # ChromaDB storage and memory search
├── requirements.txt    # Python packages needed for the project
├── .env                # Gemini API key 
└── memory_db/          # Local ChromaDB data created while the app runs
```

## Run the app

```bash
streamlit run app.py
```

Open the local URL shown in the terminal, usually `http://localhost:8501`.

## Quick memory test

Send a message such as:

```text
My name is Pratyaksh Gupta and I like RAG projects.
```

Then restart the app and ask:

```text
What is my name and what kind of projects do I like?
```

If the chatbot answers using the earlier information, the memory retrieval is working.
