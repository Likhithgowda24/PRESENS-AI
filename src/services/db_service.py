"""
Database Service for PRESENS AI
Supports local SQLite database (default, zero configuration needed)
and Supabase PostgreSQL (when SUPABASE_URL and SUPABASE_KEY are set).
"""

import os
import json
import sqlite3
import hashlib
from datetime import datetime

try:
    import bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "database", "presens.db")

# Optional Supabase client
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase_client = None

if SUPABASE_URL and SUPABASE_KEY:
    try:
        from supabase import create_client
        supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Supabase init error: {e}")


def get_connection():
    """Get SQLite database connection"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables according to PRESENS AI schema"""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Teachers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 2. Students table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT,
        face_embedding TEXT,
        voice_embedding TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 3. Subjects table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        section TEXT NOT NULL,
        teacher_id INTEGER,
        FOREIGN KEY (teacher_id) REFERENCES teachers(id)
    )
    """)

    # 4. Subject Students (Enrollments)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subject_students (
        student_id INTEGER,
        subject_id INTEGER,
        PRIMARY KEY (student_id, subject_id),
        FOREIGN KEY (student_id) REFERENCES students(id),
        FOREIGN KEY (subject_id) REFERENCES subjects(id)
    )
    """)

    # 5. Attendance Logs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject_id INTEGER,
        timestamp TEXT NOT NULL,
        is_present BOOLEAN NOT NULL,
        method TEXT DEFAULT 'face_recognition',
        FOREIGN KEY (student_id) REFERENCES students(id),
        FOREIGN KEY (subject_id) REFERENCES subjects(id)
    )
    """)

    conn.commit()
    conn.close()


# Ensure tables are created on module import
init_db()


# ================= TEACHER OPERATIONS =================

def hash_password(password: str) -> str:
    """Hash password using bcrypt or SHA-256 with salt fallback"""
    if BCRYPT_AVAILABLE:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
    else:
        salt = "presens_ai_salt_"
        return "sha256:" + hashlib.sha256((salt + password).encode("utf-8")).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    if hashed.startswith("sha256:"):
        salt = "presens_ai_salt_"
        expected = "sha256:" + hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
        return hashed == expected
    elif BCRYPT_AVAILABLE:
        try:
            return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
        except Exception:
            return False
    return False


def register_teacher(username, password, name):
    """Register a new teacher"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        hashed = hash_password(password)
        cursor.execute(
            "INSERT INTO teachers (username, password, name) VALUES (?, ?, ?)",
            (username, hashed, name)
        )
        conn.commit()
        teacher_id = cursor.lastrowid
        return True, {"id": teacher_id, "username": username, "name": name}
    except sqlite3.IntegrityError:
        return False, "Username already exists."
    finally:
        conn.close()


def authenticate_teacher(username, password):
    """Authenticate teacher with username and password"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teachers WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return False, "Teacher account not found."

    if not verify_password(password, row["password"]):
        return False, "Invalid password."

    return True, {"id": row["id"], "username": row["username"], "name": row["name"]}


# ================= STUDENT OPERATIONS =================

def register_student(name, email=None, face_embedding=None, voice_embedding=None):
    """Register student with name and optional face/voice embeddings"""
    conn = get_connection()
    cursor = conn.cursor()
    
    face_json = json.dumps(face_embedding.tolist() if hasattr(face_embedding, 'tolist') else face_embedding) if face_embedding is not None else None
    voice_json = json.dumps(voice_embedding.tolist() if hasattr(voice_embedding, 'tolist') else voice_embedding) if voice_embedding is not None else None

    cursor.execute(
        "INSERT INTO students (name, email, face_embedding, voice_embedding) VALUES (?, ?, ?, ?)",
        (name, email, face_json, voice_json)
    )
    conn.commit()
    student_id = cursor.lastrowid
    conn.close()
    return {"id": student_id, "name": name, "email": email}


def get_all_students_with_embeddings():
    """Retrieve all students with their face/voice embeddings for training the classifier"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, face_embedding, voice_embedding FROM students")
    rows = cursor.fetchall()
    conn.close()

    students = []
    for r in rows:
        face_emb = json.loads(r["face_embedding"]) if r["face_embedding"] else None
        voice_emb = json.loads(r["voice_embedding"]) if r["voice_embedding"] else None
        students.append({
            "id": r["id"],
            "name": r["name"],
            "email": r["email"],
            "face_embedding": face_emb,
            "voice_embedding": voice_emb
        })
    return students


