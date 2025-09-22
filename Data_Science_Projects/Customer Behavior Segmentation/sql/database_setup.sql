-- Customer Behavior Segmentation Database Setup
-- MySQL Database Schema for Customer Transaction Analysis

-- Create database
CREATE DATABASE IF NOT EXISTS customer_segmentation;
USE customer_segmentation;

-- Create main transactions table
CREATE TABLE IF NOT EXISTS Transactions (
    CustomerID INT NOT NULL,
    Name VARCHAR(100),
    Surname VARCHAR(100),
    Gender CHAR(1),
    Birthdate DATE,
    TransactionAmount DECIMAL(10,2) NOT NULL,
    Date DATE NOT NULL,
    MerchantName VARCHAR(100),
    Category VARCHAR(50),
    TransactionID INT AUTO_INCREMENT PRIMARY KEY,
    INDEX idx_customer (CustomerID),
    INDEX idx_date (Date),
    INDEX idx_amount (TransactionAmount),
    INDEX idx_category (Category),
    INDEX idx_merchant (MerchantName)
);

-- Data validation constraints
ALTER TABLE Transactions 
ADD CONSTRAINT chk_amount_positive CHECK (TransactionAmount > 0),
ADD CONSTRAINT chk_date_valid CHECK (Date IS NOT NULL),
ADD CONSTRAINT chk_customer_not_null CHECK (CustomerID IS NOT NULL);

-- Create RFM View
CREATE OR REPLACE VIEW RFM_View AS
SELECT 
    CustomerID,
    DATEDIFF(CURDATE(), MAX(Date)) AS Recency,
    COUNT(*) AS Frequency,
    SUM(TransactionAmount) AS Monetary,
    AVG(TransactionAmount) AS AvgTransactionAmount,
    MAX(Date) AS LastTransactionDate,
    MIN(Date) AS FirstTransactionDate
FROM Transactions
GROUP BY CustomerID;

-- Create Demographics View
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
    END AS AgeGroup
FROM Transactions
GROUP BY CustomerID, Name, Surname, Gender, Birthdate;

-- Create Category Preferences View
CREATE OR REPLACE VIEW Category_View AS
SELECT 
    CustomerID,
    Category,
    COUNT(*) AS Purchases,
    SUM(TransactionAmount) AS TotalSpent,
    AVG(TransactionAmount) AS AvgSpent
FROM Transactions
GROUP BY CustomerID, Category;

-- Create Merchant Loyalty View
CREATE OR REPLACE VIEW Merchant_View AS
SELECT 
    CustomerID,
    MerchantName,
    COUNT(*) AS Visits,
    SUM(TransactionAmount) AS TotalSpent,
    AVG(TransactionAmount) AS AvgSpent
FROM Transactions
GROUP BY CustomerID, MerchantName;

-- Create RFM Segmentation View
CREATE OR REPLACE VIEW RFM_Segmentation AS
SELECT 
    r.CustomerID,
    r.Recency,
    r.Frequency,
    r.Monetary,
    -- RFM Scores (1-5 scale)
    CASE 
        WHEN r.Recency <= 30 THEN 5
        WHEN r.Recency <= 60 THEN 4
        WHEN r.Recency <= 90 THEN 3
        WHEN r.Recency <= 180 THEN 2
        ELSE 1
    END AS RecencyScore,
    CASE 
        WHEN r.Frequency >= 20 THEN 5
        WHEN r.Frequency >= 15 THEN 4
        WHEN r.Frequency >= 10 THEN 3
        WHEN r.Frequency >= 5 THEN 2
        ELSE 1
    END AS FrequencyScore,
    CASE 
        WHEN r.Monetary >= 5000 THEN 5
        WHEN r.Monetary >= 3000 THEN 4
        WHEN r.Monetary >= 1500 THEN 3
        WHEN r.Monetary >= 500 THEN 2
        ELSE 1
    END AS MonetaryScore
FROM RFM_View r;

-- Create Customer Segments View
CREATE OR REPLACE VIEW Customer_Segments AS
SELECT 
    s.CustomerID,
    s.Recency,
    s.Frequency,
    s.Monetary,
    s.RecencyScore,
    s.FrequencyScore,
    s.MonetaryScore,
    CONCAT(s.RecencyScore, s.FrequencyScore, s.MonetaryScore) AS RFM_Score,
    CASE 
        WHEN s.RecencyScore >= 4 AND s.FrequencyScore >= 4 AND s.MonetaryScore >= 4 THEN 'Champions'
        WHEN s.RecencyScore >= 3 AND s.FrequencyScore >= 3 AND s.MonetaryScore >= 3 THEN 'Loyal Customers'
        WHEN s.RecencyScore >= 4 AND s.FrequencyScore >= 2 AND s.MonetaryScore >= 2 THEN 'Potential Loyalists'
        WHEN s.RecencyScore >= 4 AND s.FrequencyScore <= 2 AND s.MonetaryScore <= 2 THEN 'New Customers'
        WHEN s.RecencyScore >= 3 AND s.FrequencyScore >= 2 AND s.MonetaryScore >= 3 THEN 'Promising'
        WHEN s.RecencyScore <= 2 AND s.FrequencyScore >= 3 AND s.MonetaryScore >= 3 THEN 'Need Attention'
        WHEN s.RecencyScore <= 2 AND s.FrequencyScore >= 2 AND s.MonetaryScore >= 2 THEN 'About to Sleep'
        WHEN s.RecencyScore <= 2 AND s.FrequencyScore <= 2 AND s.MonetaryScore >= 3 THEN 'At Risk'
        WHEN s.RecencyScore <= 1 AND s.FrequencyScore <= 2 AND s.MonetaryScore <= 2 THEN 'Cannot Lose Them'
        WHEN s.RecencyScore <= 1 AND s.FrequencyScore <= 1 AND s.MonetaryScore <= 1 THEN 'Lost'
        ELSE 'Others'
    END AS CustomerSegment
FROM RFM_Segmentation s;

-- Create comprehensive customer analysis view
CREATE OR REPLACE VIEW Customer_Analysis AS
SELECT 
    cs.CustomerID,
    d.Name,
    d.Surname,
    d.Gender,
    d.Age,
    d.AgeGroup,
    cs.Recency,
    cs.Frequency,
    cs.Monetary,
    cs.RecencyScore,
    cs.FrequencyScore,
    cs.MonetaryScore,
    cs.RFM_Score,
    cs.CustomerSegment,
    r.LastTransactionDate,
    r.FirstTransactionDate,
    r.AvgTransactionAmount
FROM Customer_Segments cs
JOIN Demographics_View d ON cs.CustomerID = d.CustomerID
JOIN RFM_View r ON cs.CustomerID = r.CustomerID;

-- Create segment summary view for Power BI
CREATE OR REPLACE VIEW Segment_Summary AS
SELECT 
    CustomerSegment,
    COUNT(*) AS CustomerCount,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Customer_Segments), 2) AS Percentage,
    ROUND(AVG(Monetary), 2) AS AvgMonetary,
    ROUND(AVG(Frequency), 2) AS AvgFrequency,
    ROUND(AVG(Recency), 2) AS AvgRecency
FROM Customer_Segments
GROUP BY CustomerSegment
ORDER BY CustomerCount DESC;
