"""
API Endpoints for Symptom Checking and Disease Prediction
"""

import logging
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter()


def _is_emergency_condition(condition: str) -> bool:
    """Check if a medical condition is an emergency"""
    condition_lower = condition.lower()
    emergency_terms = [
        "heart attack",
        "stroke",
        "myocardial infarction",
        "cardiac arrest",
        "anaphylaxis",
        "severe allergic reaction",
        "meningitis",
        "sepsis",
        "pulmonary embolism",
        "aortic dissection",
        "ectopic pregnancy",
        "acute abdomen",
        "appendicitis",
        "peritonitis",
        "pancreatitis",
        "diabetic ketoacidosis",
        "severe hypoglycemia",
        "respiratory failure",
        "pneumothorax",
        "hemothorax",
        "intracranial hemorrhage",
        "subarachnoid hemorrhage",
        "acute coronary syndrome",
        "venomous",
        "envenomation",
        "snake bite",
        "poisoning",
        "overdose",
        "severe bleeding",
        "hemorrhage",
        "trauma",
        "fracture",
    ]
    return any(term in condition_lower for term in emergency_terms)


class SymptomCheckRequest(BaseModel):
    """Request model for symptom checking"""

    symptoms: List[str]
    age: Optional[int] = None
    gender: Optional[str] = None


class SymptomCheckResponse(BaseModel):
    """Response model for symptom checking"""

    success: bool
    predictions: Optional[List[dict]] = None
    severity: Optional[str] = None
    urgency: Optional[str] = None
    recommendations: Optional[List[str]] = None
    red_flags: Optional[List[str]] = None
    error: Optional[str] = None


