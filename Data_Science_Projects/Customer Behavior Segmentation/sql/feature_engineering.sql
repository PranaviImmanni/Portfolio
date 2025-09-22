-- Feature Engineering SQL Script
-- Customer Behavior Segmentation - RFM Analysis
-- This script creates all necessary views for Power BI integration

-- =====================================================
-- RFM METRICS CALCULATION
-- =====================================================

-- RFM View: Complete RFM metrics for all customers
CREATE OR REPLACE VIEW RFM_View AS
SELECT 
    CustomerID,
    DATEDIFF(CURDATE(), MAX(Date)) AS Recency,
    COUNT(*) AS Frequency,
    SUM(TransactionAmount) AS Monetary,
    AVG(TransactionAmount) AS AvgTransactionAmount,
    MAX(Date) AS LastTransactionDate,
    MIN(Date) AS FirstTransactionDate,
    COUNT(DISTINCT Date) AS UniqueDays,
    COUNT(DISTINCT Category) AS CategoryDiversity,
    COUNT(DISTINCT MerchantName) AS MerchantDiversity
FROM Transactions
GROUP BY CustomerID;

-- =====================================================
-- DEMOGRAPHIC ANALYSIS
-- =====================================================

-- Demographics View: Age and gender analysis
CREATE OR REPLACE VIEW Demographics_View AS
SELECT 
    CustomerID,
    Name,
    Surname,
    Gender,
    Birthdate,
    DATEDIFF(CURDATE(), Birthdate) / 365.25 AS Age,
    CASE 
        WHEN DATEDIFF(CURDATE(), Birthdate) / 365.25 < 25 THEN 'Gen Z'
        WHEN DATEDIFF(CURDATE(), Birthdate) / 365.25 BETWEEN 25 AND 40 THEN 'Millennials'
        WHEN DATEDIFF(CURDATE(), Birthdate) / 365.25 BETWEEN 41 AND 55 THEN 'Gen X'
        WHEN DATEDIFF(CURDATE(), Birthdate) / 365.25 >= 56 THEN 'Boomers'
        ELSE 'Unknown'
    END AS AgeGroup,
    CASE 
        WHEN DATEDIFF(CURDATE(), Birthdate) / 365.25 < 25 THEN 1
        WHEN DATEDIFF(CURDATE(), Birthdate) / 365.25 BETWEEN 25 AND 40 THEN 2
        WHEN DATEDIFF(CURDATE(), Birthdate) / 365.25 BETWEEN 41 AND 55 THEN 3
        WHEN DATEDIFF(CURDATE(), Birthdate) / 365.25 >= 56 THEN 4
        ELSE 0
    END AS AgeGroupCode
FROM Transactions
GROUP BY CustomerID, Name, Surname, Gender, Birthdate;

-- =====================================================
-- CATEGORY PREFERENCES
-- =====================================================

-- Category View: Category preferences and spending
CREATE OR REPLACE VIEW Category_View AS
SELECT 
    CustomerID,
    Category,
    COUNT(*) AS Purchases,
    SUM(TransactionAmount) AS TotalSpent,
    AVG(TransactionAmount) AS AvgSpent,
    MIN(TransactionAmount) AS MinSpent,
    MAX(TransactionAmount) AS MaxSpent,
    COUNT(DISTINCT MerchantName) AS UniqueMerchants,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY CustomerID), 2) AS CategoryPercentage
FROM Transactions
GROUP BY CustomerID, Category;

-- Top Categories per Customer
CREATE OR REPLACE VIEW Top_Categories_View AS
SELECT 
    CustomerID,
    Category,
    TotalSpent,
    Purchases,
    ROW_NUMBER() OVER (PARTITION BY CustomerID ORDER BY TotalSpent DESC) AS CategoryRank
FROM Category_View;

-- =====================================================
-- MERCHANT LOYALTY
-- =====================================================

-- Merchant View: Merchant loyalty and spending
CREATE OR REPLACE VIEW Merchant_View AS
SELECT 
    CustomerID,
    MerchantName,
    COUNT(*) AS Visits,
    SUM(TransactionAmount) AS TotalSpent,
    AVG(TransactionAmount) AS AvgSpent,
    MIN(TransactionAmount) AS MinSpent,
    MAX(TransactionAmount) AS MaxSpent,
    COUNT(DISTINCT Category) AS CategoryDiversity,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY CustomerID), 2) AS MerchantPercentage
FROM Transactions
GROUP BY CustomerID, MerchantName;

-- Top Merchants per Customer
CREATE OR REPLACE VIEW Top_Merchants_View AS
SELECT 
    CustomerID,
    MerchantName,
    TotalSpent,
    Visits,
    ROW_NUMBER() OVER (PARTITION BY CustomerID ORDER BY TotalSpent DESC) AS MerchantRank
FROM Merchant_View;

-- =====================================================
-- RFM SCORING SYSTEM
-- =====================================================

