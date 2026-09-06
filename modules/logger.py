import logging
import os
import sys
from logging.handlers import RotatingFileHandler

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = os.path.join(LOG_DIR, 'usb_audit.log')

# Force UTF-8 on the stdout stream so Windows CMD (cp1252) doesn't crash on special chars.
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

def get_logger(name="USB_Framework"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # File Handler — always UTF-8
        file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3, encoding='utf-8')
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(name)s] - %(message)s')
        file_handler.setFormatter(file_formatter)

        # Console Handler — writes to stdout (already reconfigured to UTF-8 above)
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

logger = get_logger()
