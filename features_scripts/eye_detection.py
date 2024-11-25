import cv2
import mediapipe as mp
import numpy as np
import time
import winsound

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def play_alert_sound():
    winsound.Beep(1000, 1000)

def get_eye_coordinates(landmarks, image_shape):
    left_eye_left = landmarks[33]
    left_eye_right = landmarks[133]
    right_eye_left = landmarks[362]
    right_eye_right = landmarks[263]
    height, width = image_shape[:2]
    left_eye_left = (int(left_eye_left.x * width), int(left_eye_left.y * height))
    left_eye_right = (int(left_eye_right.x * width), int(left_eye_right.y * height))
    right_eye_left = (int(right_eye_left.x * width), int(right_eye_left.y * height))
    right_eye_right = (int(right_eye_right.x * width), int(right_eye_right.y * height))
    return left_eye_left, left_eye_right, right_eye_left, right_eye_right

looking_away_start = None
cheating_detected = False

def detect_cheating(frame):
    global looking_away_start, cheating_detected
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)
    looking_away = False

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            left_eye_left, left_eye_right, right_eye_left, right_eye_right = get_eye_coordinates(face_landmarks.landmark, frame.shape)
            center_x = (left_eye_left[0] + left_eye_right[0] + right_eye_left[0] + right_eye_right[0]) // 4
            center_y = (left_eye_left[1] + left_eye_right[1] + right_eye_left[1] + right_eye_right[1]) // 4
            height, width = frame.shape[:2]
            screen_center_x, screen_center_y = width // 2, height // 2
            distance = np.sqrt((center_x - screen_center_x)**2 + (center_y - screen_center_y)**2)
            threshold = width * 0.15
            if distance > threshold:
                looking_away = True

    current_time = time.time()
    if looking_away:
        if looking_away_start is None:
            looking_away_start = current_time
        elif current_time - looking_away_start >= 2:
            if not cheating_detected:
                cheating_detected = True
                print("looking away !!")
                play_alert_sound()
            return True
    else:
        looking_away_start = None
        cheating_detected = False

    return False