-- RFM Scores: Assign scores 1-5 for each metric
CREATE OR REPLACE VIEW RFM_Scores AS
SELECT 
    CustomerID,
    Recency,
    Frequency,
    Monetary,
    -- Recency Score (1-5, higher is better)
    CASE 
        WHEN Recency <= 30 THEN 5
        WHEN Recency <= 60 THEN 4
        WHEN Recency <= 90 THEN 3
        WHEN Recency <= 180 THEN 2
        ELSE 1
    END AS RecencyScore,
    -- Frequency Score (1-5, higher is better)
    CASE 
        WHEN Frequency >= 20 THEN 5
        WHEN Frequency >= 15 THEN 4
        WHEN Frequency >= 10 THEN 3
        WHEN Frequency >= 5 THEN 2
        ELSE 1
    END AS FrequencyScore,
    -- Monetary Score (1-5, higher is better)
    CASE 
        WHEN Monetary >= 5000 THEN 5
        WHEN Monetary >= 3000 THEN 4
        WHEN Monetary >= 1500 THEN 3
        WHEN Monetary >= 500 THEN 2
        ELSE 1
    END AS MonetaryScore
FROM RFM_View;

-- =====================================================
-- CUSTOMER SEGMENTATION
-- =====================================================

-- Customer Segments: 11 distinct segments based on RFM scores
CREATE OR REPLACE VIEW Customer_Segments AS
SELECT 
    rs.CustomerID,
    rs.Recency,
    rs.Frequency,
    rs.Monetary,
    rs.RecencyScore,
    rs.FrequencyScore,
    rs.MonetaryScore,
    CONCAT(rs.RecencyScore, rs.FrequencyScore, rs.MonetaryScore) AS RFM_Score,
    CASE 
        -- Champions: High R, F, M (555, 554, 544)
        WHEN rs.RecencyScore >= 4 AND rs.FrequencyScore >= 4 AND rs.MonetaryScore >= 4 THEN 'Champions'
        
        -- Loyal Customers: Good R, F, M (444, 443, 442)
        WHEN rs.RecencyScore >= 3 AND rs.FrequencyScore >= 3 AND rs.MonetaryScore >= 3 THEN 'Loyal Customers'
        
        -- Potential Loyalists: High R, low F, M (544, 543, 542)
        WHEN rs.RecencyScore >= 4 AND rs.FrequencyScore <= 2 AND rs.MonetaryScore >= 2 THEN 'Potential Loyalists'
        
        -- New Customers: High R only (5XX)
        WHEN rs.RecencyScore >= 4 AND rs.FrequencyScore <= 2 AND rs.MonetaryScore <= 2 THEN 'New Customers'
        
        -- Promising: Good R, F, low M (544, 543, 542)
        WHEN rs.RecencyScore >= 3 AND rs.FrequencyScore >= 2 AND rs.MonetaryScore <= 2 THEN 'Promising'
        
        -- Need Attention: Low R, good F, M (344, 343, 342)
        WHEN rs.RecencyScore <= 2 AND rs.FrequencyScore >= 3 AND rs.MonetaryScore >= 3 THEN 'Need Attention'
        
        -- About to Sleep: Low R, F, good M (244, 243, 242)
        WHEN rs.RecencyScore <= 2 AND rs.FrequencyScore >= 2 AND rs.MonetaryScore >= 2 THEN 'About to Sleep'
        
        -- At Risk: Low R, good M (144, 143, 142)
        WHEN rs.RecencyScore <= 2 AND rs.FrequencyScore <= 2 AND rs.MonetaryScore >= 3 THEN 'At Risk'
        
        -- Cannot Lose Them: Very low R, F, high M (144, 143, 142)
        WHEN rs.RecencyScore <= 1 AND rs.FrequencyScore <= 2 AND rs.MonetaryScore >= 4 THEN 'Cannot Lose Them'
        
        -- Lost: Low R, F, M (111, 112, 113)
        WHEN rs.RecencyScore <= 1 AND rs.FrequencyScore <= 1 AND rs.MonetaryScore <= 1 THEN 'Lost'
        
        -- Others: Mixed patterns
        ELSE 'Others'
    END AS CustomerSegment,
    -- Segment Priority (1=Highest, 5=Lowest)
    CASE 
        WHEN rs.RecencyScore >= 4 AND rs.FrequencyScore >= 4 AND rs.MonetaryScore >= 4 THEN 1
        WHEN rs.RecencyScore >= 3 AND rs.FrequencyScore >= 3 AND rs.MonetaryScore >= 3 THEN 2
        WHEN rs.RecencyScore <= 2 AND rs.FrequencyScore <= 2 AND rs.MonetaryScore >= 3 THEN 3
        WHEN rs.RecencyScore >= 4 AND rs.FrequencyScore <= 2 AND rs.MonetaryScore >= 2 THEN 4
        ELSE 5
    END AS SegmentPriority
FROM RFM_Scores rs;

-- =====================================================
-- COMPREHENSIVE CUSTOMER ANALYSIS
-- =====================================================

