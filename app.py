import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from google import genai
import tempfile
import os
import numpy as np
import time

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(page_title="PDF Chat App", page_icon="📄", layout="centered")

st.markdown("""
<style>
.stApp { background-color: #F1EFE8; }
header[data-testid="stHeader"] { background: transparent; }

.app-header {
    background: #534AB7;
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 16px;
}
.app-header-icon {
    width: 52px; height: 52px;
    background: #EEEDFE;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 26px; flex-shrink: 0;
}
.app-header h1 { color: #EEEDFE; font-size: 22px; font-weight: 600; margin: 0; }
.app-header p  { color: #AFA9EC; font-size: 13px; margin: 3px 0 0; }

.stats-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-bottom: 1rem;
}
.stat-card { border-radius: 12px; padding: 14px; text-align: center; }
.stat-pages   { background: #FBEAF0; }
.stat-chunks  { background: #E1F5EE; }
.stat-questions { background: #FAEEDA; }
.stat-num-pages     { font-size: 26px; font-weight: 700; color: #993556; }
.stat-num-chunks    { font-size: 26px; font-weight: 700; color: #0F6E56; }
.stat-num-questions { font-size: 26px; font-weight: 700; color: #854F0B; }
.stat-lbl-pages     { font-size: 12px; color: #72243E; margin-top: 2px; }
.stat-lbl-chunks    { font-size: 12px; color: #085041; margin-top: 2px; }
.stat-lbl-questions { font-size: 12px; color: #633806; margin-top: 2px; }

.pdf-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: #EEEDFE; color: #3C3489;
    border-radius: 8px; padding: 6px 14px;
    font-size: 13px; font-weight: 500;
    margin-bottom: 1rem;
}

.chat-container {
    background: white;
    border-radius: 16px;
    padding: 1.25rem;
    border: 1px solid #CECBF6;
    margin-bottom: 1rem;
}
.chat-label {
    font-size: 11px; font-weight: 600;
    color: #888780; letter-spacing: 0.07em;
    margin-bottom: 1rem;
}
.user-msg {
    background: #534AB7; color: #EEEDFE;
    padding: 10px 16px;
    border-radius: 16px 16px 4px 16px;
    font-size: 14px; max-width: 78%;
    margin-left: auto; margin-bottom: 8px;
    line-height: 1.6;
}
.ai-msg {
    background: #F1EFE8; color: #2C2C2A;
    padding: 10px 16px;
    border-radius: 16px 16px 16px 4px;
    font-size: 14px; max-width: 78%;
    margin-bottom: 4px;
    line-height: 1.6;
}
.source-chip {
    display: inline-block;
    background: #E1F5EE; color: #0F6E56;
    font-size: 11px; padding: 3px 10px;
    border-radius: 20px;
    margin-top: 4px; margin-bottom: 14px;
}

[data-testid="stFileUploader"] {
    background: white;
    border-radius: 14px;
    padding: 1rem;
    border: 2px dashed #AFA9EC;
}

.stButton button {
    background: #534AB7 !important;
    color: #EEEDFE !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    padding: 0.5rem 1.2rem !important;
}
.stButton button:hover {
    background: #3C3489 !important;
}

div[data-testid="stChatInput"] {
    border: 2px solid #CECBF6 !important;
    border-radius: 12px !important;
}

.stInfo {
    background: #EEEDFE !important;
    border: 1px solid #CECBF6 !important;
    border-radius: 12px !important;
    color: #3C3489 !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================
# HEADER
# ============================================
st.markdown("""
<div class="app-header">
    <div class="app-header-icon">📄</div>
    <div>
        <h1>PDF Chat App</h1>
        <p>Upload any PDF and ask questions using AI</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# FUNCTIONS
# ============================================
def process_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    try:
        from langchain_community.document_loaders import PyPDFLoader
        loader = PyPDFLoader(tmp_path)
        pages = loader.load()
        if not pages:
            st.error("PDF has no readable text! Try a different PDF.")
            st.stop()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(pages)
        chunks = [c for c in chunks if c.page_content.strip()]
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        st.stop()
    finally:
        os.unlink(tmp_path)
    return chunks, len(pages)

def get_embedding(text):
    text = text.strip()
    if not text:
        return None
    try:
        response = client.models.embed_content(
            model="gemini-embedding-001", contents=text)
        return response.embeddings[0].values
    except Exception:
        return None

def create_vector_store(chunks):
    texts = [c.page_content for c in chunks]
    embeddings = [e for e in (get_embedding(t) for t in texts) if e is not None]
    if not embeddings:
        st.error("Could not create embeddings. Check your API key.")
        st.stop()
    import faiss
    arr = np.array(embeddings, dtype=np.float32)
    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(arr)
    return index, texts

def search_chunks(question, index, texts, k=3):
    q_emb = get_embedding(question)
    if q_emb is None:
        return []
    _, idxs = index.search(np.array([q_emb], dtype=np.float32), k)
    return [texts[i] for i in idxs[0] if i < len(texts)]

def get_answer(question, chunks):
    time.sleep(3)
    context = "\n\n".join(chunks)
    prompt = f"""You are a helpful assistant answering questions from a PDF.
Use only the context below. If the answer isn't there, say so clearly.

Context:
{context}

Question: {question}
Answer:"""
    for attempt in range(3):
        try:
            r = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            return r.text
        except Exception as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                if attempt < 2:
                    time.sleep(10)
                else:
                    return "Server is busy. Please wait and try again."
            else:
                raise e

# ============================================
# SESSION STATE
# ============================================
for key, val in [("chat_history", []), ("vector_store", None),
                 ("texts", None), ("pdf_processed", False), ("pdf_stats", {})]:
    if key not in st.session_state:
        st.session_state[key] = val

# ============================================
# PDF UPLOAD
# ============================================
if not st.session_state.pdf_processed:
    uploaded_file = st.file_uploader(
        "📂 Upload your PDF here", type="pdf",
        help="Upload any text-based PDF"
    )
    if uploaded_file:
        with st.status("Processing your PDF...", expanded=True) as status:
            st.write("📖 Reading your PDF...")
            chunks, total_pages = process_pdf(uploaded_file)
            st.write(f"✅ Found {total_pages} pages → {len(chunks)} chunks")
            st.write("🧠 Understanding content...")
            index, texts = create_vector_store(chunks)
            st.session_state.vector_store = index
            st.session_state.texts = texts
            st.session_state.pdf_stats = {
                "pages": total_pages,
                "chunks": len(chunks),
                "name": uploaded_file.name
            }
            st.session_state.pdf_processed = True
            status.update(label="Ready to chat!", state="complete")

# ============================================
# CHAT INTERFACE
# ============================================
if st.session_state.pdf_processed:
    stats = st.session_state.pdf_stats
    pages   = stats.get("pages", 0)
    chunks  = stats.get("chunks", 0)
    asked   = len(st.session_state.chat_history)

    st.markdown(f'<div class="pdf-badge">📄 {stats.get("name","document.pdf")}</div>',
                unsafe_allow_html=True)

    st.markdown(f"""
    <div class="stats-row">
      <div class="stat-card stat-pages">
        <div class="stat-num-pages">{pages}</div>
        <div class="stat-lbl-pages">Pages read</div>
      </div>
      <div class="stat-card stat-chunks">
        <div class="stat-num-chunks">{chunks}</div>
        <div class="stat-lbl-chunks">Chunks created</div>
      </div>
      <div class="stat-card stat-questions">
        <div class="stat-num-questions">{asked}</div>
        <div class="stat-lbl-questions">Questions asked</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔄 Upload a different PDF"):
        for key in ["pdf_processed","vector_store","texts","chat_history","pdf_stats"]:
            st.session_state[key] = [] if key == "chat_history" else (
                {} if key == "pdf_stats" else None if key != "pdf_processed" else False)
        st.rerun()

    st.divider()

    st.markdown('<div class="chat-container"><div class="chat-label">CONVERSATION</div>',
                unsafe_allow_html=True)

    for chat in st.session_state.chat_history:
        st.markdown(f'<div class="user-msg">{chat["question"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="ai-msg">{chat["answer"]}</div>', unsafe_allow_html=True)
        st.markdown('<div class="source-chip">📄 From your PDF</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    question = st.chat_input("Ask anything about your PDF...")
    if question:
        st.markdown(f'<div class="user-msg">{question}</div>', unsafe_allow_html=True)
        with st.spinner("Thinking..."):
            relevant = search_chunks(question, st.session_state.vector_store,
                                     st.session_state.texts)
            answer = get_answer(question, relevant)
        st.markdown(f'<div class="ai-msg">{answer}</div>', unsafe_allow_html=True)
        st.markdown('<div class="source-chip">📄 From your PDF</div>', unsafe_allow_html=True)
        st.session_state.chat_history.append({"question": question, "answer": answer})
        st.rerun()

# ============================================
# EMPTY STATE
# ============================================
if not st.session_state.pdf_processed:
    st.info("""
    👆 Upload a PDF above to get started!

    Try asking:
    - "What is this document about?"
    - "Summarize the main points"
    - "What does it say about [any topic]?"
    """)