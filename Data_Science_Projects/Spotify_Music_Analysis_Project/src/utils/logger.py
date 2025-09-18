"""
Logging configuration for the Spotify Music Analysis Project.
"""

import logging
import sys
from pathlib import Path

def setup_logger(name: str, level: str = 'INFO') -> logging.Logger:
    """
    Set up logger with consistent formatting.
    
    Args:
        name: Logger name
        level: Logging level
        
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Avoid adding multiple handlers
    if logger.handlers:
        return logger
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    file_handler = logging.FileHandler(log_dir / 'spotify_analysis.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger
