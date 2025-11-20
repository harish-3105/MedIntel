"""
MedIntel Backend - Minimal Production Version for Railway
"""

import logging
import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

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


@app.post("/api/v1/chat")
async def chat(request: dict):
    """Basic chat endpoint"""
    try:
        message = request.get("message", "")
        logger.info(f"Received chat message: {message}")
        
        return {
            "response": f"Echo: {message}",
            "status": "success",
            "note": "This is a minimal version. Full AI features require complete deployment."
        }
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "message": "Chat processing failed"}
        )


@app.post("/api/chat")
async def chat_alt(request: dict):
    """Alternative chat endpoint"""
    return await chat(request)


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
