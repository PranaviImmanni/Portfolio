-- =====================================================
-- SPOTIFY MUSIC ANALYSIS - ARTIST ANALYSIS
-- =====================================================
-- This script analyzes artists and their performance metrics
-- using Common Table Expressions (CTEs) for modular analysis

-- 1. Top Artists by Track Count with Performance Metrics
WITH artist_stats AS (
    SELECT 
        track_artist,
        COUNT(*) as track_count,
        AVG(track_popularity) as avg_popularity,
        AVG(energy) as avg_energy,
        AVG(danceability) as avg_danceability,
        AVG(valence) as avg_valence,
        AVG(tempo) as avg_tempo,
        AVG(duration_minutes) as avg_duration,
        MAX(track_popularity) as max_popularity,
        MIN(track_popularity) as min_popularity,
        COUNT(DISTINCT playlist_genre) as genres_covered,
        COUNT(DISTINCT release_year) as years_active
    FROM spotify_clean
    WHERE track_artist IS NOT NULL
    GROUP BY track_artist
    HAVING COUNT(*) >= 2  -- Only include artists with at least 2 tracks
),
artist_rankings AS (
    SELECT 
        *,
        RANK() OVER (ORDER BY track_count DESC) as rank_by_tracks,
        RANK() OVER (ORDER BY avg_popularity DESC) as rank_by_popularity,
        RANK() OVER (ORDER BY avg_energy DESC) as rank_by_energy,
        RANK() OVER (ORDER BY genres_covered DESC) as rank_by_genre_diversity
    FROM artist_stats
)
SELECT 
    track_artist,
    track_count,
    ROUND(avg_popularity, 2) as avg_popularity,
    ROUND(avg_energy, 3) as avg_energy,
    ROUND(avg_danceability, 3) as avg_danceability,
    ROUND(avg_valence, 3) as avg_valence,
    ROUND(avg_tempo, 1) as avg_tempo,
    ROUND(avg_duration, 2) as avg_duration_minutes,
    max_popularity,
    min_popularity,
    genres_covered,
    years_active,
    rank_by_tracks,
    rank_by_popularity,
    rank_by_energy,
    rank_by_genre_diversity
FROM artist_rankings
ORDER BY track_count DESC
LIMIT 20;

-- 2. Artist Performance by Genre
WITH artist_genre_performance AS (
    SELECT 
        track_artist,
        playlist_genre,
        COUNT(*) as track_count,
        AVG(track_popularity) as avg_popularity,
        AVG(energy) as avg_energy,
        AVG(danceability) as avg_danceability,
        AVG(valence) as avg_valence
    FROM spotify_clean
    WHERE track_artist IS NOT NULL 
        AND playlist_genre IS NOT NULL
    GROUP BY track_artist, playlist_genre
    HAVING COUNT(*) >= 2
)
SELECT 
    track_artist,
    playlist_genre,
    track_count,
    ROUND(avg_popularity, 2) as avg_popularity,
    ROUND(avg_energy, 3) as avg_energy,
    ROUND(avg_danceability, 3) as avg_danceability,
    ROUND(avg_valence, 3) as avg_valence,
    ROUND(avg_energy + avg_danceability + avg_valence, 3) as combined_score
FROM artist_genre_performance
ORDER BY avg_popularity DESC, track_count DESC;

-- 3. Artist Evolution Over Time
WITH artist_yearly_stats AS (
    SELECT 
        track_artist,
        release_year,
        COUNT(*) as track_count,
        AVG(track_popularity) as avg_popularity,
        AVG(energy) as avg_energy,
        AVG(danceability) as avg_danceability,
        AVG(valence) as avg_valence
    FROM spotify_clean
    WHERE track_artist IS NOT NULL 
        AND release_year IS NOT NULL
        AND release_year >= 1990
    GROUP BY track_artist, release_year
    HAVING COUNT(*) >= 1
),
artist_trends AS (
    SELECT 
        track_artist,
        COUNT(DISTINCT release_year) as years_active,
        AVG(avg_popularity) as overall_avg_popularity,
        AVG(avg_energy) as overall_avg_energy,
        AVG(avg_danceability) as overall_avg_danceability,
        MAX(avg_popularity) - MIN(avg_popularity) as popularity_range,
        MAX(release_year) - MIN(release_year) as career_span
    FROM artist_yearly_stats
    GROUP BY track_artist
    HAVING COUNT(DISTINCT release_year) >= 3  -- Artists active for at least 3 years
)
SELECT 
    track_artist,
    years_active,
    career_span,
    ROUND(overall_avg_popularity, 2) as overall_avg_popularity,
    ROUND(overall_avg_energy, 3) as overall_avg_energy,
    ROUND(overall_avg_danceability, 3) as overall_avg_danceability,
    ROUND(popularity_range, 2) as popularity_range,
    CASE 
        WHEN popularity_range > 20 THEN 'High Variability'
        WHEN popularity_range > 10 THEN 'Moderate Variability'
        ELSE 'Consistent'
    END as popularity_consistency
