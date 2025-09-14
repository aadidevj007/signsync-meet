from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import asyncio
import json
import base64
import io
import cv2
import numpy as np
from typing import List, Dict, Optional
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our AI modules
from ai_services.sign_recognition import SignLanguageRecognizer
from ai_services.voice_recognition import VoiceRecognizer
from ai_services.caption_service import CaptionService
from utils.model_loader import ModelLoader, check_model_requirements

# Initialize FastAPI app
app = FastAPI(
    title="SignSync Meet API",
    description="AI-Powered Video Conferencing Backend with Real-Time Captions",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Check model requirements
check_model_requirements()

# Initialize AI services
sign_recognizer = SignLanguageRecognizer()
voice_recognizer = VoiceRecognizer()
caption_service = CaptionService()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.room_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        
        if room_id not in self.room_connections:
            self.room_connections[room_id] = []
        self.room_connections[room_id].append(websocket)
        
        logging.info(f"Client connected to room {room_id}")

    def disconnect(self, websocket: WebSocket, room_id: str):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        
        if room_id in self.room_connections and websocket in self.room_connections[room_id]:
            self.room_connections[room_id].remove(websocket)
            
        logging.info(f"Client disconnected from room {room_id}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast_to_room(self, message: str, room_id: str, exclude_websocket: WebSocket = None):
        if room_id in self.room_connections:
            for connection in self.room_connections[room_id]:
                if connection != exclude_websocket:
                    try:
                        await connection.send_text(message)
                    except:
                        # Remove broken connections
                        self.room_connections[room_id].remove(connection)

manager = ConnectionManager()

@app.get("/")
async def root():
    return {
        "message": "SignSync Meet API",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "sign_recognition": sign_recognizer.is_ready(),
            "voice_recognition": voice_recognizer.is_ready(),
            "caption_service": caption_service.is_ready()
        }
    }

@app.get("/api/models/status")
async def get_model_status():
    """
    Get status of all AI models
    """
    model_loader = ModelLoader()
    model_info = model_loader.get_model_info()
    
    return {
        "models_directory": model_info["models_directory"],
        "available_models": model_info["available_models"],
        "validation_results": model_info["validation_results"],
        "asl_model_path": model_info["asl_model_path"],
        "vosk_models": model_info["vosk_models"],
        "services_ready": {
            "sign_recognition": sign_recognizer.is_ready(),
            "voice_recognition": voice_recognizer.is_ready(),
            "caption_service": caption_service.is_ready()
        }
    }

@app.post("/api/voice-to-text")
async def voice_to_text(
    audio_data: str,
    language: str = "en",
    user_id: str = None
):
    """
    Convert audio data to text using voice recognition
    """
    try:
        # Decode base64 audio data
        audio_bytes = base64.b64decode(audio_data)
        
        # Process with voice recognizer
        text = await voice_recognizer.transcribe(audio_bytes, language)
        
        if text:
            # Generate caption
            caption = caption_service.create_caption(
                text=text,
                type="voice",
                user_id=user_id,
                language=language
            )
            
            return {
                "success": True,
                "text": text,
                "caption": caption,
                "language": language
            }
        else:
            return {
                "success": False,
                "text": "",
                "message": "No speech detected"
            }
            
    except Exception as e:
        logging.error(f"Voice recognition error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/sign-to-text")
async def sign_to_text(
    image_data: str,
    language: str = "en",
    user_id: str = None
):
    """
    Convert sign language image to text using computer vision
    """
    try:
        # Decode base64 image data
        image_bytes = base64.b64decode(image_data)
        
        # Convert to OpenCV format
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Process with sign recognizer
        text = await sign_recognizer.recognize(image, language)
        
        if text:
            # Generate caption
            caption = caption_service.create_caption(
                text=text,
                type="sign",
                user_id=user_id,
                language=language
            )
            
            return {
                "success": True,
                "text": text,
                "caption": caption,
                "language": language
            }
        else:
            return {
                "success": False,
                "text": "",
                "message": "No sign detected"
            }
            
    except Exception as e:
        logging.error(f"Sign recognition error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    """
    Upload audio file for processing
    """
    try:
        # Read audio file
        audio_data = await file.read()
        
        # Process with voice recognizer
        text = await voice_recognizer.transcribe(audio_data, "en")
        
        return {
            "success": True,
            "text": text,
            "filename": file.filename
        }
        
    except Exception as e:
        logging.error(f"Audio upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload-image")
async def upload_image(file: UploadFile = File(...)):
    """
    Upload image file for sign language recognition
    """
    try:
        # Read image file
        image_data = await file.read()
        
        # Convert to OpenCV format
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Process with sign recognizer
        text = await sign_recognizer.recognize(image, "en")
        
        return {
            "success": True,
            "text": text,
            "filename": file.filename
        }
        
    except Exception as e:
        logging.error(f"Image upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    """
    WebSocket endpoint for real-time communication
    """
    await manager.connect(websocket, room_id)
    
    try:
        while True:
            # Receive data from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message["type"] == "audio_data":
                # Process audio data
                audio_data = message["data"]
                language = message.get("language", "en")
                user_id = message.get("user_id")
                
                # Convert to text
                result = await voice_to_text(audio_data, language, user_id)
                
                # Broadcast to room
                await manager.broadcast_to_room(
                    json.dumps({
                        "type": "caption",
                        "data": result
                    }),
                    room_id,
                    exclude_websocket=websocket
                )
                
            elif message["type"] == "image_data":
                # Process image data
                image_data = message["data"]
                language = message.get("language", "en")
                user_id = message.get("user_id")
                
                # Convert to text
                result = await sign_to_text(image_data, language, user_id)
                
                # Broadcast to room
                await manager.broadcast_to_room(
                    json.dumps({
                        "type": "caption",
                        "data": result
                    }),
                    room_id,
                    exclude_websocket=websocket
                )
                
            elif message["type"] == "ping":
                # Respond to ping
                await manager.send_personal_message(
                    json.dumps({"type": "pong"}),
                    websocket
                )
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
    except Exception as e:
        logging.error(f"WebSocket error: {str(e)}")
        manager.disconnect(websocket, room_id)

@app.get("/api/languages")
async def get_supported_languages():
    """
    Get list of supported languages
    """
    return {
        "languages": [
            {"code": "en", "name": "English"},
            {"code": "ta", "name": "Tamil"},
            {"code": "ml", "name": "Malayalam"},
            {"code": "te", "name": "Telugu"}
        ]
    }

@app.get("/api/room/{room_id}/participants")
async def get_room_participants(room_id: str):
    """
    Get participants in a room
    """
    if room_id in manager.room_connections:
        return {
            "room_id": room_id,
            "participant_count": len(manager.room_connections[room_id])
        }
    else:
        return {
            "room_id": room_id,
            "participant_count": 0
        }

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Run the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
