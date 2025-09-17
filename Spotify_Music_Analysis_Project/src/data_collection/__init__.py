"""
Data collection module for the Spotify Music Analysis Project.

This module provides data collection functionality including
Spotify API integration and sample data generation.
"""

from .spotify_api import SpotifyDataCollector
from .sample_data_generator import SampleDataGenerator

__all__ = ['SpotifyDataCollector', 'SampleDataGenerator']
