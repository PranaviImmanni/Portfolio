"""
Database Manager for the Spotify Music Analysis Project.

This module handles all database operations including initialization,
data storage, and query execution.
"""

import sqlite3
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

from config import SQLITE_DB_PATH, DATABASE_SCHEMA, PROCESSED_DATA_DIR

logger = logging.getLogger(__name__)

class DatabaseManager:
    """
    Manages database operations for the Spotify Music Analysis Project.
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize the database manager.
        
        Args:
            db_path: Path to SQLite database (optional)
        """
        self.db_path = db_path or SQLITE_DB_PATH
        self.connection = None
        
        # Ensure directory exists
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
    
    def connect(self):
        """Establish database connection."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            logger.info(f"Connected to database: {self.db_path}")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
    
    def disconnect(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")
    
    def initialize_database(self):
        """Initialize database with schema."""
        try:
            self.connect()
            cursor = self.connection.cursor()
            
            # Execute schema
            cursor.executescript(DATABASE_SCHEMA)
            self.connection.commit()
            
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
        finally:
            self.disconnect()
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> pd.DataFrame:
        """
        Execute a SQL query and return results as DataFrame.
        
        Args:
            query: SQL query string
            params: Query parameters (optional)
            
        Returns:
            DataFrame with query results
        """
        try:
            self.connect()
            result = pd.read_sql_query(query, self.connection, params=params)
            return result
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise
        finally:
            self.disconnect()
    
    def insert_artists(self, artists_df: pd.DataFrame):
        """
        Insert artists data into the database.
        
        Args:
            artists_df: DataFrame containing artists data
        """
        try:
            self.connect()
            artists_df.to_sql('artists', self.connection, if_exists='replace', index=False)
            self.connection.commit()
            logger.info(f"Inserted {len(artists_df)} artists")
        except Exception as e:
            logger.error(f"Failed to insert artists: {e}")
            raise
        finally:
            self.disconnect()
    
    def insert_albums(self, albums_df: pd.DataFrame):
        """
        Insert albums data into the database.
        
        Args:
            albums_df: DataFrame containing albums data
        """
        try:
            self.connect()
            albums_df.to_sql('albums', self.connection, if_exists='replace', index=False)
            self.connection.commit()
            logger.info(f"Inserted {len(albums_df)} albums")
        except Exception as e:
            logger.error(f"Failed to insert albums: {e}")
            raise
        finally:
            self.disconnect()
    
    def insert_tracks(self, tracks_df: pd.DataFrame):
        """
        Insert tracks data into the database.
        
        Args:
            tracks_df: DataFrame containing tracks data
        """
        try:
            self.connect()
            tracks_df.to_sql('tracks', self.connection, if_exists='replace', index=False)
            self.connection.commit()
            logger.info(f"Inserted {len(tracks_df)} tracks")
        except Exception as e:
            logger.error(f"Failed to insert tracks: {e}")
            raise
        finally:
            self.disconnect()
    
    def get_table_info(self, table_name: str) -> pd.DataFrame:
        """
        Get information about a table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            DataFrame with table information
        """
        query = f"PRAGMA table_info({table_name})"
        return self.execute_query(query)
    
    def get_table_counts(self) -> Dict[str, int]:
        """
        Get row counts for all tables.
        
        Returns:
            Dictionary with table names and row counts
        """
        tables = ['artists', 'albums', 'tracks']
        counts = {}
        
        for table in tables:
            try:
                query = f"SELECT COUNT(*) as count FROM {table}"
                result = self.execute_query(query)
                counts[table] = result['count'].iloc[0]
            except Exception as e:
                logger.warning(f"Failed to get count for {table}: {e}")
                counts[table] = 0
        
        return counts
    
    def execute_analysis_queries(self) -> Dict[str, pd.DataFrame]:
        """
        Execute common analysis queries.
        
        Returns:
            Dictionary with query names and results
        """
        queries = {
            'top_artists': """
                SELECT 
                    a.name as artist_name,
                    a.popularity,
                    a.followers,
                    COUNT(t.track_id) as track_count,
                    AVG(t.popularity) as avg_track_popularity
                FROM artists a
                JOIN tracks t ON a.artist_id = t.artist_id
                GROUP BY a.artist_id, a.name, a.popularity, a.followers
                ORDER BY a.popularity DESC
                LIMIT 10
            """,
            'genre_analysis': """
                SELECT 
                    a.genres,
                    COUNT(DISTINCT a.artist_id) as artist_count,
                    AVG(t.energy) as avg_energy,
                    AVG(t.valence) as avg_valence,
                    AVG(t.danceability) as avg_danceability,
                    AVG(t.popularity) as avg_popularity
                FROM artists a
                JOIN tracks t ON a.artist_id = t.artist_id
                WHERE a.genres IS NOT NULL
                GROUP BY a.genres
                HAVING artist_count > 2
                ORDER BY avg_popularity DESC
            """,
            'audio_features_trends': """
                SELECT 
                    CASE 
                        WHEN t.tempo < 100 THEN 'Slow'
                        WHEN t.tempo < 140 THEN 'Medium'
                        ELSE 'Fast'
                    END as tempo_category,
                    COUNT(*) as track_count,
                    AVG(t.energy) as avg_energy,
                    AVG(t.valence) as avg_valence,
                    AVG(t.danceability) as avg_danceability,
                    AVG(t.acousticness) as avg_acousticness
                FROM tracks t
                WHERE t.tempo IS NOT NULL
                GROUP BY tempo_category
                ORDER BY avg_energy DESC
            """
        }
        
        results = {}
        for name, query in queries.items():
            try:
                results[name] = self.execute_query(query)
                logger.info(f"Executed query: {name}")
            except Exception as e:
                logger.error(f"Failed to execute query {name}: {e}")
                results[name] = pd.DataFrame()
        
        return results
