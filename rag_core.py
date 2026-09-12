import os
import chromadb
from sentence_transformers import SentenceTransformer

def load_kb_documents():
    kb_dir = "knowledge_base"
    documents = []
    for filename in sorted(os.listdir(kb_dir)):
        if filename.endswith(".txt"):
            path = os.path.join(kb_dir, filename)
            with open(path, "r", encoding="utf-8") as f:
                documents.append({"id": filename, "text": f.read()})
    return documents

def chunk_fixed_size(text, chunk_size=150, overlap=30):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def chunk_sentence_based(text):
    # Split text into sentences using simple period-based splitting
    sentences = [s.strip() for s in text.split(".") if s.strip()]
    return sentences

def setup_rag_pipeline():
    docs = load_kb_documents()
    print(f"Loaded {len(docs)} documents from knowledge base.")
    
    # Initialize ChromaDB client and collections
    client = chromadb.Client()
    fixed_coll = client.get_or_create_collection("kb_fixed_size")
    sentence_coll = client.get_or_create_collection("kb_sentence_based")
    
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    fixed_count = 0
    sentence_count = 0
    
    for doc in docs:
        # 1. Fixed-size chunks
        f_chunks = chunk_fixed_size(doc["text"])
        for idx, chunk in enumerate(f_chunks):
            cid = f"{doc['id']}_f_{idx}"
            emb = model.encode(chunk).tolist()
            fixed_coll.add(ids=[cid], embeddings=[emb], documents=[chunk], metadatas=[{"source": doc["id"]}])
            fixed_count += 1
            
        # 2. Sentence-based chunks
        s_chunks = chunk_sentence_based(doc["text"])
        for idx, chunk in enumerate(s_chunks):
            cid = f"{doc['id']}_s_{idx}"
            emb = model.encode(chunk).tolist()
            sentence_coll.add(ids=[cid], embeddings=[emb], documents=[chunk], metadatas=[{"source": doc["id"]}])
            sentence_count += 1
            
    print(f"Indexed {fixed_count} chunks into 'kb_fixed_size'.")
    print(f"Indexed {sentence_count} chunks into 'kb_sentence_based'.")

if __name__ == "__main__":
    setup_rag_pipeline()