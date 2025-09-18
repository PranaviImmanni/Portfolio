-- =====================================================
-- Advanced Genre Analysis for Spotify Music Data
-- =====================================================
-- This script provides comprehensive genre analysis using advanced SQL techniques
-- including CTEs, window functions, and statistical analysis for business insights

-- =====================================================
-- 1. GENRE PERFORMANCE OVERVIEW WITH RANKINGS
-- =====================================================

WITH genre_performance AS (
    SELECT 
        unnest(artists.genres) AS genre,
        COUNT(DISTINCT tracks.track_id) AS track_count,
        COUNT(DISTINCT artists.artist_id) AS artist_count,
        AVG(tracks.popularity) AS avg_popularity,
        AVG(tracks.danceability) AS avg_danceability,
        AVG(tracks.energy) AS avg_energy,
        AVG(tracks.valence) AS avg_valence,
        AVG(tracks.acousticness) AS avg_acousticness,
        AVG(tracks.instrumentalness) AS avg_instrumentalness,
        AVG(tracks.liveness) AS avg_liveness,
        AVG(tracks.speechiness) AS avg_speechiness,
        AVG(tracks.tempo) AS avg_tempo,
        SUM(COALESCE(streaming_history.ms_played, 0)) / 60000.0 AS total_minutes_played,
        COUNT(streaming_history.stream_id) AS total_streams
    FROM tracks
    JOIN artists ON tracks.artist_id = artists.artist_id
    LEFT JOIN streaming_history ON tracks.track_id = streaming_history.track_id
    WHERE artists.genres IS NOT NULL
    GROUP BY unnest(artists.genres)
),
genre_rankings AS (
    SELECT 
        genre,
        track_count,
        artist_count,
        ROUND(avg_popularity, 2) AS avg_popularity,
        ROUND(avg_danceability, 3) AS avg_danceability,
        ROUND(avg_energy, 3) AS avg_energy,
        ROUND(avg_valence, 3) AS avg_valence,
        ROUND(avg_acousticness, 3) AS avg_acousticness,
        ROUND(avg_instrumentalness, 3) AS avg_instrumentalness,
        ROUND(avg_liveness, 3) AS avg_liveness,
        ROUND(avg_speechiness, 3) AS avg_speechiness,
        ROUND(avg_tempo, 2) AS avg_tempo,
        ROUND(total_minutes_played, 2) AS total_minutes,
        total_streams,
        -- Multiple ranking dimensions
        RANK() OVER (ORDER BY total_minutes_played DESC) AS popularity_rank,
        RANK() OVER (ORDER BY avg_popularity DESC) AS trend_rank,
        RANK() OVER (ORDER BY track_count DESC) AS catalog_rank,
        RANK() OVER (ORDER BY artist_count DESC) AS diversity_rank,
        RANK() OVER (ORDER BY avg_danceability DESC) AS danceability_rank
    FROM genre_performance
    WHERE track_count >= 5  -- Filter out genres with insufficient data
)
SELECT 
    genre,
    track_count,
    artist_count,
    avg_popularity,
    avg_danceability,
    avg_energy,
    avg_valence,
    avg_acousticness,
    avg_instrumentalness,
    avg_liveness,
    avg_speechiness,
    avg_tempo,
    total_minutes,
    total_streams,
    popularity_rank,
    trend_rank,
    catalog_rank,
    diversity_rank,
    danceability_rank,
    -- Composite score for overall genre performance
    ROUND(
        (popularity_rank + trend_rank + catalog_rank + diversity_rank) / 4.0, 
        2
    ) AS overall_score
FROM genre_rankings
WHERE popularity_rank <= 20  -- Top 20 genres
ORDER BY overall_score;

-- =====================================================
-- 2. GENRE EVOLUTION ANALYSIS BY DECADE
-- =====================================================

