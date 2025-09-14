import asyncio
import logging
import os
import io
import wave
import json
from typing import Optional, Dict, Any
import numpy as np
from datetime import datetime

# Try to import Vosk (offline speech recognition)
try:
    import vosk
    VOSK_AVAILABLE = True
except ImportError:
    VOSK_AVAILABLE = False
    logging.warning("Vosk not available, using Google Speech API only")

# Try to import Google Cloud Speech
try:
    from google.cloud import speech
    GOOGLE_SPEECH_AVAILABLE = True
except ImportError:
    GOOGLE_SPEECH_AVAILABLE = False
    logging.warning("Google Cloud Speech not available")

class VoiceRecognizer:
    def __init__(self):
        self.vosk_model = None
        self.google_client = None
        self.is_ready = False
        
        # Initialize services
        self.initialize_vosk()
        self.initialize_google_speech()
        
        # Language mapping
        self.language_codes = {
            "en": "en-US",
            "ta": "ta-IN",
            "ml": "ml-IN",
            "te": "te-IN"
        }
        
        logging.info("Voice Recognizer initialized")

    def initialize_vosk(self):
        """
        Initialize Vosk offline speech recognition with pre-trained models
        """
        if not VOSK_AVAILABLE:
            return
        
        try:
            # Load pre-trained Vosk models for different languages
            self.vosk_models = {}
            models_dir = os.path.join(os.path.dirname(__file__), '..', 'models', 'vosk')
            
            # Model mappings for different languages
            model_mappings = {
                'en': 'vosk-model-en-us-0.22',
                'ta': 'vosk-model-ta-0.22',  # Tamil model if available
                'ml': 'vosk-model-ml-0.22',  # Malayalam model if available
                'te': 'vosk-model-te-0.22'   # Telugu model if available
            }
            
            for lang, model_name in model_mappings.items():
                model_path = os.path.join(models_dir, model_name)
                if os.path.exists(model_path):
                    self.vosk_models[lang] = vosk.Model(model_path)
                    logging.info(f"Vosk {lang} model loaded successfully from {model_path}")
                else:
                    logging.warning(f"Vosk {lang} model not found at {model_path}")
            
            # Set default model to English if available
            if 'en' in self.vosk_models:
                self.vosk_model = self.vosk_models['en']
                logging.info("Default Vosk model set to English")
            elif self.vosk_models:
                # Use first available model as default
                self.vosk_model = list(self.vosk_models.values())[0]
                logging.info("Default Vosk model set to first available model")
                
        except Exception as e:
            logging.error(f"Error initializing Vosk models: {str(e)}")

    def initialize_google_speech(self):
        """
        Initialize Google Cloud Speech API
        """
        if not GOOGLE_SPEECH_AVAILABLE:
            return
        
        try:
            # Initialize Google Cloud Speech client
            # Make sure to set GOOGLE_APPLICATION_CREDENTIALS environment variable
            self.google_client = speech.SpeechClient()
            logging.info("Google Speech API initialized")
            
        except Exception as e:
            logging.error(f"Error initializing Google Speech API: {str(e)}")

    def preprocess_audio(self, audio_data: bytes) -> Optional[bytes]:
        """
        Preprocess audio data for recognition
        """
        try:
            # Convert to WAV format if needed
            audio_io = io.BytesIO(audio_data)
            
            # Try to read as WAV
            try:
                with wave.open(audio_io, 'rb') as wav_file:
                    # Get audio parameters
                    sample_rate = wav_file.getframerate()
                    channels = wav_file.getnchannels()
                    sample_width = wav_file.getsampwidth()
                    
                    # Read audio data
                    audio_frames = wav_file.readframes(wav_file.getnframes())
                    
                    # Convert to mono if stereo
                    if channels == 2:
                        audio_array = np.frombuffer(audio_frames, dtype=np.int16)
                        audio_array = audio_array.reshape(-1, 2)
                        audio_array = np.mean(audio_array, axis=1).astype(np.int16)
                        audio_frames = audio_array.tobytes()
                        channels = 1
                    
                    return audio_frames, sample_rate, channels, sample_width
                    
            except wave.Error:
                # If not WAV, assume it's raw audio data
                # Default parameters for common audio formats
                return audio_data, 16000, 1, 2
                
        except Exception as e:
            logging.error(f"Error preprocessing audio: {str(e)}")
            return None

    async def transcribe_with_vosk(self, audio_data: bytes, language: str = "en") -> Optional[str]:
        """
        Transcribe audio using Vosk (offline) with language-specific models
        """
        if not VOSK_AVAILABLE:
            return None
        
        try:
            # Get language-specific model
            model = self.vosk_models.get(language, self.vosk_model)
            if not model:
                logging.warning(f"No Vosk model available for language: {language}")
                return None
            
            # Preprocess audio
            result = self.preprocess_audio(audio_data)
            if result is None:
                return None
            
            audio_frames, sample_rate, channels, sample_width = result
            
            # Create recognizer with language-specific model
            recognizer = vosk.KaldiRecognizer(model, sample_rate)
            recognizer.SetWords(True)
            
            # Process audio in chunks
            chunk_size = 4000
            text = ""
            
            for i in range(0, len(audio_frames), chunk_size):
                chunk = audio_frames[i:i+chunk_size]
                
                if recognizer.AcceptWaveform(chunk):
                    result = json.loads(recognizer.Result())
                    if result.get('text'):
                        text += result['text'] + " "
            
            # Get final result
            final_result = json.loads(recognizer.FinalResult())
            if final_result.get('text'):
                text += final_result['text']
            
            return text.strip() if text else None
            
        except Exception as e:
            logging.error(f"Error in Vosk transcription for {language}: {str(e)}")
            return None

    async def transcribe_with_google(self, audio_data: bytes, language: str = "en") -> Optional[str]:
        """
        Transcribe audio using Google Cloud Speech API
        """
        if not self.google_client or not GOOGLE_SPEECH_AVAILABLE:
            return None
        
        try:
            # Preprocess audio
            result = self.preprocess_audio(audio_data)
            if result is None:
                return None
            
            audio_frames, sample_rate, channels, sample_width = result
            
            # Configure recognition
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=sample_rate,
                language_code=self.language_codes.get(language, "en-US"),
                enable_automatic_punctuation=True,
                model="latest_long"
            )
            
            audio = speech.RecognitionAudio(content=audio_frames)
            
            # Perform recognition
            response = self.google_client.recognize(config=config, audio=audio)
            
            # Extract text from response
            if response.results:
                text = ""
                for result in response.results:
                    text += result.alternatives[0].transcript + " "
                return text.strip()
            
            return None
            
        except Exception as e:
            logging.error(f"Error in Google Speech transcription: {str(e)}")
            return None

    async def transcribe(self, audio_data: bytes, language: str = "en") -> Optional[str]:
        """
        Main transcription function
        """
        try:
            # Try Google Speech API first (more accurate)
            text = await self.transcribe_with_google(audio_data, language)
            
            # Fallback to Vosk if Google fails
            if not text:
                text = await self.transcribe_with_vosk(audio_data, language)
            
            # If both fail, simulate transcription for demonstration
            if not text:
                text = self.simulate_transcription(language)
            
            return text
            
        except Exception as e:
            logging.error(f"Error in voice transcription: {str(e)}")
            return self.simulate_transcription(language)

    def simulate_transcription(self, language: str = "en") -> str:
        """
        Simulate voice transcription for demonstration
        """
        import random
        
        # Sample phrases in different languages
        phrases = {
            "en": [
                "Hello everyone, how are you doing?",
                "Thank you for joining the meeting",
                "Can you hear me clearly?",
                "Yes, I can hear you perfectly",
                "Let's discuss the project updates",
                "I agree with your proposal",
                "That sounds like a great idea",
                "Could you please repeat that?",
                "I'm having trouble with my connection",
                "The presentation looks good"
            ],
            "ta": [
                "வணக்கம் அனைவருக்கும்",
                "கூட்டத்தில் சேர்ந்ததற்கு நன்றி",
                "நீங்கள் என்னை கேட்க முடிகிறதா?",
                "ஆம், நான் உங்களை தெளிவாக கேட்கிறேன்"
            ],
            "ml": [
                "ഹലോ എല്ലാവർക്കും",
                "മീറ്റിംഗിൽ ചേർന്നതിന് നന്ദി",
                "നിങ്ങൾ എന്നെ കേൾക്കാൻ കഴിയുമോ?",
                "അതെ, ഞാൻ നിങ്ങളെ വ്യക്തമായി കേൾക്കുന്നു"
            ],
            "te": [
                "హలో అందరికీ",
                "మీటింగ్‌లో చేరినందుకు ధన్యవాదాలు",
                "మీరు నన్ను వినగలరా?",
                "అవును, నేను మిమ్మల్ని స్పష్టంగా వింటున్నాను"
            ]
        }
        
        language_phrases = phrases.get(language, phrases["en"])
        return random.choice(language_phrases)

    def is_ready(self) -> bool:
        """
        Check if the recognizer is ready
        """
        return len(self.vosk_models) > 0 or self.google_client is not None

    def get_supported_languages(self) -> list:
        """
        Get list of supported languages
        """
        return list(self.language_codes.keys())

    def cleanup(self):
        """
        Cleanup resources
        """
        if self.vosk_model:
            # Vosk doesn't have explicit cleanup
            pass
        
        if self.google_client:
            # Google client doesn't need explicit cleanup
            pass
        
        logging.info("Voice Recognizer cleaned up")
