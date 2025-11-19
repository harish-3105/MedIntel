# MedIntel - AI-Driven Healthcare Intelligence System

## Overview

MedIntel is an advanced AI-driven healthcare intelligence system that bridges the gap between complex clinical information and real-world patient understanding.

## Features

- 💬 **Conversational AI Chat Interface** - Natural language interaction with medical AI
- 🏥 **Medical Report Analysis** - Extract and analyze findings from medical documents
- 🔍 **Intelligent Symptom Analysis** - Disease prediction and severity assessment
- 📁 **Document Processing** - Upload PDF, images, and DOCX files with OCR support
- 📊 **Patient-friendly Explanations** - Complex medical information simplified
- ⚠️ **Risk Assessment** - Urgency detection and red flag identification
- 🔒 **Privacy-focused** - Local processing with no external data storage

## Project Structure

```
medintel/
├── backend/
│   ├── models/          # Pre-trained ML models
│   ├── services/        # Core business logic
│   ├── api/             # REST API endpoints
│   └── knowledge_base/  # Medical databases (ICD-10, RxNorm, etc.)
├── frontend/            # Web UI
├── data/                # Sample data and datasets
├── tests/               # Unit and integration tests
└── docs/                # Documentation
```

## Tech Stack

- **Backend**: Python, FastAPI
- **ML/NLP**: PyTorch, Transformers, BioBERT, ClinicalBERT
- **Medical NLP**: scispaCy, Med7
- **Database**: PostgreSQL, MongoDB
- **Frontend**: React.js
- **Deployment**: Docker

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Git

### Installation

1. Clone the repository:

```bash
cd medintel
```

2. Set up Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install backend dependencies:

```bash
cd backend
pip install -r requirements.txt
```

4. Download pre-trained models:

```bash
python download_models.py
```

5. Install frontend dependencies:

```bash
cd ../frontend
npm install
```

### Running the Application

1. Start the backend server:

```bash
cd backend
python main.py
```

2. Start the frontend (in another terminal):

```bash
cd frontend
npm start
```

3. Access the application at `http://localhost:3000`

## Using the Chat Interface

MedIntel now features a unified conversational AI interface:

### Quick Start

1. Navigate to the **AI Chat** page
2. Type your symptoms or paste medical report text
3. Or upload a document (PDF, images, DOCX) for analysis
4. Get instant AI-powered insights

### Example Queries

- **Symptoms**: "I have been experiencing headache, fever, and fatigue for 2 days"
- **Reports**: Upload a blood test PDF and ask "What do these results mean?"
- **Follow-ups**: Ask clarifying questions based on AI responses

### Supported Files

- PDF documents (lab reports, prescriptions)
- Images (JPG, PNG) - OCR processed
- Word documents (DOCX)

See [CHAT_INTERFACE_GUIDE.md](CHAT_INTERFACE_GUIDE.md) for detailed usage instructions.

## Development Status

### Completed Features ✅

- [x] Project setup and architecture
- [x] Core NLP Engine (BioBERT + ClinicalBERT integration)
- [x] Medical Report Analyzer with OCR
- [x] Symptom Analysis Engine with disease prediction
- [x] Conversational AI Chat Interface
- [x] Risk assessment and urgency detection
- [x] Document processing (PDF, images, DOCX)
- [x] Modern responsive UI
- [x] API layer (FastAPI)
- [x] File upload system
- [x] Real-time analysis

### Future Enhancements 🚀

- [ ] Conversation history persistence
- [ ] Multi-language support
- [ ] Voice input capabilities
- [ ] Medical imaging analysis
- [ ] Wearable device integration
- [ ] Export to PDF reports

## Contributing

This is a college expo project. Contributions welcome!

## License

MIT License

## Contact

For questions or collaboration: [Your Email]

## Acknowledgments

- BioBERT (dmis-lab)
- ClinicalBERT (Emily Alsentzer)
- scispaCy
- National Library of Medicine (NLM) for free medical databases
