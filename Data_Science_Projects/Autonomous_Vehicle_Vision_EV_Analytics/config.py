"""
Configuration file for Autonomous Vehicle Vision & EV Analytics
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"
SQL_DIR = PROJECT_ROOT / "sql"

# Database configuration
DATABASE_CONFIG = {
    "postgresql": {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", "5432"),
        "database": os.getenv("DB_NAME", "ev_analytics"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "postgres")
    },
    "mysql": {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", "3306"),
        "database": os.getenv("DB_NAME", "ev_analytics"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", "")
    }
}

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql://{DATABASE_CONFIG['postgresql']['user']}:{DATABASE_CONFIG['postgresql']['password']}@{DATABASE_CONFIG['postgresql']['host']}:{DATABASE_CONFIG['postgresql']['port']}/{DATABASE_CONFIG['postgresql']['database']}"
)

# AWS configuration
AWS_CONFIG = {
    "access_key_id": os.getenv("AWS_ACCESS_KEY_ID", ""),
    "secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY", ""),
    "region": os.getenv("AWS_REGION", "us-east-1"),
    "s3_bucket": os.getenv("AWS_S3_BUCKET", "ev-analytics-models"),
    "s3_model_path": "models/"
}

# Model paths
YOLO_MODEL_PATH = MODELS_DIR / "yolo_weights" / "yolov8n.pt"
EV_MODEL_PATH = MODELS_DIR / "ev_models" / "failure_predictor.pkl"

# Object detection configuration
DETECTION_CONFIG = {
    "confidence_threshold": 0.5,
    "iou_threshold": 0.45,
    "image_size": 640,
    "classes": ["car", "truck", "bus", "motorcycle", "person", "bicycle", "traffic_sign", "obstacle"],
    "target_classes": {
        "vehicles": ["car", "truck", "bus", "motorcycle"],
        "pedestrians": ["person"],
        "obstacles": ["obstacle", "traffic_sign"]
    }
}

# EV Analytics configuration
EV_ANALYTICS_CONFIG = {
    "failure_threshold": 0.7,
    "prediction_window_days": 30,
    "sensor_update_interval": 60,  # seconds
    "components": ["battery", "motor", "charging_system", "brake_system", "cooling_system"],
    "maintenance_categories": {
        "urgent": 0.9,
        "high": 0.7,
        "medium": 0.5,
        "low": 0.3
    }
}

# API configuration
API_CONFIG = {
    "host": os.getenv("API_HOST", "0.0.0.0"),
    "port": int(os.getenv("API_PORT", "5000")),
    "debug": os.getenv("DEBUG", "False").lower() == "true",
    "max_upload_size": 16 * 1024 * 1024,  # 16MB
    "allowed_extensions": {"jpg", "jpeg", "png", "mp4", "avi", "mov"}
}

# Logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        }
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": PROJECT_ROOT / "logs" / "app.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5
        }
    },
    "loggers": {
        "": {
            "handlers": ["default", "file"],
            "level": "INFO",
            "propagate": False
        }
    }
}

