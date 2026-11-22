"""
Home Screen for PRESENS AI
Created by Likhith Gowda M A
Matches the landing page design with:
- Google Font 'Climate Crisis' and 'Outfit'
- PRESENS AI graduation logo
- Glassmorphic role selection cards
- Mascot illustrations from i.ibb.co
- Likhith Gowda M A creator footer
"""

import streamlit as st

LOGO_URL = "https://i.ibb.co/YTYGn5qV/logo.png"
STUDENT_MASCOT_URL = "https://i.ibb.co/844D9Lrt/mascot-student.png"
TEACHER_MASCOT_URL = "https://i.ibb.co/CsmQQV6X/mascot-prof.png"


def apply_home_styles():
    """Apply Google fonts and custom landing page theme"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis&family=Outfit:wght@300;400;500;600;700;800&display=swap');

        /* Clean full gradient */
        .stApp {
            background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
            font-family: 'Outfit', sans-serif;
            color: white;
        }

        #MainMenu, footer, header {
            visibility: hidden;
        }

        [data-testid="stSidebar"] {
            display: none;
        }

        .home-logo-box {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin-top: 30px;
            margin-bottom: 25px;
        }

        .home-logo-box img {
            width: 85px;
            height: 85px;
            border-radius: 18px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.25);
        }

        .home-title {
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            font-size: 24px;
            letter-spacing: 4px;
            color: #ffffff;
            margin-top: 16px;
            text-align: center;
            text-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }

        .home-subtitle {
            font-size: 15px;
            color: rgba(255, 255, 255, 0.85);
            text-align: center;
            margin-top: 4px;
            letter-spacing: 0.5px;
        }

        /* Glassmorphic Portal Cards */
        .portal-card {
            background: rgba(255, 255, 255, 0.12);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border: 1px solid rgba(255, 255, 255, 0.25);
            border-radius: 24px;
            padding: 35px 25px 25px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
            transition: all 0.3s ease;
        }

        .portal-card:hover {
            transform: translateY(-8px) scale(1.01);
            box-shadow: 0 20px 45px rgba(0,0,0,0.25);
            border-color: rgba(255, 255, 255, 0.45);
        }

        .portal-card h2 {
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            font-size: 28px;
            color: #ffffff;
            margin-bottom: 15px;
        }

        .portal-card img {
            width: 140px;
            height: 140px;
            object-fit: contain;
            margin: 10px auto 20px;
            filter: drop-shadow(0 6px 12px rgba(0,0,0,0.15));
        }

        /* Streamlit Button Styling */
        div[data-testid="stColumn"] button {
            background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 14px !important;
            padding: 14px 28px !important;
            font-weight: 600 !important;
            font-size: 16px !important;
            letter-spacing: 0.5px !important;
            box-shadow: 0 4px 14px rgba(79, 70, 229, 0.4) !important;
            transition: all 0.3s ease !important;
            width: 100% !important;
        }

        div[data-testid="stColumn"] button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 20px rgba(79, 70, 229, 0.6) !important;
            background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%) !important;
        }

        .home-footer {
            text-align: center;
            color: rgba(255, 255, 255, 0.75);
            font-size: 14px;
            margin-top: 60px;
            padding-bottom: 30px;
            letter-spacing: 0.5px;
        }
    </style>
    """, unsafe_allow_html=True)


def show_home_screen():
    """Render the PRESENS AI home screen"""
    apply_home_styles()

    # Top Brand Header
    st.markdown(f"""
    <div class="home-logo-box">
        <img src="{LOGO_URL}" alt="PRESENS AI Logo">
        <div class="home-title">PRESENS AI</div>
        <div class="home-subtitle">Making Attendance faster using AI</div>
    </div>
    """, unsafe_allow_html=True)

    # 2-Column Portal Selector Cards
    col_left, col_center, col_right = st.columns([1, 2.4, 1])

    with col_center:
        card1, card2 = st.columns(2)

        with card1:
            st.markdown(f"""
            <div class="portal-card">
                <h2>I'm Student</h2>
                <img src="{STUDENT_MASCOT_URL}" alt="Student Mascot">
            </div>
            """, unsafe_allow_html=True)
            if st.button("Student Portal", key="btn_student_portal", use_container_width=True):
                st.session_state["login_type"] = "student"
                st.rerun()

        with card2:
            st.markdown(f"""
            <div class="portal-card">
                <h2>I'm Teacher</h2>
                <img src="{TEACHER_MASCOT_URL}" alt="Teacher Mascot">
            </div>
            """, unsafe_allow_html=True)
            if st.button("Teacher Portal", key="btn_teacher_portal", use_container_width=True):
                st.session_state["login_type"] = "teacher"
                st.rerun()

    # Footer
    st.markdown("""
    <div class="home-footer">
        Created with ❤️ by Likhith Gowda M A
    </div>
    """, unsafe_allow_html=True)
