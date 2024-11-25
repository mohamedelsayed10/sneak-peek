from flask import Flask, render_template, request,session,redirect, url_for
import pandas as pd
from utilities_functions.login import login  # Import your login functions
from utilities_functions.adminfun import start_exam, stop_exam,register_proctor, login_admin, ongoing_exams, show_grades,show_logs,ongoing_exams,admin
from utilities_functions.registration import register_user ,register_route1  # Import the register_user function
from utilities_functions.exam import  *# Import the register_user function
from utilities_functions.monitoring import start_monitoring
from utilities_functions.monitor_activity import start_monitoring_activity
import threading
import openpyxl
from utilities_functions.recored import record_audio
from flask_cors import CORS
from utilities_functions.log_media import *
# Load the existing workbook
workbook_path ='.\data\logs.xlsx'
 # Replace with your file path
workbook = openpyxl.load_workbook(".\data\logs.xlsx")

# Select the active worksheet or a specific sheet
sheet = workbook.active  # or workbook['SheetName']

app = Flask(__name__)
app.secret_key = "12345"  # Replace this with a strong, random value
CORS(app)  # Enable Cross-Origin Resource Sharing (if needed)
monitoring_flag = [False]
actvity_flag =[ False]
voice_flag=[False]

monitor_thread = None
actvity_thread = None
voice_thread = None


@app.route('/')
def home():
    return render_template('index.html')

# Student login route
@app.route('/login', methods=['GET', 'POST'])
def login_route():
   # Save user_id in session
    return login()
     

# Admin (Proctor) login route
@app.route('/loginAdmin', methods=['GET', 'POST'])
def login_admin_route():
    if request.method == 'POST':
        
        return login_admin()  # Call the login function to handle the form data
    return render_template('loginAdmin.html')  # Adjust as necessary  # Render the login form for GET request


# Admin (Proctor) registration route
@app.route('/registerAdmin', methods=['GET', 'POST'])
def register_admin_route():
    return register_proctor()  # This now handles both GET and POST


# Admin dashboard route
@app.route('/admin', methods=['GET', 'POST'])
def admin_route():
    return admin()
    


# Start exam route
@app.route('/start_exam', methods=['POST'])
def start_exam_teacher():
    return start_exam()

# Stop exam route
@app.route('/stop_exam', methods=['POST'])
def stop_exam_teacher():
    return stop_exam()

# Student profile route after successful login

@app.route('/student')
def student():
    return index()


# Route for the registration pag
@app.route('/register', methods=['GET', 'POST'])
def register_route():
    return register_route1()

@app.route('/register', methods=['GET', 'POST'])
def register_student_route():
    return register_user()  # Call the register_user function




@app.route('/exam/<int:exam_id>', methods=['GET'])

def student_exam(exam_id):
    session['exam_id'] = exam_id
    user_id = session.get('user_id')
    if exam_id is None:
        print("exam id is none")
    global monitoring_thread, monitoring_flag, actvity_thread,actvity_flag,voice_thread,voice_flag
    monitoring_flag[0] = True
    actvity_flag[0]=True
    voice_flag[0]=True


    monitoring_thread =  threading.Thread(target=start_monitoring, args=(monitoring_flag, user_id, exam_id,workbook,workbook_path))
    voice_thread=threading.Thread(target=record_audio,args=(voice_flag,user_id, exam_id))
    actvity_thread = threading.Thread(target=start_monitoring_activity, args=(actvity_flag,user_id, exam_id,workbook,workbook_path))
    monitoring_thread.start()
    actvity_thread.start()
    voice_thread.start()
    return start_exam_student(exam_id)


@app.route('/submit/<int:exam_id>', methods=['POST'])
def submit_exam(exam_id):
    global monitoring_flag,monitoring_thread,actvity_thread,actvity_flag
    monitoring_flag[0] = False
    monitoring_thread.join()  # Wait for monitoring to finish
    actvity_flag[0]=False
    actvity_thread.join()
    voice_flag[0]=False
    voice_thread.join()

    user_id = session.get('user_id')
    exam_id2 = session.get('exam_id')
    return submit_exam_student(exam_id, user_id, exam_id2)

@app.route('/submit_answers', methods=['POST'])

def submit_answers():
    answers = request.form.to_dict()
    # Process the answers as needed, e.g., compare them to the correct answers
    # You can add your logic here to check if answers are correct
    return 'Answers submitted successfully!'

df = pd.read_excel('./data/grades.xlsx')

@app.route('/ongoing_exams')
def ongoing_exams_route():
    return ongoing_exams()

@app.route('/logs_media')
def logs_media_route():
    return log_media()

@app.route('/students/<exam>')
def students(exam):
    students = get_students(exam)
    return jsonify(students)

@app.route('/media/<exam>/<student>/<path:filename>')
def media_files_routes(exam, student, filename):
    return media_files(exam, student, filename)


@app.route('/media/<exam>/<student>')
def media(exam, student):
    media_files = get_student_media(exam, student)
    return jsonify(media_files)

@app.route('/show_grades', methods=['POST', 'GET'])
def show_grades_route():
    return show_grades()
    
@app.route('/show_logs', methods=['POST', 'GET'])
def show_logs_route():
    return show_logs()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


