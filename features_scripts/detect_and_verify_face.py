import face_recognition

def detect_and_verify(webcam_image, device_image):
    """
    Detects and verifies if the face in the webcam image matches the face in the device image.

    Args:
        webcam_image: An image from the webcam.
        device_image: An image from the device.

    Returns:
        bool: True if the faces match, False otherwise.
    """
    try:
        # Encode faces from both images
        webcam_face_encodings = face_recognition.face_encodings(webcam_image)
        device_face_encodings = face_recognition.face_encodings(device_image)

        # Check if any faces were found in both images
        if not webcam_face_encodings or not device_face_encodings:
            return False

        # Compare the first face found in each image
        results = face_recognition.compare_faces([webcam_face_encodings[0]], device_face_encodings[0])
        return results[0]

    except Exception as e:
        # Log the exception for debugging purposes (consider using logging instead of print in production)
        print(f"An error occurred: {e}")
        return False
