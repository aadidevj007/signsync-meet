"""
Sign Language Recognition Inference Script
This script provides real-time sign language recognition using the trained model.
"""

import cv2
import numpy as np
import tensorflow as tf
import mediapipe as mp
import json
import os
import logging
from typing import Optional, Tuple, Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SignLanguageInference:
    def __init__(self, model_path="models/sign_language_model.h5"):
        self.model_path = model_path
        self.img_size = (64, 64)
        self.model = None
        self.asl_alphabet = {}
        self.reverse_alphabet = {}
        
        # Initialize MediaPipe
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        # Load model and metadata
        self.load_model()
        self.load_metadata()

    def load_model(self):
        """
        Load the trained model
        """
        try:
            if os.path.exists(self.model_path):
                self.model = tf.keras.models.load_model(self.model_path)
                logger.info(f"Model loaded successfully from {self.model_path}")
            else:
                logger.error(f"Model file not found: {self.model_path}")
                self.model = None
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            self.model = None

    def load_metadata(self):
        """
        Load model metadata
        """
        try:
            metadata_path = os.path.join(os.path.dirname(self.model_path), 'model_info.json')
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                    self.asl_alphabet = metadata.get('classes', {})
                    self.reverse_alphabet = {v: k for k, v in self.asl_alphabet.items()}
                logger.info("Model metadata loaded successfully")
            else:
                # Default alphabet mapping
                self.asl_alphabet = {
                    'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9,
                    'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19,
                    'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25, 'SPACE': 26, 'DELETE': 27, 'NOTHING': 28
                }
                self.reverse_alphabet = {v: k for k, v in self.asl_alphabet.items()}
                logger.warning("Using default alphabet mapping")
        except Exception as e:
            logger.error(f"Error loading metadata: {str(e)}")

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for model input
        """
        try:
            # Resize to model input size
            resized = cv2.resize(image, self.img_size)
            
            # Normalize pixel values
            normalized = resized.astype(np.float32) / 255.0
            
            # Add batch dimension
            return np.expand_dims(normalized, axis=0)
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            return None

    def extract_hand_region(self, image: np.ndarray) -> Optional[np.ndarray]:
        """
        Extract hand region from image using MediaPipe
        """
        try:
            # Convert BGR to RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Process the image
            results = self.hands.process(rgb_image)
            
            if results.multi_hand_landmarks:
                # Get the first hand
                hand_landmarks = results.multi_hand_landmarks[0]
                
                # Get bounding box
                h, w, _ = image.shape
                x_coords = [landmark.x * w for landmark in hand_landmarks.landmark]
                y_coords = [landmark.y * h for landmark in hand_landmarks.landmark]
                
                x_min, x_max = int(min(x_coords)), int(max(x_coords))
                y_min, y_max = int(min(y_coords)), int(max(y_coords))
                
                # Add padding
                padding = 20
                x_min = max(0, x_min - padding)
                y_min = max(0, y_min - padding)
                x_max = min(w, x_max + padding)
                y_max = min(h, y_max + padding)
                
                # Extract hand region
                hand_region = image[y_min:y_max, x_min:x_max]
                
                return hand_region
            
            return None
        except Exception as e:
            logger.error(f"Error extracting hand region: {str(e)}")
            return None

    def predict_sign(self, image: np.ndarray) -> Tuple[Optional[str], float]:
        """
        Predict sign language from image
        """
        try:
            if self.model is None:
                return None, 0.0
            
            # Extract hand region
            hand_region = self.extract_hand_region(image)
            
            if hand_region is None:
                return None, 0.0
            
            # Preprocess image
            processed_image = self.preprocess_image(hand_region)
            
            if processed_image is None:
                return None, 0.0
            
            # Make prediction
            predictions = self.model.predict(processed_image, verbose=0)
            predicted_class = np.argmax(predictions[0])
            confidence = float(np.max(predictions[0]))
            
            # Get class name
            class_name = self.reverse_alphabet.get(predicted_class, 'UNKNOWN')
            
            return class_name, confidence
        except Exception as e:
            logger.error(f"Error predicting sign: {str(e)}")
            return None, 0.0

    def is_ready(self) -> bool:
        """
        Check if the model is ready for inference
        """
        return self.model is not None

    def get_supported_classes(self) -> list:
        """
        Get list of supported sign language classes
        """
        return list(self.asl_alphabet.keys())

    def cleanup(self):
        """
        Cleanup resources
        """
        if hasattr(self, 'hands'):
            self.hands.close()
        logger.info("Sign Language Inference cleaned up")

def main():
    """
    Main function for testing the inference
    """
    # Initialize inference
    inference = SignLanguageInference()
    
    if not inference.is_ready():
        logger.error("Model not ready for inference!")
        return
    
    # Test with webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        logger.error("Could not open webcam!")
        return
    
    logger.info("Starting real-time sign language recognition...")
    logger.info("Press 'q' to quit")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Predict sign
        sign, confidence = inference.predict_sign(frame)
        
        # Draw results on frame
        if sign and confidence > 0.7:
            cv2.putText(frame, f"Sign: {sign}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Confidence: {confidence:.2f}", (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "No sign detected", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Show frame
        cv2.imshow('Sign Language Recognition', frame)
        
        # Break on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    inference.cleanup()
    
    logger.info("Sign language recognition stopped")

if __name__ == "__main__":
    main()
