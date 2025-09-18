-- =====================================================
-- SPOTIFY MUSIC ANALYSIS - FEATURE TRENDS
-- =====================================================
-- This script analyzes trends in audio features over time
-- and identifies patterns in music characteristics

-- 1. Yearly Feature Trends Analysis
WITH yearly_feature_trends AS (
    SELECT 
        release_year,
        COUNT(*) as track_count,
        AVG(track_popularity) as avg_popularity,
        AVG(energy) as avg_energy,
        AVG(danceability) as avg_danceability,
        AVG(valence) as avg_valence,
        AVG(tempo) as avg_tempo,
        AVG(loudness) as avg_loudness,
        AVG(speechiness) as avg_speechiness,
        AVG(acousticness) as avg_acousticness,
        AVG(instrumentalness) as avg_instrumentalness,
        AVG(liveness) as avg_liveness,
        AVG(duration_minutes) as avg_duration
    FROM spotify_clean
    WHERE release_year IS NOT NULL 
        AND release_year >= 1990
    GROUP BY release_year
    HAVING COUNT(*) >= 5  -- Only include years with at least 5 tracks
),
yearly_rankings AS (
    SELECT 
        *,
        RANK() OVER (ORDER BY avg_popularity DESC) as popularity_rank,
        RANK() OVER (ORDER BY avg_energy DESC) as energy_rank,
        RANK() OVER (ORDER BY avg_danceability DESC) as danceability_rank,
        RANK() OVER (ORDER BY avg_valence DESC) as valence_rank
    FROM yearly_feature_trends
)
SELECT 
    release_year,
    track_count,
    ROUND(avg_popularity, 2) as avg_popularity,
    ROUND(avg_energy, 3) as avg_energy,
    ROUND(avg_danceability, 3) as avg_danceability,
    ROUND(avg_valence, 3) as avg_valence,
    ROUND(avg_tempo, 1) as avg_tempo,
    ROUND(avg_loudness, 2) as avg_loudness,
    ROUND(avg_duration, 2) as avg_duration_minutes,
    popularity_rank,
    energy_rank,
    danceability_rank,
    valence_rank
FROM yearly_rankings
ORDER BY release_year;

-- 2. Decade Feature Comparison
WITH decade_feature_analysis AS (
    SELECT 
        decade,
        COUNT(*) as track_count,
        AVG(track_popularity) as avg_popularity,
        AVG(energy) as avg_energy,
        AVG(danceability) as avg_danceability,
        AVG(valence) as avg_valence,
        AVG(tempo) as avg_tempo,
        AVG(loudness) as avg_loudness,
        AVG(speechiness) as avg_speechiness,
        AVG(acousticness) as avg_acousticness,
        AVG(instrumentalness) as avg_instrumentalness,
        AVG(liveness) as avg_liveness,
        AVG(duration_minutes) as avg_duration,
        STDDEV(energy) as energy_variability,
        STDDEV(danceability) as danceability_variability,
        STDDEV(valence) as valence_variability
    FROM spotify_clean
    WHERE decade IS NOT NULL
    GROUP BY decade
)
SELECT 
    decade,
    track_count,
    ROUND(avg_popularity, 2) as avg_popularity,
    ROUND(avg_energy, 3) as avg_energy,
    ROUND(avg_danceability, 3) as avg_danceability,
    ROUND(avg_valence, 3) as avg_valence,
    ROUND(avg_tempo, 1) as avg_tempo,
    ROUND(avg_loudness, 2) as avg_loudness,
    ROUND(avg_duration, 2) as avg_duration_minutes,
    ROUND(energy_variability, 3) as energy_variability,
    ROUND(danceability_variability, 3) as danceability_variability,
    ROUND(valence_variability, 3) as valence_variability,
    CASE 
        WHEN avg_energy > 0.7 AND avg_danceability > 0.7 THEN 'High Energy & Danceable'
        WHEN avg_energy > 0.7 THEN 'High Energy'
        WHEN avg_danceability > 0.7 THEN 'High Danceability'
        WHEN avg_acousticness > 0.7 THEN 'Acoustic'
        WHEN avg_instrumentalness > 0.7 THEN 'Instrumental'
        ELSE 'Balanced'
    END as decade_characteristic
FROM decade_feature_analysis
ORDER BY 
    CASE decade
        WHEN '1960s' THEN 1
        WHEN '1970s' THEN 2
        WHEN '1980s' THEN 3
        WHEN '1990s' THEN 4
        WHEN '2000s' THEN 5
        WHEN '2010s' THEN 6
        WHEN '2020s' THEN 7
        ELSE 8
    END;

