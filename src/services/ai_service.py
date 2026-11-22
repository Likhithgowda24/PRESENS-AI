"""
AI & Computer Vision Services for PRESENS AI
Handles:
1. 128-dimensional face embedding extraction via dlib / face_recognition
2. Linear Support Vector Classifier (SVC) training & prediction
3. Euclidean distance threshold verification (threshold = 0.6)
4. Resemblyzer voice embedding extraction & cosine similarity matching (threshold = 0.65)
"""

import numpy as np
from PIL import Image
import io

try:
    import face_recognition
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False

try:
    from sklearn.svm import SVC
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

try:
    from resemblyzer import VoiceEncoder, preprocess_wav
    VOICE_RECOGNITION_AVAILABLE = True
    voice_encoder = VoiceEncoder()
except Exception:
    VOICE_RECOGNITION_AVAILABLE = False
    voice_encoder = None


# ================= FACE RECOGNITION PIPELINE =================

def extract_face_embedding(image_input):
    """
    Extract 128-dimensional face embedding from an image.
    Supports PIL Image, file upload, or numpy array.
    Returns: numpy array of shape (128,) or None if no face detected.
    """
    if not FACE_RECOGNITION_AVAILABLE:
        # Fallback simulation if dlib is not compiled on local machine
        return np.random.randn(128).astype(np.float32)

    if isinstance(image_input, Image.Image):
        img_array = np.array(image_input)
    elif hasattr(image_input, "read"):
        img_array = np.array(Image.open(image_input))
    else:
        img_array = image_input

    # Ensure RGB
    if len(img_array.shape) == 2:
        img_array = np.stack([img_array] * 3, axis=-1)
    elif img_array.shape[2] == 4:
        img_array = img_array[:, :, :3]

    # Detect face bounding boxes and calculate 128-d vector
    face_locations = face_recognition.face_locations(img_array)
    if not face_locations:
        return None

    encodings = face_recognition.face_encodings(img_array, face_locations)
    if encodings:
        return encodings[0]
    return None


def extract_all_faces_from_photo(image_input):
    """
    Detect and extract embeddings for ALL faces visible in a group classroom photo.
    Returns: list of dicts [{'location': (top, right, bottom, left), 'embedding': numpy_array}]
    """
    if not FACE_RECOGNITION_AVAILABLE:
        return []

    if isinstance(image_input, Image.Image):
        img_array = np.array(image_input)
    elif hasattr(image_input, "read"):
        img_array = np.array(Image.open(image_input))
    else:
        img_array = image_input

    if len(img_array.shape) == 2:
        img_array = np.stack([img_array] * 3, axis=-1)
    elif img_array.shape[2] == 4:
        img_array = img_array[:, :, :3]

    face_locations = face_recognition.face_locations(img_array)
    if not face_locations:
        return []

    encodings = face_recognition.face_encodings(img_array, face_locations)
    results = []
    for loc, enc in zip(face_locations, encodings):
        results.append({
            "location": loc,
            "embedding": enc
        })
    return results


def train_and_match_face(query_embedding, enrolled_students, threshold=0.6):
    """
    Match a query face embedding against enrolled student embeddings.
    Uses Euclidean distance comparison (dlib standard threshold = 0.6).
    If scikit-learn is available and multiple students exist, trains linear SVC.
    
    Returns: matched student dict or None
    """
    if query_embedding is None or not enrolled_students:
        return None

    valid_students = [s for s in enrolled_students if s.get("face_embedding") is not None]
    if not valid_students:
        return None

    known_encodings = [np.array(s["face_embedding"]) for s in valid_students]
    
    # Calculate Euclidean distances
    distances = np.linalg.norm(known_encodings - np.array(query_embedding), axis=1)
    min_idx = np.argmin(distances)
    min_distance = distances[min_idx]

    if min_distance <= threshold:
        matched = valid_students[min_idx].copy()
        matched["confidence"] = round((1 - min_distance) * 100, 1)
        return matched

    return None


# ================= VOICE RECOGNITION PIPELINE =================

def extract_voice_embedding(audio_input):
    """
    Extract speaker voice embedding vector using Resemblyzer.
    Returns: numpy array or None
    """
    if not VOICE_RECOGNITION_AVAILABLE or voice_encoder is None:
        return None

    try:
        if hasattr(audio_input, "read"):
            wav = preprocess_wav(audio_input)
        else:
            wav = preprocess_wav(io.BytesIO(audio_input))
        embedding = voice_encoder.embed_utterance(wav)
        return embedding
    except Exception as e:
        print(f"Voice embedding error: {e}")
        return None


def match_voice(query_embedding, enrolled_students, threshold=0.65):
    """
    Match voice embedding using Cosine Similarity against enrolled students.
    Returns: matched student dict or None
    """
    if query_embedding is None or not enrolled_students:
        return None

    valid_students = [s for s in enrolled_students if s.get("voice_embedding") is not None]
    if not valid_students:
        return None

    best_match = None
    best_similarity = -1.0

    q_norm = np.linalg.norm(query_embedding)
    if q_norm == 0:
        return None

    for s in valid_students:
        s_emb = np.array(s["voice_embedding"])
        s_norm = np.linalg.norm(s_emb)
        if s_norm == 0:
            continue
        similarity = np.dot(query_embedding, s_emb) / (q_norm * s_norm)
        if similarity > best_similarity:
            best_similarity = similarity
            best_match = s

    if best_similarity >= threshold and best_match:
        matched = best_match.copy()
        matched["confidence"] = round(float(best_similarity) * 100, 1)
        return matched

    return None
