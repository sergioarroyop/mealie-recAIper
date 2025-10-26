import logging
from telegram import Update
from telegram.ext import Application

from config.settings import BOT_TOKEN
from bot.router import setup_handlers

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger("Mealie-Reciper")

def main():
    logger.info("Starting...")
    app = Application.builder().token(BOT_TOKEN).build()
    setup_handlers(app)
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()