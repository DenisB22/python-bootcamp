import logging
import time

from logging.handlers import RotatingFileHandler


def create_rotating_log(path):

    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler(path, maxBytes=2400, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


log_file = "web-scraping.log"
logger = create_rotating_log(log_file)