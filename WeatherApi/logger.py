# /opt/myapp/logger_setup.py
import logging
import sys
from logging.handlers import RotatingFileHandler
import pathlib

LOG_PATH = "/var/log/myapp/job.log"
pathlib.Path(LOG_PATH).parent.mkdir(parents=True, exist_ok=True)

def get_logger(name="myapp"):
    logger = logging.getLogger(name)

    if logger.handlers:  # avoid adding handlers twice
        return logger

    logger.setLevel(logging.INFO)

    # Console handler (for cron capture)
    console = logging.StreamHandler(sys.stdout)

    # File handler (persistent log)
    file_handler = RotatingFileHandler(LOG_PATH, maxBytes=5_000_000, backupCount=5)

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s [%(name)s] %(message)s"
    )
    console.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console)
    logger.addHandler(file_handler)

    return logger
