from flask import Flask, render_template, jsonify, send_from_directory
import os
import mimetypes
from flask_cors import CORS


EXAMS_FOLDER = '.\data\logs_data\exams'

# Get the list of exams
def get_exams():
    return [exam for exam in os.listdir(EXAMS_FOLDER) if os.path.isdir(os.path.join(EXAMS_FOLDER, exam))]

# Get the list of students for a given exam
def get_students(exam):
    exam_path = os.path.join(EXAMS_FOLDER, exam)
    return [student for student in os.listdir(exam_path) if os.path.isdir(os.path.join(exam_path, student))]

# Get media files for a given student in a given exam
def get_student_media(exam, student):
    student_path = os.path.join(EXAMS_FOLDER, exam, student)
    img_folder = os.path.join(student_path, 'imgs')

    images = [f"/media/{exam}/{student}/imgs/{img}" 
              for img in os.listdir(img_folder) if img.lower().endswith(('.png', '.jpg', '.jpeg'))]
    video = f"/media/{exam}/{student}/out.mp4" if 'out.mp4' in os.listdir(student_path) else None
    audio = f"/media/{exam}/{student}/audio.wav" if 'audio.wav' in os.listdir(student_path) else None

    return {'images': images, 'video': video, 'audio': audio}
def media_files(exam, student, filename):
    file_path = os.path.join(EXAMS_FOLDER, exam, student, filename)
    if not os.path.exists(file_path):
        return "File not found", 404
    
    mime_type = 'video/mp4' if filename.endswith('.mp4') else None
    response = send_from_directory(os.path.join(EXAMS_FOLDER, exam, student), filename)
    response.headers['Accept-Ranges'] = 'bytes'
    response.headers['Content-Type'] = mime_type
    return response
def log_media():
    exams = get_exams()
    return render_template('logs_media.html', exams=exams)

