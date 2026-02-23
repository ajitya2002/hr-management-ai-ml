
from fastapi import FastAPI, UploadFile, File
from pypdf import PdfReader
import rag
import os
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://frontend:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # For dev (restrict in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
def upload(file: UploadFile = File(...)):
    os.makedirs("temp", exist_ok=True)
    file_path = f"temp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    rag.create_index(text)
    return {"status": "Document indexed successfully"}

@app.post("/ask")
def ask(query: str):
    try:
        answer = rag.ask_question(query)
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}
