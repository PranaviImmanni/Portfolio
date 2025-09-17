"""
Utility module for the Spotify Music Analysis Project.

This module provides utility functions including
helper functions and logging configuration.
"""

from .logger import setup_logger
from .helpers import *

__all__ = ['setup_logger']
