# 🏥 MedIntel - Quick Start Guide

## Installation Steps

### 1. Prerequisites

Make sure you have installed:

- Python 3.8 or higher
- pip (Python package manager)
- Git

Check your Python version:

```bash
python --version
```

### 2. Navigate to the Project

```bash
cd c:/Users/Mathir/EXPO/medintel
```

### 3. Create Virtual Environment

```bash
python -m venv venv
```

### 4. Activate Virtual Environment

**On Windows (Git Bash):**

```bash
source venv/Scripts/activate
```

**On Windows (CMD):**

```bash
venv\Scripts\activate
```

**On Windows (PowerShell):**

```bash
venv\Scripts\Activate.ps1
```

You should see `(venv)` at the start of your command prompt.

### 5. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This will take a few minutes and download ~500MB of packages.

### 6. Download Pre-trained Models

```bash
python download_models.py
```

When prompted, type `y` and press Enter.

This will download:

- BioBERT (~400MB)
- ClinicalBERT (~400MB)
- scispaCy models (~100MB)

**Total download: ~1GB** (one-time only)

### 7. Create Environment File

```bash
cp .env.example .env
```

The default settings will work for local development.

### 8. Start the Backend Server

```bash
python main.py
```

You should see:

```
🏥 MedIntel - AI-Driven Healthcare Intelligence System
📍 Server: http://0.0.0.0:8000
📚 API Docs: http://0.0.0.0:8000/docs
```

### 9. Test the API

Open your browser and go to:

```
http://localhost:8000
```

You should see:

```json
{
  "message": "🏥 MedIntel API is running",
  "version": "1.0.0",
  "status": "healthy"
}
```

### 10. Explore API Documentation

Go to:

```
http://localhost:8000/docs
```

This shows all available API endpoints with interactive testing!

## Testing the Features

### Test 1: Medical Report Analysis

**Using the browser (go to /docs):**

1. Click on `/api/v1/analyze/report`
2. Click "Try it out"
3. Use this sample report:

```json
{
  "report_text": "Patient presents with Type 2 Diabetes Mellitus. Glucose: 145 mg/dL (Normal: 70-100). Prescribed Metformin 500mg twice daily."
}
```

4. Click "Execute"

### Test 2: Symptom Checker

1. Click on `/api/v1/analyze/symptoms`
2. Click "Try it out"
3. Use this sample:

```json
{
  "symptoms": ["fever", "cough", "fatigue"],
  "age": 35
}
```

4. Click "Execute"

### Test 3: Sample Endpoints

Try these URLs in your browser:

- http://localhost:8000/api/v1/analyze/report/sample
- http://localhost:8000/api/v1/analyze/symptoms/sample

## Common Issues & Solutions

### Issue: "transformers" module not found

**Solution:**

```bash
pip install transformers torch
```

### Issue: "spacy" module not found

**Solution:**

```bash
pip install spacy
python -m spacy download en_core_web_sm
```

### Issue: Port 8000 already in use

**Solution:** Change the port in `.env`:

```
API_PORT=8001
```

### Issue: Models downloading slowly

**Solution:**

- Make sure you have a good internet connection
- The models are large (~1GB total)
- Download will only happen once

### Issue: Python not found

**Solution:**

- Make sure Python is installed
- Try `python3` instead of `python`

## Next Steps

### Phase 1 Checklist:

- [x] Backend setup complete
- [x] API endpoints created
- [ ] Test with real medical reports
- [ ] Add more medical knowledge
- [ ] Create frontend UI

### To Add More Features:

1. Enhance entity extraction in `services/nlp_engine.py`
2. Add more symptom-disease mappings in `api/symptom_checker.py`
3. Integrate medical databases (ICD-10, RxNorm)
4. Build the frontend UI

### To Prepare for Expo:

1. Create sample medical reports
2. Test all features thoroughly
3. Prepare demo scenarios
4. Create presentation slides

## Development Commands

**Start server:**

```bash
python main.py
```

**Stop server:**
Press `Ctrl+C`

**Update dependencies:**

```bash
pip install -r requirements.txt
```

**Run tests:**

```bash
pytest
```

## Project Structure

```
medintel/
├── backend/
│   ├── main.py              # Main application entry
│   ├── config.py            # Configuration settings
│   ├── requirements.txt     # Python dependencies
│   ├── api/                 # API endpoints
│   │   ├── report_analyzer.py
│   │   ├── symptom_checker.py
│   │   └── ocr_service.py
│   ├── services/            # Business logic
│   │   ├── nlp_engine.py
│   │   └── report_analyzer.py
│   └── models/              # Downloaded ML models
├── frontend/                # (Coming next)
└── data/                    # Sample data
```

## Getting Help

If you encounter issues:

1. Check the error message carefully
2. Make sure all dependencies are installed
3. Verify Python version (3.8+)
4. Check if virtual environment is activated
5. Look at the logs in the terminal

## Success Indicators

You know everything is working when:

- ✅ Server starts without errors
- ✅ http://localhost:8000 shows API status
- ✅ /docs page loads and shows endpoints
- ✅ Sample endpoints return JSON responses
- ✅ No red error messages in terminal

## Resources

- **API Documentation:** http://localhost:8000/docs
- **Project README:** See README.md
- **Module Documentation:** See ../MODULES.md
- **Feasibility Analysis:** See ../FEASIBILITY_ANALYSIS.md

---

**🎉 Congratulations! MedIntel backend is now running!**

Next step: Test the API endpoints and start building the frontend.
