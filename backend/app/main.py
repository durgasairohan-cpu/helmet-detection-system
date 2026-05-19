from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import cv2
import tempfile
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = YOLO("yolov8n.pt")

@app.get("/")
def home():
    return {"message": "API Running"}

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    try:
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        contents = await file.read()

        temp.write(contents)
        temp.close()

        cap = cv2.VideoCapture(temp.name)

        if not cap.isOpened():
            return {"error": "Could not open video"}

        frame_count = 0
        detections = []

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            frame_count += 1

            # Skip frames for speed
            if frame_count % 15 != 0:
                continue

            results = model.predict(frame, verbose=False)

            count = 0

            for result in results:
                count += len(result.boxes)

            detections.append({
                "frame": frame_count,
                "objects": count
            })

            # Prevent memory overload
            if len(detections) >= 10:
                break

        cap.release()

        os.remove(temp.name)

        return {
            "status": "processed",
            "frames_processed": frame_count,
            "sample_detections": detections
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
