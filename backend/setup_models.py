"""
Model Setup Script for SignSync Meet
This script helps download and organize pre-trained models.
"""

import os
import sys
import logging
import urllib.request
import zipfile
import shutil
from pathlib import Path
from typing import Dict, List

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ModelSetup:
    """
    Setup class for downloading and organizing pre-trained models
    """
    
    def __init__(self, models_dir: str = "models"):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(exist_ok=True)
        
        # Model URLs and information
        self.model_info = {
            "asl_model": {
                "description": "Pre-trained ASL Alphabet CNN model from Kaggle",
                "filename": "asl_model.h5",
                "note": "Please download asl_model.h5 from Kaggle ASL Alphabet dataset and place it in models/ directory"
            },
            "vosk_models": {
                "en": {
                    "url": "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip",
                    "filename": "vosk-model-en-us-0.22.zip",
                    "extract_dir": "vosk-model-en-us-0.22"
                },
                "ta": {
                    "url": "https://alphacephei.com/vosk/models/vosk-model-ta-0.22.zip",
                    "filename": "vosk-model-ta-0.22.zip", 
                    "extract_dir": "vosk-model-ta-0.22"
                },
                "ml": {
                    "url": "https://alphacephei.com/vosk/models/vosk-model-ml-0.22.zip",
                    "filename": "vosk-model-ml-0.22.zip",
                    "extract_dir": "vosk-model-ml-0.22"
                },
                "te": {
                    "url": "https://alphacephei.com/vosk/models/vosk-model-te-0.22.zip",
                    "filename": "vosk-model-te-0.22.zip",
                    "extract_dir": "vosk-model-te-0.22"
                }
            }
        }
    
    def setup_directory_structure(self):
        """
        Create the models directory structure
        """
        logger.info("Setting up models directory structure...")
        
        # Create main directories
        (self.models_dir / "vosk").mkdir(exist_ok=True)
        (self.models_dir / "asl").mkdir(exist_ok=True)
        (self.models_dir / "temp").mkdir(exist_ok=True)
        
        logger.info(f"Models directory structure created at: {self.models_dir}")
    
    def download_file(self, url: str, filename: str, progress_callback=None) -> bool:
        """
        Download a file from URL
        """
        try:
            filepath = self.models_dir / "temp" / filename
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
            extract_path = self.models_dir / "vosk" / extract_dir
            
            logger.info(f"Extracting {zip_path.name}...")
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.models_dir / "vosk")
            
            logger.info(f"Extracted to {extract_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error extracting {zip_path.name}: {str(e)}")
            return False
    
    def setup_vosk_model(self, language: str) -> bool:
        """
        Setup Vosk model for a specific language
        """
        if language not in self.model_info["vosk_models"]:
            logger.error(f"Unsupported language: {language}")
            return False
        
        model_info = self.model_info["vosk_models"][language]
        zip_path = self.models_dir / "temp" / model_info["filename"]
        extract_path = self.models_dir / "vosk" / model_info["extract_dir"]
        
        # Check if model is already extracted
        if extract_path.exists():
            logger.info(f"Vosk {language} model already exists at {extract_path}")
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
    
    def setup_all_vosk_models(self) -> bool:
        """
        Setup all Vosk models
        """
        success = True
        
        for language in self.model_info["vosk_models"].keys():
            logger.info(f"Setting up Vosk {language} model...")
            if not self.setup_vosk_model(language):
                success = False
                logger.error(f"Failed to setup Vosk {language} model")
            else:
                logger.info(f"Successfully setup Vosk {language} model")
        
        return success
    
    def check_asl_model(self) -> bool:
        """
        Check if ASL model is available
        """
        asl_model_path = self.models_dir / "asl_model.h5"
        
        if asl_model_path.exists():
            logger.info(f"ASL model found at: {asl_model_path}")
            return True
        else:
            logger.warning(f"ASL model not found at: {asl_model_path}")
            logger.info("Please download asl_model.h5 from Kaggle ASL Alphabet dataset")
            logger.info("and place it in the models/ directory")
            return False
    
    def cleanup_temp_files(self):
        """
        Clean up temporary files
        """
        temp_dir = self.models_dir / "temp"
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
            logger.info("Cleaned up temporary files")
    
    def get_model_status(self) -> Dict:
        """
        Get status of all models
        """
        status = {
            "asl_model": self.check_asl_model(),
            "vosk_models": {}
        }
        
        for language in self.model_info["vosk_models"].keys():
            model_path = self.models_dir / "vosk" / self.model_info["vosk_models"][language]["extract_dir"]
            status["vosk_models"][language] = model_path.exists()
        
        return status
    
    def print_model_info(self):
        """
        Print information about models
        """
        print("\n" + "="*60)
        print("SignSync Meet - Model Setup Information")
        print("="*60)
        
        print("\n📁 Models Directory Structure:")
        print(f"   {self.models_dir}/")
        print(f"   ├── asl_model.h5          # ASL Alphabet CNN model")
        print(f"   └── vosk/                 # Vosk speech recognition models")
        print(f"       ├── vosk-model-en-us-0.22/")
        print(f"       ├── vosk-model-ta-0.22/")
        print(f"       ├── vosk-model-ml-0.22/")
        print(f"       └── vosk-model-te-0.22/")
        
        print("\n🤖 Required Models:")
        print("   1. ASL Model (asl_model.h5)")
        print("      - Download from Kaggle ASL Alphabet dataset")
        print("      - Place in models/ directory")
        print("      - Used for sign language recognition")
        
        print("\n   2. Vosk Models (for speech recognition)")
        print("      - English: vosk-model-en-us-0.22")
        print("      - Tamil: vosk-model-ta-0.22")
        print("      - Malayalam: vosk-model-ml-0.22")
        print("      - Telugu: vosk-model-te-0.22")
        
        print("\n📊 Current Model Status:")
        status = self.get_model_status()
        
        print(f"   ASL Model: {'✅ Available' if status['asl_model'] else '❌ Missing'}")
        for lang, available in status["vosk_models"].items():
            print(f"   Vosk {lang.upper()}: {'✅ Available' if available else '❌ Missing'}")
        
        print("\n" + "="*60)

def main():
    """
    Main function for model setup
    """
    setup = ModelSetup()
    
    print("SignSync Meet - Model Setup")
    print("="*40)
    
    # Setup directory structure
    setup.setup_directory_structure()
    
    # Print model information
    setup.print_model_info()
    
    # Ask user what to do
    print("\nOptions:")
    print("1. Download Vosk models")
    print("2. Check model status")
    print("3. Setup all models")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        print("\nWhich Vosk models to download?")
        print("1. English only")
        print("2. All languages")
        
        sub_choice = input("Enter choice (1-2): ").strip()
        
        if sub_choice == "1":
            setup.setup_vosk_model("en")
        elif sub_choice == "2":
            setup.setup_all_vosk_models()
    
    elif choice == "2":
        status = setup.get_model_status()
        print(f"\nModel Status: {status}")
    
    elif choice == "3":
        print("\nSetting up all models...")
        setup.setup_all_vosk_models()
        setup.check_asl_model()
    
    elif choice == "4":
        print("Exiting...")
        return
    
    else:
        print("Invalid choice!")
        return
    
    # Cleanup
    setup.cleanup_temp_files()
    
    # Final status
    print("\nFinal Model Status:")
    setup.print_model_info()
    
    print("\nSetup completed!")

if __name__ == "__main__":
    main()
