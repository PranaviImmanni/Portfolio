# API Documentation

## Base URL
```
http://localhost:5000
```

## Endpoints

### 1. Health Check
**GET** `/health`

Returns API health status.

**Response:**
```json
{
  "status": "healthy",
  "service": "Autonomous Vehicle Vision & EV Analytics API",
  "version": "1.0.0"
}
```

### 2. Object Detection
**POST** `/api/v1/detect`

Detects objects in an uploaded image.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: image file (jpg, jpeg, png)

**Response:**
```json
{
  "detections": [
    {
      "class": "car",
      "confidence": 0.95,
      "bbox": {
        "x1": 100.0,
        "y1": 150.0,
        "x2": 300.0,
        "y2": 400.0
      }
    }
  ],
  "statistics": {
    "total_detections": 1,
    "avg_confidence": 0.95
  },
  "accuracy": 0.92,
  "total_detections": 1
}
```

### 3. Failure Prediction
**POST** `/api/v1/predict/failure`

Predicts EV component failure probability.

**Request:**
```json
{
  "battery_voltage": 380.5,
  "battery_temp": 35.2,
  "motor_temp": 42.1,
  "charging_current": 45.0,
  "mileage": 15000
}
```

**Response:**
```json
{
  "failure_probability": 0.15,
  "will_fail": false,
  "component": "battery",
  "severity": "medium",
  "recommended_action": "Schedule maintenance for battery within 2 weeks.",
  "confidence": 0.87,
  "prediction_window_days": 30
}
```

### 4. Dashboard Metrics
**GET** `/api/v1/dashboard/metrics?vehicle_id=EV_001`

Returns aggregated metrics for dashboard.

**Response:**
```json
{
  "total_records": 1000,
  "avg_battery_voltage": 385.5,
  "avg_battery_temp": 35.2,
  "avg_motor_temp": 42.1,
  "last_update": "2024-01-15T10:30:00"
}
```

### 5. Sensor Data Stream
**POST** `/api/v1/sensors/stream`

Stream sensor data for real-time analysis.

**Request:** JSON array of sensor records

**Response:**
```json
{
  "total_records": 100,
  "anomalies_detected": 5,
  "anomaly_rate": 0.05,
  "anomalies": [...]
}
```

### 6. Batch Prediction
**POST** `/api/v1/predict/batch`

Batch failure prediction from CSV file.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: CSV file with sensor data

**Response:**
```json
{
  "predictions": [...],
  "total_predictions": 100,
  "high_risk_count": 5
}
```

## Error Responses

All endpoints return standard error responses:

```json
{
  "error": "Error message"
}
```

HTTP Status Codes:
- 200: Success
- 400: Bad Request
- 404: Not Found
- 500: Internal Server Error

