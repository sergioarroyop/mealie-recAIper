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
            metadata = download_audio_from_url(text)
            transcription = speech_to_text(metadata.get("audio_path"))
            metadata['transcription'] = transcription
            prompt = parse_prompt(metadata)
            json_receipe = generate_receipe_json(prompt)
            create_receipe(json_receipe)
            clean_environment(metadata.get("audio_path"))
            await update.channel_post.reply_text(f"🥳 Receta subida a Mealie!")
        except Exception as e:
            logger.error(f"❌ Process error: {e}")

    else:
        logger.error(f"Not a URL")
        await update.channel_post.reply_text(f"Maldita sea solo funciono con enlaces")