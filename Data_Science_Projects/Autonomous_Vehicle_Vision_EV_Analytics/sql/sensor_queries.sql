-- Sensor Data Queries
-- Common queries for sensor telemetry analysis

-- Get latest sensor readings for a vehicle
SELECT * FROM sensor_telemetry
WHERE vehicle_id = 'EV_001'
ORDER BY timestamp DESC
LIMIT 10;

-- Average sensor readings by vehicle
SELECT 
    vehicle_id,
    AVG(battery_voltage) as avg_battery_voltage,
    AVG(battery_temp) as avg_battery_temp,
    AVG(motor_temp) as avg_motor_temp,
    AVG(charging_current) as avg_charging_current,
    MAX(mileage) as total_mileage
FROM sensor_telemetry
GROUP BY vehicle_id;

-- Sensor readings in the last 24 hours
SELECT * FROM sensor_telemetry
WHERE timestamp >= CURRENT_TIMESTAMP - INTERVAL '24 hours'
ORDER BY timestamp DESC;

-- Sensor readings with anomalies
SELECT 
    st.*,
    ad.anomaly_score,
    ad.is_anomaly
FROM sensor_telemetry st
JOIN anomaly_detections ad ON st.vehicle_id = ad.vehicle_id 
    AND st.timestamp = ad.timestamp
WHERE ad.is_anomaly = TRUE
ORDER BY ad.anomaly_score DESC;

-- Temperature trends over time
SELECT 
    DATE(timestamp) as date,
    AVG(battery_temp) as avg_battery_temp,
    AVG(motor_temp) as avg_motor_temp,
    MAX(battery_temp) as max_battery_temp,
    MAX(motor_temp) as max_motor_temp
FROM sensor_telemetry
WHERE timestamp >= CURRENT_TIMESTAMP - INTERVAL '30 days'
GROUP BY DATE(timestamp)
ORDER BY date DESC;

-- Battery health analysis
SELECT 
    vehicle_id,
    AVG(battery_voltage) as avg_voltage,
    MIN(battery_voltage) as min_voltage,
    MAX(battery_voltage) as max_voltage,
    STDDEV(battery_voltage) as voltage_stddev,
    AVG(battery_temp) as avg_temp,
    MAX(battery_temp) as max_temp,
    CASE 
        WHEN AVG(battery_voltage) < 350 THEN 'Critical'
        WHEN AVG(battery_voltage) < 370 THEN 'Warning'
        ELSE 'Normal'
    END as battery_status
FROM sensor_telemetry
GROUP BY vehicle_id;

