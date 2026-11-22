"""
Teacher Screen for PRESENS AI
Features:
1. Teacher Authentication (Login with bcrypt & Registration)
2. 4-Tab Instructor Workspace:
   - Tab 1: Take Attendance (Live camera / Multi-photo classroom gallery, Face & Voice batch analysis)
   - Tab 2: Manage Subjects (Course creation, QR Code sharing via Segno)
   - Tab 3: Attendance Records (Session breakdown & CSV export)
   - Tab 4: Register Student (Direct student enrollment)
"""

import streamlit as st
import pandas as pd
from PIL import Image

from src.services import db_service, ai_service
from src.utils import qr_utils
from src.components.camera_selector import render_camera_selector

LOGO_URL = "https://i.ibb.co/YTYGn5qV/logo.png"


def apply_teacher_styles():
    """Apply styling for the teacher portal"""
    st.markdown("""
    <style>
        .stApp {
            background-color: #f8fafc;
            color: #1e1b4b;
            font-family: 'Outfit', sans-serif;
        }

        .tab-btn {
            background: white;
            border: 1px solid #e2e8f0;
            padding: 10px 18px;
            border-radius: 10px;
            font-weight: 600;
        }
    </style>
    """, unsafe_allow_html=True)


def show_teacher_screen():
    """Main teacher screen controller"""
    apply_teacher_styles()

    if "teacher_auth_mode" not in st.session_state:
        st.session_state["teacher_auth_mode"] = "login"

    # Top Navigation Bar
    col_nav1, col_nav2 = st.columns([3, 1])
    with col_nav1:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px;">
            <img src="{LOGO_URL}" style="width: 42px; height: 42px; border-radius: 10px;">
            <span style="font-size: 22px; font-weight: 700; color: #1e1b4b;">PRESENS AI</span>
            <span style="background: #fef3c7; color: #b45309; padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: 600;">Teacher Portal</span>
        </div>
        """, unsafe_allow_html=True)
    with col_nav2:
        if st.session_state.get("current_teacher"):
            if st.button("Logout", key="btn_teacher_logout"):
                st.session_state["current_teacher"] = None
                st.session_state["teacher_auth_mode"] = "login"
                st.rerun()
        else:
            if st.button("⬅️ Back to Home", key="btn_teacher_back_home"):
                st.session_state["login_type"] = None
                st.rerun()

    # Route based on login state
    current_teacher = st.session_state.get("current_teacher")

    if current_teacher:
        show_teacher_dashboard(current_teacher)
    else:
        if st.session_state["teacher_auth_mode"] == "login":
            show_teacher_login()
        else:
            show_teacher_register()


def show_teacher_login():
    """Teacher Login with username and hashed password"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("Login using password")
        with st.form("form_teacher_login"):
            username = st.text_input("Enter username", placeholder="ananyaroy")
            password = st.text_input("Enter password", type="password")
            st.markdown("---")
            submit = st.form_submit_button("Login", type="primary", use_container_width=True)

            if submit:
                if not username or not password:
                    st.warning("Please fill in both username and password.")
                else:
                    ok, res = db_service.authenticate_teacher(username, password)
                    if ok:
                        st.session_state["current_teacher"] = res
                        st.toast(f"Welcome back, {res['name']}!")
                        st.rerun()
                    else:
                        st.error(res)

        if st.button("Register Instead", use_container_width=True):
            st.session_state["teacher_auth_mode"] = "register"
            st.rerun()


