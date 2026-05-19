
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

model = YOLO("yolov8n.pt", task="detect")

@app.get("/")
def root():
    return {"message": "Helmet Detection API Running"}

@app.post("/detect")
async def detect_video(file: UploadFile = File(...)):
    try:
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.write(await file.read())

        cap = cv2.VideoCapture(temp.name)

        detections = []
        frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            frame_count += 1

            # process every 10th frame
            if frame_count % 10 != 0:
                continue

            results = model(frame)

            for result in results:
                boxes = result.boxes

                detections.append({
                    "objects_detected": len(boxes)
                })

            # prevent Render memory crash
            if len(detections) > 20:
                break

        cap.release()

        return {
            "status": "processed",
            "frames_processed": frame_count,
            "detections": detections
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
