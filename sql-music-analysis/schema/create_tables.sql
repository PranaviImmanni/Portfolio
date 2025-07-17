-- Table schema for Spotify Music Analysis

CREATE TABLE artists (
    artist_id INT PRIMARY KEY,
    artist_name VARCHAR(100),
    genre VARCHAR(50),
    country VARCHAR(50),
    debut_year INT
);

CREATE TABLE albums (
    album_id INT PRIMARY KEY,
    artist_id INT,
    album_name VARCHAR(100),
    release_year INT,
    sales_millions DECIMAL(5,2),
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id)
);

CREATE TABLE songs (
    song_id INT PRIMARY KEY,
    album_id INT,
    song_name VARCHAR(100),
    duration_seconds INT,
    chart_position INT,
    FOREIGN KEY (album_id) REFERENCES albums(album_id)
); 