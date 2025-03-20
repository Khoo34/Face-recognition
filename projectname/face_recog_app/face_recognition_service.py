import cv2
import numpy as np
import face_recognition
from face_recog_app.models import Employee

# Load known faces ONCE when the script runs
known_encodings = []
known_names = []

def load_known_faces():
    global known_encodings, known_names  

    employees = Employee.objects.all()
    for emp in employees:
        img_path = emp.photo.path
        image = face_recognition.load_image_file(img_path)
        encoding = face_recognition.face_encodings(image)
        
        if encoding:  
            known_encodings.append(encoding[0])
            known_names.append(emp.name)

# Call this function ONCE at startup to preload known faces
load_known_faces()

def recognize_face(frame):
    if not known_encodings:  
        return frame, "No known faces loaded"

    # Convert BGR (OpenCV) to RGB (face_recognition uses RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect face locations and encodings in the input frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    name = "Unknown"

    for encoding, location in zip(face_encodings, face_locations):
        # Compare with known faces
        matches = face_recognition.compare_faces(known_encodings, encoding)
        face_distances = face_recognition.face_distance(known_encodings, encoding)  

        if True in matches:
            best_match_index = np.argmin(face_distances)  
            name = known_names[best_match_index]

        # Draw a rectangle around the face
        top, right, bottom, left = location
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    return frame, name
