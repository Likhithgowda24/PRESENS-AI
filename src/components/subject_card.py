"""
Subject Card Component for PRESENS AI
Displays enrolled course details, attendance progress, and unenroll button.
"""

import streamlit as st

def render_subject_card(subject, on_unenroll_callback=None):
    """
    Render a subject card with custom styling:
    - 8px solid #EB459E left border
    - Subject name, code tag, section
    - Attendance statistics chips
    - Unenroll button
    """
    card_html = f"""
    <div style="
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 8px solid #EB459E;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        display: flex;
        flex-direction: column;
        gap: 12px;
    ">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <h3 style="margin: 0; color: #1e1b4b; font-size: 20px; font-weight: 700;">{subject['name']}</h3>
                <div style="display: flex; gap: 8px; margin-top: 6px;">
                    <span style="background: #e0e7ff; color: #4338ca; padding: 2px 10px; border-radius: 6px; font-size: 12px; font-weight: 600;">
                        {subject['subject_code']}
                    </span>
                    <span style="background: #f1f5f9; color: #475569; padding: 2px 10px; border-radius: 6px; font-size: 12px; font-weight: 600;">
                        Section {subject['section']}
                    </span>
                </div>
            </div>
        </div>
        <div style="display: flex; gap: 15px; margin-top: 8px;">
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 6px 14px; font-size: 13px; font-weight: 600; color: #334155;">
                📅 Total Sessions: <span style="color: #6366f1;">{subject.get('total_sessions', 0)}</span>
            </div>
            <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 6px 14px; font-size: 13px; font-weight: 600; color: #166534;">
                ✅ Attended: <span style="color: #15803d;">{subject.get('attended_sessions', 0)}</span>
            </div>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
    
    if on_unenroll_callback:
        col_space, col_btn = st.columns([3, 1])
        with col_btn:
            if st.button(f"Unenroll", key=f"unenroll_{subject['id']}", help="Unenroll from this course"):
                on_unenroll_callback(subject["id"])
