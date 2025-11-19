"""
Chat Service API - AI-Powered Conversational Interface for Healthcare
Uses Groq API for fast, ChatGPT-level AI responses
"""

import json
import logging
import os
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])


# Initialize conversational AI with Groq
class ConversationalAI:
    """AI-powered conversational model using Groq API (free, fast alternative to OpenAI)"""

    _instance = None
    _client = None
    _model_name = (
        "llama-3.3-70b-versatile"  # Latest Llama model, excellent for conversations
    )

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        """Initialize Groq client"""
        try:
            from groq import Groq

            # Get API key from environment or config
            api_key = os.getenv("GROQ_API_KEY", "")

            if api_key and api_key != "your-groq-api-key-here":
                ConversationalAI._client = Groq(api_key=api_key)
                logger.info("✅ Groq AI initialized for ChatGPT-level conversations")
            else:
                logger.warning("⚠️ No Groq API key found, using fallback system")
                logger.info("💡 Get free API key at: https://console.groq.com/")
        except ImportError:
            logger.warning(
                "⚠️ Groq library not installed. Install with: pip install groq"
            )
        except Exception as e:
            logger.error(f"❌ Error initializing Groq: {e}")

    def _load_transformers(self):
        """Lazy load transformers library"""
        if not ConversationalAI._transformers_loaded:
            try:
                import torch
                from transformers import AutoModelForCausalLM, AutoTokenizer

                ConversationalAI._torch = torch
                ConversationalAI._AutoTokenizer = AutoTokenizer
                ConversationalAI._AutoModelForCausalLM = AutoModelForCausalLM
                ConversationalAI._transformers_loaded = True
                return True
            except Exception as e:
                logger.error(f"❌ Error loading transformers: {e}")
                return False
        return True

    def _initialize_model(self):
        """Initialize the conversational model"""
        try:
            # Lazy load transformers
            if not self._load_transformers():
                logger.info("⚠️ Transformers not available, using intelligent fallback")
                return

            logger.info("🤖 Initializing conversational AI model...")
            ConversationalAI._device = (
                "cuda" if ConversationalAI._torch.cuda.is_available() else "cpu"
            )

            # Use smaller, faster model for better performance
            # DialoGPT-small is much faster and still provides good conversation
            model_name = "microsoft/DialoGPT-small"
            logger.info(f"📥 Loading {model_name}...")

            ConversationalAI._tokenizer = (
                ConversationalAI._AutoTokenizer.from_pretrained(
                    model_name, cache_dir="./models/cache"
                )
            )
            ConversationalAI._model = (
                ConversationalAI._AutoModelForCausalLM.from_pretrained(
                    model_name, cache_dir="./models/cache"
                )
            )
            ConversationalAI._model.to(ConversationalAI._device)

            # Set padding token
            if ConversationalAI._tokenizer.pad_token is None:
                ConversationalAI._tokenizer.pad_token = (
                    ConversationalAI._tokenizer.eos_token
                )

            logger.info("✅ Conversational AI model loaded successfully")
        except Exception as e:
            logger.error(f"❌ Error loading conversational model: {e}")
            logger.info("⚠️ Will use intelligent fallback response system")
            # Model stays None, fallback will be used

    def generate_response(
        self, user_message: str, conversation_history: List[dict], context: dict = None
    ) -> str:
        """Generate AI response using Groq API for ChatGPT-level conversation"""

        if ConversationalAI._client is None:
            # Fallback if no API available
            return self._fallback_response(user_message, conversation_history, context)

        try:
            # Build system prompt for medical context
            system_prompt = self._build_medical_system_prompt(context)

            # Format conversation history for API
            messages = [{"role": "system", "content": system_prompt}]

            # Add conversation summary if history is long (better long-term context)
            if len(conversation_history) > 20:
                summary = self._summarize_early_conversation(conversation_history[:-20])
                if summary:
                    messages.append(
                        {
                            "role": "system",
                            "content": f"Earlier conversation summary: {summary}",
                        }
                    )

            # Add conversation history (last 20 messages for better context)
            recent_history = (
                conversation_history[-20:]
                if len(conversation_history) > 20
                else conversation_history
            )
            for msg in recent_history:
                # Handle both dict and object formats
                if isinstance(msg, dict):
                    role = msg.get("role", "user")
                    content = msg.get("content", "")
                else:
                    # Handle Message object or similar
                    role = getattr(msg, "role", "user")
                    content = getattr(msg, "content", "")

                messages.append({"role": role, "content": content})

            # Add current message
            messages.append({"role": "user", "content": user_message})

            # Call Groq API with better parameters for context
            response = ConversationalAI._client.chat.completions.create(
                model=ConversationalAI._model_name,
                messages=messages,
                temperature=0.7,
                max_tokens=800,  # More tokens for detailed, context-aware responses
                top_p=0.9,
            )

            # Extract response
            ai_response = response.choices[0].message.content.strip()

            return ai_response

        except Exception as e:
            logger.error(f"❌ Error calling Groq API: {e}")
            return self._fallback_response(user_message, conversation_history, context)

    def _summarize_early_conversation(self, early_messages: List[dict]) -> str:
        """Summarize earlier parts of long conversations for context retention"""
        try:
            # Extract key information from early conversation
            text = " ".join(
                [
                    (
                        msg.get("content", "")
                        if isinstance(msg, dict)
                        else getattr(msg, "content", "")
                    )
                    for msg in early_messages[-10:]  # Last 10 of the early messages
                ]
            )

            # Quick extraction of key medical details
            summary_parts = []
            if "pain" in text.lower() or "hurt" in text.lower():
                summary_parts.append("discussed pain/discomfort")
            if "medication" in text.lower() or "medicine" in text.lower():
                summary_parts.append("mentioned medications")
            if "doctor" in text.lower() or "hospital" in text.lower():
                summary_parts.append("talked about medical visits")
            if "test" in text.lower() or "report" in text.lower():
                summary_parts.append("discussed test results")

            return "; ".join(summary_parts) if summary_parts else ""
        except:
            return ""

    def extract_symptoms_from_conversation(
        self, conversation_history: List[dict]
    ) -> dict:
        """
        Extract structured symptom data from conversation history using AI
        This data will be passed to the medical analysis model
        """
        if ConversationalAI._client is None:
            return self._manual_symptom_extraction(conversation_history)

        try:
            # Create extraction prompt
            conversation_text = "\n".join(
                [
                    f"{msg.get('role', 'user') if isinstance(msg, dict) else getattr(msg, 'role', 'user')}: {msg.get('content', '') if isinstance(msg, dict) else getattr(msg, 'content', '')}"
                    for msg in conversation_history
                ]
            )

            extraction_prompt = f"""You are a medical assistant. Extract ALL health-related information from this conversation.

Conversation:
{conversation_text}

Extract symptoms, complaints, and health issues mentioned. Be INCLUSIVE - even if something seems minor, include it.

Examples:
- "dog bite on leg" → symptoms: ["dog bite", "animal bite", "leg injury", "bite wound"]
- "fruity breath" → symptoms: ["fruity breath", "abnormal breath odor"]
- "stomach pain" → symptoms: ["stomach pain", "abdominal pain"]
- "fever and cough" → symptoms: ["fever", "cough"]

Return ONLY a JSON object with this structure:
{{"symptoms": ["list"], "primary_symptom": "main", "location": "part", "duration": "time", "severity": "scale", "onset": "type", "timing": "when", "aggravating_factors": "worse", "alleviating_factors": "better", "associated_symptoms": ["other"], "frequency": "often", "progression": "trend"}}

IMPORTANT: symptoms array MUST have at least 1 item. Return ONLY valid JSON."""

            response = ConversationalAI._client.chat.completions.create(
                model=ConversationalAI._model_name,
                messages=[{"role": "user", "content": extraction_prompt}],
                temperature=0.3,
                max_tokens=1000,
            )

            extracted_text = response.choices[0].message.content.strip()

            # Try to parse JSON
            import re

            json_match = re.search(r"\{.*\}", extracted_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return json.loads(extracted_text)

        except Exception as e:
            logger.error(f"❌ Error extracting symptoms: {e}")
            return self._manual_symptom_extraction(conversation_history)

    def _manual_symptom_extraction(self, conversation_history: List[dict]) -> dict:
        """Fallback: manually extract symptoms from conversation"""
        symptoms = []
        all_text = " ".join(
            [
                (
                    msg.get("content", "")
                    if isinstance(msg, dict)
                    else getattr(msg, "content", "")
                )
                for msg in conversation_history
                if (
                    msg.get("role")
                    if isinstance(msg, dict)
                    else getattr(msg, "role", None)
                )
                == "user"
            ]
        )
        all_text_lower = all_text.lower()

        # Common symptom keywords
        symptom_keywords = [
            "pain",
            "ache",
            "fever",
            "cough",
            "headache",
            "nausea",
            "dizzy",
            "tired",
            "fatigue",
            "sore",
            "swelling",
            "rash",
            "vomiting",
        ]

        for keyword in symptom_keywords:
            if keyword in all_text_lower:
                symptoms.append(keyword)

        return {
            "symptoms": symptoms,
            "primary_symptom": symptoms[0] if symptoms else "unspecified",
            "raw_conversation": all_text[:500],  # First 500 chars
        }

    def _build_medical_system_prompt(self, context: dict = None) -> str:
        """Build system prompt for medical assistance"""
        prompt = (
            "You are MedIntel, a comprehensive medical AI assistant. "
            "You help with ALL health-related matters:\n"
            "• Minor injuries and first aid (cuts, bruises, sprains, hits, bumps)\n"
            "• Home remedies and self-care advice\n"
            "• Symptom analysis and disease prediction\n"
            "• Medical report interpretation\n"
            "• General health questions and wellness tips\n\n"
            "CONTEXT AWARENESS - YOU MUST:\n"
            "- REMEMBER everything the user has told you in this conversation\n"
            '- REFERENCE previous details they mentioned (e.g., "you mentioned your wrist pain earlier")\n'
            "- BUILD on previous answers instead of asking repeated questions\n"
            '- When they say "I told you" or "scroll up", acknowledge you have that information\n\n'
            "HANDLING DIFFERENT REQUESTS:\n\n"
            "1. MINOR INJURIES/FIRST AID (e.g., hit hand, small cut, bruise):\n"
            "   - Provide IMMEDIATE practical advice (RICE: Rest, Ice, Compression, Elevation)\n"
            "   - Suggest home remedies and over-the-counter treatments\n"
            "   - Explain what to do, what NOT to do\n"
            "   - Mention when to see a doctor (warning signs)\n"
            "   - Be direct and helpful - they need quick guidance\n\n"
            "2. COMPLEX SYMPTOMS (ongoing pain, multiple symptoms, unclear cause):\n"
            "   - Ask clarifying questions to gather complete details:\n"
            "     • Duration, severity, location, timing\n"
            "     • Triggers, relief factors, associated symptoms\n"
            "   - After gathering info, offer to run medical analysis\n"
            "   - Only trigger analysis when user says: 'analyze', 'that's all', 'done', 'give results'\n\n"
            "3. REMEDIES/TREATMENT QUESTIONS:\n"
            "   - Provide practical, evidence-based advice\n"
            "   - Suggest home remedies, medications, lifestyle changes\n"
            "   - Be specific (dosages, application methods, frequency)\n"
            "   - Always include safety warnings and when to seek professional help\n\n"
            "4. GENERAL HEALTH/WELLNESS:\n"
            "   - Answer directly with helpful information\n"
            "   - Provide tips, explanations, and guidance\n"
            "   - Be informative and encouraging\n\n"
            "CRITICAL RULES:\n"
            "- NEVER ask for information already provided in the conversation\n"
            "- For simple injuries, give direct advice - don't over-complicate\n"
            "- For serious/emergency symptoms, IMMEDIATELY advise seeing a doctor\n"
            "- Always mention safety precautions and when professional help is needed\n"
            "- You CAN provide treatment advice for minor issues (OTC meds, home remedies)\n"
            "- Balance being helpful with being safe and responsible\n\n"
            "Communication:\n"
            "- Be warm, empathetic, and conversational\n"
            "- Match your response length to the question (simple Q = concise A)\n"
            "- Acknowledge what they share before providing advice\n"
            "- REFER to previous details they've shared to show you remember\n"
            "- Be practical and actionable - people need solutions, not just sympathy\n"
        )

        if context:
            prompt += "\n\nPatient context:\n"
            if context.get("age"):
                prompt += f"- Age: {context['age']} years old\n"
            if context.get("gender"):
                prompt += f"- Gender: {context['gender']}\n"
            if context.get("medical_history"):
                prompt += (
                    f"- Medical history: {', '.join(context['medical_history'])}\n"
                )
            if context.get("current_medications"):
                prompt += f"- Current medications: {', '.join(context['current_medications'])}\n"

        return prompt

    def _format_conversation(
        self, history: List[dict], current_message: str, system_prompt: str
    ) -> str:
        """Format conversation for the model"""
        # Start with system context
        conversation = system_prompt + "\n\n"

        # Add conversation history (last 5 exchanges to keep context manageable)
        recent_history = history[-10:] if len(history) > 10 else history
        for msg in recent_history:
            role = "User" if msg["role"] == "user" else "Assistant"
            conversation += f"{role}: {msg['content']}\n"

        # Add current message
        conversation += f"User: {current_message}\nAssistant:"

        return conversation

    def _ensure_medical_safety(self, response: str) -> str:
        """Ensure response includes medical disclaimers when appropriate"""
        # Check if giving medical advice
        advice_keywords = ["should", "recommend", "suggest", "try", "take", "avoid"]
        if any(keyword in response.lower() for keyword in advice_keywords):
            if "consult" not in response.lower() and "doctor" not in response.lower():
                response += "\n\nNote: This is general information. Please consult a healthcare professional for personalized medical advice."

        return response

    def _fallback_response(
        self, user_message: str, history: List[dict], context: dict = None
    ) -> str:
        """Intelligent fallback response when AI model is unavailable"""
        message_lower = user_message.lower()

        # Get conversation context
        history_context = self._analyze_conversation_context(history)

        # Greetings - varied responses
        greetings = [
            "hello",
            "hi",
            "hey",
            "good morning",
            "good evening",
            "good afternoon",
        ]
        if (
            any(greeting in message_lower for greeting in greetings)
            and len(message_lower) < 20
        ):
            if len(history) == 0:
                return "Hey there! 👋 I'm MedIntel, your AI health assistant. I can help with:\n\n• Minor injuries & first aid\n• Symptom analysis\n• Medical report interpretation\n• Health questions & wellness\n\nWhat's on your mind today?"
            else:
                return "Hi! What else can I help you with?"

        # Thank you - acknowledge and offer more help
        if any(thanks in message_lower for thanks in ["thank", "thanks", "appreciate"]):
            responses = [
                "You're very welcome! I'm glad I could help. Is there anything else you'd like to know?",
                "Happy to help! Feel free to ask if you have more questions.",
                "You're welcome! Don't hesitate to ask if you need more information.",
            ]
            import random

            return random.choice(responses)

        # Goodbye
        if any(
            bye in message_lower for bye in ["bye", "goodbye", "see you", "farewell"]
        ):
            return "Take care of your health! Feel free to return anytime. Remember, for serious concerns, always consult with a healthcare professional."

        # How are you
        if "how are you" in message_lower or "how r u" in message_lower:
            return "I'm functioning well, thank you! More importantly, how are YOU feeling? I'm here to discuss any health concerns you might have."

        # Questions about capabilities
        if any(
            q in message_lower
            for q in [
                "what can you do",
                "what do you do",
                "how can you help",
                "what are you",
            ]
        ):
            return (
                "I'm a comprehensive AI health assistant. I can help you with:\n\n"
                "🩹 **First aid & remedies** - Minor injuries, cuts, bruises, sprains, how to ease pain\n"
                "💊 **Treatment advice** - Home remedies, OTC medications, self-care tips\n"
                "🔍 **Symptom analysis** - Understand what you're experiencing, get medical insights\n"
                "📄 **Report analysis** - Upload medical reports for interpretation\n"
                "💬 **General health** - Wellness tips, prevention, lifestyle advice\n\n"
                "Whether it's a small bump or ongoing symptoms, I'm here to help. What do you need?"
            )

        # Symptom-related - conversational response based on detail level
        symptom_keywords = [
            "pain",
            "hurt",
            "ache",
            "feel",
            "feeling",
            "symptom",
            "sick",
            "ill",
            "unwell",
            "fever",
            "cough",
            "headache",
            "dizzy",
            "nausea",
            "tired",
            "fatigue",
            "sore",
        ]
        if any(symptom in message_lower for symptom in symptom_keywords):
            # Check what info we already have
            has_duration = any(
                word in message_lower
                for word in [
                    "days",
                    "weeks",
                    "hours",
                    "yesterday",
                    "today",
                    "ago",
                    "since",
                ]
            )
            has_severity = any(
                word in message_lower
                for word in [
                    "severe",
                    "mild",
                    "moderate",
                    "bad",
                    "terrible",
                    "slight",
                    "/10",
                ]
            )
            has_location = any(
                word in message_lower
                for word in [
                    "head",
                    "chest",
                    "stomach",
                    "back",
                    "arm",
                    "leg",
                    "throat",
                    "neck",
                ]
            )

            # Build contextual response
            if has_duration and has_severity:
                return (
                    "I understand - you've mentioned some key details already. Let me make sure I have a complete picture. "
                    "Can you describe any other symptoms you're experiencing alongside this? Also, does anything make it better or worse?"
                )
            elif has_location:
                return (
                    f"I see you're experiencing discomfort. To help you better, could you tell me:\n\n"
                    f"• When did this start?\n"
                    f"• On a scale of 1-10, how severe is it?\n"
                    f"• Does it come and go, or is it constant?\n"
                    f"• Have you noticed any other symptoms?\n\n"
                    f"The more details you share, the better guidance I can provide."
                )
            else:
                return (
                    "I'm here to help you understand what you're experiencing. Could you tell me more? For example:\n\n"
                    "• Where exactly do you feel the discomfort?\n"
                    "• When did it begin?\n"
                    "• How would you rate the severity?\n"
                    "• Are there any other symptoms?\n\n"
                    "Share as much or as little as you're comfortable with."
                )

        # Medical report / test results
        if any(
            word in message_lower
            for word in [
                "report",
                "test",
                "result",
                "blood work",
                "lab",
                "scan",
                "xray",
                "x-ray",
                "mri",
            ]
        ):
            return (
                "I can help you understand your medical reports! You can:\n\n"
                "📤 **Upload the file** (PDF, image, or document)\n"
                "📋 **Paste the text** from your report\n"
                "❓ **Ask specific questions** about results you already shared\n\n"
                "I'll break down the findings in plain language and explain what they mean for your health."
            )

        # Very short/incomplete messages in ongoing conversation - be natural
        if len(history) > 2 and len(user_message.strip()) < 15:
            # Check recent context
            if history_context["discussing_symptoms"]:
                # They might be answering a question about severity, duration, etc.
                if any(
                    num in message_lower
                    for num in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
                ):
                    return (
                        "Got it. That helps me understand the intensity. "
                        "Can you tell me more about when this started and if anything makes it better or worse?"
                    )
                return (
                    "I see. Can you give me a bit more detail about that? "
                    "For example, how long has this been going on, and how would you rate the severity?"
                )

        # Follow-up in ongoing conversation
        if len(history) > 2:
            # Check what was discussed
            if history_context["discussing_symptoms"]:
                return (
                    "Thanks for sharing that. Let me make sure I have the full picture. "
                    "Is there anything else about your symptoms that seems important? "
                    "Like when they started, what makes them better or worse, or any other symptoms you've noticed?"
                )
            elif history_context["discussing_reports"]:
                return (
                    "I'm following along. Are there specific values or findings in your report you'd like me to explain? "
                    "Or would you like to know what these results might mean for your health?"
                )

        # Generic continuing conversation
        if len(history) > 0:
            return (
                "I'm here to help. Tell me more about what's going on. "
                "The more details you share, the better I can assist you."
            )

        # Default first message
        return (
            "Hello! I'm here to help with your health concerns. You can ask me about:\n\n"
            "• Symptoms you're experiencing\n"
            "• Medical reports or test results\n"
            "• General health questions\n\n"
            "What's on your mind?"
        )

    def _analyze_conversation_context(self, history: List[dict]) -> dict:
        """Analyze what's been discussed in the conversation"""
        context = {
            "discussing_symptoms": False,
            "discussing_reports": False,
            "message_count": len(history),
        }

        # Look through recent history
        recent = history[-5:] if len(history) > 5 else history
        for msg in recent:
            content_lower = msg.get("content", "").lower()
            if any(
                word in content_lower
                for word in ["pain", "symptom", "feel", "hurt", "ache"]
            ):
                context["discussing_symptoms"] = True
            if any(
                word in content_lower for word in ["report", "test", "result", "lab"]
            ):
                context["discussing_reports"] = True

        return context


class Message(BaseModel):
    """Single chat message"""

    role: str  # 'user' or 'assistant'
    content: str
    timestamp: Optional[str] = None


class ChatRequest(BaseModel):
    """Chat request with conversation history"""

    message: str
    conversation_history: Optional[List[Message]] = []
    patient_context: Optional[dict] = None  # Age, gender, medical history, etc.


class ChatResponse(BaseModel):
    """Chat response"""

    response: str
    intent: str  # 'symptom_check', 'report_analysis', 'general_conversation', 'clarification'
    confidence: float
    follow_up_questions: Optional[List[str]] = []
    requires_human_intervention: bool = False
    needs_more_info: bool = False  # Indicates if AI needs to gather more information
    ready_for_analysis: bool = False  # True when enough info collected to analyze


class IntentClassifier:
    """Classify user intent from conversation"""

    # Keywords for different intents
    SYMPTOM_KEYWORDS = [
        "symptom",
        "pain",
        "ache",
        "hurt",
        "feel",
        "experiencing",
        "fever",
        "cough",
        "headache",
        "nausea",
        "dizzy",
        "tired",
        "fatigue",
        "sick",
        "sore",
        "swelling",
        "rash",
        "itching",
        "vomiting",
        "diarrhea",
        "breathing",
        "chest",
        "stomach",
        "back",
        "joint",
        "muscle",
        "throat",
        "ear",
        "nose",
    ]

    REPORT_KEYWORDS = [
        "report",
        "test",
        "result",
        "lab",
        "blood",
        "urine",
        "x-ray",
        "scan",
        "mri",
        "ct",
        "ultrasound",
        "biopsy",
        "diagnosis",
        "prescribed",
        "medication",
        "treatment",
        "doctor said",
        "hospital",
        "clinic",
        "prescription",
    ]

    GREETING_KEYWORDS = [
        "hello",
        "hi",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
        "greetings",
        "how are you",
        "thanks",
        "thank you",
        "bye",
        "goodbye",
    ]

    CLARIFICATION_KEYWORDS = [
        "what",
        "why",
        "how",
        "when",
        "where",
        "explain",
        "tell me more",
        "elaborate",
        "what does",
        "mean",
        "understand",
        "confused",
        "unclear",
        "help",
    ]

    @classmethod
    def classify_intent(cls, message: str, history: List[Message]) -> tuple[str, float]:
        """
        Classify the intent of the user message

        Returns:
            (intent, confidence) tuple
        """
        message_lower = message.lower()

        # Check for greetings
        if any(kw in message_lower for kw in cls.GREETING_KEYWORDS):
            return "general_conversation", 0.9

        # Check for clarification questions
        if (
            any(kw in message_lower for kw in cls.CLARIFICATION_KEYWORDS)
            and len(history) > 0
        ):
            return "clarification", 0.85

        # Check for symptom-related content
        symptom_score = sum(1 for kw in cls.SYMPTOM_KEYWORDS if kw in message_lower)

        # Check for report-related content
        report_score = sum(1 for kw in cls.REPORT_KEYWORDS if kw in message_lower)

        # Determine intent based on scores
        if symptom_score > report_score and symptom_score > 0:
            confidence = min(0.95, 0.6 + (symptom_score * 0.1))
            return "symptom_check", confidence
        elif report_score > symptom_score and report_score > 0:
            confidence = min(0.95, 0.6 + (report_score * 0.1))
            return "report_analysis", confidence
        elif len(message.split()) < 5 and len(history) > 0:
            # Short message in context might be clarification
            return "clarification", 0.7
        else:
            return "general_conversation", 0.6


class ConversationManager:
    """Manage conversation context and generate appropriate responses"""

    # Varied greeting responses for natural conversation
    GREETINGS = [
        "Hello! I'm here to help with your health questions. What's on your mind today?",
        "Hi there! How can I assist you with your health concerns?",
        "Hey! I'm your MedIntel assistant. What would you like to discuss?",
        "Hello! Ready to help you understand your health better. What brings you here today?",
    ]

    FAREWELLS = [
        "Take care! Remember, if you have serious concerns, please consult a healthcare professional.",
        "Goodbye! Feel free to come back anytime you have health questions.",
        "Take care of yourself! Don't hesitate to return if you need more information.",
        "Wishing you good health! Remember, I'm here whenever you need assistance.",
    ]

    @staticmethod
    def generate_greeting_response(message: str = "") -> str:
        """Generate a friendly, varied greeting"""
        import random

        message_lower = message.lower()

        # Handle farewells
        if any(
            word in message_lower for word in ["bye", "goodbye", "see you", "take care"]
        ):
            return random.choice(ConversationManager.FAREWELLS)

        # Handle "how are you"
        if "how are you" in message_lower or "how r u" in message_lower:
            return (
                "I'm functioning well, thank you for asking! More importantly, "
                "how are YOU feeling? I'm here to help with any health concerns you might have."
            )

        # Handle thank you
        if any(word in message_lower for word in ["thanks", "thank you", "appreciate"]):
            return (
                "You're very welcome! I'm glad I could help. Is there anything else "
                "you'd like to know or discuss about your health?"
            )

        # Regular greeting
        return random.choice(ConversationManager.GREETINGS)

    @staticmethod
    def generate_clarification_response(history: List[Message]) -> str:
        """Generate response for clarification requests"""
        if len(history) == 0:
            return "I'd be happy to clarify! Could you please provide more context about what you'd like to know?"

        last_assistant_message = None
        for msg in reversed(history):
            if msg.role == "assistant":
                last_assistant_message = msg.content
                break

        if last_assistant_message:
            return (
                "I'm happy to explain further! Based on my previous response, is there "
                "a specific part you'd like me to elaborate on? Feel free to ask about:\n\n"
                "• Medical terms I used\n"
                "• The reasoning behind my recommendations\n"
                "• What specific symptoms or findings mean\n"
                "• Next steps you should consider"
            )
        else:
            return "What would you like to know more about? I'm here to help clarify any medical information."

    @staticmethod
    def generate_symptom_prompt(message: str, context: Optional[dict]) -> str:
        """Generate enhanced prompt for symptom analysis"""
        prompt_parts = [f"Patient reports: {message}"]

        if context:
            if context.get("age"):
                prompt_parts.append(f"Patient age: {context['age']}")
            if context.get("gender"):
                prompt_parts.append(f"Patient gender: {context['gender']}")
            if context.get("medical_history"):
                prompt_parts.append(
                    f"Medical history: {', '.join(context['medical_history'])}"
                )
            if context.get("current_medications"):
                prompt_parts.append(
                    f"Current medications: {', '.join(context['current_medications'])}"
                )

        return " | ".join(prompt_parts)

    @staticmethod
    def extract_symptom_info(history: List[Message]) -> dict:
        """Extract symptom information from conversation history"""
        info = {
            "symptoms_mentioned": [],
            "duration": None,
            "severity": None,
            "frequency": None,
            "triggers": None,
            "timing": None,
            "associated_symptoms": [],
            "alleviating_factors": None,
            "aggravating_factors": None,
            "previous_episodes": None,
            "medication_taken": None,
        }

        # Analyze conversation history for mentioned details
        for msg in history:
            if msg.role == "user":
                content_lower = msg.content.lower()

                # Check for duration mentions
                if not info["duration"]:
                    duration_keywords = [
                        "days",
                        "weeks",
                        "months",
                        "hours",
                        "yesterday",
                        "today",
                        "ago",
                    ]
                    if any(kw in content_lower for kw in duration_keywords):
                        info["duration"] = "mentioned"

                # Check for severity mentions
                if not info["severity"]:
                    severity_keywords = [
                        "severe",
                        "mild",
                        "moderate",
                        "unbearable",
                        "slight",
                        "intense",
                        "scale",
                        "/10",
                    ]
                    if any(kw in content_lower for kw in severity_keywords):
                        info["severity"] = "mentioned"

                # Check for timing patterns
                if not info["timing"]:
                    timing_keywords = [
                        "morning",
                        "evening",
                        "night",
                        "after eating",
                        "before",
                        "during",
                    ]
                    if any(kw in content_lower for kw in timing_keywords):
                        info["timing"] = "mentioned"

                # Check for triggers
                if not info["triggers"]:
                    trigger_keywords = [
                        "after",
                        "when",
                        "triggers",
                        "caused by",
                        "started when",
                    ]
                    if any(kw in content_lower for kw in trigger_keywords):
                        info["triggers"] = "mentioned"

        return info

    @staticmethod
    def generate_follow_up_questions(
        intent: str, message: str, history: List[Message] = None
    ) -> List[str]:
        """Generate contextual follow-up questions like a doctor would"""

        if intent == "symptom_check":
            # Analyze what info we already have
            symptom_info = ConversationManager.extract_symptom_info(history or [])
            questions = []

            # Ask SOCRATES-style questions (Symptom analysis framework used by doctors)
            # S - Site: Where is it?
            # O - Onset: When did it start?
            # C - Character: What is it like?
            # R - Radiation: Does it spread?
            # A - Associated symptoms: Anything else?
            # T - Timing: When does it occur?
            # E - Exacerbating/Alleviating factors: What makes it better/worse?
            # S - Severity: How bad is it?

            if not symptom_info["duration"]:
                questions.append(
                    "When did these symptoms first start? (hours, days, weeks ago?)"
                )

            if not symptom_info["severity"]:
                questions.append(
                    "On a scale of 1-10, how would you rate the severity? (1 being mild, 10 being the worst)"
                )

            if not symptom_info["timing"]:
                questions.append(
                    "Do the symptoms occur at specific times? (morning, after meals, at night?)"
                )

            if not symptom_info["triggers"]:
                questions.append(
                    "Have you noticed anything that triggers or worsens the symptoms?"
                )

            if not symptom_info["alleviating_factors"]:
                questions.append(
                    "Does anything make the symptoms better? (rest, medication, position?)"
                )

            if not symptom_info["medication_taken"]:
                questions.append(
                    "Have you taken any medications or tried any treatments for this?"
                )

            # Always ask about associated symptoms
            questions.append(
                "Are you experiencing any other symptoms alongside this? (fever, nausea, fatigue?)"
            )

            # Return first 3-4 most important questions
            return questions[:4]

        elif intent == "report_analysis":
            return [
                "Do you have any questions about specific values in your report?",
                "Are you experiencing any symptoms related to these results?",
                "Has your doctor provided any recommendations?",
                "Would you like me to explain any medical terms?",
            ]

        elif intent == "general_conversation":
            return [
                "Is there something specific about your health you'd like to discuss?",
                "Do you have any medical reports or test results to share?",
                "Are you experiencing any symptoms or concerns?",
            ]

        return []

    @staticmethod
    def check_if_ready_for_analysis(history: List[Message]) -> bool:
        """Check if we have enough information to provide analysis"""
        if len(history) < 3:  # Need at least a few exchanges
            return False

        symptom_info = ConversationManager.extract_symptom_info(history)

        # Need at least 3 key pieces of information
        info_count = sum(
            [
                1 if symptom_info["duration"] else 0,
                1 if symptom_info["severity"] else 0,
                1 if symptom_info["timing"] or symptom_info["triggers"] else 0,
            ]
        )

        return info_count >= 2  # At least 2 key details provided

    @staticmethod
    def generate_natural_response(
        intent: str, message: str, history: List[Message], context: Optional[dict]
    ) -> str:
        """Generate natural, context-aware responses"""
        import random

        message_lower = message.lower()

        # Handle general conversation with varied responses
        if intent == "general_conversation":
            # Greetings
            if any(
                kw in message_lower
                for kw in [
                    "hello",
                    "hi",
                    "hey",
                    "good morning",
                    "good afternoon",
                    "good evening",
                ]
            ):
                return ConversationManager.generate_greeting_response(message)

            # Thanks
            if any(kw in message_lower for kw in ["thanks", "thank you"]):
                return ConversationManager.generate_greeting_response(message)

            # Farewells
            if any(kw in message_lower for kw in ["bye", "goodbye", "see you"]):
                return ConversationManager.generate_greeting_response(message)

            # How are you
            if "how are you" in message_lower:
                return ConversationManager.generate_greeting_response(message)

            # General health discussion
            responses = [
                "I'm here to help with your health concerns. Could you tell me more about what's bothering you?",
                "I'd be happy to assist! What specific health topic would you like to discuss?",
                "Let's talk about your health. What's on your mind?",
                "I'm listening. Please share more details so I can provide better guidance.",
            ]
            return random.choice(responses)

        # Handle clarification with context
        elif intent == "clarification":
            if len(history) > 0:
                responses = [
                    "Let me explain that differently. What specific part would you like me to clarify?",
                    "I understand you need more information. What exactly would you like to know more about?",
                    "Sure, I can elaborate! Which aspect should I focus on?",
                    "Happy to provide more details. What's unclear?",
                ]
                return random.choice(responses)
            else:
                return "I'd love to help! What would you like to know?"

        # Handle symptom checking with doctor-like information gathering
        elif intent == "symptom_check":
            # Check if we have enough info to analyze
            ready_for_analysis = ConversationManager.check_if_ready_for_analysis(
                history
            )

            if ready_for_analysis:
                # Enough information gathered, proceed to analysis
                greeting = ""
                if context and context.get("age"):
                    greeting = "Thank you for providing those details. "
                else:
                    greeting = "I appreciate you sharing that information. "

                return (
                    f"{greeting}Now let me analyze what you've told me. I'll process your symptoms "
                    "along with the details you've provided about duration, severity, and timing to give you "
                    "a thorough preliminary assessment.\n\n"
                    "Analyzing your symptoms now..."
                )
            else:
                # Need more information - act like a doctor asking follow-up questions
                symptom_info = ConversationManager.extract_symptom_info(history)

                responses = [
                    "I understand. To help you better, I need to ask a few more questions about your symptoms.",
                    "Thank you for sharing that. Let me ask you some additional questions to get a clearer picture.",
                    "I see. To give you the most accurate assessment, I'd like to know a bit more.",
                    "Okay, I'm noting that down. A few more details will help me understand your situation better.",
                ]

                return random.choice(responses)

        # Handle report analysis
        elif intent == "report_analysis":
            responses = [
                (
                    "I can help you understand your medical report! You can either:\n"
                    "• Upload the file directly (PDF, image, or document)\n"
                    "• Paste the text from your report\n\n"
                    "I'll extract the key findings and explain what they mean in plain language. "
                    "What would you like me to focus on?"
                ),
                (
                    "Let's review your medical report together. Please share it by uploading the file "
                    "or pasting the content, and I'll help you understand the results and what they "
                    "might indicate about your health."
                ),
                (
                    "I'm ready to analyze your medical report! Once you upload or share it, "
                    "I'll break down the findings and help you understand what they mean. "
                    "Do you have any specific concerns about the results?"
                ),
            ]
            return random.choice(responses)

        # Default response
        else:
            return "I'm here to help with your health questions. Could you provide more details?"

    @staticmethod
    def check_emergency_indicators(message: str) -> bool:
        """Check if message contains emergency indicators"""
        emergency_keywords = [
            "chest pain",
            "can't breathe",
            "cannot breathe",
            "difficulty breathing",
            "severe pain",
            "unconscious",
            "bleeding heavily",
            "severe bleeding",
            "stroke",
            "heart attack",
            "seizure",
            "suicide",
            "overdose",
            "severe allergic",
            "anaphylaxis",
            "choking",
            "severe burn",
            "head injury",
            "severe trauma",
            "loss of consciousness",
        ]

        message_lower = message.lower()
        return any(kw in message_lower for kw in emergency_keywords)

    @staticmethod
    def generate_emergency_response() -> str:
        """Generate response for potential emergency situations"""
        return (
            "⚠️ **URGENT**: Based on what you've described, this could be a medical emergency.\n\n"
            "**PLEASE TAKE IMMEDIATE ACTION:**\n"
            "• Call emergency services (911 in US, 112 in EU, or your local emergency number)\n"
            "• Go to the nearest emergency room immediately\n"
            "• If symptoms worsen, don't wait - seek help NOW\n\n"
            "Do not rely on this AI for emergency medical advice. Your safety is the top priority."
        )


# Pydantic models for React frontend compatibility
class FrontendChatRequest(BaseModel):
    """Chat request from React frontend"""

    question: str
    context: Optional[str] = ""
    conversation_history: Optional[List[dict]] = []
    model_provider: Optional[str] = "groq"
    student_mode: bool = False
    mode: str = "medical"
    session_id: Optional[str] = None
    user_profile: Optional[dict] = None


class AnalysisResult(BaseModel):
    """Structured medical analysis result"""

    conditions: List[dict] = []
    severity: Optional[str] = None
    urgency: Optional[str] = None
    red_flags: List[str] = []
    recommendations: List[str] = []


class FrontendChatResponse(BaseModel):
    """Chat response for React frontend"""

    summary: str
    answer: str
    risk_level: str = "Green"
    confidence: str = "N/A"
    emotion: str = "neutral"
    next_steps: List[str] = []
    citations: List[str] = []
    human_line: Optional[str] = None
    raw_text: Optional[str] = None
    analysis: Optional[AnalysisResult] = None  # Structured analysis data


@router.post("", response_model=FrontendChatResponse)
async def chat_endpoint_for_frontend(request: FrontendChatRequest):
    """
    Main chat endpoint for React frontend - FULL BACKEND CAPABILITIES
    Endpoint: POST /api/v1/chat

    Features:
    - Context-aware conversations (20-message history)
    - Symptom extraction and analysis triggering
    - Intent classification and smart routing
    - Emergency detection with appropriate responses
    - Intelligent risk assessment
    - Report analysis integration
    - Student mode for educational content
    """
    try:
        logger.info(f"💬 Chat request: {request.question[:100]}")

        # Check for emergency indicators FIRST
        is_emergency = ConversationManager.check_emergency_indicators(request.question)

        if is_emergency:
            logger.warning(f"🚨 EMERGENCY detected: {request.question[:50]}")
            return FrontendChatResponse(
                summary="EMERGENCY - Immediate Action Required",
                answer=ConversationManager.generate_emergency_response(),
                risk_level="Red",
                confidence="High",
                emotion="urgent",
                next_steps=[
                    "🚨 CALL 911 OR LOCAL EMERGENCY NUMBER IMMEDIATELY",
                    "Do not wait or delay seeking emergency medical care",
                    "Stay on the line with emergency services",
                    "Follow dispatcher instructions carefully",
                ],
                citations=["Emergency Medical Protocols"],
                human_line="⚠️ This appears to be a medical emergency. Call 911 immediately.",
                raw_text=ConversationManager.generate_emergency_response(),
            )

        # Get conversational AI instance
        ai = ConversationalAI.get_instance()

        # Build full context for the conversation
        context = {
            "mode": request.mode,
            "student_mode": request.student_mode,
            "user_profile": request.user_profile,
            "report_context": request.context,
        }

        # Generate intelligent AI response with FULL conversation history
        conversation_history = request.conversation_history or []
        logger.info(
            f"📚 Using conversation history: {len(conversation_history)} messages"
        )

        try:
            ai_response = ai.generate_response(
                user_message=request.question,
                conversation_history=conversation_history,
                context=context,
            )
            using_fallback = False
        except Exception as ai_error:
            # Check if it's a rate limit error
            if "rate_limit" in str(ai_error).lower() or "429" in str(ai_error):
                logger.warning(f"⚠️ Groq API rate limit - using intelligent fallback")
                using_fallback = True
            else:
                logger.error(f"❌ AI error: {ai_error}")
                using_fallback = True

            # Generate response using fallback
            ai_response = ai._fallback_response(
                request.question, conversation_history, context
            )

        # Classify intent for intelligent routing
        intent, confidence = IntentClassifier.classify_intent(
            request.question, conversation_history
        )
        logger.info(f"🎯 Intent: {intent} (confidence: {confidence:.2f})")

        # Check if user wants analysis OR AI suggests it
        ready_for_analysis = False
        ai_lower = ai_response.lower()
        user_lower = request.question.lower()

        # User completion phrases
        completion_phrases = [
            "that's all",
            "thats all",
            "that's it",
            "thats it",
            "done",
            "finish",
            "finished",
            "analyze",
            "analyze now",
            "give me results",
            "give me the report",
            "show me results",
            "what's the diagnosis",
            "get the report",
            "run analysis",
        ]

        # AI trigger phrase - ONLY check user input, not AI response
        # This prevents automatic triggering
        if any(phrase in user_lower for phrase in completion_phrases):
            ready_for_analysis = True
            logger.info("✅ User requested analysis")

        # If ready for analysis, extract symptoms and run medical analysis
        if ready_for_analysis and len(conversation_history) > 2:
            logger.info("🔬 Extracting symptoms for medical analysis...")

            try:
                # Import symptom analysis functions
                from api.symptom_checker import (
                    _assess_severity,
                    _assess_urgency,
                    _check_red_flags,
                    _generate_recommendations,
                    _predict_conditions,
                )

                # Extract symptoms from conversation using AI
                symptom_data = ai.extract_symptoms_from_conversation(
                    conversation_history
                )
                symptoms_list = symptom_data.get("symptoms", [])

                if symptoms_list and len(symptoms_list) > 0:
                    logger.info(
                        f"📊 Extracted {len(symptoms_list)} symptoms: {symptoms_list}"
                    )

                    # Run full medical analysis
                    predictions = _predict_conditions(symptoms_list)
                    severity = _assess_severity(symptoms_list, predictions)
                    urgency = _assess_urgency(symptoms_list, predictions)
                    recommendations = _generate_recommendations(severity, urgency)
                    red_flags = _check_red_flags(symptoms_list)

                    # Create structured analysis data for frontend rendering
                    analysis_data = AnalysisResult(
                        conditions=[
                            {
                                "name": pred.get("condition", "Unknown"),
                                "confidence": f"{pred.get('confidence', 0)*100:.1f}%",
                                "reasoning": pred.get("reasoning", ""),
                                "emergency": pred.get("emergency", False),
                            }
                            for pred in predictions[:3]
                        ],
                        severity=severity,
                        urgency=urgency,
                        red_flags=red_flags if red_flags else [],
                        recommendations=recommendations if recommendations else [],
                    )

                    # Add simple text to AI response
                    ai_response += "\n\n📋 **Medical Analysis Complete**\n\nI've analyzed your symptoms. Please review the detailed results below."

                    # Update risk level based on analysis
                    risk_level = "Green"
                    if severity == "CRITICAL" or urgency == "EMERGENCY":
                        risk_level = "Red"
                    elif severity in ["HIGH", "MODERATE"] or urgency == "URGENT":
                        risk_level = "Amber"

                    # Use recommendations from medical analysis
                    next_steps = recommendations

                    logger.info(
                        f"✅ Medical analysis complete: Severity={severity}, Urgency={urgency}"
                    )
                else:
                    logger.warning(
                        "⚠️ No symptoms extracted, continuing with AI response only"
                    )
                    # Use basic risk assessment
                    risk_level = "Green"
                    if any(
                        word in request.question.lower()
                        for word in [
                            "severe",
                            "extreme",
                            "unbearable",
                            "worst",
                            "emergency",
                        ]
                    ):
                        risk_level = "Amber"

                    next_steps = [
                        "Monitor your symptoms",
                        "Consult healthcare provider if symptoms worsen",
                        "Keep track of any changes",
                    ]

            except Exception as analysis_error:
                logger.error(f"❌ Analysis error: {analysis_error}", exc_info=True)
                # Fallback to basic assessment
                risk_level = "Green"
                next_steps = [
                    "Monitor symptoms",
                    "Consult healthcare provider if needed",
                ]
        else:
            # Not ready for analysis - use basic risk assessment
            risk_level = "Green"

            # Intelligent risk assessment based on keywords and context
            question_lower = request.question.lower()

            if any(
                word in question_lower
                for word in [
                    "severe",
                    "intense",
                    "unbearable",
                    "worst",
                    "can't breathe",
                    "chest pain",
                    "stroke",
                    "heart attack",
                    "bleeding heavily",
                ]
            ):
                risk_level = "Amber"

            if any(
                word in question_lower for word in ["pain", "ache", "hurts", "sore"]
            ):
                if any(
                    word in question_lower
                    for word in ["severe", "intense", "10", "terrible"]
                ):
                    risk_level = "Amber"

            # Generate context-appropriate next steps
            if risk_level == "Amber":
                next_steps = [
                    "Monitor symptoms closely",
                    "Consult healthcare provider soon",
                    "Seek immediate care if symptoms worsen",
                    "Keep track of all changes",
                ]
            else:
                next_steps = [
                    "Follow the advice provided",
                    "Monitor your condition",
                    "Consult healthcare provider if symptoms worsen",
                ]

        # Determine emotion based on situation
        emotion = "supportive"
        if risk_level == "Red":
            emotion = "urgent"
        elif risk_level == "Amber":
            emotion = "concerned"
        elif "student" in request.mode.lower():
            emotion = "educational"

        # Create intelligent summary
        if intent == "symptom_analysis":
            summary = f"Symptom discussion: {request.question[:50]}..."
        elif intent == "report_analysis":
            summary = f"Report analysis: {request.question[:50]}..."
        elif request.student_mode:
            summary = f"Educational response: {request.question[:50]}..."
        else:
            summary = f"Medical guidance: {request.question[:50]}..."

        return FrontendChatResponse(
            summary=summary,
            answer=ai_response,
            risk_level=risk_level,
            confidence=f"{confidence:.2f}" if confidence else "High",
            emotion=emotion,
            next_steps=next_steps,
            citations=[
                "MedIntel AI (Groq - llama-3.3-70b)",
                "Medical Knowledge Base",
                "Clinical Guidelines",
            ],
            human_line=(
                ai_response[:200] + "..." if len(ai_response) > 200 else ai_response
            ),
            raw_text=ai_response,
            analysis=analysis_data if "analysis_data" in locals() else None,
        )

    except Exception as e:
        logger.error(f"❌ Error in chat endpoint: {e}", exc_info=True)
        return FrontendChatResponse(
            summary="Error occurred",
            answer=f"I apologize, but I encountered an error: {str(e)}. Please try again or rephrase your question.",
            risk_level="Green",
            confidence="N/A",
            emotion="neutral",
            next_steps=["Try rephrasing your question", "Check system status"],
            citations=["System"],
        )


@router.post("/message", response_model=ChatResponse)
async def process_chat_message(request: ChatRequest):
    """
    Process a chat message with AI-powered conversation understanding

    Uses conversational AI to understand context, maintain conversation flow,
    and provide intelligent, empathetic responses to health-related queries.
    """
    try:
        logger.info(f"Processing chat message: {request.message[:100]}")

        # Check for emergency indicators first
        is_emergency = ConversationManager.check_emergency_indicators(request.message)

        if is_emergency:
            return ChatResponse(
                response=ConversationManager.generate_emergency_response(),
                intent="emergency",
                confidence=1.0,
                follow_up_questions=[],
                requires_human_intervention=True,
            )

        # Get conversational AI instance
        ai = ConversationalAI.get_instance()

        # Generate AI response with full context
        ai_response = ai.generate_response(
            user_message=request.message,
            conversation_history=request.conversation_history,
            context=request.patient_context,
        )

        # Classify intent for routing purposes
        intent, confidence = IntentClassifier.classify_intent(
            request.message, request.conversation_history
        )

        logger.info(f"Detected intent: {intent} (confidence: {confidence:.2f})")

        # Check if user explicitly wants analysis OR AI triggers it
        ready_for_analysis = False

        ai_lower = ai_response.lower()
        user_lower = request.message.lower()

        # User completion phrases - they're done providing info
        user_completion_phrases = [
            "that's all",
            "that's it",
            "thats all",
            "thats it",
            "done",
            "finish",
            "finished",
            "analyze",
            "analyze now",
            "give me results",
            "give me the report",
            "show me results",
            "what's the diagnosis",
            "get the report",
            "run analysis",
        ]

        # AI trigger phrase - when AI decides to pass info
        ai_trigger_phrase = "pass this information to our medical analysis system"

        # Check if user says they're done
        user_wants_analysis = any(
            phrase in user_lower for phrase in user_completion_phrases
        )

        # Check if AI triggers analysis
        ai_triggers_analysis = ai_trigger_phrase in ai_lower

        if user_wants_analysis or ai_triggers_analysis:
            ready_for_analysis = True
            logger.info("🔍 Analysis triggered - user completed information gathering")

        # Always set needs_more_info unless analysis is triggered
        needs_more_info = not ready_for_analysis

        # No follow-up questions - AI handles conversation flow naturally
        follow_ups = []

        return ChatResponse(
            response=ai_response,
            intent=intent,
            confidence=confidence,
            follow_up_questions=follow_ups,
            requires_human_intervention=False,
            needs_more_info=needs_more_info,
            ready_for_analysis=ready_for_analysis,
        )

    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}")
        # Provide graceful fallback
        return ChatResponse(
            response=(
                "I apologize, but I'm having trouble processing your message right now. "
                "Could you rephrase your question? I'm here to help with:\n\n"
                "• Symptom discussion and preliminary assessment\n"
                "• Medical report analysis and interpretation\n"
                "• General health information and guidance\n\n"
                "What would you like to discuss?"
            ),
            intent="general_conversation",
            confidence=0.5,
            follow_up_questions=[],
            requires_human_intervention=False,
        )


