import logging

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = logging.INFO

root_logger = logging.getLogger()
if root_logger.handlers:
    root_logger.handlers.clear()
    
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(LOG_FORMAT))
root_logger.addHandler(handler)
root_logger.setLevel(LOG_LEVEL)

logger = logging.getLogger("Mealie-RecAIper")

logging.getLogger("httpx").setLevel(logging.WARNING)