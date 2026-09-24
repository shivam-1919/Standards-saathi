"""
FastAPI Server for Standards Saathi (मानक साथी)
Serves the Accessible Multilingual Web UI and exposes RAG, Google Gemini AI, and BIS Proactive Endpoints.
Only Admin Portal can view/update API keys and internal configurations.
"""

import os
import sys
import re
import json
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from rag_engine import get_rag_engine
from sample_data import get_all_standards

load_dotenv(override=True)

app = FastAPI(
    title="Standards Saathi API",
    description="Backend for Indian Standards & BIS Services AI Assistant with Google Gemini & Accessible Voice Integration",
    version="3.5.0"
)

# Request Models
class ChatRequest(BaseModel):
    query: str
    top_k: int = 3
    temperature: float = 0.2
    chat_history: Optional[List[Dict[str, str]]] = None
    language: Optional[str] = "English"
    msme_mode: Optional[bool] = False
    voice_mode: Optional[bool] = False
    saral_mode: Optional[bool] = False
    model_override: Optional[str] = None

class AdminConfigRequest(BaseModel):
    admin_password: str
    gemini_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None
    new_admin_password: Optional[str] = None

class ChecklistRequest(BaseModel):
    product: str
    language: Optional[str] = "English"
    is_msme: Optional[bool] = True

class TenderAnalyzerRequest(BaseModel):
    tender_text: str
    language: Optional[str] = "English"

class ExplainClauseRequest(BaseModel):
    clause_text: str
    language: Optional[str] = "English"

class OnboardingInterviewRequest(BaseModel):
    answers: Dict[str, str]
    language: Optional[str] = "English"

class StandardIngestRequest(BaseModel):
    admin_password: str
    standard_number: str
    title: str
    category: str = "General"
    status: str = "User Ingested Standard"
    summary: str = ""
    clauses: List[Dict[str, Any]] = []

class AuthRequest(BaseModel):
    password: str

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def get_index():
    """Serves the main Standards Saathi HTML frontend."""
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"message": "Standards Saathi API Running. Place static/index.html to view UI."})

# ---------------------------------------------------------------------------
# HEALTH CHECK & MONITORING ENDPOINTS (FOR UPTIMEROBOT & RENDER)
# ---------------------------------------------------------------------------

@app.get("/health", status_code=200)
@app.get("/healthz", status_code=200)
@app.get("/api/health", status_code=200)
@app.head("/health", status_code=200)
@app.head("/healthz", status_code=200)
async def health_check():
    """Lightweight health check endpoint for UptimeRobot, Render, and external uptime monitors."""
    import datetime
    return {
        "status": "healthy",
        "service": "Standards Saathi AI",
        "version": "2.0.0",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "uptime": "active"
    }

# ---------------------------------------------------------------------------
# CORE CHAT & RAG ENDPOINTS
# ---------------------------------------------------------------------------

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    """Executes RAG search and multilingual LLM synthesis via Gemini / Groq."""
    engine = get_rag_engine()
    response = engine.generate_response(
        query=req.query,
        chat_history=req.chat_history,
        top_k=req.top_k,
        temperature=req.temperature,
        language=req.language or "English",
        model_override=req.model_override,
        msme_mode=req.msme_mode or False,
        voice_mode=req.voice_mode or False,
        saral_mode=req.saral_mode or False
    )
    return response

@app.get("/api/standards")
async def get_standards_endpoint():
    """Returns all Indian Standards loaded in the system."""
    return get_all_standards()

@app.post("/api/standards")
async def ingest_standard_endpoint(req: StandardIngestRequest):
    """Admin endpoint to dynamically ingest a new standard into the FAISS vector index."""
    current_admin_pwd = os.getenv("ADMIN_PASSWORD", "admin123")
    if req.admin_password != current_admin_pwd:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid admin password")

    engine = get_rag_engine()
    std_dict = {
        "id": req.standard_number.replace(" ", "-"),
        "standard_number": req.standard_number,
        "title": req.title,
        "category": req.category,
        "status": req.status,
        "summary": req.summary,
        "clauses": req.clauses
    }
    total_chunks = engine.add_custom_standard(std_dict)
    return {
        "status": "success",
        "message": f"Standard {req.standard_number} ingested successfully.",
        "total_chunks_indexed": total_chunks
    }

# ---------------------------------------------------------------------------
# 5 PROACTIVE TOOLS API ENDPOINTS
# ---------------------------------------------------------------------------

@app.post("/api/tools/checklist")
async def compliance_checklist_endpoint(req: ChecklistRequest):
    """Feature 1: Generates a complete Compliance Checklist for any product/IS code."""
    engine = get_rag_engine()
    return engine.generate_compliance_checklist(
        product=req.product,
        language=req.language or "English",
        is_msme=req.is_msme if req.is_msme is not None else True
    )

