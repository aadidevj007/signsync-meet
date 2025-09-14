# SignSync Meet Deployment Guide

This guide covers deploying SignSync Meet to production environments.

## Overview

SignSync Meet consists of three main components:
- **Frontend**: React application (Firebase Hosting)
- **Backend**: FastAPI server (Render/Heroku)
- **AI Models**: Python scripts and trained models

## Prerequisites

### Required Accounts
- **Firebase** account and project
- **Google Cloud** account with Speech API enabled
- **Render** or **Heroku** account for backend hosting
- **GitHub** repository for code hosting

### Required Tools
- **Node.js** 18+ and npm
- **Python** 3.11+
- **Firebase CLI**: `npm install -g firebase-tools`
- **Git** for version control

## Frontend Deployment (Firebase Hosting)

### 1. Setup Firebase Project

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login to Firebase
firebase login

# Initialize Firebase project
cd frontend
firebase init hosting
```

### 2. Configure Firebase

Update `firebase.json`:
```json
{
  "hosting": {
    "public": "build",
    "ignore": [
      "firebase.json",
      "**/.*",
      "**/node_modules/**"
    ],
    "rewrites": [
      {
        "source": "**",
        "destination": "/index.html"
      }
    ]
  }
}
```

Update `.firebaserc`:
```json
{
  "projects": {
    "default": "your-firebase-project-id"
  }
}
```

### 3. Environment Configuration

Create `.env.production`:
```env
REACT_APP_FIREBASE_API_KEY=your_production_firebase_api_key
REACT_APP_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
REACT_APP_FIREBASE_PROJECT_ID=your_project_id
REACT_APP_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
REACT_APP_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
REACT_APP_FIREBASE_APP_ID=your_app_id
REACT_APP_API_URL=https://your-backend-domain.com
REACT_APP_WS_URL=wss://your-backend-domain.com
REACT_APP_JITSI_DOMAIN=meet.jit.si
```

### 4. Build and Deploy

```bash
# Install dependencies
npm install

# Build for production
npm run build

# Deploy to Firebase
firebase deploy
```

### 5. Custom Domain (Optional)

```bash
# Add custom domain
firebase hosting:channel:deploy production --only hosting

# Configure SSL certificate
firebase hosting:channel:open production
```

## Backend Deployment (Render)

### 1. Prepare Backend

Create `render.yaml`:
```yaml
services:
  - type: web
    name: signsync-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: FIREBASE_API_KEY
        value: your_firebase_api_key
      - key: GOOGLE_APPLICATION_CREDENTIALS
        value: your_google_credentials_json
      - key: PORT
        value: 8000
```

### 2. Environment Variables

Set these in Render dashboard:
```env
FIREBASE_API_KEY=your_firebase_api_key
FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_STORAGE_BUCKET=your_project.appspot.com
FIREBASE_MESSAGING_SENDER_ID=your_sender_id
FIREBASE_APP_ID=your_app_id
GOOGLE_APPLICATION_CREDENTIALS=your_google_credentials_json
GOOGLE_CLOUD_PROJECT_ID=your_google_cloud_project_id
PORT=8000
HOST=0.0.0.0
DEBUG=False
ALLOWED_ORIGINS=https://your-frontend-domain.com
JITSI_MEET_DOMAIN=meet.jit.si
SIGN_MODEL_PATH=models/sign_language_model.h5
VOSK_MODEL_PATH=models/vosk-model-en-us-0.22
LOG_LEVEL=INFO
```

### 3. Deploy to Render

```bash
# Connect GitHub repository to Render
# Render will auto-deploy on git push

# Or deploy manually
git push origin main
```

## Backend Deployment (Heroku)

### 1. Setup Heroku

```bash
# Install Heroku CLI
npm install -g heroku

# Login to Heroku
heroku login

# Create Heroku app
heroku create your-app-name

# Add Python buildpack
heroku buildpacks:set heroku/python
```

### 2. Environment Variables

```bash
# Set environment variables
heroku config:set FIREBASE_API_KEY=your_firebase_api_key
heroku config:set GOOGLE_APPLICATION_CREDENTIALS=your_google_credentials_json
heroku config:set PORT=8000
heroku config:set HOST=0.0.0.0
heroku config:set DEBUG=False
heroku config:set ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### 3. Deploy

```bash
# Deploy to Heroku
git push heroku main

# Check logs
heroku logs --tail
```

## AI Models Setup

### 1. Train Sign Language Model

```bash
cd ai-model
pip install -r requirements.txt

# Train the model
python train_sign_language_model.py
```

### 2. Setup Vosk Models

```bash
# Download and setup Vosk models
python setup_vosk.py
```

### 3. Upload Models to Backend

```bash
# Copy trained models to backend
cp models/sign_language_model.h5 ../backend/models/
cp -r models/vosk-model-* ../backend/models/
```

## Google Cloud Setup

### 1. Enable APIs

```bash
# Enable Speech-to-Text API
gcloud services enable speech.googleapis.com

# Enable Cloud Storage API (if needed)
gcloud services enable storage.googleapis.com
```

### 2. Create Service Account

```bash
# Create service account
gcloud iam service-accounts create signsync-api \
    --description="SignSync API Service Account" \
    --display-name="SignSync API"

# Grant permissions
gcloud projects add-iam-policy-binding your-project-id \
    --member="serviceAccount:signsync-api@your-project-id.iam.gserviceaccount.com" \
    --role="roles/speech.admin"

# Create and download key
gcloud iam service-accounts keys create service-account-key.json \
    --iam-account=signsync-api@your-project-id.iam.gserviceaccount.com
```

