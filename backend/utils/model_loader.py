"""
Model Loading Utility for SignSync Meet
This utility helps load pre-trained models from the models directory.
"""

import os
import logging
from typing import Dict, Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)

class ModelLoader:
    """
    Utility class for loading pre-trained models
    """
    
    def __init__(self, models_dir: str = "models"):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(exist_ok=True)
        
    def get_asl_model_path(self) -> Optional[str]:
        """
        Get the path to the pre-trained ASL model
        """
        asl_model_path = self.models_dir / "asl_model.h5"
        
        if asl_model_path.exists():
            logger.info(f"ASL model found at: {asl_model_path}")
            return str(asl_model_path)
        else:
            logger.warning(f"ASL model not found at: {asl_model_path}")
            return None
    
    def get_vosk_models(self) -> Dict[str, str]:
        """
        Get paths to all available Vosk models
        """
        vosk_dir = self.models_dir / "vosk"
        vosk_models = {}
        
        if not vosk_dir.exists():
            logger.warning(f"Vosk models directory not found: {vosk_dir}")
            return vosk_models
        
        # Look for Vosk model directories
        for model_dir in vosk_dir.iterdir():
            if model_dir.is_dir() and model_dir.name.startswith("vosk-model"):
                # Extract language from model name
                model_name = model_dir.name
                if "en-us" in model_name:
                    vosk_models["en"] = str(model_dir)
                elif "ta" in model_name:
                    vosk_models["ta"] = str(model_dir)
                elif "ml" in model_name:
                    vosk_models["ml"] = str(model_dir)
                elif "te" in model_name:
                    vosk_models["te"] = str(model_dir)
                else:
                    # Generic model
                    vosk_models["generic"] = str(model_dir)
        
        logger.info(f"Found Vosk models: {list(vosk_models.keys())}")
        return vosk_models
    
    def list_available_models(self) -> Dict[str, List[str]]:
        """
        List all available models
        """
        available_models = {
            "asl_models": [],
            "vosk_models": [],
            "other_models": []
        }
        
        # Check for ASL models
        for file in self.models_dir.glob("*.h5"):
            if "asl" in file.name.lower():
                available_models["asl_models"].append(file.name)
        
        # Check for Vosk models
        vosk_dir = self.models_dir / "vosk"
        if vosk_dir.exists():
            for model_dir in vosk_dir.iterdir():
                if model_dir.is_dir() and model_dir.name.startswith("vosk-model"):
                    available_models["vosk_models"].append(model_dir.name)
        
        # Check for other models
        for file in self.models_dir.glob("*"):
            if file.is_file() and file.suffix in [".pkl", ".joblib", ".pt", ".pth"]:
                available_models["other_models"].append(file.name)
        
        return available_models
    
    def validate_models(self) -> Dict[str, bool]:
        """
        Validate that required models are available
        """
        validation_results = {
            "asl_model": False,
            "vosk_english": False,
            "vosk_tamil": False,
            "vosk_malayalam": False,
            "vosk_telugu": False
        }
        
        # Check ASL model
        asl_path = self.get_asl_model_path()
        validation_results["asl_model"] = asl_path is not None
        
        # Check Vosk models
        vosk_models = self.get_vosk_models()
        validation_results["vosk_english"] = "en" in vosk_models
        validation_results["vosk_tamil"] = "ta" in vosk_models
        validation_results["vosk_malayalam"] = "ml" in vosk_models
        validation_results["vosk_telugu"] = "te" in vosk_models
        
        return validation_results
    
    def get_model_info(self) -> Dict[str, any]:
        """
        Get information about available models
        """
        model_info = {
            "models_directory": str(self.models_dir),
            "available_models": self.list_available_models(),
            "validation_results": self.validate_models(),
            "asl_model_path": self.get_asl_model_path(),
            "vosk_models": self.get_vosk_models()
        }
        
        return model_info

def setup_models_directory():
    """
    Setup the models directory structure
    """
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    # Create subdirectories
    (models_dir / "vosk").mkdir(exist_ok=True)
    (models_dir / "asl").mkdir(exist_ok=True)
    (models_dir / "temp").mkdir(exist_ok=True)
    
    logger.info(f"Models directory structure created at: {models_dir}")
    
    return str(models_dir)

def check_model_requirements():
    """
    Check if all required models are available
    """
    loader = ModelLoader()
    validation = loader.validate_models()
    
    missing_models = []
    for model, available in validation.items():
        if not available:
            missing_models.append(model)
    
    if missing_models:
        logger.warning(f"Missing models: {missing_models}")
        logger.info("Please ensure the following models are available:")
        logger.info("1. ASL Model: models/asl_model.h5")
        logger.info("2. Vosk Models: models/vosk/vosk-model-*")
        return False
    else:
        logger.info("All required models are available!")
        return True

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Setup models directory
    setup_models_directory()
    
    # Check model requirements
    check_model_requirements()
    
    # Display model information
    loader = ModelLoader()
    info = loader.get_model_info()
    
    print("\n=== Model Information ===")
    print(f"Models Directory: {info['models_directory']}")
    print(f"Available Models: {info['available_models']}")
    print(f"Validation Results: {info['validation_results']}")
    print(f"ASL Model Path: {info['asl_model_path']}")
    print(f"Vosk Models: {info['vosk_models']}")
