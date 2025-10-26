from telegram import Update
from telegram.ext import ContextTypes
from lib.ytlp import download_audio_from_url
from lib.ai import whisper_audio, parse_prompt, generate_receipe_json, speech_to_text
from lib.mealie import create_receipe
from lib.cleaner import clean_environment
from validators import url

import logging

logger = logging.getLogger(__name__)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.channel_post.text.strip()
    
    if url(text):
        logger.info(f"📫 Received URL: {text}")
        logger.info(f"🧲 Starting processing")

        try:
            app_data = context.application.bot_data
            openai_client = app_data.get("openai_client")
            elevenlabs_client = app_data.get("elevenlabs_client")
            whisper_model = app_data.get("whisper_model")

            metadata = download_audio_from_url(text)
            audio_path = metadata.get("audio_path")

            if elevenlabs_client:
                logger.info("🎤 Using ElevenLabs for transcription")
                transcription = speech_to_text(elevenlabs_client, audio_path)
            elif whisper_model:
                logger.info("🎤 Using Whisper for transcription")
                transcription = whisper_audio(whisper_model, audio_path)
            else:
                raise RuntimeError("No transcription client configured")

            if openai_client is None:
                raise RuntimeError("OpenAI client is not configured")

            metadata['transcription'] = transcription
            prompt = parse_prompt(metadata)
            json_receipe = generate_receipe_json(openai_client, prompt)
            create_receipe(json_receipe)
            clean_environment(metadata.get("audio_path"))
            await update.channel_post.reply_text(f"🥳 Receipe uploaded to Mealie!")
        except Exception as e:
            logger.error(f"❌ Process error: {e}")

    else:
        logger.error(f"Not a URL")
        await update.channel_post.reply_text(f"❌ The message is not a valid URL")
