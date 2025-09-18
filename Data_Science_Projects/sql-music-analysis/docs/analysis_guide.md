# 📊 Analysis Guide

This guide provides comprehensive instructions for running advanced SQL analysis on Spotify music data using the professional analysis framework.

## 🎯 Overview

The analysis framework provides multiple levels of complexity:

1. **Basic Analysis**: Simple aggregations and filtering
2. **Intermediate Analysis**: CTEs and window functions
3. **Advanced Analysis**: Complex business intelligence queries
4. **Custom Analysis**: Building your own analytical queries

## 🗄️ Database Schema

### Core Tables

#### `tracks` Table
```sql
CREATE TABLE tracks (
    track_id VARCHAR(50) PRIMARY KEY,
    track_name VARCHAR(255) NOT NULL,
    artist_name VARCHAR(255),
    genre VARCHAR(100),
    popularity INTEGER CHECK (popularity >= 0 AND popularity <= 100),
    danceability DECIMAL(3,2) CHECK (danceability >= 0.0 AND danceability <= 1.0),
    energy DECIMAL(3,2) CHECK (energy >= 0.0 AND energy <= 1.0),
    valence DECIMAL(3,2) CHECK (valence >= 0.0 AND valence <= 1.0),
    acousticness DECIMAL(3,2) CHECK (acousticness >= 0.0 AND acousticness <= 1.0),
    instrumentalness DECIMAL(3,2) CHECK (instrumentalness >= 0.0 AND instrumentalness <= 1.0),
    liveness DECIMAL(3,2) CHECK (liveness >= 0.0 AND liveness <= 1.0),
    speechiness DECIMAL(3,2) CHECK (speechiness >= 0.0 AND speechiness <= 1.0),
    tempo DECIMAL(5,2) CHECK (tempo > 0),
    duration_ms INTEGER CHECK (duration_ms > 0),
    release_year INTEGER
);
```

#### `artists` Table
```sql
CREATE TABLE artists (
    artist_id INTEGER PRIMARY KEY,
    artist_name VARCHAR(255) NOT NULL,
    genre VARCHAR(100),
    popularity INTEGER,
    followers_count INTEGER
);
```

## 📈 Analysis Examples

### 1. Basic Genre Analysis

```sql
-- Simple genre performance overview
SELECT 
    genre,
    COUNT(*) as track_count,
    ROUND(AVG(popularity), 2) as avg_popularity,
    ROUND(AVG(danceability), 3) as avg_danceability,
    ROUND(AVG(energy), 3) as avg_energy
FROM tracks 
GROUP BY genre 
ORDER BY avg_popularity DESC;
```

### 2. Advanced Genre Analysis with CTEs

```sql
-- Genre performance with rankings and market insights
WITH genre_performance AS (
    SELECT 
        genre,
        COUNT(*) as track_count,
        AVG(popularity) as avg_popularity,
        AVG(danceability) as avg_danceability,
        AVG(energy) as avg_energy,
        AVG(valence) as avg_valence
    FROM tracks 
    GROUP BY genre
),
genre_rankings AS (
    SELECT 
        genre,
        track_count,
        ROUND(avg_popularity, 2) as avg_popularity,
        ROUND(avg_danceability, 3) as avg_danceability,
        ROUND(avg_energy, 3) as avg_energy,
        ROUND(avg_valence, 3) as avg_valence,
        RANK() OVER (ORDER BY avg_popularity DESC) as popularity_rank,
        RANK() OVER (ORDER BY avg_danceability DESC) as danceability_rank
    FROM genre_performance
)
SELECT 
    genre,
    track_count,
    avg_popularity,
    avg_danceability,
    avg_energy,
    avg_valence,
    popularity_rank,
    danceability_rank,
    CASE 
        WHEN avg_popularity > 70 THEN 'High Potential'
        WHEN avg_popularity > 60 THEN 'Growing Market'
        ELSE 'Emerging Market'
    END as market_potential
FROM genre_rankings
ORDER BY popularity_rank;
```

### 3. Artist Performance Analysis

```sql
-- Top artists with feature analysis
SELECT 
    artist_name,
    COUNT(*) as track_count,
    ROUND(AVG(popularity), 2) as avg_popularity,
    ROUND(AVG(danceability), 3) as avg_danceability,
    ROUND(AVG(energy), 3) as avg_energy,
    ROUND(AVG(valence), 3) as avg_valence,
    CASE 
        WHEN AVG(danceability) > 0.7 AND AVG(energy) > 0.7 THEN 'High Energy Dance'
        WHEN AVG(acousticness) > 0.7 THEN 'Acoustic Focus'
        WHEN AVG(valence) > 0.7 THEN 'Positive Mood'
        ELSE 'Balanced'
    END as artist_characteristic
FROM tracks 
GROUP BY artist_name
HAVING COUNT(*) >= 5
ORDER BY avg_popularity DESC
LIMIT 10;
```

