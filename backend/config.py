"""
Configuration settings for MedIntel backend
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# API Settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
API_DEBUG = os.getenv("API_DEBUG", "True").lower() == "true"

# Models Directory
MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(exist_ok=True)

# Pre-trained Model Paths
BIOBERT_MODEL = "dmis-lab/biobert-v1.1"
CLINICALBERT_MODEL = "emilyalsentzer/Bio_ClinicalBERT"
MEDICAL_NER_MODEL = "samrawal/bert-base-uncased_clinical-ner"

# Knowledge Base Settings
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"
KNOWLEDGE_BASE_DIR.mkdir(exist_ok=True)

# ICD-10 Database
ICD10_API_URL = "https://clinicaltables.nlm.nih.gov/api/icd10cm/v3/search"

# RxNorm API
RXNORM_API_URL = "https://rxnav.nlm.nih.gov/REST"

# OpenFDA API
OPENFDA_API_URL = "https://api.fda.gov"
OPENFDA_API_KEY = os.getenv("OPENFDA_API_KEY", "")

# Database Settings (PostgreSQL)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/medintel")

# MongoDB Settings (for document storage)
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "medintel")

# Security Settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# CORS Settings
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:5173",  # Vite dev server (alternative)
    "http://localhost:8000",
    "https://astonishing-empathy-production.up.railway.app",  # Railway Frontend
    "https://medintel-frontend.onrender.com",  # Render Frontend
    "*",  # Allow all origins for deployment
]

# File Upload Settings
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {".pdf", ".txt", ".jpg", ".jpeg", ".png"}
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# OCR Settings
OCR_ENABLED = os.getenv("OCR_ENABLED", "True").lower() == "true"
TESSERACT_PATH = os.getenv("TESSERACT_PATH", None)

# Logging Settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Model Settings
MODEL_CACHE_DIR = MODELS_DIR / "cache"
MODEL_CACHE_DIR.mkdir(exist_ok=True)

# Confidence Thresholds
DISEASE_PREDICTION_THRESHOLD = 0.5
ENTITY_EXTRACTION_THRESHOLD = 0.6
URGENCY_THRESHOLD = 0.7

# Risk Levels
RISK_LEVELS = {
    "LOW": {"min": 0.0, "max": 0.3},
    "MEDIUM": {"min": 0.3, "max": 0.6},
    "HIGH": {"min": 0.6, "max": 0.8},
    "CRITICAL": {"min": 0.8, "max": 1.0},
}

# Red Flag Symptoms (require immediate attention)
RED_FLAG_SYMPTOMS = [
    "chest pain",
    "difficulty breathing",
    "severe headache",
    "loss of consciousness",
    "severe bleeding",
    "stroke symptoms",
    "severe abdominal pain",
    "suicidal thoughts",
]

print(f"✅ Configuration loaded")
print(f"📁 Base directory: {BASE_DIR}")
print(f"🤖 Models directory: {MODELS_DIR}")
print(f"📚 Knowledge base directory: {KNOWLEDGE_BASE_DIR}")