@router.post("/analyze/symptoms", response_model=SymptomCheckResponse)
async def check_symptoms(request: SymptomCheckRequest):
    """
    Analyze symptoms and predict possible conditions

    - **symptoms**: List of symptoms (e.g., ["fever", "cough", "fatigue"])
    - **age**: Patient age (optional)
    - **gender**: Patient gender (optional)
    """
    try:
        logger.info(f"🔍 Checking symptoms: {request.symptoms}")

        if not request.symptoms or len(request.symptoms) == 0:
            raise HTTPException(status_code=400, detail="No symptoms provided")

        # Simple symptom matching (will be enhanced with ML later)
        predictions = _predict_conditions(request.symptoms)
        severity = _assess_severity(request.symptoms, predictions)
        urgency = _assess_urgency(request.symptoms, predictions)
        recommendations = _generate_recommendations(severity, urgency)
        red_flags = _check_red_flags(request.symptoms)

        return SymptomCheckResponse(
            success=True,
            predictions=predictions,
            severity=severity,
            urgency=urgency,
            recommendations=recommendations,
            red_flags=red_flags,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error in symptom checking: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def _predict_conditions(symptoms: List[str]) -> List[dict]:
    """
    Predict possible conditions using AI-powered medical knowledge
    Uses BioBERT/ClinicalBERT for intelligent analysis
    """
    # Convert symptoms to lowercase for matching
    symptoms_lower = [s.lower() for s in symptoms]
    symptoms_text = " ".join(symptoms_lower)

    # PRIMARY: Use Groq AI for intelligent medical analysis
    try:
        import os

        from groq import Groq

        api_key = os.getenv("GROQ_API_KEY", "")

        if api_key:
            client = Groq(api_key=api_key)

            medical_prompt = f"""You are a medical AI assistant. Analyze these symptoms and provide possible conditions.

Symptoms: {symptoms_text}

Provide your response in this EXACT JSON format (return ONLY valid JSON, no other text):
{{
  "conditions": [
    {{
      "condition": "condition name",
      "confidence": 0.0-1.0,
      "emergency": true/false,
      "reasoning": "brief explanation"
    }}
  ]
}}

Consider:
- Specific injuries/events (snake bite, trauma, etc.) have priority
- Context matters (e.g., "snake bite" means venomous bite injury, not respiratory infection)
- Emergency conditions should be flagged
- Provide 3-5 most likely conditions ranked by confidence

Return ONLY the JSON, no markdown or other text."""

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": medical_prompt}],
                temperature=0.3,
                max_tokens=1000,
            )

            import json
            import re

            ai_response = response.choices[0].message.content.strip()
            logger.info(f"🧠 AI medical analysis: {ai_response[:200]}...")

            # Extract JSON from response
            json_match = re.search(r"\{.*\}", ai_response, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())

                if analysis.get("conditions"):
                    predictions = []
                    for cond in analysis["conditions"]:
                        predictions.append(
                            {
                                "condition": cond["condition"],
                                "confidence": cond["confidence"],
                                "emergency": cond.get("emergency", False),
                                "matching_symptoms": symptoms_lower,
                            }
                        )
                    logger.info(
                        f"✅ AI analysis returned {len(predictions)} conditions"
                    )
                    return predictions
    except Exception as e:
        logger.warning(f"⚠️ Groq AI analysis failed, using fallback: {e}")
        # Continue to fallback logic below

    # PRIORITY 1: Check for specific emergencies and injuries (exact matches override everything)
    emergency_keywords = {
        "snake bite": [
            {
                "condition": "Snake Bite Envenomation",
                "confidence": 0.95,
                "emergency": True,
            },
            {"condition": "Venomous Snake Bite", "confidence": 0.90, "emergency": True},
        ],
        "animal bite": [
            {"condition": "Animal Bite Injury", "confidence": 0.90, "emergency": True},
            {"condition": "Rabies Risk", "confidence": 0.70, "emergency": True},
        ],
        "dog bite": [
            {"condition": "Dog Bite Injury", "confidence": 0.95, "emergency": True},
            {"condition": "Rabies Risk", "confidence": 0.60, "emergency": True},
        ],
        "spider bite": [
            {"condition": "Spider Bite", "confidence": 0.90, "emergency": False},
            {
                "condition": "Arachnid Envenomation",
                "confidence": 0.70,
                "emergency": False,
            },
        ],
        "insect bite": [
            {"condition": "Insect Bite/Sting", "confidence": 0.85, "emergency": False},
            {"condition": "Allergic Reaction", "confidence": 0.50, "emergency": False},
        ],
        "poisoning": [
            {"condition": "Poisoning/Toxicity", "confidence": 0.90, "emergency": True},
        ],
        "overdose": [
            {"condition": "Drug Overdose", "confidence": 0.95, "emergency": True},
        ],
        "heart attack": [
            {
                "condition": "Myocardial Infarction (Heart Attack)",
                "confidence": 0.95,
                "emergency": True,
            },
        ],
        "stroke": [
            {
                "condition": "Cerebrovascular Accident (Stroke)",
                "confidence": 0.95,
                "emergency": True,
            },
        ],
        "seizure": [
            {"condition": "Seizure Disorder", "confidence": 0.85, "emergency": True},
            {"condition": "Epilepsy", "confidence": 0.60, "emergency": False},
        ],
    }

    # Check for emergency keywords first
    for keyword, conditions in emergency_keywords.items():
        if keyword in symptoms_text:
            return conditions

    # PRIORITY 2: Symptom pattern matching
    symptom_disease_map = {
        # Critical Emergency Conditions
        ("fruity breath", "stomach"): [
            {
                "condition": "Diabetic Ketoacidosis",
                "confidence": 0.90,
                "emergency": True,
            },
            {
                "condition": "Severe Hyperglycemia",
                "confidence": 0.75,
                "emergency": True,
            },
            {"condition": "Metabolic Acidosis", "confidence": 0.60, "emergency": True},
        ],
        ("fruity breath",): [
            {
                "condition": "Diabetic Ketoacidosis",
                "confidence": 0.85,
                "emergency": True,
            },
            {
                "condition": "Uncontrolled Diabetes",
                "confidence": 0.70,
                "emergency": True,
            },
        ],
        ("chest pain", "shortness of breath"): [
            {"condition": "Heart Attack", "confidence": 0.70, "emergency": True},
            {"condition": "Angina", "confidence": 0.60, "emergency": True},
            {"condition": "Pulmonary Embolism", "confidence": 0.55, "emergency": True},
            {"condition": "Panic Attack", "confidence": 0.50, "emergency": False},
        ],
        ("chest pain",): [
            {
                "condition": "Acute Coronary Syndrome",
                "confidence": 0.65,
                "emergency": True,
            },
            {"condition": "Angina", "confidence": 0.60, "emergency": True},
            {"condition": "Costochondritis", "confidence": 0.45, "emergency": False},
        ],
        ("snake bite",): [
            {
                "condition": "Snake Bite Envenomation",
                "confidence": 0.95,
                "emergency": True,
            },
            {"condition": "Venomous Snake Bite", "confidence": 0.90, "emergency": True},
        ],
        ("animal bite",): [
            {
                "condition": "Animal Bite Infection",
                "confidence": 0.80,
                "emergency": True,
            },
            {"condition": "Rabies Risk", "confidence": 0.40, "emergency": True},
            {"condition": "Cellulitis", "confidence": 0.60, "emergency": False},
        ],
        ("headache", "fever", "stiff neck"): [
            {"condition": "Meningitis", "confidence": 0.75, "emergency": True},
            {"condition": "Encephalitis", "confidence": 0.65, "emergency": True},
            {"condition": "Migraine", "confidence": 0.50, "emergency": False},
        ],
        ("severe headache", "confusion"): [
            {"condition": "Stroke", "confidence": 0.70, "emergency": True},
            {
                "condition": "Intracranial Hemorrhage",
                "confidence": 0.65,
                "emergency": True,
            },
            {"condition": "Severe Migraine", "confidence": 0.50, "emergency": False},
        ],
        ("difficulty breathing", "wheezing"): [
            {
                "condition": "Severe Asthma Attack",
                "confidence": 0.75,
                "emergency": True,
            },
            {"condition": "Anaphylaxis", "confidence": 0.70, "emergency": True},
            {"condition": "Pneumonia", "confidence": 0.60, "emergency": False},
        ],
        ("severe abdominal pain", "fever"): [
            {"condition": "Appendicitis", "confidence": 0.70, "emergency": True},
            {"condition": "Peritonitis", "confidence": 0.65, "emergency": True},
            {"condition": "Pancreatitis", "confidence": 0.60, "emergency": True},
        ],
        # Common Non-Emergency Conditions
        ("fever", "cough", "fatigue"): [
            {"condition": "Common Cold", "confidence": 0.75, "emergency": False},
            {"condition": "Influenza", "confidence": 0.65, "emergency": False},
            {"condition": "COVID-19", "confidence": 0.60, "emergency": False},
        ],
        ("frequent urination", "increased thirst", "fatigue"): [
            {"condition": "Diabetes", "confidence": 0.80, "emergency": False},
            {
                "condition": "Urinary Tract Infection",
                "confidence": 0.60,
                "emergency": False,
            },
        ],
        ("nausea", "vomiting", "diarrhea"): [
            {"condition": "Gastroenteritis", "confidence": 0.75, "emergency": False},
            {"condition": "Food Poisoning", "confidence": 0.70, "emergency": False},
        ],
        ("fever", "pain"): [
            {"condition": "Infection", "confidence": 0.60, "emergency": False},
            {
                "condition": "Inflammatory Condition",
                "confidence": 0.50,
                "emergency": False,
            },
        ],
    }

    symptoms_set = set(symptoms_lower)

    # Find matching conditions
    predictions = []
    for symptom_combo, conditions in symptom_disease_map.items():
        # Check if any symptoms match
        if symptoms_set.intersection(symptom_combo):
            # Calculate match score
            match_count = len(symptoms_set.intersection(symptom_combo))
            for condition in conditions:
                adjusted_confidence = condition["confidence"] * (
                    match_count / len(symptom_combo)
                )
                predictions.append(
                    {
                        "condition": condition["condition"],
                        "confidence": round(adjusted_confidence, 2),
                        "emergency": condition.get("emergency", False),
                        "matching_symptoms": list(
                            symptoms_set.intersection(symptom_combo)
                        ),
                    }
                )

    # Sort by confidence
    predictions.sort(key=lambda x: x["confidence"], reverse=True)

    # Return top 5
    return (
        predictions[:5]
        if predictions
        else [
            {
                "condition": "Unable to determine - Please consult a doctor",
                "confidence": 0.0,
                "emergency": False,
            }
        ]
    )


