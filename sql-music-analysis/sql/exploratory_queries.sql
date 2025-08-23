-- =====================================================
-- SPOTIFY MUSIC ANALYSIS - EXPLORATORY QUERIES
-- =====================================================
-- This script contains advanced exploratory queries
-- using window functions, CTEs, and complex aggregations

-- 1. Top Tracks by Feature Combinations
WITH track_scores AS (
    SELECT 
        track_name,
        track_artist,
        playlist_genre,
        track_popularity,
        energy,
        danceability,
        valence,
        tempo,
        duration_minutes,
        -- Create composite scores
        (energy * 0.3 + danceability * 0.3 + valence * 0.2 + (track_popularity/100) * 0.2) as overall_score,
        (energy + danceability) / 2 as energy_dance_score,
        (valence + danceability) / 2 as mood_score,
        ROW_NUMBER() OVER (ORDER BY track_popularity DESC) as popularity_rank,
        ROW_NUMBER() OVER (ORDER BY energy DESC) as energy_rank,
        ROW_NUMBER() OVER (ORDER BY danceability DESC) as danceability_rank
    FROM spotify_clean
    WHERE track_popularity IS NOT NULL
)
SELECT 
    track_name,
    track_artist,
    playlist_genre,
    track_popularity,
    ROUND(energy, 3) as energy,
    ROUND(danceability, 3) as danceability,
    ROUND(valence, 3) as valence,
    ROUND(tempo, 1) as tempo,
    ROUND(duration_minutes, 2) as duration_minutes,
    ROUND(overall_score, 3) as overall_score,
    ROUND(energy_dance_score, 3) as energy_dance_score,
    ROUND(mood_score, 3) as mood_score,
    popularity_rank,
    energy_rank,
    danceability_rank
FROM track_scores
WHERE popularity_rank <= 20 OR energy_rank <= 20 OR danceability_rank <= 20
ORDER BY overall_score DESC
LIMIT 30;

-- 2. Genre Evolution Analysis
WITH genre_evolution AS (
    SELECT 
        playlist_genre,
        release_year,
        COUNT(*) as track_count,
        AVG(track_popularity) as avg_popularity,
        AVG(energy) as avg_energy,
        AVG(danceability) as avg_danceability,
        AVG(valence) as avg_valence,
        LAG(AVG(track_popularity)) OVER (PARTITION BY playlist_genre ORDER BY release_year) as prev_year_popularity,
        LAG(AVG(energy)) OVER (PARTITION BY playlist_genre ORDER BY release_year) as prev_year_energy
    FROM spotify_clean
    WHERE playlist_genre IS NOT NULL 
        AND release_year IS NOT NULL
        AND release_year >= 1990
    GROUP BY playlist_genre, release_year
    HAVING COUNT(*) >= 3
)
SELECT 
    playlist_genre,
    release_year,
    track_count,
    ROUND(avg_popularity, 2) as avg_popularity,
    ROUND(avg_energy, 3) as avg_energy,
    ROUND(avg_danceability, 3) as avg_danceability,
    ROUND(avg_valence, 3) as avg_valence,
    ROUND(avg_popularity - prev_year_popularity, 2) as popularity_change,
    ROUND(avg_energy - prev_year_energy, 3) as energy_change,
    CASE 
        WHEN avg_popularity > prev_year_popularity THEN 'Increasing'
        WHEN avg_popularity < prev_year_popularity THEN 'Decreasing'
        ELSE 'Stable'
    END as popularity_trend
FROM genre_evolution
WHERE prev_year_popularity IS NOT NULL
ORDER BY playlist_genre, release_year;

