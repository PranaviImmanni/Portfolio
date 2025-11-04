"""
EV Sensor Data Processing
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from pathlib import Path
from src.utils.logger import get_logger
from src.utils.database import DatabaseManager

logger = get_logger(__name__)

class SensorProcessor:
    """Process and analyze EV sensor telemetry data"""
    
    def __init__(self):
        """Initialize sensor processor"""
        self.db = DatabaseManager()
        self.db.connect()
    
    def process_batch(self, input_path: str, output_path: str = None) -> pd.DataFrame:
        """
        Process batch of sensor data
        
        Args:
            input_path: Path to input CSV file
            output_path: Path to save processed data
            
        Returns:
            Processed DataFrame
        """
        try:
            # Load data
            df = pd.read_csv(input_path)
            logger.info(f"Loaded {len(df)} sensor records")
            
            # Data cleaning
            df = self._clean_data(df)
            
            # Feature engineering
            df = self._engineer_features(df)
            
            # Save processed data
            if output_path:
                df.to_csv(output_path, index=False)
                logger.info(f"Processed data saved: {output_path}")
            
            # Store in database
            self._store_in_database(df)
            
            return df
            
        except Exception as e:
            logger.error(f"Batch processing failed: {e}")
            raise
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean sensor data"""
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Handle missing values
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        
        # Remove outliers (values beyond 3 standard deviations)
        for col in numeric_cols:
            mean = df[col].mean()
            std = df[col].std()
            df = df[(df[col] >= mean - 3*std) & (df[col] <= mean + 3*std)]
        
        logger.info(f"Data cleaned: {len(df)} records remaining")
        return df
    
    def _engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer features from sensor data"""
        # Rolling statistics
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
        
        # Rolling averages
        for col in ['battery_voltage', 'battery_temp', 'motor_temp']:
            if col in df.columns:
                df[f'{col}_rolling_mean'] = df[col].rolling(window=10, min_periods=1).mean()
                df[f'{col}_rolling_std'] = df[col].rolling(window=10, min_periods=1).std()
        
        # Rate of change
        if 'battery_voltage' in df.columns:
            df['voltage_change_rate'] = df['battery_voltage'].diff()
        
        if 'battery_temp' in df.columns:
            df['temp_change_rate'] = df['battery_temp'].diff()
        
        # Health scores
        df['battery_health_score'] = self._calculate_battery_health(df)
        df['motor_health_score'] = self._calculate_motor_health(df)
        
        logger.info("Features engineered successfully")
        return df
    
    def _calculate_battery_health(self, df: pd.DataFrame) -> pd.Series:
        """Calculate battery health score"""
        if 'battery_voltage' not in df.columns or 'battery_temp' not in df.columns:
            return pd.Series([0.5] * len(df))
        
        # Normalize voltage (ideal: 380-420V)
        voltage_score = np.where(
            (df['battery_voltage'] >= 380) & (df['battery_voltage'] <= 420),
            1.0,
            np.where(df['battery_voltage'] < 380, df['battery_voltage'] / 380, 420 / df['battery_voltage'])
        )
        
        # Normalize temperature (ideal: 20-35°C)
        temp_score = np.where(
            (df['battery_temp'] >= 20) & (df['battery_temp'] <= 35),
            1.0,
            np.where(df['battery_temp'] < 20, df['battery_temp'] / 20, 35 / df['battery_temp'])
        )
        
        # Combined health score
        health_score = (voltage_score + temp_score) / 2
        return pd.Series(health_score)
    
    def _calculate_motor_health(self, df: pd.DataFrame) -> pd.Series:
        """Calculate motor health score"""
        if 'motor_temp' not in df.columns:
            return pd.Series([0.5] * len(df))
        
        # Normalize temperature (ideal: 30-45°C)
        temp_score = np.where(
            (df['motor_temp'] >= 30) & (df['motor_temp'] <= 45),
            1.0,
            np.where(df['motor_temp'] < 30, df['motor_temp'] / 30, 45 / df['motor_temp'])
        )
        
        return pd.Series(temp_score)
    
    def _store_in_database(self, df: pd.DataFrame):
        """Store processed data in database"""
        try:
            if not self.db.engine:
                self.db.connect()
            
            # Select relevant columns for database
            db_columns = ['vehicle_id', 'timestamp', 'battery_voltage', 'battery_temp',
                         'motor_temp', 'charging_current', 'mileage']
            
            available_columns = [col for col in db_columns if col in df.columns]
            df_to_store = df[available_columns].copy()
            
            if not df_to_store.empty:
                self.db.insert_dataframe(df_to_store, 'sensor_telemetry', if_exists='append')
                logger.info(f"Stored {len(df_to_store)} records in database")
        except Exception as e:
            logger.warning(f"Database storage failed: {e}")

