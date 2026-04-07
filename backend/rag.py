import faiss
import numpy as np
import pickle
import os
import requests
from sentence_transformers import SentenceTransformer

# ================================
# CONFIG
# ================================
VECTOR_PATH = "vector_db/index.faiss"
CHUNKS_PATH = "vector_db/chunks.pkl"
OLLAMA_URL = "http://ollama:11434/api/generate"

MODEL_NAME = "phi3:mini" #Lightweight model


# ================================
# LOAD EMBEDDING MODEL ONCE
# ================================
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    device="cpu"
)

faiss_index = None
document_chunks = None


# ================================
# CREATE INDEX (OPTIMIZED)
# ================================
def create_index(text):

    # Larger chunks = fewer vectors = faster
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]

    embeddings = embedding_model.encode(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True,
        batch_size=16   # reduce CPU spike
    )

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    os.makedirs("vector_db", exist_ok=True)
    faiss.write_index(index, VECTOR_PATH)

    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(chunks, f)


# ================================
# LOAD INDEX ONLY ONCE
# ================================
def load_index():
    global faiss_index, document_chunks

    if not os.path.exists(VECTOR_PATH):
        return False

    if faiss_index is None:
        faiss_index = faiss.read_index(VECTOR_PATH)

    if document_chunks is None:
        with open(CHUNKS_PATH, "rb") as f:
            document_chunks = pickle.load(f)

    return True


# ================================
# FAST SEARCH
# ================================
def search(query):

    if not load_index():
        return None

    query_vector = embedding_model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    scores, indices = faiss_index.search(query_vector, k=1)

    return [document_chunks[indices[0][0]]]


# ================================
# FAST OLLAMA CALL
# ================================
def ask_llm(prompt):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_ctx": 1024, 
                "temperature": 0.2,
                "num_predict": 200   # limit output length
            }
        },
        timeout=180
    )

    if response.status_code != 200:
        return "LLM error: " + response.text

    return response.json().get("response", "")


# ================================
# MAIN RAG
# ================================
def ask_question(query):

    context_chunks = search(query)

    if context_chunks is None:
        return "Please upload HR policy document first."

    context = context_chunks[0]

    final_prompt = f"""
You are an HR assistant.
Answer briefly and clearly using the HR policy below.

HR POLICY:
{context}

QUESTION:
{query}
"""

    return ask_llm(final_prompt)