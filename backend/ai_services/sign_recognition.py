import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from typing import Optional, Dict, Any
import logging
import os
from datetime import datetime

class SignLanguageRecognizer:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        # Load the trained CNN model
        self.model = self.load_model()
        self.is_model_ready = self.model is not None
        
        # ASL alphabet mapping
        self.asl_alphabet = {
            0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J',
            10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T',
            20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z', 26: 'SPACE', 27: 'DELETE', 28: 'NOTHING'
        }
        
        # Common sign language phrases
        self.common_phrases = {
            'HELLO': ['H', 'E', 'L', 'L', 'O'],
            'THANK YOU': ['T', 'H', 'A', 'N', 'K', ' ', 'Y', 'O', 'U'],
            'YES': ['Y', 'E', 'S'],
            'NO': ['N', 'O'],
            'PLEASE': ['P', 'L', 'E', 'A', 'S', 'E'],
            'SORRY': ['S', 'O', 'R', 'R', 'Y'],
            'GOOD': ['G', 'O', 'O', 'D'],
            'BAD': ['B', 'A', 'D'],
            'HELP': ['H', 'E', 'L', 'P'],
            'WATER': ['W', 'A', 'T', 'E', 'R'],
            'FOOD': ['F', 'O', 'O', 'D'],
            'HOME': ['H', 'O', 'M', 'E']
        }
        
        self.sequence_buffer = []
        self.max_sequence_length = 10
        
        logging.info("Sign Language Recognizer initialized")

    def load_model(self) -> Optional[tf.keras.Model]:
        """
        Load the pre-trained ASL CNN model from Kaggle dataset
        """
        try:
            # Load the pre-trained ASL model
            model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'asl_model.h5')
            
            if os.path.exists(model_path):
                model = tf.keras.models.load_model(model_path)
                logging.info("Pre-trained ASL model loaded successfully from asl_model.h5")
                return model
            else:
                logging.error(f"ASL model not found at {model_path}")
                return None
                
        except Exception as e:
            logging.error(f"Error loading ASL model: {str(e)}")
            return None

    def create_simple_model(self) -> tf.keras.Model:
        """
        Create a simple CNN model for demonstration
        """
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(29, activation='softmax')  # 26 letters + space + delete + nothing
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model

    def extract_hand_features(self, image: np.ndarray) -> Optional[np.ndarray]:
        """
        Extract hand landmarks and features from image
        """
        try:
            # Convert BGR to RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Process the image
            results = self.hands.process(rgb_image)
            
            if results.multi_hand_landmarks:
                # Get the first hand
                hand_landmarks = results.multi_hand_landmarks[0]
                
                # Extract landmark coordinates
                landmarks = []
                for landmark in hand_landmarks.landmark:
                    landmarks.extend([landmark.x, landmark.y, landmark.z])
                
                return np.array(landmarks)
            
            return None
            
        except Exception as e:
            logging.error(f"Error extracting hand features: {str(e)}")
            return None

    def preprocess_image_for_asl(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for ASL model input (28x28 grayscale)
        """
        try:
            # Convert to grayscale
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            
            # Resize to 28x28 (ASL model input size)
            resized = cv2.resize(gray, (28, 28))
            
            # Normalize pixel values to 0-1
            normalized = resized.astype(np.float32) / 255.0
            
            # Reshape for model input (28, 28, 1)
            reshaped = np.expand_dims(normalized, axis=-1)
            
            # Add batch dimension
            return np.expand_dims(reshaped, axis=0)
        except Exception as e:
            logging.error(f"Error preprocessing image for ASL: {str(e)}")
            return None

    def predict_sign(self, image: np.ndarray) -> Optional[str]:
        """
        Predict sign language from image using pre-trained ASL model
        """
        try:
            if not self.is_model_ready or self.model is None:
                logging.warning("ASL model not ready, using simulation")
                return self.simulate_prediction()
            
            # Preprocess image for ASL model (28x28 grayscale)
            processed_image = self.preprocess_image_for_asl(image)
            if processed_image is None:
                return None
            
            # Make prediction
            predictions = self.model.predict(processed_image, verbose=0)
            predicted_class = np.argmax(predictions[0])
            confidence = np.max(predictions[0])
            
            # Only return prediction if confidence is high enough
            if confidence > 0.7:
                return self.asl_alphabet.get(predicted_class, 'UNKNOWN')
            
            return None
            
        except Exception as e:
            logging.error(f"Error predicting sign: {str(e)}")
            return self.simulate_prediction()

    def simulate_prediction(self) -> str:
        """
        Simulate sign language prediction for demonstration
        """
        import random
        
        # Simulate some common signs
        signs = ['HELLO', 'THANK YOU', 'YES', 'NO', 'PLEASE', 'SORRY', 'GOOD', 'BAD', 'HELP']
        return random.choice(signs)

    def update_sequence_buffer(self, sign: str):
        """
        Update the sequence buffer with new sign
        """
        self.sequence_buffer.append(sign)
        
        # Keep only the last N signs
        if len(self.sequence_buffer) > self.max_sequence_length:
            self.sequence_buffer = self.sequence_buffer[-self.max_sequence_length:]

    def recognize_phrase(self) -> Optional[str]:
        """
        Recognize common phrases from sequence buffer
        """
        if len(self.sequence_buffer) < 3:
            return None
        
        # Convert sequence to string
        sequence_str = ''.join(self.sequence_buffer)
        
        # Check for common phrases
        for phrase, pattern in self.common_phrases.items():
            if self.sequence_matches_pattern(sequence_str, pattern):
                # Clear buffer after recognizing phrase
                self.sequence_buffer = []
                return phrase
        
        return None

    def sequence_matches_pattern(self, sequence: str, pattern: list) -> bool:
        """
        Check if sequence matches a pattern
        """
        if len(sequence) < len(pattern):
            return False
        
        # Simple pattern matching
        for i in range(len(sequence) - len(pattern) + 1):
            if sequence[i:i+len(pattern)] == pattern:
                return True
        
        return False

    async def recognize(self, image: np.ndarray, language: str = "en") -> Optional[str]:
        """
        Main recognition function
        """
        try:
            # Extract hand features
            features = self.extract_hand_features(image)
            
            if features is not None:
                # Predict sign
                sign = self.predict_sign(image)
                
                if sign and sign != 'NOTHING':
                    # Update sequence buffer
                    self.update_sequence_buffer(sign)
                    
                    # Try to recognize phrase
                    phrase = self.recognize_phrase()
                    
                    if phrase:
                        return phrase
                    else:
                        # Return individual sign
                        return sign
            
            return None
            
        except Exception as e:
            logging.error(f"Error in sign recognition: {str(e)}")
            return None

    def is_ready(self) -> bool:
        """
        Check if the recognizer is ready
        """
        return self.is_model_ready

    def get_supported_languages(self) -> list:
        """
        Get list of supported languages
        """
        return ["en", "ta", "ml", "te"]

    def cleanup(self):
        """
        Cleanup resources
        """
        if hasattr(self, 'hands'):
            self.hands.close()
        logging.info("Sign Language Recognizer cleaned up")