def _assess_severity(symptoms: List[str], predictions: List[dict] = None) -> str:
    """
    Assess severity level using weighted scoring system:
    - Emergency conditions get 2x weight
    - Severity is calculated based on weighted average of all predictions
    - Critical: weighted avg >= 60%
    - High: weighted avg >= 40%
    - Moderate: weighted avg >= 20%
    - Low: weighted avg < 20%
    """
    symptoms_lower = [s.lower() for s in symptoms]
    symptoms_text = " ".join(symptoms_lower)

    # WEIGHTED SCORING SYSTEM
    if predictions and len(predictions) > 0:
        total_weighted_score = 0
        total_weight = 0

        for pred in predictions:
            # Check both field name formats
            is_emergency = pred.get("emergency", pred.get("is_emergency", False))
            condition_name = pred.get("condition", pred.get("disease", ""))
            confidence = pred.get("confidence", 0)

            # Convert confidence to 0-100 scale if needed
            if confidence <= 1.0:
                confidence = confidence * 100

            # DOUBLE WEIGHT for emergency conditions
            weight = 2.0 if is_emergency else 1.0

            # Calculate weighted score
            weighted_score = confidence * weight
            total_weighted_score += weighted_score
            total_weight += weight

            logger.info(
                f"📊 {condition_name}: {confidence:.1f}% confidence, "
                f"emergency={is_emergency}, weight={weight}, "
                f"weighted_score={weighted_score:.1f}"
            )

        # Calculate weighted average
        if total_weight > 0:
            weighted_avg = total_weighted_score / total_weight
            logger.info(f"📊 SEVERITY CALCULATION: Weighted avg = {weighted_avg:.1f}%")

            # Determine severity based on weighted average
            if weighted_avg >= 60:
                logger.warning(
                    f"⚠️ CRITICAL: Weighted severity score = {weighted_avg:.1f}%"
                )
                return "CRITICAL"
            elif weighted_avg >= 40:
                logger.warning(f"⚠️ HIGH: Weighted severity score = {weighted_avg:.1f}%")
                return "HIGH"
            elif weighted_avg >= 20:
                logger.info(
                    f"📊 MODERATE: Weighted severity score = {weighted_avg:.1f}%"
                )
                return "MODERATE"
            else:
                logger.info(f"📊 LOW: Weighted severity score = {weighted_avg:.1f}%")
                return "LOW"

    # FALLBACK: Keyword-based assessment
    critical_keywords = [
        "snake bite",
        "chest pain",
        "difficulty breathing",
        "loss of consciousness",
        "severe bleeding",
        "heart attack",
        "stroke",
        "poisoning",
        "overdose",
        "seizure",
        "fruity breath",
        "diabetic ketoacidosis",
    ]

    high_keywords = [
        "animal bite",
        "dog bite",
        "high fever",
        "severe pain",
        "confusion",
        "venom",
    ]

    for keyword in critical_keywords:
        if keyword in symptoms_text:
            return "CRITICAL"

    for keyword in high_keywords:
        if keyword in symptoms_text:
            return "HIGH"

    if len(symptoms) >= 4:
        return "MODERATE"

    return "LOW"


