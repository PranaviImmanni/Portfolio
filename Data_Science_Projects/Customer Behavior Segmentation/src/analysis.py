"""
Customer Behavior Segmentation - Analysis Script
Performs RFM analysis and customer segmentation
"""

import pandas as pd
import mysql.connector
from mysql.connector import Error
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CustomerSegmentationAnalysis:
    """Performs customer segmentation analysis using RFM methodology"""
    
    def __init__(self, host='localhost', user='root', password='', database='customer_segmentation'):
        """
        Initialize the analysis
        
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
    
    def get_customer_analysis(self):
        """Get customer analysis data from database"""
        try:
            if not self.connect():
                return None
            
            query = """
            SELECT 
                CustomerID,
                Name,
                Surname,
                Gender,
                Age,
                AgeGroup,
                Recency,
                Frequency,
                Monetary,
                RecencyScore,
                FrequencyScore,
                MonetaryScore,
                RFM_Score,
                CustomerSegment,
                LastTransactionDate,
                FirstTransactionDate,
                AvgTransactionAmount
            FROM Customer_Analysis
            """
            
            df = pd.read_sql(query, self.connection)
            logger.info(f"Retrieved {len(df)} customer records")
            return df
            
        except Error as e:
            logger.error(f"Error retrieving customer analysis: {e}")
            return None
        finally:
            self.disconnect()
    
    def get_segment_summary(self):
        """Get segment summary statistics"""
        try:
            if not self.connect():
                return None
            
            query = "SELECT * FROM Segment_Summary ORDER BY CustomerCount DESC"
            df = pd.read_sql(query, self.connection)
            logger.info(f"Retrieved segment summary for {len(df)} segments")
            return df
            
        except Error as e:
            logger.error(f"Error retrieving segment summary: {e}")
            return None
        finally:
            self.disconnect()
    
    def get_category_analysis(self):
        """Get category preferences by segment"""
        try:
            if not self.connect():
                return None
            
            query = """
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
            ORDER BY cs.CustomerSegment, TotalSpent DESC
            """
            
            df = pd.read_sql(query, self.connection)
            logger.info(f"Retrieved category analysis for {len(df)} segment-category combinations")
            return df
            
        except Error as e:
            logger.error(f"Error retrieving category analysis: {e}")
            return None
        finally:
            self.disconnect()
    
    def create_visualizations(self, output_dir='reports/figures'):
        """Create comprehensive visualizations"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Get data
        customer_df = self.get_customer_analysis()
        segment_df = self.get_segment_summary()
        category_df = self.get_category_analysis()
        
        if customer_df is None or segment_df is None:
            logger.error("Failed to retrieve data for visualization")
            return
        
        # Set style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # 1. Customer Segment Distribution
        plt.figure(figsize=(12, 8))
        plt.subplot(2, 2, 1)
        segment_df.plot(x='CustomerSegment', y='CustomerCount', kind='bar', ax=plt.gca())
        plt.title('Customer Distribution by Segment')
        plt.xlabel('Customer Segment')
        plt.ylabel('Number of Customers')
        plt.xticks(rotation=45)
        
        # 2. Average Spending by Segment
        plt.subplot(2, 2, 2)
        segment_df.plot(x='CustomerSegment', y='AvgMonetary', kind='bar', ax=plt.gca())
        plt.title('Average Spending by Segment')
        plt.xlabel('Customer Segment')
        plt.ylabel('Average Monetary Value')
        plt.xticks(rotation=45)
        
        # 3. RFM Score Distribution
        plt.subplot(2, 2, 3)
        rfm_counts = customer_df['RFM_Score'].value_counts().sort_index()
        rfm_counts.plot(kind='bar', ax=plt.gca())
        plt.title('RFM Score Distribution')
        plt.xlabel('RFM Score')
        plt.ylabel('Number of Customers')
        plt.xticks(rotation=45)
        
        # 4. Age Distribution by Segment
        plt.subplot(2, 2, 4)
        age_segment = customer_df.groupby(['CustomerSegment', 'AgeGroup']).size().unstack(fill_value=0)
        age_segment.plot(kind='bar', stacked=True, ax=plt.gca())
        plt.title('Age Group Distribution by Segment')
        plt.xlabel('Customer Segment')
        plt.ylabel('Number of Customers')
        plt.xticks(rotation=45)
        plt.legend(title='Age Group', bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/customer_segmentation_overview.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 5. Category Preferences Heatmap
        if category_df is not None and not category_df.empty:
            plt.figure(figsize=(14, 8))
            
            # Pivot data for heatmap
            heatmap_data = category_df.pivot_table(
                values='TotalSpent', 
                index='CustomerSegment', 
                columns='Category', 
                fill_value=0
            )
            
            sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='YlOrRd')
            plt.title('Spending by Customer Segment and Category')
            plt.xlabel('Category')
            plt.ylabel('Customer Segment')
            plt.xticks(rotation=45)
            plt.yticks(rotation=0)
            
            plt.tight_layout()
            plt.savefig(f'{output_dir}/category_preferences_heatmap.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        # 6. Gender Distribution
        plt.figure(figsize=(10, 6))
        gender_segment = customer_df.groupby(['CustomerSegment', 'Gender']).size().unstack(fill_value=0)
        gender_segment.plot(kind='bar', ax=plt.gca())
        plt.title('Gender Distribution by Customer Segment')
        plt.xlabel('Customer Segment')
        plt.ylabel('Number of Customers')
        plt.xticks(rotation=45)
        plt.legend(title='Gender')
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/gender_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Visualizations saved to {output_dir}")
    
    def generate_insights_report(self, output_file='reports/segmentation_insights.txt'):
        """Generate insights report"""
        import os
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        customer_df = self.get_customer_analysis()
        segment_df = self.get_segment_summary()
        
        if customer_df is None or segment_df is None:
            logger.error("Failed to retrieve data for insights report")
            return
        
        with open(output_file, 'w') as f:
            f.write("CUSTOMER SEGMENTATION ANALYSIS REPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Overall Statistics
            f.write("OVERALL STATISTICS\n")
            f.write("-" * 20 + "\n")
            f.write(f"Total Customers: {len(customer_df):,}\n")
            f.write(f"Total Revenue: ${customer_df['Monetary'].sum():,.2f}\n")
            f.write(f"Average Customer Value: ${customer_df['Monetary'].mean():,.2f}\n")
            f.write(f"Average Transaction Value: ${customer_df['AvgTransactionAmount'].mean():,.2f}\n\n")
            
            # Segment Analysis
            f.write("SEGMENT ANALYSIS\n")
            f.write("-" * 15 + "\n")
            for _, row in segment_df.iterrows():
                f.write(f"\n{row['CustomerSegment']}:\n")
                f.write(f"  Customers: {row['CustomerCount']:,} ({row['Percentage']:.1f}%)\n")
                f.write(f"  Avg Spending: ${row['AvgMonetary']:,.2f}\n")
                f.write(f"  Avg Frequency: {row['AvgFrequency']:.1f}\n")
                f.write(f"  Avg Recency: {row['AvgRecency']:.1f} days\n")
            
            # Top Customers
            f.write("\nTOP CUSTOMERS BY SEGMENT\n")
            f.write("-" * 25 + "\n")
            for segment in ['Champions', 'Loyal Customers', 'At Risk']:
                segment_customers = customer_df[customer_df['CustomerSegment'] == segment].nlargest(5, 'Monetary')
                if not segment_customers.empty:
                    f.write(f"\n{segment} (Top 5 by Spending):\n")
                    for _, customer in segment_customers.iterrows():
                        f.write(f"  {customer['Name']} {customer['Surname']}: ${customer['Monetary']:,.2f}\n")
            
            # Recommendations
            f.write("\nRECOMMENDATIONS\n")
            f.write("-" * 15 + "\n")
            f.write("1. Champions: Maintain high engagement, offer premium products\n")
            f.write("2. Loyal Customers: Increase frequency with loyalty programs\n")
            f.write("3. At Risk: Win-back campaigns, special offers\n")
            f.write("4. New Customers: Onboarding programs, welcome offers\n")
            f.write("5. Lost: Re-engagement campaigns, survey feedback\n")
        
        logger.info(f"Insights report saved to {output_file}")

def main():
    """Main function to run analysis"""
    # Configuration
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',  # Update with your MySQL password
        'database': 'customer_segmentation'
    }
    
    # Create analysis instance
    analysis = CustomerSegmentationAnalysis(**config)
    
    # Generate visualizations
    logger.info("Creating visualizations...")
    analysis.create_visualizations()
    
    # Generate insights report
    logger.info("Generating insights report...")
    analysis.generate_insights_report()
    
    logger.info("Analysis completed successfully!")

if __name__ == "__main__":
    main()
