# Customer Behavior Segmentation Analysis

A comprehensive customer segmentation project using RFM (Recency, Frequency, Monetary) analysis with MySQL database integration and Power BI dashboard creation.

## 📊 Project Overview

This project demonstrates advanced customer analytics by implementing a complete RFM analysis pipeline that transforms raw customer transaction data into actionable business insights through professional database design, SQL-based feature engineering, and interactive Power BI dashboards.

## 🎯 Key Features

- **Professional Database Design** - MySQL schema with proper indexing and constraints
- **Complete RFM Analysis** - Recency, Frequency, Monetary metrics calculation
- **11 Customer Segments** - From Champions to Lost customers with business insights
- **Power BI Integration** - Interactive dashboards with real-time filtering
- **Demographic Analysis** - Age groups, gender distribution, and preferences
- **Category & Merchant Analysis** - Spending patterns and loyalty tracking
- **Automated Reporting** - Comprehensive insights and visualizations

## 🏗️ Project Architecture

```
Customer Behavior Segmentation/
├── README.md                          # Project documentation
├── requirements.txt                   # Python dependencies
├── main.py                           # Main execution script
├── data/                             # Data directory
│   └── customer_transactions.csv     # Customer transaction dataset
├── sql/                              # SQL scripts and views
│   ├── database_setup.sql            # MySQL database schema
│   └── feature_engineering.sql       # RFM and demographic views
├── src/                              # Source code
│   ├── data_loader.py               # Data loading and validation
│   ├── analysis.py                  # Analysis and visualization
│   └── powerbi_connector.py         # Power BI integration utilities
├── powerbi/                          # Power BI resources
│   ├── analysis_queries.sql         # Power BI SQL queries
│   ├── dashboard_guide.md           # Dashboard configuration guide
│   └── segment_definitions.md       # RFM segment definitions
├── reports/                          # Generated reports
│   ├── figures/                      # Generated visualizations
│   └── insights/                     # Business insights reports
└── docs/                             # Additional documentation
    ├── database_schema.md            # Database design documentation
    └── business_insights.md          # Business recommendations
```

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8+
- MySQL Server 8.0+
- Power BI Desktop
- Git

### Installation
   ```bash
# Clone the repository
   git clone https://github.com/PranaviImmanni/Portfolio.git
cd Portfolio/Data_Science_Projects/Customer\ Behavior\ Segmentation

# Install dependencies
   pip install -r requirements.txt

# Ensure MySQL server is running
# Update database credentials in main.py
```

### Step 1: Load & Clean the Data

The project automatically loads and cleans your dataset into a MySQL database:

```python
# Data validation includes:
# - TransactionAmount > 0 (no negative values)
# - Valid Date format
# - CustomerID not null
# - Missing value handling
```

**Database Table: `Transactions`**
- CustomerID (Primary Key)
- Name, Surname, Gender
- Birthdate, TransactionAmount, Date
- MerchantName, Category

### Step 2: Feature Engineering in SQL

The project creates comprehensive SQL views for segmentation:

#### (a) RFM Metrics
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

#### (b) Demographics
```sql
SELECT CustomerID,
       Gender,
       DATEDIFF(CURDATE(), Birthdate) / 365.25 AS Age
FROM Transactions
GROUP BY CustomerID, Gender, Birthdate;
```

**Age Groups:**
- Gen Z: < 25
- Millennials: 25–40
- Gen X: 41–55
- Boomers: 56+

#### (c) Category Preferences
```sql
SELECT CustomerID,
       Category,
       COUNT(*) AS Purchases,
       SUM(TransactionAmount) AS TotalSpent
FROM Transactions
GROUP BY CustomerID, Category;
```

#### (d) Merchant Loyalty
```sql
SELECT CustomerID,
       MerchantName,
       COUNT(*) AS Visits,
       SUM(TransactionAmount) AS TotalSpent
FROM Transactions
GROUP BY CustomerID, MerchantName;
```

**Database Views Created:**
- `RFM_View` - Complete RFM metrics
- `Demographics_View` - Age and gender analysis
- `Category_View` - Category preferences
- `Merchant_View` - Merchant loyalty
- `Customer_Segments` - Final segmentation results

### Step 3: Load into Power BI

1. **Connect to MySQL Database:**
   - Server: `localhost`
   - Database: `customer_segmentation`
   - Username: `root` (or your MySQL username)
   - Password: (your MySQL password)

2. **Import Views:**
   - `Customer_Analysis` (main data source)
   - `Segment_Summary` (for pie charts)
   - `Category_View` (for category analysis)
   - `Merchant_View` (for merchant analysis)

3. **Build Relationships:**
   - All views connected on `CustomerID`

### Step 4: Build Segments

The project automatically creates 11 customer segments based on RFM scores:

#### RFM Scoring System
- **Recency Score (1-5):**
  - 5: < 30 days
  - 4: 30-60 days
  - 3: 60-90 days
  - 2: 90-180 days
  - 1: > 180 days

- **Frequency Score (1-5):**
  - 5: ≥ 20 transactions
  - 4: 15-19 transactions
  - 3: 10-14 transactions
  - 2: 5-9 transactions
  - 1: < 5 transactions

- **Monetary Score (1-5):**
  - 5: ≥ $5,000
  - 4: $3,000-$4,999
  - 3: $1,500-$2,999
  - 2: $500-$1,499
  - 1: < $500

