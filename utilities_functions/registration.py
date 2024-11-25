from flask import render_template, request
import os
import base64
import cv2
import pandas as pd
import numpy as np

# Create or load the users Excel file for storing registration data
def load_user_data(file_path='data/users.xlsx'):
    if os.path.exists(file_path):
        return pd.read_excel(file_path)
    else:
        return pd.DataFrame(columns=['id', 'password', 'img_path'])

# Save the user data to the Excel file
def save_user_data(data, file_path='data/users.xlsx'):
    data.to_excel(file_path, index=False)

# Function to save the captured image
def save_image(img_data, user_id):
    img_path = f"data/user_images/{user_id}.jpg"  # Store the image as a .jpg file
    os.makedirs(os.path.dirname(img_path), exist_ok=True)  # Ensure the directory exists
    with open(img_path, 'wb') as img_file:
        img_file.write(base64.b64decode(img_data.split(',')[1]))  # Remove data:image/png;base64,
    return img_path

def register_user():
    if request.method == 'POST':
        user_id = request.form['id']
        password = request.form['password']
        captured_image_data = request.form.get('capturedImage', None)

        # Load existing user data or create new DataFrame
        user_data = load_user_data()

        # Check if user already exists
        if user_id in user_data['id'].values:
            return render_template('result.html', message="User ID already exists. Please try another.")

        if captured_image_data:
            # Save the captured image
            try:
                img_path = save_image(captured_image_data, user_id)

                # Append the new user's data
                new_user = pd.DataFrame({
                    'id': [user_id],
                    'password': [password],
                    'img_path': [img_path]
                })
                user_data = pd.concat([user_data, new_user], ignore_index=True)

                # Save the updated user data
                save_user_data(user_data)

                return render_template('result.html', message="Registration Successful!")
            except Exception as e:
                return render_template('result.html', message=f"Image saving failed: {str(e)}")
        else:
            return render_template('result.html', message="No image captured for registration.")
    
    return render_template('register.html')
def register_route1():
    if request.method == 'POST':
        user_id = request.form['id']
        password = request.form['password']
        captured_image_data = request.form.get('capturedImage', None)

        # Load existing user data or create new DataFrame
        user_data = load_user_data()

        # Check if user already exists
        if user_id in user_data['id'].values:
            return render_template('result.html', message="User ID already exists. Please try another.")

        if captured_image_data:
            # Save the captured image
            try:
                img_path = save_image(captured_image_data, user_id)

                # Append the new user's data
                new_user = pd.DataFrame({
                    'id': [user_id],
                    'password': [password],
                    'img_path': [img_path]
                })
                user_data = pd.concat([user_data, new_user], ignore_index=True)

                # Save the updated user data
                save_user_data(user_data)

                return render_template('result.html', message="Registration Successful!")
            except Exception as e:
                return render_template('result.html', message=f"Image saving failed: {str(e)}")
        else:
            return render_template('result.html', message="No image captured for registration.")

    return render_template('register.html')