def get_student_by_id(student_id):
    """Get single student details"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM students WHERE id = ?", (student_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row["id"], "name": row["name"], "email": row["email"]}
    return None


# ================= SUBJECT & ENROLLMENT OPERATIONS =================

def create_subject(subject_code, name, section, teacher_id):
    """Create a new subject / course"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO subjects (subject_code, name, section, teacher_id) VALUES (?, ?, ?, ?)",
            (subject_code.upper().strip(), name.strip(), section.strip(), teacher_id)
        )
        conn.commit()
        return True, "Subject created successfully!"
    except sqlite3.IntegrityError:
        return False, f"Subject with code '{subject_code}' already exists."
    finally:
        conn.close()


def get_teacher_subjects(teacher_id):
    """Get list of subjects created by a teacher with student and class count stats"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT s.id, s.subject_code, s.name, s.section,
           COUNT(DISTINCT ss.student_id) as student_count,
           COUNT(DISTINCT al.timestamp) as class_count
    FROM subjects s
    LEFT JOIN subject_students ss ON s.id = ss.subject_id
    LEFT JOIN attendance_logs al ON s.id = al.subject_id
    WHERE s.teacher_id = ?
    GROUP BY s.id
    """, (teacher_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_student_enrolled_subjects(student_id):
    """Get subjects enrolled by a student along with attendance stats"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT s.id, s.subject_code, s.name, s.section,
           (SELECT COUNT(DISTINCT timestamp) FROM attendance_logs WHERE subject_id = s.id) as total_sessions,
           (SELECT COUNT(*) FROM attendance_logs WHERE subject_id = s.id AND student_id = ? AND is_present = 1) as attended_sessions
    FROM subjects s
    JOIN subject_students ss ON s.id = ss.subject_id
    WHERE ss.student_id = ?
    """, (student_id, student_id))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def enroll_student_in_subject(student_id, subject_code):
    """Enroll student into a subject via subject code"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name FROM subjects WHERE UPPER(subject_code) = ?", (subject_code.upper().strip(),))
    subject = cursor.fetchone()
    
    if not subject:
        conn.close()
        return False, f"Subject code '{subject_code}' not found."

    subject_id = subject["id"]
    try:
        cursor.execute(
            "INSERT INTO subject_students (student_id, subject_id) VALUES (?, ?)",
            (student_id, subject_id)
        )
        conn.commit()
        return True, f"Enrolled successfully in {subject['name']}!"
    except sqlite3.IntegrityError:
        return False, "You are already enrolled in this subject."
    finally:
        conn.close()


def unenroll_student(student_id, subject_id):
    """Unenroll a student from a course"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM subject_students WHERE student_id = ? AND subject_id = ?",
        (student_id, subject_id)
    )
    conn.commit()
    conn.close()
    return True


def get_students_for_subject(subject_id):
    """Get list of students enrolled in a subject"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT st.id, st.name, st.email, st.face_embedding, st.voice_embedding
    FROM students st
    JOIN subject_students ss ON st.id = ss.student_id
    WHERE ss.subject_id = ?
    """, (subject_id,))
    rows = cursor.fetchall()
    conn.close()
    
    res = []
    for r in rows:
        face_emb = json.loads(r["face_embedding"]) if r["face_embedding"] else None
        voice_emb = json.loads(r["voice_embedding"]) if r["voice_embedding"] else None
        res.append({
            "id": r["id"],
            "name": r["name"],
            "email": r["email"],
            "face_embedding": face_emb,
            "voice_embedding": voice_emb
        })
    return res


# ================= ATTENDANCE OPERATIONS =================

def log_attendance(student_id, subject_id, timestamp, is_present, method="face_recognition"):
    """Record single attendance entry"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO attendance_logs (student_id, subject_id, timestamp, is_present, method)
    VALUES (?, ?, ?, ?, ?)
    """, (student_id, subject_id, timestamp, 1 if is_present else 0, method))
    conn.commit()
    conn.close()


def log_batch_attendance(subject_id, attendance_records, method="face_analysis"):
    """
    Log attendance for a list of students for a session
    attendance_records: list of dicts [{'student_id': 1, 'is_present': True}, ...]
    """
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %I:%M %p")

    for rec in attendance_records:
        cursor.execute("""
        INSERT INTO attendance_logs (student_id, subject_id, timestamp, is_present, method)
        VALUES (?, ?, ?, ?, ?)
        """, (rec["student_id"], subject_id, now_str, 1 if rec["is_present"] else 0, method))

    conn.commit()
    conn.close()
    return now_str


def get_teacher_attendance_records(teacher_id):
    """Get attendance logs grouped by session for all subjects of a teacher"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT al.timestamp as session_time,
           s.name as subject_name,
           s.subject_code,
           COUNT(*) as total_students,
           SUM(CASE WHEN al.is_present = 1 THEN 1 ELSE 0 END) as present_count
    FROM attendance_logs al
    JOIN subjects s ON al.subject_id = s.id
    WHERE s.teacher_id = ?
    GROUP BY al.timestamp, s.id
    ORDER BY al.timestamp DESC
    """, (teacher_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]
