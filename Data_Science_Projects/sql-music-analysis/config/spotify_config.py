"""
Spotify API Configuration Module

This module contains configuration settings for the Spotify Web API integration,
including authentication credentials, API endpoints, and rate limiting parameters.

Author: Data Analysis Team
Date: 2024
License: MIT
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# =====================================================
# SPOTIFY API CREDENTIALS
# =====================================================

# Spotify Developer Application Credentials
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

# OAuth Configuration
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI', 'http://localhost:8888/callback')
SPOTIFY_SCOPE = os.getenv('SPOTIFY_SCOPE', 'user-read-recently-played user-top-read playlist-read-private')

# Cache Configuration
SPOTIFY_CACHE_PATH = os.getenv('SPOTIFY_CACHE_PATH', '.spotify_cache')

# =====================================================
# API ENDPOINTS AND LIMITS
# =====================================================

# Base API URLs
SPOTIFY_API_BASE = 'https://api.spotify.com/v1'
SPOTIFY_ACCOUNTS_BASE = 'https://accounts.spotify.com'

# Rate Limiting
SPOTIFY_RATE_LIMIT_DELAY = float(os.getenv('SPOTIFY_RATE_LIMIT_DELAY', '0.1'))  # seconds
SPOTIFY_MAX_RETRIES = int(os.getenv('SPOTIFY_MAX_RETRIES', '3'))
SPOTIFY_BATCH_SIZE = int(os.getenv('SPOTIFY_BATCH_SIZE', '50'))

# API Endpoints
SPOTIFY_ENDPOINTS = {
    'user_profile': '/me',
    'top_tracks': '/me/top/tracks',
    'recently_played': '/me/player/recently-played',
    'playlists': '/me/playlists',
    'playlist_tracks': '/playlists/{playlist_id}/tracks',
    'artist': '/artists/{artist_id}',
    'artist_albums': '/artists/{artist_id}/albums',
    'album_tracks': '/albums/{album_id}/tracks',
    'audio_features': '/audio-features',
    'track': '/tracks/{track_id}',
    'search': '/search'
}

# =====================================================
# DATA COLLECTION PARAMETERS
# =====================================================

# Time ranges for analysis
TIME_RANGES = {
    'short_term': '4 weeks',
    'medium_term': '6 months', 
    'long_term': 'calculated from several years'
}

# Default collection limits
DEFAULT_LIMITS = {
    'top_tracks': 50,
    'recently_played': 50,
    'playlist_tracks': 100,
    'artist_albums': 50,
    'search_results': 20
}

# =====================================================
# AUDIO FEATURE MAPPINGS
# =====================================================

# Audio feature descriptions and ranges
AUDIO_FEATURES = {
    'danceability': {
        'description': 'How suitable a track is for dancing',
        'range': (0.0, 1.0),
        'interpretation': {
            'low': 'Not danceable',
            'medium': 'Somewhat danceable', 
            'high': 'Very danceable'
        }
    },
    'energy': {
        'description': 'Perceptual measure of intensity and activity',
        'range': (0.0, 1.0),
        'interpretation': {
            'low': 'Low energy, calm',
            'medium': 'Moderate energy',
            'high': 'High energy, aggressive'
        }
    },
    'valence': {
        'description': 'Musical positiveness conveyed by a track',
        'range': (0.0, 1.0),
        'interpretation': {
            'low': 'Negative, sad, angry',
            'medium': 'Neutral',
            'high': 'Positive, happy, cheerful'
        }
    },
    'acousticness': {
        'description': 'Confidence measure of whether the track is acoustic',
        'range': (0.0, 1.0),
        'interpretation': {
            'low': 'Electronic, synthesized',
            'medium': 'Mixed acoustic/electronic',
            'high': 'Acoustic instruments'
        }
    },
    'instrumentalness': {
        'description': 'Predicts whether a track contains no vocals',
        'range': (0.0, 1.0),
        'interpretation': {
            'low': 'Contains vocals',
            'medium': 'Mixed instrumental/vocal',
            'high': 'No vocals, instrumental'
        }
    },
    'liveness': {
        'description': 'Detects presence of audience in recording',
        'range': (0.0, 1.0),
        'interpretation': {
            'low': 'Studio recording',
            'medium': 'Mixed live/studio',
            'high': 'Live performance'
        }
    },
    'speechiness': {
        'description': 'Detects presence of spoken words',
        'range': (0.0, 1.0),
        'interpretation': {
            'low': 'Musical content',
            'medium': 'Mixed speech/music',
            'high': 'Spoken word'
        }
    },
    'tempo': {
        'description': 'Overall estimated tempo in BPM',
        'range': (0.0, 300.0),
        'interpretation': {
            'low': 'Slow, relaxed',
            'medium': 'Moderate pace',
            'high': 'Fast, energetic'
        }
    }
}

# Musical key mapping
MUSICAL_KEYS = {
    -1: 'No key detected',
    0: 'C',
    1: 'C♯/D♭',
    2: 'D',
    3: 'D♯/E♭',
    4: 'E',
    5: 'F',
    6: 'F♯/G♭',
    7: 'G',
    8: 'G♯/A♭',
    9: 'A',
    10: 'A♯/B♭',
    11: 'B'
}

# Musical mode mapping
MUSICAL_MODES = {
    0: 'Minor',
    1: 'Major'
}

# =====================================================
# ERROR HANDLING AND LOGGING
# =====================================================

# Logging configuration
LOGGING_CONFIG = {
    'level': os.getenv('LOG_LEVEL', 'INFO'),
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'spotify_data_collection.log',
    'max_size': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5
}

# Error messages
ERROR_MESSAGES = {
    'authentication_failed': 'Failed to authenticate with Spotify API',
    'rate_limit_exceeded': 'Rate limit exceeded, please wait before retrying',
    'invalid_credentials': 'Invalid Spotify API credentials',
    'network_error': 'Network error occurred while connecting to Spotify API',
    'data_parsing_error': 'Error parsing response data from Spotify API'
}

# =====================================================
# VALIDATION AND SANITIZATION
# =====================================================

# Input validation rules
VALIDATION_RULES = {
    'playlist_id': r'^[0-9a-zA-Z]{22}$',
    'artist_id': r'^[0-9a-zA-Z]{22}$',
    'track_id': r'^[0-9a-zA-Z]{22}$',
    'album_id': r'^[0-9a-zA-Z]{22}$',
    'user_id': r'^[0-9a-zA-Z]{22}$'
}

# Data sanitization
SANITIZATION_RULES = {
    'max_string_length': 255,
    'max_description_length': 1000,
    'allowed_special_chars': r'[a-zA-Z0-9\s\-_.,!?()&\'"]'
}

# =====================================================
# PERFORMANCE AND CACHING
# =====================================================

# Caching configuration
CACHE_CONFIG = {
    'enabled': os.getenv('CACHE_ENABLED', 'true').lower() == 'true',
    'ttl': int(os.getenv('CACHE_TTL', '3600')),  # 1 hour
    'max_size': int(os.getenv('CACHE_MAX_SIZE', '1000')),
    'cleanup_interval': int(os.getenv('CACHE_CLEANUP_INTERVAL', '300'))  # 5 minutes
}

# Performance thresholds
PERFORMANCE_THRESHOLDS = {
    'max_response_time': float(os.getenv('MAX_RESPONSE_TIME', '5.0')),  # seconds
    'max_concurrent_requests': int(os.getenv('MAX_CONCURRENT_REQUESTS', '10')),
    'request_timeout': float(os.getenv('REQUEST_TIMEOUT', '30.0'))  # seconds
}

# =====================================================
# CONFIGURATION VALIDATION
# =====================================================

def validate_config() -> Dict[str, Any]:
    """
    Validate the configuration and return any issues found.
    
    Returns:
        Dictionary containing validation results and any errors
    """
    errors = []
    warnings = []
    
    # Check required credentials
    if not SPOTIFY_CLIENT_ID:
        errors.append("SPOTIFY_CLIENT_ID is required but not set")
    if not SPOTIFY_CLIENT_SECRET:
        errors.append("SPOTIFY_CLIENT_SECRET is required but not set")
    
    # Check rate limiting
    if SPOTIFY_RATE_LIMIT_DELAY < 0.05:
        warnings.append("SPOTIFY_RATE_LIMIT_DELAY is very low, may cause rate limiting issues")
    
    # Check batch sizes
    if SPOTIFY_BATCH_SIZE > 100:
        warnings.append("SPOTIFY_BATCH_SIZE exceeds recommended maximum of 100")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings
    }

def get_config_summary() -> Dict[str, Any]:
    """
    Get a summary of the current configuration.
    
    Returns:
        Dictionary containing configuration summary
    """
    return {
        'client_id_set': bool(SPOTIFY_CLIENT_ID),
        'client_secret_set': bool(SPOTIFY_CLIENT_SECRET),
        'redirect_uri': SPOTIFY_REDIRECT_URI,
        'scope': SPOTIFY_SCOPE,
        'rate_limit_delay': SPOTIFY_RATE_LIMIT_DELAY,
        'max_retries': SPOTIFY_MAX_RETRIES,
        'batch_size': SPOTIFY_BATCH_SIZE,
        'cache_enabled': CACHE_CONFIG['enabled'],
        'validation': validate_config()
    }

# =====================================================
# ENVIRONMENT-SPECIFIC OVERRIDES
# =====================================================

# Development overrides
if os.getenv('ENVIRONMENT') == 'development':
    SPOTIFY_RATE_LIMIT_DELAY = 0.2  # Slower for development
    LOGGING_CONFIG['level'] = 'DEBUG'
    CACHE_CONFIG['enabled'] = False

# Production overrides  
if os.getenv('ENVIRONMENT') == 'production':
    SPOTIFY_RATE_LIMIT_DELAY = 0.05  # Faster for production
    LOGGING_CONFIG['level'] = 'WARNING'
    CACHE_CONFIG['enabled'] = True

# Test overrides
if os.getenv('ENVIRONMENT') == 'test':
    SPOTIFY_RATE_LIMIT_DELAY = 0.0  # No delay for testing
    LOGGING_CONFIG['level'] = 'ERROR'
    CACHE_CONFIG['enabled'] = False

# =====================================================
# MAIN EXECUTION
# =====================================================

if __name__ == "__main__":
    # Print configuration summary
    summary = get_config_summary()
    print("Spotify API Configuration Summary:")
    print(f"Valid: {summary['valid']}")
    print(f"Client ID Set: {summary['client_id_set']}")
    print(f"Client Secret Set: {summary['client_secret_set']}")
    print(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    
    if summary['validation']['errors']:
        print("\nConfiguration Errors:")
        for error in summary['validation']['errors']:
            print(f"  - {error}")
    
    if summary['validation']['warnings']:
        print("\nConfiguration Warnings:")
        for warning in summary['validation']['warnings']:
            print(f"  - {warning}")

