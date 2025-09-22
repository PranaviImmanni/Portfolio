"""
Power BI Connector Utilities
Helper functions for Power BI integration and data export
"""

import pandas as pd
import mysql.connector
from mysql.connector import Error
import json
import logging
from datetime import datetime
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PowerBIConnector:
    """Utilities for Power BI integration and data export"""
    
    def __init__(self, host='localhost', user='root', password='', database='customer_segmentation'):
        """
        Initialize the Power BI connector
        
        Args:
            host: MySQL host
            user: MySQL username
            password: MySQL password
            database: Database name
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    
    def connect(self):
        """Connect to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                logger.info("Successfully connected to MySQL database")
                return True
        except Error as e:
            logger.error(f"Error connecting to MySQL: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from MySQL database"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("MySQL connection closed")
    
    def export_to_csv(self, view_name, output_file):
        """
        Export a database view to CSV for Power BI
        
        Args:
            view_name: Name of the database view
            output_file: Output CSV file path
        """
        try:
            if not self.connect():
                return False
            
            query = f"SELECT * FROM {view_name}"
            df = pd.read_sql(query, self.connection)
            
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Export to CSV
            df.to_csv(output_file, index=False)
            logger.info(f"Exported {view_name} to {output_file}")
            return True
            
        except Error as e:
            logger.error(f"Error exporting {view_name}: {e}")
            return False
        finally:
            self.disconnect()
    
    def export_all_views(self, output_dir='powerbi/data'):
        """
        Export all Power BI views to CSV files
        
        Args:
            output_dir: Output directory for CSV files
        """
        views = [
            'PowerBI_Main',
            'PowerBI_Category_Analysis',
            'PowerBI_Merchant_Analysis',
            'Segment_Summary',
            'Customer_Analysis'
        ]
        
        os.makedirs(output_dir, exist_ok=True)
        
        for view in views:
            output_file = f"{output_dir}/{view.lower()}.csv"
            self.export_to_csv(view, output_file)
    
    def generate_connection_string(self):
        """
        Generate MySQL connection string for Power BI
        
        Returns:
            Connection string for Power BI
        """
        return f"Server={self.host};Database={self.database};Uid={self.user};Pwd={self.password};"
    
    def create_powerbi_config(self, output_file='powerbi/powerbi_config.json'):
        """
        Create Power BI configuration file
        
        Args:
            output_file: Output configuration file path
        """
        config = {
            "database": {
                "host": self.host,
                "database": self.database,
                "user": self.user,
                "connection_string": self.generate_connection_string()
            },
            "views": {
                "main_data": "PowerBI_Main",
                "category_analysis": "PowerBI_Category_Analysis",
                "merchant_analysis": "PowerBI_Merchant_Analysis",
                "segment_summary": "Segment_Summary",
                "customer_analysis": "Customer_Analysis"
            },
            "segments": {
                "champions": "Champions",
                "loyal_customers": "Loyal Customers",
                "potential_loyalists": "Potential Loyalists",
                "new_customers": "New Customers",
                "promising": "Promising",
                "need_attention": "Need Attention",
                "about_to_sleep": "About to Sleep",
                "at_risk": "At Risk",
                "cannot_lose_them": "Cannot Lose Them",
                "lost": "Lost",
                "others": "Others"
            },
            "age_groups": {
                "gen_z": "Gen Z",
                "millennials": "Millennials",
                "gen_x": "Gen X",
                "boomers": "Boomers"
            },
            "value_tiers": {
                "high_value": "High Value",
                "medium_value": "Medium Value",
                "low_value": "Low Value"
            },
            "lifecycle_stages": {
                "active": "Active",
                "engaged": "Engaged",
                "at_risk": "At Risk",
                "inactive": "Inactive"
            }
        }
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        logger.info(f"Power BI configuration saved to {output_file}")
    
    def generate_dax_measures(self, output_file='powerbi/dax_measures.txt'):
        """
        Generate DAX measures for Power BI
        
        Args:
            output_file: Output file for DAX measures
        """
        dax_measures = """
-- Power BI DAX Measures for Customer Segmentation

-- Total Customers
Total_Customers = COUNTROWS(PowerBI_Main)

-- Total Revenue
Total_Revenue = SUM(PowerBI_Main[Monetary])

-- Average Transaction Value
Avg_Transaction_Value = AVERAGE(PowerBI_Main[AvgTransactionAmount])

-- Average Customer Value
Avg_Customer_Value = AVERAGE(PowerBI_Main[Monetary])

-- Champions Count
Champions_Count = 
CALCULATE(
    COUNTROWS(PowerBI_Main),
    PowerBI_Main[CustomerSegment] = "Champions"
)

-- Champions Percentage
Champions_Percentage = 
DIVIDE(
    [Champions_Count],
    [Total_Customers]
) * 100

-- At Risk Count
At_Risk_Count = 
CALCULATE(
    COUNTROWS(PowerBI_Main),
    PowerBI_Main[CustomerSegment] = "At Risk"
)

-- At Risk Percentage
At_Risk_Percentage = 
DIVIDE(
    [At_Risk_Count],
    [Total_Customers]
) * 100

-- High Value Customers
High_Value_Customers = 
CALCULATE(
    COUNTROWS(PowerBI_Main),
    PowerBI_Main[ValueTier] = "High Value"
)

-- High Value Percentage
High_Value_Percentage = 
DIVIDE(
    [High_Value_Customers],
    [Total_Customers]
) * 100

-- Average Recency
Avg_Recency = AVERAGE(PowerBI_Main[Recency])

-- Average Frequency
Avg_Frequency = AVERAGE(PowerBI_Main[Frequency])

-- Average Monetary
Avg_Monetary = AVERAGE(PowerBI_Main[Monetary])

-- Revenue by Segment
Revenue_by_Segment = 
SUMX(
    VALUES(PowerBI_Main[CustomerSegment]),
    [Total_Revenue]
)

-- Customers by Age Group
Customers_by_Age_Group = 
SUMX(
    VALUES(PowerBI_Main[AgeGroup]),
    [Total_Customers]
)

-- Top Category Revenue
Top_Category_Revenue = 
SUMX(
    VALUES(PowerBI_Category_Analysis[Category]),
    SUM(PowerBI_Category_Analysis[TotalSpent])
)

-- Top Merchant Revenue
Top_Merchant_Revenue = 
SUMX(
    VALUES(PowerBI_Merchant_Analysis[MerchantName]),
    SUM(PowerBI_Merchant_Analysis[TotalSpent])
)

-- Customer Retention Rate
Customer_Retention_Rate = 
DIVIDE(
    [Champions_Count] + CALCULATE(COUNTROWS(PowerBI_Main), PowerBI_Main[CustomerSegment] = "Loyal Customers"),
    [Total_Customers]
) * 100

-- Customer Churn Rate
Customer_Churn_Rate = 
DIVIDE(
    CALCULATE(COUNTROWS(PowerBI_Main), PowerBI_Main[CustomerSegment] = "Lost"),
    [Total_Customers]
) * 100

-- Revenue per Customer by Segment
Revenue_per_Customer_by_Segment = 
DIVIDE(
    [Total_Revenue],
    [Total_Customers]
)

-- Category Diversity Score
Category_Diversity_Score = 
AVERAGE(PowerBI_Main[CategoryDiversity])

-- Merchant Diversity Score
Merchant_Diversity_Score = 
AVERAGE(PowerBI_Main[MerchantDiversity])

-- Active Customers (Last 30 days)
Active_Customers = 
CALCULATE(
    COUNTROWS(PowerBI_Main),
    PowerBI_Main[Recency] <= 30
)

-- Active Customer Percentage
Active_Customer_Percentage = 
DIVIDE(
    [Active_Customers],
    [Total_Customers]
) * 100

-- New Customers (Last 90 days)
New_Customers = 
CALCULATE(
    COUNTROWS(PowerBI_Main),
    PowerBI_Main[CustomerSegment] = "New Customers"
)

-- New Customer Percentage
New_Customer_Percentage = 
DIVIDE(
    [New_Customers],
    [Total_Customers]
) * 100
"""
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w') as f:
            f.write(dax_measures)
        
        logger.info(f"DAX measures saved to {output_file}")
    
    def create_powerbi_template(self, output_file='powerbi/powerbi_template.pbix'):
        """
        Create Power BI template file (placeholder)
        
        Args:
            output_file: Output template file path
        """
        # This is a placeholder - actual PBIX file creation would require Power BI SDK
        template_info = {
            "template_name": "Customer Segmentation Dashboard",
            "version": "1.0",
            "created_date": datetime.now().isoformat(),
            "description": "Professional customer segmentation dashboard template",
            "pages": [
                "Customer Segmentation Overview",
                "Demographic Insights", 
                "Category Preferences",
                "Merchant Loyalty"
            ],
            "data_sources": [
                "PowerBI_Main",
                "PowerBI_Category_Analysis",
                "PowerBI_Merchant_Analysis",
                "Segment_Summary"
            ]
        }
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file.replace('.pbix', '.json'), 'w') as f:
            json.dump(template_info, f, indent=2)
        
        logger.info(f"Power BI template info saved to {output_file.replace('.pbix', '.json')}")

def main():
    """Main function to generate Power BI resources"""
    # Configuration
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',  # Update with your MySQL password
        'database': 'customer_segmentation'
    }
    
    # Create Power BI connector
    connector = PowerBIConnector(**config)
    
    # Generate Power BI resources
    logger.info("Generating Power BI resources...")
    
    # Export all views to CSV
    connector.export_all_views()
    
    # Create configuration file
    connector.create_powerbi_config()
    
    # Generate DAX measures
    connector.generate_dax_measures()
    
    # Create template info
    connector.create_powerbi_template()
    
    logger.info("Power BI resources generated successfully!")
    logger.info("Next steps:")
    logger.info("1. Open Power BI Desktop")
    logger.info("2. Connect to MySQL database using the connection string")
    logger.info("3. Import the views from the database")
    logger.info("4. Use the DAX measures provided")
    logger.info("5. Follow the dashboard guide for layout")

if __name__ == "__main__":
    main()
