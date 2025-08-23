-- =====================================================
-- SPOTIFY MUSIC ANALYSIS - DATA CLEANING
-- =====================================================
-- This script handles data cleaning and preprocessing
-- for the Spotify music dataset

-- 1. Create a cleaned version of the dataset
CREATE TABLE spotify_clean AS
SELECT 
    track_id,
    track_name,
    track_artist,
    track_album_name,
    track_album_release_date,
    playlist_genre,
    playlist_subgenre,
    track_popularity,
    duration_ms,
    energy,
    danceability,
    valence,
    tempo,
    loudness,
    speechiness,
    acousticness,
    instrumentalness,
    liveness,
    key,
    mode,
    time_signature,
    track_href,
    uri,
    analysis_url,
    playlist_name,
    playlist_id,
    type,
    id
FROM spotify_tracks;

-- 2. Handle missing values in key columns
UPDATE spotify_clean 
SET 
    track_popularity = COALESCE(track_popularity, 0),
    energy = COALESCE(energy, 0.5),
    danceability = COALESCE(danceability, 0.5),
    valence = COALESCE(valence, 0.5),
    tempo = COALESCE(tempo, 120),
    loudness = COALESCE(loudness, -10),
    speechiness = COALESCE(speechiness, 0.05),
    acousticness = COALESCE(acousticness, 0.1),
    instrumentalness = COALESCE(instrumentalness, 0),
    liveness = COALESCE(liveness, 0.1);

-- 3. Convert release date to proper format and extract year
ALTER TABLE spotify_clean ADD COLUMN release_year INTEGER;
UPDATE spotify_clean 
SET release_year = CAST(SUBSTR(track_album_release_date, 1, 4) AS INTEGER)
WHERE track_album_release_date IS NOT NULL;

-- 4. Create decade column for analysis
ALTER TABLE spotify_clean ADD COLUMN decade VARCHAR(10);
UPDATE spotify_clean 
SET decade = 
    CASE 
        WHEN release_year >= 2020 THEN '2020s'
        WHEN release_year >= 2010 THEN '2010s'
        WHEN release_year >= 2000 THEN '2000s'
        WHEN release_year >= 1990 THEN '1990s'
        WHEN release_year >= 1980 THEN '1980s'
        WHEN release_year >= 1970 THEN '1970s'
        WHEN release_year >= 1960 THEN '1960s'
        ELSE 'Pre-1960s'
    END;

-- 5. Create duration in minutes
ALTER TABLE spotify_clean ADD COLUMN duration_minutes DECIMAL(5,2);
UPDATE spotify_clean 
SET duration_minutes = ROUND(duration_ms / 60000.0, 2);

-- 6. Create popularity categories
ALTER TABLE spotify_clean ADD COLUMN popularity_category VARCHAR(20);
UPDATE spotify_clean 
SET popularity_category = 
    CASE 
        WHEN track_popularity >= 80 THEN 'Very Popular'
        WHEN track_popularity >= 60 THEN 'Popular'
        WHEN track_popularity >= 40 THEN 'Moderate'
        WHEN track_popularity >= 20 THEN 'Low'
        ELSE 'Very Low'
    END;

-- 7. Remove duplicate tracks based on track_id
DELETE FROM spotify_clean 
WHERE rowid NOT IN (
    SELECT MIN(rowid) 
    FROM spotify_clean 
    GROUP BY track_id
);

-- 8. Create indexes for better query performance
CREATE INDEX idx_genre ON spotify_clean(playlist_genre);
CREATE INDEX idx_artist ON spotify_clean(track_artist);
CREATE INDEX idx_year ON spotify_clean(release_year);
CREATE INDEX idx_popularity ON spotify_clean(track_popularity);

-- 9. Summary of cleaning operations
SELECT 
    'Data Cleaning Summary' as operation,
    COUNT(*) as total_tracks,
    COUNT(DISTINCT track_artist) as unique_artists,
    COUNT(DISTINCT playlist_genre) as unique_genres,
    COUNT(DISTINCT release_year) as year_span
FROM spotify_clean; 