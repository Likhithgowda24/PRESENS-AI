"""
Seed initial demo data for PRESENS AI
Seeds:
1. Demo Teacher (ananyaroy / password123)
2. Demo Subjects (CS101, CS202)
3. Demo Students (Likhith Gowda M A, Ada Lovelace)
4. Subject enrollments and historical attendance logs
"""

import sys
import os

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.services import db_service
import numpy as np

def run_seed():
    print("🌱 Seeding PRESENS AI database...")

    # 1. Register Teacher
    ok, teacher = db_service.register_teacher("ananyaroy", "password123", "Prof. Ananya Roy")
    if not ok:
        # Retrieve if already exists
        conn = db_service.get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM teachers WHERE username = 'ananyaroy'")
        teacher = dict(c.fetchone())
        conn.close()
    print(f"Teacher: {teacher['name']} (Username: ananyaroy | Password: password123)")

    # 2. Create Subjects
    db_service.create_subject("CS101", "Introduction to Computer Science", "A", teacher["id"])
    db_service.create_subject("CS202", "Artificial Intelligence & ML", "B", teacher["id"])
    print("Subjects: CS101 & CS202 created.")

    # 3. Register Students
    dummy_face_1 = np.random.randn(128).astype(np.float32)
    dummy_face_2 = np.random.randn(128).astype(np.float32)

    s1 = db_service.register_student("Likhith Gowda M A", "likhith@university.edu", dummy_face_1)
    s2 = db_service.register_student("Ada Lovelace", "ada@university.edu", dummy_face_2)
    print(f"Students: {s1['name']} (ID: {s1['id']}), {s2['name']} (ID: {s2['id']})")

    # 4. Enroll Students
    db_service.enroll_student_in_subject(s1["id"], "CS101")
    db_service.enroll_student_in_subject(s1["id"], "CS202")
    db_service.enroll_student_in_subject(s2["id"], "CS101")
    print("Enrollments linked.")

    # 5. Log Sample Attendance
    subjects = db_service.get_teacher_subjects(teacher["id"])
    if subjects:
        db_service.log_attendance(s1["id"], subjects[0]["id"], "2026-11-20 09:30 AM", True)
        db_service.log_attendance(s2["id"], subjects[0]["id"], "2026-11-20 09:30 AM", True)
        db_service.log_attendance(s1["id"], subjects[0]["id"], "2026-11-21 09:30 AM", True)
        db_service.log_attendance(s2["id"], subjects[0]["id"], "2026-11-21 09:30 AM", False)

    print("✅ Demo dataset initialized successfully!")

if __name__ == "__main__":
    run_seed()
