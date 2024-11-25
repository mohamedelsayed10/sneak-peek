from flask import  render_template, request, abort,session
import pandas as pd
import os
import docx
import fitz  # Required for reading PDF files

import cv2
import time
import pandas as pd

# Detection log


def load_exam_data(filename):
    df = pd.read_excel(filename)
    exams = df.to_dict(orient='records')
    return exams
def index():
    # Load exams from the Excel file
    
    exams = load_exam_data(".\data\exams.xlsx")
    
    # Filter for active exams
    active_exams = [exam for exam in exams if bool(exam['Active']) == True]
    return render_template('exams.html', exams=active_exams)


def load_exam_data(filename):
    df = pd.read_excel(filename)
    exams = df.to_dict(orient='records')
    return exams

# Function to get questions from a specific Excel or Word file for an exam

def get_questions(file_path):
    questions = []

    # Check the file extension to determine how to read the file
    if file_path.endswith('.xlsx'):
        # Load the Excel file
        df = pd.read_excel(file_path)
        
        # Parse the questions
        for i, row in df.iterrows():
            question_data = {
                'question': row['Question'],
                'options': {
                    'A': row['Option A'],
                    'B': row['Option B'],
                    'C': row['Option C'],
                    'D': row['Option D'],
                },
                'correct_answer': row['Correct Answer']
            }
            questions.append(question_data)
    
    elif file_path.endswith('.docx'):
        # Load the Word file
        doc = docx.Document(file_path)
        
        # Assuming the Word document is structured in a specific way:
        for para in doc.paragraphs:
            if para.text.startswith("Q: "):
                question_data = {
                    'question': para.text[3:],  # Remove "Q: "
                    'options': {},
                    'correct_answer': None  # This can be updated later based on your structure
                }
                questions.append(question_data)
            elif para.text.startswith("A: "):
                questions[-1]['options']['A'] = para.text[3:]  # Remove "A: "
            elif para.text.startswith("B: "):
                questions[-1]['options']['B'] = para.text[3:]  # Remove "B: "
            elif para.text.startswith("C: "):
                questions[-1]['options']['C'] = para.text[3:]  # Remove "C: "
            elif para.text.startswith("D: "):
                questions[-1]['options']['D'] = para.text[3:]  # Remove "D: "
            elif para.text.startswith("Correct Answer: "):
                questions[-1]['correct_answer'] = para.text[16:]  # Remove "Correct Answer: "

    elif file_path.endswith('.pdf'):
        # Load the PDF file
        pdf_document = fitz.open(file_path)
        
        # Extract text from each page
        for page in pdf_document:
            text = page.get_text().splitlines()
            for line in text:
                if line.startswith("Q: "):
                    question_data = {
                        'question': line[3:],  # Remove "Q: "
                        'options': {},
                        'correct_answer': None  # This can be updated later based on your structure
                    }
                    questions.append(question_data)
                elif line.startswith("A: "):
                    questions[-1]['options']['A'] = line[3:]  # Remove "A: "
                elif line.startswith("B: "):
                    questions[-1]['options']['B'] = line[3:]  # Remove "B: "
                elif line.startswith("C: "):
                    questions[-1]['options']['C'] = line[3:]  # Remove "C: "
                elif line.startswith("D: "):
                    questions[-1]['options']['D'] = line[3:]  # Remove "D: "
                elif line.startswith("Correct Answer: "):
                    questions[-1]['correct_answer'] = line[16:]  # Remove "Correct Answer: "

        pdf_document.close()
    else:
        abort(404, description="Unsupported file type")

    return questions

def start_exam_student(exam_id):
    # Load the exams data again to find the corresponding file path
    print("this exam id start paramter")
    print(exam_id)
    exams = load_exam_data('.\data\exams.xlsx')
    session['exam_id'] = exam_id
    print("this exam id from start exam")
    print(session.get('exam_id'))
    selected_exam = next((exam for exam in exams if int(exam['Exam ID']) == int(session.get('exam_id'))), None)

    if not selected_exam:
        abort(404, description="Exam not found")
    
    # Get the questions for the selected exam
    questions = get_questions(f".\{selected_exam['Exam File']}")

    return render_template('exam.html', questions=questions, enumerate=enumerate)

def submit_exam_student(exam_id, user_id, exam_id2):
    print(exam_id)
    print(exam_id2)
    # Load the exams data again to find the corresponding file path
    exams = load_exam_data('.\data\exams.xlsx')
    selected_exam = next((exam for exam in exams if int(exam['Exam ID']) == int(exam_id)), None)

    if not selected_exam:
        abort(404, description="Exam not found")
    
    # Get the questions again to validate answers
    questions = get_questions(selected_exam['Exam File'])
    score = 0
    total = len(questions)

    # Calculate score based on the submitted answers
    for i, question in enumerate(questions):
        user_answer = request.form.get(f'question-{i}')
        if user_answer == question['correct_answer']:
            score += 1

    grade = (score / total) * 100
    student_grade = {
        'user_id': user_id,
        'exam_id': exam_id2,
        'grade': grade
    }

    # Save the student's grade to the database
    df = pd.read_excel('.\data\grades.xlsx')
    new_row = pd.DataFrame([student_grade], columns=['user_id', 'exam_id', 'grade'])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_excel('.\data\grades.xlsx', index=False)

    # Prepare the message
    message = f'Your score for exam {exam_id} is {score}/{total} ({grade:.2f}%)'
    return render_template('exam_result.html', message=message)