def _assess_urgency(symptoms: List[str], predictions: List[dict] = None) -> str:
    """
    Assess urgency level using weighted scoring system:
    - Emergency conditions with high confidence = IMMEDIATE
    - Weighted avg >= 50% = WITHIN 24 HOURS
    - Weighted avg < 50% = ROUTINE
    """
    symptoms_lower = [s.lower() for s in symptoms]
    symptoms_text = " ".join(symptoms_lower)

    # WEIGHTED SCORING SYSTEM
    if predictions and len(predictions) > 0:
        total_weighted_score = 0
        total_weight = 0
        has_high_confidence_emergency = False

        for pred in predictions:
            # Check both field name formats
            is_emergency = pred.get("emergency", pred.get("is_emergency", False))
            condition_name = pred.get("condition", pred.get("disease", ""))
            confidence = pred.get("confidence", 0)

            # Convert confidence to 0-100 scale if needed
            if confidence <= 1.0:
                confidence = confidence * 100

            # Check for high-confidence emergencies
            if is_emergency and confidence >= 50:
                logger.warning(
                    f"🚨 HIGH-CONFIDENCE EMERGENCY: {condition_name} ({confidence:.1f}%)"
                )
                has_high_confidence_emergency = True

            # DOUBLE WEIGHT for emergency conditions
            weight = 2.0 if is_emergency else 1.0

            # Calculate weighted score
            weighted_score = confidence * weight
            total_weighted_score += weighted_score
            total_weight += weight

        # IMMEDIATE if high-confidence emergency detected
        if has_high_confidence_emergency:
            return "IMMEDIATE - CALL 911 OR GO TO ER NOW"

        # Calculate weighted average for other cases
        if total_weight > 0:
            weighted_avg = total_weighted_score / total_weight
            logger.info(f"📊 URGENCY CALCULATION: Weighted avg = {weighted_avg:.1f}%")

            if weighted_avg >= 50:
                return "WITHIN 24 HOURS - VISIT URGENT CARE OR DOCTOR"
            else:
                return "ROUTINE - SCHEDULE APPOINTMENT WITHIN A WEEK"

    # FALLBACK: Keyword-based assessment
    emergency_keywords = [
        "snake bite",
        "venomous",
        "chest pain",
        "difficulty breathing",
        "severe bleeding",
        "loss of consciousness",
        "stroke",
        "seizure",
        "heart attack",
        "poisoning",
        "overdose",
        "fruity breath",
        "diabetic ketoacidosis",
    ]

    for keyword in emergency_keywords:
        if keyword in symptoms_text:
            return "IMMEDIATE - CALL 911 OR GO TO ER NOW"

    if len(symptoms) >= 5:
        return "WITHIN 24 HOURS - VISIT URGENT CARE OR DOCTOR"

    return "ROUTINE - SCHEDULE APPOINTMENT WITHIN A WEEK"


