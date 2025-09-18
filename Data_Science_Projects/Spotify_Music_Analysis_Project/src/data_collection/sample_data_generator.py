"""
Sample Data Generator for the Spotify Music Analysis Project.

This module generates comprehensive sample data for demonstration
and testing purposes when Spotify API credentials are not available.
"""

import pandas as pd
import numpy as np
from typing import Tuple
import logging

from config import GENRE_CATEGORIES

logger = logging.getLogger(__name__)

class SampleDataGenerator:
    """
    Generates sample Spotify data for demonstration and testing.
    """
    
    def __init__(self):
        """Initialize the sample data generator."""
        self.artists_data = None
        self.tracks_data = None
        self.albums_data = None
    
    def create_sample_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Create comprehensive sample Spotify data for analysis.
        
        Returns:
            Tuple of (artists_df, tracks_df)
        """
        logger.info("Creating sample Spotify data for analysis")
        
        np.random.seed(42)  # For reproducible results
        
        # Sample artists
        artist_names = [
            'Taylor Swift', 'Ed Sheeran', 'Drake', 'Ariana Grande', 'The Weeknd',
            'Billie Eilish', 'Post Malone', 'Dua Lipa', 'Olivia Rodrigo', 'Bad Bunny',
            'Justin Bieber', 'SZA', 'Harry Styles', 'Doja Cat', 'Lil Nas X',
            'The Kid LAROI', 'Bruno Mars', 'Adele', 'Kendrick Lamar', 'Travis Scott',
            'Lana Del Rey', 'Frank Ocean', 'Tyler, The Creator', 'Kanye West', 'Rihanna',
            'Beyoncé', 'Jay-Z', 'Eminem', 'Katy Perry', 'Lady Gaga',
            'Coldplay', 'Imagine Dragons', 'Maroon 5', 'OneRepublic', 'The Chainsmokers',
            'Calvin Harris', 'David Guetta', 'Martin Garrix', 'Skrillex', 'Deadmau5',
            'Pink Floyd', 'Led Zeppelin', 'The Beatles', 'Queen', 'AC/DC',
            'Metallica', 'Nirvana', 'Radiohead', 'Arctic Monkeys', 'The Strokes'
        ]
        
        genres = list(GENRE_CATEGORIES.keys())
        
        self.artists_data = {
            'artist_id': [f'artist_{i:03d}' for i in range(1, 51)],
            'name': artist_names,
            'popularity': np.random.randint(20, 100, 50),
            'followers': np.random.randint(10000, 10000000, 50),
            'genres': [np.random.choice(genres) for _ in range(50)]
        }
        
        # Sample tracks
        self.tracks_data = {
            'track_id': [f'track_{i:04d}' for i in range(1, 201)],
            'name': [f'Sample Track {i}' for i in range(1, 201)],
            'artist_id': np.random.choice(self.artists_data['artist_id'], 200),
            'album_id': [f'album_{i:03d}' for i in range(1, 201)],
            'duration_ms': np.random.randint(120000, 300000, 200),  # 2-5 minutes
            'explicit': np.random.choice([True, False], 200, p=[0.3, 0.7]),
            'popularity': np.random.randint(10, 100, 200),
            'danceability': np.random.uniform(0.0, 1.0, 200),
            'energy': np.random.uniform(0.0, 1.0, 200),
            'key': np.random.randint(0, 11, 200),
            'loudness': np.random.uniform(-20, 0, 200),
            'mode': np.random.choice([0, 1], 200),
            'speechiness': np.random.uniform(0.0, 1.0, 200),
            'acousticness': np.random.uniform(0.0, 1.0, 200),
            'instrumentalness': np.random.uniform(0.0, 1.0, 200),
            'liveness': np.random.uniform(0.0, 1.0, 200),
            'valence': np.random.uniform(0.0, 1.0, 200),
            'tempo': np.random.uniform(60, 200, 200),
            'time_signature': np.random.choice([3, 4, 5], 200, p=[0.1, 0.8, 0.1])
        }
        
        # Create albums data
        unique_albums = list(set(self.tracks_data['album_id']))
        self.albums_data = {
            'album_id': unique_albums,
            'name': [f'Album {i}' for i in range(1, len(unique_albums) + 1)],
            'artist_id': [self.tracks_data['artist_id'][self.tracks_data['album_id'].index(aid)] for aid in unique_albums],
            'release_date': '2023-01-01',
            'total_tracks': np.random.randint(8, 20, len(unique_albums)),
            'album_type': 'album',
            'popularity': np.random.randint(30, 90, len(unique_albums))
        }
        
        artists_df = pd.DataFrame(self.artists_data)
        tracks_df = pd.DataFrame(self.tracks_data)
        
        logger.info(f"Created sample data: {len(artists_df)} artists, {len(tracks_df)} tracks")
        
        return artists_df, tracks_df
    
    def save_to_database(self, artists_df: pd.DataFrame, tracks_df: pd.DataFrame):
        """
        Save sample data to database.
        
        Args:
            artists_df: Artists DataFrame
            tracks_df: Tracks DataFrame
        """
        from src.database.database_manager import DatabaseManager
        
        try:
            db_manager = DatabaseManager()
            
            # Save artists
            db_manager.insert_artists(artists_df)
            
            # Save albums
            albums_df = pd.DataFrame(self.albums_data)
            db_manager.insert_albums(albums_df)
            
            # Save tracks
            db_manager.insert_tracks(tracks_df)
            
            logger.info("Sample data saved to database successfully")
            
        except Exception as e:
            logger.error(f"Failed to save sample data to database: {e}")
            raise
    
    def get_data_summary(self) -> dict:
        """
        Get summary of generated data.
        
        Returns:
            Dictionary with data summary
        """
        if self.artists_data is None or self.tracks_data is None:
            return {}
        
        return {
            'total_artists': len(self.artists_data['artist_id']),
            'total_tracks': len(self.tracks_data['track_id']),
            'total_albums': len(self.albums_data['album_id']),
            'unique_genres': len(set(self.artists_data['genres'])),
            'avg_popularity': np.mean(self.tracks_data['popularity']),
            'avg_danceability': np.mean(self.tracks_data['danceability']),
            'avg_energy': np.mean(self.tracks_data['energy']),
            'avg_valence': np.mean(self.tracks_data['valence'])
        }