### 4. Trend Analysis with Window Functions

```sql
-- Year-over-year trend analysis
WITH yearly_stats AS (
    SELECT 
        release_year,
        genre,
        COUNT(*) as track_count,
        AVG(popularity) as avg_popularity,
        AVG(danceability) as avg_danceability
    FROM tracks 
    WHERE release_year IS NOT NULL
    GROUP BY release_year, genre
),
trend_analysis AS (
    SELECT 
        release_year,
        genre,
        track_count,
        ROUND(avg_popularity, 2) as avg_popularity,
        ROUND(avg_danceability, 3) as avg_danceability,
        LAG(avg_popularity) OVER (
            PARTITION BY genre 
            ORDER BY release_year
        ) as prev_year_popularity
    FROM yearly_stats
)
SELECT 
    release_year,
    genre,
    track_count,
    avg_popularity,
    avg_danceability,
    CASE 
        WHEN prev_year_popularity IS NOT NULL 
        THEN ROUND(avg_popularity - prev_year_popularity, 2)
        ELSE 0 
    END as popularity_change,
    CASE 
        WHEN avg_popularity - prev_year_popularity > 5 THEN 'Rising'
        WHEN avg_popularity - prev_year_popularity > 0 THEN 'Growing'
        WHEN avg_popularity - prev_year_popularity > -5 THEN 'Stable'
        ELSE 'Declining'
    END as trend_category
FROM trend_analysis
WHERE track_count >= 2
ORDER BY genre, release_year DESC;
```

## 🎯 Business Intelligence Queries

### Market Opportunity Analysis

```sql
-- Identify market opportunities by genre
WITH genre_analysis AS (
    SELECT 
        genre,
        COUNT(*) as track_count,
        COUNT(DISTINCT artist_name) as artist_count,
        AVG(popularity) as avg_popularity,
        AVG(danceability) as avg_danceability,
        AVG(energy) as avg_energy
    FROM tracks 
    GROUP BY genre
)
SELECT 
    genre,
    track_count,
    artist_count,
    ROUND(avg_popularity, 2) as avg_popularity,
    ROUND(avg_danceability, 3) as avg_danceability,
    ROUND(avg_energy, 3) as avg_energy,
    -- Market potential assessment
    CASE 
        WHEN avg_popularity > 70 AND track_count > 15 THEN 'High Potential - Trending'
        WHEN avg_popularity > 60 AND track_count > 10 THEN 'Growing Market'
        WHEN avg_popularity > 50 THEN 'Established Market'
        WHEN avg_popularity > 40 THEN 'Emerging Market'
        ELSE 'Niche Market'
    END as market_potential,
    -- Competition level
    CASE 
        WHEN artist_count < 5 THEN 'Oversaturated - High Competition'
        WHEN artist_count < 15 THEN 'Competitive - Strategic Positioning Needed'
        WHEN artist_count < 30 THEN 'Moderate Competition - Growth Opportunity'
        ELSE 'Low Competition - Market Entry Opportunity'
    END as competition_level
FROM genre_analysis
ORDER BY avg_popularity DESC;
```

### Content Strategy Insights

```sql
-- Content strategy recommendations based on audio features
SELECT 
    genre,
    COUNT(*) as track_count,
    ROUND(AVG(popularity), 2) as avg_popularity,
    ROUND(AVG(danceability), 3) as avg_danceability,
    ROUND(AVG(energy), 3) as avg_energy,
    ROUND(AVG(valence), 3) as avg_valence,
    ROUND(AVG(acousticness), 3) as avg_acousticness,
    -- Content strategy recommendations
    CASE 
        WHEN AVG(danceability) > 0.7 AND AVG(energy) > 0.7 THEN 'Party/Club Focus'
        WHEN AVG(acousticness) > 0.7 THEN 'Chill/Relaxation Focus'
        WHEN AVG(valence) > 0.7 THEN 'Positive/Uplifting Focus'
        WHEN AVG(instrumentalness) > 0.7 THEN 'Background/Study Focus'
        ELSE 'General Audience'
    END as content_strategy,
    -- Target audience
    CASE 
        WHEN AVG(tempo) > 140 THEN 'High Energy - Workout/Party'
        WHEN AVG(tempo) > 120 THEN 'Moderate Energy - General Listening'
        WHEN AVG(tempo) > 100 THEN 'Relaxed - Background Music'
        ELSE 'Very Relaxed - Meditation/Study'
    END as target_audience
FROM tracks 
GROUP BY genre
HAVING COUNT(*) >= 5
ORDER BY avg_popularity DESC;
```

