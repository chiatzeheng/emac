import cv2
import torch
import numpy as np
from ultralytics import YOLO
import os
from datetime import datetime

# Initialize YOLOv8 model
model = YOLO("yolov10n.pt")  # Load the smallest YOLOv8 model

# Video setup for live streaming
cap = cv2.VideoCapture(
    0
)  # Use 0 for default webcam, or change to the appropriate camera index

if not cap.isOpened():
    print("Error while trying to open camera. Please check camera index.")
    exit()

# Create a directory for saving alert images
alert_dir = "fall_alerts"
os.makedirs(alert_dir, exist_ok=True)

# Setup logging
log_file = "fall_detection_log.txt"


def log_fall_detection(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"{timestamp} - {message}\n")


# Parameters for fall detection
ASPECT_RATIO_THRESHOLD = 1.2  # Threshold for width/height ratio to detect fall

frame_count = 0
fall_cooldown = 50  # Frames to wait before detecting another fall
frames_since_last_fall = fall_cooldown

# Status variables
status = "Normal"
status_color = (0, 255, 0)  # Green for normal status

while True:
    ret, frame = cap.read()

    if ret:
        frame_count += 1
        frames_since_last_fall += 1

        # Run YOLOv8 inference on the frame
        results = model(frame)

        fall_detected = False

        for r in results:
            boxes = r.boxes

            for box in boxes:
                # Check if the detected object is a person
                if int(box.cls) == 0:  # Class 0 is 'person' in COCO dataset
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                    # Calculate aspect ratio of the bounding box
                    aspect_ratio = (x2 - x1) / (y2 - y1)

                    # Outline the person with green
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    # Check if the aspect ratio indicates a fall (person more horizontal than vertical)
                    if (
                        aspect_ratio > ASPECT_RATIO_THRESHOLD
                        and frames_since_last_fall >= fall_cooldown
                    ):
                        fall_detected = True
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                        cv2.putText(
                            frame,
                            "Fall Detected",
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.9,
                            (0, 0, 255),
                            2,
                        )

        if fall_detected:
            status = "Fall Detected"
            status_color = (0, 0, 255)  # Red for fall detected
            # Alert logging
            alert_message = f"Fall detected in frame {frame_count}"
            log_fall_detection(alert_message)
            print(alert_message)

            # Save alert image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            alert_filename = os.path.join(alert_dir, f"fall_alert_{timestamp}.jpg")
            cv2.imwrite(alert_filename, frame)

            frames_since_last_fall = 0
        else:
            status = "Normal"
            status_color = (0, 255, 0)  # Green for normal status

        # Display status on the top left
        cv2.putText(
            frame,
            f"Status: {status}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            status_color,
            2,
        )

        # Display the frame
        cv2.imshow("Live Fall Detection", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        print("Failed to capture frame. Check camera connection.")
        break

cap.release()
cv2.destroyAllWindows()
print("Live fall detection stopped. Check 'fall_detection_log.txt' for alerts.")
