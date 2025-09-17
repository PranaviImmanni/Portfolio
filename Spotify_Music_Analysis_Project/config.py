"""
Configuration settings for the Spotify Music Analysis Project.

This module contains all configuration settings, database schemas,
and project constants.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
DATABASE_TYPE = os.getenv('DATABASE_TYPE', 'sqlite')
SQLITE_DB_PATH = os.getenv('SQLITE_DB_PATH', 'data/processed/spotify_analysis.db')

# Data Collection Settings
MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
BATCH_SIZE = int(os.getenv('BATCH_SIZE', '50'))
RATE_LIMIT_DELAY = float(os.getenv('RATE_LIMIT_DELAY', '0.1'))

# File Paths
BASE_DIR = Path(__file__).parent
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

# Audio Features Configuration
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

# Genre Categories for Analysis
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

# Analysis Parameters
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

# Database Schema
DATABASE_SCHEMA = """
-- Artists table
CREATE TABLE IF NOT EXISTS artists (
    artist_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    popularity INTEGER,
    followers INTEGER,
    genres TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Albums table
CREATE TABLE IF NOT EXISTS albums (
    album_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    artist_id TEXT,
    release_date DATE,
    total_tracks INTEGER,
    album_type TEXT,
    popularity INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (artist_id) REFERENCES artists (artist_id)
);

-- Tracks table
CREATE TABLE IF NOT EXISTS tracks (
    track_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    artist_id TEXT,
    album_id TEXT,
    duration_ms INTEGER,
    explicit BOOLEAN,
    popularity INTEGER,
    danceability REAL,
    energy REAL,
    key INTEGER,
    loudness REAL,
    mode INTEGER,
    speechiness REAL,
    acousticness REAL,
    instrumentalness REAL,
    liveness REAL,
    valence REAL,
    tempo REAL,
    time_signature INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (artist_id) REFERENCES artists (artist_id),
    FOREIGN KEY (album_id) REFERENCES albums (album_id)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_tracks_artist_id ON tracks(artist_id);
CREATE INDEX IF NOT EXISTS idx_tracks_album_id ON tracks(album_id);
CREATE INDEX IF NOT EXISTS idx_tracks_popularity ON tracks(popularity);
CREATE INDEX IF NOT EXISTS idx_albums_artist_id ON albums(artist_id);
"""

def create_directories():
    """Create necessary directories if they don't exist."""
    directories = [
        DATA_DIR,
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        SAMPLE_DATA_DIR,
        REPORTS_DIR,
        FIGURES_DIR,
        INSIGHTS_DIR
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

def validate_spotify_credentials():
    """Validate that Spotify API credentials are configured."""
    return bool(SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET)

def get_database_url():
    """Get the appropriate database URL based on configuration."""
    if DATABASE_TYPE == 'sqlite':
        return f"sqlite:///{SQLITE_DB_PATH}"
    else:
        raise ValueError(f"Unsupported database type: {DATABASE_TYPE}")
