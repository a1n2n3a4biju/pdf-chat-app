<img width="656" height="635" alt="image" src="https://github.com/user-attachments/assets/2eb9970d-c571-4d45-ab8b-ac8f96b6131d" />

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
## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/pdf-chat-app.git
cd pdf-chat-app
```

### 2. Install required packages
```bash
pip install langchain langchain-community langchain-text-splitters faiss-cpu pypdf streamlit python-dotenv google-genai numpy
```

### 3. Get your free Gemini API key
- Go to [aistudio.google.com](https://aistudio.google.com)
- Sign in with your Google account
- Click **Get API Key** → **Create API Key**
- Copy your key

### 4. Create your .env file
Create a file called `.env` in the project folder:
GOOGLE_API_KEY=your_gemini_api_key_here

### 5. Run the app
```bash
streamlit run app.py
```

Your browser will open automatically at `http://localhost:8501`

---

## 🚀 How to Use

1. Open the app in your browser
2. Click **Browse files** and upload any PDF
3. Wait for the app to process your PDF
4. Type your question in the chat box
5. Get your answer instantly!

### Example Questions
- *"What is this document about?"*
- *"Summarize the main points"*
- *"What does it say about [any topic]?"*
- *"Explain [any concept from the PDF]"*

---

## 📁 Project Structure
pdf-chat-app/
│
├── app.py              # Main application code
├── requirements.txt    # Python dependencies
├── .gitignore          # Files to exclude from Git
├── .env                # Your API key (never shared)
└── README.md           # This file

---

## ⚙️ Requirements

- Python 3.10 or higher
- Google Gemini API key (free at aistudio.google.com)
- Internet connection for API calls

---

## ⚠️ Important Notes

- Only works with **text-based PDFs** (not scanned images)
- Free Gemini API has rate limits — wait 10-15 seconds between questions
- Never share your `.env` file or API key publicly
- The `.env` file is excluded from GitHub via `.gitignore`

---

## 🔮 Future Improvements

- [ ] Support for multiple PDF uploads
- [ ] Download chat history as text file
- [ ] Show exact page numbers for each answer
- [ ] One-click PDF summary button
- [ ] Support for scanned PDFs using OCR

---

## 👨‍💻 Built With

- [LangChain](https://python.langchain.com) — Document processing framework
- [Google Gemini](https://aistudio.google.com) — AI model for embeddings and answers
- [FAISS](https://github.com/facebookresearch/faiss) — Vector similarity search by Meta
- [Streamlit](https://streamlit.io) — Python web app framework

---





## 📄 License

This project is open source and available under the [MIT License](LICENSE).
