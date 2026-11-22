"""
Database utilities for PRESENS AI
Handles attendance records storage and retrieval using CSV/JSON files
"""

import os
import json
import csv
from datetime import datetime, date
import pandas as pd

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database")
ATTENDANCE_FILE = os.path.join(DB_DIR, "attendance.csv")
USERS_FILE = os.path.join(DB_DIR, "users.json")
CLASSES_FILE = os.path.join(DB_DIR, "classes.json")


def ensure_dirs():
    """Ensure database directory exists"""
    os.makedirs(DB_DIR, exist_ok=True)


def init_attendance_file():
    """Initialize attendance CSV file if it doesn't exist"""
    ensure_dirs()
    if not os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "date", "time", "student_id", "student_name",
                "class_name", "subject", "status", "confidence", "method"
            ])


def mark_attendance(student_id, student_name, class_name="", subject="", 
                     confidence=0, method="face_recognition"):
    """
    Mark attendance for a student
    
    Args:
        student_id: Student ID
        student_name: Student name
        class_name: Class name
        subject: Subject name
        confidence: Recognition confidence percentage
        method: Method used (face_recognition, manual, etc.)
        
    Returns:
        tuple: (success: bool, message: str)
    """
    init_attendance_file()
    
    today = date.today().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M:%S")
    
    # Check if already marked today
    if is_already_marked(student_id, today, subject):
        return False, f"Attendance already marked for {student_name} today in {subject or 'this session'}."
    
    with open(ATTENDANCE_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            today, now, student_id, student_name,
            class_name, subject, "Present", confidence, method
        ])
    
    return True, f"✅ Attendance marked for {student_name} (ID: {student_id}) at {now}"


def is_already_marked(student_id, date_str, subject=""):
    """Check if attendance is already marked for today"""
    if not os.path.exists(ATTENDANCE_FILE):
        return False
    
    df = pd.read_csv(ATTENDANCE_FILE, dtype=str)
    
    if df.empty:
        return False
    
    mask = (df["student_id"] == str(student_id)) & (df["date"] == date_str)
    
    if subject:
        mask = mask & (df["subject"] == subject)
    
    return mask.any()


def get_attendance_records(date_str=None, class_name=None, student_id=None):
    """
    Get attendance records with optional filters
    
    Args:
        date_str: Filter by date (YYYY-MM-DD)
        class_name: Filter by class name
        student_id: Filter by student ID
        
    Returns:
        pandas DataFrame
    """
    init_attendance_file()
    
    df = pd.read_csv(ATTENDANCE_FILE, dtype=str)
    
    if df.empty:
        return df
    
    if date_str:
        df = df[df["date"] == date_str]
    
    if class_name:
        df = df[df["class_name"] == class_name]
    
    if student_id:
        df = df[df["student_id"] == str(student_id)]
    
    return df


def get_attendance_summary(date_str=None, class_name=None):
    """Get attendance summary statistics"""
    df = get_attendance_records(date_str=date_str, class_name=class_name)
    
    if df.empty:
        return {
            "total_records": 0,
            "unique_students": 0,
            "dates_covered": 0,
            "subjects": []
        }
    
    return {
        "total_records": len(df),
        "unique_students": df["student_id"].nunique(),
        "dates_covered": df["date"].nunique(),
        "subjects": df["subject"].unique().tolist() if "subject" in df.columns else []
    }


def get_student_attendance_report(student_id):
    """Get detailed attendance report for a specific student"""
    df = get_attendance_records(student_id=student_id)
    
    if df.empty:
        return None
    
    total_days = df["date"].nunique()
    
    return {
        "student_id": student_id,
        "student_name": df["student_name"].iloc[0] if not df.empty else "Unknown",
        "total_days_present": total_days,
        "records": df.to_dict("records"),
        "dates": df["date"].unique().tolist()
    }


# ---- User Management ----

def load_users():
    """Load users from JSON file"""
    ensure_dirs()
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {"students": {}, "teachers": {}}


def save_users(users):
    """Save users to JSON file"""
    ensure_dirs()
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def register_user(role, username, password, name, extra_info=None):
    """
    Register a new user
    
    Args:
        role: 'student' or 'teacher'
        username: Username/ID
        password: Password
        name: Full name
        extra_info: Dict with additional info (class, subject, etc.)
        
    Returns:
        tuple: (success: bool, message: str)
    """
    users = load_users()
    key = f"{role}s"
    
    if username in users.get(key, {}):
        return False, f"Username '{username}' already exists."
    
    users.setdefault(key, {})[username] = {
        "password": password,
        "name": name,
        "created_at": datetime.now().isoformat(),
        **(extra_info or {})
    }
    
    save_users(users)
    return True, f"Registration successful! Welcome, {name}."


def authenticate_user(role, username, password):
    """
    Authenticate a user
    
    Args:
        role: 'student' or 'teacher'
        username: Username/ID
        password: Password
        
    Returns:
        tuple: (success: bool, user_data or error message)
    """
    users = load_users()
    key = f"{role}s"
    
    user = users.get(key, {}).get(username)
    
    if user is None:
        return False, "User not found. Please register first."
    
    if user["password"] != password:
        return False, "Incorrect password."
    
    return True, user


# ---- Class Management ----

def load_classes():
    """Load classes from JSON file"""
    ensure_dirs()
    if os.path.exists(CLASSES_FILE):
        with open(CLASSES_FILE, "r") as f:
            return json.load(f)
    return {}


def save_classes(classes):
    """Save classes to JSON file"""
    ensure_dirs()
    with open(CLASSES_FILE, "w") as f:
        json.dump(classes, f, indent=2)


def create_class(class_name, teacher_name, subject, students=None):
    """Create a new class"""
    classes = load_classes()
    
    if class_name in classes:
        return False, f"Class '{class_name}' already exists."
    
    classes[class_name] = {
        "teacher": teacher_name,
        "subject": subject,
        "students": students or [],
        "created_at": datetime.now().isoformat()
    }
    
    save_classes(classes)
    return True, f"Class '{class_name}' created successfully."


def get_class_list():
    """Get all classes"""
    return load_classes()


def add_student_to_class(class_name, student_id, student_name):
    """Add a student to a class"""
    classes = load_classes()
    
    if class_name not in classes:
        return False, f"Class '{class_name}' not found."
    
    student_entry = {"id": student_id, "name": student_name}
    
    # Check if already in class
    for s in classes[class_name]["students"]:
        if s["id"] == student_id:
            return False, f"Student {student_name} is already in {class_name}."
    
    classes[class_name]["students"].append(student_entry)
    save_classes(classes)
    return True, f"Student {student_name} added to {class_name}."


def export_attendance_csv(date_str=None, class_name=None):
    """Export attendance data as CSV string"""
    df = get_attendance_records(date_str=date_str, class_name=class_name)
    return df.to_csv(index=False)
