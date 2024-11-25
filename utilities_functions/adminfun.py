from flask import Flask, Response, render_template, request, redirect, url_for,session
import cv2
import torch
import winsound
import pandas as pd
from datetime import datetime


def play_alert_sound():
    winsound.Beep(1000, 1000)  # Frequency: 1000Hz, Duration: 1000ms





def home():
    return render_template('index.html')

import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'data/uploaded_exams'  # Define the folder where uploaded files will be stored
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'xlsx', 'pptx'}  # Define allowed file types

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def admin():
    try:
        df = pd.read_excel('data/exams.xlsx')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Exam ID', 'Exam Name', 'Exam Date', 'Exam Time', 'Teacher ID', 'Active', 'Created At', 'Exam File'])

    ongoing_exams = df[df['Active'] == True]  # Filter ongoing exams

    # Convert the DataFrame to a list of dictionaries
    ongoing_exams_list = ongoing_exams.to_dict(orient='records')


    if request.method == 'POST':
        exam_id = request.form['exam_id']
        exam_name = request.form['exam_name']
        exam_date = request.form['exam_date']
        exam_time = request.form['exam_time']
        teacher_id = request.form['teacher_id']
        active = request.form.get('active') == 'true'

        # Handle file upload
        if 'exam_file' not in request.files:
            return render_template('proctor_profile.html', ongoing_exams=ongoing_exams_list, message='No file part.')
        file = request.files['exam_file']

        if file.filename == '':
            return render_template('proctor_profile.html', ongoing_exams=ongoing_exams_list, message='No selected file.')
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            exam_file_path = os.path.join(UPLOAD_FOLDER, filename)
        else:
            return render_template('proctor_profile.html', ongoing_exams=ongoing_exams_list, message='File type not allowed.')

        if exam_id in df['Exam ID'].values:
            return render_template('proctor_profile.html', ongoing_exams=ongoing_exams_list, message='Exam ID already exists.')

        exam_data = {
            'Exam ID': exam_id,
            'Exam Name': exam_name,
            'Exam Date': exam_date,
            'Exam Time': exam_time,
            'Exam File': exam_file_path,  # Save the file path
            'Teacher ID': teacher_id,
            'Active': active,
            'Created At': datetime.now()
        }

        new_exam_df = pd.DataFrame([exam_data])
        df = pd.concat([df, new_exam_df], ignore_index=True)
        df['Exam ID'] = df['Exam ID'].astype(int)
        df.drop_duplicates(subset=['Exam ID'], inplace=True)

        try:
            df.to_excel('data/exams.xlsx', index=False)
        except Exception as e:
            return render_template('proctor_profile.html', ongoing_exams=ongoing_exams_list, message='Error saving Excel file.',id=session.get('admin_id'),phone=session.get('mobile'),name=session.get('name'),email=session.get('Email'),num_exams=session.get('num_exams'),num_exams_active=session.get('num_exams_active'),num_logs=session.get('num_logs'),num_students=session.get('num_students'))

        return redirect(url_for('admin_route'))

    return render_template('proctor_profile.html', ongoing_exams=ongoing_exams_list,id=session.get('admin_id'),phone=session.get('mobile'),name=session.get('name'),email=session.get('Email'),num_exams=session.get('num_exams'),num_exams_active=session.get('num_exams_active'),num_logs=session.get('num_logs'),num_students=session.get('num_students'))

    # Pass ongoing exams to the template




def start_exam():
    exam_id = request.form['exam_id']
    print(f"Starting exam with ID: {exam_id}")  # Debugging line

    # Load existing exams
    try:
        df = pd.read_excel('data/exams.xlsx')
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return render_template('proctor_profile.html', message='Error reading Excel file.',id=session.get('admin_id'),phone=session.get('mobile'),name=session.get('name'),email=session.get('Email'),num_exams=session.get('num_exams'),num_exams_active=session.get('num_exams_active'),num_logs=session.get('num_logs'),num_students=session.get('num_students'))

    # Check if the exam_id exists
    # if exam_id not in df['Exam ID'].values:
    #     print("Exam ID does not exist.")  # Debugging line
    #     return render_template('proctor_profile.html', message='Exam ID does not exist.')

    # Update the 'Active' status of the exam
    df.loc[df['Exam ID'].astype(int) == int(exam_id), 'Active'] = True
    print("Updated Active status to True.")  # Debugging line

    # Save the updated DataFrame to Excel
    try:
        df.to_excel('data/exams.xlsx', index=False)
        print("Excel file updated successfully.")  # Debugging line
    except Exception as e:
        print(f"Error saving Excel file: {e}")
        return render_template('proctor_profile.html', message='Error saving Excel file.',id=session.get('admin_id'),phone=session.get('mobile'),name=session.get('name'),email=session.get('Email'),num_exams=session.get('num_exams'),num_exams_active=session.get('num_exams_active'),num_logs=session.get('num_logs'),num_students=session.get('num_students'))

    return redirect(url_for('admin_route'))


