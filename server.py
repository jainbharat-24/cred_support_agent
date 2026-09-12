import os
import json
import logging
import uuid
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Cred Domain Support Agent API")

# Configure structured JSON-Lines logging
logging.basicConfig(filename="agent_audit.log", level=logging.INFO, format="%(message)s")
logger = logging.getLogger("cred_agent")

class QueryRequest(BaseModel):
    query: str
    trace_id: str = None

class QueryResponse(BaseModel):
    trace_id: str
    response: str
    grounded: bool

def mask_pii(text: str) -> str:
    import re
    masked = re.sub(r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b', '[PAN-REDACTED]', text)
    masked = re.sub(r'\b\d{4}\s?\d{4}\s?\d{4}\b', '[AADHAAR-REDACTED]', masked)
    return masked

@app.post("/ask", response_model=QueryResponse)
def ask_agent(req: QueryRequest):
    trace_id = req.trace_id or str(uuid.uuid4())
    masked_query = mask_pii(req.query)
    
    log_entry = {
        "trace_id": trace_id,
        "endpoint": "/ask",
        "query_masked": masked_query,
        "status": "success"
    }
    logger.info(json.dumps(log_entry))
    
    response_text = "Processed query successfully under MOCK_LLM mode."
    return QueryResponse(trace_id=trace_id, response=response_text, grounded=True)

@app.get("/health")
def health_check():
    return {"status": "healthy", "mode": "MOCK_LLM"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)