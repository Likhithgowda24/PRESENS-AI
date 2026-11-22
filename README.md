# PRESENS AI - Making Attendance Faster Using AI 🎓

Created by **Likhith Gowda M A**

PRESENS AI is an intelligent biometric attendance tracking system designed for educational institutions, combining **Facial Recognition (dlib & Linear SVC)**, **Speaker Voice Verification (Resemblyzer)**, and **Instant Course Sharing via QR Codes (Segno)**.

---

## 🌟 Key Capabilities

### 👨‍🎓 Student Portal
- **Biometric FaceID Login**: Snapshot face recognition directly via camera.
- **New Student Registration**: Face embedding extraction (128-dimensional vector via dlib/ResNet) and optional voice enrollment signature.
- **Course Enrollment**: Join courses using teacher-provided subject codes or scanning dynamic QR codes.
- **Personalized Attendance Dashboard**: Track total classes held vs. attended sessions with real-time percentages.

### 👨‍🏫 Teacher / Instructor Portal
- **Secure Instructor Auth**: Account creation and login with encrypted passwords (`bcrypt` / salted SHA-256).
- **Classroom Batch Scanner**: Add photos to a session gallery via live camera or multi-image upload; runs simultaneous face detection and recognition across all enrolled students in the frame.
- **Voice Attendance**: Record classroom audio to verify vocal signatures via Cosine Similarity (`resemblyzer`).
- **Subject Management**: Create courses, monitor enrolled student rosters, and generate scannable QR join codes.
- **Session Attendance Records**: View attendance history grouped by class sessions, track present vs. absent ratios, and export one-click CSV reports.

---

## 🛠️ Architecture & Tech Stack

```text
d:\My Twin\presens-ai\
├── .streamlit/
│   └── config.toml               # Custom theme & UI settings (Streamlit & Git branding removed)
├── app.py                        # State-driven entrypoint & query router (/?join-code=<code>)
├── requirements.txt              # Production Python package requirements
├── README.md                     # Documentation & setup guide
├── src/
│   ├── screens/
│   │   ├── home_screen.py        # Landing page with mascot cards & Google fonts
│   │   ├── student_screen.py     # Student FaceID login, registration & dashboard
│   │   └── teacher_screen.py     # Instructor 4-tab dashboard, photo gallery & scanner
│   ├── components/
│   │   └── subject_card.py       # Custom styled course cards with session counters
│   ├── services/
│   │   ├── ai_service.py         # 128-d face embedding, Linear SVC & Resemblyzer voice matching
│   │   ├── db_service.py         # SQLite / Supabase database abstraction layer
│   │   └── seed_demo_data.py     # Test dataset generator
│   └── utils/
│       └── qr_utils.py           # QR code generation with Segno
└── database/
    └── presens.db                # Auto-generated SQLite local database
```

---

## 🚀 Quick Start Guide

### 1. Open Terminal
```powershell
cd "d:\My Twin\presens-ai"
```

### 2. Set Up Virtual Environment (Recommended)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Seed Demo Data (Optional)
```powershell
python src/services/seed_demo_data.py
```

### 5. Run the Application
```powershell
streamlit run app.py
```

---

## 🔑 Pre-Seeded Demo Credentials

| Role | Username / ID | Password | Notes |
| :--- | :--- | :--- | :--- |
| **Teacher** | `ananyaroy` | `password123` | Has 2 pre-created courses: `CS101` and `CS202` |
| **Student 1** | ID: `1` (Likhith Gowda M A) | FaceID / ID Login | Enrolled in `CS101` and `CS202` |
| **Student 2** | ID: `2` (Ada Lovelace) | FaceID / ID Login | Enrolled in `CS101` |

---

## 👤 Author
- **Likhith Gowda M A**
