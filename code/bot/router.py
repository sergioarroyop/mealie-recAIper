from telegram.ext import MessageHandler, filters
from .handlers.message_handler import handle_message

def setup_handlers(app):
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))