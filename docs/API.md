# SignSync Meet API Documentation

## Overview

The SignSync Meet API provides endpoints for AI-powered voice and sign language recognition, real-time caption generation, and WebSocket communication for live video conferencing.

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://your-backend-domain.com`

## Authentication

Most endpoints require authentication via Firebase JWT tokens. Include the token in the Authorization header:

```
Authorization: Bearer <firebase_jwt_token>
```

## Endpoints

### Health Check

#### GET `/health`

Check the health status of the API and AI services.

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "sign_recognition": true,
    "voice_recognition": true,
    "caption_service": true
  }
}
```

#### GET `/api/models/status`

Get detailed status of all AI models and their availability.

**Response:**
```json
{
  "models_directory": "models",
  "available_models": {
    "asl_models": ["asl_model.h5"],
    "vosk_models": ["vosk-model-en-us-0.22", "vosk-model-ta-0.22"],
    "other_models": []
  },
  "validation_results": {
    "asl_model": true,
    "vosk_english": true,
    "vosk_tamil": true,
    "vosk_malayalam": false,
    "vosk_telugu": false
  },
  "asl_model_path": "models/asl_model.h5",
  "vosk_models": {
    "en": "models/vosk/vosk-model-en-us-0.22",
    "ta": "models/vosk/vosk-model-ta-0.22"
  },
  "services_ready": {
    "sign_recognition": true,
    "voice_recognition": true,
    "caption_service": true
  }
}
```

### Voice Recognition

#### POST `/api/voice-to-text`

Convert audio data to text using voice recognition.

**Request Body:**
```json
{
  "audio_data": "base64_encoded_audio",
  "language": "en",
  "user_id": "user123"
}
```

**Parameters:**
- `audio_data` (string, required): Base64 encoded audio data
- `language` (string, optional): Language code (en, ta, ml, te). Default: "en"
- `user_id` (string, optional): User identifier for caption attribution

**Response:**
```json
{
  "success": true,
  "text": "Hello everyone, how are you doing?",
  "caption": {
    "id": "caption_123",
    "text": "Hello everyone, how are you doing?",
    "type": "voice",
    "user_id": "user123",
    "user_name": "John Doe",
    "user_photo": "https://example.com/photo.jpg",
    "language": "en",
    "timestamp": "2024-01-15T10:30:00Z",
    "confidence": 0.95
  },
  "language": "en"
}
```

### Sign Language Recognition

#### POST `/api/sign-to-text`

Convert sign language image to text using computer vision.

**Request Body:**
```json
{
  "image_data": "base64_encoded_image",
  "language": "en",
  "user_id": "user123"
}
```

**Parameters:**
- `image_data` (string, required): Base64 encoded image data
- `language` (string, optional): Language code (en, ta, ml, te). Default: "en"
- `user_id` (string, optional): User identifier for caption attribution

**Response:**
```json
{
  "success": true,
  "text": "Thank you",
  "caption": {
    "id": "caption_456",
    "text": "Thank you",
    "type": "sign",
    "user_id": "user123",
    "user_name": "John Doe",
    "user_photo": "https://example.com/photo.jpg",
    "language": "en",
    "timestamp": "2024-01-15T10:30:00Z",
    "confidence": 0.92
  },
  "language": "en"
}
```

### File Upload

#### POST `/api/upload-audio`

Upload audio file for processing.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: audio file

**Response:**
```json
{
  "success": true,
  "text": "Transcribed text from audio file",
  "filename": "audio.wav"
}
```

#### POST `/api/upload-image`

Upload image file for sign language recognition.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: image file

**Response:**
```json
{
  "success": true,
  "text": "Recognized sign language text",
  "filename": "sign_image.jpg"
}
```

### Language Support

#### GET `/api/languages`

Get list of supported languages.

**Response:**
```json
{
  "languages": [
    {"code": "en", "name": "English"},
    {"code": "ta", "name": "Tamil"},
    {"code": "ml", "name": "Malayalam"},
    {"code": "te", "name": "Telugu"}
  ]
}
```

### Room Management

#### GET `/api/room/{room_id}/participants`

Get participants in a specific room.

**Parameters:**
- `room_id` (string, required): Room identifier

**Response:**
```json
{
  "room_id": "meeting_123",
  "participant_count": 5
}
```

## WebSocket API

### Connection

Connect to WebSocket endpoint for real-time communication:

```
ws://localhost:8000/ws/{room_id}
```

### Message Types

#### Audio Data

Send audio data for real-time voice recognition:

```json
{
  "type": "audio_data",
  "data": "base64_encoded_audio",
  "language": "en",
  "user_id": "user123"
}
```

#### Image Data

Send image data for real-time sign language recognition:

```json
{
  "type": "image_data",
  "data": "base64_encoded_image",
  "language": "en",
  "user_id": "user123"
}
```

#### Ping/Pong

Keep connection alive:

```json
{
  "type": "ping"
}
```

**Response:**
```json
{
  "type": "pong"
}
```

### Caption Broadcast

When a caption is generated, it's broadcast to all participants in the room:

```json
{
  "type": "caption",
  "data": {
    "success": true,
    "text": "Hello everyone",
    "caption": {
      "id": "caption_123",
      "text": "Hello everyone",
      "type": "voice",
      "user_id": "user123",
      "user_name": "John Doe",
      "user_photo": "https://example.com/photo.jpg",
      "language": "en",
      "timestamp": "2024-01-15T10:30:00Z",
      "confidence": 0.95
    },
    "language": "en"
  }
}
```

## Error Handling

### Error Response Format

```json
{
  "detail": "Error message description",
  "status_code": 400,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Common Error Codes

- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Missing or invalid authentication
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

### Example Error Response

```json
{
  "detail": "Invalid audio data format",
  "status_code": 400,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Rate Limiting

API endpoints are rate-limited to prevent abuse:

- **Voice Recognition**: 100 requests per minute per user
- **Sign Recognition**: 100 requests per minute per user
- **File Upload**: 50 requests per minute per user
- **WebSocket**: 1000 messages per minute per connection

## Data Formats

### Audio Data

Supported audio formats:
- **WAV**: 16-bit PCM, 16kHz sample rate
- **MP3**: 128kbps or higher
- **OGG**: Vorbis codec

### Image Data

Supported image formats:
- **JPEG**: RGB color space
- **PNG**: RGB or RGBA color space
- **WebP**: RGB color space

Recommended image specifications:
- **Resolution**: 640x480 or higher
- **Format**: JPEG
- **Quality**: 80% or higher

## SDK Examples

### JavaScript/TypeScript

```typescript
// Voice recognition
const response = await fetch('/api/voice-to-text', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${firebaseToken}`
  },
  body: JSON.stringify({
    audio_data: base64AudioData,
    language: 'en',
    user_id: userId
  })
});

const result = await response.json();
console.log('Transcribed text:', result.text);
```

### Python

```python
import requests
import base64

# Voice recognition
def transcribe_audio(audio_data, language='en', user_id=None):
    url = 'http://localhost:8000/api/voice-to-text'
    headers = {
        'Authorization': f'Bearer {firebase_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'audio_data': base64.b64encode(audio_data).decode('utf-8'),
        'language': language,
        'user_id': user_id
    }
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()
```

## WebSocket Client Example

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/meeting_123');

ws.onopen = () => {
  console.log('Connected to WebSocket');
};

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  
  if (message.type === 'caption') {
    console.log('New caption:', message.data.caption.text);
    // Display caption in UI
  }
};

// Send audio data
function sendAudioData(audioData, language, userId) {
  const message = {
    type: 'audio_data',
    data: audioData,
    language: language,
    user_id: userId
  };
  ws.send(JSON.stringify(message));
}
```

## Testing

### Using curl

```bash
# Health check
curl -X GET http://localhost:8000/health

# Voice recognition
curl -X POST http://localhost:8000/api/voice-to-text \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_FIREBASE_TOKEN" \
  -d '{
    "audio_data": "base64_encoded_audio",
    "language": "en",
    "user_id": "user123"
  }'
```

### Using Postman

1. Import the API collection
2. Set environment variables for base URL and auth token
3. Run the test suite

## Changelog

### v1.0.0
- Initial API release
- Voice and sign language recognition
- WebSocket real-time communication
- Multilingual support
- File upload endpoints

## Support

For API support and questions:
- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/your-username/signsync-meet/issues)
- **Email**: api-support@signsync-meet.com
