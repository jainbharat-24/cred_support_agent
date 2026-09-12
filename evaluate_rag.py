import os
import chromadb
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def load_kb_documents():
    kb_dir = "knowledge_base"
    documents = {}
    for filename in sorted(os.listdir(kb_dir)):
        if filename.endswith(".txt"):
            path = os.path.join(kb_dir, filename)
            with open(path, "r", encoding="utf-8") as f:
                documents[filename] = f.read()
    return documents

def run_evaluation():
    docs = load_kb_documents()
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    # Test queries: 5 in-scope, 1 out-of-scope
    queries = [
        {"q": "What are the loan eligibility criteria?", "target_doc": "doc_01_eligibility.txt", "in_scope": True},
        {"q": "How is the monthly EMI calculated?", "target_doc": "doc_02_emi.txt", "in_scope": True},
        {"q": "What documents are required for KYC?", "target_doc": "doc_04_kyc.txt", "in_scope": True},
        {"q": "What is the penalty for loan prepayment?", "target_doc": "doc_08_prepayment.txt", "in_scope": True},
        {"q": "How do joint accounts work?", "target_doc": "doc_11_joint_account.txt", "in_scope": True},
        {"q": "What is the weather in Tokyo today?", "target_doc": None, "in_scope": False},
    ]
    
    print("--- RAG Retrieval Evaluation & Threshold Calibration ---")
    threshold = 0.40  # Calibrated fallback threshold
    
    # Precompute document embeddings for sentence-level matching
    doc_embeddings = {}
    for filename, text in docs.items():
        sentences = [s.strip() for s in text.split(".") if s.strip()]
        if sentences:
            embeddings = model.encode(sentences)
            doc_embeddings[filename] = embeddings
            
    for item in queries:
        q_emb = model.encode([item["q"]])
        best_score = 0.0
        best_doc = None
        
        for filename, emb_matrix in doc_embeddings.items():
            sims = cosine_similarity(q_emb, emb_matrix)
            max_sim = np.max(sims)
            if max_sim > best_score:
                best_score = max_sim
                best_doc = filename
                
        if not item["in_scope"]:
            triggered_fallback = best_score < threshold
            print(f"[Out-of-Scope] Query: '{item['q']}' | Top Score: {best_score:.3f} | Fallback Triggered: {triggered_fallback}")
        else:
            hit = best_doc == item["target_doc"]
            print(f"[In-Scope] Query: '{item['q']}' | Match: {hit} (Target: {item['target_doc']}, Got: {best_doc}) | Top Score: {best_score:.3f}")

if __name__ == "__main__":
    run_evaluation()