# MedIntel AI Chat Interface Guide

## Overview

The MedIntel AI Chat Interface provides a unified, conversational way to interact with the medical AI assistant. Instead of separate forms for symptom checking and report analysis, users can now chat naturally with the AI assistant.

## Features

### 1. Unified Chat Experience

- Single conversational interface for all interactions
- Natural language processing for symptom analysis and report review
- Context-aware responses based on user input

### 2. Multi-Modal Input

- **Text Input**: Type symptoms, paste report text, or ask questions
- **File Upload**: Attach PDF, images, or DOCX files directly in chat
- **Quick Actions**: Pre-filled templates for common tasks

### 3. Intelligent Routing

The AI automatically detects the type of query:

- **Symptom Queries**: Keywords like "symptom", "pain", "fever", etc. trigger symptom analysis
- **Report Queries**: General medical text or file uploads are analyzed as reports
- **Contextual Understanding**: The AI adapts based on conversation flow

### 4. File Processing

Supported file types:

- **PDF**: Medical reports, lab results, prescriptions
- **Images** (JPG, PNG): Scanned documents, X-rays, lab results (OCR processed)
- **DOCX**: Word documents with medical information

## How to Use

### Starting a Conversation

1. Click the "Start AI Chat" button from the home page or navigate to "AI Chat" in the menu
2. You'll see a welcome message from the AI assistant
3. Start typing in the input box at the bottom

### Checking Symptoms

**Option 1: Natural Language**

```
Type: "I have been experiencing headache, fever, and fatigue for 2 days"
```

**Option 2: Quick Action**

1. Click the "Check Symptoms" quick action button
2. Complete the pre-filled text with your symptoms

**Example Inputs:**

- "I have a severe headache and nausea"
- "Experiencing chest pain, shortness of breath, and dizziness"
- "fever, cough, sore throat"

### Analyzing Reports

**Option 1: Paste Text**

```
Type: "Please analyze this medical report: [paste report text]"
```

**Option 2: Upload File**

1. Click the "Upload File" quick action button
2. Select your PDF, image, or DOCX file
3. Optionally add context: "This is my recent blood test"
4. Click send

**Option 3: Drag & Drop**

- Drag a file directly onto the chat input area

### Chat Interface Elements

#### Header

- **AI Assistant Name**: Shows "MedIntel AI Assistant"
- **Status Indicator**: Green dot shows the AI is ready
- **Clear Chat**: Remove all conversation history

#### Message Bubbles

- **User Messages**: Blue gradient, aligned to the right
- **AI Responses**: Light blue/purple background, aligned to the left
- **Timestamps**: Display when each message was sent

#### Input Area

- **Quick Actions**: Shortcuts for common tasks
  - Check Symptoms
  - Analyze Report
  - Upload File
- **Text Input**: Multi-line text area (Shift+Enter for new line)
- **File Attachment**: Preview of attached files
- **Send Button**: Submit message (or press Enter)

#### Loading Indicator

- Animated typing dots appear while AI is processing

## Understanding AI Responses

### Symptom Analysis Response

The AI provides:

- **Possible Conditions**: Ranked by confidence level
- **Severity**: Low, Medium, or High (color-coded)
- **Urgency**: Immediate, Soon, or Routine
- **Recommendations**: Next steps and care suggestions
- **Warning Signs**: Red flags to watch for

### Report Analysis Response

The AI provides:

- **Summary**: Overview of the report
- **Key Findings**: Important medical observations
- **Areas of Concern**: Abnormal results or findings
- **Recommendations**: Follow-up actions
- **Extracted Text**: OCR results from uploaded files

## Tips for Best Results

### For Symptom Checking

1. **Be Specific**: Include duration, severity, and associated symptoms
2. **List Multiple Symptoms**: Separate with commas or new lines
3. **Add Context**: Mention recent activities, medications, or medical history
4. **Use Common Terms**: "chest pain" instead of medical jargon

**Good Example:**

```
I have been experiencing sharp chest pain on the left side for 3 hours,
shortness of breath, sweating, and nausea. I'm 45 years old with a history
of high blood pressure.
```

### For Report Analysis

1. **Clear Images**: Ensure scanned documents are high-quality and readable
2. **Complete Text**: If pasting text, include all relevant sections
3. **Add Context**: Mention what type of report (blood test, X-ray, etc.)
4. **Multiple Pages**: For multi-page reports, combine into one PDF or upload separately with context

**Good Example with File:**