-- Customer Analysis: Complete customer profile with all metrics
CREATE OR REPLACE VIEW Customer_Analysis AS
SELECT 
    cs.CustomerID,
    d.Name,
    d.Surname,
    d.Gender,
    d.Age,
    d.AgeGroup,
    d.AgeGroupCode,
    cs.Recency,
    cs.Frequency,
    cs.Monetary,
    cs.RecencyScore,
    cs.FrequencyScore,
    cs.MonetaryScore,
    cs.RFM_Score,
    cs.CustomerSegment,
    cs.SegmentPriority,
    r.LastTransactionDate,
    r.FirstTransactionDate,
    r.AvgTransactionAmount,
    r.UniqueDays,
    r.CategoryDiversity,
    r.MerchantDiversity,
    -- Customer Value Tier
    CASE 
        WHEN cs.Monetary >= 5000 THEN 'High Value'
        WHEN cs.Monetary >= 2000 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS ValueTier,
    -- Customer Lifecycle Stage
    CASE 
        WHEN cs.Recency <= 30 AND cs.Frequency >= 10 THEN 'Active'
        WHEN cs.Recency <= 60 AND cs.Frequency >= 5 THEN 'Engaged'
        WHEN cs.Recency <= 180 AND cs.Frequency >= 3 THEN 'At Risk'
        ELSE 'Inactive'
    END AS LifecycleStage
FROM Customer_Segments cs
JOIN Demographics_View d ON cs.CustomerID = d.CustomerID
JOIN RFM_View r ON cs.CustomerID = r.CustomerID;

-- =====================================================
-- SEGMENT SUMMARY STATISTICS
-- =====================================================

-- Segment Summary: Statistics for each segment
CREATE OR REPLACE VIEW Segment_Summary AS
SELECT 
    CustomerSegment,
    COUNT(*) AS CustomerCount,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Customer_Segments), 2) AS Percentage,
    ROUND(AVG(Monetary), 2) AS AvgMonetary,
    ROUND(AVG(Frequency), 2) AS AvgFrequency,
    ROUND(AVG(Recency), 2) AS AvgRecency,
    ROUND(SUM(Monetary), 2) AS TotalRevenue,
    ROUND(AVG(AvgTransactionAmount), 2) AS AvgTransactionValue,
    ROUND(AVG(CategoryDiversity), 2) AS AvgCategoryDiversity,
    ROUND(AVG(MerchantDiversity), 2) AS AvgMerchantDiversity
FROM Customer_Analysis
GROUP BY CustomerSegment
ORDER BY CustomerCount DESC;

-- =====================================================
-- POWER BI OPTIMIZED VIEWS
-- =====================================================

-- Power BI Main View: Optimized for Power BI performance
CREATE OR REPLACE VIEW PowerBI_Main AS
SELECT 
    CustomerID,
    Name,
    Surname,
    Gender,
    Age,
    AgeGroup,
    CustomerSegment,
    Recency,
    Frequency,
    Monetary,
    RFM_Score,
    ValueTier,
    LifecycleStage,
    LastTransactionDate,
    FirstTransactionDate,
    AvgTransactionAmount
FROM Customer_Analysis;

-- Power BI Category Analysis: Category preferences by segment
CREATE OR REPLACE VIEW PowerBI_Category_Analysis AS
SELECT 
    ca.CustomerSegment,
    cv.Category,
    COUNT(DISTINCT cv.CustomerID) AS CustomerCount,
    SUM(cv.Purchases) AS TotalPurchases,
    ROUND(SUM(cv.TotalSpent), 2) AS TotalSpent,
    ROUND(AVG(cv.AvgSpent), 2) AS AvgSpentPerTransaction,
    ROUND(SUM(cv.TotalSpent) / COUNT(DISTINCT cv.CustomerID), 2) AS RevenuePerCustomer
FROM Customer_Analysis ca
JOIN Category_View cv ON ca.CustomerID = cv.CustomerID
GROUP BY ca.CustomerSegment, cv.Category
ORDER BY ca.CustomerSegment, TotalSpent DESC;

-- Power BI Merchant Analysis: Merchant loyalty by segment
CREATE OR REPLACE VIEW PowerBI_Merchant_Analysis AS
SELECT 
    ca.CustomerSegment,
    mv.MerchantName,
    COUNT(DISTINCT mv.CustomerID) AS CustomerCount,
    SUM(mv.Visits) AS TotalVisits,
    ROUND(SUM(mv.TotalSpent), 2) AS TotalSpent,
    ROUND(AVG(mv.AvgSpent), 2) AS AvgSpentPerVisit,
    ROUND(SUM(mv.TotalSpent) / COUNT(DISTINCT mv.CustomerID), 2) AS RevenuePerCustomer
FROM Customer_Analysis ca
JOIN Merchant_View mv ON ca.CustomerID = mv.CustomerID
GROUP BY ca.CustomerSegment, mv.MerchantName
ORDER BY ca.CustomerSegment, TotalSpent DESC;
