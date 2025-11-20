"""
MedIntel Backend - Minimal Production Version for Railway
"""

import logging
import os
from typing import Optional

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get config from environment
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("PORT", os.getenv("API_PORT", 8000)))

# CORS origins
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://astonishing-empathy-production.up.railway.app",
    "https://medintel-frontend.onrender.com",
    "*",
]

# Create FastAPI app
app = FastAPI(
    title="MedIntel API",
    description="AI-Driven Healthcare Intelligence System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "🏥 MedIntel API is running",
        "version": "1.0.0",
        "status": "healthy",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "api": "/api/v1",
        },
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "MedIntel Backend", "version": "1.0.0"}


@app.get("/api/v1/status")
async def api_status():
    """API status endpoint"""
    return {
        "status": "operational",
        "message": "MedIntel API is running in lightweight mode",
        "features": {
            "basic_api": "available",
            "health_checks": "available",
            "full_ml_features": "requires full deployment",
        },
    }


# Request models
class ChatRequest(BaseModel):
    question: Optional[str] = None
    message: Optional[str] = None
    context: Optional[str] = None
    conversation_history: Optional[list] = None
    model_provider: Optional[str] = "openai"
    student_mode: Optional[bool] = False
    mode: Optional[str] = "student"
    session_id: Optional[str] = None
    user_profile: Optional[dict] = None


@app.post("/api/v1/chat")
async def chat_v1(chat_request: ChatRequest):
    """Chat endpoint v1"""
    try:
        # Get message from either question or message field
        msg = chat_request.question or chat_request.message or ""
        logger.info(f"Received chat - question: {msg}, mode: {chat_request.mode}")
        
        response_text = f"Hello! I'm MedIntel AI assistant. You said: '{msg}'. "
        
        if chat_request.student_mode:
            response_text += "I'm running in student mode to help with your medical learning. "
        
        response_text += "Note: This is a minimal deployment. Full AI features with medical analysis require complete setup with ML models."
        
        return {
            "response": response_text,
            "summary": "Demo Response",
            "content": response_text,
            "status": "success",
            "emotion": "neutral",
            "riskLevel": "Green",
            "confidence": "Demo",
            "nextSteps": ["This is a demo response", "Full features coming soon"],
            "sources": ["MedIntel Demo System"],
            "sessionId": chat_request.session_id or "demo-session"
        }
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "message": "Chat processing failed"}
        )


@app.post("/v1/chat")
async def chat_v1_no_prefix(chat_request: ChatRequest):
    """Chat endpoint v1 without /api prefix (for proxy)"""
    return await chat_v1(chat_request)


@app.post("/api/chat")
async def chat_simple(request: Request):
    """Alternative chat endpoint - accepts any JSON"""
    try:
        body = await request.json()
        message = body.get("message", body.get("text", ""))
        logger.info(f"Received chat message: {message}")
        
        return {
            "response": f"MedIntel AI: I received your message - '{message}'. This is a minimal deployment.",
            "status": "success",
            "data": body
        }
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "message": "Chat processing failed"}
        )


# Middleware to log all requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"📨 {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"📤 Response status: {response.status_code}")
    return response


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
        },
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Starting MedIntel Backend (Lightweight Mode)...")
    logger.info(f"📍 API Host: {API_HOST}")
    logger.info(f"🔌 API Port: {API_PORT}")
    logger.info("✅ MedIntel Backend started successfully")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 Shutting down MedIntel Backend...")


# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=False,
        log_level="info",
    )
