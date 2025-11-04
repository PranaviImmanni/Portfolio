"""
Sample Data Generator for EV Sensor Analytics
Generates realistic sensor telemetry data for testing and demonstration
"""
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional
from config import DATA_DIR
from src.utils.logger import get_logger

logger = get_logger(__name__)

class SampleDataGenerator:
    """Generate sample EV sensor data"""
    
    def __init__(self, num_vehicles: int = 10, days: int = 30):
        """
        Initialize data generator
        
        Args:
            num_vehicles: Number of vehicles to generate data for
            days: Number of days of data to generate
        """
        self.num_vehicles = num_vehicles
        self.days = days
        self.vehicle_ids = [f'EV_{i:03d}' for i in range(1, num_vehicles + 1)]
    
    def generate_sensor_data(self, output_path: str = None) -> pd.DataFrame:
        """
        Generate sensor telemetry data
        
        Args:
            output_path: Path to save CSV file
            
        Returns:
            DataFrame with sensor data
        """
        try:
            # Generate timestamps (hourly data)
            start_date = datetime.now() - timedelta(days=self.days)
            timestamps = pd.date_range(
                start=start_date,
                periods=self.days * 24,
                freq='H'
            )
            
            data = []
            
            for vehicle_id in self.vehicle_ids:
                # Base values for each vehicle
                base_voltage = np.random.uniform(380, 420)
                base_battery_temp = np.random.uniform(30, 40)
                base_motor_temp = np.random.uniform(35, 45)
                base_charging_current = np.random.uniform(40, 50)
                base_mileage = np.random.randint(1000, 50000)
                
                # Add some degradation over time
                for i, timestamp in enumerate(timestamps):
                    # Simulate gradual degradation
                    degradation = i / (self.days * 24) * 0.1
                    
                    # Generate sensor readings with realistic variation
                    battery_voltage = base_voltage * (1 - degradation) + np.random.normal(0, 5)
                    battery_temp = base_battery_temp + np.random.normal(0, 3)
                    motor_temp = base_motor_temp + np.random.normal(0, 3)
                    charging_current = base_charging_current + np.random.normal(0, 5)
                    
                    # Add some anomalies (5% of data)
                    if np.random.random() < 0.05:
                        battery_voltage *= np.random.uniform(0.8, 0.9)
                        battery_temp += np.random.uniform(10, 20)
                    
                    # Calculate derived values
                    battery_cycles = int(base_mileage / 100 + i / 24)
                    motor_rpm = np.random.uniform(2500, 3500)
                    cooling_system_temp = motor_temp - np.random.uniform(5, 10)
                    brake_pressure = np.random.uniform(40, 60)
                    
                    data.append({
                        'vehicle_id': vehicle_id,
                        'timestamp': timestamp,
                        'battery_voltage': round(battery_voltage, 2),
                        'battery_temp': round(battery_temp, 2),
                        'motor_temp': round(motor_temp, 2),
                        'charging_current': round(charging_current, 2),
                        'mileage': base_mileage + int(i * 2),
                        'battery_cycles': battery_cycles,
                        'motor_rpm': round(motor_rpm, 0),
                        'cooling_system_temp': round(cooling_system_temp, 2),
                        'brake_pressure': round(brake_pressure, 2)
                    })
            
            df = pd.DataFrame(data)
            
            # Save to CSV
            if output_path is None:
                output_path = DATA_DIR / "sample" / "sensor_data.csv"
            
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(output_path, index=False)
            
            logger.info(f"Generated {len(df)} sensor records for {self.num_vehicles} vehicles")
            logger.info(f"Data saved to: {output_path}")
            
            return df
            
        except Exception as e:
            logger.error(f"Data generation failed: {e}")
            raise
    
    def generate_training_data(self, output_path: str = None) -> pd.DataFrame:
        """
        Generate training data with failure labels
        
        Args:
            output_path: Path to save CSV file
            
        Returns:
            DataFrame with training data and labels
        """
        try:
            # Generate base sensor data
            df = self.generate_sensor_data()
            
            # Add failure labels based on sensor readings
            failure_labels = []
            failure_components = []
            
            for _, row in df.iterrows():
                will_fail = False
                component = 'none'
                
                # Battery failure indicators
                if row['battery_voltage'] < 350 or row['battery_temp'] > 50:
                    will_fail = np.random.random() < 0.8
                    component = 'battery' if will_fail else 'none'
                
                # Motor failure indicators
                elif row['motor_temp'] > 55 or row['cooling_system_temp'] > 60:
                    will_fail = np.random.random() < 0.7
                    component = 'motor' if will_fail else 'none'
                
                # Charging system failure indicators
                elif row['charging_current'] < 20 or row['charging_current'] > 70:
                    will_fail = np.random.random() < 0.6
                    component = 'charging_system' if will_fail else 'none'
                
                # Random failures (5% chance)
                elif np.random.random() < 0.05:
                    will_fail = True
                    component = np.random.choice(['battery', 'motor', 'charging_system', 
                                                 'cooling_system', 'brake_system'])
                
                failure_labels.append(will_fail)
                failure_components.append(component)
            
            df['will_fail'] = failure_labels
            df['failure_component'] = failure_components
            
            # Map components to numeric values
            component_map = {
                'none': 0,
                'battery': 1,
                'motor': 2,
                'charging_system': 3,
                'cooling_system': 4,
                'brake_system': 5
            }
            df['failure_component'] = df['failure_component'].map(component_map)
            
            # Save to CSV
            if output_path is None:
                output_path = DATA_DIR / "sample" / "training_data.csv"
            
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(output_path, index=False)
            
            logger.info(f"Generated training data with {df['will_fail'].sum()} failure cases")
            logger.info(f"Data saved to: {output_path}")
            
            return df
            
        except Exception as e:
            logger.error(f"Training data generation failed: {e}")
            raise
    
    def generate_vehicle_info(self, output_path: str = None) -> pd.DataFrame:
        """
        Generate vehicle information
        
        Args:
            output_path: Path to save CSV file
            
        Returns:
            DataFrame with vehicle information
        """
        try:
            manufacturers = ['Tesla', 'Nissan', 'BMW', 'Chevrolet', 'Hyundai']
            models = {
                'Tesla': ['Model 3', 'Model S', 'Model Y'],
                'Nissan': ['Leaf', 'Ariya'],
                'BMW': ['i3', 'iX'],
                'Chevrolet': ['Bolt', 'Volt'],
                'Hyundai': ['Kona Electric', 'Ioniq']
            }
            
            data = []
            for vehicle_id in self.vehicle_ids:
                manufacturer = np.random.choice(manufacturers)
                model = np.random.choice(models[manufacturer])
                year = np.random.randint(2020, 2024)
                
                data.append({
                    'vehicle_id': vehicle_id,
                    'vehicle_type': 'EV',
                    'manufacturer': manufacturer,
                    'model': model,
                    'year': year,
                    'total_mileage': np.random.randint(1000, 50000),
                    'registration_date': datetime(year, 1, 1).strftime('%Y-%m-%d')
                })
            
            df = pd.DataFrame(data)
            
            # Save to CSV
            if output_path is None:
                output_path = DATA_DIR / "sample" / "vehicles.csv"
            
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(output_path, index=False)
            
            logger.info(f"Generated vehicle information for {len(df)} vehicles")
            logger.info(f"Data saved to: {output_path}")
            
            return df
            
        except Exception as e:
            logger.error(f"Vehicle info generation failed: {e}")
            raise

def main():
    """Generate all sample data"""
    generator = SampleDataGenerator(num_vehicles=10, days=30)
    
    print("Generating sample data...")
    generator.generate_sensor_data()
    generator.generate_training_data()
    generator.generate_vehicle_info()
    print("Sample data generation complete!")

if __name__ == '__main__':
    main()