```
[Attach: blood_test_results.pdf]
"This is my annual blood work from last week. Are there any concerning values?"
```

### General Chat Tips

1. **One Topic at a Time**: Focus on one issue per message for clearer analysis
2. **Follow-Up Questions**: Ask for clarification or more details
3. **Privacy**: Don't include sensitive personal identifiers unnecessarily
4. **Disclaimer**: Remember this is informational; always consult healthcare professionals

## Keyboard Shortcuts

- **Enter**: Send message
- **Shift + Enter**: New line in message
- **Escape**: Clear current input (when empty)

## File Upload Specifications

### Maximum File Size

- All files: 10 MB maximum

### Supported Formats

- **PDF**: `.pdf`
- **Images**: `.jpg`, `.jpeg`, `.png`
- **Documents**: `.doc`, `.docx`
- **Text**: `.txt`

### OCR Processing

Images and scanned PDFs are automatically processed using:

- Advanced image preprocessing for better accuracy
- EasyOCR or Tesseract for text extraction
- Medical terminology recognition

## Privacy & Security

### Data Handling

- All processing happens locally on the server
- No data is sent to external AI services
- Uploaded files are temporarily stored during processing
- Chat history is stored in browser memory only
- Clear chat to remove all conversation data

### Disclaimers

Every AI response includes a medical disclaimer:

> "This is an AI-generated analysis. Please consult a healthcare professional for proper diagnosis and treatment."

## Technical Details

### API Endpoints Used

- `/api/v1/analyze/symptoms`: Symptom analysis
- `/api/v1/analyze/report`: Text-based report analysis
- `/api/v1/analyze/report/file`: File upload report analysis

### AI Models

- **BioBERT**: Biomedical text understanding
- **ClinicalBERT**: Clinical entity recognition
- **Clinical NER**: Named entity recognition for medical terms

### Response Time

- Text analysis: 1-3 seconds
- File processing: 3-10 seconds (depending on file size and OCR needs)
- Large files: May take longer for OCR processing

## Troubleshooting

### Common Issues

**Problem**: AI not responding

- **Solution**: Check if backend server is running (should be on port 8000)
- **Check**: Browser console for error messages

**Problem**: File upload fails

- **Solution**: Ensure file is under 10 MB and in supported format
- **Try**: Converting large files to lower resolution

**Problem**: OCR not extracting text

- **Solution**: Ensure image is clear and high-contrast
- **Try**: Taking a new photo with better lighting

**Problem**: Inaccurate symptom analysis

- **Solution**: Provide more detailed descriptions and context
- **Remember**: AI provides preliminary insights only

### Getting Help

If you encounter issues:

1. Check the API status indicator in the About page
2. Review browser console for error messages
3. Ensure both frontend (port 3000) and backend (port 8000) servers are running
4. Try refreshing the page

## Future Enhancements

Planned features:

- Conversation history persistence
- Export chat to PDF
- Voice input support
- Multi-language support
- Image analysis for medical imaging
- Integration with wearable health data

## Examples

### Example 1: Simple Symptom Check

**User**: "I have a headache and feel dizzy"

**AI Response**: Provides analysis with possible conditions, severity assessment, and recommendations

### Example 2: Report with Context

**User**: [Uploads blood_test.pdf] "What do these results mean?"

**AI Response**: Extracts test values, identifies abnormalities, explains findings in simple terms

### Example 3: Follow-up Question

**User**: "I have chest pain"
**AI**: [Provides analysis with high urgency]
**User**: "What should I do immediately?"
**AI**: [Provides specific emergency guidance]

## Medical Disclaimer

⚠️ **IMPORTANT**: The MedIntel AI Assistant is designed to provide informational insights based on AI analysis of medical data. It is NOT a substitute for professional medical advice, diagnosis, or treatment.

**Always**:

- Consult qualified healthcare professionals for medical concerns
- Seek immediate emergency care for severe or life-threatening symptoms
- Follow your doctor's advice over AI recommendations
- Use this tool as a supplementary information source only

**Never**:

- Use AI responses as a sole basis for medical decisions
- Delay seeking professional medical care based on AI feedback
- Share sensitive personal health information unnecessarily
- Rely on AI for emergency medical situations

---

## Getting Started Now

Ready to try the AI Chat Interface?

1. Navigate to the **AI Chat** page
2. Start with a simple question or symptom
3. Explore the quick actions for guided inputs
4. Upload a medical document to see OCR in action

The AI assistant is here to help you understand your health information better! 🩺