WITH genre_decade_analysis AS (
    SELECT 
        unnest(artists.genres) AS genre,
        EXTRACT(DECADE FROM tracks.release_date) AS decade,
        COUNT(DISTINCT tracks.track_id) AS track_count,
        AVG(tracks.popularity) AS avg_popularity,
        AVG(tracks.danceability) AS avg_danceability,
        AVG(tracks.energy) AS avg_energy,
        AVG(tracks.valence) AS avg_valence,
        AVG(tracks.acousticness) AS avg_acousticness,
        AVG(tracks.instrumentalness) AS avg_instrumentalness,
        AVG(tracks.liveness) AS avg_liveness,
        AVG(tracks.speechiness) AS avg_speechiness,
        AVG(tracks.tempo) AS avg_tempo,
        COUNT(DISTINCT artists.artist_id) AS artist_count
    FROM tracks
    JOIN artists ON tracks.artist_id = artists.artist_id
    WHERE tracks.release_date IS NOT NULL 
        AND artists.genres IS NOT NULL
        AND EXTRACT(YEAR FROM tracks.release_date) >= 1960
    GROUP BY unnest(artists.genres), EXTRACT(DECADE FROM tracks.release_date)
),
genre_decade_trends AS (
    SELECT 
        genre,
        decade,
        track_count,
        ROUND(avg_popularity, 2) AS avg_popularity,
        ROUND(avg_danceability, 3) AS avg_danceability,
        ROUND(avg_energy, 3) AS avg_energy,
        ROUND(avg_valence, 3) AS avg_valence,
        ROUND(avg_acousticness, 3) AS avg_acousticness,
        ROUND(avg_instrumentalness, 3) AS avg_instrumentalness,
        ROUND(avg_liveness, 3) AS avg_liveness,
        ROUND(avg_speechiness, 3) AS avg_speechiness,
        ROUND(avg_tempo, 2) AS avg_tempo,
        artist_count,
        -- Calculate trend indicators
        LAG(avg_popularity) OVER (
            PARTITION BY genre 
            ORDER BY decade
        ) AS prev_decade_popularity,
        LAG(avg_danceability) OVER (
            PARTITION BY genre 
            ORDER BY decade
        ) AS prev_decade_danceability,
        LAG(avg_energy) OVER (
            PARTITION BY genre 
            ORDER BY decade
        ) AS prev_decade_energy
    FROM genre_decade_analysis
),
genre_evolution AS (
    SELECT 
        genre,
        decade,
        track_count,
        avg_popularity,
        avg_danceability,
        avg_energy,
        avg_valence,
        avg_acousticness,
        avg_instrumentalness,
        avg_liveness,
        avg_speechiness,
        avg_tempo,
        artist_count,
        -- Calculate evolution metrics
        CASE 
            WHEN prev_decade_popularity IS NOT NULL 
            THEN ROUND(avg_popularity - prev_decade_popularity, 2)
            ELSE 0 
        END AS popularity_change,
        CASE 
            WHEN prev_decade_danceability IS NOT NULL 
            THEN ROUND(avg_danceability - prev_decade_danceability, 3)
            ELSE 0 
        END AS danceability_change,
        CASE 
            WHEN prev_decade_energy IS NOT NULL 
            THEN ROUND(avg_energy - prev_decade_energy, 3)
            ELSE 0 
        END AS energy_change,
        -- Evolution trend classification
        CASE 
            WHEN prev_decade_popularity IS NOT NULL 
            THEN CASE 
                WHEN avg_popularity - prev_decade_popularity > 10 THEN 'Rising Star'
                WHEN avg_popularity - prev_decade_popularity > 5 THEN 'Growing'
                WHEN avg_popularity - prev_decade_popularity > -5 THEN 'Stable'
                WHEN avg_popularity - prev_decade_popularity > -10 THEN 'Declining'
                ELSE 'Fading'
            END
            ELSE 'New Genre'
        END AS evolution_trend
    FROM genre_decade_trends
)
SELECT 
    genre,
    decade,
    track_count,
    avg_popularity,
    avg_danceability,
    avg_energy,
    avg_valence,
    avg_acousticness,
    avg_instrumentalness,
    avg_liveness,
    avg_speechiness,
    avg_tempo,
    artist_count,
    popularity_change,
    danceability_change,
    energy_change,
    evolution_trend