-- 3. Artist Diversity Analysis
WITH artist_diversity AS (
    SELECT 
        track_artist,
        COUNT(DISTINCT playlist_genre) as genre_count,
        COUNT(DISTINCT release_year) as year_span,
        COUNT(*) as total_tracks,
        AVG(track_popularity) as avg_popularity,
        STDDEV(track_popularity) as popularity_variability,
        AVG(energy) as avg_energy,
        STDDEV(energy) as energy_variability,
        AVG(danceability) as avg_danceability,
        STDDEV(danceability) as danceability_variability
    FROM spotify_clean
    WHERE track_artist IS NOT NULL
    GROUP BY track_artist
    HAVING COUNT(*) >= 3
),
diversity_rankings AS (
    SELECT 
        *,
        RANK() OVER (ORDER BY genre_count DESC) as genre_diversity_rank,
        RANK() OVER (ORDER BY year_span DESC) as longevity_rank,
        RANK() OVER (ORDER BY popularity_variability DESC) as variability_rank
    FROM artist_diversity
)
SELECT 
    track_artist,
    genre_count,
    year_span,
    total_tracks,
    ROUND(avg_popularity, 2) as avg_popularity,
    ROUND(popularity_variability, 2) as popularity_variability,
    ROUND(avg_energy, 3) as avg_energy,
    ROUND(energy_variability, 3) as energy_variability,
    ROUND(avg_danceability, 3) as avg_danceability,
    ROUND(danceability_variability, 3) as danceability_variability,
    genre_diversity_rank,
    longevity_rank,
    variability_rank,
    CASE 
        WHEN genre_count >= 3 AND year_span >= 5 THEN 'Versatile & Long-lasting'
        WHEN genre_count >= 3 THEN 'Versatile'
        WHEN year_span >= 5 THEN 'Long-lasting'
        ELSE 'Specialized'
    END as artist_type
FROM diversity_rankings
WHERE genre_diversity_rank <= 20 OR longevity_rank <= 20
ORDER BY genre_count DESC, year_span DESC;

-- 4. Seasonal Analysis (by release month)
WITH seasonal_analysis AS (
    SELECT 
        CASE 
            WHEN CAST(SUBSTR(track_album_release_date, 6, 2) AS INTEGER) IN (12, 1, 2) THEN 'Winter'
            WHEN CAST(SUBSTR(track_album_release_date, 6, 2) AS INTEGER) IN (3, 4, 5) THEN 'Spring'
            WHEN CAST(SUBSTR(track_album_release_date, 6, 2) AS INTEGER) IN (6, 7, 8) THEN 'Summer'
            WHEN CAST(SUBSTR(track_album_release_date, 6, 2) AS INTEGER) IN (9, 10, 11) THEN 'Fall'
            ELSE 'Unknown'
        END as season,
        COUNT(*) as track_count,
        AVG(track_popularity) as avg_popularity,
        AVG(energy) as avg_energy,
        AVG(danceability) as avg_danceability,
        AVG(valence) as avg_valence,
        AVG(tempo) as avg_tempo
    FROM spotify_clean
    WHERE track_album_release_date IS NOT NULL
        AND track_album_release_date != ''
    GROUP BY 
        CASE 
            WHEN CAST(SUBSTR(track_album_release_date, 6, 2) AS INTEGER) IN (12, 1, 2) THEN 'Winter'
            WHEN CAST(SUBSTR(track_album_release_date, 6, 2) AS INTEGER) IN (3, 4, 5) THEN 'Spring'
            WHEN CAST(SUBSTR(track_album_release_date, 6, 2) AS INTEGER) IN (6, 7, 8) THEN 'Summer'
            WHEN CAST(SUBSTR(track_album_release_date, 6, 2) AS INTEGER) IN (9, 10, 11) THEN 'Fall'
            ELSE 'Unknown'
        END
)
SELECT 
    season,
    track_count,
    ROUND(avg_popularity, 2) as avg_popularity,
    ROUND(avg_energy, 3) as avg_energy,
    ROUND(avg_danceability, 3) as avg_danceability,
    ROUND(avg_valence, 3) as avg_valence,
    ROUND(avg_tempo, 1) as avg_tempo,
    ROUND((track_count * 100.0) / (SELECT COUNT(*) FROM spotify_clean), 2) as percentage_of_total
FROM seasonal_analysis
WHERE season != 'Unknown'
ORDER BY 
    CASE season
        WHEN 'Spring' THEN 1
        WHEN 'Summer' THEN 2
        WHEN 'Fall' THEN 3
        WHEN 'Winter' THEN 4
    END;

