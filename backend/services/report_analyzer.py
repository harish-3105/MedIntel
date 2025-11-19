"""
Medical Report Analyzer Service
Analyzes medical reports and provides simplified explanations
"""

import logging
import re
from typing import Any, Dict, List

from services.nlp_engine import nlp_engine

logger = logging.getLogger(__name__)


class ReportAnalyzer:
    """Analyzes medical reports and simplifies findings"""

    def __init__(self):
        self.nlp_engine = nlp_engine
        logger.info("✅ Report Analyzer initialized")

    def analyze_report(self, report_text: str) -> Dict[str, Any]:
        """
        Analyze a medical report using AI-powered analysis
        """
        try:
            logger.info("📄 Analyzing medical report with AI...")

            # PRIMARY: Use Groq AI for intelligent medical report analysis
            try:
                import json
                import os
                import re

                from groq import Groq

                api_key = os.getenv("GROQ_API_KEY", "")

                if api_key:
                    client = Groq(api_key=api_key)

                    analysis_prompt = f"""You are a medical AI assistant analyzing a medical report. Provide a comprehensive analysis in JSON format.

Medical Report:
{report_text[:3000]}

Analyze this report and provide response in this EXACT JSON format (return ONLY valid JSON):
{{
  "summary": "Brief 2-3 sentence summary of the report",
  "key_findings": [
    "Finding 1",
    "Finding 2",
    "Finding 3"
  ],
  "diseases_conditions": [
    {{"name": "condition", "status": "confirmed/suspected/ruled out"}}
  ],
  "lab_values": [
    {{"test": "test name", "value": "value", "unit": "unit", "status": "normal/high/low", "significance": "brief explanation"}}
  ],
  "medications": [
    {{"name": "medication", "purpose": "why prescribed"}}
  ],
  "abnormalities": [
    {{"finding": "abnormal finding", "severity": "mild/moderate/severe", "clinical_significance": "what it means"}}
  ],
  "severity": "NORMAL/MILD/MODERATE/SEVERE/CRITICAL",
  "recommendations": [
    "Recommendation 1",
    "Recommendation 2"
  ],
  "explanation": "Patient-friendly explanation of what the report means"
}}

Extract actual values, findings, and conditions from the report. Be specific and accurate."""

                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": analysis_prompt}],
                        temperature=0.3,
                        max_tokens=2000,
                    )

                    ai_response = response.choices[0].message.content.strip()
                    logger.info(
                        f"🧠 AI report analysis received ({len(ai_response)} chars)"
                    )
                    logger.info(f"Full AI response: {ai_response}")

                    # Extract JSON from response
                    json_match = re.search(r"\{.*\}", ai_response, re.DOTALL)
                    if json_match:
                        try:
                            analysis = json.loads(json_match.group())
                            logger.info(f"✅ Parsed JSON: {list(analysis.keys())}")

                            result = {
                                "success": True,
                                "summary": analysis.get("summary", "Analysis complete"),
                                "key_findings": analysis.get("key_findings", []),
                                "entities": {
                                    "diseases": [
                                        {
                                            "text": d.get("name", "Unknown"),
                                            "status": d.get("status", "unknown"),
                                        }
                                        for d in (
                                            analysis.get("diseases_conditions", [])
                                            or []
                                        )
                                    ],
                                    "medications": [
                                        {
                                            "text": m.get("name", "Unknown"),
                                            "purpose": m.get("purpose", ""),
                                        }
                                        for m in (analysis.get("medications", []) or [])
                                    ],
                                    "procedures": [],
                                },
                                "lab_values": analysis.get("lab_values", []),
                                "abnormalities": analysis.get("abnormalities", []),
                                "explanation": analysis.get(
                                    "explanation", "No detailed explanation available"
                                ),
                                "severity": analysis.get("severity", "UNKNOWN"),
                                "recommendations": analysis.get("recommendations", []),
                            }

                            logger.info("✅ AI report analysis complete")
                            return result
                        except json.JSONDecodeError as je:
                            logger.error(f"❌ JSON decode error: {je}")
                            logger.error(f"Failed JSON: {json_match.group()[:500]}")
                    else:
                        logger.warning("⚠️ No JSON found in AI response")
            except Exception as e:
                logger.error(f"⚠️ AI analysis failed: {e}", exc_info=True)
                # Continue to fallback logic below

            # FALLBACK: Use basic NLP extraction
            entities = self.nlp_engine.extract_entities(report_text)
            lab_values = self._extract_lab_values(report_text)
            abnormalities = self._identify_abnormalities(lab_values)
            summary = self._generate_summary(entities, abnormalities)
            explanation = self._create_explanation(entities, abnormalities)

            result = {
                "success": True,
                "summary": summary,
                "entities": {
                    "diseases": entities["diseases"],
                    "medications": entities["medications"],
                    "procedures": entities["procedures"],
                },
                "lab_values": lab_values,
                "abnormalities": abnormalities,
                "explanation": explanation,
                "severity": self._assess_severity(abnormalities),
                "recommendations": self._generate_recommendations(abnormalities),
            }

            logger.info("✅ Report analysis complete (fallback mode)")
            return result

        except Exception as e:
            logger.error(f"❌ Error analyzing report: {e}")
            return {"success": False, "error": str(e)}

    def _extract_lab_values(self, text: str) -> List[Dict[str, Any]]:
        """Extract lab values from report text"""
        lab_values = []

        # Common lab test patterns
        patterns = [
            r"(\w+(?:\s+\w+)?)\s*:\s*([0-9.]+)\s*(\w+/?\w*)",  # Test: Value Unit
            r"(\w+(?:\s+\w+)?)\s+([0-9.]+)\s+(\w+/?\w*)",  # Test Value Unit
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                test_name = match.group(1).strip()
                value = float(match.group(2))
                unit = match.group(3).strip() if len(match.groups()) >= 3 else ""

                # Check if this looks like a lab test
                if self._is_lab_test(test_name):
                    lab_values.append(
                        {
                            "test": test_name,
                            "value": value,
                            "unit": unit,
                            "normal_range": self._get_normal_range(test_name),
                            "status": "pending",  # Will be determined
                        }
                    )

        return lab_values

    def _is_lab_test(self, name: str) -> bool:
        """Check if name looks like a lab test"""
        common_tests = [
            "glucose",
            "hemoglobin",
            "wbc",
            "rbc",
            "platelet",
            "cholesterol",
            "hdl",
            "ldl",
            "triglycerides",
            "creatinine",
            "bun",
            "alt",
            "ast",
            "bilirubin",
            "sodium",
            "potassium",
            "calcium",
        ]
        name_lower = name.lower()
        return any(test in name_lower for test in common_tests)

    def _get_normal_range(self, test_name: str) -> Dict[str, float]:
        """Get normal range for a lab test"""
        # Simplified normal ranges (should come from database in production)
        normal_ranges = {
            "glucose": {"min": 70, "max": 100, "unit": "mg/dL"},
            "hemoglobin": {"min": 13, "max": 17, "unit": "g/dL"},
            "wbc": {"min": 4, "max": 11, "unit": "K/uL"},
            "cholesterol": {"min": 0, "max": 200, "unit": "mg/dL"},
            "creatinine": {"min": 0.6, "max": 1.2, "unit": "mg/dL"},
        }

        test_lower = test_name.lower()
        for key, range_val in normal_ranges.items():
            if key in test_lower:
                return range_val

        return {"min": 0, "max": 0, "unit": ""}

    def _identify_abnormalities(self, lab_values: List[Dict]) -> List[Dict]:
        """Identify abnormal lab values"""
        abnormalities = []

        for lab in lab_values:
            normal_range = lab["normal_range"]
            if not normal_range or normal_range["max"] == 0:
                continue

            value = lab["value"]
            min_val = normal_range["min"]
            max_val = normal_range["max"]

            if value < min_val:
                deviation = ((min_val - value) / min_val) * 100
                abnormalities.append(
                    {
                        "test": lab["test"],
                        "value": value,
                        "unit": lab["unit"],
                        "normal_range": f"{min_val}-{max_val}",
                        "status": "LOW",
                        "deviation": f"{deviation:.1f}% below normal",
                    }
                )
            elif value > max_val:
                deviation = ((value - max_val) / max_val) * 100
                abnormalities.append(
                    {
                        "test": lab["test"],
                        "value": value,
                        "unit": lab["unit"],
                        "normal_range": f"{min_val}-{max_val}",
                        "status": "HIGH",
                        "deviation": f"{deviation:.1f}% above normal",
                    }
                )

        return abnormalities

    def _generate_summary(self, entities: Dict, abnormalities: List[Dict]) -> str:
        """Generate a brief summary"""
        num_diseases = len(entities["diseases"])
        num_meds = len(entities["medications"])
        num_abnormal = len(abnormalities)

        summary = (
            f"Report contains {num_diseases} condition(s), {num_meds} medication(s)"
        )
        if num_abnormal > 0:
            summary += f", and {num_abnormal} abnormal lab value(s)"
        summary += "."

        return summary

    def _create_explanation(self, entities: Dict, abnormalities: List[Dict]) -> str:
        """Create patient-friendly explanation"""
        explanation = []

        if entities["diseases"]:
            explanation.append("**Conditions Identified:**")
            for disease in entities["diseases"][:3]:  # Top 3
                explanation.append(f"- {disease['text']}")

        if entities["medications"]:
            explanation.append("\n**Medications:**")
            for med in entities["medications"][:3]:  # Top 3
                explanation.append(f"- {med['text']}")

        if abnormalities:
            explanation.append("\n**Abnormal Values:**")
            for abn in abnormalities[:5]:  # Top 5
                explanation.append(
                    f"- {abn['test']}: {abn['value']} {abn['unit']} "
                    f"({abn['status']} - {abn['deviation']})"
                )

        return "\n".join(explanation) if explanation else "No significant findings."

    def _assess_severity(self, abnormalities: List[Dict]) -> str:
        """Assess overall severity"""
        if not abnormalities:
            return "NORMAL"
        elif len(abnormalities) <= 2:
            return "MILD"
        elif len(abnormalities) <= 4:
            return "MODERATE"
        else:
            return "SIGNIFICANT"

    def _generate_recommendations(self, abnormalities: List[Dict]) -> List[str]:
        """Generate recommendations based on findings"""
        if not abnormalities:
            return ["All values within normal range. Continue regular checkups."]

        recommendations = [
            "Consult with your healthcare provider about abnormal values.",
            "Share this report with your doctor during your next visit.",
        ]

        if len(abnormalities) >= 3:
            recommendations.append(
                "Consider scheduling a follow-up appointment within 1-2 weeks."
            )

        return recommendations


# Global instance
report_analyzer = ReportAnalyzer()
