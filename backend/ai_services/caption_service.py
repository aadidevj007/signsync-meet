import logging
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

class CaptionService:
    def __init__(self):
        self.caption_history = []
        self.max_history = 100
        self.is_ready = True
        
        logging.info("Caption Service initialized")

    def create_caption(
        self, 
        text: str, 
        type: str, 
        user_id: str, 
        language: str = "en",
        user_name: Optional[str] = None,
        user_photo: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a caption object
        """
        try:
            caption = {
                "id": str(uuid.uuid4()),
                "text": text,
                "type": type,  # 'voice' or 'sign'
                "user_id": user_id,
                "user_name": user_name or "Unknown User",
                "user_photo": user_photo or "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=40&h=40&fit=crop&crop=face",
                "language": language,
                "timestamp": datetime.now().isoformat(),
                "confidence": 0.95,  # Simulated confidence score
                "metadata": {
                    "processing_time": 0.5,  # Simulated processing time
                    "model_version": "1.0.0"
                }
            }
            
            # Add to history
            self.add_to_history(caption)
            
            return caption
            
        except Exception as e:
            logging.error(f"Error creating caption: {str(e)}")
            return None

    def add_to_history(self, caption: Dict[str, Any]):
        """
        Add caption to history
        """
        try:
            self.caption_history.append(caption)
            
            # Keep only the last N captions
            if len(self.caption_history) > self.max_history:
                self.caption_history = self.caption_history[-self.max_history:]
                
        except Exception as e:
            logging.error(f"Error adding caption to history: {str(e)}")

    def get_caption_history(self, limit: int = 50) -> list:
        """
        Get caption history
        """
        try:
            return self.caption_history[-limit:] if limit else self.caption_history
            
        except Exception as e:
            logging.error(f"Error getting caption history: {str(e)}")
            return []

    def get_captions_by_user(self, user_id: str, limit: int = 20) -> list:
        """
        Get captions by specific user
        """
        try:
            user_captions = [c for c in self.caption_history if c.get("user_id") == user_id]
            return user_captions[-limit:] if limit else user_captions
            
        except Exception as e:
            logging.error(f"Error getting captions by user: {str(e)}")
            return []

    def get_captions_by_type(self, caption_type: str, limit: int = 20) -> list:
        """
        Get captions by type (voice or sign)
        """
        try:
            type_captions = [c for c in self.caption_history if c.get("type") == caption_type]
            return type_captions[-limit:] if limit else type_captions
            
        except Exception as e:
            logging.error(f"Error getting captions by type: {str(e)}")
            return []

    def get_captions_by_language(self, language: str, limit: int = 20) -> list:
        """
        Get captions by language
        """
        try:
            language_captions = [c for c in self.caption_history if c.get("language") == language]
            return language_captions[-limit:] if limit else language_captions
            
        except Exception as e:
            logging.error(f"Error getting captions by language: {str(e)}")
            return []

    def translate_caption(self, caption: Dict[str, Any], target_language: str) -> Optional[Dict[str, Any]]:
        """
        Translate caption to target language
        """
        try:
            # In a real implementation, you would use a translation service
            # For now, we'll simulate translation
            
            translated_text = self.simulate_translation(caption["text"], target_language)
            
            if translated_text:
                translated_caption = caption.copy()
                translated_caption["id"] = str(uuid.uuid4())
                translated_caption["text"] = translated_text
                translated_caption["language"] = target_language
                translated_caption["timestamp"] = datetime.now().isoformat()
                translated_caption["metadata"]["translated"] = True
                translated_caption["metadata"]["original_language"] = caption["language"]
                
                return translated_caption
            
            return None
            
        except Exception as e:
            logging.error(f"Error translating caption: {str(e)}")
            return None

    def simulate_translation(self, text: str, target_language: str) -> Optional[str]:
        """
        Simulate translation for demonstration
        """
        # Simple translation mapping for demonstration
        translations = {
            "en": {
                "ta": {
                    "Hello everyone": "வணக்கம் அனைவருக்கும்",
                    "Thank you": "நன்றி",
                    "Yes": "ஆம்",
                    "No": "இல்லை",
                    "Please": "தயவு செய்து",
                    "Sorry": "மன்னிக்கவும்"
                },
                "ml": {
                    "Hello everyone": "ഹലോ എല്ലാവർക്കും",
                    "Thank you": "നന്ദി",
                    "Yes": "അതെ",
                    "No": "ഇല്ല",
                    "Please": "ദയവായി",
                    "Sorry": "ക്ഷമിക്കണം"
                },
                "te": {
                    "Hello everyone": "హలో అందరికీ",
                    "Thank you": "ధన్యవాదాలు",
                    "Yes": "అవును",
                    "No": "కాదు",
                    "Please": "దయచేసి",
                    "Sorry": "క్షమించండి"
                }
            }
        }
        
        # Check if translation exists
        if target_language in translations.get("en", {}):
            return translations["en"][target_language].get(text, text)
        
        return text

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get caption service statistics
        """
        try:
            total_captions = len(self.caption_history)
            
            if total_captions == 0:
                return {
                    "total_captions": 0,
                    "voice_captions": 0,
                    "sign_captions": 0,
                    "languages": {},
                    "users": {},
                    "average_confidence": 0.0
                }
            
            # Count by type
            voice_captions = len([c for c in self.caption_history if c.get("type") == "voice"])
            sign_captions = len([c for c in self.caption_history if c.get("type") == "sign"])
            
            # Count by language
            languages = {}
            for caption in self.caption_history:
                lang = caption.get("language", "unknown")
                languages[lang] = languages.get(lang, 0) + 1
            
            # Count by user
            users = {}
            for caption in self.caption_history:
                user_id = caption.get("user_id", "unknown")
                users[user_id] = users.get(user_id, 0) + 1
            
            # Calculate average confidence
            confidences = [c.get("confidence", 0) for c in self.caption_history]
            average_confidence = sum(confidences) / len(confidences) if confidences else 0.0
            
            return {
                "total_captions": total_captions,
                "voice_captions": voice_captions,
                "sign_captions": sign_captions,
                "languages": languages,
                "users": users,
                "average_confidence": round(average_confidence, 3)
            }
            
        except Exception as e:
            logging.error(f"Error getting statistics: {str(e)}")
            return {}

    def clear_history(self):
        """
        Clear caption history
        """
        try:
            self.caption_history = []
            logging.info("Caption history cleared")
            
        except Exception as e:
            logging.error(f"Error clearing history: {str(e)}")

    def is_ready(self) -> bool:
        """
        Check if the service is ready
        """
        return self.is_ready

    def cleanup(self):
        """
        Cleanup resources
        """
        try:
            self.caption_history = []
            logging.info("Caption Service cleaned up")
            
        except Exception as e:
            logging.error(f"Error cleaning up caption service: {str(e)}")
