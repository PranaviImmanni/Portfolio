# Customer Behavior Segmentation Analysis

A comprehensive customer segmentation project using RFM (Recency, Frequency, Monetary) analysis with MySQL database integration and Power BI dashboard creation.

## Project Overview

This project demonstrates advanced customer analytics by:
- Loading customer transaction data into MySQL database
- Performing RFM analysis using SQL queries
- Creating customer segments based on behavioral patterns
- Building interactive Power BI dashboards
- Generating actionable business insights

## Features

### Data Management
- **MySQL Database Integration** - Professional database design with proper indexing
- **Data Validation** - Comprehensive data cleaning and validation
- **SQL Views** - Pre-built views for easy Power BI integration
- **RFM Analysis** - Complete Recency, Frequency, Monetary analysis

### Customer Segmentation
- **11 Customer Segments** - From Champions to Lost customers
- **Demographic Analysis** - Age groups, gender distribution
- **Category Preferences** - Spending patterns by product category
- **Merchant Loyalty** - Customer loyalty to specific merchants

### Visualization & Reporting
- **Power BI Dashboards** - Interactive business intelligence dashboards
- **Python Visualizations** - Comprehensive charts and analysis
- **Insights Reports** - Automated report generation
- **Export Capabilities** - Multiple export formats

## Project Structure

```
Customer Behavior Segmentation/
├── README.md                          # Project documentation
├── requirements.txt                   # Python dependencies
├── main.py                           # Main execution script
├── data/                             # Data directory
│   └── customer_transactions.csv     # Customer transaction data
├── sql/                              # SQL scripts
│   └── database_setup.sql            # MySQL database schema
├── src/                              # Source code
│   ├── data_loader.py               # Data loading utilities
│   └── analysis.py                  # Analysis and visualization
├── powerbi/                          # Power BI resources
│   ├── analysis_queries.sql         # Power BI SQL queries
│   └── dashboard_guide.md           # Dashboard configuration guide
└── reports/                          # Generated reports
    ├── figures/                      # Generated visualizations
    └── segmentation_insights.txt     # Insights report
```

## Quick Start

### Prerequisites
- Python 3.8+
- MySQL Server
- Power BI Desktop (optional)

### 1. Installation
   ```bash
# Install dependencies
   pip install -r requirements.txt

# Ensure MySQL server is running
# Update database credentials in main.py
   ```

### 2. Database Setup
   ```bash
# Run the main script
python main.py
```

This will:
- Create MySQL database and tables
- Load customer transaction data
- Perform RFM analysis
- Generate visualizations and reports

### 3. Power BI Dashboard
1. Open Power BI Desktop
2. Connect to MySQL database `customer_segmentation`
3. Import views from `sql/database_setup.sql`
4. Follow `powerbi/dashboard_guide.md` for dashboard setup

## Customer Segments

The analysis creates 11 distinct customer segments:

| Segment | Description | Characteristics |
|---------|-------------|-----------------|
| **Champions** | Best customers | High R, F, M scores |
| **Loyal Customers** | Regular buyers | Good R, F, M scores |
| **Potential Loyalists** | Recent, infrequent | High R, low F, M |
| **New Customers** | Recent first-time | High R only |
| **Promising** | Recent, some frequency | Good R, F, low M |
| **Need Attention** | Declining frequency | Low R, good F, M |
| **About to Sleep** | Low recent activity | Low R, F, good M |
| **At Risk** | High value, low recency | Low R, good M |
| **Cannot Lose Them** | High value, very low activity | Very low R, F, high M |
| **Lost** | No recent activity | Low R, F, M |
| **Others** | Mixed patterns | Various combinations |

## SQL Analysis

### RFM Metrics Calculation
```sql
-- Recency (days since last transaction)
SELECT CustomerID,
       DATEDIFF(CURDATE(), MAX(Date)) AS Recency
FROM Transactions
GROUP BY CustomerID;

-- Frequency (number of transactions)
SELECT CustomerID,
       COUNT(*) AS Frequency
FROM Transactions
GROUP BY CustomerID;

-- Monetary (total spend)
SELECT CustomerID,
       SUM(TransactionAmount) AS Monetary
FROM Transactions
GROUP BY CustomerID;
```

### Customer Segmentation
```sql
-- Complete customer analysis
SELECT 
    cs.CustomerID,
    d.AgeGroup,
    d.Gender,
    cs.CustomerSegment,
    cs.Recency,
    cs.Frequency,
    cs.Monetary
FROM Customer_Segments cs
JOIN Demographics_View d ON cs.CustomerID = d.CustomerID;
```

## Power BI Dashboard Features

### Page 1: Customer Segmentation Overview
- **KPI Cards**: Total customers, revenue, average transaction value
- **Pie Chart**: Customer distribution by segment
- **Bar Chart**: Average spending by segment

### Page 2: Demographic Insights
- **Matrix**: Segments vs age groups
- **Bar Chart**: Gender distribution across segments
- **Scatter Plot**: Age vs spending by segment

### Page 3: Category Preferences
- **Heatmap**: Spending by segment and category
- **Bar Chart**: Top categories by segment

### Page 4: Merchant Loyalty
- **Tree Map**: Merchant revenue by segment
- **Table**: Top merchants by customer segment

## Business Insights

### Key Metrics
- **Customer Lifetime Value** - Total monetary value per customer
- **Purchase Frequency** - Average transactions per customer
- **Recency Analysis** - Days since last purchase
- **Segment Performance** - Revenue and customer count by segment

### Actionable Recommendations
1. **Champions**: Maintain engagement, offer premium products
2. **Loyal Customers**: Increase frequency with loyalty programs
3. **At Risk**: Win-back campaigns, special offers
4. **New Customers**: Onboarding programs, welcome offers
5. **Lost**: Re-engagement campaigns, survey feedback

## Technical Implementation

### Database Design
- **Normalized Schema** - Proper table relationships
- **Indexing** - Optimized for query performance
- **Views** - Pre-calculated metrics for Power BI
- **Constraints** - Data validation and integrity

### Analysis Pipeline
1. **Data Loading** - CSV to MySQL with validation
2. **RFM Calculation** - SQL-based metric computation
3. **Segmentation** - Rule-based customer grouping
4. **Visualization** - Python and Power BI charts
5. **Reporting** - Automated insight generation

## Configuration

Update database credentials in `main.py`:
```python
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',  # Update this
    'database': 'customer_segmentation'
}
```

## Output Files

### Generated Reports
- `reports/figures/customer_segmentation_overview.png`
- `reports/figures/category_preferences_heatmap.png`
- `reports/figures/gender_distribution.png`
- `reports/segmentation_insights.txt`

### Database Views
- `Customer_Analysis` - Complete customer data
- `Segment_Summary` - Segment statistics
- `Category_View` - Category preferences
- `Merchant_View` - Merchant loyalty

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Acknowledgments

- Customer transaction data from Kaggle
- RFM analysis methodology
- Power BI for visualization capabilities