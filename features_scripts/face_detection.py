import cv2
import winsound

# Load pre-trained face detector (Haar cascades)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def play_alert_sound():
    winsound.Beep(1000, 1000)  # 1000 Hz sound for 1000 ms

def detect_2faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Count the number of faces
    face_count = len(faces)

    # Check for more than one face
    if face_count > 1:
        print("ALERT: You cannot sign in with others present!")  # Output text
        play_alert_sound()  # Play audio alert for admin
        return True
    
