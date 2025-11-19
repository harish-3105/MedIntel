# General Communication Capabilities - Implementation Guide

## Overview

Enhanced MedIntel AI Chat Interface with advanced general communication capabilities to better understand patients through natural conversation, context awareness, and intelligent intent detection.

## New Features

### 1. Intent Classification System

The AI now intelligently classifies user messages into different categories:

- **General Conversation**: Greetings, small talk, general questions
- **Symptom Check**: Messages describing symptoms or health concerns
- **Report Analysis**: Messages about medical reports or test results
- **Clarification**: Follow-up questions seeking more information
- **Emergency**: Urgent medical situations requiring immediate attention

### 2. Conversation History Management

- Tracks entire conversation flow
- Maintains context across messages
- Enables follow-up questions and clarifications
- Stores conversation in browser memory

### 3. Patient Context Profile

New patient profile system that stores:

- **Demographics**: Age, gender
- **Medical History**: Chronic conditions, past diagnoses
- **Current Medications**: Active prescriptions
- **Allergies**: Known allergic reactions
- **Lifestyle**: Smoking, exercise, diet habits

### 4. Emergency Detection

Automatically identifies emergency keywords and provides:

- Urgent warning messages
- Emergency contact recommendations
- Immediate action guidance
- Escalation to human intervention flag

### 5. Follow-up Questions

AI generates contextual follow-up questions based on:

- Intent type
- Message content
- Conversation history
- Patient context

## API Endpoints

### POST /api/v1/chat/message

Main chat endpoint for general communication.

**Request:**

```json
{
  "message": "I have been feeling dizzy lately",
  "conversation_history": [
    {
      "role": "user",
      "content": "Hello",
      "timestamp": "2024-11-18T10:00:00Z"
    },
    {
      "role": "assistant",
      "content": "Hello! How can I help?",
      "timestamp": "2024-11-18T10:00:01Z"
    }
  ],
  "patient_context": {
    "age": 45,
    "gender": "female",
    "medical_history": ["hypertension", "diabetes"],
    "current_medications": ["metformin", "lisinopril"]
  }
}
```

**Response:**

```json
{
  "response": "I can see you're describing symptoms...",
  "intent": "symptom_check",
  "confidence": 0.85,
  "follow_up_questions": [
    "How long have you been experiencing these symptoms?",
    "Have you noticed any triggers or patterns?",
    "Are you currently taking any medications?"
  ],
  "requires_human_intervention": false
}
```

### POST /api/v1/chat/context

Update patient context information.

**Request:**

```json
{
  "age": 35,
  "gender": "male",
  "medical_history": ["asthma"],
  "current_medications": ["albuterol"],
  "allergies": ["penicillin"],
  "lifestyle": "non-smoker, regular exercise"
}
```

**Response:**

```json
{
  "status": "success",
  "message": "Patient context updated",
  "fields_updated": [
    "age",
    "gender",
    "medical_history",
    "current_medications",
    "allergies",
    "lifestyle"
  ]
}
```

### GET /api/v1/chat/conversation/summary

Get conversation summary and insights.

**Response:**

```json
{
  "summary": "Conversation summary feature",
  "key_topics": ["symptom_discussion", "report_review"],
  "concerns_identified": [],
  "recommendations": [
    "Continue monitoring symptoms",
    "Consider scheduling follow-up with healthcare provider"
  ],
  "next_steps": "Further discussion needed"
}
```

## Intent Classification Logic

### Keyword-Based Detection

**Symptom Keywords:**

- symptom, pain, ache, hurt, feel, experiencing
- fever, cough, headache, nausea, dizzy, tired
- fatigue, sick, sore, swelling, rash, itching
- vomiting, diarrhea, breathing, chest, stomach
- back, joint, muscle, throat, ear, nose

**Report Keywords:**

- report, test, result, lab, blood, urine
- x-ray, scan, mri, ct, ultrasound, biopsy
- diagnosis, prescribed, medication, treatment
- doctor said, hospital, clinic, prescription

**Greeting Keywords:**

- hello, hi, hey, good morning, good afternoon
- good evening, greetings, how are you, thanks
- thank you, bye, goodbye

**Clarification Keywords:**

- what, why, how, when, where, explain
- tell me more, elaborate, what does, mean
- understand, confused, unclear, help

### Confidence Scoring

```python
# Symptom detection
symptom_score = count of symptom keywords in message
confidence = min(0.95, 0.6 + (symptom_score * 0.1))

# Report detection
report_score = count of report keywords in message
confidence = min(0.95, 0.6 + (report_score * 0.1))
```

## Emergency Detection System

### Emergency Keywords

- chest pain, can't breathe, cannot breathe
- difficulty breathing, severe pain
- unconscious, bleeding heavily, severe bleeding
- stroke, heart attack, seizure
- suicide, overdose, severe allergic
- anaphylaxis, choking, severe burn
- head injury, severe trauma, loss of consciousness

### Emergency Response

When emergency keywords detected:

```json
{
  "response": "⚠️ URGENT: Based on what you've described, this could be a medical emergency...",
  "intent": "emergency",
  "confidence": 1.0,
  "follow_up_questions": [],
  "requires_human_intervention": true
}
```

## Patient Context Usage

### How Context Enhances Responses

**Without Context:**

```
User: "I have chest pain"
AI: "Chest pain can have various causes..."
```

**With Context (age: 65, medical_history: ["heart disease"]):**

```
User: "I have chest pain"
AI: "Given your age and history of heart disease, chest pain requires immediate attention. Please call emergency services..."
```

### Context Storage

- **Frontend**: localStorage (browser-based)
- **Backend**: Validated and can be stored in database
- **Privacy**: All data stored locally, never shared externally

## Frontend Integration

### Patient Profile Modal

Access via chat header "Profile" button:

1. Opens modal form
2. User fills in demographics and medical information
3. Data saved to localStorage
4. Sent to backend for server-side processing
5. Used in all subsequent chat interactions

### Form Fields

- Age (number input)
- Gender (dropdown)
- Medical History (comma-separated text)
- Current Medications (comma-separated text)
- Allergies (comma-separated text)
- Lifestyle Notes (textarea)

### Conversation History

```javascript
chatHistory = [
  {
    role: "user",
    content: "I have a headache",
    timestamp: "2024-11-18T10:00:00Z",
  },
  {
    role: "assistant",
    content: "I understand you have a headache...",
    timestamp: "2024-11-18T10:00:01Z",
  },
];
```

## Message Flow

### Standard Message Flow

```
1. User types message
   ↓
2. Message sent to /api/v1/chat/message with history + context
   ↓
3. Backend classifies intent and confidence
   ↓
4. Backend generates appropriate response
   ↓
5. If intent = symptom_check → route to symptom analyzer
   If intent = report_analysis → route to report analyzer
   If intent = general/clarification → return conversational response
   If intent = emergency → return urgent warning
   ↓
6. Response displayed with follow-up questions
   ↓
7. Message added to conversation history
```

### File Upload Flow

```
1. User uploads file + optional message
   ↓
2. File sent directly to /api/v1/analyze/report/file
   ↓
3. OCR + Analysis performed
   ↓
4. Results formatted and displayed
   ↓
5. Message added to history
```

## Follow-up Questions Generation

### Based on Intent

**Symptom Check:**

- "How long have you been experiencing these symptoms?"
- "Have you noticed any triggers or patterns?"
- "Are you currently taking any medications?"
- "Do you have any existing medical conditions?"
- "On a scale of 1-10, how would you rate the severity?"

**Report Analysis:**

- "Do you have any questions about specific values in your report?"
- "Are you experiencing any symptoms related to these results?"
- "Has your doctor provided any recommendations?"
- "Would you like me to explain any medical terms?"
- "Do you need help understanding what these results mean?"

**General Conversation:**

- "Is there something specific about your health you'd like to discuss?"
- "Do you have any medical reports or test results to share?"
- "Are you experiencing any symptoms or concerns?"
- "Would you like information about a particular medical condition?"

## Usage Examples

### Example 1: First-Time User

```
User: "Hello"
AI: "Hello! I'm your MedIntel AI Assistant. I'm here to help you understand
     your health concerns better. You can:
     • Describe your symptoms for a preliminary analysis
     • Share or upload medical reports for review
     • Ask questions about medical terms or conditions
     • Get guidance on when to seek medical care

     How can I assist you today?"
```

### Example 2: Symptom Discussion

```
User: "I've had a headache for 3 days"
AI: [Detects symptom_check intent]
    [Routes to symptom analyzer]
    [Returns detailed symptom analysis]

    Follow-up Questions:
    • How severe is the pain on a scale of 1-10?
    • Have you taken any pain medication?
    • Are you experiencing any other symptoms?
```

### Example 3: With Patient Context

```
User Profile:
- Age: 45
- Medical History: diabetes, hypertension
- Medications: metformin, lisinopril

User: "I feel dizzy when I stand up"
AI: "Given your age and medications (lisinopril can cause dizziness),
     this could be related to blood pressure changes. Let me analyze
     your symptoms more thoroughly considering your medical history..."
```

### Example 4: Emergency Situation

```
User: "I'm having severe chest pain and can't breathe"
AI: "⚠️ URGENT: Based on what you've described, this could be a
     medical emergency.

     PLEASE TAKE IMMEDIATE ACTION:
     • Call emergency services (911) immediately
     • Go to the nearest emergency room
     • If symptoms worsen, don't wait - seek help NOW

     Do not rely on this AI for emergency medical advice."
```

### Example 5: Clarification Request

```
User: "I got my blood test results"
AI: "I understand you'd like me to analyze a medical report. For the
     best results:
     • Upload the report file (PDF, image, or DOCX)
     • Or paste the text content of the report
     • Let me know what specific aspects you'd like me to focus on"

User: "What does elevated glucose mean?"
AI: [Detects clarification intent]
    "Elevated glucose (blood sugar) means your blood sugar levels are
     higher than normal range. This could indicate..."
```

