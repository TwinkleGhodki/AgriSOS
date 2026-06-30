import logging
from logging.handlers import RotatingFileHandler

from agrisos.config.settings import LOG_DIR, LOG_FILE


def configure_logging():
    LOG_DIR.mkdir(exist_ok=True)

    logger = logging.getLogger("agrisos")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.propagate = False
    return logger


def get_logger(name):
    configure_logging()
    return logging.getLogger(f"agrisos.{name}")
