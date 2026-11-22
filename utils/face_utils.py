"""
Face Recognition Utilities for PRESENS AI
Handles face detection, encoding, and recognition using face_recognition library
"""

import os
import pickle
import numpy as np
from PIL import Image

try:
    import face_recognition
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False


REGISTERED_FACES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "registered_faces")
ENCODINGS_FILE = os.path.join(REGISTERED_FACES_DIR, "encodings.pkl")


def ensure_dirs():
    """Ensure required directories exist"""
    os.makedirs(REGISTERED_FACES_DIR, exist_ok=True)


def load_encodings():
    """Load saved face encodings from disk"""
    if os.path.exists(ENCODINGS_FILE):
        with open(ENCODINGS_FILE, "rb") as f:
            return pickle.load(f)
    return {"names": [], "encodings": []}


def save_encodings(data):
    """Save face encodings to disk"""
    ensure_dirs()
    with open(ENCODINGS_FILE, "wb") as f:
        pickle.dump(data, f)


def register_face(name, student_id, image):
    """
    Register a new face for attendance
    
    Args:
        name: Student's name
        student_id: Student's ID/Roll number
        image: PIL Image or numpy array of the face
        
    Returns:
        tuple: (success: bool, message: str)
    """
    if not FACE_RECOGNITION_AVAILABLE:
        return False, "face_recognition library not installed. Please install it with: pip install face-recognition"
    
    ensure_dirs()
    
    # Convert PIL Image to numpy array if needed
    if isinstance(image, Image.Image):
        img_array = np.array(image)
    else:
        img_array = image
    
    # Convert BGR to RGB if needed (OpenCV format)
    if len(img_array.shape) == 3 and img_array.shape[2] == 3:
        if CV2_AVAILABLE:
            img_rgb = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB) if img_array.dtype == np.uint8 else img_array
        else:
            img_rgb = img_array
    else:
        img_rgb = img_array
    
    # Detect faces
    face_locations = face_recognition.face_locations(img_rgb)
    
    if len(face_locations) == 0:
        return False, "No face detected in the image. Please upload a clear photo with your face visible."
    
    if len(face_locations) > 1:
        return False, "Multiple faces detected. Please upload a photo with only your face."
    
    # Get face encoding
    face_encodings = face_recognition.face_encodings(img_rgb, face_locations)
    
    if len(face_encodings) == 0:
        return False, "Could not encode the face. Please try with a different photo."
    
    # Save the image
    identifier = f"{student_id}_{name.replace(' ', '_')}"
    img_path = os.path.join(REGISTERED_FACES_DIR, f"{identifier}.jpg")
    
    pil_img = Image.fromarray(img_rgb)
    pil_img.save(img_path)
    
    # Save encoding
    data = load_encodings()
    
    # Check if student already registered
    if identifier in data.get("identifiers", []):
        idx = data["identifiers"].index(identifier)
        data["encodings"][idx] = face_encodings[0]
        data["names"][idx] = name
        msg = f"Face updated for {name} (ID: {student_id})"
    else:
        data.setdefault("identifiers", []).append(identifier)
        data["names"].append(name)
        data["encodings"].append(face_encodings[0])
        data.setdefault("student_ids", []).append(student_id)
        msg = f"Face registered successfully for {name} (ID: {student_id})"
    
    save_encodings(data)
    return True, msg


def recognize_faces(image, tolerance=0.5):
    """
    Recognize faces in an image against registered faces
    
    Args:
        image: PIL Image or numpy array
        tolerance: How much distance between faces to consider a match (lower = more strict)
        
    Returns:
        list of dicts with recognized face info
    """
    if not FACE_RECOGNITION_AVAILABLE:
        return []
    
    data = load_encodings()
    
    if not data.get("encodings"):
        return []
    
    # Convert to numpy array
    if isinstance(image, Image.Image):
        img_array = np.array(image)
    else:
        img_array = image
    
    # Detect faces
    face_locations = face_recognition.face_locations(img_array)
    face_encodings = face_recognition.face_encodings(img_array, face_locations)
    
    results = []
    known_encodings = data["encodings"]
    known_names = data["names"]
    known_ids = data.get("student_ids", ["N/A"] * len(known_names))
    
    for face_encoding, face_location in zip(face_encodings, face_locations):
        # Compare against all known faces
        matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=tolerance)
        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        
        name = "Unknown"
        student_id = "N/A"
        confidence = 0
        
        if True in matches:
            best_match_idx = np.argmin(face_distances)
            if matches[best_match_idx]:
                name = known_names[best_match_idx]
                student_id = known_ids[best_match_idx] if best_match_idx < len(known_ids) else "N/A"
                confidence = round((1 - face_distances[best_match_idx]) * 100, 2)
        
        results.append({
            "name": name,
            "student_id": student_id,
            "confidence": confidence,
            "location": face_location
        })
    
    return results


def draw_face_boxes(image, results):
    """
    Draw bounding boxes and labels on recognized faces
    
    Args:
        image: numpy array (RGB)
        results: list of recognition results
        
    Returns:
        numpy array with drawn boxes
    """
    if not CV2_AVAILABLE:
        return image
    
    img = image.copy()
    
    for result in results:
        top, right, bottom, left = result["location"]
        name = result["name"]
        confidence = result["confidence"]
        
        # Choose color based on recognition
        if name == "Unknown":
            color = (255, 0, 0)  # Red for unknown
        else:
            color = (0, 255, 0)  # Green for recognized
        
        # Draw rectangle
        cv2.rectangle(img, (left, top), (right, bottom), color, 2)
        
        # Draw label background
        label = f"{name} ({confidence}%)" if name != "Unknown" else "Unknown"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        thickness = 2
        
        (text_width, text_height), _ = cv2.getTextSize(label, font, font_scale, thickness)
        cv2.rectangle(img, (left, bottom), (left + text_width + 10, bottom + text_height + 15), color, -1)
        cv2.putText(img, label, (left + 5, bottom + text_height + 8), font, font_scale, (255, 255, 255), thickness)
    
    return img


def get_registered_students():
    """Get list of all registered students"""
    data = load_encodings()
    students = []
    names = data.get("names", [])
    ids = data.get("student_ids", [])
    
    for i, name in enumerate(names):
        student_id = ids[i] if i < len(ids) else "N/A"
        students.append({
            "name": name,
            "student_id": student_id
        })
    
    return students


def delete_student(student_id):
    """Remove a registered student"""
    data = load_encodings()
    identifiers = data.get("identifiers", [])
    
    idx_to_remove = None
    for i, identifier in enumerate(identifiers):
        if identifier.startswith(student_id):
            idx_to_remove = i
            break
    
    if idx_to_remove is not None:
        data["names"].pop(idx_to_remove)
        data["encodings"].pop(idx_to_remove)
        data["identifiers"].pop(idx_to_remove)
        if "student_ids" in data and idx_to_remove < len(data["student_ids"]):
            data["student_ids"].pop(idx_to_remove)
        
        # Remove image file
        for f in os.listdir(REGISTERED_FACES_DIR):
            if f.startswith(student_id) and f.endswith(('.jpg', '.png')):
                os.remove(os.path.join(REGISTERED_FACES_DIR, f))
        
        save_encodings(data)
        return True
    
    return False
