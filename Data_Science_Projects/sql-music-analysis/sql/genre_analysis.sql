-- =====================================================
-- SPOTIFY MUSIC ANALYSIS - GENRE ANALYSIS
-- =====================================================
-- This script analyzes music genres and their characteristics
-- using Common Table Expressions (CTEs) for modular analysis

-- 1. Genre Overview with CTE for reusable metrics
WITH genre_stats AS (
    SELECT 
        playlist_genre,
        COUNT(*) as track_count,
        COUNT(DISTINCT track_artist) as unique_artists,
        AVG(track_popularity) as avg_popularity,
        AVG(energy) as avg_energy,
        AVG(danceability) as avg_danceability,
        AVG(valence) as avg_valence,
        AVG(tempo) as avg_tempo,
        AVG(loudness) as avg_loudness,
        AVG(duration_minutes) as avg_duration,
        STDDEV(track_popularity) as std_popularity,
        STDDEV(energy) as std_energy
    FROM spotify_clean
    WHERE playlist_genre IS NOT NULL
    GROUP BY playlist_genre
),
genre_rankings AS (
    SELECT 
        *,
        RANK() OVER (ORDER BY track_count DESC) as rank_by_tracks,
        RANK() OVER (ORDER BY avg_popularity DESC) as rank_by_popularity,
        RANK() OVER (ORDER BY avg_energy DESC) as rank_by_energy,
        RANK() OVER (ORDER BY avg_danceability DESC) as rank_by_danceability
    FROM genre_stats
)
SELECT 
    playlist_genre,
    track_count,
    unique_artists,
    ROUND(avg_popularity, 2) as avg_popularity,
    ROUND(avg_energy, 3) as avg_energy,
    ROUND(avg_danceability, 3) as avg_danceability,
    ROUND(avg_valence, 3) as avg_valence,
    ROUND(avg_tempo, 1) as avg_tempo,
    ROUND(avg_duration, 2) as avg_duration_minutes,
    rank_by_tracks,
    rank_by_popularity,
    rank_by_energy,
    rank_by_danceability
FROM genre_rankings
ORDER BY track_count DESC;

-- 2. Genre Energy Analysis by Decade
WITH genre_decade_energy AS (
    SELECT 
        playlist_genre,
        decade,
        COUNT(*) as track_count,
        AVG(energy) as avg_energy,
        AVG(danceability) as avg_danceability,
        AVG(valence) as avg_valence
    FROM spotify_clean
    WHERE playlist_genre IS NOT NULL 
        AND decade IS NOT NULL
    GROUP BY playlist_genre, decade
)
SELECT 
    playlist_genre,
    decade,
    track_count,
    ROUND(avg_energy, 3) as avg_energy,
    ROUND(avg_danceability, 3) as avg_danceability,
    ROUND(avg_valence, 3) as avg_valence,
    ROUND(avg_energy + avg_danceability + avg_valence, 3) as energy_dance_valence_score
FROM genre_decade_energy
ORDER BY playlist_genre, decade;

-- 3. Genre Popularity Trends
WITH genre_popularity_trends AS (
    SELECT 
        playlist_genre,
        release_year,
        COUNT(*) as track_count,
        AVG(track_popularity) as avg_popularity,
        MAX(track_popularity) as max_popularity,
        MIN(track_popularity) as min_popularity
    FROM spotify_clean
    WHERE playlist_genre IS NOT NULL 
        AND release_year IS NOT NULL
        AND release_year >= 1990
    GROUP BY playlist_genre, release_year
    HAVING COUNT(*) >= 5  -- Only include years with at least 5 tracks
)
SELECT 
    playlist_genre,
    release_year,
    track_count,
    ROUND(avg_popularity, 2) as avg_popularity,
    max_popularity,
    min_popularity,
    ROUND((max_popularity - min_popularity), 2) as popularity_range
FROM genre_popularity_trends
ORDER BY playlist_genre, release_year;

-- 4. Genre Feature Correlations
WITH genre_features AS (
    SELECT 
        playlist_genre,
        AVG(energy) as avg_energy,
        AVG(danceability) as avg_danceability,
        AVG(valence) as avg_valence,
        AVG(tempo) as avg_tempo,
        AVG(loudness) as avg_loudness,
        AVG(speechiness) as avg_speechiness,
        AVG(acousticness) as avg_acousticness,
        AVG(instrumentalness) as avg_instrumentalness,
        AVG(liveness) as avg_liveness
    FROM spotify_clean
    WHERE playlist_genre IS NOT NULL
    GROUP BY playlist_genre
)
SELECT 
    playlist_genre,
    ROUND(avg_energy, 3) as avg_energy,
    ROUND(avg_danceability, 3) as avg_danceability,
    ROUND(avg_valence, 3) as avg_valence,
    ROUND(avg_tempo, 1) as avg_tempo,
    ROUND(avg_loudness, 2) as avg_loudness,
    ROUND(avg_speechiness, 3) as avg_speechiness,
    ROUND(avg_acousticness, 3) as avg_acousticness,
    ROUND(avg_instrumentalness, 3) as avg_instrumentalness,
    ROUND(avg_liveness, 3) as avg_liveness,
    CASE 
        WHEN avg_energy > 0.7 AND avg_danceability > 0.7 THEN 'High Energy & Danceable'
        WHEN avg_energy > 0.7 THEN 'High Energy'
        WHEN avg_danceability > 0.7 THEN 'High Danceability'
        WHEN avg_acousticness > 0.7 THEN 'Acoustic'
        WHEN avg_instrumentalness > 0.7 THEN 'Instrumental'
        ELSE 'Balanced'
    END as genre_characteristic
FROM genre_features
ORDER BY avg_energy DESC;

-- 5. Subgenre Analysis
SELECT 
    playlist_genre,
    playlist_subgenre,
    COUNT(*) as track_count,
    ROUND(AVG(track_popularity), 2) as avg_popularity,
    ROUND(AVG(energy), 3) as avg_energy,
    ROUND(AVG(danceability), 3) as avg_danceability,
    ROUND(AVG(valence), 3) as avg_valence
FROM spotify_clean
WHERE playlist_genre IS NOT NULL 
    AND playlist_subgenre IS NOT NULL
GROUP BY playlist_genre, playlist_subgenre
HAVING COUNT(*) >= 3  -- Only include subgenres with at least 3 tracks
ORDER BY playlist_genre, track_count DESC; 