## Technical Implementation

### Backend Components

**IntentClassifier Class:**

- Keyword matching for different intents
- Confidence scoring algorithm
- History-aware classification

**ConversationManager Class:**

- Generate contextual responses
- Create follow-up questions
- Emergency detection and response
- Context-aware prompt generation

**ChatRequest Model:**

```python
class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[Message]] = []
    patient_context: Optional[dict] = None
```

**ChatResponse Model:**

```python
class ChatResponse(BaseModel):
    response: str
    intent: str
    confidence: float
    follow_up_questions: Optional[List[str]] = []
    requires_human_intervention: bool = False
```

### Frontend Components

**Chat Functions:**

- `processChatMessage()` - Send to chat service
- `getPatientContext()` - Retrieve stored context
- `formatFollowUpQuestions()` - Display questions nicely

**Modal Functions:**

- `showPatientContextModal()` - Open profile form
- `closePatientContextModal()` - Close profile form
- Form submission handler for saving context

**State Management:**

```javascript
let chatHistory = []; // Conversation history
let currentFile = null; // Currently attached file
```

## Privacy & Security

### Data Handling

- All context stored in browser localStorage
- No external data transmission
- Server-side validation of context fields
- Optional backend storage (not implemented by default)

### Allowed Context Fields

- age, gender, weight, height
- medical_history, current_medications
- allergies, family_history, lifestyle

### Data Not Stored

- Personal identifiers (name, SSN, address)
- Insurance information
- Contact details
- Financial information

## Benefits of General Communication

### 1. Better Understanding

- AI adapts to user communication style
- Conversational flow feels natural
- Less rigid than form-based input

### 2. Personalized Responses

- Context-aware suggestions
- Age-appropriate recommendations
- History-conscious analysis

### 3. Continuous Learning

- Conversation history provides context
- Follow-up questions gather more information
- Iterative refinement of understanding

### 4. Emergency Safety

- Automatic detection of urgent situations
- Clear guidance for emergencies
- Human intervention flags

### 5. User Engagement

- More interactive experience
- Encourages detailed information sharing
- Builds trust through natural dialogue

## Future Enhancements

### Planned Features

1. **Conversation Memory**

   - Persistent history across sessions
   - Long-term patient tracking
   - Trend analysis over time

2. **Advanced NLP**

   - Sentiment analysis
   - Emotion detection
   - Tone adjustment

3. **Multi-turn Conversations**

   - Complex diagnosis workflows
   - Guided symptom assessment
   - Interactive report review

4. **Voice Integration**

   - Speech-to-text input
   - Text-to-speech responses
   - Hands-free operation

5. **Multilingual Support**
   - Multiple language interfaces
   - Automatic translation
   - Cultural context awareness

## Testing the Feature

### Test Cases

**1. Test General Greeting:**

```
Input: "Hello"
Expected: Welcome message with capabilities list
```

**2. Test Intent Detection:**

```
Input: "I have a fever"
Expected: Routes to symptom analysis
```

**3. Test Patient Context:**

```
1. Open Profile modal
2. Fill in age: 35, medications: "aspirin"
3. Save profile
4. Send message with symptoms
Expected: Context used in analysis
```

**4. Test Emergency Detection:**

```
Input: "Severe chest pain"
Expected: Emergency warning message
```

**5. Test Follow-up Questions:**

```
Input: "My blood test shows high cholesterol"
Expected: Response includes 3-5 follow-up questions
```

**6. Test Clarification:**

```
Previous: AI explains blood pressure
Input: "What does that mean?"
Expected: Clarification based on previous message
```

## Troubleshooting

### Common Issues

**Issue:** Chat service not responding

- **Check:** Backend server running
- **Verify:** `/api/v1/chat/message` endpoint available
- **Solution:** Restart backend with new chat_service.py loaded

**Issue:** Patient context not saving

- **Check:** Browser localStorage enabled
- **Verify:** No browser privacy mode
- **Solution:** Check browser console for errors

**Issue:** Follow-up questions not showing

- **Check:** Response includes `follow_up_questions` array
- **Verify:** `formatFollowUpQuestions()` function working
- **Solution:** Check browser console for JS errors

**Issue:** Intent misclassification

- **Check:** Message contains relevant keywords
- **Adjust:** Add more specific keywords in message
- **Solution:** Provide more context in messages

## Conclusion

The general communication capabilities transform MedIntel from a simple form-based tool into an intelligent conversational health assistant that:

✅ Understands natural language
✅ Maintains conversation context
✅ Personalizes responses based on patient profile
✅ Detects emergencies automatically
✅ Provides guided interaction through follow-ups
✅ Routes intelligently to specialized analyzers
✅ Prioritizes patient safety and privacy

This creates a more engaging, helpful, and human-like interaction experience for users seeking medical information and guidance.
