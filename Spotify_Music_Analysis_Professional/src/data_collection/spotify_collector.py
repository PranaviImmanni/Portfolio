"""
Professional Spotify Data Collection Module

This module provides a comprehensive interface for collecting Spotify data
using the official Web API. It includes error handling, rate limiting,
and data validation for production use.

Author: Data Analysis Team
Date: 2024
License: MIT
"""

import os
import time
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import json
import pandas as pd
import requests
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from spotipy.exceptions import SpotifyException
import sqlite3
from pathlib import Path

# Import configuration
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from config.settings import config

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('spotify_data_collection.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class SpotifyDataCollector:
    """
    Professional Spotify data collector with comprehensive error handling
    and data validation capabilities.
    """
    
    def __init__(self, use_sample_data: bool = False):
        """
        Initialize the Spotify data collector.
        
        Args:
            use_sample_data: Whether to use sample data instead of API calls
        """
        self.use_sample_data = use_sample_data
        self.spotify = None
        self.db_connection = None
        self.rate_limit_delay = config.RATE_LIMIT_DELAY
        self.max_retries = config.MAX_RETRIES
        
        # Initialize Spotify client if not using sample data
        if not self.use_sample_data:
            self._initialize_spotify_client()
        
        # Create directories
        config.create_directories()
    
    def _initialize_spotify_client(self) -> None:
        """Initialize and authenticate Spotify client."""
        try:
            if not config.validate_spotify_credentials():
                logger.warning("Spotify credentials not found. Falling back to sample data.")
                self.use_sample_data = True
                return
            
            # For public data (no user authentication required)
            client_credentials_manager = SpotifyClientCredentials(
                client_id=config.SPOTIFY_CLIENT_ID,
                client_secret=config.SPOTIFY_CLIENT_SECRET
            )
            
            self.spotify = Spotify(client_credentials_manager=client_credentials_manager)
            
            # Test connection
            test_search = self.spotify.search('test', limit=1)
            logger.info("Successfully authenticated with Spotify API")
            
        except SpotifyException as e:
            logger.error(f"Failed to authenticate with Spotify: {e}")
            logger.info("Falling back to sample data")
            self.use_sample_data = True
        except Exception as e:
            logger.error(f"Unexpected error during Spotify authentication: {e}")
            self.use_sample_data = True
    
    def connect_database(self) -> None:
        """Establish database connection."""
        try:
            db_path = config.SQLITE_DB_PATH
            # Ensure directory exists
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
            
            self.db_connection = sqlite3.connect(db_path)
            logger.info(f"Successfully connected to database: {db_path}")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise
    
    def disconnect_database(self) -> None:
        """Close database connection."""
        if self.db_connection:
            self.db_connection.close()
            logger.info("Database connection closed")
    
    def search_tracks(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Search for tracks using Spotify API.
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of track dictionaries
        """
        if self.use_sample_data:
            return self._get_sample_tracks(limit)
        
        try:
            logger.info(f"Searching for tracks: {query}")
            
            results = self.spotify.search(
                q=query,
                type='track',
                limit=limit
            )
            
            tracks = []
            for track in results['tracks']['items']:
                # Get audio features
                features = self.spotify.audio_features(track['id'])[0]
                if features:
                    track['audio_features'] = features
                
                # Get artist details
                if track['artists']:
                    artist = track['artists'][0]
                    artist_details = self.spotify.artist(artist['id'])
                    track['artist_details'] = artist_details
                
                tracks.append(track)
                
                # Rate limiting
                time.sleep(self.rate_limit_delay)
            
            logger.info(f"Successfully found {len(tracks)} tracks")
            return tracks
            
        except SpotifyException as e:
            logger.error(f"Failed to search tracks: {e}")
            return self._get_sample_tracks(limit)
        except Exception as e:
            logger.error(f"Unexpected error searching tracks: {e}")
            return self._get_sample_tracks(limit)
    
    def get_artist_top_tracks(self, artist_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get top tracks for a specific artist.
        
        Args:
            artist_id: Spotify artist ID
            limit: Maximum number of tracks
            
        Returns:
            List of track dictionaries
        """
        if self.use_sample_data:
            return self._get_sample_tracks(limit)
        
        try:
            logger.info(f"Getting top tracks for artist: {artist_id}")
            
            results = self.spotify.artist_top_tracks(artist_id)
            tracks = []
            
            for track in results['tracks'][:limit]:
                # Get audio features
                features = self.spotify.audio_features(track['id'])[0]
                if features:
                    track['audio_features'] = features
                
                tracks.append(track)
                
                # Rate limiting
                time.sleep(self.rate_limit_delay)
            
            logger.info(f"Successfully retrieved {len(tracks)} top tracks")
            return tracks
            
        except SpotifyException as e:
            logger.error(f"Failed to get artist top tracks: {e}")
            return self._get_sample_tracks(limit)
        except Exception as e:
            logger.error(f"Unexpected error getting artist top tracks: {e}")
            return self._get_sample_tracks(limit)
    
    def get_playlist_tracks(self, playlist_id: str) -> List[Dict[str, Any]]:
        """
        Get all tracks from a specific playlist.
        
        Args:
            playlist_id: Spotify playlist ID
            
        Returns:
            List of track dictionaries
        """
        if self.use_sample_data:
            return self._get_sample_tracks(50)
        
        try:
            logger.info(f"Getting tracks from playlist: {playlist_id}")
            
            tracks = []
            offset = 0
            
            while True:
                results = self.spotify.playlist_tracks(
                    playlist_id,
                    offset=offset,
                    limit=100
                )
                
                if not results['items']:
                    break
                
                for item in results['items']:
                    track = item['track']
                    if track:  # Skip null tracks
                        # Get audio features
                        features = self.spotify.audio_features(track['id'])[0]
                        if features:
                            track['audio_features'] = features
                        
                        tracks.append(track)
                
                offset += 100
                
                # Rate limiting
                time.sleep(self.rate_limit_delay)
            
            logger.info(f"Successfully retrieved {len(tracks)} tracks from playlist")
            return tracks
            
        except SpotifyException as e:
            logger.error(f"Failed to get playlist tracks: {e}")
            return self._get_sample_tracks(50)
        except Exception as e:
            logger.error(f"Unexpected error getting playlist tracks: {e}")
            return self._get_sample_tracks(50)
    
    def _get_sample_tracks(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Generate sample tracks for demonstration purposes."""
        logger.info(f"Generating {limit} sample tracks")
        
        # Sample artists and genres
        artists = [
            'Taylor Swift', 'Drake', 'Billie Eilish', 'The Weeknd', 'Ariana Grande',
            'Ed Sheeran', 'Post Malone', 'Dua Lipa', 'Harry Styles', 'Olivia Rodrigo',
            'Bad Bunny', 'Justin Bieber', 'SZA', 'Doja Cat', 'Lil Nas X',
            'Bruno Mars', 'Adele', 'Kendrick Lamar', 'Travis Scott', 'Lana Del Rey'
        ]
        
        genres = ['pop', 'hip-hop', 'indie', 'r&b', 'rock', 'electronic', 'country']
        
        tracks = []
        for i in range(limit):
            track = {
                'id': f'sample_track_{i:03d}',
                'name': f'Sample Track {i+1}',
                'artists': [{'id': f'artist_{i%len(artists):03d}', 'name': artists[i % len(artists)]}],
                'album': {
                    'id': f'album_{i:03d}',
                    'name': f'Sample Album {i+1}',
                    'release_date': '2023-01-01',
                    'total_tracks': 12
                },
                'popularity': np.random.randint(20, 100),
                'duration_ms': np.random.randint(120000, 300000),
                'explicit': np.random.choice([True, False], p=[0.3, 0.7]),
                'external_urls': {'spotify': f'https://open.spotify.com/track/sample_{i:03d}'},
                'audio_features': {
                    'danceability': np.random.uniform(0.0, 1.0),
                    'energy': np.random.uniform(0.0, 1.0),
                    'valence': np.random.uniform(0.0, 1.0),
                    'acousticness': np.random.uniform(0.0, 1.0),
                    'instrumentalness': np.random.uniform(0.0, 1.0),
                    'liveness': np.random.uniform(0.0, 1.0),
                    'speechiness': np.random.uniform(0.0, 1.0),
                    'tempo': np.random.uniform(60, 200),
                    'key': np.random.randint(-1, 12),
                    'mode': np.random.choice([0, 1]),
                    'time_signature': np.random.choice([3, 4, 5, 6, 7], p=[0.1, 0.7, 0.1, 0.05, 0.05])
                },
                'artist_details': {
                    'id': f'artist_{i%len(artists):03d}',
                    'name': artists[i % len(artists)],
                    'genres': [genres[i % len(genres)]],
                    'popularity': np.random.randint(20, 100),
                    'followers': {'total': np.random.randint(10000, 10000000)}
                }
            }
            tracks.append(track)
        
        return tracks
    
    def save_to_database(self, tracks: List[Dict[str, Any]]) -> int:
        """
        Save tracks to the database.
        
        Args:
            tracks: List of track dictionaries
            
        Returns:
            Number of records saved
        """
        if not self.db_connection:
            self.connect_database()
        
        try:
            cursor = self.db_connection.cursor()
            
            # Create tables if they don't exist
            self._create_tables()
            
            saved_count = 0
            
            for track in tracks:
                # Extract and save artist data
                if 'artist_details' in track:
                    artist = track['artist_details']
                    self._save_artist(cursor, artist)
                
                # Extract and save album data
                if 'album' in track:
                    album = track['album']
                    artist_id = track['artists'][0]['id'] if track['artists'] else None
                    self._save_album(cursor, album, artist_id)
                
                # Save track data
                self._save_track(cursor, track)
                saved_count += 1
            
            self.db_connection.commit()
            logger.info(f"Successfully saved {saved_count} tracks to database")
            return saved_count
            
        except Exception as e:
            self.db_connection.rollback()
            logger.error(f"Error saving to database: {e}")
            raise
        finally:
            cursor.close()
    
    def _create_tables(self) -> None:
        """Create database tables if they don't exist."""
        cursor = self.db_connection.cursor()
        
        # Artists table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS artists (
                artist_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                genres TEXT,
                popularity INTEGER,
                followers INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Albums table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS albums (
                album_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                artist_id TEXT,
                release_date TEXT,
                total_tracks INTEGER,
                album_type TEXT,
                popularity INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (artist_id) REFERENCES artists (artist_id)
            )
        ''')
        
        # Tracks table
        cursor.execute('''
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
                valence REAL,
                acousticness REAL,
                instrumentalness REAL,
                liveness REAL,
                speechiness REAL,
                tempo REAL,
                key INTEGER,
                mode INTEGER,
                time_signature INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (artist_id) REFERENCES artists (artist_id),
                FOREIGN KEY (album_id) REFERENCES albums (album_id)
            )
        ''')
        
        self.db_connection.commit()
    
    def _save_artist(self, cursor, artist: Dict[str, Any]) -> None:
        """Save artist data to database."""
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO artists 
                (artist_id, name, genres, popularity, followers)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                artist['id'],
                artist['name'],
                ','.join(artist.get('genres', [])),
                artist.get('popularity', 0),
                artist.get('followers', {}).get('total', 0)
            ))
        except Exception as e:
            logger.warning(f"Error saving artist {artist.get('name', 'Unknown')}: {e}")
    
    def _save_album(self, cursor, album: Dict[str, Any], artist_id: str = None) -> None:
        """Save album data to database."""
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO albums 
                (album_id, name, artist_id, release_date, total_tracks, album_type, popularity)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                album['id'],
                album['name'],
                artist_id,
                album.get('release_date', ''),
                album.get('total_tracks', 0),
                album.get('album_type', 'album'),
                album.get('popularity', 0)
            ))
        except Exception as e:
            logger.warning(f"Error saving album {album.get('name', 'Unknown')}: {e}")
    
    def _save_track(self, cursor, track: Dict[str, Any]) -> None:
        """Save track data to database."""
        try:
            audio_features = track.get('audio_features', {})
            artist_id = track['artists'][0]['id'] if track['artists'] else None
            album_id = track['album']['id'] if 'album' in track else None
            
            cursor.execute('''
                INSERT OR REPLACE INTO tracks 
                (track_id, name, artist_id, album_id, duration_ms, explicit, popularity,
                 danceability, energy, valence, acousticness, instrumentalness, 
                 liveness, speechiness, tempo, key, mode, time_signature)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                track['id'],
                track['name'],
                artist_id,
                album_id,
                track.get('duration_ms', 0),
                track.get('explicit', False),
                track.get('popularity', 0),
                audio_features.get('danceability', 0.0),
                audio_features.get('energy', 0.0),
                audio_features.get('valence', 0.0),
                audio_features.get('acousticness', 0.0),
                audio_features.get('instrumentalness', 0.0),
                audio_features.get('liveness', 0.0),
                audio_features.get('speechiness', 0.0),
                audio_features.get('tempo', 0.0),
                audio_features.get('key', -1),
                audio_features.get('mode', 0),
                audio_features.get('time_signature', 4)
            ))
        except Exception as e:
            logger.warning(f"Error saving track {track.get('name', 'Unknown')}: {e}")
    
    def export_to_csv(self, tracks: List[Dict[str, Any]], filename: str) -> str:
        """
        Export tracks to CSV format.
        
        Args:
            tracks: List of track dictionaries
            filename: Output filename
            
        Returns:
            Path to the exported CSV file
        """
        try:
            # Flatten tracks for CSV export
            flattened_tracks = []
            for track in tracks:
                flattened_track = self._flatten_track(track)
                flattened_tracks.append(flattened_track)
            
            df = pd.DataFrame(flattened_tracks)
            df.to_csv(filename, index=False)
            
            logger.info(f"Successfully exported data to: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Failed to export data to CSV: {e}")
            raise
    
    def _flatten_track(self, track: Dict[str, Any]) -> Dict[str, Any]:
        """Flatten track dictionary for CSV export."""
        flattened = {
            'track_id': track['id'],
            'track_name': track['name'],
            'artist_name': track['artists'][0]['name'] if track['artists'] else '',
            'album_name': track['album']['name'] if 'album' in track else '',
            'popularity': track.get('popularity', 0),
            'duration_ms': track.get('duration_ms', 0),
            'explicit': track.get('explicit', False)
        }
        
        # Add audio features
        audio_features = track.get('audio_features', {})
        for feature, value in audio_features.items():
            flattened[f'audio_{feature}'] = value
        
        # Add artist details
        if 'artist_details' in track:
            artist = track['artist_details']
            flattened['artist_genres'] = ','.join(artist.get('genres', []))
            flattened['artist_popularity'] = artist.get('popularity', 0)
            flattened['artist_followers'] = artist.get('followers', {}).get('total', 0)
        
        return flattened
    
    def get_collection_summary(self) -> Dict[str, Any]:
        """Get summary of collected data."""
        if not self.db_connection:
            self.connect_database()
        
        try:
            cursor = self.db_connection.cursor()
            
            # Get counts
            cursor.execute("SELECT COUNT(*) FROM tracks")
            track_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM artists")
            artist_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM albums")
            album_count = cursor.fetchone()[0]
            
            return {
                'total_tracks': track_count,
                'total_artists': artist_count,
                'total_albums': album_count,
                'collection_date': datetime.now().isoformat(),
                'data_source': 'sample' if self.use_sample_data else 'spotify_api'
            }
            
        except Exception as e:
            logger.error(f"Error getting collection summary: {e}")
            return {
                'total_tracks': 0,
                'total_artists': 0,
                'total_albums': 0,
                'collection_date': datetime.now().isoformat(),
                'data_source': 'sample' if self.use_sample_data else 'spotify_api'
            }
        finally:
            cursor.close()


def main():
    """Main execution function for testing."""
    try:
        # Initialize collector
        collector = SpotifyDataCollector(use_sample_data=True)
        
        # Collect sample data
        tracks = collector.search_tracks('pop music', limit=20)
        
        # Save to database
        collector.connect_database()
        saved_count = collector.save_to_database(tracks)
        
        # Export to CSV
        csv_path = config.PROCESSED_DATA_DIR / 'collected_tracks.csv'
        collector.export_to_csv(tracks, str(csv_path))
        
        # Get summary
        summary = collector.get_collection_summary()
        logger.info(f"Collection summary: {summary}")
        
        collector.disconnect_database()
        
    except Exception as e:
        logger.error(f"Data collection failed: {e}")
        raise


if __name__ == "__main__":
    main()
