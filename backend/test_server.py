"""
Minimal test server to verify API structure
Run this to test if the server starts without ML models
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app
app = FastAPI(
    title="MedIntel API - Test Mode",
    description="Testing API structure without ML models",
    version="1.0.0-test",
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "🏥 MedIntel API Test Server",
        "status": "running",
        "mode": "test (without ML models)",
        "note": "To run full server, install dependencies and run main.py",
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "MedIntel Test Server"}


@app.get("/test/sample")
async def sample_test():
    return {
        "success": True,
        "message": "API structure is working!",
        "features": {
            "report_analysis": "Available (requires ML models)",
            "symptom_checker": "Available (requires ML models)",
            "api_docs": "http://localhost:8000/docs",
        },
    }


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("MedIntel Test Server")
    print("=" * 60)
    print("This is a minimal test server to verify API structure")
    print("For full functionality, run: python main.py")
    print("=" * 60 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
