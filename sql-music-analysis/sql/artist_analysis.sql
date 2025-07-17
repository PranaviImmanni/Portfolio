-- Top selling artists by total album sales
SELECT 
    a.artist_name,
    SUM(al.sales_millions) as total_sales_millions
FROM artists a
JOIN albums al ON a.artist_id = al.artist_id
GROUP BY a.artist_id, a.artist_name
ORDER BY total_sales_millions DESC;

-- Artist debut year analysis
SELECT 
    a.debut_year,
    COUNT(DISTINCT a.artist_id) as new_artists,
    AVG(al.sales_millions) as avg_sales
FROM artists a
LEFT JOIN albums al ON a.artist_id = al.artist_id
GROUP BY a.debut_year
ORDER BY a.debut_year;

-- Country-wise artist performance
SELECT 
    a.country,
    COUNT(DISTINCT a.artist_id) as artist_count,
    SUM(al.sales_millions) as total_sales
FROM artists a
LEFT JOIN albums al ON a.artist_id = al.artist_id
GROUP BY a.country
ORDER BY total_sales DESC; 