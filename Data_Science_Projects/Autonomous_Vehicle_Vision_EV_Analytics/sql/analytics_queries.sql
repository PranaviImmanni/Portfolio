-- Analytics Queries
-- Queries for dashboard metrics and insights

-- Overall system health metrics
SELECT 
    COUNT(DISTINCT v.vehicle_id) as total_vehicles,
    COUNT(DISTINCT st.vehicle_id) as vehicles_with_data,
    COUNT(st.id) as total_sensor_readings,
    COUNT(fp.id) as total_predictions,
    COUNT(CASE WHEN fp.severity = 'urgent' THEN 1 END) as urgent_predictions,
    COUNT(CASE WHEN fp.severity = 'high' THEN 1 END) as high_predictions,
    AVG(fp.failure_probability) as avg_failure_probability
FROM vehicles v
LEFT JOIN sensor_telemetry st ON v.vehicle_id = st.vehicle_id
LEFT JOIN failure_predictions fp ON v.vehicle_id = fp.vehicle_id;

-- Component failure distribution
SELECT 
    component,
    COUNT(*) as prediction_count,
    AVG(failure_probability) as avg_failure_probability,
    MAX(failure_probability) as max_failure_probability,
    COUNT(CASE WHEN severity = 'urgent' THEN 1 END) as urgent_count,
    COUNT(CASE WHEN severity = 'high' THEN 1 END) as high_count
FROM failure_predictions
WHERE prediction_timestamp >= CURRENT_TIMESTAMP - INTERVAL '30 days'
GROUP BY component
ORDER BY avg_failure_probability DESC;

-- Detection statistics
SELECT 
    detection_class,
    COUNT(*) as detection_count,
    AVG(confidence) as avg_confidence,
    MIN(confidence) as min_confidence,
    MAX(confidence) as max_confidence
FROM detection_results
WHERE timestamp >= CURRENT_TIMESTAMP - INTERVAL '7 days'
GROUP BY detection_class
ORDER BY detection_count DESC;

-- Vehicles requiring immediate attention
SELECT 
    v.vehicle_id,
    v.vehicle_type,
    fp.component,
    fp.failure_probability,
    fp.severity,
    fp.recommended_action,
    fp.prediction_timestamp,
    st.mileage
FROM vehicles v
JOIN failure_predictions fp ON v.vehicle_id = fp.vehicle_id
LEFT JOIN sensor_telemetry st ON v.vehicle_id = st.vehicle_id
WHERE fp.failure_probability >= 0.7
    AND fp.prediction_timestamp >= CURRENT_TIMESTAMP - INTERVAL '7 days'
ORDER BY fp.failure_probability DESC, fp.prediction_timestamp DESC;

-- Maintenance cost analysis
SELECT 
    mr.component,
    COUNT(*) as maintenance_count,
    SUM(mr.cost) as total_cost,
    AVG(mr.cost) as avg_cost,
    MIN(mr.maintenance_date) as first_maintenance,
    MAX(mr.maintenance_date) as last_maintenance
FROM maintenance_records mr
WHERE mr.maintenance_date >= CURRENT_DATE - INTERVAL '12 months'
GROUP BY mr.component
ORDER BY total_cost DESC;

-- Anomaly detection summary
SELECT 
    vehicle_id,
    COUNT(*) as total_anomalies,
    AVG(anomaly_score) as avg_anomaly_score,
    MIN(timestamp) as first_anomaly,
    MAX(timestamp) as last_anomaly
FROM anomaly_detections
WHERE is_anomaly = TRUE
    AND timestamp >= CURRENT_TIMESTAMP - INTERVAL '30 days'
GROUP BY vehicle_id
ORDER BY total_anomalies DESC;

