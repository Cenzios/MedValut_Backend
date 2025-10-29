import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# File logger with rotation
file_handler = RotatingFileHandler(
    filename=os.path.join(LOG_DIR, "app.log"),
    maxBytes=5*1024*1024,  # 5 MB
    backupCount=5,
)
formatter = logging.Formatter(
    '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
)
file_handler.setFormatter(formatter)

logger = logging.getLogger("medvault_logger")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.propagate = False

def log_info(message: str):
    logger.info(message)

def log_error(message: str):
    logger.error(message)