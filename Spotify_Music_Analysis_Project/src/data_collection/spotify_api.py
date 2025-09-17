"""
Spotify API Data Collector for the Spotify Music Analysis Project.

This module handles real-time data collection from the Spotify Web API
with proper error handling and rate limiting.
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time
from typing import List, Dict, Any, Optional
import logging

from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, RATE_LIMIT_DELAY, MAX_RETRIES

logger = logging.getLogger(__name__)

class SpotifyDataCollector:
    """
    Collects data from the Spotify Web API with proper error handling.
    """
    
    def __init__(self):
        """Initialize the Spotify data collector."""
        self.spotify = None
        self.rate_limit_delay = RATE_LIMIT_DELAY
        self.max_retries = MAX_RETRIES
        
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Spotify client."""
        try:
            if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
                raise ValueError("Spotify API credentials not configured")
            
            client_credentials_manager = SpotifyClientCredentials(
                client_id=SPOTIFY_CLIENT_ID,
                client_secret=SPOTIFY_CLIENT_SECRET
            )
            
            self.spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
            
            # Test connection
            test_search = self.spotify.search('test', limit=1)
            logger.info("Spotify client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Spotify client: {e}")
            raise
    
    def search_tracks(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Search for tracks using Spotify API.
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of track dictionaries
        """
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
            
        except Exception as e:
            logger.error(f"Failed to search tracks: {e}")
            raise
    
    def get_artist_top_tracks(self, artist_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get top tracks for a specific artist.
        
        Args:
            artist_id: Spotify artist ID
            limit: Maximum number of tracks
            
        Returns:
            List of track dictionaries
        """
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
            
        except Exception as e:
            logger.error(f"Failed to get artist top tracks: {e}")
            raise
    
    def get_playlist_tracks(self, playlist_id: str) -> List[Dict[str, Any]]:
        """
        Get all tracks from a specific playlist.
        
        Args:
            playlist_id: Spotify playlist ID
            
        Returns:
            List of track dictionaries
        """
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
            
        except Exception as e:
            logger.error(f"Failed to get playlist tracks: {e}")
            raise
    
    def save_to_database(self, tracks: List[Dict[str, Any]]):
        """
        Save tracks to database.
        
        Args:
            tracks: List of track dictionaries
        """
        from src.database.database_manager import DatabaseManager
        
        try:
            # Convert tracks to DataFrames
            artists_data = []
            albums_data = []
            tracks_data = []
            
            for track in tracks:
                # Extract artist data
                if 'artist_details' in track:
                    artist = track['artist_details']
                    artists_data.append({
                        'artist_id': artist['id'],
                        'name': artist['name'],
                        'popularity': artist.get('popularity', 0),
                        'followers': artist.get('followers', {}).get('total', 0),
                        'genres': ','.join(artist.get('genres', []))
                    })
                
                # Extract album data
                if 'album' in track:
                    album = track['album']
                    albums_data.append({
                        'album_id': album['id'],
                        'name': album['name'],
                        'artist_id': track['artists'][0]['id'] if track['artists'] else None,
                        'release_date': album.get('release_date', ''),
                        'total_tracks': album.get('total_tracks', 0),
                        'album_type': album.get('album_type', 'album'),
                        'popularity': album.get('popularity', 0)
                    })
                
                # Extract track data
                audio_features = track.get('audio_features', {})
                tracks_data.append({
                    'track_id': track['id'],
                    'name': track['name'],
                    'artist_id': track['artists'][0]['id'] if track['artists'] else None,
                    'album_id': track['album']['id'] if 'album' in track else None,
                    'duration_ms': track.get('duration_ms', 0),
                    'explicit': track.get('explicit', False),
                    'popularity': track.get('popularity', 0),
                    'danceability': audio_features.get('danceability', 0.0),
                    'energy': audio_features.get('energy', 0.0),
                    'key': audio_features.get('key', -1),
                    'loudness': audio_features.get('loudness', 0.0),
                    'mode': audio_features.get('mode', 0),
                    'speechiness': audio_features.get('speechiness', 0.0),
                    'acousticness': audio_features.get('acousticness', 0.0),
                    'instrumentalness': audio_features.get('instrumentalness', 0.0),
                    'liveness': audio_features.get('liveness', 0.0),
                    'valence': audio_features.get('valence', 0.0),
                    'tempo': audio_features.get('tempo', 0.0),
                    'time_signature': audio_features.get('time_signature', 4)
                })
            
            # Save to database
            db_manager = DatabaseManager()
            
            if artists_data:
                artists_df = pd.DataFrame(artists_data)
                db_manager.insert_artists(artists_df)
            
            if albums_data:
                albums_df = pd.DataFrame(albums_data)
                db_manager.insert_albums(albums_df)
            
            if tracks_data:
                tracks_df = pd.DataFrame(tracks_data)
                db_manager.insert_tracks(tracks_df)
            
            logger.info(f"Successfully saved {len(tracks)} tracks to database")
            
        except Exception as e:
            logger.error(f"Failed to save tracks to database: {e}")
            raise