-- 3. Feature Correlation Analysis
WITH feature_correlations AS (
    SELECT 
        'Energy vs Danceability' as feature_pair,
        CORR(energy, danceability) as correlation_coefficient
    FROM spotify_clean
    WHERE energy IS NOT NULL AND danceability IS NOT NULL
    
    UNION ALL
    
    SELECT 
        'Energy vs Valence' as feature_pair,
        CORR(energy, valence) as correlation_coefficient
    FROM spotify_clean
    WHERE energy IS NOT NULL AND valence IS NOT NULL
    
    UNION ALL
    
    SELECT 
        'Danceability vs Valence' as feature_pair,
        CORR(danceability, valence) as correlation_coefficient
    FROM spotify_clean
    WHERE danceability IS NOT NULL AND valence IS NOT NULL
    
    UNION ALL
    
    SELECT 
        'Tempo vs Energy' as feature_pair,
        CORR(tempo, energy) as correlation_coefficient
    FROM spotify_clean
    WHERE tempo IS NOT NULL AND energy IS NOT NULL
    
    UNION ALL
    
    SELECT 
        'Loudness vs Energy' as feature_pair,
        CORR(loudness, energy) as correlation_coefficient
    FROM spotify_clean
    WHERE loudness IS NOT NULL AND energy IS NOT NULL
    
    UNION ALL
    
    SELECT 
        'Popularity vs Energy' as feature_pair,
        CORR(track_popularity, energy) as correlation_coefficient
    FROM spotify_clean
    WHERE track_popularity IS NOT NULL AND energy IS NOT NULL
)
SELECT 
    feature_pair,
    ROUND(correlation_coefficient, 4) as correlation_coefficient,
    CASE 
        WHEN ABS(correlation_coefficient) >= 0.7 THEN 'Strong'
        WHEN ABS(correlation_coefficient) >= 0.5 THEN 'Moderate'
        WHEN ABS(correlation_coefficient) >= 0.3 THEN 'Weak'
        ELSE 'Very Weak'
    END as correlation_strength,
    CASE 
        WHEN correlation_coefficient > 0 THEN 'Positive'
        WHEN correlation_coefficient < 0 THEN 'Negative'
        ELSE 'No Correlation'
    END as correlation_direction
FROM feature_correlations
ORDER BY ABS(correlation_coefficient) DESC;

-- 4. Feature Distribution Analysis
WITH feature_quartiles AS (
    SELECT 
        'Energy' as feature_name,
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY energy) as q1,
        PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY energy) as median,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY energy) as q3,
        AVG(energy) as mean,
        STDDEV(energy) as std_dev
    FROM spotify_clean
    WHERE energy IS NOT NULL
    
    UNION ALL
    
    SELECT 
        'Danceability' as feature_name,
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY danceability) as q1,
        PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY danceability) as median,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY danceability) as q3,
        AVG(danceability) as mean,
        STDDEV(danceability) as std_dev
    FROM spotify_clean
    WHERE danceability IS NOT NULL
    
    UNION ALL
    
    SELECT 
        'Valence' as feature_name,
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY valence) as q1,
        PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY valence) as median,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY valence) as q3,
        AVG(valence) as mean,
        STDDEV(valence) as std_dev
    FROM spotify_clean
    WHERE valence IS NOT NULL
    
    UNION ALL
    
    SELECT 
        'Tempo' as feature_name,
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY tempo) as q1,
        PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY tempo) as median,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY tempo) as q3,
        AVG(tempo) as mean,
        STDDEV(tempo) as std_dev
    FROM spotify_clean
    WHERE tempo IS NOT NULL
)
SELECT 
    feature_name,
    ROUND(q1, 3) as q1,
    ROUND(median, 3) as median,
    ROUND(q3, 3) as q3,
    ROUND(mean, 3) as mean,
    ROUND(std_dev, 3) as std_dev,
    ROUND(q3 - q1, 3) as iqr
FROM feature_quartiles
ORDER BY feature_name;

-- 5. Popularity vs Feature Analysis
WITH popularity_feature_analysis AS (
    SELECT 
        popularity_category,
        COUNT(*) as track_count,
        AVG(energy) as avg_energy,
        AVG(danceability) as avg_danceability,
        AVG(valence) as avg_valence,
        AVG(tempo) as avg_tempo,
        AVG(loudness) as avg_loudness,
        AVG(duration_minutes) as avg_duration,
        STDDEV(energy) as energy_variability,
        STDDEV(danceability) as danceability_variability
    FROM spotify_clean
    WHERE popularity_category IS NOT NULL
    GROUP BY popularity_category
)
SELECT 
    popularity_category,
    track_count,
    ROUND(avg_energy, 3) as avg_energy,
    ROUND(avg_danceability, 3) as avg_danceability,
    ROUND(avg_valence, 3) as avg_valence,
    ROUND(avg_tempo, 1) as avg_tempo,
    ROUND(avg_loudness, 2) as avg_loudness,
    ROUND(avg_duration, 2) as avg_duration_minutes,
    ROUND(energy_variability, 3) as energy_variability,
    ROUND(danceability_variability, 3) as danceability_variability,
    ROUND((track_count * 100.0) / (SELECT COUNT(*) FROM spotify_clean), 2) as percentage_of_total
FROM popularity_feature_analysis
ORDER BY 
    CASE popularity_category
        WHEN 'Very Popular' THEN 1
        WHEN 'Popular' THEN 2
        WHEN 'Moderate' THEN 3
        WHEN 'Low' THEN 4
        WHEN 'Very Low' THEN 5
    END; 