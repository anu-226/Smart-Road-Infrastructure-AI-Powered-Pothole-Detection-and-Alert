import cv2
import pandas as pd
from ultralytics import YOLO
from tracker import *
import cvzone
import curr_loc as curr_loc
import os
import datetime

def detect(source=0):
    """Run pothole detection on a webcam (default) or a given video file path.

    Args:
        source: 0 for default webcam, or a string path to a video file.
    """
    # Load YOLO model weights (expects custom.pt in the working directory)
    model = YOLO(os.path.join(os.path.dirname(__file__), 'custom.pt'))

    # Open video source
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print(f"Error: cannot open video source: {source}")
        return

    # Define colors and trackers
    tracker = Tracker()
    classNames = ['pothole']

    current_date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    data = {}

    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            print("End of stream or cannot fetch frame.")
            break

        results = model(frame, verbose=False)

        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                w, h = x2 - x1, y2 - y1
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                cls_name = classNames[cls] if cls < len(classNames) else str(cls)

                cvzone.cornerRect(frame, (x1, y1, w, h), l=8)
                cvzone.putTextRect(frame, f"{cls_name} {conf:.2f}", (max(0, x1), max(35, y1)), scale=1, thickness=1)

        cv2.imshow('Pothole Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if data:
        df = pd.DataFrame.from_dict(data, orient='index')
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'id'}, inplace=True)
        df.to_csv(f'{current_date}.csv', index=True)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # Try opening default webcam; fallback to a sample file if present
    default_video = os.path.join(os.path.dirname(__file__), 'test2.mp4')
    src = default_video if os.path.exists(default_video) else 0
    detect(src)