## 🔧 Running Analysis

### Using Python

```python
import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect('data/processed/spotify_analysis.db')

# Run analysis query
query = """
SELECT 
    genre,
    COUNT(*) as track_count,
    ROUND(AVG(popularity), 2) as avg_popularity
FROM tracks 
GROUP BY genre 
ORDER BY avg_popularity DESC
"""

result = pd.read_sql_query(query, conn)
print(result)

conn.close()
```

### Using Command Line

```bash
# SQLite
sqlite3 data/processed/spotify_analysis.db < sql/analysis/genre_analysis.sql

# PostgreSQL
psql -d spotify_analysis -f sql/analysis/genre_analysis.sql
```

## 📊 Visualization Integration

### Export for Tableau

```sql
-- Export data for Tableau visualization
SELECT 
    genre,
    artist_name,
    track_name,
    popularity,
    danceability,
    energy,
    valence,
    acousticness,
    instrumentalness,
    liveness,
    speechiness,
    tempo,
    duration_ms,
    release_year
FROM tracks
ORDER BY popularity DESC;
```

### Export for Power BI

```sql
-- Export aggregated data for Power BI
SELECT 
    genre,
    COUNT(*) as track_count,
    ROUND(AVG(popularity), 2) as avg_popularity,
    ROUND(AVG(danceability), 3) as avg_danceability,
    ROUND(AVG(energy), 3) as avg_energy,
    ROUND(AVG(valence), 3) as avg_valence,
    ROUND(AVG(tempo), 2) as avg_tempo
FROM tracks 
GROUP BY genre
ORDER BY avg_popularity DESC;
```

## 🎯 Custom Analysis Development

### Building Your Own Queries

1. **Start with basic aggregations**
2. **Add CTEs for complex logic**
3. **Use window functions for rankings and trends**
4. **Include business logic with CASE statements**
5. **Add performance optimizations with indexes**

### Best Practices

- **Use meaningful column aliases**
- **Include data quality checks**
- **Add comments for complex logic**
- **Test with sample data first**
- **Optimize for performance**

### Performance Tips

- **Use indexes on frequently queried columns**
- **Limit result sets with WHERE clauses**
- **Use appropriate data types**
- **Consider partitioning for large datasets**

## 📈 Advanced Techniques

### Statistical Analysis

```sql
-- Calculate correlation between features
SELECT 
    genre,
    COUNT(*) as track_count,
    ROUND(AVG(popularity), 2) as avg_popularity,
    ROUND(STDDEV(popularity), 2) as popularity_stddev,
    ROUND(AVG(danceability), 3) as avg_danceability,
    ROUND(STDDEV(danceability), 3) as danceability_stddev
FROM tracks 
GROUP BY genre
HAVING COUNT(*) >= 10
ORDER BY avg_popularity DESC;
```

### Clustering Analysis

```sql
-- Identify track clusters by audio features
WITH track_features AS (
    SELECT 
        track_id,
        track_name,
        artist_name,
        genre,
        popularity,
        danceability,
        energy,
        valence,
        acousticness
    FROM tracks
),
feature_clusters AS (
    SELECT 
        track_id,
        track_name,
        artist_name,
        genre,
        popularity,
        -- Create feature clusters
        CASE 
            WHEN danceability > 0.7 AND energy > 0.7 THEN 'High Energy Dance'
            WHEN acousticness > 0.7 THEN 'Acoustic'
            WHEN valence > 0.7 THEN 'Positive'
            WHEN valence < 0.3 THEN 'Melancholic'
            ELSE 'Balanced'
        END as feature_cluster
    FROM track_features
)
SELECT 
    feature_cluster,
    COUNT(*) as track_count,
    ROUND(AVG(popularity), 2) as avg_popularity,
    COUNT(DISTINCT genre) as genre_diversity
FROM feature_clusters
GROUP BY feature_cluster
ORDER BY avg_popularity DESC;
```

This analysis guide provides the foundation for conducting comprehensive music data analysis using professional SQL techniques and business intelligence methodologies.

