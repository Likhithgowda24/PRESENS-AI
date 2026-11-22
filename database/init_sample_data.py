"""
Sample Data Initializer for PRESENS AI
Seeds dummy classes, demo student, and demo teacher accounts for quick testing.
"""

import sys
import os

# Add parent directory to path so imports work cleanly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db_utils
from datetime import date, timedelta


def seed_demo_data():
    print("🌱 Seeding PRESENS AI demo data...")

    # 1. Register Demo Teacher
    ok, msg = db_utils.register_user(
        role="teacher",
        username="teacher_demo",
        password="password123",
        name="Prof. Alan Turing",
        extra_info={"department": "Computer Science & Engineering", "subject": "Artificial Intelligence"}
    )
    print(f"Teacher account: {msg}")

    # 2. Register Demo Student
    ok, msg = db_utils.register_user(
        role="student",
        username="CS2024001",
        password="password123",
        name="Ada Lovelace",
        extra_info={"class_name": "CSE-A", "email": "ada@example.com"}
    )
    print(f"Student account: {msg}")

    # 3. Create Demo Classes
    db_utils.create_class("CSE-A", "Prof. Alan Turing", "Artificial Intelligence")
    db_utils.create_class("CSE-B", "Prof. Alan Turing", "Data Structures")
    print("Demo classes created.")

    # 4. Mark Sample Attendance
    today = date.today()
    yesterday = (today - timedelta(days=1)).strftime("%Y-%m-%d")
    two_days_ago = (today - timedelta(days=2)).strftime("%Y-%m-%d")

    db_utils.init_attendance_file()
    
    # Insert some sample historical attendance
    import csv
    with open(db_utils.ATTENDANCE_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([yesterday, "09:30:15", "CS2024001", "Ada Lovelace", "CSE-A", "Artificial Intelligence", "Present", 95.4, "face_recognition"])
        writer.writerow([two_days_ago, "09:28:40", "CS2024001", "Ada Lovelace", "CSE-A", "Data Structures", "Present", 92.1, "face_recognition"])

    print("✅ Sample historical attendance logs initialized!")
    print("\nDefault Credentials:")
    print(" - Student: ID: CS2024001 | Password: password123")
    print(" - Teacher: ID: teacher_demo | Password: password123")


if __name__ == "__main__":
    seed_demo_data()
