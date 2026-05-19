
# Real-Time Helmet Detection and Traffic Safety System

## Features
- Helmet Detection
- No Helmet Detection
- Multiple Rider Detection
- Traffic Violation Detection
- Real-Time Video Processing

## Tech Stack
- YOLOv8
- OpenCV
- FastAPI
- Docker
- React Frontend
- Render Deployment
- Vercel Frontend Hosting

## Run Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Run Frontend
```bash
cd frontend
npm install
npm run dev
```

## Docker
```bash
docker build -t helmet-system .
docker run -p 8000:8000 helmet-system
```
