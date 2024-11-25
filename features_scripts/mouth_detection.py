import cv2
import mediapipe as mp
import numpy as np
import time
import winsound

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def play_alert_sound():
    winsound.Beep(1000, 1000)  # Frequency: 1000Hz, Duration: 1000ms

talking_start = None
talking_detected = False

def calculate_lip_distance(landmarks, image_shape):
    # Get relevant lip landmarks
    upper_lip_top = landmarks[13]
    lower_lip_bottom = landmarks[14]
    
    # Convert normalized coordinates to pixel coordinates
    height, width = image_shape[:2]
    upper_lip_top = (int(upper_lip_top.x * width), int(upper_lip_top.y * height))
    lower_lip_bottom = (int(lower_lip_bottom.x * width), int(lower_lip_bottom.y * height))
    
    # Calculate the distance between upper and lower lip
    distance = np.sqrt((upper_lip_top[0] - lower_lip_bottom[0])**2 + (upper_lip_top[1] - lower_lip_bottom[1])**2)
    return distance

def detect_mouth_open(frame):
    global talking_start, talking_detected
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)
    
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            lip_distance = calculate_lip_distance(face_landmarks.landmark, frame.shape)
            if lip_distance > 5:  # Threshold for detecting open lips; adjust based on calibration
                if talking_start is None:
                    talking_start = time.time()
                elif time.time() - talking_start >= 2:
                    if not talking_detected:
                        talking_detected = True
                        play_alert_sound()
                        print("speaking !")
                    return True
            else:
                talking_start = None
                talking_detected = False
    return False
