from flask import render_template, request
import os
import cv2
import face_recognition
import pandas as pd
import base64
import numpy as np

from flask import render_template, request, redirect, url_for,session
from features_scripts.detect_and_verify_face import detect_and_verify



# Load user data from Excel file
def load_user_data(file_path):
    return pd.read_excel(file_path)

# Load device image
def load_device_image(image_path):
    return cv2.imread(image_path)

# Verify faces using face_recognition library
def detect_and_verify(webcam_image, device_image):
    try:
        # Convert both images to RGB format (as face_recognition works on RGB images)
        webcam_rgb = cv2.cvtColor(webcam_image, cv2.COLOR_BGR2RGB)
        device_rgb = cv2.cvtColor(device_image, cv2.COLOR_BGR2RGB)

        # Find face encodings for both images
        webcam_face_encoding = face_recognition.face_encodings(webcam_rgb)
        device_face_encoding = face_recognition.face_encodings(device_rgb)

        if len(webcam_face_encoding) > 0 and len(device_face_encoding) > 0:
            webcam_encoding = webcam_face_encoding[0]
            device_encoding = device_face_encoding[0]

            # Compare the faces
            results = face_recognition.compare_faces([device_encoding], webcam_encoding)
            return results[0]  # Return True if matched, False otherwise

        else:
            return False  # Return False if no face found in one of the images

    except Exception as e:
        print(f"Error in face detection: {e}")
        return False

# Login route function
def login():
    if request.method == 'POST':
        user_data = load_user_data('data/users.xlsx')  # Adjust the path if necessary
        user_id = request.form['id']
        session['user_id'] = user_id 
        password = request.form['password']
        captured_image_data = request.form.get('capturedImage', None)  # Use get to avoid KeyError

        user_data['id'] = user_data['id'].astype(str)
        user_data['password'] = user_data['password'].astype(str)
        user_row = user_data[(user_data['id'] == user_id) & (user_data['password'] == password)]

        # Initialize the message variable
        message = "Invalid ID or Password."  # Default message

        if not user_row.empty:
            image_path = user_row.iloc[0]['img_path']

            # Check if captured_image_data is provided
            if captured_image_data:
                try:
                    img_data = captured_image_data.split(',')[1]  # Assume format is 'data:image/jpeg;base64,...'
                    nparr = np.frombuffer(base64.b64decode(img_data), np.uint8)
                    webcam_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                    if webcam_image is not None:
                        device_image = load_device_image(image_path)
                        if device_image is not None:
                            is_verified = detect_and_verify(webcam_image, device_image)
                            if is_verified:
                                # Redirect to the student profile page on success
                                return (redirect(url_for('student')))
                            else:
                                message = "Verification Failed!"
                        else:
                            message = "Could not load device image. Verification Failed!"
                    else:
                        message = "Could not process captured image. Verification Failed!"
                except Exception as e:
                    message = f"Error processing the captured image: {str(e)}. Verification Failed!"
            else:
                message = "No image captured. Please provide an image to verify. Verification Failed!"
        else:
            message = "Invalid ID or Password."

        # Always render the result page with the final message if verification fails
        return render_template('result.html', message=message)
    return render_template('login.html')  # Render login form


# Admin Login function
import os

# Function to handle user registration
def register_user():
    if request.method == 'POST':
        user_data = load_user_data('data/users.xlsx')  # Adjust the path if necessary
        user_id = request.form['id']
        password = request.form['password']
        captured_image_data = request.form.get('capturedImage', None)

        # Ensure captured image data exists
        if captured_image_data:
            try:
                # Decode the base64 image data
                img_data = captured_image_data.split(',')[1]  # Extract base64 part after 'data:image/png;base64,'
                nparr = np.frombuffer(base64.b64decode(img_data), np.uint8)
                captured_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                # Save the captured image to a directory (ensure the directory exists)
                img_filename = f'static/images/{user_id}.png'  # Save with user_id as the filename
                cv2.imwrite(img_filename, captured_image)

                # Save the user details to the Excel file
                new_user = {
                    'id': [user_id],
                    'password': [password],
                    'img_path': [img_filename]  # Save the image path
                }
                new_user_df = pd.DataFrame(new_user)
                user_data = pd.concat([user_data, new_user_df], ignore_index=True)
                user_data.to_excel('data/users.xlsx', index=False)

                return render_template('result.html', message="Registration Successful!")

            except Exception as e:
                return render_template('result.html', message=f"Error during registration: {str(e)}")

        return render_template('result.html', message="No image captured. Please provide an image.")

    return render_template('register.html')
