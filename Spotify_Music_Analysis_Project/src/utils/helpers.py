"""
Helper functions for the Spotify Music Analysis Project.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional

def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
    """
    Flatten nested dictionary for CSV export.
    
    Args:
        d: Dictionary to flatten
        parent_key: Parent key for nested items
        sep: Separator for keys
        
    Returns:
        Flattened dictionary
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            # Handle lists by joining with semicolon
            items.append((new_key, ';'.join(map(str, v))))
        else:
            items.append((new_key, v))
    return dict(items)

def validate_audio_features(features: Dict[str, Any]) -> bool:
    """
    Validate audio features data.
    
    Args:
        features: Dictionary of audio features
        
    Returns:
        True if valid, False otherwise
    """
    required_features = ['danceability', 'energy', 'valence', 'acousticness']
    
    for feature in required_features:
        if feature not in features:
            return False
        
        value = features[feature]
        if not isinstance(value, (int, float)) or not (0 <= value <= 1):
            return False
    
    return True

def calculate_audio_feature_stats(df: pd.DataFrame, features: List[str]) -> Dict[str, Dict[str, float]]:
    """
    Calculate statistics for audio features.
    
    Args:
        df: DataFrame with audio features
        features: List of feature names
        
    Returns:
        Dictionary with feature statistics
    """
    stats = {}
    
    for feature in features:
        if feature in df.columns:
            feature_data = df[feature].dropna()
            stats[feature] = {
                'mean': feature_data.mean(),
                'median': feature_data.median(),
                'std': feature_data.std(),
                'min': feature_data.min(),
                'max': feature_data.max(),
                'q25': feature_data.quantile(0.25),
                'q75': feature_data.quantile(0.75)
            }
    
    return stats

def format_duration_ms(duration_ms: int) -> str:
    """
    Format duration in milliseconds to readable format.
    
    Args:
        duration_ms: Duration in milliseconds
        
    Returns:
        Formatted duration string
    """
    minutes = duration_ms // 60000
    seconds = (duration_ms % 60000) // 1000
    return f"{minutes}:{seconds:02d}"

def categorize_tempo(tempo: float) -> str:
    """
    Categorize tempo into speed categories.
    
    Args:
        tempo: Tempo in BPM
        
    Returns:
        Tempo category
    """
    if tempo < 100:
        return 'Slow'
    elif tempo < 140:
        return 'Medium'
    else:
        return 'Fast'

def calculate_popularity_score(track_data: Dict[str, Any]) -> float:
    """
    Calculate a custom popularity score based on multiple factors.
    
    Args:
        track_data: Dictionary containing track data
        
    Returns:
        Calculated popularity score
    """
    base_popularity = track_data.get('popularity', 0)
    
    # Audio features that might influence popularity
    danceability = track_data.get('danceability', 0.5)
    energy = track_data.get('energy', 0.5)
    valence = track_data.get('valence', 0.5)
    
    # Weighted score
    audio_score = (danceability * 0.3 + energy * 0.4 + valence * 0.3) * 100
    
    # Combine with base popularity
    final_score = (base_popularity * 0.7 + audio_score * 0.3)
    
    return min(final_score, 100)  # Cap at 100

def detect_outliers(df: pd.DataFrame, column: str, threshold: float = 3.0) -> pd.DataFrame:
    """
    Detect outliers in a DataFrame column using Z-score.
    
    Args:
        df: DataFrame to analyze
        column: Column name to check for outliers
        threshold: Z-score threshold for outlier detection
        
    Returns:
        DataFrame containing outliers
    """
    if column not in df.columns:
        return pd.DataFrame()
    
    z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
    outliers = df[z_scores > threshold]
    
    return outliers

def create_summary_statistics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Create comprehensive summary statistics for a DataFrame.
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        Dictionary with summary statistics
    """
    summary = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'missing_values': df.isnull().sum().to_dict(),
        'data_types': df.dtypes.to_dict(),
        'memory_usage': df.memory_usage(deep=True).sum(),
        'numeric_columns': df.select_dtypes(include=[np.number]).columns.tolist(),
        'categorical_columns': df.select_dtypes(include=['object']).columns.tolist()
    }
    
    # Add basic statistics for numeric columns
    if summary['numeric_columns']:
        summary['numeric_stats'] = df[summary['numeric_columns']].describe().to_dict()
    
    return summary
