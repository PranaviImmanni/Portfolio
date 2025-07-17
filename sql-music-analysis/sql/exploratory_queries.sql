-- Exploratory Queries for Spotify Music Analysis

-- Example: List all albums and their artists
SELECT al.album_name, a.artist_name
FROM albums al
JOIN artists a ON al.artist_id = a.artist_id; 