@router.post("/analyze-symptoms")
async def analyze_symptoms_from_conversation(request: dict):
    """
    Extract symptoms from conversation and run through medical analysis models

    This endpoint:
    1. Uses AI to extract structured symptom data from conversation
    2. Passes the data to local medical models (BioBERT, ClinicalBERT)
    3. Returns medical analysis without legal issues
    """
    try:
        conversation_history = request.get("conversation_history", [])
        patient_context = request.get("patient_context", {})

        logger.info("🔬 Starting medical analysis from conversation")

        # Step 1: Extract structured symptom data using AI
        ai = ConversationalAI.get_instance()
        symptom_data = ai.extract_symptoms_from_conversation(conversation_history)

        # Ensure symptom_data is not None
        if symptom_data is None:
            symptom_data = {"symptoms": [], "primary_symptom": "unspecified"}

        logger.info(f"📊 Extracted symptoms: {symptom_data.get('symptoms', [])}")

        # Step 2: Import medical analysis functions directly
        from api.symptom_checker import (
            _assess_severity,
            _assess_urgency,
            _check_red_flags,
            _generate_recommendations,
            _predict_conditions,
        )

        symptoms_list = symptom_data.get("symptoms", [])

        if not symptoms_list:
            raise HTTPException(
                status_code=400,
                detail="No symptoms could be extracted from the conversation",
            )

        # Step 3: Run through medical analysis functions
        logger.info("🏥 Running medical analysis with medical system")

        predictions = _predict_conditions(symptoms_list)
        severity = _assess_severity(symptoms_list, predictions)
        urgency = _assess_urgency(symptoms_list, predictions)
        recommendations = _generate_recommendations(severity, urgency)
        red_flags = _check_red_flags(symptoms_list)

        # Build medical analysis response
        medical_analysis = {
            "possible_conditions": predictions or [],
            "severity": severity or "unknown",
            "urgency": urgency or "unknown",
            "recommendations": recommendations or [],
            "red_flags": red_flags or [],
            "extracted_info": {
                "duration": symptom_data.get("duration", "unknown"),
                "location": symptom_data.get("location", "unknown"),
                "onset": symptom_data.get("onset", "unknown"),
                "aggravating_factors": symptom_data.get(
                    "aggravating_factors", "unknown"
                ),
                "alleviating_factors": symptom_data.get(
                    "alleviating_factors", "unknown"
                ),
                "associated_symptoms": symptom_data.get("associated_symptoms", []),
            },
        }

        logger.info(
            f"✅ Medical analysis complete: {len(predictions)} conditions identified"
        )

        return {
            "status": "success",
            "extracted_data": symptom_data,
            "medical_analysis": medical_analysis,
            "note": "Analysis performed by local medical AI models",
        }

    except Exception as e:
        logger.error(f"❌ Error analyzing symptoms: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error analyzing symptoms: {str(e)}"
        )


