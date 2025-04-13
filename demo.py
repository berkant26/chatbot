import streamlit as st
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import tempfile
import re

st.set_page_config(page_title="📄 PDF Chatbot", layout="centered")

# 🔹 Model Loader
class PDFChatbotModel:
    @staticmethod
    @st.cache_resource
    def load_model():
        return SentenceTransformer("all-MiniLM-L6-v2")

# 🔹 PDF Text Extractor
class PDFTextExtractor:
    @staticmethod
    def extract_text_from_pdf(file_path):
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

# 🔹 Text Chunker
class TextChunker:
    @staticmethod
    def chunk_text(text, max_tokens=300):
        sentences = text.split(". ")
        chunks, current_chunk = [], ""
        for sentence in sentences:
            if len(current_chunk.split()) + len(sentence.split()) < max_tokens:
                current_chunk += sentence + ". "
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        if current_chunk:
            chunks.append(current_chunk.strip())
        return chunks

# 🔹 Relevance Finder
class RelevanceFinder:
    @staticmethod
    def get_most_relevant_sentence(user_question, chunks, chunk_embeddings, model, threshold=0.4):
        question_embedding = model.encode([user_question])
        similarities = cosine_similarity(question_embedding, chunk_embeddings)
        best_chunk_idx = np.argmax(similarities)
        best_chunk = chunks[best_chunk_idx]

        sentences = re.split(r'(?<=[.?!])\s+', best_chunk.strip())
        sentence_embeddings = model.encode(sentences)
        sentence_similarities = cosine_similarity(question_embedding, sentence_embeddings)
        best_score = np.max(sentence_similarities)
        best_sentence_idx = np.argmax(sentence_similarities)

        if best_score < threshold:
            return "❌ Sorry, I couldn't find a relevant answer in the manual."
        return sentences[best_sentence_idx]

# 🔹 Streamlit Chat Interface
class PDFChatbotApp:
    def __init__(self):
        self.model = PDFChatbotModel.load_model()
        self.messages = []
        self.chunks = []
        self.embeddings = []

    def setup_session_state(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "chunks" not in st.session_state:
            st.session_state.chunks = []
        if "embeddings" not in st.session_state:
            st.session_state.embeddings = []

    def upload_pdf(self):
        uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
        if uploaded_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())
                file_path = tmp_file.name

            pdf_text = PDFTextExtractor.extract_text_from_pdf(file_path)
            self.chunks = TextChunker.chunk_text(pdf_text)
            self.embeddings = self.model.encode(self.chunks)

            st.session_state.chunks = self.chunks
            st.session_state.embeddings = self.embeddings
            st.success(f"✅ PDF processed. Ready to chat!")

    def chat_input(self):
        user_input = st.chat_input("Ask something about the PDF. ( this is demo version, it can be further developed!)")
        return user_input

    def generate_answer(self, user_input):
        answer = RelevanceFinder.get_most_relevant_sentence(
            user_input,
            st.session_state.chunks,
            st.session_state.embeddings,
            self.model,
        )
        return answer

    def show_chat_messages(self):
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                with st.chat_message("user"):
                    st.write(msg["content"])
            else:
                with st.chat_message("assistant"):
                    st.write(msg["content"])

    def run(self):
        self.setup_session_state()

        st.title("🧠 Chat with your PDF")
        self.upload_pdf()

        st.divider()

        user_input = self.chat_input()

        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Generate bot reply
            answer = self.generate_answer(user_input)
            st.session_state.messages.append({"role": "bot", "content": answer})

        self.show_chat_messages()


# 🔹 Running the App
if __name__ == "__main__":
    app = PDFChatbotApp()
    app.run()
