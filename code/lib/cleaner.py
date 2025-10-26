import logging
from os import remove

logger = logging.getLogger(__name__)

def clean_environment(audio_file: str):
    try:
        logger.info("🗑️ Cleaning files")
        remove(audio_file)
    except Exception as e:
        logger.error(f"❌ There was an error cleaning files: {e}")
        raise