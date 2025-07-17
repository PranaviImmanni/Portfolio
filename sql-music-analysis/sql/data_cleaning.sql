-- Data Cleaning Queries for Spotify Music Analysis

-- Example: Remove duplicate songs
DELETE FROM songs
WHERE song_id NOT IN (
    SELECT MIN(song_id)
    FROM songs
    GROUP BY song_name, album_id
); 