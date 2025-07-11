-- SQL Music Analysis
-- Sample queries demonstrating music industry data analysis

-- Create sample tables
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

-- Sample data insertion
INSERT INTO artists VALUES 
(1, 'Taylor Swift', 'Pop', 'USA', 2006),
(2, 'Drake', 'Hip-Hop', 'Canada', 2006),
(3, 'BTS', 'K-Pop', 'South Korea', 2013),
(4, 'Ed Sheeran', 'Pop', 'UK', 2011);

INSERT INTO albums VALUES 
(1, 1, '1989', 2014, 10.1),
(2, 1, 'Reputation', 2017, 4.5),
(3, 2, 'Scorpion', 2018, 3.9),
(4, 3, 'Map of the Soul: 7', 2020, 4.2);

-- Analysis Queries

-- 1. Top selling artists by total album sales
SELECT 
    a.artist_name,
    SUM(al.sales_millions) as total_sales_millions
FROM artists a
JOIN albums al ON a.artist_id = al.artist_id
GROUP BY a.artist_id, a.artist_name
ORDER BY total_sales_millions DESC;

-- 2. Genre performance analysis
SELECT 
    a.genre,
    COUNT(DISTINCT a.artist_id) as artist_count,
    AVG(al.sales_millions) as avg_album_sales,
    SUM(al.sales_millions) as total_genre_sales
FROM artists a
JOIN albums al ON a.artist_id = al.artist_id
GROUP BY a.genre
ORDER BY total_genre_sales DESC;

-- 3. Year-over-year sales trends
SELECT 
    al.release_year,
    COUNT(al.album_id) as albums_released,
    SUM(al.sales_millions) as total_sales,
    AVG(al.sales_millions) as avg_sales_per_album
FROM albums al
GROUP BY al.release_year
ORDER BY al.release_year;

-- 4. Artist debut year analysis
SELECT 
    a.debut_year,
    COUNT(DISTINCT a.artist_id) as new_artists,
    AVG(al.sales_millions) as avg_sales
FROM artists a
LEFT JOIN albums al ON a.artist_id = al.artist_id
GROUP BY a.debut_year
ORDER BY a.debut_year;

-- 5. Country-wise artist performance
SELECT 
    a.country,
    COUNT(DISTINCT a.artist_id) as artist_count,
    SUM(al.sales_millions) as total_sales
FROM artists a
LEFT JOIN albums al ON a.artist_id = al.artist_id
GROUP BY a.country
ORDER BY total_sales DESC; 