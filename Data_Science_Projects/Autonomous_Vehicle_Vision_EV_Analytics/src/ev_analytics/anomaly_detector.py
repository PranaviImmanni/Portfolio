"""
Anomaly Detection for EV Sensor Data
"""
import numpy as np
import pandas as pd
from typing import Dict, List
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from src.utils.logger import get_logger

logger = get_logger(__name__)

class AnomalyDetector:
    """Detect anomalies in EV sensor data"""
    
    def __init__(self, contamination: float = 0.1):
        """
        Initialize anomaly detector
        
        Args:
            contamination: Expected proportion of anomalies
        """
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.scaler = StandardScaler()
        self.feature_names = [
            'battery_voltage', 'battery_temp', 'motor_temp',
            'charging_current', 'cooling_system_temp'
        ]
    
    def detect_anomalies(self, sensor_data: pd.DataFrame) -> pd.DataFrame:
        """
        Detect anomalies in sensor data
        
        Args:
            sensor_data: DataFrame with sensor readings
            
        Returns:
            DataFrame with anomaly labels
        """
        try:
            # Prepare features
            available_features = [f for f in self.feature_names if f in sensor_data.columns]
            X = sensor_data[available_features].copy()
            
            # Handle missing values
            X = X.fillna(X.median())
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Fit model
            self.model.fit(X_scaled)
            
            # Predict anomalies
            predictions = self.model.predict(X_scaled)
            anomaly_scores = self.model.score_samples(X_scaled)
            
            # Add results to dataframe
            sensor_data = sensor_data.copy()
            sensor_data['is_anomaly'] = predictions == -1
            sensor_data['anomaly_score'] = anomaly_scores
            
            n_anomalies = (predictions == -1).sum()
            logger.info(f"Detected {n_anomalies} anomalies out of {len(sensor_data)} records")
            
            return sensor_data
            
        except Exception as e:
            logger.error(f"Anomaly detection failed: {e}")
            raise

