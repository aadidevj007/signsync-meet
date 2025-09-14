"""
Sign Language Recognition Model Training Script
This script trains a CNN model to recognize ASL (American Sign Language) alphabet signs.
"""

import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers, callbacks
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import mediapipe as mp
from tqdm import tqdm
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SignLanguageTrainer:
    def __init__(self, data_dir="data/asl_dataset", model_dir="models"):
        self.data_dir = data_dir
        self.model_dir = model_dir
        self.img_size = (64, 64)
        self.num_classes = 29  # 26 letters + space + delete + nothing
        self.batch_size = 32
        self.epochs = 50
        
        # Create directories
        os.makedirs(self.model_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
        
        # ASL alphabet mapping
        self.asl_alphabet = {
            'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9,
            'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19,
            'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25, 'SPACE': 26, 'DELETE': 27, 'NOTHING': 28
        }
        
        self.reverse_alphabet = {v: k for k, v in self.asl_alphabet.items()}
        
        # Initialize MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=1,
            min_detection_confidence=0.7
        )

    def create_synthetic_dataset(self):
        """
        Create a synthetic dataset for demonstration purposes
        In a real implementation, you would use actual ASL dataset
        """
        logger.info("Creating synthetic dataset...")
        
        # Create synthetic images for each class
        for class_name, class_id in self.asl_alphabet.items():
            class_dir = os.path.join(self.data_dir, class_name)
            os.makedirs(class_dir, exist_ok=True)
            
            # Generate synthetic images
            for i in range(100):  # 100 images per class
                img = self.generate_synthetic_image(class_name)
                img_path = os.path.join(class_dir, f"{class_name}_{i:03d}.jpg")
                cv2.imwrite(img_path, img)
        
        logger.info(f"Synthetic dataset created with {len(self.asl_alphabet)} classes")

    def generate_synthetic_image(self, class_name):
        """
        Generate synthetic images for demonstration
        In a real implementation, you would use actual ASL images
        """
        # Create a random image with some pattern based on class
        img = np.random.randint(0, 255, (self.img_size[0], self.img_size[1], 3), dtype=np.uint8)
        
        # Add some class-specific patterns
        if class_name == 'A':
            # Draw a simple 'A' pattern
            cv2.circle(img, (32, 32), 15, (255, 255, 255), -1)
        elif class_name == 'B':
            # Draw a simple 'B' pattern
            cv2.rectangle(img, (20, 20), (44, 44), (255, 255, 255), -1)
        elif class_name == 'SPACE':
            # Empty image for space
            img = np.zeros((self.img_size[0], self.img_size[1], 3), dtype=np.uint8)
        elif class_name == 'NOTHING':
            # Random noise for nothing
            img = np.random.randint(0, 50, (self.img_size[0], self.img_size[1], 3), dtype=np.uint8)
        else:
            # Add some random shapes for other classes
            center = (np.random.randint(20, 44), np.random.randint(20, 44))
            radius = np.random.randint(5, 15)
            color = (np.random.randint(100, 255), np.random.randint(100, 255), np.random.randint(100, 255))
            cv2.circle(img, center, radius, color, -1)
        
        return img

    def load_dataset(self):
        """
        Load and preprocess the dataset
        """
        logger.info("Loading dataset...")
        
        images = []
        labels = []
        
        for class_name, class_id in self.asl_alphabet.items():
            class_dir = os.path.join(self.data_dir, class_name)
            
            if not os.path.exists(class_dir):
                logger.warning(f"Class directory {class_dir} not found, skipping...")
                continue
            
            for img_file in os.listdir(class_dir):
                if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    img_path = os.path.join(class_dir, img_file)
                    
                    # Load and preprocess image
                    img = cv2.imread(img_path)
                    if img is not None:
                        img = cv2.resize(img, self.img_size)
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        img = img.astype(np.float32) / 255.0
                        
                        images.append(img)
                        labels.append(class_id)
        
        images = np.array(images)
        labels = np.array(labels)
        
        logger.info(f"Dataset loaded: {len(images)} images, {len(set(labels))} classes")
        return images, labels

    def create_model(self):
        """
        Create the CNN model architecture
        """
        model = models.Sequential([
            # First convolutional block
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=(*self.img_size, 3)),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Second convolutional block
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Third convolutional block
            layers.Conv2D(128, (3, 3), activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Fourth convolutional block
            layers.Conv2D(256, (3, 3), activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Flatten and dense layers
            layers.Flatten(),
            layers.Dense(512, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            layers.Dense(256, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(self.num_classes, activation='softmax')
        ])
        
        return model

    def compile_model(self, model):
        """
        Compile the model with optimizer and loss function
        """
        model.compile(
            optimizer=optimizers.Adam(learning_rate=0.001),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model

    def train_model(self, model, X_train, y_train, X_val, y_val):
        """
        Train the model
        """
        logger.info("Starting model training...")
        
        # Data augmentation
        train_datagen = ImageDataGenerator(
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            horizontal_flip=True,
            zoom_range=0.2,
            fill_mode='nearest'
        )
        
        # Callbacks
        callbacks_list = [
            callbacks.EarlyStopping(
                monitor='val_accuracy',
                patience=10,
                restore_best_weights=True
            ),
            callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=0.0001
            ),
            callbacks.ModelCheckpoint(
                filepath=os.path.join(self.model_dir, 'best_model.h5'),
                monitor='val_accuracy',
                save_best_only=True,
                save_weights_only=False
            )
        ]
        
        # Train the model
        history = model.fit(
            train_datagen.flow(X_train, y_train, batch_size=self.batch_size),
            steps_per_epoch=len(X_train) // self.batch_size,
            epochs=self.epochs,
            validation_data=(X_val, y_val),
            callbacks=callbacks_list,
            verbose=1
        )
        
        return history

    def evaluate_model(self, model, X_test, y_test):
        """
        Evaluate the model performance
        """
        logger.info("Evaluating model...")
        
        # Get predictions
        y_pred = model.predict(X_test)
        y_pred_classes = np.argmax(y_pred, axis=1)
        
        # Calculate accuracy
        accuracy = np.mean(y_pred_classes == y_test)
        logger.info(f"Test Accuracy: {accuracy:.4f}")
        
        # Classification report
        report = classification_report(y_test, y_pred_classes, target_names=list(self.asl_alphabet.keys()))
        logger.info(f"Classification Report:\n{report}")
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred_classes)
        
        # Plot confusion matrix
        plt.figure(figsize=(12, 10))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                   xticklabels=list(self.asl_alphabet.keys()),
                   yticklabels=list(self.asl_alphabet.keys()))
        plt.title('Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.tight_layout()
        plt.savefig(os.path.join(self.model_dir, 'confusion_matrix.png'))
        plt.show()
        
        return accuracy, report, cm

    def plot_training_history(self, history):
        """
        Plot training history
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # Plot accuracy
        ax1.plot(history.history['accuracy'], label='Training Accuracy')
        ax1.plot(history.history['val_accuracy'], label='Validation Accuracy')
        ax1.set_title('Model Accuracy')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Accuracy')
        ax1.legend()
        ax1.grid(True)
        
        # Plot loss
        ax2.plot(history.history['loss'], label='Training Loss')
        ax2.plot(history.history['val_loss'], label='Validation Loss')
        ax2.set_title('Model Loss')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Loss')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.model_dir, 'training_history.png'))
        plt.show()

    def save_model_info(self, model, accuracy, report):
        """
        Save model information and metadata
        """
        model_info = {
            'model_name': 'sign_language_recognition',
            'version': '1.0.0',
            'input_shape': (*self.img_size, 3),
            'num_classes': self.num_classes,
            'classes': self.asl_alphabet,
            'test_accuracy': float(accuracy),
            'training_date': pd.Timestamp.now().isoformat(),
            'model_architecture': 'CNN with 4 convolutional blocks',
            'optimizer': 'Adam',
            'loss_function': 'sparse_categorical_crossentropy'
        }
        
        # Save model info
        with open(os.path.join(self.model_dir, 'model_info.json'), 'w') as f:
            json.dump(model_info, f, indent=2)
        
        # Save classification report
        with open(os.path.join(self.model_dir, 'classification_report.txt'), 'w') as f:
            f.write(report)
        
        logger.info("Model information saved")

    def run_training(self):
        """
        Run the complete training pipeline
        """
        logger.info("Starting Sign Language Model Training Pipeline")
        
        # Create synthetic dataset if it doesn't exist
        if not os.path.exists(os.path.join(self.data_dir, 'A')):
            self.create_synthetic_dataset()
        
        # Load dataset
        images, labels = self.load_dataset()
        
        if len(images) == 0:
            logger.error("No images found in dataset!")
            return
        
        # Split dataset
        X_train, X_temp, y_train, y_temp = train_test_split(
            images, labels, test_size=0.3, random_state=42, stratify=labels
        )
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
        )
        
        logger.info(f"Dataset split - Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
        
        # Create and compile model
        model = self.create_model()
        model = self.compile_model(model)
        
        # Print model summary
        model.summary()
        
        # Train model
        history = self.train_model(model, X_train, y_train, X_val, y_val)
        
        # Evaluate model
        accuracy, report, cm = self.evaluate_model(model, X_test, y_test)
        
        # Plot training history
        self.plot_training_history(history)
        
        # Save model
        model.save(os.path.join(self.model_dir, 'sign_language_model.h5'))
        
        # Save model information
        self.save_model_info(model, accuracy, report)
        
        logger.info("Training completed successfully!")
        
        return model, history

def main():
    """
    Main function to run the training
    """
    trainer = SignLanguageTrainer()
    model, history = trainer.run_training()
    
    print("Training completed!")
    print(f"Model saved to: {trainer.model_dir}")
    print("You can now use this model for sign language recognition.")

if __name__ == "__main__":
    main()
