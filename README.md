📄 PDF Chat App

An AI-powered application that lets you upload any PDF and have a conversation with it using Google Gemini AI and RAG (Retrieval Augmented Generation) technology.

🎯 What This App Does

- Upload any PDF document
- Ask questions about its content in plain English
- Get accurate answers pulled directly from your PDF
- See exactly how many pages and chunks were processed



🖥️ Demo

> Upload a PDF → Ask questions → Get instant AI-powered answers



🧠 How It Works

This app uses a technique called **RAG (Retrieval Augmented Generation)**:

1. **Upload** — You upload a PDF file
2. **Read** — App reads and splits PDF into small chunks
3. **Embed** — Each chunk is converted into numbers (embeddings) using Gemini
4. **Store** — Embeddings are stored in a FAISS vector database
5. **Search** — When you ask a question, app finds the most relevant chunks
6. **Answer** — Google Gemini reads those chunks and generates an accurate answer

---
 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core programming language |
| Streamlit | Web interface |
| LangChain | Document loading and splitting |
| FAISS | Vector storage and similarity search |
| Google Gemini API | Embeddings and text generation |
| python-dotenv | Secure API key management |

---
