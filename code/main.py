import whisper
from elevenlabs import ElevenLabs
from openai import OpenAI
from telegram import Update
from telegram.ext import Application
from lib.logger import logger as base_logger

logger = base_logger.getChild(__name__)

from config.settings import (
    BOT_TOKEN,
    ELEVENLABS_TOKEN,
    OPENAI_TOKEN,
    WHISPER_CONFIG,
)
from bot.router import setup_handlers

def main():
    logger.info("Starting...")
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not configured")
    if not OPENAI_TOKEN:
        raise RuntimeError("OPENAI_TOKEN is not configured")

    app = Application.builder().token(BOT_TOKEN).build()

    logger.info("Initializing OpenAI client")
    openai_client = OpenAI(api_key=OPENAI_TOKEN)

    elevenlabs_client = None
    whisper_model = None

    if ELEVENLABS_TOKEN:
        logger.info("Initializing ElevenLabs client")
        elevenlabs_client = ElevenLabs(
            base_url="https://api.elevenlabs.io",
            api_key=ELEVENLABS_TOKEN,
        )
    else:
        model_name = WHISPER_CONFIG.get("model", "medium")
        logger.info("Loading Whisper model: %s", model_name)
        whisper_model = whisper.load_model(model_name)

    app.bot_data["openai_client"] = openai_client
    app.bot_data["elevenlabs_client"] = elevenlabs_client
    app.bot_data["whisper_model"] = whisper_model

    setup_handlers(app)
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
