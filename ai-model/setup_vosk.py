"""
Vosk Speech Recognition Setup Script
This script downloads and sets up the Vosk model for offline speech recognition.
"""

import os
import urllib.request
import zipfile
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VoskSetup:
    def __init__(self, models_dir="models"):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(exist_ok=True)
        
        # Vosk model URLs and info
        self.models = {
            "small": {
                "url": "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip",
                "filename": "vosk-model-small-en-us-0.15.zip",
                "extract_dir": "vosk-model-small-en-us-0.15"
            },
            "medium": {
                "url": "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip",
                "filename": "vosk-model-en-us-0.22.zip",
                "extract_dir": "vosk-model-en-us-0.22"
            },
            "large": {
                "url": "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip",
                "filename": "vosk-model-en-us-0.22-lgraph.zip",
                "extract_dir": "vosk-model-en-us-0.22-lgraph"
            }
        }

    def download_file(self, url: str, filename: str) -> bool:
        """
        Download a file from URL
        """
        try:
            filepath = self.models_dir / filename
            logger.info(f"Downloading {filename}...")
            
            def progress_hook(block_num, block_size, total_size):
                downloaded = block_num * block_size
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    print(f"\rProgress: {percent:.1f}%", end="", flush=True)
            
            urllib.request.urlretrieve(url, filepath, progress_hook)
            print()  # New line after progress
            
            logger.info(f"Downloaded {filename} successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error downloading {filename}: {str(e)}")
            return False

    def extract_zip(self, zip_path: Path, extract_dir: str) -> bool:
        """
        Extract ZIP file
        """
        try:
            extract_path = self.models_dir / extract_dir
            
            logger.info(f"Extracting {zip_path.name}...")
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.models_dir)
            
            logger.info(f"Extracted to {extract_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error extracting {zip_path.name}: {str(e)}")
            return False

    def setup_model(self, model_size: str = "medium") -> bool:
        """
        Setup Vosk model
        """
        if model_size not in self.models:
            logger.error(f"Invalid model size: {model_size}")
            return False
        
        model_info = self.models[model_size]
        zip_path = self.models_dir / model_info["filename"]
        extract_path = self.models_dir / model_info["extract_dir"]
        
        # Check if model is already extracted
        if extract_path.exists():
            logger.info(f"Model {model_size} already exists at {extract_path}")
            return True
        
        # Download if not exists
        if not zip_path.exists():
            if not self.download_file(model_info["url"], model_info["filename"]):
                return False
        
        # Extract
        if not self.extract_zip(zip_path, model_info["extract_dir"]):
            return False
        
        # Clean up zip file
        try:
            zip_path.unlink()
            logger.info(f"Cleaned up {zip_path.name}")
        except Exception as e:
            logger.warning(f"Could not delete {zip_path.name}: {str(e)}")
        
        return True

    def setup_all_models(self) -> bool:
        """
        Setup all available models
        """
        success = True
        
        for model_size in self.models.keys():
            logger.info(f"Setting up {model_size} model...")
            if not self.setup_model(model_size):
                success = False
                logger.error(f"Failed to setup {model_size} model")
            else:
                logger.info(f"Successfully setup {model_size} model")
        
        return success

    def get_model_path(self, model_size: str = "medium") -> str:
        """
        Get the path to the model
        """
        if model_size not in self.models:
            return None
        
        model_info = self.models[model_size]
        extract_path = self.models_dir / model_info["extract_dir"]
        
        if extract_path.exists():
            return str(extract_path)
        
        return None

    def list_available_models(self) -> list:
        """
        List available models
        """
        available = []
        
        for model_size, model_info in self.models.items():
            extract_path = self.models_dir / model_info["extract_dir"]
            if extract_path.exists():
                available.append(model_size)
        
        return available

def main():
    """
    Main function to setup Vosk models
    """
    setup = VoskSetup()
    
    print("Vosk Speech Recognition Setup")
    print("=" * 40)
    
    # Ask user which model to setup
    print("Available models:")
    print("1. small - Fast, less accurate (~40MB)")
    print("2. medium - Balanced speed and accuracy (~1.8GB)")
    print("3. large - Slower, most accurate (~1.8GB)")
    print("4. all - Setup all models")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        setup.setup_model("small")
    elif choice == "2":
        setup.setup_model("medium")
    elif choice == "3":
        setup.setup_model("large")
    elif choice == "4":
        setup.setup_all_models()
    else:
        print("Invalid choice!")
        return
    
    # List available models
    available = setup.list_available_models()
    if available:
        print(f"\nAvailable models: {', '.join(available)}")
        
        # Show model paths
        for model_size in available:
            path = setup.get_model_path(model_size)
            print(f"{model_size}: {path}")
    else:
        print("\nNo models available!")
    
    print("\nSetup completed!")

if __name__ == "__main__":
    main()
