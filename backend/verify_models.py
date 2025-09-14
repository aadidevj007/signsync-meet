#!/usr/bin/env python3
"""
Model Verification Script for SignSync Meet
This script verifies that all required models are properly set up.
"""

import os
import sys
import logging
from pathlib import Path

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.model_loader import ModelLoader, check_model_requirements

def main():
    """
    Main function to verify model setup
    """
    print("SignSync Meet - Model Verification")
    print("=" * 40)
    
    # Initialize model loader
    loader = ModelLoader()
    
    # Get model information
    model_info = loader.get_model_info()
    
    print(f"\n📁 Models Directory: {model_info['models_directory']}")
    
    # Check ASL model
    print("\n🤖 ASL Model Status:")
    if model_info['asl_model_path']:
        print(f"   ✅ ASL Model: {model_info['asl_model_path']}")
    else:
        print("   ❌ ASL Model: Not found")
        print("   📝 Please download asl_model.h5 from Kaggle ASL Alphabet dataset")
        print("   📝 Place it in the models/ directory")
    
    # Check Vosk models
    print("\n🗣️ Vosk Models Status:")
    vosk_models = model_info['vosk_models']
    if vosk_models:
        for lang, path in vosk_models.items():
            print(f"   ✅ {lang.upper()}: {path}")
    else:
        print("   ❌ No Vosk models found")
        print("   📝 Please run: python setup_models.py")
    
    # Check available models
    print("\n📊 Available Models:")
    available = model_info['available_models']
    if available['asl_models']:
        print(f"   ASL Models: {', '.join(available['asl_models'])}")
    if available['vosk_models']:
        print(f"   Vosk Models: {', '.join(available['vosk_models'])}")
    if available['other_models']:
        print(f"   Other Models: {', '.join(available['other_models'])}")
    
    # Validation results
    print("\n✅ Validation Results:")
    validation = model_info['validation_results']
    for model, status in validation.items():
        status_icon = "✅" if status else "❌"
        print(f"   {status_icon} {model.replace('_', ' ').title()}")
    
    # Services ready status
    print("\n🔧 Services Ready:")
    services = model_info.get('services_ready', {})
    for service, status in services.items():
        status_icon = "✅" if status else "❌"
        print(f"   {status_icon} {service.replace('_', ' ').title()}")
    
    # Overall status
    print("\n" + "=" * 40)
    all_models_ready = all(validation.values())
    if all_models_ready:
        print("🎉 All required models are ready!")
        print("   You can now start the SignSync Meet backend.")
    else:
        print("⚠️  Some models are missing.")
        print("   Please run: python setup_models.py")
        print("   Or manually download the required models.")
    
    print("\n📚 For more information, see:")
    print("   - README.md")
    print("   - docs/API.md")
    print("   - docs/DEPLOYMENT.md")

if __name__ == "__main__":
    main()