def stop_exam():
    exam_id = request.form['exam_id']
    
    # Load existing exams
    df = pd.read_excel('data/exams.xlsx')

    # Check if the exam_id exists
    if int(exam_id) not in df['Exam ID'].values:

        return render_template('proctor_profile.html', message='Exam ID does not exist.',id=session.get('admin_id'),phone=session.get('mobile'),name=session.get('name'),email=session.get('Email'),num_exams=session.get('num_exams'),num_exams_active=session.get('num_exams_active'),num_logs=session.get('num_logs'),num_students=session.get('num_students'))

    # Update the 'Active' status of the exam
    df.loc[df['Exam ID'].astype(int) == int(exam_id), 'Active'] = False

    # Save the updated DataFrame to Excel
    df.to_excel('data/exams.xlsx', index=False)

    return redirect(url_for('admin_route'))


def student():
    return render_template('student_profile.html')


def ongoing_exams():
    try:
        # Load the Excel file
        df = pd.read_excel('data/exams.xlsx')
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return render_template('ongoing_exams.html', ongoing_exams=None)

    # Filter to get only active exams
    ongoing_exams = df[df['Active'] == True]  # Ensure to check the correct column name
    print(ongoing_exams)  # Debugging line

    return render_template('ongoing_exams.html', ongoing_exams=ongoing_exams)



def register_proctor():
    if request.method == 'POST':
        # Load existing proctor data or create a new DataFrame
        try:
            df = pd.read_excel('data/admins.xlsx')
        except FileNotFoundError:
            df = pd.DataFrame(columns=['ID', 'Password'])  # Ensure to match the correct column names

        # Get data from the registration form
        proctor_id = request.form['id']
        proctor_password = request.form['password']
        proctor_Email= request.form['email']
        proctor_name= request.form['name']
        proctor_mobile= request.form['mobile']




        # Check if the proctor_id already exists
        if proctor_id in df['ID'].values:
            return render_template('registerAdmin.html', message='Proctor ID already exists.')

        # Append new proctor data to the DataFrame
        new_data = pd.DataFrame({'ID': [proctor_id], 'Password': [proctor_password], 'Email': [proctor_Email], 'name': [proctor_name], 'mobile': [proctor_mobile]})
        df = pd.concat([df, new_data], ignore_index=True)

        # Save updated DataFrame to Excel
        df.to_excel('data/admins.xlsx', index=False)
        return redirect(url_for('login_admin_route'))
    
    # Handle GET request by rendering the registration form
    return render_template('registerAdmin.html')


def login_admin():
    if request.method == 'POST':  # Ensure it only processes POST requests
        # Load existing proctor data
        try:
            df = pd.read_excel('data/admins.xlsx')
        except FileNotFoundError:
            return render_template('loginAdmin.html', message='No proctor data available.')

        proctor_id = request.form['id']
        proctor_password = request.form['password']


        if proctor_id in df['ID'].values and df.loc[df['ID'] == proctor_id, 'Password'].values[0] == proctor_password:
            logs=pd.read_excel('data/logs.xlsx')
            exam=pd.read_excel('data/exams.xlsx')
            student=pd.read_excel('data/users.xlsx')
            session["num_students"]=student.shape[0]
            session["num_exams"]=exam.shape[0]
            session["num_logs"]=logs.shape[0]
            session["num_exams_active"]=exam[exam['Active'] == True].shape[0]
            session['admin_id'] = proctor_id
            session["Email"]=df.loc[df['ID'] == proctor_id, 'Email'].values[0]
            session["name"]=df.loc[df['ID'] == proctor_id, 'name'].values[0]
            session["mobile"]=df.loc[df['ID'] == proctor_id, 'mobile'].values[0]


            return redirect(url_for('admin_route'))  # Redirect to admin page
        else:
            return render_template('loginAdmin.html', message='Invalid ID or password.')
    
    return render_template('loginAdmin.html')  # Handle GET request






def show_grades():
    # Load your DataFrame here
    df = pd.read_excel('data/grades.xlsx')

    if request.method == 'POST':
        # Get the exam ID from the form
        exam_id = request.form['exam_id']
        
        # Filter the DataFrame based on the provided exam ID
        filtered_df = df[df['exam_id'] == int(exam_id)]
        
        if filtered_df.empty:
            message = "No grades found for this exam."
            return render_template('grades.html', message=message)
        
        # Convert the filtered DataFrame to a list of dictionaries to pass to the HTML template
        grades = filtered_df[['user_id', 'grade']].to_dict(orient='records')
        
        # Render the HTML template with the filtered DataFrame
        return render_template('grades.html', grades=grades)

    # Handle GET request by displaying the form
    return render_template('grades.html')  # or another template that includes the form

def show_logs():
    # Load your DataFrame here
    df = pd.read_excel('data/logs.xlsx')

    if request.method == 'POST':
        # Get the exam ID from the form
        exam_id = request.form['exam_id']
        
        # Filter the DataFrame based on the provided exam ID
        filtered_df = df[df['exam_id'] == int(exam_id)]
        
        if filtered_df.empty:
            message = "No logs found for this exam."
            return render_template('logs.html', message=message)
        
        # Convert the filtered DataFrame to a list of dictionaries to pass to the HTML template
        print(filtered_df.columns)
    
        logs=filtered_df.to_dict(orient='records')
        
        # Render the HTML template with the filtered DataFrame
        return render_template('logs.html', logs=logs)

    # Handle GET request by displaying the form
    return render_template('logs.html')  # or another template that includes the form



