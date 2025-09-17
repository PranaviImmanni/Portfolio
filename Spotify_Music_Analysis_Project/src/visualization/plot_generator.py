"""
Plot Generator for the Spotify Music Analysis Project.

This module creates professional visualizations for the music analysis data.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
import logging
from typing import Dict, Any, Optional

from config import FIGURES_DIR, FIGURE_SIZE, DPI, STYLE, COLOR_PALETTE
from src.database.database_manager import DatabaseManager

logger = logging.getLogger(__name__)

class PlotGenerator:
    """
    Generates professional visualizations for music analysis data.
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize the plot generator.
        
        Args:
            db_path: Path to SQLite database (optional)
        """
        self.db_manager = DatabaseManager(db_path)
        self.figures_dir = FIGURES_DIR
        self.figures_dir.mkdir(parents=True, exist_ok=True)
        
        # Set plotting style
        plt.style.use(STYLE)
        sns.set_palette(COLOR_PALETTE)
    
    def create_all_visualizations(self):
        """Create all standard visualizations."""
        try:
            logger.info("Creating all visualizations")
            
            # Get analysis data
            analysis_data = self.db_manager.execute_analysis_queries()
            
            # Create individual plots
            self.create_top_artists_plot(analysis_data['top_artists'])
            self.create_genre_analysis_plot(analysis_data['genre_analysis'])
            self.create_audio_features_plot(analysis_data['audio_features_trends'])
            self.create_comprehensive_dashboard(analysis_data)
            
            logger.info("All visualizations created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create visualizations: {e}")
            raise
    
    def create_top_artists_plot(self, top_artists_df: pd.DataFrame):
        """Create top artists visualization."""
        try:
            fig, ax = plt.subplots(figsize=FIGURE_SIZE)
            
            # Top 10 artists by popularity
            top_10 = top_artists_df.head(10)
            bars = ax.barh(top_10['artist_name'], top_10['popularity'], 
                          color=plt.cm.viridis(np.linspace(0, 1, 10)))
            
            ax.set_title('Top 10 Artists by Popularity', fontsize=16, fontweight='bold')
            ax.set_xlabel('Popularity Score')
            ax.grid(True, alpha=0.3)
            
            # Add value labels
            for i, (bar, value) in enumerate(zip(bars, top_10['popularity'])):
                ax.text(value + 1, bar.get_y() + bar.get_height()/2, 
                       f'{value}', ha='left', va='center', fontweight='bold')
            
            plt.tight_layout()
            plt.savefig(self.figures_dir / 'top_artists.png', dpi=DPI, bbox_inches='tight')
            plt.close()
            
            logger.info("Created top artists plot")
            
        except Exception as e:
            logger.error(f"Failed to create top artists plot: {e}")
    
    def create_genre_analysis_plot(self, genre_analysis_df: pd.DataFrame):
        """Create genre analysis visualization."""
        try:
            if genre_analysis_df.empty:
                logger.warning("No genre analysis data available")
                return
            
            fig, ax = plt.subplots(figsize=FIGURE_SIZE)
            
            # Genre energy vs valence scatter plot
            scatter = ax.scatter(genre_analysis_df['avg_energy'], 
                               genre_analysis_df['avg_valence'], 
                               s=genre_analysis_df['artist_count']*20, 
                               c=genre_analysis_df['avg_popularity'], 
                               cmap='plasma', alpha=0.7, edgecolors='black')
            
            # Add genre labels
            for i, genre in enumerate(genre_analysis_df['genres']):
                ax.annotate(genre, 
                           (genre_analysis_df['avg_energy'].iloc[i], 
                            genre_analysis_df['avg_valence'].iloc[i]),
                           xytext=(5, 5), textcoords='offset points', fontsize=8)
            
            ax.set_title('Genre Analysis: Energy vs Valence', fontsize=16, fontweight='bold')
            ax.set_xlabel('Average Energy')
            ax.set_ylabel('Average Valence')
            ax.grid(True, alpha=0.3)
            
            # Add colorbar
            cbar = plt.colorbar(scatter, ax=ax)
            cbar.set_label('Average Popularity')
            
            plt.tight_layout()
            plt.savefig(self.figures_dir / 'genre_analysis.png', dpi=DPI, bbox_inches='tight')
            plt.close()
            
            logger.info("Created genre analysis plot")
            
        except Exception as e:
            logger.error(f"Failed to create genre analysis plot: {e}")
    
    def create_audio_features_plot(self, audio_trends_df: pd.DataFrame):
        """Create audio features visualization."""
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
            
            # Audio feature distribution
            audio_features = ['danceability', 'energy', 'valence', 'acousticness']
            
            # Get tracks data for feature analysis
            tracks_df = self.db_manager.execute_query("SELECT * FROM tracks")
            feature_means = [tracks_df[feature].mean() for feature in audio_features]
            
            bars1 = ax1.bar(audio_features, feature_means, 
                           color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
            ax1.set_title('Average Audio Features', fontsize=14, fontweight='bold')
            ax1.set_ylabel('Average Score')
            ax1.set_ylim(0, 1)
            ax1.grid(True, alpha=0.3)
            
            # Add value labels
            for bar, value in zip(bars1, feature_means):
                ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                        f'{value:.3f}', ha='center', va='bottom', fontweight='bold')
            
            # Tempo category analysis
            tempo_colors = ['#FF9999', '#66B2FF', '#99FF99']
            bars2 = ax2.bar(audio_trends_df['tempo_category'], 
                           audio_trends_df['track_count'], 
                           color=tempo_colors)
            ax2.set_title('Track Distribution by Tempo', fontsize=14, fontweight='bold')
            ax2.set_ylabel('Number of Tracks')
            ax2.grid(True, alpha=0.3)
            
            # Add value labels
            for bar, value in zip(bars2, audio_trends_df['track_count']):
                ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                        f'{value}', ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            plt.savefig(self.figures_dir / 'audio_features.png', dpi=DPI, bbox_inches='tight')
            plt.close()
            
            logger.info("Created audio features plot")
            
        except Exception as e:
            logger.error(f"Failed to create audio features plot: {e}")
    
    def create_comprehensive_dashboard(self, analysis_data: Dict[str, pd.DataFrame]):
        """Create a comprehensive dashboard with multiple visualizations."""
        try:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
            
            # 1. Top Artists
            top_artists = analysis_data['top_artists'].head(10)
            bars1 = ax1.barh(top_artists['artist_name'], top_artists['popularity'], 
                            color=plt.cm.viridis(np.linspace(0, 1, 10)))
            ax1.set_title('Top 10 Artists by Popularity', fontsize=14, fontweight='bold')
            ax1.set_xlabel('Popularity Score')
            ax1.grid(True, alpha=0.3)
            
            # 2. Genre Analysis
            if not analysis_data['genre_analysis'].empty:
                genre_df = analysis_data['genre_analysis']
                scatter = ax2.scatter(genre_df['avg_energy'], genre_df['avg_valence'], 
                                    s=genre_df['artist_count']*20, 
                                    c=genre_df['avg_popularity'], 
                                    cmap='plasma', alpha=0.7, edgecolors='black')
                ax2.set_title('Genre Analysis: Energy vs Valence', fontsize=14, fontweight='bold')
                ax2.set_xlabel('Average Energy')
                ax2.set_ylabel('Average Valence')
                ax2.grid(True, alpha=0.3)
                plt.colorbar(scatter, ax=ax2, label='Avg Popularity')
            
            # 3. Audio Features
            tracks_df = self.db_manager.execute_query("SELECT * FROM tracks")
            audio_features = ['danceability', 'energy', 'valence', 'acousticness']
            feature_means = [tracks_df[feature].mean() for feature in audio_features]
            
            bars3 = ax3.bar(audio_features, feature_means, 
                           color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
            ax3.set_title('Average Audio Features', fontsize=14, fontweight='bold')
            ax3.set_ylabel('Average Score')
            ax3.set_ylim(0, 1)
            ax3.grid(True, alpha=0.3)
            
            # 4. Tempo Analysis
            tempo_df = analysis_data['audio_features_trends']
            tempo_colors = ['#FF9999', '#66B2FF', '#99FF99']
            bars4 = ax4.bar(tempo_df['tempo_category'], tempo_df['track_count'], 
                           color=tempo_colors)
            ax4.set_title('Track Distribution by Tempo', fontsize=14, fontweight='bold')
            ax4.set_ylabel('Number of Tracks')
            ax4.grid(True, alpha=0.3)
            
            plt.suptitle('Spotify Music Analysis Dashboard', fontsize=20, fontweight='bold')
            plt.tight_layout()
            plt.savefig(self.figures_dir / 'comprehensive_dashboard.png', 
                       dpi=DPI, bbox_inches='tight')
            plt.close()
            
            logger.info("Created comprehensive dashboard")
            
        except Exception as e:
            logger.error(f"Failed to create comprehensive dashboard: {e}")
    
    def create_correlation_heatmap(self):
        """Create correlation heatmap for audio features."""
        try:
            tracks_df = self.db_manager.execute_query("SELECT * FROM tracks")
            
            # Select audio features for correlation
            audio_features = ['danceability', 'energy', 'valence', 'acousticness', 
                             'instrumentalness', 'liveness', 'speechiness', 'tempo']
            
            # Calculate correlation matrix
            corr_matrix = tracks_df[audio_features].corr()
            
            # Create heatmap
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                       square=True, ax=ax, cbar_kws={'shrink': 0.8})
            
            ax.set_title('Audio Features Correlation Matrix', fontsize=16, fontweight='bold')
            plt.tight_layout()
            plt.savefig(self.figures_dir / 'correlation_heatmap.png', 
                       dpi=DPI, bbox_inches='tight')
            plt.close()
            
            logger.info("Created correlation heatmap")
            
        except Exception as e:
            logger.error(f"Failed to create correlation heatmap: {e}")
