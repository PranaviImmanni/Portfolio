"""
Professional Spotify Music Analysis - Configuration Settings

This module contains all configuration settings for the Spotify Music Analysis project.
It supports both Google Colab and local development environments.

Author: Data Analysis Team
Date: 2024
License: MIT
"""

import os
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Main configuration class for the Spotify Music Analysis project."""
    
    # Project Information
    PROJECT_NAME = "Spotify Music Analysis"
    VERSION = "1.0.0"
    DESCRIPTION = "Professional music data analysis using Spotify Web API and SQL"
    
    # Environment Settings
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Spotify API Configuration
    SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID', '')
    SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET', '')
    SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI', 'http://127.0.0.1:8888/callback')
    SPOTIFY_SCOPE = os.getenv('SPOTIFY_SCOPE', 'user-read-recently-played user-top-read playlist-read-private')
    
    # Database Configuration
    DATABASE_TYPE = os.getenv('DATABASE_TYPE', 'sqlite')  # sqlite or postgresql
    SQLITE_DB_PATH = os.getenv('SQLITE_DB_PATH', 'data/processed/spotify_analysis.db')
    POSTGRES_URL = os.getenv('DATABASE_URL', '')
    
    # Data Collection Settings
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', '50'))
    RATE_LIMIT_DELAY = float(os.getenv('RATE_LIMIT_DELAY', '0.1'))
    
    # File Paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / 'data'
    RAW_DATA_DIR = DATA_DIR / 'raw'
    PROCESSED_DATA_DIR = DATA_DIR / 'processed'
    SAMPLE_DATA_DIR = DATA_DIR / 'sample'
    REPORTS_DIR = BASE_DIR / 'reports'
    FIGURES_DIR = REPORTS_DIR / 'figures'
    INSIGHTS_DIR = REPORTS_DIR / 'insights'
    
    # Visualization Settings
    FIGURE_SIZE = (12, 8)
    DPI = 300
    STYLE = 'seaborn-v0_8'
    COLOR_PALETTE = 'husl'
    
    # Analysis Settings
    DEFAULT_TIME_RANGES = ['short_term', 'medium_term', 'long_term']
    DEFAULT_LIMIT = 50
    MIN_POPULARITY_THRESHOLD = 20
    
    # Colab Specific Settings
    IS_COLAB = 'google.colab' in str(os.getenv('_', ''))
    
    @classmethod
    def get_database_url(cls) -> str:
        """Get the appropriate database URL based on configuration."""
        if cls.DATABASE_TYPE == 'postgresql' and cls.POSTGRES_URL:
            return cls.POSTGRES_URL
        else:
            return f"sqlite:///{cls.SQLITE_DB_PATH}"
    
    @classmethod
    def validate_spotify_credentials(cls) -> bool:
        """Validate that Spotify API credentials are configured."""
        return bool(cls.SPOTIFY_CLIENT_ID and cls.SPOTIFY_CLIENT_SECRET)
    
    @classmethod
    def get_sample_data_path(cls) -> str:
        """Get the path to sample data file."""
        return str(cls.SAMPLE_DATA_DIR / 'sample_spotify_data.csv')
    
    @classmethod
    def create_directories(cls) -> None:
        """Create necessary directories if they don't exist."""
        directories = [
            cls.DATA_DIR,
            cls.RAW_DATA_DIR,
            cls.PROCESSED_DATA_DIR,
            cls.SAMPLE_DATA_DIR,
            cls.REPORTS_DIR,
            cls.FIGURES_DIR,
            cls.INSIGHTS_DIR
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

# Colab-specific configuration
class ColabConfig(Config):
    """Configuration optimized for Google Colab environment."""
    
    # Override paths for Colab
    BASE_DIR = Path('/content/spotify_analysis')
    DATA_DIR = BASE_DIR / 'data'
    RAW_DATA_DIR = DATA_DIR / 'raw'
    PROCESSED_DATA_DIR = DATA_DIR / 'processed'
    SAMPLE_DATA_DIR = DATA_DIR / 'sample'
    REPORTS_DIR = BASE_DIR / 'reports'
    FIGURES_DIR = REPORTS_DIR / 'figures'
    INSIGHTS_DIR = REPORTS_DIR / 'insights'
    
    # Colab-specific settings
    ENABLE_GPU = True
    MOUNT_DRIVE = True
    SAVE_TO_DRIVE = True

# Get the appropriate config based on environment
def get_config() -> Config:
    """Get the appropriate configuration based on the environment."""
    if Config.IS_COLAB:
        return ColabConfig()
    return Config()

# Global config instance
config = get_config()

# Database schema configuration
DATABASE_SCHEMA = {
    'artists': {
        'columns': [
            'artist_id', 'artist_name', 'genres', 'popularity', 
            'followers_count', 'market', 'spotify_uri', 'external_urls', 
            'images', 'created_at', 'updated_at'
        ],
        'primary_key': 'artist_id'
    },
    'tracks': {
        'columns': [
            'track_id', 'track_name', 'artist_id', 'album_id', 
            'disc_number', 'track_number', 'duration_ms', 'popularity',
            'danceability', 'energy', 'valence', 'acousticness',
            'instrumentalness', 'liveness', 'speechiness', 'tempo',
            'key', 'mode', 'time_signature', 'spotify_uri',
            'external_urls', 'is_explicit', 'created_at', 'updated_at'
        ],
        'primary_key': 'track_id'
    },
    'albums': {
        'columns': [
            'album_id', 'album_name', 'artist_id', 'album_type',
            'total_tracks', 'release_date', 'release_date_precision',
            'popularity', 'spotify_uri', 'external_urls', 'images',
            'created_at', 'updated_at'
        ],
        'primary_key': 'album_id'
    }
}

# Audio features configuration
AUDIO_FEATURES = {
    'danceability': {'min': 0.0, 'max': 1.0, 'description': 'How suitable a track is for dancing'},
    'energy': {'min': 0.0, 'max': 1.0, 'description': 'Perceptual measure of intensity and activity'},
    'valence': {'min': 0.0, 'max': 1.0, 'description': 'Musical positiveness conveyed by a track'},
    'acousticness': {'min': 0.0, 'max': 1.0, 'description': 'Confidence measure of whether the track is acoustic'},
    'instrumentalness': {'min': 0.0, 'max': 1.0, 'description': 'Predicts whether a track contains no vocals'},
    'liveness': {'min': 0.0, 'max': 1.0, 'description': 'Detects the presence of an audience in the recording'},
    'speechiness': {'min': 0.0, 'max': 1.0, 'description': 'Detects the presence of spoken words in a track'},
    'tempo': {'min': 0.0, 'max': 300.0, 'description': 'Overall estimated tempo of a track in BPM'},
    'key': {'min': -1, 'max': 11, 'description': 'Key the track is in (using standard Pitch Class notation)'},
    'mode': {'min': 0, 'max': 1, 'description': 'Mode (major or minor)'},
    'time_signature': {'min': 3, 'max': 7, 'description': 'Estimated overall time signature of a track'}
}

# Genre categories for analysis
GENRE_CATEGORIES = {
    'pop': ['pop', 'dance pop', 'indie pop', 'pop rock'],
    'rock': ['rock', 'alternative rock', 'indie rock', 'pop rock', 'classic rock'],
    'hip_hop': ['hip hop', 'rap', 'trap', 'gangsta rap'],
    'electronic': ['electronic', 'edm', 'house', 'techno', 'trance'],
    'r&b': ['r&b', 'soul', 'neo soul', 'contemporary r&b'],
    'country': ['country', 'country pop', 'folk', 'bluegrass'],
    'jazz': ['jazz', 'bebop', 'swing', 'blues'],
    'classical': ['classical', 'orchestral', 'chamber music'],
    'reggae': ['reggae', 'dancehall', 'ska'],
    'blues': ['blues', 'rhythm and blues', 'delta blues']
}

# Analysis parameters
ANALYSIS_CONFIG = {
    'clustering': {
        'n_clusters': 5,
        'random_state': 42,
        'features': ['danceability', 'energy', 'valence', 'acousticness']
    },
    'correlation_threshold': 0.7,
    'outlier_threshold': 3.0,
    'min_tracks_per_artist': 3,
    'min_artists_per_genre': 2
}
