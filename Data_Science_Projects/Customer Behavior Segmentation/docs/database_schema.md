# Database Schema Documentation

## Overview

The Customer Behavior Segmentation database is designed to support comprehensive RFM analysis with optimal performance for Power BI integration. The schema follows normalized design principles with strategic denormalization for analytical performance.

## Database Structure

### Main Table: Transactions

**Purpose:** Stores all customer transaction data
**Primary Key:** TransactionID (Auto-increment)
**Indexes:** CustomerID, Date, TransactionAmount, Category, MerchantName

```sql
CREATE TABLE Transactions (
    TransactionID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT NOT NULL,
    Name VARCHAR(100),
    Surname VARCHAR(100),
    Gender CHAR(1),
    Birthdate DATE,
    TransactionAmount DECIMAL(10,2) NOT NULL,
    Date DATE NOT NULL,
    MerchantName VARCHAR(100),
    Category VARCHAR(50),
    
    -- Constraints
    CONSTRAINT chk_amount_positive CHECK (TransactionAmount > 0),
    CONSTRAINT chk_date_valid CHECK (Date IS NOT NULL),
    CONSTRAINT chk_customer_not_null CHECK (CustomerID IS NOT NULL),
    
    -- Indexes
    INDEX idx_customer (CustomerID),
    INDEX idx_date (Date),
    INDEX idx_amount (TransactionAmount),
    INDEX idx_category (Category),
    INDEX idx_merchant (MerchantName)
);
```

### Analytical Views

#### 1. RFM_View
**Purpose:** Core RFM metrics calculation
**Key Metrics:**
- Recency (days since last transaction)
- Frequency (total transactions)
- Monetary (total spend)
- Additional metrics (avg transaction, unique days, diversity)

#### 2. Demographics_View
**Purpose:** Customer demographic analysis
**Key Metrics:**
- Age calculation
- Age group classification (Gen Z, Millennials, Gen X, Boomers)
- Gender distribution

#### 3. Category_View
**Purpose:** Category preferences analysis
**Key Metrics:**
- Purchases per category
- Total spent per category
- Category diversity
- Category percentage of total spending

#### 4. Merchant_View
**Purpose:** Merchant loyalty analysis
**Key Metrics:**
- Visits per merchant
- Total spent per merchant
- Merchant diversity
- Merchant percentage of total spending

#### 5. Customer_Segments
**Purpose:** Final customer segmentation
**Key Metrics:**
- RFM scores (1-5 scale)
- Customer segment assignment
- Segment priority
- RFM score combination

#### 6. Customer_Analysis
**Purpose:** Comprehensive customer profile
**Key Metrics:**
- All demographic data
- All RFM metrics
- Segment information
- Value tier classification
- Lifecycle stage

## Data Validation

### Input Validation
- **TransactionAmount:** Must be positive (> 0)
- **Date:** Must be valid date format
- **CustomerID:** Cannot be null
- **Gender:** Standardized to M/F format

### Data Cleaning
- **Missing Values:** Handled appropriately for each field type
- **Text Fields:** Trimmed and standardized
- **Date Fields:** Validated and converted to proper format
- **Numeric Fields:** Validated and converted to appropriate types

## Performance Optimization

### Indexing Strategy
- **Primary Indexes:** CustomerID, Date, TransactionAmount
- **Secondary Indexes:** Category, MerchantName
- **Composite Indexes:** (CustomerID, Date) for time-series queries

### Query Optimization
- **Views:** Pre-calculated metrics for Power BI
- **Aggregations:** Optimized for analytical queries
- **Partitioning:** Considered for large datasets

## Power BI Integration

### Optimized Views
- **PowerBI_Main:** Core customer data for dashboards
- **PowerBI_Category_Analysis:** Category preferences by segment
- **PowerBI_Merchant_Analysis:** Merchant loyalty by segment

### Data Types
- **Compatible Types:** All data types optimized for Power BI
- **Date Formatting:** Standardized date formats
- **Numeric Precision:** Appropriate decimal precision

## Security Considerations

### Access Control
- **User Permissions:** Read-only access for Power BI
- **Data Privacy:** Customer data protection
- **Audit Logging:** Track data access and modifications

### Data Protection
- **Encryption:** At rest and in transit
- **Backup:** Regular automated backups
- **Recovery:** Point-in-time recovery capabilities

## Maintenance

### Regular Tasks
- **Index Maintenance:** Rebuild indexes periodically
- **Statistics Update:** Keep query statistics current
- **Data Archiving:** Archive old transaction data
- **Performance Monitoring:** Monitor query performance

### Monitoring
- **Query Performance:** Track slow queries
- **Index Usage:** Monitor index effectiveness
- **Storage Growth:** Monitor database size
- **Connection Count:** Monitor concurrent connections

## Scalability Considerations

### Horizontal Scaling
- **Read Replicas:** For Power BI connections
- **Sharding:** Consider for very large datasets
- **Caching:** Implement query result caching

### Vertical Scaling
- **Memory:** Increase for larger datasets
- **CPU:** Optimize for analytical queries
- **Storage:** SSD for better performance

## Backup and Recovery

### Backup Strategy
- **Full Backups:** Daily full database backups
- **Incremental Backups:** Hourly incremental backups
- **Transaction Log Backups:** Every 15 minutes

### Recovery Testing
- **Regular Testing:** Monthly recovery testing
- **Documentation:** Recovery procedures documented
- **Training:** Team trained on recovery procedures

## Data Quality

### Quality Metrics
- **Completeness:** Percentage of non-null values
- **Accuracy:** Data validation results
- **Consistency:** Cross-field validation
- **Timeliness:** Data freshness metrics

### Quality Monitoring
- **Automated Checks:** Daily data quality checks
- **Alerts:** Notifications for quality issues
- **Reporting:** Regular quality reports

## Future Enhancements

### Planned Improvements
- **Real-time Updates:** Near real-time data refresh
- **Advanced Analytics:** Machine learning integration
- **Data Lake:** Integration with data lake architecture
- **API Access:** RESTful API for data access

### Performance Optimizations
- **Columnar Storage:** Consider columnar databases
- **Compression:** Implement data compression
- **Caching:** Advanced caching strategies
- **Partitioning:** Table partitioning for large datasets