def show_teacher_register():
    """Teacher registration form"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("Register your teacher profile")
        with st.form("form_teacher_reg"):
            username = st.text_input("Enter username", placeholder="ananyaroy")
            name = st.text_input("Enter name", placeholder="Ananya Roy")
            password = st.text_input("Enter password", type="password")
            confirm_pwd = st.text_input("Confirm your password", type="password")
            st.markdown("---")
            submit = st.form_submit_button("Register now", type="primary", use_container_width=True)

            if submit:
                if not username or not name or not password:
                    st.warning("Please complete all required fields.")
                elif password != confirm_pwd:
                    st.error("Passwords do not match.")
                else:
                    ok, res = db_service.register_teacher(username, password, name)
                    if ok:
                        st.session_state["current_teacher"] = res
                        st.success("Registration successful!")
                        st.rerun()
                    else:
                        st.error(res)

        if st.button("Login Instead", use_container_width=True):
            st.session_state["teacher_auth_mode"] = "login"
            st.rerun()


def show_teacher_dashboard(teacher):
    """Teacher 4-Tab Workspace"""
    st.markdown(f"""
    <div style="background: white; border-radius: 14px; padding: 20px 24px; margin-bottom: 25px; box-shadow: 0 2px 10px rgba(0,0,0,0.03);">
        <div style="font-size: 22px; font-weight: 700; color: #1e1b4b;">Welcome, {teacher['name']} 👋</div>
        <div style="color: #64748b; font-size: 14px; margin-top: 4px;">Instructor Dashboard &bull; Username: @{teacher['username']}</div>
    </div>
    """, unsafe_allow_html=True)

    tab_attendance, tab_subjects, tab_records, tab_register_student = st.tabs([
        "📸 Take Attendance",
        "📚 Manage Subjects",
        "📊 Attendance Records",
        "👤 Register Student"
    ])

    with tab_attendance:
        teacher_tab_take_attendance(teacher)

    with tab_subjects:
        teacher_tab_manage_subjects(teacher)

    with tab_records:
        teacher_tab_attendance_records(teacher)

    with tab_register_student:
        teacher_tab_register_student(teacher)


# ================= TAB 1: TAKE ATTENDANCE =================

def teacher_tab_take_attendance(teacher):
    """Classroom batch photo attendance with face & voice analysis"""
    subjects = db_service.get_teacher_subjects(teacher["id"])

    if not subjects:
        st.warning("Please create at least one subject in the **'Manage Subjects'** tab before taking attendance.")
        return

    subject_options = {f"{s['name']} ({s['subject_code']} - Sec {s['section']})": s["id"] for s in subjects}
    selected_label = st.selectbox("Select Subject", list(subject_options.keys()))
    selected_subject_id = subject_options[selected_label]

    enrolled_students = db_service.get_students_for_subject(selected_subject_id)
    st.caption(f"Currently enrolled students in this course: **{len(enrolled_students)}**")

    if "classroom_photos" not in st.session_state:
        st.session_state["classroom_photos"] = []

    # Camera Source Preference Option
    st.markdown("##### ⚙️ Camera Source Preference:")
    teacher_cam_mode = st.radio(
        "Choose camera / upload mode:",
        [
            "🎯 Camera Selector (Choose System Camera / Iriun)",
            "📷 Standard Streamlit Camera",
            "📁 Upload Classroom Photos"
        ],
        horizontal=True,
        label_visibility="collapsed",
        key="teacher_cam_mode_pref"
    )

    col_cam_box, col_cam_info = st.columns([1.3, 1])

    with col_cam_box:
        if teacher_cam_mode == "🎯 Camera Selector (Choose System Camera / Iriun)":
            st.caption("Select your preferred camera from the dropdown below to capture classroom snapshot:")
            custom_pic = render_camera_selector(key="teacher_attendance_custom_cam")
            if custom_pic is not None:
                img_obj = Image.open(custom_pic)
                pic_bytes = custom_pic.getvalue()
                if "last_teacher_pic_hash" not in st.session_state or st.session_state["last_teacher_pic_hash"] != pic_bytes:
                    st.session_state["last_teacher_pic_hash"] = pic_bytes
                    st.session_state["classroom_photos"].append(img_obj)
                    st.toast("📸 Photo added to session gallery!")
                    st.rerun()

        elif teacher_cam_mode == "📷 Standard Streamlit Camera":
            cam_pic = st.camera_input("Snapshot classroom from webcam", key="teacher_std_cam")
            if cam_pic:
                img_obj = Image.open(cam_pic)
                pic_bytes = cam_pic.getvalue()
                if "last_teacher_std_hash" not in st.session_state or st.session_state["last_teacher_std_hash"] != pic_bytes:
                    st.session_state["last_teacher_std_hash"] = pic_bytes
                    st.session_state["classroom_photos"].append(img_obj)
                    st.toast("📸 Photo added to session gallery!")

        else:
            uploaded_pics = st.file_uploader(
                "Upload classroom photos (JPG/PNG)",
                type=["jpg", "jpeg", "png"],
                accept_multiple_files=True,
                key="teacher_upload_cam"
            )
            if uploaded_pics:
                for up in uploaded_pics:
                    st.session_state["classroom_photos"].append(Image.open(up))
                st.toast(f"📁 {len(uploaded_pics)} photos added to gallery!")

    with col_cam_info:
        st.markdown(f"""
        <div style="background: white; border-radius: 12px; padding: 16px; border: 1px solid #e2e8f0; box-shadow: 0 2px 8px rgba(0,0,0,0.03);">
            <div style="font-weight: 700; color: #1e1b4b; margin-bottom: 8px;">📊 Session Photo Gallery</div>
            <div style="font-size: 14px; color: #64748b;">Current Photos: <b>{len(st.session_state['classroom_photos'])}</b></div>
            <div style="font-size: 13px; color: #64748b; margin-top: 6px;">
                💡 Take or upload multiple angle photos of your classroom. PRESENS AI will analyze all photos simultaneously.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Display Photo Gallery
    photos = st.session_state.get("classroom_photos", [])
    if photos:
        st.markdown(f"#### Classroom Photos ({len(photos)})")
        gallery_cols = st.columns(min(len(photos), 4))
        for idx, p in enumerate(photos):
            gallery_cols[idx % 4].image(p, caption=f"Photo #{idx + 1}", use_container_width=True)

        # Action Buttons
        st.markdown("---")
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("🗑️ Clear all photos"):
                st.session_state["classroom_photos"] = []
                st.rerun()

        with btn_col2:
            if st.button("🔍 Run Face Analysis", type="primary", use_container_width=True):
                with st.spinner("Analyzing classroom photos for enrolled student faces..."):
                    detected_ids = set()
                    for img in photos:
                        faces = ai_service.extract_all_faces_from_photo(img)
                        for f in faces:
                            match = ai_service.train_and_match_face(f["embedding"], enrolled_students, threshold=0.6)
                            if match:
                                detected_ids.add(match["id"])

                    # Build attendance status list
                    attendance_result = []
                    for st_item in enrolled_students:
                        is_present = st_item["id"] in detected_ids
                        attendance_result.append({
                            "student_id": st_item["id"],
                            "name": st_item["name"],
                            "status": "✅ Present" if is_present else "❌ Absent",
                            "is_present": is_present
                        })

                    st.session_state["pending_attendance"] = {
                        "subject_id": selected_subject_id,
                        "records": attendance_result
                    }

    # Render Attendance Result Dialog / Confirmation
    if "pending_attendance" in st.session_state and st.session_state["pending_attendance"].get("records"):
        pending = st.session_state["pending_attendance"]
        st.markdown("### 📋 Attendance Results Review")
        
        df_result = pd.DataFrame([
            {"Student Name": r["name"], "Status": r["status"]}
            for r in pending["records"]
        ])
        st.dataframe(df_result, use_container_width=True)

        conf_col1, conf_col2 = st.columns(2)
        with conf_col1:
            if st.button("Discard Results"):
                del st.session_state["pending_attendance"]
                st.rerun()
        with conf_col2:
            if st.button("💾 Confirm & Save Attendance", type="primary", use_container_width=True):
                db_service.log_batch_attendance(
                    subject_id=pending["subject_id"],
                    attendance_records=pending["records"],
                    method="face_analysis"
                )
                st.success("Attendance saved successfully!")
                del st.session_state["pending_attendance"]
                st.session_state["classroom_photos"] = []
                st.balloons()
                st.rerun()


