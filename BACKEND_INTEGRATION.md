# MedIntel Backend Integration - Complete Guide

## 🎉 Issue Fixed

**Problem**: Frontend was showing error `name '_build_medical_system_prompt' is not defined`

**Solution**: The function `_build_medical_system_prompt()` was being called as a standalone function on line 1274 of `chat_service.py`, but it's actually a method of the `ConversationalAI` class. Fixed by calling it as `ai._build_medical_system_prompt(context)` instead.

---

## 🏗️ Backend Architecture

### Core Modules Integrated

1. **Chat Service** (`api/chat_service.py`)

   - Main conversational AI using Groq API (llama-3.3-70b-versatile)
   - Emergency detection and risk assessment
   - Context-aware conversations with 20-message history
   - Student mode for educational responses

2. **Symptom Checker** (`api/symptom_checker.py`)

   - AI-powered symptom analysis using Groq
   - Disease prediction with confidence scores
   - Severity assessment (LOW, MODERATE, HIGH, CRITICAL)
   - Urgency classification (NON_URGENT, ROUTINE, URGENT, EMERGENCY)
   - Red flag detection for emergency conditions

3. **Report Analyzer** (`api/report_analyzer.py`)

   - Medical report interpretation
   - Lab value extraction and analysis
   - Abnormality detection
   - Simplified explanations for patients

4. **OCR Service** (`api/ocr_service.py`)

   - PDF text extraction (PyPDF2, pdfplumber)
   - Image OCR (Tesseract, OpenCV)
   - Scanned document processing
   - Medical report parsing

5. **NLP Engine** (`services/nlp_engine.py`)
   - Medical entity recognition
   - Symptom extraction from text
   - Clinical term normalization

---

## 🔌 API Endpoints Available

### 1. Chat Endpoint (Primary)

```http
POST /api/v1/chat
Content-Type: application/json

{
  "question": "I have a headache and fever for 3 days",
  "context": "",
  "model_provider": "groq",
  "student_mode": false,
  "mode": "medical",
  "session_id": "session-123",
  "user_profile": {
    "age": 30,
    "gender": "male"
  }
}
```

**Response:**

```json
{
  "summary": "Medical guidance for: I have a headache and fever...",
  "answer": "Based on your symptoms of headache and fever lasting 3 days...",
  "risk_level": "Amber",
  "confidence": "High",
  "emotion": "supportive",
  "next_steps": [
    "Monitor symptoms closely",
    "Consult healthcare provider soon",
    "Keep track of any changes"
  ],
  "citations": ["MedIntel AI", "Medical Knowledge Base", "Clinical Guidelines"],
  "human_line": "Based on your symptoms...",
  "raw_text": "Full AI response text"
}
```

### 2. Symptom Analysis Endpoint

```http
POST /api/v1/chat/analyze-symptoms
Content-Type: application/json

{
  "conversation_history": [
    {"role": "user", "content": "I have chest pain"},
    {"role": "assistant", "content": "Can you describe the pain?"},
    {"role": "user", "content": "It's sharp and radiates to my left arm"}
  ],
  "patient_context": {
    "age": 45,
    "gender": "male"
  }
}
```

**Response:**

```json
{
  "status": "success",
  "extracted_data": {
    "symptoms": ["chest pain", "radiating pain", "left arm pain"],
    "duration": "unknown",
    "location": "chest",
    "onset": "unknown"
  },
  "medical_analysis": {
    "possible_conditions": [
      {
        "condition": "Myocardial Infarction (Heart Attack)",
        "confidence": 0.85,
        "emergency": true,
        "reasoning": "Chest pain with radiation to left arm is classic presentation"
      }
    ],
    "severity": "CRITICAL",
    "urgency": "EMERGENCY",
    "recommendations": [
      "🚨 CALL 911 IMMEDIATELY",
      "Chew aspirin if not allergic",
      "Do not drive yourself to hospital"
    ],
    "red_flags": ["Chest pain with radiation - possible cardiac emergency"]
  }
}
```

### 3. Report Analysis Endpoint

```http
POST /api/v1/analyze/report
Content-Type: application/json

{
  "report_text": "Complete Blood Count: Hemoglobin 10.2 g/dL (Low), WBC 12,000...",
  "patient_id": "patient-123"
}
```

### 4. OCR/Upload Endpoint

```http
POST /api/v1/ocr/upload
Content-Type: multipart/form-data

file: [medical_report.pdf]
```

---

## 🎯 How Frontend Uses Backend

### Current Integration in `ChatPage.jsx`

```javascript
// Line 103-114: Main chat API call
const response = await axios.post("/api/v1/chat", {
  question: text,
  context: currentReport?.extractedText || "",
  model_provider: activeMode === "student" ? "openai" : "gemini",
  student_mode: activeMode === "student",
  mode: activeMode,
  session_id: getSessionId(),
  user_profile: getUserProfile(),
});
```

### Response Handling

The frontend receives structured responses with:

- ✅ `summary` - Brief overview of the response
- ✅ `answer` - Full AI response text
- ✅ `risk_level` - "Green", "Amber", or "Red"
- ✅ `confidence` - Confidence level
- ✅ `emotion` - Emotional tone of response
- ✅ `next_steps` - Array of recommended actions
- ✅ `citations` - Sources used
- ✅ `human_line` - Conversational summary
- ✅ `raw_text` - Raw AI output

---

## 🔧 Backend Features Used

### 1. Emergency Detection

