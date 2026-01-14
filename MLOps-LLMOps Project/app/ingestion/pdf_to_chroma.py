"""
Document ingestion pipeline for the RAG system.
Parses PDF files, splits text into overlapping chunks,
generates embeddings, and stores them in a persistent ChromaDB collection.
"""

import os

# To suppress info/warning message from TensorFlow (sentence-transformers)
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

from pathlib import Path

import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from PyPDF2 import PdfReader

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PDF_FOLDER = PROJECT_ROOT / "pdfs"
PERSIST_DIR = PROJECT_ROOT / "chroma_db_data"

# Initialize ChromaDB client with persistence
client = chromadb.PersistentClient(path=str(PERSIST_DIR))
# Note: Collection name and distance metric must match the API service
collection = client.get_or_create_collection(
    name="papers",
    metadata={"hnsw:space": "cosine"},  # Cosine similarity for vector search
)

# Embedding model (PyTorch)
embeddings_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
)

# Split text into overlapping chunks to preserve semantic continuity
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)


# Extract and concatenate text from all pages of a PDF file
def parse_pdf(file_path: Path) -> str:
    reader = PdfReader(str(file_path))
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


# Ingestion | Read PDFs, split into chunks, embed, and store in ChromaDB
# Re-running will overwrite or duplicate entries unless the collection is cleared
def ingest_pdfs():
    PDF_FOLDER.mkdir(exist_ok=True)
    PERSIST_DIR.mkdir(exist_ok=True)

    files = list(PDF_FOLDER.glob("*.pdf"))
    if not files:
        print(f"No PDFs found in {PDF_FOLDER}. Place some PDFs to ingest.")
        return

    for pdf_file in files:
        print(f"Processing {pdf_file.name}...")
        text = parse_pdf(pdf_file)
        chunks = text_splitter.split_text(text)

        for i, chunk in enumerate(chunks):
            vector = embeddings_model.embed_documents([chunk])[0]
            collection.add(
                ids=[f"{pdf_file.stem}_{i}"],
                documents=[chunk],
                metadatas=[{"source": pdf_file.name}],
                embeddings=[vector],
            )

    print("ChromaDB ingestion completed. Data saved at:", PERSIST_DIR)


# Run ingestion
if __name__ == "__main__":
    ingest_pdfs()