FROM genre_evolution
WHERE track_count >= 3  -- Minimum tracks for meaningful analysis
ORDER BY genre, decade;

-- =====================================================
-- 3. GENRE FEATURE CORRELATION ANALYSIS
-- =====================================================

WITH genre_feature_stats AS (
    SELECT 
        unnest(artists.genres) AS genre,
        -- Calculate feature statistics
        COUNT(tracks.track_id) AS track_count,
        ROUND(AVG(tracks.danceability), 3) AS avg_danceability,
        ROUND(STDDEV(tracks.danceability), 3) AS std_danceability,
        ROUND(AVG(tracks.energy), 3) AS avg_energy,
        ROUND(STDDEV(tracks.energy), 3) AS std_energy,
        ROUND(AVG(tracks.valence), 3) AS avg_valence,
        ROUND(STDDEV(tracks.valence), 3) AS std_valence,
        ROUND(AVG(tracks.acousticness), 3) AS avg_acousticness,
        ROUND(STDDEV(tracks.acousticness), 3) AS std_acousticness,
        ROUND(AVG(tracks.instrumentalness), 3) AS avg_instrumentalness,
        ROUND(STDDEV(tracks.instrumentalness), 3) AS std_instrumentalness,
        ROUND(AVG(tracks.liveness), 3) AS avg_liveness,
        ROUND(STDDEV(tracks.liveness), 3) AS std_liveness,
        ROUND(AVG(tracks.speechiness), 3) AS avg_speechiness,
        ROUND(STDDEV(tracks.speechiness), 3) AS std_speechiness,
        ROUND(AVG(tracks.tempo), 2) AS avg_tempo,
        ROUND(STDDEV(tracks.tempo), 2) AS std_tempo,
        -- Calculate feature consistency (lower std = more consistent)
        ROUND(
            (STDDEV(tracks.danceability) + STDDEV(tracks.energy) + STDDEV(tracks.valence)) / 3.0, 
            3
        ) AS feature_consistency
    FROM tracks
    JOIN artists ON tracks.artist_id = artists.artist_id
    WHERE artists.genres IS NOT NULL
    GROUP BY unnest(artists.genres)
),
genre_feature_analysis AS (
    SELECT 
        genre,
        track_count,
        avg_danceability,
        std_danceability,
        avg_energy,
        std_energy,
        avg_valence,
        std_valence,
        avg_acousticness,
        std_acousticness,
        avg_instrumentalness,
        std_instrumentalness,
        avg_liveness,
        std_liveness,
        avg_speechiness,
        std_speechiness,
        avg_tempo,
        std_tempo,
        feature_consistency,
        -- Feature characteristic identification
        CASE 
            WHEN avg_danceability > 0.7 AND avg_energy > 0.7 THEN 'High Energy Dance'
            WHEN avg_acousticness > 0.7 AND avg_instrumentalness > 0.5 THEN 'Acoustic Instrumental'
            WHEN avg_speechiness > 0.3 THEN 'Speech-Heavy'
            WHEN avg_liveness > 0.6 THEN 'Live Performance'
            WHEN avg_valence > 0.7 THEN 'Positive Mood'
            WHEN avg_valence < 0.3 THEN 'Melancholic'
            ELSE 'Balanced'
        END AS primary_characteristic,
        -- Consistency rating
        CASE 
            WHEN feature_consistency < 0.1 THEN 'Very Consistent'
            WHEN feature_consistency < 0.2 THEN 'Consistent'
            WHEN feature_consistency < 0.3 THEN 'Moderately Consistent'
            WHEN feature_consistency < 0.4 THEN 'Variable'
            ELSE 'Highly Variable'
        END AS consistency_rating
    FROM genre_feature_stats
    WHERE track_count >= 10  -- Sufficient data for analysis
)
SELECT 
    genre,
    track_count,
    primary_characteristic,
    consistency_rating,
    avg_danceability,
    std_danceability,
    avg_energy,
    std_energy,
    avg_valence,
    std_valence,
    avg_acousticness,
    std_acousticness,
    avg_instrumentalness,
    std_instrumentalness,
    avg_liveness,
    std_liveness,
    avg_speechiness,
    std_speechiness,
    avg_tempo,
    std_tempo,
    feature_consistency