@router.post("/context")
async def update_patient_context(context: dict):
    """
    Update patient context information

    Store demographic and medical history information to provide
    more personalized and accurate responses.
    """
    try:
        logger.info(f"Updating patient context: {context.keys()}")

        # In a production system, this would store to a database
        # For now, we'll just validate the structure

        allowed_fields = [
            "age",
            "gender",
            "weight",
            "height",
            "medical_history",
            "current_medications",
            "allergies",
            "family_history",
            "lifestyle",
        ]

        validated_context = {k: v for k, v in context.items() if k in allowed_fields}

        return {
            "status": "success",
            "message": "Patient context updated",
            "fields_updated": list(validated_context.keys()),
        }

    except Exception as e:
        logger.error(f"Error updating context: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating context: {str(e)}")


@router.get("/conversation/summary")
async def get_conversation_summary(conversation_id: Optional[str] = None):
    """
    Get a summary of the conversation

    Provides insights into what has been discussed, key concerns identified,
    and recommended next steps.
    """
    try:
        # In production, would retrieve actual conversation from database

        return {
            "summary": "Conversation summary feature",
            "key_topics": ["symptom_discussion", "report_review"],
            "concerns_identified": [],
            "recommendations": [
                "Continue monitoring symptoms",
                "Consider scheduling follow-up with healthcare provider",
            ],
            "next_steps": "Further discussion needed",
        }

    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error generating summary: {str(e)}"
        )
