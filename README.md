
# SneakPeek  

**SneakPeek** is an advanced **exam monitoring and management platform** designed to enhance the security and efficiency of online exams. By integrating AI-powered features such as facial detection, voice analysis, and activity monitoring, it ensures a fair exam environment while streamlining the proctoring process.

---

## 🌟 Features  

- **AI-Powered Monitoring**  
  - **Face Detection**: Verifies a student's identity by comparing the captured webcam image with the stored one.  
  - **Eye Movement Detection**: Flags if the student looks away from the screen for too long, indicating potential cheating.  
  - **Prohibited Object Detection**: Uses YOLOv5 to detect suspicious objects (e.g., phones or laptops) in the exam environment.  
  - **Voice Detection**: Monitors for unauthorized verbal communication during exams.  
  - **Activity Monitoring**: Detects unauthorized actions like switching tabs or copy-paste actions.

- **Student Registration with Image Verification**  
  - Ensures secure and accurate identity verification during student login using facial recognition.

- **Proctor Registration**  
  - Easy and secure proctor registration without image verification.

- **Question Management**  
  - Supports file uploads in formats like PDF, Word, and Excel for automatic question generation.  
  - Automatically grades objective-type questions.

- **Video Storage for Review**  
  - Stores video footage of exams for review by proctors in case of suspicious behavior.

---

## 🧑‍💻 Feature Breakdown

### 1. `detect_and_verify_face.py`  
- **Face Verification**:  
  - Uses the `face_recognition` library to match the captured face with the registered face image.  
  - Returns `True` if faces match, otherwise `False`.

### 2. `eye_detection.py`  
- **Eye Gaze Detection**:  
  - Tracks eye movements using `mediapipe` to ensure the student is focused on the screen.  
  - Flags if the user looks away for more than 2 seconds and triggers an alert.

### 3. `face_detection.py`  
- **Multi-Face Detection**:  
  - Uses OpenCV’s Haar cascade classifier for detecting multiple faces in real-time.  
  - Alerts the system if more than one face is detected, ensuring a single-user environment.

### 4. `mouth_open_detection.py`  
- **Mouth State Detection**:  
  - Monitors the student’s mouth using `mediapipe` to check if the mouth is open, potentially indicating speaking.  
  - Alerts the system if the mouth remains open for more than 2 seconds.

### 5. `yolo_object_detection.py`  
- **Real-Time Object Detection**:  
  - Uses YOLOv5 to detect objects like phones or laptops during exams.  
  - Alerts the system if suspicious objects are detected, with the option for custom alerts.

### 6. `voice_detection.py`  
- **Voice Activity Detection**:  
  - Detects audio input from the student’s microphone to flag any voice activity.  
  - Alerts the system if it detects unauthorized voice input.

---

## 🔧 Tech Stack  

- **AI and Machine Learning**:  
  - TensorFlow, PyTorch, OpenCV, MediaPipe  
  - YOLOv5 for real-time object detection  
  - PyAudio for voice detection  
  - Face_Recognition for facial verification

- **Frontend**:  
  - HTML, CSS, JavaScript

- **Backend**:  
  - Python, Flask  

---

## 🗂️ Directory Structure  

```
SneakPeek/
├── app/
│   ├── static/              
│   │   ├── css/            # CSS files  
│   │   ├── js/             # JavaScript files  
│   │   ├── images/         # Image assets  
│   │   ├── fonts/          # Font files  
│   ├── utilities_functions/  # Backend helper scripts  
│   ├── templates/          # HTML templates  
│   ├── features_scripts/   # AI/ML models for detection  
│   ├── data/               # Uploaded files and datasets  
│   ├── app.py              # Main Flask app  
├── README.md               # Project documentation  
```

---

## 🚀 Installation  

1. **Clone the repository**:  
   ```bash
   git clone https://github.com/mohamedelsayed10/sneak-peek.git
   cd sneak-peek
   ```

2. **Create and activate a virtual environment**:  
   ```bash
   python -m venv env  
   source env/bin/activate   # For Linux/Mac  
   env\Scripts\activate      # For Windows  
   ```

3. **Install dependencies**:  
   ```bash
   pip install -r requirements.txt  
   ```

4. **Run the app**:  
   ```bash
   python app.py  
   ```

5. **Access the platform**:  
   Open your browser and visit `http://127.0.0.1:5000`.

---

## 📝 Usage  

1. **Register as a Student or Proctor**:  
   - Students need to register with image verification.  
   - Proctors can register without the image verification process.  

2. **Upload Exam Files**:  
   - Upload exam papers in formats like PDF, Word, or Excel for question generation.  

3. **Start the Exam**:  
   - The system will monitor students during the exam, tracking activities like face detection, eye movements, voice detection, and object presence.

4. **Review Logs and Videos**:  
   - Proctors can review recorded video footage and logs for any suspicious activity during the exam.

---

## 📧 Contact  

For more information or collaboration inquiries, reach out to:  
**[Mohamed Elsayed](https://www.linkedin.com/in/mohamed-elsayed-319a24204/)**
**[Manar Ramadan](https://www.linkedin.com/in/manar-ramadan-60a613216/)**


 