FROM genre_feature_analysis
ORDER BY track_count DESC, feature_consistency;

-- =====================================================
-- 4. GENRE POPULARITY TREND ANALYSIS
-- =====================================================

WITH genre_yearly_trends AS (
    SELECT 
        unnest(artists.genres) AS genre,
        EXTRACT(YEAR FROM tracks.release_date) AS release_year,
        COUNT(DISTINCT tracks.track_id) AS track_count,
        AVG(tracks.popularity) AS avg_popularity,
        COUNT(streaming_history.stream_id) AS stream_count,
        SUM(COALESCE(streaming_history.ms_played, 0)) / 60000.0 AS total_minutes
    FROM tracks
    JOIN artists ON tracks.artist_id = artists.artist_id
    LEFT JOIN streaming_history ON tracks.track_id = streaming_history.track_id
    WHERE tracks.release_date IS NOT NULL 
        AND artists.genres IS NOT NULL
        AND EXTRACT(YEAR FROM tracks.release_date) >= 2010
    GROUP BY unnest(artists.genres), EXTRACT(YEAR FROM tracks.release_date)
),
genre_trend_analysis AS (
    SELECT 
        genre,
        release_year,
        track_count,
        ROUND(avg_popularity, 2) AS avg_popularity,
        stream_count,
        ROUND(total_minutes, 2) AS total_minutes,
        -- Calculate year-over-year changes
        LAG(avg_popularity) OVER (
            PARTITION BY genre 
            ORDER BY release_year
        ) AS prev_year_popularity,
        LAG(track_count) OVER (
            PARTITION BY genre 
            ORDER BY release_year
        ) AS prev_year_tracks,
        LAG(total_minutes) OVER (
            PARTITION BY genre 
            ORDER BY release_year
        ) AS prev_year_minutes
    FROM genre_yearly_trends
),
genre_growth_metrics AS (
    SELECT 
        genre,
        release_year,
        track_count,
        avg_popularity,
        stream_count,
        total_minutes,
        -- Growth calculations
        CASE 
            WHEN prev_year_popularity IS NOT NULL 
            THEN ROUND(
                ((avg_popularity - prev_year_popularity) / prev_year_popularity) * 100, 2
            )
            ELSE 0 
        END AS popularity_growth_pct,
        CASE 
            WHEN prev_year_tracks IS NOT NULL 
            THEN ROUND(
                ((track_count - prev_year_tracks) / prev_year_tracks) * 100, 2
            )
            ELSE 0 
        END AS track_growth_pct,
        CASE 
            WHEN prev_year_minutes IS NOT NULL 
            THEN ROUND(
                ((total_minutes - prev_year_minutes) / prev_year_minutes) * 100, 2
            )
            ELSE 0 
        END AS engagement_growth_pct,
        -- Trend classification
        CASE 
            WHEN prev_year_popularity IS NOT NULL 
            THEN CASE 
                WHEN avg_popularity - prev_year_popularity > 15 THEN 'Explosive Growth'
                WHEN avg_popularity - prev_year_popularity > 8 THEN 'Strong Growth'
                WHEN avg_popularity - prev_year_popularity > 3 THEN 'Moderate Growth'
                WHEN avg_popularity - prev_year_popularity > -3 THEN 'Stable'
                WHEN avg_popularity - prev_year_popularity > -8 THEN 'Declining'
                ELSE 'Significant Decline'
            END
            ELSE 'New Trend'
        END AS growth_trend
    FROM genre_trend_analysis
)
SELECT 
    genre,
    release_year,
    track_count,
    avg_popularity,
    stream_count,
    total_minutes,
    popularity_growth_pct,
    track_growth_pct,
    engagement_growth_pct,
    growth_trend