-- 5. Advanced Feature Clustering
WITH feature_clusters AS (
    SELECT 
        track_id,
        track_name,
        track_artist,
        playlist_genre,
        track_popularity,
        energy,
        danceability,
        valence,
        tempo,
        -- Create feature-based clusters
        CASE 
            WHEN energy > 0.8 AND danceability > 0.8 THEN 'High Energy & Danceable'
            WHEN energy > 0.8 AND valence > 0.8 THEN 'High Energy & Positive'
            WHEN danceability > 0.8 AND valence > 0.8 THEN 'Danceable & Positive'
            WHEN energy > 0.8 THEN 'High Energy'
            WHEN danceability > 0.8 THEN 'High Danceability'
            WHEN valence > 0.8 THEN 'High Positivity'
            WHEN energy < 0.3 AND danceability < 0.3 THEN 'Low Energy & Low Dance'
            WHEN valence < 0.3 THEN 'Low Positivity'
            ELSE 'Balanced'
        END as feature_cluster,
        -- Calculate distance from ideal points
        SQRT(POWER(energy - 1, 2) + POWER(danceability - 1, 2) + POWER(valence - 1, 2)) as distance_from_ideal
    FROM spotify_clean
    WHERE energy IS NOT NULL AND danceability IS NOT NULL AND valence IS NOT NULL
),
cluster_stats AS (
    SELECT 
        feature_cluster,
        COUNT(*) as cluster_size,
        AVG(track_popularity) as avg_popularity,
        AVG(energy) as avg_energy,
        AVG(danceability) as avg_danceability,
        AVG(valence) as avg_valence,
        AVG(tempo) as avg_tempo,
        AVG(distance_from_ideal) as avg_distance_from_ideal,
        STDDEV(track_popularity) as popularity_variability
    FROM feature_clusters
    GROUP BY feature_cluster
)
SELECT 
    feature_cluster,
    cluster_size,
    ROUND(avg_popularity, 2) as avg_popularity,
    ROUND(avg_energy, 3) as avg_energy,
    ROUND(avg_danceability, 3) as avg_danceability,
    ROUND(avg_valence, 3) as avg_valence,
    ROUND(avg_tempo, 1) as avg_tempo,
    ROUND(avg_distance_from_ideal, 3) as avg_distance_from_ideal,
    ROUND(popularity_variability, 2) as popularity_variability,
    ROUND((cluster_size * 100.0) / (SELECT COUNT(*) FROM feature_clusters), 2) as percentage_of_total
FROM cluster_stats
ORDER BY cluster_size DESC;

-- 6. Cross-Genre Similarity Analysis
WITH genre_centroids AS (
    SELECT 
        playlist_genre,
        AVG(energy) as centroid_energy,
        AVG(danceability) as centroid_danceability,
        AVG(valence) as centroid_valence,
        AVG(tempo) as centroid_tempo
    FROM spotify_clean
    WHERE playlist_genre IS NOT NULL
    GROUP BY playlist_genre
),
genre_similarity AS (
    SELECT 
        g1.playlist_genre as genre1,
        g2.playlist_genre as genre2,
        SQRT(
            POWER(g1.centroid_energy - g2.centroid_energy, 2) +
            POWER(g1.centroid_danceability - g2.centroid_danceability, 2) +
            POWER(g1.centroid_valence - g2.centroid_valence, 2) +
            POWER((g1.centroid_tempo - g2.centroid_tempo) / 200, 2)
        ) as similarity_distance
    FROM genre_centroids g1
    CROSS JOIN genre_centroids g2
    WHERE g1.playlist_genre < g2.playlist_genre
)
SELECT 
    genre1,
    genre2,
    ROUND(similarity_distance, 4) as similarity_distance,
    CASE 
        WHEN similarity_distance < 0.1 THEN 'Very Similar'
        WHEN similarity_distance < 0.2 THEN 'Similar'
        WHEN similarity_distance < 0.3 THEN 'Moderately Similar'
        WHEN similarity_distance < 0.4 THEN 'Different'
        ELSE 'Very Different'
    END as similarity_level
FROM genre_similarity
ORDER BY similarity_distance ASC
LIMIT 20; 