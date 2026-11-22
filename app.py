"""
PRESENS AI - Making Attendance faster using AI
Created by Likhith Gowda M A
Main Application Entry Point

Features:
- State-driven routing via st.session_state['login_type']
- Query parameter support (/?join-code=<subject_code>)
- Modern glassmorphic theme with Google Fonts ('Outfit' & 'Climate Crisis')
- FaceID biometric login and Support Vector Classifier (SVC) attendance scanning
"""

import streamlit as st

# Configure page metadata
st.set_page_config(
    page_title="PRESENS AI - Making Attendance faster using AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Global CSS to completely remove Streamlit logo, GitHub repository links, toolbars, and branding
st.markdown("""
<style>
    /* Hide Streamlit Header, Main Menu, Footers, and Toolbars */
    #MainMenu {visibility: hidden !important; display: none !important;}
    header {visibility: hidden !important; display: none !important;}
    footer {visibility: hidden !important; display: none !important;}
    [data-testid="stHeader"] {visibility: hidden !important; display: none !important;}
    [data-testid="stToolbar"] {visibility: hidden !important; display: none !important;}
    [data-testid="stDecoration"] {visibility: hidden !important; display: none !important;}
    [data-testid="stStatusWidget"] {visibility: hidden !important; display: none !important;}
    [data-testid="stDeployButton"] {visibility: hidden !important; display: none !important;}
    .stDeployButton {visibility: hidden !important; display: none !important;}
    #manage-app-button {visibility: hidden !important; display: none !important;}
    [data-testid="stAppViewContainer"] > header {visibility: hidden !important; display: none !important;}
    [data-testid="stBottom"] {visibility: hidden !important; display: none !important;}
    
    /* Remove Streamlit viewer badges and watermarks */
    .viewerBadge_container__1QSob,
    .viewerBadge_link__1QSob,
    [class*="viewerBadge"] {
        visibility: hidden !important;
        display: none !important;
    }

    /* Remove GitHub repository icons and links */
    a[href*="github.com"] {
        display: none !important;
    }
    
    /* Remove Streamlit cloud links */
    a[href*="streamlit.io"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

from src.screens.home_screen import show_home_screen
from src.screens.student_screen import show_student_screen
from src.screens.teacher_screen import show_teacher_screen


def main():
    # Handle query parameters (e.g. /?join-code=CS101)
    query_params = st.query_params
    if "join-code" in query_params:
        join_code = query_params["join-code"]
        st.session_state["join_code"] = join_code
        if "login_type" not in st.session_state or st.session_state["login_type"] is None:
            st.session_state["login_type"] = "student"

    # Initialize session navigation state
    if "login_type" not in st.session_state:
        st.session_state["login_type"] = None

    # Route based on login_type
    login_type = st.session_state.get("login_type")

    if login_type == "student":
        show_student_screen()
    elif login_type == "teacher":
        show_teacher_screen()
    else:
        show_home_screen()


if __name__ == "__main__":
    main()