```python
# Automatically detects emergency keywords
is_emergency = ConversationManager.check_emergency_indicators(request.question)

if is_emergency:
    risk_level = "Red"
    next_steps = [
        "🚨 Call emergency services (911) immediately",
        "Do not delay seeking professional medical attention",
        "Stay calm and follow emergency protocols"
    ]
```

### 2. Context Awareness

- Maintains conversation history (20 messages)
- Remembers patient information
- References previous discussions
- Builds on earlier answers

### 3. Student Mode

- Detailed explanations with educational content
- Step-by-step breakdowns
- Medical terminology definitions
- Learning-focused responses

### 4. Risk Assessment

```python
# Three-tier risk system
"Green"  # Normal, non-urgent
"Amber"  # Needs attention, see doctor soon
"Red"    # Emergency, call 911 immediately
```

### 5. Intelligent Recommendations

- Tailored to risk level
- Specific action items
- Time-sensitive guidance
- Safety-first approach

---

## 🚀 Testing the Integration

### 1. Start Backend

```bash
cd backend
python main.py
# Server runs on http://0.0.0.0:8000
```

### 2. Start Frontend

```bash
cd frontend
npm run dev
# Server runs on http://127.0.0.1:5173
```

### 3. Test Cases

#### Test 1: Simple Question

```
User: "What should I do for a minor cut?"
Expected: Green risk level, practical first aid advice
```

#### Test 2: Urgent Symptoms

```
User: "I have severe chest pain radiating to my arm"
Expected: Red risk level, emergency instructions
```

#### Test 3: Student Mode

```
Toggle "Student Mode" ON
User: "How does insulin work?"
Expected: Detailed educational explanation
```

#### Test 4: Context Awareness

```
User: "I have wrist pain"
AI: "Can you describe the pain?"
User: "It hurts when I move it"
AI: Should reference "the wrist pain you mentioned"
```

---

## 📊 Backend Logs

When the chat endpoint is called, you'll see:

```
2025-11-19 21:33:16 - chat_service - INFO - Frontend chat request: I have a headache...
2025-11-19 21:33:17 - chat_service - INFO - ✅ Groq AI initialized for ChatGPT-level conversations
2025-11-19 21:33:18 - chat_service - INFO - 🤖 Generating AI response...
```

---

## ✅ What's Working Now

1. ✅ **Chat endpoint fixed** - No more `_build_medical_system_prompt` error
2. ✅ **Symptom analysis** - AI extracts symptoms and analyzes them
3. ✅ **Report analyzer** - Interprets medical reports
4. ✅ **OCR service** - Processes PDF and image uploads
5. ✅ **Emergency detection** - Identifies critical situations
6. ✅ **Risk assessment** - Three-tier risk classification
7. ✅ **Context awareness** - 20-message conversation memory
8. ✅ **Student mode** - Educational explanations
9. ✅ **Groq AI integration** - Fast, ChatGPT-level responses
10. ✅ **CORS configured** - Frontend can communicate with backend

---

## 🔍 Debugging Tips

### Check Backend Logs

```bash
# Watch backend terminal for errors
cd backend
python main.py
```

### Check Frontend Console

```javascript
// Open browser DevTools (F12)
// Look for errors in Console tab
// Check Network tab for API calls
```

### Test API Directly

```bash
# Use curl or Postman
curl -X POST http://127.0.0.1:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "test", "mode": "medical"}'
```

---

## 📝 Key Files Modified

1. **`backend/api/chat_service.py`** (Line 1260-1350)

   - Fixed `_build_medical_system_prompt` bug
   - Enhanced risk assessment
   - Improved emergency detection
   - Added structured next steps

2. **`backend/config.py`**

   - Added CORS for port 5173
   - Configured proxy settings

3. **`frontend/src/pages/ChatPage.jsx`**
   - Already configured to use `/api/v1/chat`
   - Handles all response fields
   - Displays risk levels and next steps

---

## 🎓 How to Add New Features

### Add New Backend Endpoint

```python
# In api/chat_service.py or new router file
@router.post("/new-feature")
async def new_feature(request: dict):
    # Your logic here
    return {"result": "data"}
```

### Use in Frontend

```javascript
// In ChatPage.jsx or component
const response = await axios.post("/api/v1/new-feature", {
  data: "your-data",
});
```

---

## 📚 Resources

- **Backend**: FastAPI (Python 3.13.7)
- **Frontend**: React 18.3.1 + Vite 5.4.21
- **AI**: Groq API (llama-3.3-70b-versatile)
- **OCR**: Tesseract, OpenCV 4.12.0.88
- **Styling**: TailwindCSS 3.4.17

---

## 🐛 Known Issues & Solutions

1. **Groq API Rate Limit** (99,251/100,000 tokens)

   - Get new key from https://console.groq.com/
   - Update in `chat_service.py` or set `GROQ_API_KEY` env var

2. **EasyOCR Not Available**

   - Optional dependency, not critical
   - Tesseract OCR is working fine

3. **Deprecation Warnings**
   - Using `@app.on_event` (deprecated)
   - Will update to `lifespan` handlers later
   - Not affecting functionality

---

## ✨ Summary

**All your custom backend modules are now properly integrated with the React frontend:**

✅ Chat AI with Groq
✅ Symptom Checker
✅ Report Analyzer  
✅ OCR Service
✅ Emergency Detection
✅ Risk Assessment
✅ Context Awareness
✅ Student Mode

**Servers Running:**

- Backend: http://0.0.0.0:8000 ✅
- Frontend: http://127.0.0.1:5173 ✅

**Fixed Bug:** `_build_medical_system_prompt` error is resolved! 🎉