### 3. Upload Credentials

Upload `service-account-key.json` to your backend hosting platform.

## Firebase Configuration

### 1. Authentication Setup

1. Go to Firebase Console
2. Enable Authentication
3. Enable Email/Password and Google providers
4. Configure authorized domains

### 2. Firestore Setup

1. Create Firestore database
2. Set up security rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

### 3. Hosting Configuration

1. Configure custom domain
2. Set up SSL certificate
3. Configure redirects and rewrites

## Domain Configuration

### 1. Custom Domain Setup

**Frontend (Firebase Hosting):**
```bash
# Add custom domain
firebase hosting:channel:deploy production --only hosting

# Configure DNS
# Add CNAME record: www -> your-project.web.app
# Add A record: @ -> Firebase IP
```

**Backend (Render/Heroku):**
- Render: Automatic custom domain
- Heroku: Add custom domain in dashboard

### 2. SSL Certificates

- **Firebase**: Automatic SSL
- **Render**: Automatic SSL
- **Heroku**: Automatic SSL with custom domains

## Monitoring and Logging

### 1. Application Monitoring

**Frontend:**
- Firebase Analytics
- Google Analytics
- Error tracking with Sentry

**Backend:**
- Render/Heroku logs
- Application metrics
- Error tracking

### 2. Log Management

```bash
# View logs
heroku logs --tail
# or
render logs --follow
```

### 3. Performance Monitoring

- **Frontend**: Lighthouse CI
- **Backend**: APM tools
- **Database**: Firestore monitoring

## Security Configuration

### 1. CORS Settings

Update backend CORS configuration:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

### 2. Environment Security

- Use environment variables for secrets
- Never commit API keys to repository
- Use different keys for development/production

### 3. Firebase Security Rules

```javascript
// Firestore rules
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

## CI/CD Pipeline

### 1. GitHub Actions

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '18'
      - name: Install dependencies
        run: cd frontend && npm install
      - name: Build
        run: cd frontend && npm run build
      - name: Deploy to Firebase
        uses: FirebaseExtended/action-hosting-deploy@v0
        with:
          repoToken: '${{ secrets.GITHUB_TOKEN }}'
          firebaseServiceAccount: '${{ secrets.FIREBASE_SERVICE_ACCOUNT }}'
          channelId: live
          projectId: your-project-id

  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Render
        uses: render-actions/deploy@v1
        with:
          service-id: your-render-service-id
          api-key: ${{ secrets.RENDER_API_KEY }}
```

### 2. Environment Variables

Set these in GitHub Secrets:
- `FIREBASE_SERVICE_ACCOUNT`
- `RENDER_API_KEY`
- `HEROKU_API_KEY`

## Troubleshooting

### Common Issues

**Frontend Issues:**
- Build failures: Check Node.js version
- Firebase auth errors: Verify API keys
- CORS errors: Check backend CORS configuration

**Backend Issues:**
- Import errors: Check Python version
- Model loading errors: Verify model paths
- API key errors: Check environment variables

**Deployment Issues:**
- Build timeouts: Increase build timeout
- Memory issues: Upgrade hosting plan
- SSL errors: Check domain configuration

### Debug Commands

```bash
# Check build logs
firebase hosting:channel:open production

# Check backend logs
heroku logs --tail
# or
render logs --follow

# Test API endpoints
curl -X GET https://your-backend-domain.com/health
```

## Performance Optimization

### 1. Frontend Optimization

- Enable gzip compression
- Use CDN for static assets
- Implement lazy loading
- Optimize images

### 2. Backend Optimization

- Enable caching
- Use connection pooling
- Optimize database queries
- Implement rate limiting

### 3. AI Model Optimization

- Use model quantization
- Implement model caching
- Optimize inference pipeline
- Use GPU acceleration

## Backup and Recovery

### 1. Database Backup

```bash
# Firestore backup
gcloud firestore export gs://your-backup-bucket/firestore-backup

# Restore
gcloud firestore import gs://your-backup-bucket/firestore-backup
```

### 2. Model Backup

```bash
# Backup AI models
tar -czf models-backup.tar.gz models/
# Upload to cloud storage
```

### 3. Configuration Backup

- Export environment variables
- Backup configuration files
- Document deployment steps

## Scaling

### 1. Horizontal Scaling

- **Frontend**: Firebase Hosting auto-scales
- **Backend**: Use load balancers
- **Database**: Firestore auto-scales

### 2. Vertical Scaling

- Upgrade hosting plans
- Increase memory/CPU
- Optimize resource usage

### 3. Performance Monitoring

- Set up alerts
- Monitor response times
- Track error rates
- Monitor resource usage

## Maintenance

### 1. Regular Updates

- Update dependencies
- Security patches
- Model retraining
- Performance optimization

### 2. Monitoring

- Health checks
- Error tracking
- Performance metrics
- User feedback

### 3. Documentation

- Keep deployment docs updated
- Document configuration changes
- Maintain runbooks
- Update troubleshooting guides

---

For additional support, refer to:
- [API Documentation](API.md)
- [Contributing Guide](CONTRIBUTING.md)
- [GitHub Issues](https://github.com/your-username/signsync-meet/issues)