#### Customer Segments
| Segment | RFM Pattern | Description | Business Action |
|---------|-------------|-------------|-----------------|
| **Champions** | 555, 554, 544 | Best customers | Maintain engagement, offer premium products |
| **Loyal Customers** | 444, 443, 442 | Regular buyers | Increase frequency with loyalty programs |
| **Potential Loyalists** | 544, 543, 542 | Recent, infrequent | Encourage more purchases |
| **New Customers** | 5XX | Recent first-time | Onboarding programs, welcome offers |
| **Promising** | 544, 543, 542 | Recent, some frequency | Nurture relationship |
| **Need Attention** | 344, 343, 342 | Declining frequency | Win-back campaigns |
| **About to Sleep** | 244, 243, 242 | Low recent activity | Re-engagement campaigns |
| **At Risk** | 144, 143, 142 | High value, low recency | Urgent win-back campaigns |
| **Cannot Lose Them** | 144, 143, 142 | High value, very low activity | Personal outreach |
| **Lost** | 111, 112, 113 | No recent activity | Survey feedback, re-engagement |
| **Others** | Mixed patterns | Various combinations | Analyze individual patterns |

### Step 5: Dashboard Design (Power BI)

#### Page 1: Customer Segmentation Overview
- **KPI Cards:**
  - Total Customers
  - Total Revenue
  - Average Transaction Value
  - Active Segments

- **Pie Chart:** Customer distribution by segment
- **Bar Chart:** Average spending by segment
- **RFM Score Distribution:** Histogram of RFM scores

#### Page 2: Demographic Insights
- **Matrix:** Segments vs Age Groups
- **Bar Chart:** Gender distribution across segments
- **Scatter Plot:** Age vs Spending by segment
- **Age Group Analysis:** Detailed demographic breakdown

#### Page 3: Category Preferences
- **Heatmap:** Segment × Top Categories
- **Bar Chart:** Category spending by segment
- **Tree Map:** Category performance visualization
- **Top Categories Table:** Detailed category analysis

#### Page 4: Merchant Loyalty
- **Tree Map:** Merchant revenue by segment
- **Bar Chart:** Top merchants by segment
- **Loyalty Analysis:** Customer-merchant relationships
- **Merchant Performance Table:** Detailed merchant metrics

#### Interactive Filtering
- **Segment Filter:** Select specific segments
- **Date Range Filter:** Filter by transaction dates
- **Demographic Filters:** Age group, gender filters
- **Category Filter:** Filter by product categories

## 🛠️ Technical Implementation

### Database Design
- **Normalized Schema** with proper relationships
- **Indexing** for optimal query performance
- **Constraints** for data validation
- **Views** for easy Power BI integration

### Analysis Pipeline
1. **Data Loading** - CSV to MySQL with validation
2. **Feature Engineering** - SQL-based RFM calculation
3. **Segmentation** - Rule-based customer grouping
4. **Visualization** - Python and Power BI charts
5. **Reporting** - Automated insight generation

### Power BI Integration
- **Direct Query** for real-time data
- **Calculated Columns** for RFM scores
- **Measures** for KPI calculations
- **Relationships** for cross-filtering

## 📈 Business Insights

### Key Metrics
- **Customer Lifetime Value** - Total monetary value per customer
- **Purchase Frequency** - Average transactions per customer
- **Recency Analysis** - Days since last purchase
- **Segment Performance** - Revenue and customer count by segment

### Actionable Recommendations
1. **Champions (5-10% of customers):** Focus on retention and premium offerings
2. **Loyal Customers (15-20%):** Increase purchase frequency
3. **At Risk (10-15%):** Immediate win-back campaigns
4. **New Customers (5-10%):** Onboarding and engagement programs
5. **Lost (20-30%):** Re-engagement and feedback collection

## 🔧 Configuration

### Database Setup
Update credentials in `main.py`:
```python
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'customer_segmentation'
}
```

### Power BI Connection
1. Open Power BI Desktop
2. Get Data → Database → MySQL database
3. Enter connection details
4. Import required views
5. Follow dashboard guide

## 📁 Output Files

### Generated Reports
- `reports/figures/customer_segmentation_overview.png`
- `reports/figures/category_preferences_heatmap.png`
- `reports/figures/demographic_analysis.png`
- `reports/insights/segmentation_insights.txt`

### Database Views
- `Customer_Analysis` - Complete customer data
- `Segment_Summary` - Segment statistics
- `Category_View` - Category preferences
- `Merchant_View` - Merchant loyalty

## 🚀 Running the Project

### Complete Pipeline
```bash
# Run the entire analysis
python main.py

# This will:
# 1. Load and clean data
# 2. Create database schema
# 3. Perform RFM analysis
# 4. Generate visualizations
# 5. Create insights report
```

### Individual Components
```bash
# Data loading only
python src/data_loader.py

# Analysis only
python src/analysis.py

# Power BI queries
# Use sql/feature_engineering.sql
```

## 📚 Documentation

- **Database Schema:** `docs/database_schema.md`
- **Business Insights:** `docs/business_insights.md`
- **Power BI Guide:** `powerbi/dashboard_guide.md`
- **Segment Definitions:** `powerbi/segment_definitions.md`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Customer transaction data from Kaggle
- RFM analysis methodology
- Power BI for visualization capabilities
- MySQL for database management

---

**Ready to transform your customer data into actionable business insights!** 🎯