FROM artist_trends
ORDER BY overall_avg_popularity DESC;

-- 4. Artist Collaboration Analysis
WITH collaboration_tracks AS (
    SELECT 
        track_id,
        track_name,
        track_artist,
        track_popularity,
        energy,
        danceability,
        valence,
        CASE 
            WHEN track_artist LIKE '%,%' OR track_artist LIKE '%&%' OR track_artist LIKE '%feat.%' 
            THEN 'Collaboration'
            ELSE 'Solo'
        END as collaboration_type
    FROM spotify_clean
    WHERE track_artist IS NOT NULL
),
collaboration_stats AS (
    SELECT 
        collaboration_type,
        COUNT(*) as track_count,
        AVG(track_popularity) as avg_popularity,
        AVG(energy) as avg_energy,
        AVG(danceability) as avg_danceability,
        AVG(valence) as avg_valence
    FROM collaboration_tracks
    GROUP BY collaboration_type
)
SELECT 
    collaboration_type,
    track_count,
    ROUND(avg_popularity, 2) as avg_popularity,
    ROUND(avg_energy, 3) as avg_energy,
    ROUND(avg_danceability, 3) as avg_danceability,
    ROUND(avg_valence, 3) as avg_valence,
    ROUND((track_count * 100.0) / (SELECT COUNT(*) FROM collaboration_tracks), 2) as percentage_of_total
FROM collaboration_stats
ORDER BY avg_popularity DESC;

-- 5. Top Artists by Feature Performance
WITH artist_feature_rankings AS (
    SELECT 
        track_artist,
        COUNT(*) as track_count,
        AVG(track_popularity) as avg_popularity,
        AVG(energy) as avg_energy,
        AVG(danceability) as avg_danceability,
        AVG(valence) as avg_valence,
        AVG(tempo) as avg_tempo,
        AVG(loudness) as avg_loudness,
        RANK() OVER (ORDER BY AVG(track_popularity) DESC) as popularity_rank,
        RANK() OVER (ORDER BY AVG(energy) DESC) as energy_rank,
        RANK() OVER (ORDER BY AVG(danceability) DESC) as danceability_rank,
        RANK() OVER (ORDER BY AVG(valence) DESC) as valence_rank
    FROM spotify_clean
    WHERE track_artist IS NOT NULL
    GROUP BY track_artist
    HAVING COUNT(*) >= 3  -- Only include artists with at least 3 tracks
)
SELECT 
    track_artist,
    track_count,
    ROUND(avg_popularity, 2) as avg_popularity,
    ROUND(avg_energy, 3) as avg_energy,
    ROUND(avg_danceability, 3) as avg_danceability,
    ROUND(avg_valence, 3) as avg_valence,
    ROUND(avg_tempo, 1) as avg_tempo,
    ROUND(avg_loudness, 2) as avg_loudness,
    popularity_rank,
    energy_rank,
    danceability_rank,
    valence_rank,
    CASE 
        WHEN popularity_rank <= 10 AND energy_rank <= 10 THEN 'High Popularity & Energy'
        WHEN popularity_rank <= 10 AND danceability_rank <= 10 THEN 'High Popularity & Danceability'
        WHEN popularity_rank <= 10 THEN 'High Popularity'
        WHEN energy_rank <= 10 THEN 'High Energy'
        WHEN danceability_rank <= 10 THEN 'High Danceability'
        ELSE 'Balanced'
    END as artist_characteristic
FROM artist_feature_rankings
WHERE popularity_rank <= 20 OR energy_rank <= 20 OR danceability_rank <= 20
ORDER BY avg_popularity DESC; 