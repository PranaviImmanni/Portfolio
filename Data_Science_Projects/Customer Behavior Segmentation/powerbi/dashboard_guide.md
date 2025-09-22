# Power BI Dashboard Configuration Guide

## Database Connection Setup

### 1. Connect to MySQL Database
1. Open Power BI Desktop
2. Click "Get Data" → "Database" → "MySQL database"
3. Enter connection details:
   - Server: `localhost` (or your MySQL server)
   - Database: `customer_segmentation`
   - Username: `root` (or your MySQL username)
   - Password: (your MySQL password)

### 2. Import Required Views
Import these views from the database:
- `Customer_Analysis` (main data source)
- `Segment_Summary` (for pie charts)
- `Category_View` (for category analysis)
- `Merchant_View` (for merchant analysis)

## Dashboard Layout

### Page 1: Customer Segmentation Overview

#### KPI Cards (Top Row)
- **Total Customers**: `COUNT(Customer_Analysis[CustomerID])`
- **Total Revenue**: `SUM(Customer_Analysis[Monetary])`
- **Average Transaction Value**: `AVERAGE(Customer_Analysis[AvgTransactionAmount])`
- **Active Segments**: `DISTINCTCOUNT(Customer_Analysis[CustomerSegment])`

#### Pie Chart: Customer Distribution
- **Data**: `Segment_Summary`
- **Legend**: `CustomerSegment`
- **Values**: `CustomerCount`
- **Title**: "Customer Distribution by Segment"

#### Bar Chart: Segment Performance
- **X-axis**: `CustomerSegment`
- **Y-axis**: `AvgMonetary` (from Segment_Summary)
- **Title**: "Average Spending by Segment"

### Page 2: Demographic Insights

#### Matrix: Segments vs Demographics
- **Rows**: `CustomerSegment`
- **Columns**: `AgeGroup`
- **Values**: `CustomerCount`
- **Title**: "Customer Count by Segment and Age Group"

#### Bar Chart: Gender Distribution
- **X-axis**: `CustomerSegment`
- **Y-axis**: `CustomerCount`
- **Legend**: `Gender`
- **Title**: "Gender Distribution Across Segments"

#### Scatter Plot: Age vs Spending
- **X-axis**: `Age`
- **Y-axis**: `Monetary`
- **Legend**: `CustomerSegment`
- **Title**: "Age vs Spending by Segment"

### Page 3: Category Preferences

#### Heatmap: Segment × Categories
- **Rows**: `CustomerSegment`
- **Columns**: `Category`
- **Values**: `TotalSpent`
- **Title**: "Spending by Segment and Category"

#### Bar Chart: Top Categories
- **X-axis**: `Category`
- **Y-axis**: `TotalSpent`
- **Legend**: `CustomerSegment`
- **Title**: "Category Spending by Segment"

### Page 4: Merchant Loyalty

#### Tree Map: Merchant Performance
- **Category**: `CustomerSegment`
- **Values**: `TotalSpent`
- **Details**: `MerchantName`
- **Title**: "Merchant Revenue by Segment"

#### Table: Top Merchants by Segment
- **Columns**: `CustomerSegment`, `MerchantName`, `TotalSpent`, `CustomerCount`
- **Title**: "Top Merchants by Customer Segment"

## Calculated Columns and Measures

### Calculated Columns
```DAX
// RFM Score as Text
RFM_Score_Text = 
CONCATENATE(
    CONCATENATE(
        CONCATENATE("R", Customer_Analysis[RecencyScore]),
        "F"
    ),
    Customer_Analysis[FrequencyScore]
) & Customer_Analysis[MonetaryScore]

// Customer Value Tier
Value_Tier = 
IF(
    Customer_Analysis[Monetary] >= 5000, "High Value",
    IF(
        Customer_Analysis[Monetary] >= 2000, "Medium Value",
        "Low Value"
    )
)
```

### Key Measures
```DAX
// Total Customers
Total_Customers = COUNTROWS(Customer_Analysis)

// Total Revenue
Total_Revenue = SUM(Customer_Analysis[Monetary])

// Average Transaction Value
Avg_Transaction_Value = AVERAGE(Customer_Analysis[AvgTransactionAmount])

// Champions Percentage
Champions_Percentage = 
DIVIDE(
    CALCULATE(COUNTROWS(Customer_Analysis), Customer_Analysis[CustomerSegment] = "Champions"),
    COUNTROWS(Customer_Analysis)
) * 100

// At Risk Customers
At_Risk_Customers = 
CALCULATE(
    COUNTROWS(Customer_Analysis),
    Customer_Analysis[CustomerSegment] = "At Risk"
)
```

## Interactive Filtering

### Slicers
1. **Customer Segment**: Multi-select dropdown
2. **Age Group**: Multi-select dropdown
3. **Gender**: Multi-select dropdown
4. **Date Range**: Date range slider

### Cross-filtering
- All charts should cross-filter when a segment is selected
- Use "Edit interactions" to control which charts affect each other

## Visual Formatting

### Color Scheme
- **Champions**: Green (#2E8B57)
- **Loyal Customers**: Blue (#4169E1)
- **At Risk**: Red (#DC143C)
- **New Customers**: Orange (#FF8C00)
- **Lost**: Gray (#808080)

### Fonts and Sizing
- **Title Font**: Segoe UI Bold, 16pt
- **Axis Labels**: Segoe UI, 12pt
- **Data Labels**: Segoe UI, 10pt
- **Card Values**: Segoe UI Bold, 24pt

## Export and Sharing

### Export Options
1. **PDF Report**: File → Export → PDF
2. **PowerPoint**: File → Export → PowerPoint
3. **Excel**: File → Export → Excel

### Publishing
1. Click "Publish" to Power BI Service
2. Set up automatic refresh schedule
3. Share with stakeholders via link or email

## Troubleshooting

### Common Issues
1. **Connection Errors**: Check MySQL server status and credentials
2. **Data Not Loading**: Verify view names and permissions
3. **Performance Issues**: Add filters to reduce data volume
4. **Visual Errors**: Check data types and relationships

### Performance Optimization
1. Use filters to limit data volume
2. Create aggregated tables for large datasets
3. Use DirectQuery for real-time data
4. Optimize MySQL queries with proper indexing
