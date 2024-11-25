# SneakPeek  

**SneakPeek** is an advanced exam monitoring and management platform designed to enhance the security and efficiency of online exams. It integrates AI-powered features to detect cheating, manage exams, and streamline the proctoring process. The platform supports various functionalities like facial detection, voice analysis, and window/tab activity monitoring, ensuring a fair exam environment.

## Features  

- **Student Registration with Image Verification**:  
  Users can register with image verification to ensure identity during login.  

- **Proctor Registration**:  
  Simple and efficient registration for proctors without image verification.  

- **AI-Powered Monitoring**:  
  Detects:  
  - Multiple faces in a video feed  
  - Eye movements and lip reading  
  - Use of unauthorized devices or apps  
  - Copy-paste actions or switching to unauthorized tabs  

- **Question Management**:  
  - Upload files in multiple formats (PDF, Word, Excel) to generate questions.  
  - Supports automatic grading for objective-type questions.  

- **Video Storage for Review**:  
  Saves video recordings during exams for proctors to review suspicious behavior.  

## Tech Stack  

- **Frontend**:  
  - HTML, CSS, JavaScript  

- **Backend**:  
  - Python, Flask  

- **AI and Machine Learning**:  
  - TensorFlow, PyTorch, OpenCV, ,mediaPipe 
  - YOLO for object detection
  - Pyaudio
  - Face_Recognition


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
 
