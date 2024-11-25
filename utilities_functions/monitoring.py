import cv2
import time
import pandas as pd
import os
import sys
import importlib
from flask import render_template, request,session
import pyaudio
import numpy as np
import re
import openpyxl


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Define the new row to append



eye_detection_module = importlib.import_module('features_scripts.eye_detection')
detect_cheating = getattr(eye_detection_module, 'detect_cheating')
mouth_detection_module = importlib.import_module('features_scripts.mouth_detection')
detect_mouth_open = getattr(mouth_detection_module, 'detect_mouth_open')
object_detection_module = importlib.import_module('features_scripts.object_detection')
detect_objects = getattr(object_detection_module, 'detect_objects')
voice_detection_module = importlib.import_module('features_scripts.human_voice')
is_voice_detected = getattr(voice_detection_module, 'is_voice_detected')
face_detection_module = importlib.import_module('features_scripts.face_detection')
detect_2faces= getattr(face_detection_module, 'detect_2faces')




# Audio parameters
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
THRESHOLD = 500  # Adjust this value to change sensitivity


p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
# Detection log





def save_log(log_type,user_id, exam_id,workbook,workbook_path,frame):
    path=f'.\data\logs_data\exams\{exam_id}\{user_id}\imgs'
    os.makedirs(path, exist_ok=True)

    new_row = [log_type, time.strftime("%Y-%m-%d %H:%M:%S"),user_id,exam_id] 
    sheet=workbook.active
    sheet.append(new_row)
    workbook.save(workbook_path)
    cv2.imwrite(os.path.join(path, f'{log_type}_{time.strftime("%Y-%m-%d_%H-%M-%S")}.jpg'), frame)





def start_monitoring(monitoring_flag, user_id, exam_id,workbook,workbook_path):
    """Starts the monitoring system when the exam begins."""
    
    path=f'.\data\logs_data\exams\{exam_id}\{user_id}'
    os.makedirs(path, exist_ok=True)
    cap = cv2.VideoCapture(0)

    output_file=os.path.join(path, 'out.mp4')
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = 20  # Frames per second
    fourcc = cv2.VideoWriter_fourcc(*'AVC1')
    out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))    

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        out.write(frame)

        # Face detection
        face_detected = detect_2faces(frame)
        if face_detected:
            save_log("Face Detected",user_id, exam_id,workbook,workbook_path,frame)
        
        detect_cheat = detect_cheating(frame)
        if detect_cheat:
            save_log("Cheating Detected",user_id, exam_id,workbook,workbook_path,frame)

        # Mouth detection (speaking)
        speaking_detected = detect_mouth_open(frame)
        if speaking_detected:
            save_log("Speaking Detected",user_id, exam_id,workbook,workbook_path,frame)

        # Object detection (weird objects)
        objects_detected = detect_objects(frame)
        if objects_detected:
            save_log("Objects Detected",user_id, exam_id,workbook,workbook_path,frame)


        # Voice detection
        is_voice = is_voice_detected(stream)
        if is_voice:
            save_log("Voice Detected",user_id, exam_id,workbook,workbook_path,frame)

        if monitoring_flag[0]==False:
            break

    cap.release()
    out.release()

    cv2.destroyAllWindows()
    

    # Save the detection log after monitoring



