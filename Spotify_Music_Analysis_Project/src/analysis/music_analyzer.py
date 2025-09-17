"""
Music Analyzer for the Spotify Music Analysis Project.

This module provides comprehensive analysis capabilities for Spotify music data,
including genre analysis, audio feature analysis, and trend identification.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
import logging
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy import stats
import warnings

from config import AUDIO_FEATURES, GENRE_CATEGORIES, ANALYSIS_CONFIG
from src.database.database_manager import DatabaseManager

logger = logging.getLogger(__name__)
warnings.filterwarnings('ignore')

class MusicAnalyzer:
    """
    Comprehensive music analysis class with advanced analytical capabilities.
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize the music analyzer.
        
        Args:
            db_path: Path to SQLite database (optional)
        """
        self.db_manager = DatabaseManager(db_path)
        self.tracks_df = None
        self.artists_df = None
        self.albums_df = None
    
    def load_data(self):
        """Load data from database into DataFrames."""
        try:
            # Load tracks data with joins
            self.tracks_df = self.db_manager.execute_query("""
                SELECT t.*, a.name as artist_name, a.genres, a.popularity as artist_popularity,
                       al.name as album_name, al.release_date
                FROM tracks t
                LEFT JOIN artists a ON t.artist_id = a.artist_id
                LEFT JOIN albums al ON t.album_id = al.album_id
            """)
            
            # Load artists data
            self.artists_df = self.db_manager.execute_query("SELECT * FROM artists")
            
            # Load albums data
            self.albums_df = self.db_manager.execute_query("SELECT * FROM albums")
            
            logger.info(f"Loaded {len(self.tracks_df)} tracks, {len(self.artists_df)} artists, {len(self.albums_df)} albums")
            
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            raise
    
    def get_basic_statistics(self) -> Dict[str, Any]:
        """Get basic statistics about the dataset."""
        if self.tracks_df is None:
            self.load_data()
        
        stats = {
            'total_tracks': len(self.tracks_df),
            'total_artists': len(self.artists_df),
            'total_albums': len(self.albums_df),
            'popularity_stats': {
                'mean': self.tracks_df['popularity'].mean(),
                'median': self.tracks_df['popularity'].median(),
                'std': self.tracks_df['popularity'].std(),
                'min': self.tracks_df['popularity'].min(),
                'max': self.tracks_df['popularity'].max()
            }
        }
        
        return stats
    
    def analyze_audio_features(self) -> Dict[str, Any]:
        """Analyze audio features across the dataset."""
        if self.tracks_df is None:
            self.load_data()
        
        audio_features = ['danceability', 'energy', 'valence', 'acousticness', 
                         'instrumentalness', 'liveness', 'speechiness']
        
        analysis = {}
        
        for feature in audio_features:
            if feature in self.tracks_df.columns:
                feature_data = self.tracks_df[feature].dropna()
                analysis[feature] = {
                    'mean': feature_data.mean(),
                    'median': feature_data.median(),
                    'std': feature_data.std(),
                    'min': feature_data.min(),
                    'max': feature_data.max(),
                    'q25': feature_data.quantile(0.25),
                    'q75': feature_data.quantile(0.75)
                }
        
        # Correlation analysis
        correlation_matrix = self.tracks_df[audio_features].corr()
        analysis['correlations'] = correlation_matrix.to_dict()
        
        return analysis
    
    def analyze_genres(self) -> Dict[str, Any]:
        """Analyze genre distribution and characteristics."""
        if self.tracks_df is None:
            self.load_data()
        
        # Extract genres from the genres column
        all_genres = []
        for genres_str in self.tracks_df['genres'].dropna():
            if isinstance(genres_str, str):
                genres = [g.strip() for g in genres_str.split(',')]
                all_genres.extend(genres)
        
        genre_counts = pd.Series(all_genres).value_counts()
        
        # Categorize genres
        categorized_genres = {}
        for category, genre_list in GENRE_CATEGORIES.items():
            category_tracks = self.tracks_df[
                self.tracks_df['genres'].str.contains('|'.join(genre_list), case=False, na=False)
            ]
            if len(category_tracks) > 0:
                categorized_genres[category] = {
                    'track_count': len(category_tracks),
                    'avg_popularity': category_tracks['popularity'].mean(),
                    'avg_danceability': category_tracks['danceability'].mean(),
                    'avg_energy': category_tracks['energy'].mean(),
                    'avg_valence': category_tracks['valence'].mean()
                }
        
        return {
            'top_genres': genre_counts.head(10).to_dict(),
            'categorized_genres': categorized_genres,
            'total_unique_genres': len(genre_counts)
        }
    
    def analyze_artists(self) -> Dict[str, Any]:
        """Analyze artist performance and characteristics."""
        if self.tracks_df is None:
            self.load_data()
        
        # Artist performance analysis
        artist_stats = self.tracks_df.groupby('artist_name').agg({
            'track_id': 'count',
            'popularity': ['mean', 'std'],
            'danceability': 'mean',
            'energy': 'mean',
            'valence': 'mean'
        }).round(3)
        
        artist_stats.columns = ['track_count', 'avg_popularity', 'popularity_std', 
                               'avg_danceability', 'avg_energy', 'avg_valence']
        
        # Top artists by different metrics
        top_artists = {
            'by_popularity': artist_stats.nlargest(10, 'avg_popularity'),
            'by_track_count': artist_stats.nlargest(10, 'track_count'),
            'by_danceability': artist_stats.nlargest(10, 'avg_danceability'),
            'by_energy': artist_stats.nlargest(10, 'avg_energy'),
            'by_valence': artist_stats.nlargest(10, 'avg_valence')
        }
        
        return {
            'artist_stats': artist_stats,
            'top_artists': top_artists,
            'total_artists': len(artist_stats)
        }
    
    def perform_clustering(self, n_clusters: int = 5) -> Dict[str, Any]:
        """Perform K-means clustering on audio features."""
        if self.tracks_df is None:
            self.load_data()
        
        # Select audio features for clustering
        features = ['danceability', 'energy', 'valence', 'acousticness', 
                   'instrumentalness', 'liveness', 'speechiness']
        
        # Prepare data
        X = self.tracks_df[features].dropna()
        
        if len(X) < n_clusters:
            logger.warning(f"Not enough data for {n_clusters} clusters. Using {len(X)} clusters instead.")
            n_clusters = len(X)
        
        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(X_scaled)
        
        # Add cluster labels to the dataframe
        X_with_clusters = X.copy()
        X_with_clusters['cluster'] = cluster_labels
        
        # Analyze clusters
        cluster_analysis = {}
        for i in range(n_clusters):
            cluster_data = X_with_clusters[X_with_clusters['cluster'] == i]
            cluster_analysis[f'cluster_{i}'] = {
                'size': len(cluster_data),
                'percentage': len(cluster_data) / len(X_with_clusters) * 100,
                'characteristics': cluster_data[features].mean().to_dict()
            }
        
        # PCA for visualization
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X_scaled)
        
        return {
            'cluster_labels': cluster_labels,
            'cluster_centers': kmeans.cluster_centers_.tolist(),
            'cluster_analysis': cluster_analysis,
            'pca_components': X_pca.tolist(),
            'explained_variance_ratio': pca.explained_variance_ratio_.tolist()
        }
    
    def generate_insights(self) -> Dict[str, Any]:
        """Generate comprehensive insights from the analysis."""
        if self.tracks_df is None:
            self.load_data()
        
        insights = {
            'summary': {},
            'recommendations': [],
            'key_findings': []
        }
        
        # Basic statistics
        basic_stats = self.get_basic_statistics()
        insights['summary'] = basic_stats
        
        # Genre analysis
        genre_analysis = self.analyze_genres()
        
        # Find most popular genre
        if genre_analysis['categorized_genres']:
            most_popular_genre = max(genre_analysis['categorized_genres'].items(), 
                                   key=lambda x: x[1]['track_count'])
            insights['key_findings'].append(f"Most popular genre: {most_popular_genre[0]} with {most_popular_genre[1]['track_count']} tracks")
        
        # Audio feature analysis
        audio_analysis = self.analyze_audio_features()
        
        # Find highest energy tracks
        if 'energy' in audio_analysis:
            high_energy_threshold = audio_analysis['energy']['q75']
            high_energy_tracks = self.tracks_df[self.tracks_df['energy'] > high_energy_threshold]
            insights['key_findings'].append(f"High energy tracks (>75th percentile): {len(high_energy_tracks)} tracks")
        
        # Artist analysis
        artist_analysis = self.analyze_artists()
        
        # Find most productive artist
        if not artist_analysis['top_artists']['by_track_count'].empty:
            most_productive = artist_analysis['top_artists']['by_track_count'].iloc[0]
            insights['key_findings'].append(f"Most productive artist: {most_productive.name} with {most_productive['track_count']} tracks")
        
        # Generate recommendations
        insights['recommendations'] = [
            "Consider analyzing seasonal trends in music preferences",
            "Investigate correlation between audio features and popularity",
            "Explore artist collaboration patterns",
            "Analyze genre evolution over time",
            "Study the impact of explicit content on popularity"
        ]
        
        return insights
    
    def export_results(self, output_dir: str = None):
        """Export analysis results to various formats."""
        from config import INSIGHTS_DIR
        
        if output_dir is None:
            output_dir = INSIGHTS_DIR
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Export basic statistics
            basic_stats = self.get_basic_statistics()
            stats_df = pd.DataFrame([basic_stats])
            stats_path = output_dir / 'basic_statistics.csv'
            stats_df.to_csv(stats_path, index=False)
            logger.info(f"Exported basic statistics to: {stats_path}")
            
            # Export audio feature analysis
            audio_analysis = self.analyze_audio_features()
            audio_df = pd.DataFrame(audio_analysis).T
            audio_path = output_dir / 'audio_features_analysis.csv'
            audio_df.to_csv(audio_path)
            logger.info(f"Exported audio features analysis to: {audio_path}")
            
            # Export genre analysis
            genre_analysis = self.analyze_genres()
            genre_df = pd.DataFrame(genre_analysis['categorized_genres']).T
            genre_path = output_dir / 'genre_analysis.csv'
            genre_df.to_csv(genre_path)
            logger.info(f"Exported genre analysis to: {genre_path}")
            
            # Export insights
            insights = self.generate_insights()
            insights_path = output_dir / 'insights.json'
            import json
            with open(insights_path, 'w') as f:
                json.dump(insights, f, indent=2, default=str)
            logger.info(f"Exported insights to: {insights_path}")
            
        except Exception as e:
            logger.error(f"Failed to export analysis results: {e}")
            raise
