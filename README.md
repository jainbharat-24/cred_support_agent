
# 🚀 CRED Support Agent & Intelligent Fintech Assistant

An advanced, production-ready AI-driven support agent built with **LangGraph**, **Dual-Chunking RAG**, **FastAPI**, and **Model Context Protocol (MCP)** support. Designed specifically for financial and credit domain assistance with strict data privacy and secure auditing.

---

## ✨ Key Features

- **🧠 Dual-Chunking RAG Core:** Intelligent document retrieval using multi-level chunking over policy files, interest rates, balance inquiries, and closure documents stored in the `knowledge_base/`.
- **🤖 LangGraph Agent & Dynamic Tool Routing:** Autonomous agent capable of understanding customer intents and intelligently routing queries to specialized financial tools.
- **🔒 PII-Masked Secure Logging:** Built-in compliance logging (`agent_audit.log`) that masks sensitive user credentials and personal identifiable information (PII) during interactions.
- **⚡ FastAPI & MCP Backend:** Exposes clean RESTful endpoints via `server.py` and supports Model Context Protocol (`mcp_server.py`) for seamless integrations.
- **📊 Evaluation & Dataset Support:** Built-in evaluation scripts (`evaluate_rag.py` and `dataset.py`) to measure RAG retrieval performance and response accuracy.

---

## 📂 Project Structure

```text
cred_support_agent/
│
├── knowledge_base/        # Policy & financial document store (.txt files)
├── .gitignore             # Git ignored files & cache directories
├── agent.py               # Core LangGraph agent orchestration logic
├── agent_audit.log        # PII-masked secure execution & audit logs
├── create_kb.py           # Knowledge base initializer & indexer
├── dataset.py             # Evaluation datasets & test cases
├── evaluate_rag.py        # RAG performance evaluation script
├── mcp_server.py          # Model Context Protocol (MCP) server implementation
├── rag_core.py            # Embedding, retrieval, and dual-chunking logic
└── server.py              # FastAPI application server entry point
🛠️ Tech Stack
Python (3.10+)

LangChain & LangGraph (Agent workflows & RAG pipelines)

FastAPI & Uvicorn (Backend API server)

Vector Search / Embeddings (Core retrieval engine)

🚀 Getting Started Locally
1. Clone the Repository
Bash
git clone [https://github.com/jainbharat-24/cred_support_agent.git](https://github.com/jainbharat-24/cred_support_agent.git)
cd cred_support_agent
2. Install Dependencies
Make sure you have your virtual environment activated, then install required packages:

Bash
pip install fastapi uvicorn langchain langgraph pydantic
3. Initialize the Knowledge Base
Run the setup script to prepare your vector store and knowledge chunks:

Bash
python create_kb.py
4. Run the FastAPI Server
Start the backend server locally:

Bash
uvicorn server:app --reload
The API server will run at http://127.0.0.1:8000. You can visit http://127.0.0.1:8000/docs to test endpoints interactively via Swagger UI.

📄 License
This project is built as an advanced AI Capstone implementation.