@app.post("/api/tools/tender-analyzer")
async def tender_analyzer_endpoint(req: TenderAnalyzerRequest):
    """Feature 2: Analyzes tender/procurement specifications for IS code compliance."""
    engine = get_rag_engine()
    return engine.analyze_tender_or_spec(
        tender_text=req.tender_text,
        language=req.language or "English"
    )

@app.post("/api/tools/explain-clause")
async def explain_clause_endpoint(req: ExplainClauseRequest):
    """Feature 3: Explains a technical standard clause in plain language with examples."""
    engine = get_rag_engine()
    return engine.explain_clause(
        clause_text=req.clause_text,
        language=req.language or "English"
    )

@app.post("/api/tools/onboarding-interview")
async def onboarding_interview_endpoint(req: OnboardingInterviewRequest):
    """Feature 5: Evaluates onboarding questions to produce a custom roadmap."""
    engine = get_rag_engine()
    return engine.evaluate_onboarding_interview(
        answers=req.answers,
        language=req.language or "English"
    )

# ---------------------------------------------------------------------------
# ADMIN & CONFIGURATION ENDPOINTS (PROTECTED)
# ---------------------------------------------------------------------------

@app.post("/api/admin/auth")
async def admin_auth_endpoint(req: AuthRequest):
    """Verifies admin credentials."""
    admin_pwd = os.getenv("ADMIN_PASSWORD", "admin123")
    if req.password == admin_pwd:
        return {
            "status": "success",
            "message": "Authenticated",
            "config": {
                "has_gemini": bool(os.getenv("GEMINI_API_KEY")),
                "has_groq": bool(os.getenv("GROQ_API_KEY")),
                "active_model": "Google Gemini (gemini-2.5-flash)" if os.getenv("GEMINI_API_KEY") else ("Groq Llama-3.1" if os.getenv("GROQ_API_KEY") else "Local RAG Engine")
            }
        }
    raise HTTPException(status_code=401, detail="Invalid admin password")

@app.post("/api/admin/config")
async def update_admin_config_endpoint(req: AdminConfigRequest):
    """Allows authenticated admin to configure Gemini and Groq API keys securely."""
    current_admin_pwd = os.getenv("ADMIN_PASSWORD", "admin123")
    if req.admin_password != current_admin_pwd:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid admin password")

    engine = get_rag_engine()
    
    if req.gemini_api_key is not None:
        os.environ["GEMINI_API_KEY"] = req.gemini_api_key
        engine.set_gemini_api_key(req.gemini_api_key)

    if req.groq_api_key is not None:
        os.environ["GROQ_API_KEY"] = req.groq_api_key
        engine.set_groq_api_key(req.groq_api_key)

    if req.new_admin_password:
        os.environ["ADMIN_PASSWORD"] = req.new_admin_password

    return {
        "status": "success",
        "message": "System configuration updated successfully.",
        "has_gemini": bool(os.getenv("GEMINI_API_KEY")),
        "has_groq": bool(os.getenv("GROQ_API_KEY"))
    }

@app.post("/api/admin/security-logs")
async def get_admin_security_logs_endpoint(req: AuthRequest):
    """Retrieves blocked prompt injection attempts and audit logs for authenticated admin."""
    current_admin_pwd = os.getenv("ADMIN_PASSWORD", "admin123")
    if req.password != current_admin_pwd:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid admin password")

    engine = get_rag_engine()
    logs = engine.get_security_logs()
    return {
        "status": "success",
        "total_blocked": len(logs),
        "logs": logs
    }

@app.post("/api/admin/clear-security-logs")
async def clear_admin_security_logs_endpoint(req: AuthRequest):
    """Clears security audit logs for authenticated admin."""
    current_admin_pwd = os.getenv("ADMIN_PASSWORD", "admin123")
    if req.password != current_admin_pwd:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid admin password")

    engine = get_rag_engine()
    engine.clear_security_logs()
    return {
        "status": "success",
        "message": "Security logs cleared successfully."
    }

@app.on_event("startup")
async def startup_event():
    print("\n" + "=" * 64)
    print("  STANDARDS SAATHI AI SERVER STARTED")
    print("=" * 64)
    print("  - Vector Index: FAISS + SentenceTransformers Ready")
    print("  - Language Models: Google Gemini + Groq Llama (5 Languages)")
    print("  - Voice Engine: 5-Language Voice Assistant (EN, HI, TA, BN, MR)")
    print("  - Web Application: http://localhost:8000")
    print("  - Admin Portal: Accessible via UI Top Bar with password")
    print("=" * 64 + "\n")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
