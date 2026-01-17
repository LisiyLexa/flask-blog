import logging
from logging.handlers import RotatingFileHandler
import os
import sys

LOG_FILE: str = "app.log"
DISABLE_LOGS: bool = "--log" in sys.argv


def setup_logger(name: str = __name__) -> logging.Logger:
    """Configure and return a standalone logger."""

    # Make sure logs folder exists
    log_dir = os.path.dirname(LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create logger
    logger = logging.getLogger(name)
    if DISABLE_LOGS:
        logger.setLevel(logging.CRITICAL)
    else:
        logger.setLevel(logging.INFO)

    # To file
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=3)
    file_handler.setLevel(logging.INFO)

    # To console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Common formatter
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Attach handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.propagate = False

    return logger
