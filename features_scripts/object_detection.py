import cv2
import torch
import winsound

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Define weird objects (based on COCO dataset classes)
weird_objects = ['cell phone', 'laptop', 'book']

def play_alert_sound():
    winsound.Beep(1000, 1000)  # Frequency: 1000Hz, Duration: 1000ms

def detect_objects(frame):
    # Run the YOLOv5 model on the frame
    results = model(frame)

    # Process results
    detections = results.pandas().xyxy[0]  # Get detections as a pandas DataFrame

    for index, row in detections.iterrows():
        class_name = row['name']
        confidence = row['confidence']  # Get confidence score
        if class_name in weird_objects:
            # Output detected object information
            print(f"ALERT: Detected {class_name} with confidence {confidence:.2f}")
            play_alert_sound()  # Play alert sound
            return True
