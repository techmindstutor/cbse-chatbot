import os
from pathlib import Path
import fitz  # pymupdf
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

DATA_DIR = "data"
CHROMA_DIR = "vectorstore/chroma_db"

def load_pdfs():
    documents = []
    
    for class_folder in ["class9", "class10", "class11", "class12"]:
        folder_path = Path(DATA_DIR) / class_folder
        
        if not folder_path.exists():
            print(f"Folder not found: {folder_path}")
            continue
            
        for pdf_file in folder_path.glob("*.pdf"):
            print(f"Reading: {pdf_file}")
            
            doc = fitz.open(pdf_file)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            
            documents.append({
                "text": text,
                "source": str(pdf_file),
                "class": class_folder
            })
    
    return documents

def ingest():
    print("Loading PDFs...")
    documents = load_pdfs()
    
    if not documents:
        print("No PDFs found. Please add PDFs to data/ folders.")
        return
    
    print(f"Found {len(documents)} PDF files")
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    
    chunks = []
    metadatas = []
    
    for doc in documents:
        split_texts = splitter.split_text(doc["text"])
        for chunk in split_texts:
            chunks.append(chunk)
            metadatas.append({
                "source": doc["source"],
                "class": doc["class"]
            })
    
    print(f"Created {len(chunks)} chunks")
    print("Creating vector database...")
    
    embeddings = SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory=CHROMA_DIR
    )
    
    print("Done! Vector database created successfully.")

if __name__ == "__main__":
    ingest()