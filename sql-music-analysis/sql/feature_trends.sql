-- Year-over-year sales trends
SELECT 
    al.release_year,
    COUNT(al.album_id) as albums_released,
    SUM(al.sales_millions) as total_sales,
    AVG(al.sales_millions) as avg_sales_per_album
FROM albums al
GROUP BY al.release_year
ORDER BY al.release_year; 