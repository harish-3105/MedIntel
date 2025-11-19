"""
Core NLP Engine - Medical Entity Extraction
Using pre-trained BioBERT and ClinicalBERT
"""

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class MedicalNLPEngine:
    """Core NLP Engine for medical text processing"""

    def __init__(self):
        """Initialize the NLP engine with pre-trained models"""
        # Lazy load torch to avoid startup delays
        try:
            import torch

            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            logger.info(f"🖥️ Using device: {self.device}")
        except:
            self.device = "cpu"
            logger.info(f"🖥️ Using device: {self.device} (torch not available)")

        # Initialize models (will load pre-trained)
        self.biobert_model = None
        self.clinicalbert_model = None
        self.ner_pipeline = None

        logger.info("✅ Medical NLP Engine initialized")

    def load_models(self):
        """Load pre-trained models (call this after initialization)"""
        try:
            from transformers import AutoModel, AutoTokenizer, pipeline

            logger.info("📥 Loading BioBERT...")
            self.biobert_tokenizer = AutoTokenizer.from_pretrained(
                "dmis-lab/biobert-v1.1"
            )
            self.biobert_model = AutoModel.from_pretrained("dmis-lab/biobert-v1.1")
            logger.info("✅ BioBERT loaded")

            logger.info("📥 Loading ClinicalBERT...")
            self.clinicalbert_tokenizer = AutoTokenizer.from_pretrained(
                "emilyalsentzer/Bio_ClinicalBERT"
            )
            self.clinicalbert_model = AutoModel.from_pretrained(
                "emilyalsentzer/Bio_ClinicalBERT"
            )
            logger.info("✅ ClinicalBERT loaded")

            logger.info("📥 Loading NER pipeline...")
            self.ner_pipeline = pipeline(
                "ner",
                model="samrawal/bert-base-uncased_clinical-ner",
                device=0 if self.device == "cuda" else -1,
            )
            logger.info("✅ NER pipeline loaded")

            return True
        except Exception as e:
            logger.error(f"❌ Error loading models: {e}")
            return False

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract medical entities from text
        Returns: Dictionary with diseases, symptoms, medications, etc.
        """
        try:
            if self.ner_pipeline is None:
                logger.warning("⚠️ NER pipeline not loaded, loading now...")
                self.load_models()

            # Extract entities using NER
            entities = self.ner_pipeline(text)

            # Organize entities by type
            result = {
                "diseases": [],
                "symptoms": [],
                "medications": [],
                "procedures": [],
                "body_parts": [],
                "all_entities": [],
            }

            for entity in entities:
                entity_text = entity["word"]
                entity_type = entity["entity"]
                confidence = entity["score"]

                # Clean up entity text
                entity_text = entity_text.replace("##", "").strip()

                # Categorize entity
                if "PROBLEM" in entity_type:
                    result["diseases"].append(
                        {"text": entity_text, "confidence": confidence}
                    )
                elif "TREATMENT" in entity_type:
                    result["medications"].append(
                        {"text": entity_text, "confidence": confidence}
                    )
                elif "TEST" in entity_type:
                    result["procedures"].append(
                        {"text": entity_text, "confidence": confidence}
                    )

                result["all_entities"].append(
                    {"text": entity_text, "type": entity_type, "confidence": confidence}
                )

            # Remove duplicates
            result["diseases"] = self._remove_duplicates(result["diseases"])
            result["medications"] = self._remove_duplicates(result["medications"])
            result["procedures"] = self._remove_duplicates(result["procedures"])

            return result

        except Exception as e:
            logger.error(f"❌ Error extracting entities: {e}")
            return {
                "error": str(e),
                "diseases": [],
                "symptoms": [],
                "medications": [],
                "procedures": [],
                "body_parts": [],
                "all_entities": [],
            }

    def _remove_duplicates(self, entities: List[Dict]) -> List[Dict]:
        """Remove duplicate entities"""
        seen = set()
        unique = []
        for entity in entities:
            text_lower = entity["text"].lower()
            if text_lower not in seen:
                seen.add(text_lower)
                unique.append(entity)
        return unique

    def get_embeddings(self, text: str, model_type: str = "biobert"):
        """
        Get embeddings for text using BioBERT or ClinicalBERT
        """
        try:
            if model_type == "biobert":
                tokenizer = self.biobert_tokenizer
                model = self.biobert_model
            else:
                tokenizer = self.clinicalbert_tokenizer
                model = self.clinicalbert_model

            # Tokenize and get embeddings
            inputs = tokenizer(
                text, return_tensors="pt", padding=True, truncation=True, max_length=512
            )

            with torch.no_grad():
                outputs = model(**inputs)

            # Get [CLS] token embedding (sentence representation)
            embeddings = outputs.last_hidden_state[:, 0, :]

            return embeddings

        except Exception as e:
            logger.error(f"❌ Error getting embeddings: {e}")
            return None


# Global instance
nlp_engine = MedicalNLPEngine()


# Test function
def test_nlp_engine():
    """Test the NLP engine"""
    print("\n" + "=" * 60)
    print("🧪 Testing Medical NLP Engine")
    print("=" * 60 + "\n")

    # Load models
    print("📥 Loading models...")
    if not nlp_engine.load_models():
        print("❌ Failed to load models")
        return

    # Test text
    test_text = """
    Patient presents with Type 2 Diabetes Mellitus and Hypertension.
    Prescribed Metformin 500mg twice daily and Lisinopril 10mg once daily.
    Patient complains of frequent urination and increased thirst.
    """

    print(f"📝 Test text:\n{test_text}\n")

    # Extract entities
    print("🔍 Extracting entities...")
    entities = nlp_engine.extract_entities(test_text)

    print(f"\n✅ Results:")
    print(f"   Diseases: {len(entities['diseases'])}")
    for disease in entities["diseases"]:
        print(f"      - {disease['text']} (confidence: {disease['confidence']:.2f})")

    print(f"\n   Medications: {len(entities['medications'])}")
    for med in entities["medications"]:
        print(f"      - {med['text']} (confidence: {med['confidence']:.2f})")

    print(f"\n   Total entities: {len(entities['all_entities'])}")

    print("\n" + "=" * 60)
    print("✅ NLP Engine test complete!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    test_nlp_engine()