# ================= TAB 2: MANAGE SUBJECTS =================

def teacher_tab_manage_subjects(teacher):
    """Subject creation and QR code sharing"""
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.subheader("Manage Subjects")
    with col_h2:
        with st.popover("➕ Create New Subject", use_container_width=True):
            st.markdown("### Create Subject")
            code_input = st.text_input("Subject Code", placeholder="e.g. CS101")
            name_input = st.text_input("Subject Name", placeholder="Introduction to Computer Science")
            sec_input = st.text_input("Section", placeholder="e.g. A")
            if st.button("Create Subject Now", type="primary", use_container_width=True):
                if code_input and name_input and sec_input:
                    ok, msg = db_service.create_subject(code_input, name_input, sec_input, teacher["id"])
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                else:
                    st.warning("Please fill in all fields.")

    subjects = db_service.get_teacher_subjects(teacher["id"])
    if not subjects:
        st.info("No subjects created yet. Click **'Create New Subject'** above to get started.")
        return

    # List of Subject Cards
    for s in subjects:
        with st.container():
            st.markdown(f"""
            <div style="background: white; border-radius: 12px; padding: 20px; margin-bottom: 16px; border-left: 8px solid #EB459E; box-shadow: 0 2px 10px rgba(0,0,0,0.04);">
                <h3 style="margin: 0; color: #1e1b4b; font-size: 20px; font-weight: 700;">{s['name']}</h3>
                <div style="display: flex; gap: 8px; margin: 8px 0 12px;">
                    <span style="background: #e0e7ff; color: #4338ca; padding: 2px 10px; border-radius: 6px; font-size: 12px; font-weight: 600;">Code: {s['subject_code']}</span>
                    <span style="background: #f1f5f9; color: #475569; padding: 2px 10px; border-radius: 6px; font-size: 12px; font-weight: 600;">Sec {s['section']}</span>
                </div>
                <div style="display: flex; gap: 15px; font-size: 13px; font-weight: 600; color: #64748b;">
                    <span>🫂 {s['student_count']} Enrolled Students</span>
                    <span>⏰ {s['class_count']} Classes Conducted</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.popover(f"🔗 Share Join Code: {s['subject_code']}"):
                st.markdown(f"### Enroll in {s['name']}")
                st.code(s['subject_code'], language="text")
                st.caption(f"Direct Join Link: `/?join-code={s['subject_code']}`")

                # Generate QR Code
                qr_bytes = qr_utils.generate_qr_code_image(f"/?join-code={s['subject_code']}")
                st.image(qr_bytes, caption=f"Scan to join {s['subject_code']}", width=220)


# ================= TAB 3: ATTENDANCE RECORDS =================

def teacher_tab_attendance_records(teacher):
    """View session attendance records and CSV export"""
    st.subheader("Attendance Records")

    records = db_service.get_teacher_attendance_records(teacher["id"])

    if not records:
        st.info("No attendance sessions recorded yet.")
        return

    df = pd.DataFrame(records)
    df.rename(columns={
        "session_time": "Session Time",
        "subject_name": "Subject Name",
        "subject_code": "Course Code",
        "total_students": "Total Enrolled",
        "present_count": "Present Count"
    }, inplace=True)

    df["Attendance Stats"] = df.apply(lambda r: f"✅ {r['Present Count']} / {r['Total Enrolled']} Students", axis=1)

    # Download CSV
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Export Attendance Records (CSV)",
        data=csv_bytes,
        file_name="presens_attendance_records.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.dataframe(df[["Session Time", "Subject Name", "Course Code", "Attendance Stats"]], use_container_width=True)


# ================= TAB 4: REGISTER STUDENT =================

def teacher_tab_register_student(teacher):
    """Instructor quick student enrollment"""
    st.subheader("Enroll Student Profile")
    st.caption("Quickly register a student into your course registry.")

    subjects = db_service.get_teacher_subjects(teacher["id"])
    if not subjects:
        st.warning("Please create a subject first before enrolling students.")
        return

    with st.form("form_quick_student_reg"):
        s_name = st.text_input("Student Full Name", placeholder="e.g. John Doe")
        s_email = st.text_input("Student Email / Roll ID", placeholder="student@college.edu")
        subject_opts = {f"{s['name']} ({s['subject_code']})": s["id"] for s in subjects}
        sel_subj = st.selectbox("Select Subject to Enroll", list(subject_opts.keys()))

        submit = st.form_submit_button("Register & Enroll Student", type="primary", use_container_width=True)

        if submit:
            if s_name:
                subj_id = subject_opts[sel_subj]
                # Register student
                s_data = db_service.register_student(name=s_name, email=s_email)
                # Enroll in subject
                db_service.enroll_student_in_subject(s_data["id"], sel_subj.split("(")[1].split(")")[0])
                st.success(f"Student {s_name} registered and enrolled in course!")
            else:
                st.warning("Please provide student's full name.")
