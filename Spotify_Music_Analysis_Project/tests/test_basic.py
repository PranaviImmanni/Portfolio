"""
Basic tests for the Spotify Music Analysis Project.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from src.data_collection.sample_data_generator import SampleDataGenerator
from src.database.database_manager import DatabaseManager

def test_sample_data_generation():
    """Test sample data generation."""
    generator = SampleDataGenerator()
    artists_df, tracks_df = generator.create_sample_data()
    
    assert len(artists_df) > 0
    assert len(tracks_df) > 0
    assert 'artist_id' in artists_df.columns
    assert 'track_id' in tracks_df.columns

def test_database_initialization():
    """Test database initialization."""
    db_manager = DatabaseManager(':memory:')  # Use in-memory database for testing
    db_manager.initialize_database()
    
    # Test that tables were created
    tables = db_manager.execute_query("SELECT name FROM sqlite_master WHERE type='table'")
    table_names = tables['name'].tolist()
    
    assert 'artists' in table_names
    assert 'albums' in table_names
    assert 'tracks' in table_names

if __name__ == "__main__":
    pytest.main([__file__])
