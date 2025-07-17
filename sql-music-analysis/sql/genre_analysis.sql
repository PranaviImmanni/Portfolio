-- Genre performance analysis
SELECT 
    a.genre,
    COUNT(DISTINCT a.artist_id) as artist_count,
    AVG(al.sales_millions) as avg_album_sales,
    SUM(al.sales_millions) as total_genre_sales
FROM artists a
JOIN albums al ON a.artist_id = al.artist_id
GROUP BY a.genre
ORDER BY total_genre_sales DESC; 