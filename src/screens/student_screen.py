"""
Student Screen for PRESENS AI
Handles:
1. Biometric Login via FaceID with explicit Camera Device Selection (System Camera vs Iriun)
2. New Student Registration (Face snapshot / photo + optional Voice enrollment)
3. Student Dashboard (enrolled subjects grid, attendance statistics, enroll dialog)
"""

import streamlit as st
from PIL import Image

from src.services import db_service, ai_service
from src.components import subject_card
from src.components.camera_selector import render_camera_selector

LOGO_URL = "https://i.ibb.co/YTYGn5qV/logo.png"


def apply_student_styles():
    """Apply styling for student portal"""
    st.markdown("""
    <style>
        .stApp {
            background-color: #f8fafc;
            color: #1e1b4b;
            font-family: 'Outfit', sans-serif;
        }

        .student-nav {
            background: white;
            padding: 16px 28px;
            border-radius: 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 12px rgba(0,0,0,0.04);
            margin-bottom: 25px;
        }

        .dashboard-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }

        .camera-choice-banner {
            background: #f1f5f9;
            border-radius: 12px;
            padding: 12px 16px;
            margin-bottom: 15px;
            border: 1px solid #e2e8f0;
        }
    </style>
    """, unsafe_allow_html=True)


def show_student_screen():
    """Main student screen entrypoint"""
    apply_student_styles()

    if "student_mode" not in st.session_state:
        st.session_state["student_mode"] = "login"

    # Top Navigation Bar
    col_nav1, col_nav2 = st.columns([3, 1])
    with col_nav1:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px;">
            <img src="{LOGO_URL}" style="width: 42px; height: 42px; border-radius: 10px;">
            <span style="font-size: 22px; font-weight: 700; color: #1e1b4b;">PRESENS AI</span>
            <span style="background: #e0e7ff; color: #4338ca; padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: 600;">Student Portal</span>
        </div>
        """, unsafe_allow_html=True)
    with col_nav2:
        if st.session_state.get("current_student"):
            if st.button("Logout", key="btn_student_logout"):
                st.session_state["current_student"] = None
                st.session_state["student_mode"] = "login"
                st.rerun()
        else:
            if st.button("⬅️ Back to Home", key="btn_student_back_home"):
                st.session_state["login_type"] = None
                st.rerun()

    # Route based on login state
    current_student = st.session_state.get("current_student")

    if current_student:
        show_student_dashboard(current_student)
    else:
        if st.session_state["student_mode"] == "login":
            show_face_login()
        else:
            show_student_registration()


def show_face_login():
    """Login using FaceID with Camera Device Preference selection"""
    col_head1, col_head2 = st.columns([2, 1])
    with col_head1:
        st.subheader("Login using FaceID")
        st.caption("Verify your identity with your chosen camera to access your dashboard.")
    with col_head2:
        if st.button("Register New Student", key="btn_to_reg"):
            st.session_state["student_mode"] = "register"
            st.rerun()

    # Separate Option to Select Preferred Camera Mode
    st.markdown("##### ⚙️ Camera Source Preference:")
    camera_mode = st.radio(
        "Choose your camera option:",
        [
            "🎯 Camera Selector (Choose System Camera / Iriun)",
            "📷 Standard Streamlit Camera",
            "📁 Upload Face Photo"
        ],
        horizontal=True,
        label_visibility="collapsed",
        key="student_cam_mode_pref"
    )

    col_cam, col_info = st.columns([1.3, 1])

    photo = None
    with col_cam:
        if camera_mode == "🎯 Camera Selector (Choose System Camera / Iriun)":
            st.caption("Select your System Camera from the dropdown below to bypass Iriun Webcam:")
            custom_shot = render_camera_selector(key="student_login_custom_cam")
            if custom_shot is not None:
                photo = custom_shot
        elif camera_mode == "📷 Standard Streamlit Camera":
            cam_shot = st.camera_input("Look at the camera and take a photo", key="student_login_std_cam")
            if cam_shot is not None:
                photo = cam_shot
        else:
            uploaded_shot = st.file_uploader("Upload clear face portrait (JPG/PNG)", type=["jpg", "jpeg", "png"], key="student_login_upload")
            if uploaded_shot is not None:
                photo = uploaded_shot

    with col_info:
        st.info("💡 Once your face is captured in the frame, PRESENS AI extracts your 128-dimensional facial embedding and matches it against your student record.")
        
        # Manual ID login fallback
        with st.expander("Or Login with Student ID"):
            sid_input = st.number_input("Enter Student ID Number", min_value=1, step=1, value=1)
            if st.button("Login with ID"):
                s = db_service.get_student_by_id(int(sid_input))
                if s:
                    st.session_state["current_student"] = s
                    st.toast(f"Welcome back, {s['name']}!")
                    st.rerun()
                else:
                    st.error("Student ID not found.")

    if photo is not None:
        with st.spinner("Analyzing facial biometric landmarks..."):
            query_emb = ai_service.extract_face_embedding(photo)
            if query_emb is None:
                st.warning("No face detected in the image. Please ensure your face is well-lit and centered.")
            else:
                students = db_service.get_all_students_with_embeddings()
                match = ai_service.train_and_match_face(query_emb, students, threshold=0.6)
                if match:
                    st.session_state["current_student"] = match
                    st.toast(f"Welcome Back {match['name']}! (Match: {match.get('confidence', 95)}%)")
                    st.success(f"Identity Verified: {match['name']}")
                    st.rerun()
                else:
                    st.error("Face not recognized in the student registry. Please register your profile or try again.")


def show_student_registration():
    """Register new student with face snapshot/upload and optional voice enrollment"""
    col_head1, col_head2 = st.columns([2, 1])
    with col_head1:
        st.subheader("New Student Registration")
    with col_head2:
        if st.button("⬅️ Back to Face Login", key="btn_to_login"):
            st.session_state["student_mode"] = "login"
            st.rerun()

    st.markdown("##### ⚙️ Camera Source Preference:")
    reg_camera_mode = st.radio(
        "Choose your registration camera option:",
        [
            "🎯 Camera Selector (Choose System Camera / Iriun)",
            "📷 Standard Streamlit Camera",
            "📁 Upload Portrait Photo"
        ],
        horizontal=True,
        label_visibility="collapsed",
        key="student_reg_mode_pref"
    )

    col1, col2 = st.columns([1.3, 1])

    photo = None
    with col1:
        if reg_camera_mode == "🎯 Camera Selector (Choose System Camera / Iriun)":
            st.caption("Select your System Camera from the dropdown below:")
            custom_shot = render_camera_selector(key="student_reg_custom_cam")
            if custom_shot is not None:
                photo = custom_shot
        elif reg_camera_mode == "📷 Standard Streamlit Camera":
            cam_shot = st.camera_input("Capture your Face for Profile Registration", key="student_reg_std_cam")
            if cam_shot is not None:
                photo = cam_shot
        else:
            uploaded_shot = st.file_uploader("Upload portrait photo (JPG/PNG)", type=["jpg", "jpeg", "png"], key="student_reg_upload")
            if uploaded_shot is not None:
                photo = uploaded_shot

    with col2:
        full_name = st.text_input("Enter your full name", placeholder="E.g. Likhith Gowda")
        email = st.text_input("Enter your email address", placeholder="student@university.edu")

        st.markdown("#### Optional : Voice Enrollment")
        st.caption("Record a short phrase like: *'I am present.'*")
        
        audio = None
        if hasattr(st, "audio_input"):
            audio = st.audio_input("Record classroom voice signature")
        else:
            audio = st.file_uploader("Upload short voice clip (WAV/MP3)", type=["wav", "mp3"])

        if st.button("Complete Registration", type="primary", use_container_width=True):
            if not full_name:
                st.warning("Please enter your full name.")
            elif photo is None:
                st.warning("Please capture a photo or upload a portrait.")
            else:
                with st.spinner("Encoding facial and vocal biometric vectors..."):
                    face_emb = ai_service.extract_face_embedding(photo)
                    voice_emb = ai_service.extract_voice_embedding(audio) if audio else None

                    student_data = db_service.register_student(
                        name=full_name,
                        email=email,
                        face_embedding=face_emb,
                        voice_embedding=voice_emb
                    )

                    st.session_state["current_student"] = student_data
                    st.session_state["student_mode"] = "dashboard"
                    st.success("Registration completed successfully!")
                    st.rerun()


def show_student_dashboard(student):
    """Student Dashboard showing enrolled subjects and attendance stats"""
    st.markdown(f"""
    <div style="background: white; border-radius: 14px; padding: 20px 24px; margin-bottom: 25px; box-shadow: 0 2px 10px rgba(0,0,0,0.03);">
        <div style="font-size: 22px; font-weight: 700; color: #1e1b4b;">Welcome, {student['name']} 👋</div>
        <div style="color: #64748b; font-size: 14px; margin-top: 4px;">Student ID: #{student['id']} &bull; Status: Active</div>
    </div>
    """, unsafe_allow_html=True)

    # Header with Enroll button
    col_d1, col_d2 = st.columns([3, 1])
    with col_d1:
        st.subheader("Your Enrolled Subjects")
    with col_d2:
        with st.popover("➕ Enroll in Subject", use_container_width=True):
            st.markdown("### Enroll in Course")
            st.caption("Enter the subject code provided by your teacher to enroll")
            subj_code = st.text_input("Subject Code", placeholder="Eg. CS101", key="enroll_code_input")
            if st.button("Enroll now", type="primary", use_container_width=True):
                if subj_code:
                    ok, msg = db_service.enroll_student_in_subject(student["id"], subj_code)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                else:
                    st.warning("Please enter a subject code.")

    # List Enrolled Subjects
    enrolled = db_service.get_student_enrolled_subjects(student["id"])

    if not enrolled:
        st.info("You are not enrolled in any subjects yet. Click **'Enroll in Subject'** above to join a course with your teacher's subject code.")
        return

    # Callback for unenroll
    def handle_unenroll(subject_id):
        db_service.unenroll_student(student["id"], subject_id)
        st.toast("Unenrolled from course.")
        st.rerun()

    # 2-column grid of subject cards
    col_sub1, col_sub2 = st.columns(2)
    for i, s in enumerate(enrolled):
        target_col = col_sub1 if i % 2 == 0 else col_sub2
        with target_col:
            subject_card.render_subject_card(s, on_unenroll_callback=handle_unenroll)
