# SneakPeek  

**SneakPeek** is an advanced exam monitoring and management platform designed to enhance the security and efficiency of online exams. It integrates AI-powered features to detect cheating, manage exams, and streamline the proctoring process. The platform supports various functionalities like facial detection, voice analysis, and window/tab activity monitoring, ensuring a fair exam environment.

## Features  
- **AI-Powered Monitoring**:  
  Detects:  
  - Multiple faces in a video feed  
  - Eye movements and lip reading  
  - Use of unauthorized devices or apps  
  - Copy-paste actions or switching to unauthorized tabs  

- **Student Registration with Image Verification**:  
  Users can register with image verification to ensure identity during login.  

- **Proctor Registration**:  
  Simple and efficient registration for proctors without image verification.  

- **Question Management**:  
  - Upload files in multiple formats (PDF, Word, Excel) to generate questions.  
  - Supports automatic grading for objective-type questions.  

- **Video Storage for Review**:  
  Saves video recordings during exams for proctors to review suspicious behavior.

  # Face and Activity Detection Scripts

## 1. `detect_and_verify_face.py`
### Features:
- **Face Verification:**
  - Uses `face_recognition` to compare a face captured from a webcam image with a stored device image.
  - Encodes faces from both images and verifies if they match.
### Output:
- Returns `True` if the faces match, otherwise `False`.
### Error Handling:
- Includes exception handling to log errors during processing.

---

## 2. `eye_detection.py`
### Features:
- **Eye Gaze Detection:**
  - Utilizes `mediapipe` to track eye landmarks and detect whether the user is looking away from the screen.
- **Cheating Detection:**
  - Flags if a user looks away from the screen for more than 2 seconds.
  - Plays an alert sound using `winsound`.
- **Custom Threshold:**
  - Allows customizable detection sensitivity by adjusting the distance threshold.

---

## 3. `face_detection.py`
### Features:
- **Multi-Face Detection:**
  - Detects faces in real-time using OpenCV's Haar cascade classifier.
- **Prohibited Multi-User Detection:**
  - Alerts (via sound and message) when more than one face is detected, ensuring a single-user presence.
- **User Notification:**
  - Outputs an alert message: `ALERT: You cannot sign in with others present!`

---

## 4. `mouth_open_detection.py`
### Features:
- **Mouth State Detection:**
  - Uses `mediapipe` to measure the distance between the upper and lower lips to detect if the mouth is open.
- **Speaking Detection:**
  - Detects if the mouth remains open for more than 2 seconds, indicating potential speaking activity.
- **Alert Mechanism:**
  - Plays an alert sound using `winsound` when speaking is detected.
- **Custom Threshold:**
  - The lip distance threshold is adjustable for calibration.

---

## 5. `yolo_object_detection.py`
### Features:
- **Real-Time Object Detection:**
  - Utilizes a `YOLOv5` model (pre-trained on the COCO dataset) to detect objects in real-time.
- **Custom Object Alert:**
  - Flags specific "weird" objects (e.g., cell phone, laptop, book) with an alert if detected.
- **Confidence Output:**
  - Prints the detected object's name and confidence score.
- **Alert Mechanism:**
  - Plays an alert sound using `winsound` upon detecting a prohibited object.

---

## 6. `voice_detection.py`
### Features:
- **Voice Activity Detection:**
  - Uses `PyAudio` to process real-time audio streams and detect voice activity.
- **Energy-Based Detection:**
  - Calculates the average energy of audio input and compares it against a user-defined threshold.
- **Custom Threshold:**
  - The sensitivity of voice detection can be adjusted by modifying the `THRESHOLD` parameter.
- **Real-Time Monitoring:**
  - Continuously monitors the microphone input for voice activity and prints `Voice Detected!` when triggered.


## Tech Stack  

- **AI and Machine Learning**:  
  - TensorFlow, PyTorch, OpenCV, ,mediaPipe 
  - YOLO for object detection
  - Pyaudio
  - Face_Recognition
    
- **Frontend**:  
  - HTML, CSS, JavaScript  

- **Backend**:  
  - Python, Flask  


## Directory Structure  

```
SneakPeek/
├── app/
│   ├── static/              
│   │   ├── css/              # CSS files  
│   │   ├── js/               # JavaScript files  
│   │   ├── images/           # Image assets  
│   │   ├── fonts/            # Font files  
│   ├── utilities_functions/            # Helper scripts for backend logic 
│   ├── templates/            # HTML templates
│   ├── features_scripts/     # AI/ML models for detection  
│   ├── data/                 # Uploaded files and datasets  
│   ├── app.py                # Main Flask app entry point  
├── README.md                 # Project documentation  
```

## Installation  

1. Clone the repository:  
   ```bash
   git clone https://github.com/mohamedelsayed10/sneak-peek.git
   cd sneak-peek
   ```

2. Create and activate a virtual environment:  
   ```bash
   python -m venv env  
   source env/bin/activate   # For Linux/Mac  
   env\Scripts\activate      # For Windows  
   ```

3. Install dependencies:  
   ```bash
   pip install -r requirements.txt  
   ```

4. Run the app:  
   ```bash
   python app.py  
   ```

5. Access the platform at `http://127.0.0.1:5000`.  

## Usage  

1. Register as a **student** or **proctor**.  
2. Upload exam files.  
3. Start the exam while SneakPeek monitors activities in real-time.  
4. Review exam logs and video footage to ensure fair conduct.  
 
