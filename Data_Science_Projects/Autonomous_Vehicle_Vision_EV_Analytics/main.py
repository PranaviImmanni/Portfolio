"""
Main Entry Point for Autonomous Vehicle Vision & EV Analytics
"""
import argparse
import sys
from pathlib import Path
from src.vision.object_detector import ObjectDetector
from src.ev_analytics.failure_predictor import FailurePredictor
from src.ev_analytics.sensor_processor import SensorProcessor
from src.visualization.dashboard import Dashboard
from src.utils.database import DatabaseManager, init_db
from src.utils.logger import get_logger
from config import DATA_DIR, MODELS_DIR, REPORTS_DIR

logger = get_logger(__name__)

def train_models(use_real_data: bool = False):
    """Train all models"""
    logger.info("Training models...")
    
    # Generate or load training data
    if use_real_data:
        # Use real Kaggle dataset
        logger.info("Loading real EV sensor dataset for training...")
        import sys
        sys.path.append(str(Path(__file__).parent))
        from data.data_loader import EVDatasetLoader
        
        loader = EVDatasetLoader()
        training_data_path = DATA_DIR / "processed" / "training_data.csv"
        
        if not training_data_path.exists():
            # Load and preprocess dataset
            df = loader.load_and_preprocess(
                output_path=str(DATA_DIR / "processed" / "ev_sensor_data.csv")
            )
            # Create training data with failure labels
            training_df = loader.create_training_data(df, str(training_data_path))
        else:
            logger.info("Training data already exists, using existing file")
    else:
        # Use synthetic data
        training_data_path = DATA_DIR / "sample" / "training_data.csv"
        if not training_data_path.exists():
            logger.info("Generating synthetic training data...")
            import sys
            sys.path.append(str(Path(__file__).parent))
            from data.sample_data_generator import SampleDataGenerator
            generator = SampleDataGenerator()
            generator.generate_training_data(str(training_data_path))
    
    # Train failure predictor
    logger.info("Training failure prediction model...")
    predictor = FailurePredictor()
    predictor.train_model(str(training_data_path))
    
    logger.info("Model training complete!")

def run_object_detection(image_path: str = None, video_path: str = None):
    """Run object detection on image or video"""
    logger.info("Initializing object detector...")
    detector = ObjectDetector()
    
    if image_path:
        logger.info(f"Processing image: {image_path}")
        detections = detector.detect_image(image_path, save_output=True)
        stats = detector.get_detection_statistics(detections)
        logger.info(f"Detection statistics: {stats}")
        
    elif video_path:
        logger.info(f"Processing video: {video_path}")
        output_path = REPORTS_DIR / "figures" / "detected_video.mp4"
        stats = detector.process_video(video_path, str(output_path))
        logger.info(f"Video processing statistics: {stats}")
        
    else:
        logger.info("Starting webcam detection...")
        detector.detect_webcam(show=True, save=False)

def run_ev_analytics(use_real_data: bool = False):
    """Run EV sensor analytics"""
    logger.info("Running EV sensor analytics...")
    
    # Process sensor data
    if use_real_data:
        # Use real Kaggle dataset
        logger.info("Loading real EV sensor dataset...")
        import sys
        sys.path.append(str(Path(__file__).parent))
        from data.data_loader import EVDatasetLoader
        
        loader = EVDatasetLoader()
        sensor_data_path = DATA_DIR / "processed" / "ev_sensor_data.csv"
        
        if not sensor_data_path.exists():
            df = loader.load_and_preprocess(output_path=str(sensor_data_path))
        else:
            import pandas as pd
            df = pd.read_csv(sensor_data_path)
    else:
        # Use synthetic data
        sensor_data_path = DATA_DIR / "sample" / "sensor_data.csv"
        if not sensor_data_path.exists():
            logger.info("Generating sample sensor data...")
            import sys
            sys.path.append(str(Path(__file__).parent))
            from data.sample_data_generator import SampleDataGenerator
            generator = SampleDataGenerator()
            generator.generate_sensor_data(str(sensor_data_path))
        import pandas as pd
        df = pd.read_csv(sensor_data_path)
    
    # Process sensor data
    processor = SensorProcessor()
    processed_data = processor.process_batch(
        str(sensor_data_path),
        str(DATA_DIR / "processed" / "processed_sensor_data.csv")
    )
    
    # Make predictions
    logger.info("Making failure predictions...")
    predictor = FailurePredictor()
    predictor.load_model(str(MODELS_DIR / "ev_models" / "failure_predictor.pkl"))
    
    # Sample predictions
    sample_data = processed_data.head(10)
    predictions = predictor.predict_batch(sample_data)
    
    logger.info(f"Generated {len(predictions)} failure predictions")
    logger.info(f"High risk vehicles: {(predictions['failure_probability'] >= 0.7).sum()}")

def generate_dashboards():
    """Generate dashboard visualizations"""
    logger.info("Generating dashboards...")
    
    dashboard = Dashboard()
    dashboard.generate_comprehensive_dashboard()
    
    logger.info("Dashboard generation complete!")

def run_api():
    """Run Flask API server"""
    logger.info("Starting Flask API server...")
    from src.api.app import create_app
    
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Autonomous Vehicle Vision & EV Sensor Analytics'
    )
    
    parser.add_argument(
        '--mode',
        type=str,
        choices=['detect', 'analytics', 'train', 'dashboard', 'api', 'init'],
        default='analytics',
        help='Operation mode'
    )
    
    parser.add_argument(
        '--image',
        type=str,
        help='Path to image file for detection'
    )
    
    parser.add_argument(
        '--video',
        type=str,
        help='Path to video file for detection'
    )
    
    parser.add_argument(
        '--use-real-data',
        action='store_true',
        help='Use real Kaggle dataset instead of synthetic data'
    )
    
    args = parser.parse_args()
    
    try:
        if args.mode == 'init':
            logger.info("Initializing database...")
            init_db()
            logger.info("Database initialized!")
            
        elif args.mode == 'train':
            train_models(use_real_data=args.use_real_data)
            
        elif args.mode == 'detect':
            run_object_detection(args.image, args.video)
            
        elif args.mode == 'analytics':
            run_ev_analytics(use_real_data=args.use_real_data)
            
        elif args.mode == 'dashboard':
            generate_dashboards()
            
        elif args.mode == 'api':
            run_api()
            
    except Exception as e:
        logger.error(f"Error: {e}")
        raise

if __name__ == '__main__':
    main()

