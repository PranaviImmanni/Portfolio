-- Database Setup Script for Autonomous Vehicle Vision & EV Analytics
-- PostgreSQL/MySQL compatible schema

-- Sensor Telemetry Table
CREATE TABLE IF NOT EXISTS sensor_telemetry (
    id SERIAL PRIMARY KEY,
    vehicle_id VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    battery_voltage FLOAT,
    battery_temp FLOAT,
    motor_temp FLOAT,
    charging_current FLOAT,
    mileage INTEGER,
    battery_cycles INTEGER,
    motor_rpm FLOAT,
    cooling_system_temp FLOAT,
    brake_pressure FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_vehicle_id (vehicle_id),
    INDEX idx_timestamp (timestamp)
);

-- Detection Results Table
CREATE TABLE IF NOT EXISTS detection_results (
    id SERIAL PRIMARY KEY,
    image_path VARCHAR(255),
    detection_class VARCHAR(50) NOT NULL,
    confidence FLOAT NOT NULL,
    bbox_x1 FLOAT,
    bbox_y1 FLOAT,
    bbox_x2 FLOAT,
    bbox_y2 FLOAT,
    vehicle_id VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_detection_class (detection_class),
    INDEX idx_confidence (confidence),
    INDEX idx_timestamp (timestamp)
);

-- Failure Predictions Table
CREATE TABLE IF NOT EXISTS failure_predictions (
    id SERIAL PRIMARY KEY,
    vehicle_id VARCHAR(50) NOT NULL,
    prediction_timestamp TIMESTAMP NOT NULL,
    failure_probability FLOAT NOT NULL,
    component VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    recommended_action TEXT,
    confidence FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_vehicle_id (vehicle_id),
    INDEX idx_component (component),
    INDEX idx_severity (severity),
    INDEX idx_failure_probability (failure_probability),
    INDEX idx_prediction_timestamp (prediction_timestamp)
);

-- Vehicle Information Table
CREATE TABLE IF NOT EXISTS vehicles (
    id SERIAL PRIMARY KEY,
    vehicle_id VARCHAR(50) UNIQUE NOT NULL,
    vehicle_type VARCHAR(50),
    manufacturer VARCHAR(50),
    model VARCHAR(50),
    year INTEGER,
    total_mileage INTEGER,
    registration_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Maintenance Records Table
CREATE TABLE IF NOT EXISTS maintenance_records (
    id SERIAL PRIMARY KEY,
    vehicle_id VARCHAR(50) NOT NULL,
    maintenance_date DATE NOT NULL,
    component VARCHAR(50) NOT NULL,
    maintenance_type VARCHAR(50),
    cost FLOAT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_vehicle_id (vehicle_id),
    INDEX idx_maintenance_date (maintenance_date),
    INDEX idx_component (component)
);

-- Anomaly Detection Table
CREATE TABLE IF NOT EXISTS anomaly_detections (
    id SERIAL PRIMARY KEY,
    vehicle_id VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    sensor_type VARCHAR(50),
    sensor_value FLOAT,
    anomaly_score FLOAT,
    is_anomaly BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_vehicle_id (vehicle_id),
    INDEX idx_timestamp (timestamp),
    INDEX idx_is_anomaly (is_anomaly)
);

-- Analytics Summary View
CREATE VIEW IF NOT EXISTS analytics_summary AS
SELECT 
    v.vehicle_id,
    v.vehicle_type,
    COUNT(DISTINCT st.id) as total_sensor_readings,
    AVG(st.battery_voltage) as avg_battery_voltage,
    AVG(st.battery_temp) as avg_battery_temp,
    AVG(st.motor_temp) as avg_motor_temp,
    MAX(st.timestamp) as last_sensor_update,
    MAX(fp.prediction_timestamp) as last_prediction,
    MAX(fp.failure_probability) as max_failure_probability,
    COUNT(CASE WHEN fp.severity = 'urgent' THEN 1 END) as urgent_predictions,
    COUNT(CASE WHEN ad.is_anomaly = TRUE THEN 1 END) as total_anomalies
FROM vehicles v
LEFT JOIN sensor_telemetry st ON v.vehicle_id = st.vehicle_id
LEFT JOIN failure_predictions fp ON v.vehicle_id = fp.vehicle_id
LEFT JOIN anomaly_detections ad ON v.vehicle_id = ad.vehicle_id
GROUP BY v.vehicle_id, v.vehicle_type;

-- Recent Predictions View
CREATE VIEW IF NOT EXISTS recent_predictions AS
SELECT 
    vehicle_id,
    component,
    failure_probability,
    severity,
    recommended_action,
    prediction_timestamp,
    confidence
FROM failure_predictions
WHERE prediction_timestamp >= CURRENT_TIMESTAMP - INTERVAL '7 days'
ORDER BY failure_probability DESC, prediction_timestamp DESC;

-- High Risk Vehicles View
CREATE VIEW IF NOT EXISTS high_risk_vehicles AS
SELECT 
    vehicle_id,
    component,
    failure_probability,
    severity,
    recommended_action,
    prediction_timestamp
FROM failure_predictions
WHERE failure_probability >= 0.7
ORDER BY failure_probability DESC;

