"""
Customer Behavior Segmentation - Data Loader
Loads customer transaction data into MySQL database
"""

import pandas as pd
import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CustomerDataLoader:
    """Loads customer transaction data into MySQL database"""
    
    def __init__(self, host='localhost', user='root', password='', database='customer_segmentation'):
        """
        Initialize the data loader
        
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
    
    def load_csv_data(self, csv_file_path):
        """
        Load data from CSV file into MySQL
        
        Args:
            csv_file_path: Path to the CSV file
        """
        try:
            # Read CSV file
            logger.info(f"Loading data from {csv_file_path}")
            df = pd.read_csv(csv_file_path)
            
            # Data cleaning and validation
            df = self.clean_data(df)
            
            # Connect to database
            if not self.connect():
                return False
            
            cursor = self.connection.cursor()
            
            # Clear existing data
            cursor.execute("DELETE FROM Transactions")
            self.connection.commit()
            logger.info("Cleared existing transaction data")
            
            # Insert data
            insert_query = """
            INSERT INTO Transactions 
            (CustomerID, Name, Surname, Gender, Birthdate, TransactionAmount, Date, MerchantName, Category)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            # Prepare data for insertion
            data_to_insert = []
            for _, row in df.iterrows():
                data_to_insert.append((
                    int(row['Customer ID']),
                    str(row['Name']) if pd.notna(row['Name']) else None,
                    str(row['Surname']) if pd.notna(row['Surname']) else None,
                    str(row['Gender']) if pd.notna(row['Gender']) else None,
                    pd.to_datetime(row['Birthdate']).date() if pd.notna(row['Birthdate']) else None,
                    float(row['Transaction Amount']),
                    pd.to_datetime(row['Date']).date(),
                    str(row['Merchant Name']) if pd.notna(row['Merchant Name']) else None,
                    str(row['Category']) if pd.notna(row['Category']) else None
                ))
            
            # Batch insert
            cursor.executemany(insert_query, data_to_insert)
            self.connection.commit()
            
            logger.info(f"Successfully loaded {len(data_to_insert)} transactions")
            return True
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return False
        finally:
            if self.connection and self.connection.is_connected():
                cursor.close()
                self.disconnect()
    
    def clean_data(self, df):
        """
        Clean and validate the data
        
        Args:
            df: DataFrame to clean
            
        Returns:
            Cleaned DataFrame
        """
        logger.info("Cleaning and validating data...")
        
        # Remove rows with missing critical data
        initial_count = len(df)
        df = df.dropna(subset=['Customer ID', 'Transaction Amount', 'Date'])
        
        # Convert data types
        df['Customer ID'] = df['Customer ID'].astype(int)
        df['Transaction Amount'] = pd.to_numeric(df['Transaction Amount'], errors='coerce')
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Birthdate'] = pd.to_datetime(df['Birthdate'], errors='coerce')
        
        # Remove rows with invalid amounts (negative or zero)
        df = df[df['Transaction Amount'] > 0]
        
        # Remove rows with invalid dates
        df = df.dropna(subset=['Date'])
        
        # Clean text fields
        text_columns = ['Name', 'Surname', 'Merchant Name', 'Category']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
                df[col] = df[col].replace('nan', None)
        
        # Clean gender field
        if 'Gender' in df.columns:
            df['Gender'] = df['Gender'].astype(str).str.upper().str.strip()
            df['Gender'] = df['Gender'].replace(['NAN', 'NONE', ''], None)
            df['Gender'] = df['Gender'].replace(['M', 'MALE'], 'M')
            df['Gender'] = df['Gender'].replace(['F', 'FEMALE'], 'F')
        
        final_count = len(df)
        logger.info(f"Data cleaning complete: {initial_count} -> {final_count} records")
        
        return df
    
    def get_data_summary(self):
        """Get summary statistics of loaded data"""
        try:
            if not self.connect():
                return None
            
            cursor = self.connection.cursor()
            
            # Get basic statistics
            queries = {
                'total_transactions': "SELECT COUNT(*) FROM Transactions",
                'unique_customers': "SELECT COUNT(DISTINCT CustomerID) FROM Transactions",
                'date_range': "SELECT MIN(Date), MAX(Date) FROM Transactions",
                'total_amount': "SELECT SUM(TransactionAmount) FROM Transactions",
                'avg_transaction': "SELECT AVG(TransactionAmount) FROM Transactions"
            }
            
            summary = {}
            for key, query in queries.items():
                cursor.execute(query)
                result = cursor.fetchone()
                summary[key] = result[0] if result else None
            
            return summary
            
        except Error as e:
            logger.error(f"Error getting data summary: {e}")
            return None
        finally:
            if self.connection and self.connection.is_connected():
                cursor.close()
                self.disconnect()

def main():
    """Main function to load data"""
    # Configuration
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',  # Update with your MySQL password
        'database': 'customer_segmentation'
    }
    
    # File path
    csv_file = 'data/customer_transactions.csv'
    
    # Create data loader
    loader = CustomerDataLoader(**config)
    
    # Load data
    if loader.load_csv_data(csv_file):
        logger.info("Data loading completed successfully!")
        
        # Get summary
        summary = loader.get_data_summary()
        if summary:
            logger.info("Data Summary:")
            for key, value in summary.items():
                logger.info(f"  {key}: {value}")
    else:
        logger.error("Data loading failed!")

if __name__ == "__main__":
    main()
