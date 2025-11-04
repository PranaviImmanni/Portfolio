"""
Data Loader for EV Sensors: Driving Pattern Diagnostics Dataset
Loads real EV sensor data from Kaggle dataset
Dataset: EV Sensors: Driving Pattern Diagnostics (2020-24)
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Optional, Dict
from config import DATA_DIR
from src.utils.logger import get_logger

logger = get_logger(__name__)

class EVDatasetLoader:
    """Load and preprocess EV Sensors: Driving Pattern Diagnostics dataset"""
    
    def __init__(self, data_dir: str = None):
        """
        Initialize dataset loader
        
        Args:
            data_dir: Directory containing the dataset CSV files
        """
        self.data_dir = Path(data_dir) if data_dir else DATA_DIR / "raw"
        self.user_types = ['rare_user', 'moderate_user', 'heavy_user', 'regular_user']
    
    def load_dataset(self, user_type: str = None, combine: bool = True) -> pd.DataFrame:
        """
        Load EV sensor dataset
        
        Args:
            user_type: Specific user type to load ('rare_user', 'moderate_user', etc.)
                       If None, loads all user types
            combine: If True, combines all user types into single DataFrame
        
        Returns:
            DataFrame with sensor data
        """
        try:
            if user_type:
                # Load specific user type
                file_path = self.data_dir / f"{user_type}.csv"
                if not file_path.exists():
                    raise FileNotFoundError(f"Dataset file not found: {file_path}")
                
                df = pd.read_csv(file_path)
                df['user_type'] = user_type
                logger.info(f"Loaded {len(df)} records from {user_type}")
                return df
            
            else:
                # Load all user types
                all_data = []
                for user in self.user_types:
                    file_path = self.data_dir / f"{user}.csv"
                    if file_path.exists():
                        df = pd.read_csv(file_path)
                        df['user_type'] = user
                        all_data.append(df)
                        logger.info(f"Loaded {len(df)} records from {user}")
                    else:
                        logger.warning(f"Dataset file not found: {file_path}")
                
                if not all_data:
                    raise FileNotFoundError(f"No dataset files found in {self.data_dir}")
                
                if combine:
                    combined_df = pd.concat(all_data, ignore_index=True)
                    logger.info(f"Combined dataset: {len(combined_df)} total records")
                    return combined_df
                else:
                    return {user: df for user, df in zip(self.user_types, all_data)}
                    
        except Exception as e:
            logger.error(f"Dataset loading failed: {e}")
            raise
    
    def preprocess_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess the loaded dataset
        
        Args:
            df: Raw dataset DataFrame
            
        Returns:
            Preprocessed DataFrame
        """
        try:
            # Make a copy
            df = df.copy()
            
            # Convert timestamp column (if it exists with different names)
            timestamp_cols = ['timestamp', 'Timestamp', 'date', 'Date', 'datetime', 'DateTime']
            timestamp_col = None
            for col in timestamp_cols:
                if col in df.columns:
                    timestamp_col = col
                    break
            
            if timestamp_col:
                df[timestamp_col] = pd.to_datetime(df[timestamp_col])
                df = df.rename(columns={timestamp_col: 'timestamp'})
            else:
                # Create timestamp if not present
                df['timestamp'] = pd.date_range(start='2020-01-01', periods=len(df), freq='H')
            
            # Standardize column names (make lowercase with underscores)
            df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')
            
            # Map common column name variations
            column_mapping = {
                'vehicle_id': ['vehicleid', 'vehicle_id', 'vehicle', 'id'],
                'battery_voltage': ['batteryvoltage', 'battery_voltage', 'voltage', 'battery_v'],
                'battery_temp': ['batterytemp', 'battery_temp', 'battery_temperature', 'battery_t'],
                'motor_temp': ['motortemp', 'motor_temp', 'motor_temperature', 'motor_t'],
                'charging_current': ['chargingcurrent', 'charging_current', 'current', 'charge_current'],
                'mileage': ['mileage', 'odometer', 'total_mileage', 'miles'],
                'speed': ['speed', 'velocity', 'mph'],
                'soc': ['soc', 'state_of_charge', 'battery_soc', 'charge_level']
            }
            
            # Rename columns based on mapping
            for standard_name, variants in column_mapping.items():
                for variant in variants:
                    if variant in df.columns and standard_name not in df.columns:
                        df = df.rename(columns={variant: standard_name})
            
            # Ensure required columns exist (create if missing with defaults)
            if 'vehicle_id' not in df.columns:
                if 'user_type' in df.columns:
                    df['vehicle_id'] = df['user_type'].apply(lambda x: f"EV_{x.upper()[:3]}")
                else:
                    df['vehicle_id'] = 'EV_001'
            
            # Add missing columns with default values if needed for model compatibility
            required_cols = {
                'battery_voltage': 380.0,
                'battery_temp': 35.0,
                'motor_temp': 40.0,
                'charging_current': 45.0,
                'mileage': 10000
            }
            
            for col, default_val in required_cols.items():
                if col not in df.columns:
                    logger.warning(f"Column '{col}' not found, using default value: {default_val}")
                    df[col] = default_val
            
            # Sort by timestamp
            df = df.sort_values('timestamp')
            
            # Remove duplicates
            df = df.drop_duplicates()
            
            logger.info(f"Preprocessed dataset: {len(df)} records")
            logger.info(f"Columns: {list(df.columns)}")
            
            return df
            
        except Exception as e:
            logger.error(f"Dataset preprocessing failed: {e}")
            raise
    
    def create_training_data(self, df: pd.DataFrame, output_path: str = None) -> pd.DataFrame:
        """
        Create training data with failure labels from the dataset
        
        Args:
            df: Preprocessed dataset DataFrame
            output_path: Path to save training data
            
        Returns:
            DataFrame with failure labels
        """
        try:
            # Copy dataframe
            training_df = df.copy()
            
            # Create failure labels based on sensor patterns
            # This simulates DTC (Diagnostic Trouble Code) prediction
            
            # Battery failure indicators
            battery_failure = (
                (training_df['battery_voltage'] < 350) | 
                (training_df['battery_temp'] > 50) |
                (training_df.get('soc', 100) < 20)
            )
            
            # Motor failure indicators
            motor_failure = (
                (training_df['motor_temp'] > 60) |
                (training_df.get('cooling_system_temp', 50) > 70)
            )
            
            # Charging system failure
            charging_failure = (
                (training_df['charging_current'] < 10) |
                (training_df['charging_current'] > 80)
            )
            
            # Create failure component column
            training_df['failure_component'] = 0  # None
            training_df.loc[battery_failure, 'failure_component'] = 1  # Battery
            training_df.loc[motor_failure & ~battery_failure, 'failure_component'] = 2  # Motor
            training_df.loc[charging_failure & ~battery_failure & ~motor_failure, 'failure_component'] = 3  # Charging
            
            # Create binary failure indicator (will fail in next 30 days)
            training_df['will_fail'] = (training_df['failure_component'] > 0).astype(int)
            
            # Add failure probability (based on severity)
            training_df['failure_probability'] = np.where(
                training_df['failure_component'] > 0,
                np.random.uniform(0.5, 0.95, len(training_df)),
                np.random.uniform(0.0, 0.3, len(training_df))
            )
            
            # Save training data
            if output_path:
                training_df.to_csv(output_path, index=False)
                logger.info(f"Training data saved: {output_path}")
            
            logger.info(f"Created training data: {len(training_df)} records")
            logger.info(f"Failure cases: {training_df['will_fail'].sum()} ({training_df['will_fail'].mean():.2%})")
            
            return training_df
            
        except Exception as e:
            logger.error(f"Training data creation failed: {e}")
            raise
    
    def load_and_preprocess(self, user_type: str = None, 
                           output_path: str = None) -> pd.DataFrame:
        """
        Load and preprocess dataset in one step
        
        Args:
            user_type: Specific user type to load
            output_path: Path to save preprocessed data
            
        Returns:
            Preprocessed DataFrame
        """
        try:
            # Load dataset
            df = self.load_dataset(user_type=user_type)
            
            # Preprocess
            df = self.preprocess_dataset(df)
            
            # Save preprocessed data
            if output_path:
                df.to_csv(output_path, index=False)
                logger.info(f"Preprocessed data saved: {output_path}")
            
            return df
            
        except Exception as e:
            logger.error(f"Load and preprocess failed: {e}")
            raise

def main():
    """Example usage"""
    loader = EVDatasetLoader()
    
    print("Loading EV Sensors: Driving Pattern Diagnostics dataset...")
    
    # Load all user types
    df = loader.load_and_preprocess(
        output_path=DATA_DIR / "processed" / "ev_sensor_data.csv"
    )
    
    print(f"\nLoaded {len(df)} records")
    print(f"User types: {df['user_type'].unique() if 'user_type' in df.columns else 'N/A'}")
    print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    
    # Create training data
    training_df = loader.create_training_data(
        df,
        output_path=DATA_DIR / "processed" / "training_data.csv"
    )
    
    print(f"\nTraining data created: {len(training_df)} records")
    print(f"Failure rate: {training_df['will_fail'].mean():.2%}")

if __name__ == '__main__':
    main()