FROM genre_growth_metrics
WHERE track_count >= 2  -- Minimum tracks for trend analysis
ORDER BY genre, release_year DESC;

-- =====================================================
-- 5. GENRE CROSS-ANALYSIS AND INSIGHTS
-- =====================================================

WITH genre_summary AS (
    SELECT 
        unnest(artists.genres) AS genre,
        COUNT(DISTINCT tracks.track_id) AS total_tracks,
        COUNT(DISTINCT artists.artist_id) AS total_artists,
        AVG(tracks.popularity) AS avg_popularity,
        AVG(tracks.danceability) AS avg_danceability,
        AVG(tracks.energy) AS avg_energy,
        AVG(tracks.valence) AS avg_valence,
        AVG(tracks.acousticness) AS avg_acousticness,
        AVG(tracks.instrumentalness) AS avg_instrumentalness,
        AVG(tracks.liveness) AS avg_liveness,
        AVG(tracks.speechiness) AS avg_speechiness,
        AVG(tracks.tempo) AS avg_tempo,
        COUNT(streaming_history.stream_id) AS total_streams,
        SUM(COALESCE(streaming_history.ms_played, 0)) / 60000.0 AS total_minutes
    FROM tracks
    JOIN artists ON tracks.artist_id = artists.artist_id
    LEFT JOIN streaming_history ON tracks.track_id = streaming_history.track_id
    WHERE artists.genres IS NOT NULL
    GROUP BY unnest(artists.genres)
),
genre_insights AS (
    SELECT 
        genre,
        total_tracks,
        total_artists,
        ROUND(avg_popularity, 2) AS avg_popularity,
        ROUND(avg_danceability, 3) AS avg_danceability,
        ROUND(avg_energy, 3) AS avg_energy,
        ROUND(avg_valence, 3) AS avg_valence,
        ROUND(avg_acousticness, 3) AS avg_acousticness,
        ROUND(avg_instrumentalness, 3) AS avg_instrumentalness,
        ROUND(avg_liveness, 3) AS avg_liveness,
        ROUND(avg_speechiness, 3) AS avg_speechiness,
        ROUND(avg_tempo, 2) AS avg_tempo,
        total_streams,
        ROUND(total_minutes, 2) AS total_minutes,
        -- Business insights
        CASE 
            WHEN avg_popularity > 70 AND total_streams > 1000 THEN 'High Potential - Trending'
            WHEN avg_popularity > 60 AND total_streams > 500 THEN 'Growing Market'
            WHEN avg_popularity > 50 THEN 'Established Market'
            WHEN avg_popularity > 40 THEN 'Emerging Market'
            ELSE 'Niche Market'
        END AS market_potential,
        -- Content strategy insights
        CASE 
            WHEN avg_danceability > 0.7 AND avg_energy > 0.7 THEN 'Party/Club Focus'
            WHEN avg_acousticness > 0.7 THEN 'Chill/Relaxation Focus'
            WHEN avg_valence > 0.7 THEN 'Positive/Uplifting Focus'
            WHEN avg_instrumentalness > 0.7 THEN 'Background/Study Focus'
            ELSE 'General Audience'
        END AS content_strategy,
        -- Artist development insights
        CASE 
            WHEN total_artists < 5 THEN 'Oversaturated - High Competition'
            WHEN total_artists < 20 THEN 'Competitive - Strategic Positioning Needed'
            WHEN total_artists < 50 THEN 'Moderate Competition - Growth Opportunity'
            ELSE 'Low Competition - Market Entry Opportunity'
        END AS competition_level
    FROM genre_summary
    WHERE total_tracks >= 5  -- Minimum data for insights
)
SELECT 
    genre,
    total_tracks,
    total_artists,
    avg_popularity,
    avg_danceability,
    avg_energy,
    avg_valence,
    avg_acousticness,
    avg_instrumentalness,
    avg_liveness,
    avg_speechiness,
    avg_tempo,
    total_streams,
    total_minutes,
    market_potential,
    content_strategy,
    competition_level
FROM genre_insights
ORDER BY total_minutes DESC, avg_popularity DESC;