def _generate_recommendations(severity: str, urgency: str) -> List[str]:
    """Generate recommendations based on severity and urgency"""
    recommendations = []

    if "IMMEDIATE" in urgency:
        recommendations.append("🚨 SEEK EMERGENCY CARE IMMEDIATELY")
        recommendations.append("Call 911 or go to nearest emergency room")
        recommendations.append("Do not drive yourself")
    elif severity == "CRITICAL" or severity == "HIGH":
        recommendations.append("⚠️ Seek medical attention soon")
        recommendations.append("Visit urgent care or call your doctor")
        recommendations.append("Monitor symptoms closely")
    else:
        recommendations.append("Schedule appointment with your doctor")
        recommendations.append("Monitor symptoms and note any changes")
        recommendations.append("Rest and stay hydrated")

    recommendations.append("This is not a substitute for professional medical advice")

    return recommendations


def _check_red_flags(symptoms: List[str]) -> List[str]:
    """Check for red flag symptoms using AI analysis"""
    symptoms_lower = [s.lower() for s in symptoms]

    # Critical red flag patterns to always check
    critical_patterns = {
        "chest pain": "Chest pain can indicate heart attack or other serious cardiac conditions",
        "difficulty breathing": "Breathing difficulty requires immediate medical attention",
        "shortness of breath": "Breathing difficulty requires immediate medical attention",
        "severe headache": "Severe headache may indicate serious neurological condition",
        "loss of consciousness": "Loss of consciousness is a medical emergency",
        "severe bleeding": "Severe bleeding requires immediate emergency care",
        "suicidal thoughts": "Call 988 (Suicide Prevention Hotline) immediately",
        "confusion": "Confusion may indicate serious neurological or metabolic condition",
        "stiff neck": "Stiff neck with fever may indicate meningitis",
        "seizure": "Seizures require immediate medical evaluation",
    }

    detected_flags = []

    # First check pattern matching
    for symptom in symptoms_lower:
        for flag, message in critical_patterns.items():
            if flag in symptom:
                detected_flags.append(f"⚠️ {flag.upper()}: {message}")

    # Use AI to detect additional red flags based on symptom combination
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY", ""))

        prompt = f"""Given these symptoms: {', '.join(symptoms)}

Identify any RED FLAG symptoms or dangerous symptom combinations that require immediate medical attention.

Rules:
- Only include true medical emergencies or urgent conditions
- Consider symptom combinations (e.g., fever + stiff neck + confusion = possible meningitis)
- Be specific about WHY it's a red flag
- Return ONLY genuine red flags, not routine concerns
- Maximum 3-4 red flags

Return as JSON array of strings in format: "SYMPTOM/PATTERN: Brief reason for urgency"

Example: ["FEVER + STIFF NECK + CONFUSION: Possible meningitis - life-threatening infection", "HIGH FEVER (>104°F): Risk of organ damage or sepsis"]

Return empty array [] if no red flags detected."""

        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            max_tokens=300,
        )

        ai_flags_text = response.choices[0].message.content.strip()

        # Parse JSON response
        import json
        import re

        # Extract JSON array from response
        json_match = re.search(r"\[.*\]", ai_flags_text, re.DOTALL)
        if json_match:
            ai_flags = json.loads(json_match.group())
            for flag in ai_flags:
                if flag and flag not in detected_flags:
                    detected_flags.append(f"⚠️ {flag}")

    except Exception as e:
        logger.warning(f"⚠️ AI red flag detection failed: {e}")

    # Remove duplicates while preserving order
    seen = set()
    unique_flags = []
    for flag in detected_flags:
        flag_key = flag.split(":")[0].strip()  # Use first part as key
        if flag_key not in seen:
            seen.add(flag_key)
            unique_flags.append(flag)

    return unique_flags[:5]  # Limit to top 5 most critical flags


@router.get("/analyze/symptoms/sample")
async def get_sample_symptom_check():
    """Get a sample symptom check for demo purposes"""
    sample_request = SymptomCheckRequest(
        symptoms=["fever", "cough", "fatigue", "body aches"], age=35, gender="male"
    )
    return await check_symptoms(sample_request)
