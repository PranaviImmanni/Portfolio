-- Power BI Analysis Queries for Customer Segmentation
-- Use these queries to connect Power BI to MySQL database

-- 1. Customer Segmentation Overview
-- This query provides the main data for Power BI dashboard
SELECT 
    ca.CustomerID,
    ca.Name,
    ca.Surname,
    ca.Gender,
    ca.Age,
    ca.AgeGroup,
    ca.Recency,
    ca.Frequency,
    ca.Monetary,
    ca.RecencyScore,
    ca.FrequencyScore,
    ca.MonetaryScore,
    ca.RFM_Score,
    ca.CustomerSegment,
    ca.LastTransactionDate,
    ca.FirstTransactionDate,
    ca.AvgTransactionAmount
FROM Customer_Analysis ca;

-- 2. Segment Summary for Pie Chart
SELECT 
    CustomerSegment,
    CustomerCount,
    Percentage,
    AvgMonetary,
    AvgFrequency,
    AvgRecency
FROM Segment_Summary
ORDER BY CustomerCount DESC;

-- 3. Demographic Analysis by Segment
SELECT 
    CustomerSegment,
    AgeGroup,
    Gender,
    COUNT(*) AS CustomerCount,
    ROUND(AVG(Age), 2) AS AvgAge,
    ROUND(AVG(Monetary), 2) AS AvgSpending
FROM Customer_Analysis
GROUP BY CustomerSegment, AgeGroup, Gender
ORDER BY CustomerSegment, CustomerCount DESC;

-- 4. Category Preferences by Segment
SELECT 
    cs.CustomerSegment,
    cv.Category,
    COUNT(DISTINCT cv.CustomerID) AS CustomerCount,
    SUM(cv.Purchases) AS TotalPurchases,
    ROUND(SUM(cv.TotalSpent), 2) AS TotalSpent,
    ROUND(AVG(cv.AvgSpent), 2) AS AvgSpentPerTransaction
FROM Customer_Segments cs
JOIN Category_View cv ON cs.CustomerID = cv.CustomerID
GROUP BY cs.CustomerSegment, cv.Category
ORDER BY cs.CustomerSegment, TotalSpent DESC;

-- 5. Merchant Loyalty by Segment
SELECT 
    cs.CustomerSegment,
    mv.MerchantName,
    COUNT(DISTINCT mv.CustomerID) AS CustomerCount,
    SUM(mv.Visits) AS TotalVisits,
    ROUND(SUM(mv.TotalSpent), 2) AS TotalSpent,
    ROUND(AVG(mv.AvgSpent), 2) AS AvgSpentPerVisit
FROM Customer_Segments cs
JOIN Merchant_View mv ON cs.CustomerSegment = cs.CustomerSegment
GROUP BY cs.CustomerSegment, mv.MerchantName
ORDER BY cs.CustomerSegment, TotalSpent DESC;

-- 6. RFM Score Distribution
SELECT 
    RFM_Score,
    CustomerSegment,
    COUNT(*) AS CustomerCount,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Customer_Segments), 2) AS Percentage
FROM Customer_Segments
GROUP BY RFM_Score, CustomerSegment
ORDER BY RFM_Score;

-- 7. Monthly Transaction Trends
SELECT 
    YEAR(Date) AS Year,
    MONTH(Date) AS Month,
    CustomerSegment,
    COUNT(*) AS TransactionCount,
    ROUND(SUM(TransactionAmount), 2) AS TotalAmount,
    ROUND(AVG(TransactionAmount), 2) AS AvgAmount
FROM Transactions t
JOIN Customer_Segments cs ON t.CustomerID = cs.CustomerID
GROUP BY YEAR(Date), MONTH(Date), CustomerSegment
ORDER BY Year, Month, CustomerSegment;

-- 8. Top Customers by Segment
SELECT 
    CustomerSegment,
    CustomerID,
    Name,
    Surname,
    Monetary,
    Frequency,
    Recency,
    RFM_Score
FROM Customer_Analysis
WHERE CustomerSegment IN ('Champions', 'Loyal Customers', 'At Risk')
ORDER BY CustomerSegment, Monetary DESC;

-- 9. Category Performance Analysis
SELECT 
    Category,
    COUNT(DISTINCT CustomerID) AS UniqueCustomers,
    COUNT(*) AS TotalTransactions,
    ROUND(SUM(TransactionAmount), 2) AS TotalRevenue,
    ROUND(AVG(TransactionAmount), 2) AS AvgTransactionValue,
    ROUND(SUM(TransactionAmount) / COUNT(DISTINCT CustomerID), 2) AS RevenuePerCustomer
FROM Transactions
GROUP BY Category
ORDER BY TotalRevenue DESC;

-- 10. Merchant Performance Analysis
SELECT 
    MerchantName,
    COUNT(DISTINCT CustomerID) AS UniqueCustomers,
    COUNT(*) AS TotalTransactions,
    ROUND(SUM(TransactionAmount), 2) AS TotalRevenue,
    ROUND(AVG(TransactionAmount), 2) AS AvgTransactionValue,
    ROUND(SUM(TransactionAmount) / COUNT(DISTINCT CustomerID), 2) AS RevenuePerCustomer
FROM Transactions
GROUP BY MerchantName
ORDER BY TotalRevenue DESC;
