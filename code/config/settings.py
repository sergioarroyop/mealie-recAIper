import os
from dotenv import load_dotenv

load_dotenv()

# TOKENS
MEALIE_TOKEN = os.getenv("MEALIE_TOKEN")
OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")
BOT_TOKEN = os.getenv("BOT_TOKEN")
ELEVENLABS_TOKEN = os.getenv("ELEVENLABS_TOKEN")

# URLs
MEALIE_API_URL = os.getenv("MEALIE_API_URL")

# CONFIGS
YLTP_CONFIG = {
    "format": "bestaudio/best",
    "download_dir": "/tmp",
    "quiet": True
}

WHISPER_CONFIG = {
    "model": os.getenv("WHISPER_MODEL", "medium")
}

EXTRA_PROMPT = os.getenv("EXTRA_PROMPT", "")