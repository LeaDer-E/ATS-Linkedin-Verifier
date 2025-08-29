# logging_config.py
import logging
import os

def setup_logger(log_file="app.log"):
    # Create logger
    logger = logging.getLogger("LinkedInChecker")
    logger.setLevel(logging.DEBUG)

    # Formatter setup
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # File handler
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)

    # Attach handlers
    if not logger.handlers:  # To avoid adding handlers multiple times
        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger
