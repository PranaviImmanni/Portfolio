"""
Logging utilities
"""
import logging
import sys
from pathlib import Path
from config import LOGGING_CONFIG

# Create logs directory if it doesn't exist
Path("logs").mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=LOGGING_CONFIG["formatters"]["standard"]["format"],
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/app.log")
    ]
)

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a module"""
    return logging.getLogger(name)

