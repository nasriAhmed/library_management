import os
import logging
from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


def setup_logger():
    """
    Configure le logger pour écrire les logs dans un fichier tournant.
    """
    logger = logging.getLogger("library_management")
    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler(LOG_FILE, maxBytes=100000, backupCount=3)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    logger.addHandler(handler)
    return logger


logger = setup_logger()
logger.info("Logger initialisé")  # pragma: no cover
