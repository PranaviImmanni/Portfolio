# Deployment Guide

## Local Development Setup

### Prerequisites
- Python 3.9+
- PostgreSQL 14+ or MySQL 8.0+
- Virtual environment (recommended)

### Installation Steps

1. **Clone and Navigate**
   ```bash
   cd Autonomous_Vehicle_Vision_EV_Analytics
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. **Initialize Database**
   ```bash
   python main.py --mode init
   ```

6. **Generate Sample Data (Optional)**
   ```bash
   python data/sample_data_generator.py
   ```

7. **Train Models (Optional)**
   ```bash
   python main.py --mode train
   ```

## Running the Application

### Start API Server
```bash
python main.py --mode api
# Or
python src/api/app.py
```

API will be available at: `http://localhost:5000`

### Run Object Detection
```bash
# Image detection
python main.py --mode detect --image path/to/image.jpg

# Video detection
python main.py --mode detect --video path/to/video.mp4

# Webcam detection
python main.py --mode detect
```

### Run EV Analytics
```bash
python main.py --mode analytics
```

### Generate Dashboards
```bash
python main.py --mode dashboard
```

## Docker Deployment

### Build Docker Image
```bash
docker build -t ev-vision-analytics .
```

### Run Container
```bash
docker run -p 5000:5000 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  ev-vision-analytics
```

### Docker Compose
```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/ev_analytics
    depends_on:
      - db
  
  db:
    image: postgres:14
    environment:
      - POSTGRES_DB=ev_analytics
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## AWS Deployment

### EC2 Deployment
1. Launch EC2 instance (Ubuntu 20.04 LTS)
2. Install Python 3.9+ and dependencies
3. Clone repository
4. Configure environment variables
5. Use systemd or supervisor for process management

### Lambda Deployment (API)
1. Package application with dependencies
2. Deploy to AWS Lambda
3. Configure API Gateway
4. Set environment variables

### S3 Model Storage
```bash
# Upload models to S3
python -c "from src.utils.aws_utils import AWSManager; \
           manager = AWSManager(); \
           manager.upload_model('models/ev_models/failure_predictor.pkl')"
```

## Production Considerations

### Performance Optimization
- Use GPU for inference (CUDA)
- Enable model caching
- Implement request queuing
- Use connection pooling for database

### Security
- Use environment variables for secrets
- Enable HTTPS/TLS
- Implement authentication/authorization
- Validate all inputs

### Monitoring
- Set up logging aggregation
- Monitor API response times
- Track model performance metrics
- Alert on failures

### Scaling
- Use load balancer for multiple instances
- Implement database replication
- Cache frequently accessed data
- Use CDN for static assets

