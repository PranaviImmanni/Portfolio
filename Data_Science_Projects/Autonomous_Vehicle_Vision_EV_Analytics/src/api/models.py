"""
API Data Models
"""
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class DetectionResult:
    """Object detection result"""
    class_name: str
    confidence: float
    bbox: Dict[str, float]
    
    def to_dict(self):
        return {
            'class': self.class_name,
            'confidence': self.confidence,
            'bbox': self.bbox
        }

@dataclass
class FailurePrediction:
    """Failure prediction result"""
    failure_probability: float
    component: str
    severity: str
    recommended_action: str
    confidence: float
    
    def to_dict(self):
        return {
            'failure_probability': self.failure_probability,
            'component': self.component,
            'severity': self.severity,
            'recommended_action': self.recommended_action,
            'confidence': self.confidence
        }

@dataclass
class SensorData:
    """Sensor data model"""
    vehicle_id: str
    timestamp: str
    battery_voltage: float
    battery_temp: float
    motor_temp: float
    charging_current: float
    mileage: int
    
    def to_dict(self):
        return {
            'vehicle_id': self.vehicle_id,
            'timestamp': self.timestamp,
            'battery_voltage': self.battery_voltage,
            'battery_temp': self.battery_temp,
            'motor_temp': self.motor_temp,
            'charging_current': self.charging_current,
            'mileage': self.mileage
        }

