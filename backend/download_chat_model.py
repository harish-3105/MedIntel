"""
Download conversational AI model for MedIntel chat interface
"""

import logging
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def download_chat_model():
    """Download the DialoGPT model for conversational AI"""
    try:
        from transformers import AutoModelForCausalLM, AutoTokenizer

        # Create cache directory
        cache_dir = Path("./models/cache")
        cache_dir.mkdir(parents=True, exist_ok=True)

        model_name = "microsoft/DialoGPT-small"

        logger.info(f"📥 Downloading {model_name}...")
        logger.info("This may take a few minutes...")

        # Download tokenizer
        logger.info("⬇️ Downloading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=str(cache_dir))

        # Download model
        logger.info("⬇️ Downloading model...")
        model = AutoModelForCausalLM.from_pretrained(
            model_name, cache_dir=str(cache_dir)
        )

        logger.info("✅ Chat model downloaded successfully!")
        logger.info(f"📁 Model cached in: {cache_dir.absolute()}")
        logger.info(
            "\n🎉 Your chat interface is now ready for AI-powered conversations!"
        )

        return True

    except Exception as e:
        logger.error(f"❌ Error downloading model: {e}")
        logger.info(
            "\n⚠️ Don't worry! The system will still work using an intelligent fallback."
        )
        logger.info(
            "You can try downloading the model later by running this script again."
        )
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("🤖 MedIntel - Chat Model Downloader")
    print("=" * 60)
    print()

    success = download_chat_model()

    print()
    print("=" * 60)
    if success:
        print("✅ Setup complete! You can now use the chat interface.")
    else:
        print("⚠️ Model download incomplete, but fallback system is ready.")
    print("=" * 60)
