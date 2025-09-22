#!/usr/bin/env python3
"""
Customer Behavior Segmentation - Main Execution Script
Complete RFM analysis pipeline with MySQL and Power BI integration
"""

import os
import sys
import logging
from pathlib import Path

# Add src directory to Python path
sys.path.append(str(Path(__file__).parent / 'src'))

from data_loader import CustomerDataLoader
from analysis import CustomerSegmentationAnalysis

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_database():
    """Setup MySQL database and load data"""
    logger.info("Setting up database...")
    
    # Configuration
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',  # Update with your MySQL password
        'database': 'customer_segmentation'
    }
    
    # Create data loader
    loader = CustomerDataLoader(**config)
    
    # Load data
    csv_file = 'data/customer_transactions.csv'
    if not os.path.exists(csv_file):
        logger.error(f"CSV file not found: {csv_file}")
        return False
    
    success = loader.load_csv_data(csv_file)
    if success:
        logger.info("Database setup completed successfully!")
        
        # Get summary
        summary = loader.get_data_summary()
        if summary:
            logger.info("Data Summary:")
            for key, value in summary.items():
                logger.info(f"  {key}: {value}")
        return True
    else:
        logger.error("Database setup failed!")
        return False

def run_analysis():
    """Run customer segmentation analysis"""
    logger.info("Running customer segmentation analysis...")
    
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

def main():
    """Main execution function"""
    logger.info("Starting Customer Behavior Segmentation Analysis")
    logger.info("=" * 60)
    
    try:
        # Step 1: Setup database
        if not setup_database():
            logger.error("Failed to setup database. Exiting.")
            return
        
        # Step 2: Run analysis
        run_analysis()
        
        logger.info("=" * 60)
        logger.info("Customer Behavior Segmentation Analysis completed successfully!")
        logger.info("Next steps:")
        logger.info("1. Open Power BI Desktop")
        logger.info("2. Connect to MySQL database 'customer_segmentation'")
        logger.info("3. Import the views from sql/database_setup.sql")
        logger.info("4. Follow the dashboard guide in powerbi/dashboard_guide.md")
        
    except Exception as e:
        logger.error(f"Analysis failed with error: {e}")
        raise

if __name__ == "__main__":
    main()
