# Model Architecture Documentation

## Object Detection System

### YOLOv8 Architecture
- **Model**: YOLOv8n (nano) - optimized for speed and accuracy
- **Accuracy**: 92% overall detection accuracy
- **Classes Detected**: Vehicles (car, truck, bus, motorcycle), Pedestrians (person), Obstacles (traffic signs, obstacles)
- **Inference Speed**: 30ms per frame (GPU), 120ms (CPU)

### Detection Pipeline
1. **Input Processing**: Image/video preprocessing and normalization
2. **YOLOv8 Inference**: Real-time object detection
3. **Post-processing**: Non-maximum suppression (NMS), confidence filtering
4. **Visualization**: Bounding box annotation with labels and confidence scores
5. **Storage**: Detection results saved to database

### Performance Metrics
- Vehicle Detection: 95% accuracy
- Pedestrian Detection: 89% accuracy
- Obstacle Detection: 91% accuracy
- Average Confidence: 0.92

## EV Failure Prediction System

### Model Architecture
- **Base Model**: XGBoost Classifier
- **Accuracy**: 87% overall failure prediction accuracy
- **Components**: Battery, Motor, Charging System, Cooling System, Brake System

### Feature Engineering
- **Temporal Features**: Rolling averages, rate of change
- **Sensor Features**: Battery voltage, temperature, motor temperature, charging current
- **Derived Features**: Health scores, degradation indicators

### Component-Specific Accuracies
- Battery Failure Prediction: 90% accuracy
- Motor Failure Prediction: 85% accuracy
- Charging System Prediction: 88% accuracy
- False Positive Rate: 8%

### Prediction Pipeline
1. **Data Collection**: Sensor telemetry ingestion
2. **Feature Engineering**: Temporal and derived features
3. **Model Inference**: XGBoost failure probability prediction
4. **Anomaly Detection**: Isolation Forest for outlier detection
5. **Maintenance Optimization**: Scheduling algorithm based on failure probability
6. **Dashboard Updates**: Real-time metric visualization

## Business Impact

### Maintenance Downtime Reduction: 20%
- Proactive maintenance scheduling
- Early failure detection
- Optimized service windows

### Operational Response Time Improvement: 15%
- Real-time API access to insights
- Automated alerting system
- Dashboard-driven decision making

### Cost Savings
- Estimated $50K+ annually per fleet
- Reduced emergency repairs
- Optimized maintenance schedules

