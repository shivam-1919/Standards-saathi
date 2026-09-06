"""
FastAPI Server for Standards Saathi (मानक साथी)
Serves the Google Stitch UI Frontend and exposes high-performance RAG endpoints.
"""

import os
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from rag_engine import get_rag_engine
from sample_data import get_all_standards

load_dotenv()

app = FastAPI(
    title="Standards Saathi API",
    description="Backend for Indian Standards & BIS Services RAG Chatbot",
    version="2.4.0"
)

# Models
class ChatRequest(BaseModel):
    query: str
    top_k: int = 3
    temperature: float = 0.2
    chat_history: Optional[List[Dict[str, str]]] = None
    language: Optional[str] = "English"

class ConfigRequest(BaseModel):
    groq_api_key: str

class StandardIngestRequest(BaseModel):
    id: Optional[str] = None
    standard_number: str
    title: str
    category: str = "General"
    status: str = "User Ingested Standard"
    summary: str = ""
    clauses: List[Dict[str, Any]] = []

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def get_index():
    """Serves the main Google Stitch HTML frontend."""
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"message": "Standards Saathi API Running. Place static/index.html to view UI."})

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    """Executes RAG search and Groq LLM synthesis."""
    engine = get_rag_engine()
    response = engine.generate_response(
        query=req.query,
        chat_history=req.chat_history,
        top_k=req.top_k,
        temperature=req.temperature,
        language=req.language or "English"
    )
    return response

@app.get("/api/standards")
async def get_standards_endpoint():
    """Returns all Indian Standards loaded in the system."""
    return get_all_standards()

@app.post("/api/standards")
async def ingest_standard_endpoint(req: StandardIngestRequest):
    """Dynamically ingests a new standard into the FAISS vector index."""
    engine = get_rag_engine()
    total_chunks = engine.add_custom_standard(req.dict())
    return {
        "status": "success",
        "message": f"Standard {req.standard_number} ingested successfully.",
        "total_chunks_indexed": total_chunks
    }

class AuthRequest(BaseModel):
    password: str

@app.post("/api/admin/auth")
async def admin_auth_endpoint(req: AuthRequest):
    admin_pwd = os.getenv("ADMIN_PASSWORD", "admin123")
    if req.password == admin_pwd:
        return {"status": "success", "message": "Authenticated"}
    raise HTTPException(status_code=401, detail="Invalid admin password")

@app.post("/api/config")
async def update_config_endpoint(req: ConfigRequest):
    """Updates Groq API key dynamically."""
    engine = get_rag_engine()
    engine.set_groq_api_key(req.groq_api_key)
    return {"status": "success", "message": "API key updated."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
