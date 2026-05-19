
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import cv2
import tempfile

app = FastAPI(title="Helmet Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = YOLO("yolov8n.pt")

@app.get("/")
def root():
    return {"message": "Helmet Detection API Running"}

@app.post("/detect")
async def detect_video(file: UploadFile = File(...)):
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(await file.read())

    cap = cv2.VideoCapture(temp.name)

    detections = []

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        results = model(frame)

        for result in results:
            boxes = result.boxes
            detections.append({
                "objects_detected": len(boxes)
            })

    cap.release()

    return {
        "status": "processed",
        "frames_processed": len(detections),
        "detections": detections[:10]
    }
