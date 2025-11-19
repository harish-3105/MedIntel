"""
MedIntel Backend - Main Application Entry Point
"""

import logging

import uvicorn
from config import ALLOWED_ORIGINS, API_DEBUG, API_HOST, API_PORT, LOG_FORMAT, LOG_LEVEL
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Configure logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

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


# Root endpoint
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
            "report_analysis": "/api/v1/analyze/report",
            "symptom_checker": "/api/v1/analyze/symptoms",
        },
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "MedIntel Backend", "version": "1.0.0"}


# Import and include routers
try:
    from api.report_analyzer import router as report_router

    app.include_router(report_router, prefix="/api/v1", tags=["Report Analysis"])
    logger.info("✅ Report Analyzer router loaded")
except ImportError as e:
    logger.warning(f"⚠️ Report Analyzer router not loaded: {e}")

try:
    from api.symptom_checker import router as symptom_router

    app.include_router(symptom_router, prefix="/api/v1", tags=["Symptom Checker"])
    logger.info("✅ Symptom Checker router loaded")
except ImportError as e:
    logger.warning(f"⚠️ Symptom Checker router not loaded: {e}")

try:
    from api.ocr_service import router as ocr_router

    app.include_router(ocr_router, prefix="/api/v1", tags=["OCR Service"])
    logger.info("✅ OCR Service router loaded")
except ImportError as e:
    logger.warning(f"⚠️ OCR Service router not loaded: {e}")

try:
    from api.chat_service import router as chat_router

    app.include_router(chat_router, tags=["Chat Service"])
    logger.info("✅ Chat Service router loaded")
except ImportError as e:
    logger.warning(f"⚠️ Chat Service router not loaded: {e}")

try:
    from api.medical_imaging import router as imaging_router

    app.include_router(imaging_router, prefix="/api/v1", tags=["Medical Imaging"])
    logger.info("✅ Medical Imaging router loaded")
except ImportError as e:
    logger.warning(f"⚠️ Medical Imaging router not loaded: {e}")


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc) if API_DEBUG else "An error occurred",
        },
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Starting MedIntel Backend...")
    logger.info(f"📍 API Host: {API_HOST}")
    logger.info(f"🔌 API Port: {API_PORT}")
    logger.info(f"🐛 Debug Mode: {API_DEBUG}")
    logger.info("✅ MedIntel Backend started successfully")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 Shutting down MedIntel Backend...")
    logger.info("✅ MedIntel Backend shut down successfully")


# Run the application
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🏥 MedIntel - AI-Driven Healthcare Intelligence System")
    print("=" * 60)
    print(f"📍 Server: http://{API_HOST}:{API_PORT}")
    print(f"📚 API Docs: http://{API_HOST}:{API_PORT}/docs")
    print(f"🔍 ReDoc: http://{API_HOST}:{API_PORT}/redoc")
    print("=" * 60 + "\n")

    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=False,  # Disabled to prevent file watcher issues
        log_level=LOG_LEVEL.lower(),
    )
