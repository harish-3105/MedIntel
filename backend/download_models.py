"""
Download and cache pre-trained models for MedIntel
Run this script once to download all required models
"""

import os
from pathlib import Path

import spacy
from transformers import AutoModel, AutoTokenizer, pipeline


def download_transformers_models():
    """Download BioBERT and ClinicalBERT models"""
    print("\n" + "=" * 60)
    print("📥 Downloading Pre-trained Transformer Models")
    print("=" * 60 + "\n")

    models = [
        "dmis-lab/biobert-v1.1",
        "emilyalsentzer/Bio_ClinicalBERT",
        "samrawal/bert-base-uncased_clinical-ner",
    ]

    for model_name in models:
        try:
            print(f"📦 Downloading {model_name}...")
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModel.from_pretrained(model_name)
            print(f"✅ {model_name} downloaded successfully\n")
        except Exception as e:
            print(f"❌ Error downloading {model_name}: {e}\n")


def download_spacy_models():
    """Download scispaCy models"""
    print("\n" + "=" * 60)
    print("📥 Downloading spaCy Medical Models")
    print("=" * 60 + "\n")

    models = ["en_core_web_sm", "en_core_sci_md"]

    for model_name in models:
        try:
            print(f"📦 Downloading {model_name}...")
            os.system(f"python -m spacy download {model_name}")
            print(f"✅ {model_name} downloaded successfully\n")
        except Exception as e:
            print(f"❌ Error downloading {model_name}: {e}\n")


def verify_installations():
    """Verify all models are installed correctly"""
    print("\n" + "=" * 60)
    print("🔍 Verifying Model Installations")
    print("=" * 60 + "\n")

    # Test BioBERT
    try:
        from transformers import AutoModel

        model = AutoModel.from_pretrained("dmis-lab/biobert-v1.1")
        print("✅ BioBERT loaded successfully")
    except Exception as e:
        print(f"❌ BioBERT verification failed: {e}")

    # Test ClinicalBERT
    try:
        model = AutoModel.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
        print("✅ ClinicalBERT loaded successfully")
    except Exception as e:
        print(f"❌ ClinicalBERT verification failed: {e}")

    # Test scispaCy
    try:
        nlp = spacy.load("en_core_sci_md")
        print("✅ scispaCy loaded successfully")
    except Exception as e:
        print(f"⚠️ scispaCy verification failed: {e}")
        print("   Run: python -m spacy download en_core_sci_md")

    print("\n" + "=" * 60)
    print("✅ Model download and verification complete!")
    print("=" * 60 + "\n")


def main():
    """Main function to download all models"""
    print("\n" + "=" * 60)
    print("🏥 MedIntel - Model Downloader")
    print("=" * 60)
    print("\nThis will download ~2-3 GB of models.")
    print("Make sure you have a good internet connection.\n")

    response = input("Continue? (y/n): ")
    if response.lower() != "y":
        print("Download cancelled.")
        return

    # Download models
    download_transformers_models()
    download_spacy_models()

    # Verify installations
    verify_installations()

    print("\n🎉 All done! You can now run MedIntel.")
    print("   Start the server with: python main.py\n")


if __name__ == "__main__":
    main()
