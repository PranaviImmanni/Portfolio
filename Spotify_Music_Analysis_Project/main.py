#!/usr/bin/env python3
"""
Main execution script for the Spotify Music Analysis Project.

This script orchestrates the complete data analysis pipeline:
1. Data collection (Spotify API or sample data)
2. Database setup and data storage
3. Analysis and insights generation
4. Visualization and reporting

Author: Data Analysis Team
Date: 2024
License: MIT
"""

import sys
import logging
from pathlib import Path

# Add src directory to Python path
sys.path.append(str(Path(__file__).parent / 'src'))

from config import create_directories, validate_spotify_credentials, LOG_LEVEL
from src.data_collection.spotify_api import SpotifyDataCollector
from src.data_collection.sample_data_generator import SampleDataGenerator
from src.database.database_manager import DatabaseManager
from src.analysis.music_analyzer import MusicAnalyzer
from src.visualization.plot_generator import PlotGenerator
from src.utils.logger import setup_logger

def main():
    """Main execution function."""
    # Setup logging
    logger = setup_logger(__name__, LOG_LEVEL)
    logger.info("Starting Spotify Music Analysis Project")
    
    try:
        # Create necessary directories
        create_directories()
        logger.info("Created project directories")
        
        # Initialize database
        db_manager = DatabaseManager()
        db_manager.initialize_database()
        logger.info("Database initialized successfully")
        
        # Data collection
        if validate_spotify_credentials():
            logger.info("Using Spotify API for data collection")
            collector = SpotifyDataCollector()
            tracks = collector.search_tracks('pop music', limit=100)
            collector.save_to_database(tracks)
        else:
            logger.info("Using sample data for demonstration")
            generator = SampleDataGenerator()
            artists_df, tracks_df = generator.create_sample_data()
            generator.save_to_database(artists_df, tracks_df)
        
        logger.info("Data collection completed")
        
        # Analysis
        analyzer = MusicAnalyzer()
        insights = analyzer.generate_insights()
        logger.info("Analysis completed")
        
        # Visualization
        plot_generator = PlotGenerator()
        plot_generator.create_all_visualizations()
        logger.info("Visualizations created")
        
        # Export results
        analyzer.export_results()
        logger.info("Results exported successfully")
        
        logger.info("Spotify Music Analysis Project completed successfully!")
        
    except Exception as e:
        logger.error(f"Project execution failed: {e}")
        raise

if __name__ == "__main__":
    main()
