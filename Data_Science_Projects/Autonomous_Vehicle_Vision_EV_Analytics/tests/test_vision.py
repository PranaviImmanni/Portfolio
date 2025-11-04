"""
Tests for vision module
"""
import pytest
import numpy as np
from PIL import Image
from pathlib import Path
from src.vision.object_detector import ObjectDetector

def test_object_detector_initialization():
    """Test object detector initialization"""
    detector = ObjectDetector()
    assert detector.model is not None
    assert detector.confidence_threshold == 0.5

def test_detection_statistics():
    """Test detection statistics calculation"""
    detector = ObjectDetector()
    
    sample_detections = [
        {'class': 'car', 'confidence': 0.95},
        {'class': 'person', 'confidence': 0.87},
        {'class': 'car', 'confidence': 0.92}
    ]
    
    stats = detector.get_detection_statistics(sample_detections)
    assert stats['total_detections'] == 3
    assert 'avg_confidence' in stats
    assert stats['accuracy'] == 0.92

