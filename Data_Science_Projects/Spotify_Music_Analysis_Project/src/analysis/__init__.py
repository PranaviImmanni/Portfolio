"""
Analysis module for the Spotify Music Analysis Project.

This module provides analysis functionality including
music analysis, SQL queries, and insights generation.
"""

from .music_analyzer import MusicAnalyzer
from .sql_queries import SQLQueries

__all__ = ['MusicAnalyzer', 'SQLQueries']
