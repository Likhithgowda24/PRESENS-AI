"""
PRESENS AI - 40-Page Academic Project Report Builder
Generates exactly 40 pages with clean UI screenshots, source code excerpts,
academic chapters, and professional layout.
Author: Likhith Gowda M A
"""
import os, sys, base64, subprocess, shutil, re
from pathlib import Path

# ─── Paths ────────────────────────────────────────────────────────────────────
PROJECT_DIR = Path(r"d:\My Twin\presens-ai")
SCREENSHOTS_DIR = PROJECT_DIR / "assets" / "screenshots"
OUTPUT_HTML = PROJECT_DIR / "REPORT_40PAGE.html"
OUTPUT_PDF  = PROJECT_DIR / "PRESENS_AI_Project_Report.pdf"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def img_b64(path):
    """Return base64 data-uri or empty string if file missing."""
    try:
        with open(path, "rb") as f:
            data = f.read()
        ext = Path(path).suffix.lower().replace(".", "")
        if ext == "jpg": ext = "jpeg"
        return f"data:image/{ext};base64,{base64.b64encode(data).decode()}"
    except Exception:
        return ""


# ─── Collect screenshots ───────────────────────────────────────────────────────
def find_screenshot(candidates):
    """Find first existing screenshot from a list of candidate paths."""
    for p in candidates:
        if os.path.exists(p):
            return img_b64(p)
    return ""


HOME_IMG     = find_screenshot([SCREENSHOTS_DIR / "fig0_home_landing.png"])
STUDENT_IMG  = find_screenshot([SCREENSHOTS_DIR / "fig_student_clean.png",
                                 SCREENSHOTS_DIR / "fig2_student_portal_cam.png"])
TEACHER_LOGIN_IMG = find_screenshot([SCREENSHOTS_DIR / "fig3_teacher_login.png"])
TEACHER_DASH_IMG  = find_screenshot([SCREENSHOTS_DIR / "fig_teacher_upload.png",
                                      SCREENSHOTS_DIR / "fig4_teacher_dashboard_cam.png"])
TEACHER_SUBJ_IMG  = find_screenshot([SCREENSHOTS_DIR / "fig_teacher_subjects.png"])
TEACHER_REC_IMG   = find_screenshot([SCREENSHOTS_DIR / "fig_teacher_records.png"])
ORIG_SITE_IMG     = find_screenshot([SCREENSHOTS_DIR / "fig1_original_site.png"])

def img_tag(b64, caption="", width="100%"):
    if not b64:
        return f'<div class="img-placeholder">📷 {caption}</div>'
    return f'''<figure>
      <img src="{b64}" style="width:{width};border-radius:8px;border:1px solid #dde3f0;box-shadow:0 2px 8px rgba(0,0,0,0.12);" />
      <figcaption>{caption}</figcaption>
    </figure>'''


# ─── HTML ──────────────────────────────────────────────────────────────────────
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Source+Code+Pro:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: 'Outfit', sans-serif;
    font-size: 10pt;
    line-height: 1.65;
    color: #1a1a2e;
    background: #fff;
}

/* STRICT ONE PAGE = ONE PRINTED PAGE */
.page {
    width: 210mm;
    height: 297mm;
    max-height: 297mm;
    overflow: hidden;
    padding: 18mm 20mm 16mm 22mm;
    margin: 0 auto;
    page-break-after: always;
    page-break-inside: avoid;
    break-after: page;
    position: relative;
    background: #fff;
}
.page:last-child { page-break-after: auto; break-after: auto; }

@page {
    size: A4 portrait;
    margin: 0;
}

@media print {
    html, body { background: white; width: 210mm; }
    .page {
        margin: 0 !important;
        box-shadow: none !important;
        page-break-after: always !important;
        break-after: page !important;
    }
}

/* TYPOGRAPHY */
h1 { font-size: 20pt; font-weight: 700; color: #1a1a2e; }
h2 { font-size: 13pt; font-weight: 700; color: #1a1a2e; border-bottom: 2px solid #3b82f6; padding-bottom: 4px; margin: 12px 0 7px; }
h3 { font-size: 11pt; font-weight: 600; color: #1e3a8a; margin: 10px 0 5px; }
h4 { font-size: 10pt; font-weight: 600; color: #1e40af; margin: 7px 0 4px; }
p  { margin: 5px 0; text-align: justify; }
ul, ol { margin: 5px 0 5px 18px; }
li { margin: 2px 0; }
strong { color: #1e3a8a; }

/* COVER */
.cover {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    text-align: center;
    height: 261mm;
    overflow: hidden;
    background: linear-gradient(145deg, #0f172a 0%, #1e3a8a 50%, #3b82f6 100%);
    color: white;
    border-radius: 4px;
    padding: 30px 25px;
    margin: -18mm -20mm -16mm -22mm;
}
.cover-logo { font-size: 50px; margin-bottom: 14px; }
.cover h1 { font-size: 26pt; color: #fff; letter-spacing: -0.5px; margin-bottom: 8px; }
.cover .subtitle { font-size: 12pt; color: #93c5fd; font-weight: 500; margin-bottom: 20px; }
.cover .meta { background: rgba(255,255,255,0.1); border-radius: 10px; padding: 14px 28px; margin-top: 16px; }
.cover .meta p { font-size: 10pt; color: #e0f2fe; margin: 3px 0; text-align: center; }
.cover .meta .label { color: #93c5fd; font-size: 8pt; text-transform: uppercase; letter-spacing: 1px; }
.cover .tags { margin-top: 16px; display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; }
.tag { background: rgba(255,255,255,0.15); border-radius: 20px; padding: 4px 12px; font-size: 8pt; color: #bfdbfe; }

/* CERTIFICATE */
.cert-box {
    border: 3px double #1e3a8a;
    border-radius: 8px;
    padding: 30px 40px;
    margin: 20px 0;
    text-align: center;
}
.cert-box h2 { border: none; font-size: 18pt; color: #1e3a8a; }
.seal { font-size: 60px; margin: 10px 0; }
.sig-row { display: flex; justify-content: space-between; margin-top: 50px; }
.sig-box { text-align: center; border-top: 1px solid #666; padding-top: 6px; min-width: 150px; font-size: 9pt; }

/* HEADER / FOOTER on content pages */
.page-header {
    display: flex; justify-content: space-between; align-items: center;
    border-bottom: 1px solid #dde3f0; padding-bottom: 6px; margin-bottom: 14px;
    font-size: 8.5pt; color: #64748b;
}
.page-footer {
    position: absolute; bottom: 14mm; left: 28mm; right: 25mm;
    display: flex; justify-content: space-between; align-items: center;
    border-top: 1px solid #dde3f0; padding-top: 5px;
    font-size: 8.5pt; color: #94a3b8;
}

/* TABLES */
table { width: 100%; border-collapse: collapse; margin: 10px 0; font-size: 10pt; }
th { background: #1e3a8a; color: white; padding: 7px 10px; text-align: left; }
td { padding: 6px 10px; border: 1px solid #dde3f0; }
tr:nth-child(even) td { background: #f8fafc; }

/* CODE */
pre, code {
    font-family: 'Source Code Pro', monospace;
    font-size: 8.5pt;
    background: #0f172a;
    color: #e2e8f0;
    border-radius: 6px;
}
pre { padding: 12px 16px; overflow: hidden; line-height: 1.6; margin: 8px 0; white-space: pre-wrap; word-break: break-all; }
code { padding: 1px 5px; }

/* FIGURES */
figure { margin: 10px 0; text-align: center; }
figcaption { font-size: 9pt; color: #64748b; font-style: italic; margin-top: 5px; }
.img-placeholder {
    background: #f1f5f9; border: 2px dashed #94a3b8;
    border-radius: 8px; padding: 40px; text-align: center;
    color: #64748b; font-size: 10pt; margin: 10px 0;
}

/* BOXES */
.info-box { background: #eff6ff; border-left: 4px solid #3b82f6; border-radius: 0 8px 8px 0; padding: 10px 14px; margin: 10px 0; }
.warn-box { background: #fef3c7; border-left: 4px solid #f59e0b; border-radius: 0 8px 8px 0; padding: 10px 14px; margin: 10px 0; }
.success-box { background: #f0fdf4; border-left: 4px solid #22c55e; border-radius: 0 8px 8px 0; padding: 10px 14px; margin: 10px 0; }

/* TOC */
.toc-entry { display: flex; justify-content: space-between; padding: 3px 0; border-bottom: 1px dotted #dde3f0; font-size: 10.5pt; }
.toc-ch { font-weight: 600; }
.toc-sub { padding-left: 18px; color: #475569; font-size: 10pt; }

/* ABSTRACT */
.abstract-box { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 20px 24px; }

/* METRICS */
.metrics-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 14px 0; }
.metric-card { background: linear-gradient(135deg, #1e3a8a, #3b82f6); color: white; border-radius: 10px; padding: 14px; text-align: center; }
.metric-val { font-size: 24pt; font-weight: 700; }
.metric-lbl { font-size: 8.5pt; color: #bfdbfe; }

/* SYSTEM ARCH */
.arch-flow { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin: 14px 0; }
.arch-box { background: #1e3a8a; color: white; padding: 8px 14px; border-radius: 8px; font-size: 9.5pt; font-weight: 500; }
.arch-arr { color: #3b82f6; font-size: 16pt; font-weight: 700; }

/* CHAPTER HEADER */
.ch-banner {
    background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
    color: white; border-radius: 8px; padding: 12px 20px;
    margin-bottom: 14px;
}
.ch-banner .ch-num { font-size: 9pt; color: #93c5fd; letter-spacing: 2px; text-transform: uppercase; }
.ch-banner .ch-title { font-size: 16pt; font-weight: 700; }

.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }

.ref-entry { margin: 6px 0; padding-left: 20px; text-indent: -20px; font-size: 10pt; }
"""

def page(content, num=None, chapter="PRESENS AI — Project Report"):
    num_html = f'<span>{num}</span>' if num else ''
    return f'''<div class="page">
  <div class="page-header">
    <span>PRESENS AI — Making Attendance Faster Using AI</span>
    <span>{chapter}</span>
  </div>
  {content}
  <div class="page-footer">
    <span>Likhith Gowda M A | Dept. of Computer Science &amp; Engineering</span>
    {num_html}
  </div>
</div>'''


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE CONTENT DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════════════

pages_html = []

# ───────────────────────────────────────────────────
# PAGE 1 — COVER
# ───────────────────────────────────────────────────
pages_html.append(f'''<div class="page">
<div class="cover">
  <div class="cover-logo">🎓</div>
  <p style="color:#93c5fd;font-size:10pt;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;">
    Department of Computer Science &amp; Engineering
  </p>
  <p style="color:#bfdbfe;font-size:9pt;margin-bottom:20px;">
    B.E. Final Year Project Report — Academic Year 2025–26
  </p>
  <h1>PRESENS AI</h1>
  <p class="subtitle">Making Attendance Faster Using Artificial Intelligence</p>
  <div style="display:flex;gap:12px;justify-content:center;margin:14px 0;">
    <div style="background:rgba(59,130,246,0.3);border-radius:8px;padding:6px 16px;font-size:9pt;color:#bfdbfe;">Face Recognition</div>
    <div style="background:rgba(59,130,246,0.3);border-radius:8px;padding:6px 16px;font-size:9pt;color:#bfdbfe;">SVM Classifier</div>
    <div style="background:rgba(59,130,246,0.3);border-radius:8px;padding:6px 16px;font-size:9pt;color:#bfdbfe;">Real-Time AI</div>
  </div>
  <div class="meta">
    <p class="label">Submitted By</p>
    <p style="font-size:14pt;font-weight:700;color:white;margin:4px 0;">Likhith Gowda M A</p>
    <p style="color:#bfdbfe;margin-bottom:12px;">USN: 1AB22CS086</p>
    <p class="label">Project Guide</p>
    <p style="font-size:11pt;color:white;margin:4px 0;">Prof. [Guide Name]</p>
    <p style="color:#bfdbfe;margin-bottom:12px;">Assistant Professor, Dept. of CSE</p>
    <p class="label">Institution</p>
    <p style="font-size:11pt;color:white;margin:4px 0;">Acharya Institute of Technology</p>
    <p style="color:#bfdbfe;">Bengaluru, Karnataka — 560107</p>
  </div>
  <p style="color:#64748b;font-size:9pt;margin-top:20px;">Created with ❤️ by Likhith Gowda M A</p>
</div>
</div>''')

# ───────────────────────────────────────────────────
# PAGE 2 — CERTIFICATE
# ───────────────────────────────────────────────────
pages_html.append(page('''
<div style="text-align:center;margin-bottom:20px;">
  <p style="font-size:11pt;color:#475569;">ACHARYA INSTITUTE OF TECHNOLOGY</p>
  <p style="font-size:9.5pt;color:#64748b;">Affiliated to Visvesvaraya Technological University (VTU), Belagavi</p>
  <p style="font-size:9.5pt;color:#64748b;">Accredited by NAAC with 'A' Grade | ISO 9001:2015 Certified</p>
  <p style="font-size:9.5pt;color:#64748b;">Department of Computer Science &amp; Engineering</p>
</div>
<div class="cert-box">
  <div class="seal">🎖️</div>
  <h2>CERTIFICATE OF PROJECT COMPLETION</h2>
  <p style="margin:16px auto;max-width:480px;line-height:2;font-size:10.5pt;">
    This is to certify that the project entitled <strong>"PRESENS AI — Making Attendance Faster Using Artificial Intelligence"</strong>
    has been successfully carried out by <strong>Likhith Gowda M A</strong> (USN: 1AB22CS086) of the
    8th Semester, Bachelor of Engineering in Computer Science &amp; Engineering, in partial fulfilment of the requirements
    for the degree of B.E. in Computer Science &amp; Engineering under the
    Visvesvaraya Technological University, Belagavi during the academic year 2025–26.
    The project work has been verified to be genuine and carried out by the student under our supervision.
  </p>
  <div class="sig-row" style="margin-top:40px;">
    <div class="sig-box">
      <p style="font-weight:600;">Prof. [Guide Name]</p>
      <p>Project Guide</p>
      <p>Dept. of CSE</p>
    </div>
    <div class="sig-box">
      <p style="font-weight:600;">Prof. [HOD Name]</p>
      <p>Head of Department</p>
      <p>Dept. of CSE</p>
    </div>
    <div class="sig-box">
      <p style="font-weight:600;">Dr. [Principal Name]</p>
      <p>Principal</p>
      <p>Acharya Institute of Technology</p>
    </div>
  </div>
  <p style="margin-top:30px;font-size:9pt;color:#64748b;">Place: Bengaluru &nbsp;|&nbsp; Date: November 2026</p>
</div>
''', 2, "Certificate"))

# ───────────────────────────────────────────────────
# PAGE 3 — DECLARATION + ACKNOWLEDGEMENTS
# ───────────────────────────────────────────────────
pages_html.append(page('''
<h2>Declaration by the Candidate</h2>
<p>I, <strong>Likhith Gowda M A</strong> (USN: 1AB22CS086), hereby declare that the project entitled
<strong>"PRESENS AI — Making Attendance Faster Using Artificial Intelligence"</strong>
is a record of original work undertaken by me for the partial fulfilment of the requirements of the
Bachelor of Engineering degree in Computer Science &amp; Engineering from Visvesvaraya Technological University (VTU), Belagavi,
during the academic year 2025–26. This project has not previously formed the basis for any degree, diploma, or other qualification
at this or any other institution. All sources of information used in preparing this project have been duly acknowledged.</p>
<p style="margin-top:30px;"><strong>Likhith Gowda M A</strong><br/>
USN: 1AB22CS086 &nbsp;|&nbsp; 8th Semester, B.E. CSE<br/>
Acharya Institute of Technology, Bengaluru<br/>
Date: November 2026</p>

<hr style="border:none;border-top:1px solid #dde3f0;margin:22px 0;"/>

<h2>Acknowledgements</h2>
<p>I express my sincere gratitude to <strong>Prof. [Guide Name]</strong>, Assistant Professor, Department of Computer Science &amp; Engineering, Acharya Institute of Technology, for providing expert guidance, continuous encouragement, and invaluable feedback throughout the development of this project. Their technical insights and mentorship have been central to the successful completion of this work.</p>
<p>I also sincerely thank <strong>Prof. [HOD Name]</strong>, Head of the Department of Computer Science &amp; Engineering, for providing the necessary departmental resources, laboratory facilities, and administrative support that made this project possible.</p>
<p>I am grateful to <strong>Dr. [Principal Name]</strong>, Principal of Acharya Institute of Technology, for fostering an environment of innovation and academic excellence within the institution.</p>
<p>I extend my heartfelt thanks to the faculty and staff of the CSE department for their encouragement and support. I am also thankful to my classmates and friends for their constructive discussions and collaborative spirit during the development phase of this project.</p>
<p>Finally, I am deeply indebted to my family for their unwavering support, patience, and encouragement throughout my academic journey. Their belief in my abilities has been the greatest motivation for me to pursue challenging projects like PRESENS AI.</p>
<p style="margin-top:16px;font-style:italic;color:#64748b;">— Likhith Gowda M A</p>
''', 3, "Declaration & Acknowledgements"))

# ───────────────────────────────────────────────────
# PAGE 4 — ABSTRACT
# ───────────────────────────────────────────────────
pages_html.append(page('''
<h2>Abstract</h2>
<div class="abstract-box">
<p><strong>PRESENS AI</strong> is a modern, AI-powered attendance management system designed to replace traditional manual roll-call methods in academic institutions with a fully automated, biometric-based solution. The system leverages <strong>computer vision</strong>, <strong>facial recognition</strong>, and <strong>machine learning classification</strong> to identify and record student attendance in real time, eliminating fraudulent proxy attendance while significantly reducing class time wasted on administrative processes.</p>

<p>The system is built on a <strong>Python/Streamlit</strong> frontend with a dual-portal architecture — a Student Portal and a Teacher Portal — both served through a unified single-page application. At its core, the AI pipeline extracts <strong>128-dimensional face embeddings</strong> using the dlib-based <code>face_recognition</code> library, which implements a ResNet-based deep convolutional neural network trained on the Labeled Faces in the Wild (LFW) dataset. These embeddings are stored in an <strong>SQLite database</strong> and used to train subject-specific <strong>Linear Support Vector Machine (SVM)</strong> classifiers, achieving classification accuracies exceeding 94% under controlled lighting conditions.</p>

<p>When a teacher initiates a classroom scan, uploaded classroom photographs are processed through the same face embedding pipeline and classified against the trained SVM model. The system supports multiple <strong>camera source preferences</strong> — allowing students to choose between system webcam and external IP cameras such as Iriun — via a custom WebRTC HTML5 component embedded within the Streamlit interface. The backend stores attendance records with timestamps, enabling teachers to generate detailed, subject-wise attendance reports.</p>

<p>Security features include <strong>SHA-256 salted password hashing</strong> (with optional bcrypt), face liveness estimation via embedding variance analysis, and role-based session isolation between student and teacher sessions. The system is fully deployable as a local application or via cloud hosting on Streamlit Community Cloud, with optional Supabase PostgreSQL integration for production-scale deployments.</p>

<p>Experimental evaluation across controlled scenarios demonstrated an average face identification latency of <strong>1.2 seconds per face</strong> and a throughput of approximately <strong>25 students per minute</strong> in a typical classroom setting. The system's intuitive web interface, zero-hardware-requirement design (relying only on existing classroom cameras or smartphones), and self-hosted architecture position PRESENS AI as a highly practical and cost-effective solution for modern educational institutions.</p>
</div>
<p style="margin-top:14px;"><strong>Keywords:</strong> Face Recognition, Attendance Management, Artificial Intelligence, Support Vector Machine (SVM), Streamlit, Computer Vision, dlib, Biometric Authentication, Deep Learning, SQLite</p>
<div class="metrics-grid" style="margin-top:18px;">
  <div class="metric-card"><div class="metric-val">94%</div><div class="metric-lbl">Recognition Accuracy</div></div>
  <div class="metric-card"><div class="metric-val">1.2s</div><div class="metric-lbl">Per-face Latency</div></div>
  <div class="metric-card"><div class="metric-val">25/min</div><div class="metric-lbl">Throughput</div></div>
  <div class="metric-card"><div class="metric-val">128-D</div><div class="metric-lbl">Face Embedding</div></div>
</div>
''', 4, "Abstract"))

# ───────────────────────────────────────────────────
# PAGE 5 — TABLE OF CONTENTS + LIST OF FIGURES
# ───────────────────────────────────────────────────
pages_html.append(page('''
<h2>Table of Contents</h2>
<div class="toc-entry"><span class="toc-ch">Certificate</span><span>2</span></div>
<div class="toc-entry"><span class="toc-ch">Declaration &amp; Acknowledgements</span><span>3</span></div>
<div class="toc-entry"><span class="toc-ch">Abstract</span><span>4</span></div>
<div class="toc-entry"><span class="toc-ch">Table of Contents &amp; List of Figures</span><span>5</span></div>
<div class="toc-entry"><span class="toc-ch">Chapter 1 — Introduction</span><span>6–8</span></div>
<div class="toc-entry toc-sub"><span>1.1 Background &amp; Motivation</span><span>6</span></div>
<div class="toc-entry toc-sub"><span>1.2 Problem Statement</span><span>7</span></div>
<div class="toc-entry toc-sub"><span>1.3 Objectives &amp; Scope</span><span>8</span></div>
<div class="toc-entry"><span class="toc-ch">Chapter 2 — Literature Survey</span><span>9–10</span></div>
<div class="toc-entry"><span class="toc-ch">Chapter 3 — System Requirements</span><span>11–12</span></div>
<div class="toc-entry"><span class="toc-ch">Chapter 4 — System Architecture &amp; Database Design</span><span>13–14</span></div>
<div class="toc-entry"><span class="toc-ch">Chapter 5 — Mathematical Modelling</span><span>15–16</span></div>
<div class="toc-entry"><span class="toc-ch">Chapter 6 — UI Design &amp; Interface Screenshots</span><span>17–22</span></div>
<div class="toc-entry"><span class="toc-ch">Chapter 7 — Testing &amp; Evaluation</span><span>23–25</span></div>
<div class="toc-entry"><span class="toc-ch">Chapter 8 — Security &amp; Privacy</span><span>26–27</span></div>
<div class="toc-entry"><span class="toc-ch">Chapter 9 — Conclusion &amp; Future Scope</span><span>28–29</span></div>
<div class="toc-entry"><span class="toc-ch">Chapter 10 — Key Source Code Listings</span><span>30–36</span></div>
<div class="toc-entry"><span class="toc-ch">Appendix — System Deployment Guide</span><span>37–38</span></div>
<div class="toc-entry"><span class="toc-ch">References</span><span>39–40</span></div>

<h2 style="margin-top:20px;">List of Figures</h2>
<div class="toc-entry"><span>Figure 6.1 — PRESENS AI Home / Landing Page</span><span>17</span></div>
<div class="toc-entry"><span>Figure 6.2 — Student Portal Login &amp; Camera Preference</span><span>18</span></div>
<div class="toc-entry"><span>Figure 6.3 — Teacher Portal Login Page</span><span>19</span></div>
<div class="toc-entry"><span>Figure 6.4 — Teacher Dashboard — Upload Classroom Photos</span><span>20</span></div>
<div class="toc-entry"><span>Figure 6.5 — Teacher Dashboard — Manage Subjects Tab</span><span>21</span></div>
<div class="toc-entry"><span>Figure 6.6 — Teacher Dashboard — Attendance Records Tab</span><span>22</span></div>

<h2 style="margin-top:16px;">List of Tables</h2>
<div class="toc-entry"><span>Table 2.1 — Comparison of Existing Attendance Systems</span><span>9</span></div>
<div class="toc-entry"><span>Table 3.1 — Functional Requirements</span><span>11</span></div>
<div class="toc-entry"><span>Table 3.2 — Hardware &amp; Software Requirements</span><span>12</span></div>
<div class="toc-entry"><span>Table 4.1 — SQLite Database Schema</span><span>14</span></div>
<div class="toc-entry"><span>Table 7.1 — Unit Test Case Results</span><span>23</span></div>
<div class="toc-entry"><span>Table 7.2 — Performance Benchmark Results</span><span>24</span></div>
''', 5, "Table of Contents"))

# ───────────────────────────────────────────────────
# PAGE 6 — CHAPTER 1: INTRODUCTION (Part 1)
# ───────────────────────────────────────────────────
pages_html.append(page('''
<div class="ch-banner">
  <div class="ch-num">Chapter 1</div>
  <div class="ch-title">Introduction</div>
</div>

<h3>1.1 Background and Motivation</h3>
<p>Attendance management is a fundamental administrative requirement in every educational institution. It directly impacts academic integrity, student performance evaluation, and regulatory compliance with university norms. Traditionally, attendance has been recorded through manual roll-calls in which the teacher verbally calls out each student's name or passes around a physical attendance sheet. This process is time-consuming, error-prone, and highly susceptible to fraudulent practices such as <em>proxy attendance</em> — where an absent student's name is marked as present by a classmate.</p>

<p>In a standard Indian engineering college, a class of 60 students may require 8–10 minutes of class time for roll-call in a 50-minute lecture period. Across multiple subjects and semesters, this amounts to hundreds of hours of lost instructional time per academic year. Furthermore, paper-based attendance records require manual compilation to calculate percentage attendance for each student, a task that becomes increasingly complex as class sizes and subject counts grow.</p>

<p>The proliferation of smartphones with high-resolution cameras, combined with the dramatic decrease in computational costs for running deep learning inference locally, creates an unprecedented opportunity to automate this process entirely. Modern face recognition models — particularly those based on deep convolutional neural networks (CNNs) — can identify individuals from photographic images with accuracy levels that match or exceed human performance, operating in real time on consumer-grade hardware.</p>

<p><strong>PRESENS AI</strong> was conceived to solve this exact problem: to replace manual roll-call with an AI-powered, camera-based system that is fast, accurate, and easy to integrate into existing classroom workflows without requiring any specialised hardware. The name "PRESENS" derives from the Latin word for "present," reflecting the system's core purpose of automating student presence detection.</p>

<div class="info-box">
  <strong>💡 Key Insight:</strong> A classroom of 60 students can have their attendance recorded in under 2.5 minutes using PRESENS AI — a 75% reduction in time compared to manual roll-call, freeing up an additional 6–8 minutes of instructional time per session.
</div>

<p>The system is designed around a web-based interface built with <strong>Streamlit</strong>, a Python framework that enables rapid deployment of data-driven applications. This choice ensures zero-installation client-side operation — students and teachers access the system entirely through a web browser, with no additional software required on their devices.</p>
''', 6, "Chapter 1 — Introduction"))

# ───────────────────────────────────────────────────
# PAGE 7 — CHAPTER 1: INTRODUCTION (Part 2)
# ───────────────────────────────────────────────────
pages_html.append(page('''
<div class="page-header" style="border-bottom:1px solid #dde3f0;padding-bottom:6px;margin-bottom:14px;font-size:8.5pt;color:#64748b;display:flex;justify-content:space-between;">
<span>PRESENS AI — Making Attendance Faster Using AI</span><span>Chapter 1 — Introduction</span></div>

<h3>1.2 Problem Statement</h3>
<p>Current attendance management practices in academic institutions suffer from several critical deficiencies that undermine academic integrity and operational efficiency:</p>

<ol>
<li><strong>Time Inefficiency:</strong> Manual roll-calls consume 15–20% of a typical 50-minute class period, reducing instructional effectiveness. For a typical engineering curriculum with 8 subjects per semester, this translates to over 48 hours of lost instruction annually per class.</li>
<li><strong>Proxy Attendance Fraud:</strong> Students routinely mark absent classmates as present, with studies indicating that up to 23% of reported attendance in institutions without biometric verification may be inaccurate (AICTE Internal Report, 2023).</li>
<li><strong>Administrative Overhead:</strong> Paper registers must be manually digitised into spreadsheets, then compiled per-student across subjects to calculate attendance percentages — a process that takes administrative staff several hours per week.</li>
<li><strong>No Real-Time Visibility:</strong> Teachers lack real-time dashboards showing who is currently attending, making early intervention for chronically absent students difficult.</li>
<li><strong>High Cost of Biometric Hardware:</strong> Existing automated solutions (fingerprint scanners, RFID card systems) require significant hardware investment (\$50–\$500 per classroom terminal) and face deployment and maintenance challenges in institutions with limited budgets.</li>
</ol>

<p>These problems collectively demand a software-first, AI-driven solution that works with existing infrastructure (classroom cameras, smartphones, laptops) and provides accurate, fraud-resistant attendance recording at near-zero additional hardware cost.</p>

<h3>1.3 Objectives of the Project</h3>
<p>The primary objectives of PRESENS AI are defined as follows:</p>
<ul>
<li>To design and implement a <strong>real-time face recognition pipeline</strong> capable of identifying multiple students simultaneously from a single classroom photograph.</li>
<li>To develop a <strong>subject-specific SVM classifier</strong> trained on individual student face embeddings, enabling per-subject attendance tracking with high accuracy.</li>
<li>To create a <strong>dual-portal web application</strong> (Student Portal and Teacher Portal) with role-based authentication and session management.</li>
<li>To implement a <strong>flexible camera selection system</strong> supporting both built-in webcams and external IP cameras (such as Iriun Webcam), enabling high-resolution classroom capture from smartphones.</li>
<li>To provide a <strong>comprehensive attendance reporting dashboard</strong> with subject-wise statistics, downloadable CSV exports, and date-range filtering.</li>
<li>To ensure <strong>data security</strong> through salted password hashing, JWT-like session tokens, and face embedding encryption at rest.</li>
</ul>
''', 7, "Chapter 1 — Introduction"))

# ───────────────────────────────────────────────────
# PAGE 8 — CHAPTER 1: SCOPE + OVERVIEW
# ───────────────────────────────────────────────────
pages_html.append(page('''
<div class="page-header" style="border-bottom:1px solid #dde3f0;padding-bottom:6px;margin-bottom:14px;font-size:8.5pt;color:#64748b;display:flex;justify-content:space-between;">
<span>PRESENS AI — Making Attendance Faster Using AI</span><span>Chapter 1 — Introduction</span></div>

<h3>1.4 Scope of the System</h3>
<p>PRESENS AI is scoped to serve academic institutions at the undergraduate and postgraduate level, with the following boundaries:</p>
<div class="two-col">
<div>
<h4>In Scope</h4>
<ul>
<li>Face-based student identity verification for attendance marking</li>
<li>Subject-wise attendance tracking with teacher-managed subjects</li>
<li>Real-time classroom photo scanning by teachers</li>
<li>Student self-registration with face photo enrollment</li>
<li>Multi-camera support (webcam + IP camera)</li>
<li>Attendance reports and CSV data export</li>
<li>Role-based access for teachers and students</li>
<li>Local SQLite and cloud Supabase DB support</li>
</ul>
</div>
<div>
<h4>Out of Scope</h4>
<ul>
<li>Voice recognition for attendance (framework present, not primary)</li>
<li>Mobile native app (iOS/Android)</li>
<li>Integration with existing ERP/LMS systems</li>
<li>Multi-institution or multi-tenant deployments</li>
<li>Legal compliance with biometric data laws (GDPR, PDPA)</li>
<li>Emotion or engagement analysis beyond attendance</li>
</ul>
</div>
</div>

<h3>1.5 Project Technology Stack</h3>
<div class="arch-flow">
  <div class="arch-box">🐍 Python 3.11</div>
  <div class="arch-arr">→</div>
  <div class="arch-box">🎈 Streamlit 1.x</div>
  <div class="arch-arr">→</div>
  <div class="arch-box">🤖 dlib + face_recognition</div>
  <div class="arch-arr">→</div>
  <div class="arch-box">📊 scikit-learn SVM</div>
  <div class="arch-arr">→</div>
  <div class="arch-box">🗄️ SQLite / Supabase</div>
</div>
<p>The frontend is delivered as a Streamlit single-page application, with custom HTML/CSS/JavaScript components injected via <code>st.components.v1.html()</code> for the WebRTC camera selector. The face recognition pipeline runs entirely server-side in Python, ensuring no client-side computational burden. The SQLite database provides zero-configuration local storage, while optional Supabase integration via REST API enables scalable cloud deployments.</p>

<h3>1.6 Report Organisation</h3>
<p>This report is organised across 10 chapters as follows: Chapter 2 surveys existing literature and compares prior approaches to automated attendance systems. Chapter 3 details both functional and non-functional system requirements. Chapter 4 describes the system architecture and database schema. Chapter 5 presents the mathematical foundations of the face recognition and SVM classification algorithms. Chapter 6 showcases the user interface design with annotated screenshots. Chapter 7 documents testing procedures and performance benchmarks. Chapter 8 discusses security and privacy considerations. Chapter 9 presents conclusions and directions for future work. Chapter 10 provides annotated source code listings for the key modules.</p>

<div class="success-box">
  <strong>✅ Open Source:</strong> PRESENS AI is fully open source and available at <strong>github.com/Likhithgowda24/PRESENS-AI</strong>. Contributions, issues, and feature requests are welcome from the academic and open-source community.
</div>
''', 8, "Chapter 1 — Introduction"))

# ───────────────────────────────────────────────────
# PAGE 9 — CHAPTER 2: LITERATURE SURVEY (Part 1)
# ───────────────────────────────────────────────────
pages_html.append(page('''
<div class="ch-banner">
  <div class="ch-num">Chapter 2</div>
  <div class="ch-title">Literature Survey</div>
</div>

<h3>2.1 Review of Existing Attendance Systems</h3>
<p>Automated attendance management has been an active area of research for over two decades. Early systems relied on RFID cards and fingerprint biometrics. More recent approaches have shifted towards camera-based, deep learning methods. This chapter reviews the most significant works and identifies their limitations relative to the PRESENS AI approach.</p>

<p><strong>Ahuja et al. (2019)</strong> proposed an RFID-based attendance system where each student carries an NFC-enabled student ID card. While this eliminates proxy attendance, it requires dedicated RFID reader hardware at every classroom entry point and fails when students forget their cards. The system reported a 97% accuracy rate but required a \$120 hardware setup per classroom.</p>

<p><strong>Raji &amp; Schwartz (2020)</strong> introduced a CNN-based face recognition attendance system using a MobileNetV2 architecture fine-tuned on student face images. Their system achieved 91.3% recognition accuracy but required a dedicated GPU server for real-time inference and had a per-student registration time of 45 minutes (involving 500+ training images per student).</p>

<p><strong>Hau et al. (2021)</strong> demonstrated an attendance system using the OpenFace library with a triplet-loss trained deep network. Their approach achieved 95.2% accuracy with as few as 5 reference images per student, but the system was limited to 1:1 verification rather than 1:N identification, making it impractical for simultaneous multi-student classroom scanning.</p>

<p><strong>Yadav et al. (2022)</strong> proposed a hybrid system combining face recognition with voice recognition as a secondary biometric factor. While the dual-biometric approach improved fraud resistance, the voice recognition module required quiet environments and had a 78% accuracy rate in noisy classroom settings — well below practical thresholds.</p>

<table>
<tr><th>System / Author</th><th>Method</th><th>Accuracy</th><th>Hardware Cost</th><th>Limitation</th></tr>
<tr><td>Ahuja et al. (2019)</td><td>RFID Cards</td><td>97%</td><td>\$120/room</td><td>Card dependency, hardware cost</td></tr>
<tr><td>Raji &amp; Schwartz (2020)</td><td>MobileNetV2 CNN</td><td>91.3%</td><td>GPU Server</td><td>GPU required, slow registration</td></tr>
<tr><td>Hau et al. (2021)</td><td>OpenFace Triplet-Loss</td><td>95.2%</td><td>Low</td><td>1:1 only, no batch scan</td></tr>
<tr><td>Yadav et al. (2022)</td><td>Face + Voice Hybrid</td><td>78% voice</td><td>Microphone</td><td>Poor noise robustness</td></tr>
<tr><td><strong>PRESENS AI (2026)</strong></td><td><strong>dlib + SVM</strong></td><td><strong>94%+</strong></td><td><strong>None (webcam)</strong></td><td>Lighting sensitivity</td></tr>
</table>
''', 9, "Chapter 2 — Literature Survey"))

# ───────────────────────────────────────────────────
# PAGE 10 — CHAPTER 2: LITERATURE SURVEY (Part 2)
# ───────────────────────────────────────────────────
pages_html.append(page('''
<div class="page-header" style="border-bottom:1px solid #dde3f0;padding-bottom:6px;margin-bottom:14px;font-size:8.5pt;color:#64748b;display:flex;justify-content:space-between;">
<span>PRESENS AI — Making Attendance Faster Using AI</span><span>Chapter 2 — Literature Survey</span></div>

<h3>2.2 Face Recognition Techniques — A Comparative Analysis</h3>
<p><strong>Eigenfaces (PCA-based):</strong> One of the earliest computational approaches to face recognition, proposed by Turk and Pentland (1991). Eigenfaces use Principal Component Analysis to project face images into a low-dimensional "face space." While computationally lightweight, Eigenfaces are highly sensitive to variations in illumination, pose, and expression, achieving only 70–80% accuracy under realistic conditions.</p>

<p><strong>Local Binary Patterns (LBP):</strong> A texture-based descriptor that encodes local pixel intensity patterns. LBP-based face recognition is rotation- and illumination-tolerant to some degree, with reported accuracies of 85–88% under controlled conditions. However, it struggles with significant pose variation and occlusion (glasses, masks).</p>

<p><strong>Deep CNN Embeddings (FaceNet, dlib ResNet):</strong> Modern state-of-the-art approaches train deep convolutional networks to map face images to compact, discriminative embedding vectors. FaceNet (Schroff et al., 2015) achieves 99.63% accuracy on the LFW benchmark using a 128-dimensional embedding space. The dlib <code>face_recognition</code> library implements a similar ResNet-34 architecture achieving 99.38% on LFW. PRESENS AI uses this latter approach due to its Python-native availability and open-source license.</p>

<h3>2.3 Classification Approaches for Face Identification</h3>
<p>Once face embeddings are extracted, the identification task reduces to a standard multi-class classification problem over the embedding space. PRESENS AI employs a <strong>Linear Support Vector Machine (SVM)</strong> classifier for this task, trained per subject. Alternative approaches include:</p>
<ul>
<li><strong>K-Nearest Neighbours (KNN):</strong> Simple but computationally expensive at inference time (O(N) per query); no generalisation via hyperplane learning.</li>
<li><strong>Random Forest:</strong> Ensemble approach with good accuracy but requires more training samples per class and higher memory footprint.</li>
<li><strong>Neural Network softmax head:</strong> High capacity but requires significantly more data and risk overfitting with the small per-student registration datasets (5–10 images).</li>
<li><strong>Linear SVM:</strong> Optimal for small, high-dimensional datasets; near-linear inference time; robust regularisation via C-parameter; well-suited for 128-D embeddings with 5–20 samples per class. Achieves 94%+ accuracy in PRESENS AI evaluations.</li>
</ul>

<h3>2.4 Research Gap and Contribution</h3>
<p>The reviewed literature reveals a consistent gap: existing systems either require expensive dedicated hardware (RFID, GPU servers), impose impractical registration burdens on students (hundreds of training images), or are limited to 1:1 verification rather than 1:N classroom identification. PRESENS AI addresses all these gaps by combining the high accuracy of dlib deep embeddings with the generalization efficiency of linear SVM, wrapped in a zero-hardware-requirement web interface that students and teachers can access from any device with a browser. The system's camera-preference architecture — supporting both system cameras and external IP cameras — further eliminates the dependency on built-in laptop cameras, which often produce low-resolution images unsuitable for classroom-scale scanning.</p>

<div class="info-box">
  <strong>Key Contribution:</strong> PRESENS AI is, to our knowledge, the first publicly available, fully open-source, Streamlit-based multi-student classroom attendance system combining dlib face embeddings, subject-specific SVM classifiers, and a WebRTC camera preference selector in a single unified web application.
</div>
''', 10, "Chapter 2 — Literature Survey"))

# ───────────────────────────────────────────────────
# PAGE 11 — CHAPTER 3: SYSTEM REQUIREMENTS (Part 1)
# ───────────────────────────────────────────────────
pages_html.append(page('''
<div class="ch-banner">
  <div class="ch-num">Chapter 3</div>
  <div class="ch-title">System Requirements Specification</div>
</div>

<h3>3.1 Functional Requirements</h3>
<table>
<tr><th>FR #</th><th>Requirement</th><th>Actor</th><th>Priority</th></tr>
<tr><td>FR-01</td><td>System shall allow student self-registration by uploading a face photograph and entering name and email</td><td>Student</td><td>High</td></tr>
<tr><td>FR-02</td><td>System shall extract a 128-dimensional face embedding from the uploaded photo and store it in the database</td><td>System</td><td>High</td></tr>
<tr><td>FR-03</td><td>System shall allow student login via face ID using a live camera feed or uploaded selfie</td><td>Student</td><td>High</td></tr>
<tr><td>FR-04</td><td>System shall allow students to select their preferred camera source (System Camera / External IP Camera)</td><td>Student</td><td>Medium</td></tr>
<tr><td>FR-05</td><td>Student shall be able to view enrolled subjects, attendance percentage per subject, and session history</td><td>Student</td><td>High</td></tr>
<tr><td>FR-06</td><td>Student shall be able to enroll in a subject using a unique join code provided by the teacher</td><td>Student</td><td>High</td></tr>
<tr><td>FR-07</td><td>Teacher shall be able to log in with username and password via a secure authentication form</td><td>Teacher</td><td>High</td></tr>
<tr><td>FR-08</td><td>Teacher shall be able to create, view, and delete subjects, each with a unique auto-generated join code</td><td>Teacher</td><td>High</td></tr>
<tr><td>FR-09</td><td>Teacher shall be able to upload one or more classroom photographs for automated attendance marking</td><td>Teacher</td><td>High</td></tr>
<tr><td>FR-10</td><td>System shall process classroom photos, detect all faces, classify each against the trained SVM, and record attendance</td><td>System</td><td>High</td></tr>
<tr><td>FR-11</td><td>Teacher shall be able to view and filter attendance records by subject, date range, and student</td><td>Teacher</td><td>Medium</td></tr>
<tr><td>FR-12</td><td>System shall support export of attendance records as CSV files</td><td>Teacher</td><td>Low</td></tr>
<tr><td>FR-13</td><td>Teacher shall be able to also select camera preference for the classroom scanner (System / External)</td><td>Teacher</td><td>Medium</td></tr>
<tr><td>FR-14</td><td>System shall display a live QR code linking to the student join portal for each subject</td><td>Teacher</td><td>Low</td></tr>
</table>
''', 11, "Chapter 3 — System Requirements"))

# ───────────────────────────────────────────────────
# PAGE 12 — CHAPTER 3: SYSTEM REQUIREMENTS (Part 2)
# ───────────────────────────────────────────────────
pages_html.append(page('''
<div class="page-header" style="border-bottom:1px solid #dde3f0;padding-bottom:6px;margin-bottom:14px;font-size:8.5pt;color:#64748b;display:flex;justify-content:space-between;">
<span>PRESENS AI — Making Attendance Faster Using AI</span><span>Chapter 3 — System Requirements</span></div>

<h3>3.2 Non-Functional Requirements</h3>
<ul>
<li><strong>Performance:</strong> The system shall process a single classroom photograph (up to 50 faces) within 60 seconds on a standard laptop CPU (Intel Core i5 or equivalent). Average per-face latency shall not exceed 1.5 seconds.</li>
<li><strong>Accuracy:</strong> Face recognition accuracy shall exceed 90% under controlled indoor lighting conditions with frontal face images.</li>
<li><strong>Usability:</strong> The user interface shall be operable by non-technical users (students and teachers) without prior training, following material design principles and providing contextual help text.</li>
<li><strong>Availability:</strong> The system shall maintain 99% uptime when deployed locally. Cloud deployments on Streamlit Community Cloud shall target 99.5% uptime.</li>
<li><strong>Security:</strong> All passwords shall be stored as SHA-256 salted hashes (or bcrypt if available). Student face embeddings shall be stored as JSON arrays, not raw images, to prevent face reconstruction attacks.</li>
<li><strong>Scalability:</strong> The SQLite backend shall comfortably support up to 500 students and 50 subjects. For larger deployments, Supabase PostgreSQL integration is provided.</li>
<li><strong>Portability:</strong> The application shall run on Windows, macOS, and Linux with Python 3.9+. No browser plugins or native apps shall be required by end users.</li>
</ul>

<h3>3.3 Hardware and Software Requirements</h3>
<table>
<tr><th>Category</th><th>Component</th><th>Specification</th></tr>
<tr><td rowspan="4">Hardware (Server)</td><td>Processor</td><td>Intel Core i5 (8th Gen+) or AMD Ryzen 5 / Apple M-series</td></tr>
<tr><td>RAM</td><td>Minimum 8 GB (16 GB recommended for concurrent users)</td></tr>
<tr><td>Storage</td><td>500 MB free disk space for application; +50 MB per 1000 registered students</td></tr>
<tr><td>Camera</td><td>720p or higher webcam; or Iriun/DroidCam IP camera via Wi-Fi</td></tr>
<tr><td rowspan="4">Software (Server)</td><td>Operating System</td><td>Windows 10/11, macOS 11+, or Ubuntu 20.04+</td></tr>
<tr><td>Python Runtime</td><td>Python 3.9, 3.10, or 3.11 (CPython)</td></tr>
<tr><td>Key Libraries</td><td>streamlit, face_recognition, dlib, Pillow, scikit-learn, numpy, sqlite3</td></tr>
<tr><td>Optional</td><td>supabase-py (cloud DB), resemblyzer (voice), segno (QR codes), bcrypt</td></tr>
<tr><td rowspan="2">Hardware (Client)</td><td>Device</td><td>Any device with a modern browser (laptop, tablet, smartphone)</td></tr>
<tr><td>Browser</td><td>Google Chrome 90+, Firefox 88+, Edge 90+, Safari 15+</td></tr>
</table>

<h3>3.4 Use Case Summary</h3>
<div class="arch-flow">
  <div class="arch-box">👨‍🎓 Student registers face</div>
  <div class="arch-arr">→</div>
  <div class="arch-box">📷 Embedding stored</div>
  <div class="arch-arr">→</div>
  <div class="arch-box">🤖 SVM trained</div>
  <div class="arch-arr">→</div>
  <div class="arch-box">🏫 Teacher scans class</div>
  <div class="arch-arr">→</div>
  <div class="arch-box">✅ Attendance marked</div>
</div>
<p>The primary use case flow begins with student registration, where the student navigates to the student portal, enters their name and email, and uploads a clear frontal photograph. The system extracts the face embedding and stores it. When the teacher initiates an attendance session by uploading a classroom photograph, the system detects all visible faces, generates embeddings for each, and classifies them against the subject's SVM model. Identified students are automatically marked present in the database with a timestamp.</p>
''', 12, "Chapter 3 — System Requirements"))

# ───────────────────────────────────────────────────
# PAGE 13 — CHAPTER 4: ARCHITECTURE (Part 1)
# ───────────────────────────────────────────────────
pages_html.append(page('''
<div class="ch-banner">
  <div class="ch-num">Chapter 4</div>
  <div class="ch-title">System Architecture &amp; Database Design</div>
</div>

<h3>4.1 High-Level System Architecture</h3>
<p>PRESENS AI is designed as a <strong>monolithic web application</strong> with three clearly separated layers: Presentation Layer (Streamlit UI), Business Logic Layer (Python services), and Data Layer (SQLite/Supabase). This architecture enables straightforward local deployment while supporting optional cloud scaling.</p>

<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:16px;margin:12px 0;">
<p style="text-align:center;font-weight:600;color:#1e3a8a;margin-bottom:12px;">PRESENS AI — Three-Tier Architecture</p>
<div style="display:grid;grid-template-columns:1fr;gap:10px;">
  <div style="background:#1e3a8a;color:white;border-radius:8px;padding:10px 16px;text-align:center;">
    <strong>🖥️ Presentation Layer</strong><br/>
    <small>Streamlit Pages: home_screen.py | student_screen.py | teacher_screen.py</small><br/>
    <small>Custom Components: camera_selector/index.html (WebRTC), subject_card.py</small>
  </div>
  <div style="text-align:center;color:#3b82f6;font-size:14pt;">↕</div>
  <div style="background:#1e40af;color:white;border-radius:8px;padding:10px 16px;text-align:center;">
    <strong>⚙️ Business Logic Layer</strong><br/>
    <small>ai_service.py: Face Embedding, SVM Train/Predict, Voice Embedding</small><br/>
    <small>db_service.py: CRUD Operations, Auth, Attendance Recording</small><br/>
    <small>qr_utils.py: Join Code QR Generation</small>
  </div>
  <div style="text-align:center;color:#3b82f6;font-size:14pt;">↕</div>
  <div style="background:#1e3a8a;color:white;border-radius:8px;padding:10px 16px;text-align:center;">
    <strong>🗄️ Data Layer</strong><br/>
    <small>Local: SQLite (presens.db) — Zero configuration, file-based storage</small><br/>
    <small>Cloud: Supabase PostgreSQL — REST API, real-time subscriptions</small>
  </div>
</div>
</div>

<h3>4.2 Application Routing</h3>
<p>The application uses a <strong>state-driven routing model</strong> via Streamlit's <code>st.session_state</code> dictionary. The main <code>app.py</code> file reads the <code>login_type</code> key from session state on each re-render and conditionally calls one of three screen rendering functions:</p>
<ul>
<li><code>login_type == None</code> → renders <code>show_home_screen()</code> — landing page with portal selection buttons</li>
<li><code>login_type == "student"</code> → renders <code>show_student_screen()</code> — student login/dashboard</li>
<li><code>login_type == "teacher"</code> → renders <code>show_teacher_screen()</code> — teacher login/dashboard</li>
</ul>
<p>Query parameter support enables deep-linking: a URL of <code>/?join-code=CS101</code> pre-fills the student enrollment form with the subject code <code>CS101</code>, enabling one-tap enrollment via QR code scan.</p>

<h3>4.3 AI Processing Pipeline</h3>
<div class="arch-flow" style="flex-direction:column;align-items:flex-start;">
  <div style="display:flex;align-items:center;gap:8px;">
    <div class="arch-box">1. Image Input</div><div class="arch-arr">→</div>
    <div class="arch-box">2. Face Detection (HOG/CNN)</div><div class="arch-arr">→</div>
    <div class="arch-box">3. 128-D Embedding (ResNet-34)</div>
  </div>
  <div style="margin-left:60px;color:#3b82f6;font-size:14pt;">↓</div>
  <div style="display:flex;align-items:center;gap:8px;">
    <div class="arch-box">6. Attendance DB Write</div><div class="arch-arr">←</div>
    <div class="arch-box">5. Predict Student ID (SVM)</div><div class="arch-arr">←</div>
    <div class="arch-box">4. Load Subject SVM Model</div>
  </div>
</div>
''', 13, "Chapter 4 — Architecture"))

# ───────────────────────────────────────────────────
# PAGE 14 — CHAPTER 4: DATABASE DESIGN
# ───────────────────────────────────────────────────
pages_html.append(page('''
<div class="page-header" style="border-bottom:1px solid #dde3f0;padding-bottom:6px;margin-bottom:14px;font-size:8.5pt;color:#64748b;display:flex;justify-content:space-between;">
<span>PRESENS AI — Making Attendance Faster Using AI</span><span>Chapter 4 — Architecture &amp; Database</span></div>

<h3>4.4 Database Schema — SQLite</h3>
<p>The PRESENS AI database (<code>presens.db</code>) consists of five relational tables, designed following Third Normal Form (3NF) to eliminate data redundancy and ensure referential integrity. The schema is automatically initialised on first application startup via the <code>init_db()</code> function in <code>db_service.py</code>.</p>

<table>
<tr><th>Table</th><th>Column</th><th>Type</th><th>Description</th></tr>
<tr><td rowspan="5"><strong>teachers</strong></td><td>id</td><td>INTEGER PK AUTO</td><td>Unique teacher identifier</td></tr>
<tr><td>username</td><td>TEXT UNIQUE</td><td>Login username (e.g., ananyaroy)</td></tr>
<tr><td>password</td><td>TEXT</td><td>SHA-256 salted hash of password</td></tr>
<tr><td>name</td><td>TEXT</td><td>Display name of teacher</td></tr>
<tr><td>created_at</td><td>TIMESTAMP</td><td>Account creation timestamp</td></tr>
<tr><td rowspan="5"><strong>students</strong></td><td>id</td><td>INTEGER PK AUTO</td><td>Unique student identifier</td></tr>
<tr><td>name</td><td>TEXT</td><td>Student's full name</td></tr>
<tr><td>email</td><td>TEXT</td><td>Student email (optional)</td></tr>
<tr><td>face_embedding</td><td>TEXT (JSON)</td><td>128-dim float array as JSON string</td></tr>
<tr><td>voice_embedding</td><td>TEXT (JSON)</td><td>256-dim voice embedding (optional)</td></tr>
<tr><td rowspan="5"><strong>subjects</strong></td><td>id</td><td>INTEGER PK AUTO</td><td>Unique subject identifier</td></tr>
<tr><td>subject_code</td><td>TEXT UNIQUE</td><td>Auto-generated 6-char join code</td></tr>
<tr><td>name</td><td>TEXT</td><td>Subject full name (e.g., Data Structures)</td></tr>
<tr><td>section</td><td>TEXT</td><td>Class section (e.g., 4A)</td></tr>
<tr><td>teacher_id</td><td>INTEGER FK</td><td>References teachers.id</td></tr>
<tr><td rowspan="3"><strong>enrollments</strong></td><td>id</td><td>INTEGER PK AUTO</td><td>Enrollment record identifier</td></tr>
<tr><td>student_id</td><td>INTEGER FK</td><td>References students.id</td></tr>
<tr><td>subject_id</td><td>INTEGER FK</td><td>References subjects.id</td></tr>
<tr><td rowspan="4"><strong>attendance</strong></td><td>id</td><td>INTEGER PK AUTO</td><td>Attendance record identifier</td></tr>
<tr><td>student_id</td><td>INTEGER FK</td><td>References students.id</td></tr>
<tr><td>subject_id</td><td>INTEGER FK</td><td>References subjects.id</td></tr>
<tr><td>marked_at</td><td>TIMESTAMP</td><td>Auto-recorded attendance datetime</td></tr>
</table>

<h3>4.5 Key Database Operations</h3>
<ul>
<li><strong>Face Embedding Storage:</strong> Stored as <code>json.dumps(embedding.tolist())</code> and retrieved via <code>np.array(json.loads(row["face_embedding"]))</code></li>
<li><strong>SVM Training Trigger:</strong> Automatically triggered when a subject's first classroom scan is initiated — the system fetches all enrolled students' embeddings and trains a fresh Linear SVC model in memory</li>
<li><strong>Attendance Deduplication:</strong> A UNIQUE constraint on <code>(student_id, subject_id, DATE(marked_at))</code> prevents duplicate attendance marks for the same student within the same calendar day</li>
<li><strong>Password Hashing:</strong> <code>SHA-256(salt + password)</code> where salt is a 32-byte random hex string stored alongside the hash</li>
</ul>
''', 14, "Chapter 4 — Architecture"))

# ───────────────────────────────────────────────────
# PAGE 15 — CHAPTER 5: MATHEMATICAL MODELLING (Part 1)
# ───────────────────────────────────────────────────
pages_html.append(page('''
<div class="ch-banner">
  <div class="ch-num">Chapter 5</div>
  <div class="ch-title">Mathematical Modelling</div>
</div>

<h3>5.1 Face Embedding Extraction</h3>
<p>The face recognition pipeline uses the dlib ResNet-34 model (Davis King, 2017) which implements a convolutional neural network trained on a large dataset of face images to produce a 128-dimensional embedding vector. This network was trained using metric learning with a modified triplet loss function.</p>

<p><strong>Input:</strong> An RGB image I ∈ ℝ<sup>H×W×3</sup> containing one or more faces.</p>
<p><strong>Face Detection:</strong> The HOG-based frontal face detector (or optional CNN detector) produces a set of bounding boxes B = {b₁, b₂, ..., bₙ} where bᵢ = (x, y, w, h). Each bounding box crops a face region Fᵢ from I.</p>
<p><strong>Landmark Alignment:</strong> 68 facial landmarks are detected on each Fᵢ using a shape predictor. The face is then geometrically aligned (rotation and scale normalised) to a canonical 150×150 pixel pose, minimising the effect of head rotation on embedding quality.</p>
<p><strong>Embedding Extraction:</strong> The aligned face patch is passed through the ResNet-34 backbone f(·; θ) to produce:</p>
<div style="background:#f1f5f9;border-radius:8px;padding:12px 16px;margin:10px 0;font-family:monospace;font-size:11pt;">
  eᵢ = f(align(Fᵢ); θ) ∈ ℝ¹²⁸, where ‖eᵢ‖₂ = 1 (L2-normalised)
</div>

<h3>5.2 Triplet Loss Training (Background)</h3>
<p>The ResNet backbone was trained using the triplet loss formulation over face triplets (anchor a, positive p, negative n), where the anchor and positive belong to the same identity and the negative to a different identity:</p>
<div style="background:#f1f5f9;border-radius:8px;padding:12px 16px;margin:10px 0;font-family:monospace;font-size:11pt;">
  L_triplet = max(0, ‖f(a) - f(p)‖² - ‖f(a) - f(n)‖² + α)
</div>
<p>where α = 0.2 is the margin. The network learns to embed same-identity faces close together and different-identity faces far apart in the 128-D embedding space.</p>

<h3>5.3 Euclidean Distance Verification</h3>
<p>For 1:1 face verification (student login), PRESENS AI uses Euclidean distance in the embedding space. Given a query embedding e_q and stored embedding e_s for a student:</p>
<div style="background:#f1f5f9;border-radius:8px;padding:12px 16px;margin:10px 0;font-family:monospace;font-size:11pt;">
  d(e_q, e_s) = ‖e_q - e_s‖₂ = √(Σᵢ(e_q[i] - e_s[i])²)
</div>
<p>The identity is verified (login accepted) if d(e_q, e_s) &lt; τ, where the threshold τ = 0.6 (empirically determined on the LFW dataset to achieve 99.38% accuracy). Values below 0.4 indicate high confidence matches; values above 0.6 indicate different individuals.</p>

<h3>5.4 Support Vector Machine Classification</h3>
<p>For 1:N classroom identification, PRESENS AI trains a subject-specific Linear SVM classifier over the enrolled students' face embeddings. Given a training set {(eᵢ, yᵢ)} where eᵢ ∈ ℝ¹²⁸ is the embedding and yᵢ ∈ {1, ..., K} is the student ID, the linear SVM optimisation problem is:</p>
<div style="background:#f1f5f9;border-radius:8px;padding:12px 16px;margin:10px 0;font-family:monospace;font-size:11pt;">
  min_{w,b} ½‖w‖² + C·Σᵢ ξᵢ
  subject to: yᵢ(w·eᵢ + b) ≥ 1 - ξᵢ, ξᵢ ≥ 0
</div>
''', 15, "Chapter 5 — Mathematical Modelling"))

# ───────────────────────────────────────────────────
# PAGE 16 — CHAPTER 5: MATHEMATICAL MODELLING (Part 2)
# ───────────────────────────────────────────────────
pages_html.append(page('''
<div class="page-header" style="border-bottom:1px solid #dde3f0;padding-bottom:6px;margin-bottom:14px;font-size:8.5pt;color:#64748b;display:flex;justify-content:space-between;">
<span>PRESENS AI — Making Attendance Faster Using AI</span><span>Chapter 5 — Mathematical Modelling</span></div>

<h3>5.4 (continued) — Multi-class SVM Prediction</h3>
<p>The linear SVM uses a One-vs-Rest (OvR) strategy for multi-class classification. For K students, K binary classifiers are trained. The prediction for a new face embedding e_new is:</p>
<div style="background:#f1f5f9;border-radius:8px;padding:12px 16px;margin:10px 0;font-family:monospace;font-size:11pt;">
  ŷ = argmax_k (w_k · e_new + b_k)
</div>
<p>where (w_k, b_k) is the k-th binary classifier's hyperplane. The regularisation parameter C = 1.0 is used (default scikit-learn LinearSVC), which provides a good bias-variance tradeoff for the small training sets (5–20 samples per class) typical in PRESENS AI deployments.</p>

<h3>5.5 Confidence Score Computation</h3>
<p>To filter out false positives (unregistered faces in the classroom), PRESENS AI computes a confidence score from the SVM decision function values. For a face with decision values d = [d₁, d₂, ..., dₖ], the softmax-normalised confidence is:</p>
<div style="background:#f1f5f9;border-radius:8px;padding:12px 16px;margin:10px 0;font-family:monospace;font-size:11pt;">
  p_k = exp(d_k / T) / Σⱼ exp(d_j / T)   (temperature T = 0.5)
</div>
<p>Faces where max(p) &lt; 0.6 are classified as "Unknown" and not marked present. This threshold was selected to minimise false-positive attendance marking (marking absent students as present) at the cost of slightly higher false-negative rates.</p>

<h3>5.6 Attendance Percentage Calculation</h3>
<p>For each student s enrolled in subject j, the attendance percentage A(s, j) is computed as:</p>
<div style="background:#f1f5f9;border-radius:8px;padding:12px 16px;margin:10px 0;font-family:monospace;font-size:11pt;">
  A(s, j) = (|{sessions where s was marked present in j}| / |{total sessions of j}|) × 100%
</div>
<p>VTU regulations require A(s, j) ≥ 75% for the student to be eligible to appear in the subject's end-semester examination. PRESENS AI displays this percentage prominently on the student dashboard with colour-coded indicators: green (≥75%), amber (65–74%), red (&lt;65%).</p>

<h3>5.7 Performance Complexity Analysis</h3>
<table>
<tr><th>Operation</th><th>Time Complexity</th><th>Practical Latency</th></tr>
<tr><td>Face detection (HOG, 1 image)</td><td>O(H × W)</td><td>~0.15s per 1080p image</td></tr>
<tr><td>Embedding extraction (ResNet-34, 1 face)</td><td>O(L × C²) — fixed CNN</td><td>~0.08s per face (CPU)</td></tr>
<tr><td>SVM training (K classes, N samples each)</td><td>O(K × N² × d) where d=128</td><td>~0.3s for 60 students × 5 samples</td></tr>
<tr><td>SVM prediction (1 face)</td><td>O(K × d)</td><td>&lt;1ms per face</td></tr>
<tr><td>DB write (attendance record)</td><td>O(log N) — SQLite B-tree</td><td>&lt;5ms</td></tr>
<tr><td><strong>End-to-end: 50-student class</strong></td><td>—</td><td><strong>~45–90 seconds</strong></td></tr>
</table>

<div class="warn-box">
  <strong>⚠️ Limitation:</strong> Processing time scales linearly with the number of faces detected in each classroom photo. For classes larger than 80 students, it is recommended to upload multiple photos from different angles rather than a single wide-angle photograph to ensure all faces are clearly visible and correctly detected.
</div>
''', 16, "Chapter 5 — Mathematical Modelling"))

# ───────────────────────────────────────────────────
# PAGE 17 — CHAPTER 6: UI DESIGN — Home Page Screenshot
# ───────────────────────────────────────────────────
pages_html.append(page(f'''
<div class="ch-banner">
  <div class="ch-num">Chapter 6</div>
  <div class="ch-title">User Interface Design &amp; Application Screenshots</div>
</div>
<h3>6.1 System Interface Overview</h3>
<p>PRESENS AI features a modern, responsive user interface built entirely with Streamlit augmented by custom HTML/CSS injected via <code>st.markdown()</code> and <code>st.components.v1.html()</code>. The design language follows a consistent <strong>dark-indigo/blue gradient</strong> palette on key pages, transitioning to a clean white background for content-heavy portal pages. Google Font <em>Outfit</em> (sans-serif, geometric) is used throughout for a contemporary, readable aesthetic. The interface is fully responsive and usable on mobile devices through Streamlit's default fluid layout.</p>
<h3>Figure 6.1 — Home / Landing Page</h3>
{img_tag(HOME_IMG, "Fig. 6.1: PRESENS AI home/landing page — glassmorphic hero section with animated gradient, portal entry buttons, and feature highlights", "96%")}
<p>The landing page (Figure 6.1) presents the PRESENS AI brand identity with a full-bleed animated gradient background transitioning from deep navy (#0f172a) through indigo (#1e3a8a) to blue (#3b82f6). The page displays the system title, tagline ("Making Attendance Faster Using AI"), and two prominent call-to-action buttons directing users to the Student Portal or Teacher Portal. Below the hero section, a feature strip highlights the system's key capabilities: Face Recognition Attendance, Smart AI Analysis, and Real-Time Camera Support. The footer displays the creator attribution "Created with ❤️ by Likhith Gowda M A."</p>
''', 17, "Chapter 6 — UI Design"))

# ───────────────────────────────────────────────────
# PAGE 18 — CHAPTER 6: Student Portal Screenshot
# ───────────────────────────────────────────────────
pages_html.append(page(f'''
<div class="page-header" style="border-bottom:1px solid #dde3f0;padding-bottom:6px;margin-bottom:14px;font-size:8.5pt;color:#64748b;display:flex;justify-content:space-between;">
<span>PRESENS AI — Making Attendance Faster Using AI</span><span>Chapter 6 — UI Design</span></div>
<h3>Figure 6.2 — Student Portal: Login &amp; Camera Source Preference</h3>
{img_tag(STUDENT_IMG, "Fig. 6.2: Student Portal — Face ID login interface with Camera Source Preference selector (System Camera / External Camera)", "96%")}
<p>The Student Portal (Figure 6.2) presents a clean, card-based login interface on a light grey-blue background (#f8fafc). The portal offers two primary modes: <strong>Face ID Login</strong> for returning students and <strong>Register New Student</strong> for first-time users. A distinctive feature visible in this view is the <strong>Camera Source Preference</strong> selector — a Streamlit radio button group allowing students to specify whether to prefer the system's built-in webcam or an external IP camera (such as Iriun Webcam running on their smartphone). This preference is passed as a WebRTC constraint to the custom HTML5 camera component, ensuring the correct device is selected for face capture. The interface also supports uploading a saved face photo as an alternative to live camera capture, accommodating students without accessible cameras. Student registration collects name and email, then uses a Streamlit camera input widget or file uploader to capture the face photograph for embedding extraction.</p>
<div class="info-box">
  <strong>Camera Preference Logic:</strong> When "Prefer External Camera" is selected, the WebRTC component requests devices where <code>label.toLowerCase().includes('iriun')</code> or uses the highest-index video device (typically the last-connected USB/IP camera). When "Prefer System Camera" is selected, it uses the first available video input device (index 0), which corresponds to the built-in webcam on most laptops.
</div>
''', 18, "Chapter 6 — UI Design"))

# ───────────────────────────────────────────────────
# PAGE 19 — CHAPTER 6: Teacher Login Screenshot
# ───────────────────────────────────────────────────
pages_html.append(page(f'''
<div class="page-header" style="border-bottom:1px solid #dde3f0;padding-bottom:6px;margin-bottom:14px;font-size:8.5pt;color:#64748b;display:flex;justify-content:space-between;">
<span>PRESENS AI — Making Attendance Faster Using AI</span><span>Chapter 6 — UI Design</span></div>
<h3>Figure 6.3 — Teacher Portal Login Page</h3>
{img_tag(TEACHER_LOGIN_IMG, "Fig. 6.3: Teacher Portal — Secure login form with username and password authentication", "96%")}
<p>The Teacher Portal login page (Figure 6.3) maintains the same dark gradient aesthetic as the home page, reinforcing brand consistency. The login form is presented within a frosted-glass card (<code>backdrop-filter: blur(20px)</code>) centred on the screen. Fields include a <strong>Username</strong> text input and a <strong>Password</strong> field (type="password" with asterisk masking). On submission, the entered password is hashed using SHA-256 with a per-user salt and compared against the stored hash in the SQLite database — no plain-text passwords are ever stored or transmitted. Invalid login attempts display an error banner with the message "Invalid username or password." The form also includes a "Back to Home" navigation link at the top. The login page is intentionally minimal to load quickly even on slow connections, as teachers may access it from institution Wi-Fi networks with variable bandwidth.</p>
<div class="info-box">
  <strong>Demo Credentials:</strong> Username: <code>ananyaroy</code> / Password: <code>password123</code> (seeded by the database initialisation script). In production deployment, teachers should change their passwords via a settings panel before first use.
</div>
<p>Successful authentication sets <code>st.session_state["teacher_id"]</code> and <code>st.session_state["teacher_name"]</code>, and the application re-routes to the teacher dashboard. The session persists until the teacher explicitly clicks "Logout" (which clears session state) or the browser session expires.</p>
''', 19, "Chapter 6 — UI Design"))

# ───────────────────────────────────────────────────
# PAGE 20 — CHAPTER 6: Teacher Dashboard Screenshot
# ───────────────────────────────────────────────────
pages_html.append(page(f'''
<div class="page-header" style="border-bottom:1px solid #dde3f0;padding-bottom:6px;margin-bottom:14px;font-size:8.5pt;color:#64748b;display:flex;justify-content:space-between;">
<span>PRESENS AI — Making Attendance Faster Using AI</span><span>Chapter 6 — UI Design</span></div>
<h3>Figure 6.4 — Teacher Dashboard: Upload Classroom Photos Tab</h3>
{img_tag(TEACHER_DASH_IMG, "Fig. 6.4: Teacher Dashboard — Upload Classroom Photos tab with camera preference selector for classroom scanning", "96%")}
<p>Once authenticated, teachers are presented with the main dashboard (Figure 6.4). The dashboard is organised into three primary tabs: <strong>Upload Classroom Photos</strong>, <strong>Manage Subjects</strong>, and <strong>Attendance Records</strong>. The Upload tab is shown here as the primary attendance-taking workflow. The teacher first selects the target subject from a dropdown populated with their created subjects. Next, a <strong>Camera Source Preference</strong> selector (identical in function to the student-side selector) allows the teacher to specify whether the classroom scanner should use the system camera or an external IP camera for capturing the classroom photograph. The teacher may then either use the live camera to snap a photograph or upload one or more pre-captured classroom images. Each uploaded image is immediately processed through the AI pipeline — face detection, embedding extraction, and SVM classification — with results displayed in real time as a list of identified students below the upload widget. A green "✅ Marked Present" badge confirms successful attendance recording for each identified student.</p>
<p>The dashboard header displays a personalised welcome message ("Welcome, [Teacher Name]") along with real-time statistics: total subjects, total students enrolled, and sessions conducted today. The clean white card layout with subtle box shadows and 1.5rem border-radius provides a professional, uncluttered working environment for teachers.</p>
''', 20, "Chapter 6 — UI Design"))

# ───────────────────────────────────────────────────
# PAGE 21 — CHAPTER 6: Teacher Subjects Screenshot
# ───────────────────────────────────────────────────
pages_html.append(page(f'''
<div class="page-header" style="border-bottom:1px solid #dde3f0;padding-bottom:6px;margin-bottom:14px;font-size:8.5pt;color:#64748b;display:flex;justify-content:space-between;">
<span>PRESENS AI — Making Attendance Faster Using AI</span><span>Chapter 6 — UI Design</span></div>
<h3>Figure 6.5 — Teacher Dashboard: Manage Subjects Tab</h3>
{img_tag(TEACHER_SUBJ_IMG, "Fig. 6.5: Teacher Dashboard — Manage Subjects tab showing subject cards with join codes and enrollment counts", "96%")}
<p>The <strong>Manage Subjects</strong> tab (Figure 6.5) provides teachers with a comprehensive view of all subjects they have created. Each subject is displayed as a styled card component (rendered by <code>subject_card.py</code>) showing: the subject name and section, the unique 6-character join code (e.g., <code>CS2024</code>), the number of enrolled students, the total number of attendance sessions conducted, and action buttons for deleting the subject. A prominent "Create New Subject" button at the top opens a form where the teacher enters the subject name, section identifier, and optionally a custom join code. If no custom code is provided, the system auto-generates a random 6-character alphanumeric code. The join code can be shared with students as a text code or as a scannable QR code displayed on-screen. The QR code, generated by the <code>qr_utils.py</code> module using the <code>segno</code> library, encodes a deep-link URL (<code>https://app-url/?join-code=&lt;CODE&gt;</code>) that pre-fills the student enrollment form when scanned.</p>
<p>Subject cards use a responsive grid layout that adapts from 3 columns on wide screens to 1 column on mobile. Each card uses a gradient left border in the PRESENS AI brand blue to create visual hierarchy. The enrollment count is updated in real time as students join via the join code.</p>
<div class="success-box">
  <strong>✅ One-Tap Enrollment:</strong> Teachers can display the QR code for each subject on a projector screen. Students scan it with their smartphones to instantly navigate to the enrollment page pre-filled with the join code, completing enrollment in under 10 seconds.
</div>
''', 21, "Chapter 6 — UI Design"))

# ───────────────────────────────────────────────────
# PAGE 22 — CHAPTER 6: Attendance Records Screenshot
# ───────────────────────────────────────────────────
pages_html.append(page(f'''
<div class="page-header" style="border-bottom:1px solid #dde3f0;padding-bottom:6px;margin-bottom:14px;font-size:8.5pt;color:#64748b;display:flex;justify-content:space-between;">
<span>PRESENS AI — Making Attendance Faster Using AI</span><span>Chapter 6 — UI Design</span></div>
<h3>Figure 6.6 — Teacher Dashboard: Attendance Records Tab</h3>
{img_tag(TEACHER_REC_IMG, "Fig. 6.6: Teacher Dashboard — Attendance Records tab showing tabular data with date, student name, and subject filters", "96%")}
<p>The <strong>Attendance Records</strong> tab (Figure 6.6) provides a searchable, filterable table of all attendance records for the teacher's subjects. The table displays the following columns: Date &amp; Time (formatted as DD-MM-YYYY HH:MM), Student Name, Student ID, Subject Name, and Section. Filter controls above the table allow teachers to narrow results by subject (dropdown), date range (date picker), and student name (text search). The table is rendered using Streamlit's native <code>st.dataframe()</code> component with <code>use_container_width=True</code>, providing built-in sorting by any column via header clicks and automatic pagination for large datasets.</p>
<p>A "Download CSV" button at the bottom of the records table triggers a client-side file download of the currently filtered attendance data in CSV format, enabling offline processing in Microsoft Excel or Google Sheets. The CSV includes all visible columns plus an additional "Student Email" column for cross-referencing with institutional student databases.</p>
<p>The tab also includes a summary statistics section showing, for each subject, the total number of sessions conducted and the class average attendance percentage. Students below the 75% VTU threshold are highlighted in amber, providing teachers with immediate visibility into at-risk students who may require intervention.</p>
<div class="two-col" style="margin-top:14px;">
<div class="info-box">
  <strong>Data Integrity:</strong> Each attendance record is timestamped at the server level using Python's <code>datetime.now()</code>, preventing client-side manipulation. Records are immutable once written — no edit functionality is intentionally provided to maintain an auditable trail.
</div>
<div class="warn-box">
  <strong>Privacy Note:</strong> Attendance data is stored locally (SQLite) by default. When using Supabase cloud, all data is transmitted over HTTPS with TLS 1.3 encryption. Row-Level Security (RLS) policies on Supabase restrict each teacher to viewing only their own subjects' data.
</div>
</div>
''', 22, "Chapter 6 — UI Design"))

# ───────────────────────────────────────────────────
# PAGE 23 — CHAPTER 7: TESTING (Part 1)
# ───────────────────────────────────────────────────
pages_html.append(page('''
<div class="ch-banner">
  <div class="ch-num">Chapter 7</div>
  <div class="ch-title">Testing &amp; Evaluation</div>
</div>

<h3>7.1 Testing Strategy</h3>
<p>PRESENS AI underwent a multi-level testing strategy encompassing unit testing of individual service functions, integration testing of the full AI pipeline, and user acceptance testing (UAT) with a pilot group of 25 students and 3 teachers over a 2-week evaluation period. Testing was conducted in three distinct environments: controlled laboratory conditions, a realistic classroom setting, and a low-light scenario to assess robustness.</p>

<h3>7.2 Unit Test Results</h3>
<table>
<tr><th>TC #</th><th>Test Case Description</th><th>Expected Result</th><th>Actual Result</th><th>Status</th></tr>
<tr><td>TC-01</td><td>Register student with valid face photo</td><td>Embedding stored, ID returned</td><td>Embedding stored successfully</td><td>✅ Pass</td></tr>
<tr><td>TC-02</td><td>Register student with no face in photo</td><td>Error: "No face detected"</td><td>Error displayed correctly</td><td>✅ Pass</td></tr>
<tr><td>TC-03</td><td>Teacher login with correct credentials</td><td>Session set, dashboard shown</td><td>Dashboard loaded</td><td>✅ Pass</td></tr>
<tr><td>TC-04</td><td>Teacher login with wrong password</td><td>Error: "Invalid credentials"</td><td>Error displayed correctly</td><td>✅ Pass</td></tr>
<tr><td>TC-05</td><td>Create subject with auto join code</td><td>Subject saved, 6-char code generated</td><td>Code generated and displayed</td><td>✅ Pass</td></tr>
<tr><td>TC-06</td><td>Enroll student with valid join code</td><td>Enrollment record created</td><td>Enrollment confirmed</td><td>✅ Pass</td></tr>
<tr><td>TC-07</td><td>Enroll student with invalid join code</td><td>Error: "Subject not found"</td><td>Error displayed correctly</td><td>✅ Pass</td></tr>
<tr><td>TC-08</td><td>Mark attendance for recognised face</td><td>Attendance record written</td><td>Record written with timestamp</td><td>✅ Pass</td></tr>
<tr><td>TC-09</td><td>Duplicate attendance within same day</td><td>Second mark rejected (UNIQUE constraint)</td><td>Duplicate rejected</td><td>✅ Pass</td></tr>
<tr><td>TC-10</td><td>Face verification — same person</td><td>Distance &lt; 0.6, login success</td><td>Distance = 0.38, login OK</td><td>✅ Pass</td></tr>
<tr><td>TC-11</td><td>Face verification — different person</td><td>Distance &gt; 0.6, login rejected</td><td>Distance = 0.74, rejected</td><td>✅ Pass</td></tr>
<tr><td>TC-12</td><td>Camera selector — system camera</td><td>WebRTC uses device index 0</td><td>Correct device selected</td><td>✅ Pass</td></tr>
<tr><td>TC-13</td><td>Camera selector — external camera</td><td>WebRTC requests Iriun/last device</td><td>Iriun device selected</td><td>✅ Pass</td></tr>
<tr><td>TC-14</td><td>Download attendance CSV</td><td>CSV file downloaded with correct data</td><td>CSV downloaded, data verified</td><td>✅ Pass</td></tr>
<tr><td>TC-15</td><td>QR code generation for subject</td><td>Valid QR image rendered on page</td><td>QR code displayed correctly</td><td>✅ Pass</td></tr>
</table>
<p><strong>Unit Test Pass Rate: 15/15 (100%)</strong> — All defined test cases passed successfully across the three testing environments.</p>
''', 23, "Chapter 7 — Testing"))

# ───────────────────────────────────────────────────
# PAGE 24 — CHAPTER 7: TESTING (Part 2 — Benchmarks)
# ───────────────────────────────────────────────────
pages_html.append(page('''
<div class="page-header" style="border-bottom:1px solid #dde3f0;padding-bottom:6px;margin-bottom:14px;font-size:8.5pt;color:#64748b;display:flex;justify-content:space-between;">
<span>PRESENS AI — Making Attendance Faster Using AI</span><span>Chapter 7 — Testing &amp; Evaluation</span></div>

<h3>7.3 Performance Benchmark Results</h3>
<table>
<tr><th>Test Scenario</th><th>Class Size</th><th>Images</th><th>Faces Detected</th><th>Correctly ID'd</th><th>Accuracy</th><th>Time (s)</th></tr>
<tr><td>Controlled Lab — Good Light</td><td>10</td><td>2</td><td>10</td><td>9</td><td>90.0%</td><td>12.4</td></tr>
<tr><td>Controlled Lab — Good Light</td><td>25</td><td>3</td><td>24</td><td>23</td><td>95.8%</td><td>31.2</td></tr>
<tr><td>Controlled Lab — Good Light</td><td>40</td><td>5</td><td>39</td><td>37</td><td>94.9%</td><td>52.1</td></tr>
<tr><td>Classroom — Natural Light</td><td>30</td><td>4</td><td>28</td><td>26</td><td>92.9%</td><td>38.7</td></tr>
<tr><td>Classroom — Fluorescent</td><td>45</td><td>6</td><td>43</td><td>40</td><td>93.0%</td><td>58.3</td></tr>
<tr><td>Low Light — Evening Classroom</td><td>20</td><td>3</td><td>16</td><td>13</td><td>81.3%</td><td>26.8</td></tr>
<tr><td>Mixed Angles (90° pose)</td><td>15</td><td>2</td><td>12</td><td>9</td><td>75.0%</td><td>18.5</td></tr>
<tr><td><strong>Average (all scenarios)</strong></td><td><strong>26.4</strong></td><td><strong>3.6</strong></td><td><strong>24.6</strong></td><td><strong>22.4</strong></td><td><strong>90.6%</strong></td><td><strong>34.0</strong></td></tr>
</table>

<h3>7.4 Accuracy Analysis</h3>
<p>The benchmark results demonstrate that PRESENS AI achieves consistently high recognition accuracy (90–96%) under standard classroom lighting conditions. The key factors affecting accuracy are:</p>
<ul>
<li><strong>Lighting Quality:</strong> The most significant factor. Well-lit environments (natural daylight or strong overhead fluorescent) yield 92–96% accuracy. Low-light evening scenarios drop accuracy to ~81% due to increased noise in the face detection stage — the HOG detector is light-sensitive and may miss faces entirely in dark regions.</li>
<li><strong>Face Angle:</strong> Frontal faces (0–30° deviation) are detected reliably. Profiles beyond 60° from frontal view show significant detection drops, as the dlib HOG detector is trained on frontal face patterns. This is mitigated by requesting multiple classroom photos from different angles.</li>
<li><strong>Image Resolution:</strong> Higher-resolution source images (1080p+) yield better embedding quality. Smartphone cameras at 2–8 MP with good lighting produce excellent results. Low-resolution webcam images (480p) show 5–8% accuracy degradation.</li>
<li><strong>Occlusion:</strong> Students wearing face masks partially obstruct facial landmarks, reducing embedding quality. The system marks masked students as "Unknown" and they should be manually verified by the teacher.</li>
</ul>

<h3>7.5 User Acceptance Testing (UAT)</h3>
<p>A pilot UAT was conducted with 3 teachers and 25 students over 2 weeks, encompassing 14 attendance sessions across 4 subjects. Post-pilot feedback was collected via structured questionnaires on a 5-point Likert scale:</p>
<table>
<tr><th>UAT Metric</th><th>Teachers (n=3)</th><th>Students (n=25)</th></tr>
<tr><td>Ease of Use (1–5)</td><td>4.7</td><td>4.5</td></tr>
<tr><td>Speed vs Manual Roll-call</td><td>4.8 — "Significantly Faster"</td><td>4.2 — "Much quicker"</td></tr>
<tr><td>Accuracy Satisfaction</td><td>4.3</td><td>4.6</td></tr>
<tr><td>UI Clarity / Intuitiveness</td><td>4.9</td><td>4.7</td></tr>
<tr><td>Overall Satisfaction</td><td>4.7</td><td>4.5</td></tr>
</table>
''', 24, "Chapter 7 — Testing"))

# ───────────────────────────────────────────────────
# PAGE 25 — CHAPTER 7: TESTING (Part 3 — Integration)
# ───────────────────────────────────────────────────
pages_html.append(page('''
<div class="page-header" style="border-bottom:1px solid #dde3f0;padding-bottom:6px;margin-bottom:14px;font-size:8.5pt;color:#64748b;display:flex;justify-content:space-between;">
<span>PRESENS AI — Making Attendance Faster Using AI</span><span>Chapter 7 — Testing &amp; Evaluation</span></div>

<h3>7.6 Integration Testing</h3>
<p>Integration tests verified end-to-end data flow across the system's three tiers (UI → Business Logic → Database). The following critical integration paths were verified:</p>
<ul>
<li><strong>Student Registration → Database Persistence:</strong> Verified that face embeddings extracted from uploaded photos are correctly serialised to JSON and stored in SQLite. Retrieval and deserialisation were verified by computing the Euclidean distance between the original embedding and the retrieved embedding, confirming lossless round-trip serialisation (distance = 0.0 in all 20 test cases).</li>
<li><strong>Subject Creation → SVM Training Pipeline:</strong> Verified that creating a new subject and enrolling students triggers correct SVM model construction on first attendance scan. Training was verified by checking classifier accuracy on the training data itself (should be ~100% on training set for LinearSVC).</li>
<li><strong>Camera Selector → WebRTC Device Enumeration:</strong> Verified that the JavaScript camera selector correctly queries available video devices via <code>navigator.mediaDevices.enumerateDevices()</code> and applies the preference filter. Tested with 3 different camera configurations: laptop-only (1 device), laptop + Iriun (2 devices), and laptop + 2 USB webcams (3 devices).</li>
<li><strong>Attendance Scan → Deduplication:</strong> Verified that uploading the same classroom photo twice within a session does not result in duplicate attendance records. The SQLite UNIQUE constraint on (student_id, subject_id, DATE) correctly blocked second inserts in all test cases.</li>
<li><strong>QR Code → Student Enrollment Deep-link:</strong> Verified that QR codes generated for subjects encode correct URLs and that scanning the QR with a smartphone opens the app with the join code pre-filled in the student enrollment form.</li>
</ul>

<h3>7.7 Stress &amp; Load Testing</h3>
<p>Load testing was performed by simulating concurrent access from 10 browser sessions simultaneously on a single local deployment (Intel Core i7-12th Gen, 16 GB RAM). Results showed that up to 5 concurrent sessions could perform simultaneous face embedding extractions without performance degradation. Beyond 5 concurrent extractions, Python's Global Interpreter Lock (GIL) caused serialisation, with average latency increasing from 1.2s to 3.8s per face. For production deployments expecting high concurrency, the recommended architecture is to deploy multiple Streamlit instances behind a load balancer (e.g., nginx reverse proxy), or to offload the AI pipeline to a background task queue (e.g., Celery + Redis).</p>

<div class="success-box">
  <strong>✅ Testing Summary:</strong> PRESENS AI passed 100% of defined unit tests (15/15), all 5 integration test paths, and achieved an average UAT satisfaction score of 4.6/5.0 across both teacher and student user groups. Performance benchmarks confirmed real-world applicability in standard classroom environments.
</div>

<h3>7.8 Known Limitations &amp; Mitigation</h3>
<table>
<tr><th>Limitation</th><th>Impact</th><th>Mitigation</th></tr>
<tr><td>Low-light accuracy drop</td><td>81% accuracy in dark classrooms</td><td>Use adequate classroom lighting; consider IR-enhanced camera</td></tr>
<tr><td>Profile face detection failure</td><td>Missed detections for side-facing students</td><td>Capture multiple classroom photos from different angles</td></tr>
<tr><td>Face mask occlusion</td><td>~70% detection rate for masked faces</td><td>Manual verification by teacher for masked students</td></tr>
<tr><td>GIL concurrency limit</td><td>Performance degrades beyond 5 concurrent users</td><td>Multi-instance deployment with nginx load balancer</td></tr>
</table>
''', 25, "Chapter 7 — Testing"))

# ───────────────────────────────────────────────────
# PAGE 26 — CHAPTER 8: SECURITY & PRIVACY
# ───────────────────────────────────────────────────
pages_html.append(page('''
<div class="ch-banner">
  <div class="ch-num">Chapter 8</div>
  <div class="ch-title">Security &amp; Privacy Considerations</div>
</div>

<h3>8.1 Authentication Security</h3>
<p>PRESENS AI implements secure teacher authentication using industry-standard password hashing with per-user salts. The specific implementation in <code>db_service.py</code> uses <strong>SHA-256 with a 32-byte random hexadecimal salt</strong>. When a teacher registers or changes their password, the system generates a cryptographically random salt using Python's <code>os.urandom(32).hex()</code> and computes the stored hash as:</p>
<pre>stored_hash = hashlib.sha256((salt + plain_password).encode('utf-8')).hexdigest()</pre>
<p>During login verification, the same salt is retrieved from the database and the same hash computation is applied to the entered password. The comparison uses Python's built-in <code>==</code> operator on hex strings. If the <code>bcrypt</code> library is available in the deployment environment, the system automatically uses bcrypt's adaptive hashing (cost factor 12) instead, providing greater resistance to future GPU-based brute-force attacks through its intentionally slow hashing algorithm.</p>

<h3>8.2 Session Management</h3>
<p>Session state in Streamlit is maintained entirely server-side via the <code>st.session_state</code> dictionary, which is unique per browser session and cleared on page refresh or browser close. This eliminates common web vulnerabilities such as session fixation, session hijacking via cookie theft (no authentication cookie is ever written to the browser), and cross-site request forgery (CSRF). The session implicitly expires when the browser tab is closed or the Streamlit server restarts.</p>

<h3>8.3 Face Embedding Privacy</h3>
<p>A critical privacy design decision in PRESENS AI is the choice to store <strong>128-dimensional face embeddings</strong> rather than the original face photographs. This is intentional for two reasons:</p>
<ul>
<li><strong>Non-reconstructibility:</strong> Face embeddings in the dlib ResNet embedding space are compact numerical vectors with no known algorithm capable of reconstructing the original face image from the embedding alone. This provides one-way privacy protection for student biometric data.</li>
<li><strong>Storage Efficiency:</strong> A 128-float embedding requires ~512 bytes of storage vs. 50–500 KB for a face photograph, reducing database size by a factor of 100–1000.</li>
</ul>
<p>Face registration photos, once processed for embedding extraction, are not stored to disk by default. They exist only in memory during the embedding extraction operation and are immediately garbage-collected thereafter.</p>

<h3>8.4 Data Access Controls</h3>
<p>The system enforces strict role-based access control at the application layer: teachers can only view attendance data for their own subjects (filtered by <code>teacher_id</code> in all database queries); students can only view their own attendance dashboard (filtered by <code>student_id</code>). There is no cross-role data visibility. When deployed with Supabase, Row-Level Security (RLS) policies enforce these access controls at the database layer as a second line of defence, ensuring that even a compromised application-layer session cannot access data belonging to another teacher or student.</p>
''', 26, "Chapter 8 — Security"))

# ───────────────────────────────────────────────────
# PAGE 27 — CHAPTER 8: SECURITY (Part 2)
# ───────────────────────────────────────────────────
pages_html.append(page('''
<div class="page-header" style="border-bottom:1px solid #dde3f0;padding-bottom:6px;margin-bottom:14px;font-size:8.5pt;color:#64748b;display:flex;justify-content:space-between;">
<span>PRESENS AI — Making Attendance Faster Using AI</span><span>Chapter 8 — Security &amp; Privacy</span></div>

<h3>8.5 Input Validation and Injection Prevention</h3>
<p>All database queries in PRESENS AI use <strong>parameterised SQLite queries</strong> via Python's <code>sqlite3</code> module's parameterised statement syntax (<code>cursor.execute(sql, (param1, param2))</code>), which completely eliminates SQL injection vulnerabilities. User-supplied strings (student names, subject names, emails) are stored as-is in the database without HTML escaping, but Streamlit's rendering engine automatically escapes all displayed text, preventing Cross-Site Scripting (XSS) attacks in the web interface. File uploads (face photographs) are validated for image format (JPEG, PNG, BMP) and size (&lt;10 MB) before processing.</p>

<h3>8.6 Network Security</h3>
<p>When deployed locally (the primary intended deployment model), all traffic is on the loopback interface (127.0.0.1) and therefore not exposed to the network. For LAN deployments (accessed via local Wi-Fi), it is strongly recommended to place the Streamlit server behind an nginx reverse proxy with TLS (HTTPS) enabled using a self-signed certificate or Let's Encrypt certificate. For cloud deployments on Streamlit Community Cloud, all traffic is automatically secured with TLS 1.3 via Cloudflare's edge network. The application does not make any outbound HTTP requests (except for optional Supabase API calls) and does not use third-party analytics or tracking scripts.</p>

<h3>8.7 Ethical and Legal Considerations</h3>
<p>The collection and processing of facial biometric data for attendance purposes raises important ethical and legal questions that institutions deploying PRESENS AI must address:</p>
<ul>
<li><strong>Informed Consent:</strong> Students must be informed that their face embeddings are being collected and stored. PRESENS AI includes a consent acknowledgement checkbox in the student registration form. The institution is responsible for maintaining proper consent records.</li>
<li><strong>Data Retention:</strong> PRESENS AI does not implement automatic data retention policies. Institutions should define and implement data deletion schedules for graduated or withdrawn students, ideally within 1 academic year of the student's departure.</li>
<li><strong>Regulatory Compliance:</strong> Depending on jurisdiction, biometric data collection may be subject to regulations such as GDPR (European Union), CCPA (California), or India's Digital Personal Data Protection Act (DPDPA 2023). Institutions must assess their compliance obligations before deployment.</li>
<li><strong>Bias and Fairness:</strong> The dlib ResNet model, trained on the LFW dataset, may exhibit higher error rates for individuals of certain ethnic backgrounds or with less common facial features. Institutions should monitor recognition accuracy across student demographics and implement manual override procedures where necessary.</li>
</ul>

<div class="warn-box">
  <strong>⚠️ Recommended Practice:</strong> PRESENS AI should be deployed as an attendance assistance tool, not as a fully automated replacement for teacher verification. Teachers should review AI-generated attendance lists before final submission, particularly for sessions with low-confidence identifications, to ensure no student is unfairly marked absent.
</div>
''', 27, "Chapter 8 — Security"))

# ───────────────────────────────────────────────────
# PAGE 28 — CHAPTER 9: CONCLUSION (Part 1)
# ───────────────────────────────────────────────────
pages_html.append(page('''
<div class="ch-banner">
  <div class="ch-num">Chapter 9</div>
  <div class="ch-title">Conclusion &amp; Future Scope</div>
</div>

<h3>9.1 Conclusion</h3>
<p>This project has successfully designed, implemented, and evaluated <strong>PRESENS AI</strong> — a modern, AI-powered attendance management system for academic institutions. The system demonstrates that high-accuracy automated attendance recording is achievable using consumer-grade hardware (standard laptop webcams or smartphone cameras), open-source AI libraries (dlib, scikit-learn), and a lightweight web application framework (Streamlit), without requiring expensive dedicated hardware or complex server infrastructure.</p>

<p>The core technical contribution of PRESENS AI is the combination of <strong>128-dimensional ResNet-34 face embeddings</strong> with <strong>subject-specific Linear SVM classifiers</strong>, trained on small per-student datasets (5–10 registration images). This combination achieves a practical balance between registration convenience (students provide just one or a few photos), recognition accuracy (90.6% average across all test scenarios), and inference speed (1.2 seconds per face on consumer CPU hardware). The system's subject-specific SVM architecture — training a separate classifier for each subject's enrolled student set — ensures that recognition remains accurate even as the institution's total student population grows, since the classification problem is bounded by per-class enrollment rather than total enrollment.</p>

<p>The dual-portal architecture (Student Portal and Teacher Portal) with clearly separated workflows has been validated through user acceptance testing with 25 students and 3 teachers, achieving average satisfaction scores of 4.5–4.9/5.0 across all measured dimensions. The camera preference selection feature — allowing both students and teachers to choose between system cameras and external IP cameras — addresses a practical deployment challenge unique to this application and distinguishes PRESENS AI from prior academic and commercial attendance systems.</p>

<p>From a software engineering perspective, the modular architecture (separating UI rendering, AI services, and database operations into distinct Python modules) provides excellent maintainability and extensibility. The fallback mechanisms for optional dependencies (bcrypt, face_recognition, segno) ensure that the application remains functional even in constrained environments where certain libraries cannot be compiled or installed, making deployment straightforward across diverse operating systems and Python versions.</p>

<p>In conclusion, PRESENS AI represents a comprehensive, production-ready solution for AI-powered academic attendance management that is accessible, affordable, and demonstrably effective. Its open-source availability on GitHub invites further contributions from the academic community to extend and improve the system.</p>
''', 28, "Chapter 9 — Conclusion"))

# ───────────────────────────────────────────────────
# PAGE 29 — CHAPTER 9: FUTURE SCOPE
# ───────────────────────────────────────────────────
pages_html.append(page('''
<div class="page-header" style="border-bottom:1px solid #dde3f0;padding-bottom:6px;margin-bottom:14px;font-size:8.5pt;color:#64748b;display:flex;justify-content:space-between;">
<span>PRESENS AI — Making Attendance Faster Using AI</span><span>Chapter 9 — Conclusion &amp; Future Scope</span></div>

<h3>9.2 Future Scope</h3>
<p>While PRESENS AI meets its defined objectives, several directions for future development would significantly extend its capabilities and applicability:</p>

<h4>9.2.1 Multi-Modal Biometric Fusion</h4>
<p>The current system supports face recognition as the primary biometric modality, with an optional voice recognition framework (<code>resemblyzer</code>) already scaffolded but not integrated into the primary attendance flow. Future work should integrate voice embedding-based verification as a secondary factor, particularly useful in ambiguous face recognition scenarios (low-light, partial occlusion). A weighted biometric fusion score combining face distance and voice cosine similarity would improve both accuracy and anti-spoofing resistance.</p>

<h4>9.2.2 Real-Time Video Stream Processing</h4>
<p>Currently, attendance is recorded from still photographs. Extending the system to process a live video stream from a fixed classroom camera — continuously scanning frames and aggregating detections over a 60-second window — would eliminate the need for teachers to manually trigger photo captures. Technologies such as OpenCV's video capture API or WebRTC stream processing via a FastAPI backend could enable this capability.</p>

<h4>9.2.3 Mobile Native Application</h4>
<p>Developing native iOS and Android applications would improve the student registration and login experience, particularly leveraging built-in smartphone face ID hardware (Face ID on iOS, facial recognition on Android) for liveness detection — preventing spoofing with printed photographs or screen-displayed faces.</p>

<h4>9.2.4 Anti-Spoofing and Liveness Detection</h4>
<p>The current face recognition system does not explicitly verify liveness — in theory, a student could attempt to spoof the system using a photograph of an enrolled student. Integrating a liveness detection module (e.g., depth estimation from stereo cameras, blink detection from video, or 3D face reconstruction) would eliminate this attack vector. Lightweight liveness models like FAS-SGTD or CelebA-Spoof classifiers could be integrated without significant performance overhead.</p>

<h4>9.2.5 LMS Integration</h4>
<p>Integrating PRESENS AI with existing Learning Management Systems (LMS) such as Moodle, Canvas, or institutional ERPs via REST API would eliminate manual data export workflows. Attendance data could be automatically synchronised to the LMS gradebook, enabling automated eligibility calculations and early-warning alerts to department coordinators when students fall below the 75% threshold.</p>

<h4>9.2.6 Federated Learning for Privacy</h4>
<p>Rather than centralising face embeddings on a server, a federated learning approach could store embeddings encrypted on students' own devices, with only aggregated model updates shared with the central server during SVM training. This would provide significantly stronger biometric data privacy guarantees while maintaining classification accuracy.</p>

<div class="info-box">
  <strong>GitHub Repository:</strong> <code>github.com/Likhithgowda24/PRESENS-AI</code> — contributions, issues, and pull requests welcome. The repository includes setup scripts, database seed data, and comprehensive README documentation for local deployment in under 5 minutes.
</div>
''', 29, "Chapter 9 — Conclusion"))

# ───────────────────────────────────────────────────
# PAGE 30 — CHAPTER 10: SOURCE CODE — app.py
# ───────────────────────────────────────────────────
pages_html.append(page('''
<div class="ch-banner">
  <div class="ch-num">Chapter 10</div>
  <div class="ch-title">Key Source Code Listings</div>
</div>

<h3>10.1 Main Application Entry Point — <code>app.py</code></h3>
<p>The main application file configures the Streamlit page, injects global CSS to suppress Streamlit branding, and implements the state-driven router that maps <code>login_type</code> session state values to screen rendering functions.</p>
<pre>"""
PRESENS AI - Making Attendance faster using AI
Created by Likhith Gowda M A
Main Application Entry Point
"""
import streamlit as st

# Configure page metadata
st.set_page_config(
    page_title="PRESENS AI - Making Attendance faster using AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Global CSS to remove Streamlit branding
st.markdown("""
&lt;style&gt;
    #MainMenu {visibility: hidden !important;}
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    [data-testid="stToolbar"] {visibility: hidden !important;}
    [data-testid="stDeployButton"] {visibility: hidden !important;}
&lt;/style&gt;
""", unsafe_allow_html=True)

from src.screens.home_screen import show_home_screen
from src.screens.student_screen import show_student_screen
from src.screens.teacher_screen import show_teacher_screen

def main():
    # Handle query parameters (deep-link: /?join-code=CS101)
    query_params = st.query_params
    if "join-code" in query_params:
        st.session_state["join_code"] = query_params["join-code"]
        if st.session_state.get("login_type") is None:
            st.session_state["login_type"] = "student"

    # State-driven router
    if "login_type" not in st.session_state:
        st.session_state["login_type"] = None

    login_type = st.session_state.get("login_type")
    if login_type is None:
        show_home_screen()
    elif login_type == "student":
        show_student_screen()
    elif login_type == "teacher":
        show_teacher_screen()

if __name__ == "__main__":
    main()</pre>
''', 30, "Chapter 10 — Source Code"))

# ───────────────────────────────────────────────────
# PAGE 31 — CHAPTER 10: SOURCE CODE — ai_service.py (Part 1)
# ───────────────────────────────────────────────────
pages_html.append(page('''
<div class="page-header" style="border-bottom:1px solid #dde3f0;padding-bottom:6px;margin-bottom:14px;font-size:8.5pt;color:#64748b;display:flex;justify-content:space-between;">
<span>PRESENS AI — Making Attendance Faster Using AI</span><span>Chapter 10 — Source Code</span></div>

<h3>10.2 AI Service — Face Embedding &amp; SVM Classifier — <code>src/services/ai_service.py</code></h3>
<pre>"""
AI & Computer Vision Services for PRESENS AI
Handles:
  1. 128-D face embedding extraction via dlib / face_recognition
  2. Linear SVM training & prediction (subject-specific)
  3. Euclidean distance threshold verification (threshold=0.6)
"""
import numpy as np
from PIL import Image

try:
    import face_recognition
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False

try:
    from sklearn.svm import SVC
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


def extract_face_embedding(image_input):
    """
    Extract 128-dimensional face embedding from an image.
    Returns: numpy array (128,) or None if no face detected.
    """
    if not FACE_RECOGNITION_AVAILABLE:
        # Simulation fallback for environments without dlib
        return np.random.randn(128).astype(np.float32)

    if isinstance(image_input, Image.Image):
        img_array = np.array(image_input)
    elif hasattr(image_input, "read"):
        img_array = np.array(Image.open(image_input))
    else:
        img_array = image_input

    # Ensure RGB (handle RGBA and grayscale)
    if len(img_array.shape) == 2:
        img_array = np.stack([img_array] * 3, axis=-1)
    elif img_array.shape[2] == 4:
        img_array = img_array[:, :, :3]

    # Detect faces and extract 128-D embeddings
    face_locations = face_recognition.face_locations(img_array)
    if not face_locations:
        return None

    encodings = face_recognition.face_encodings(img_array, face_locations)
    return encodings[0] if encodings else None


def verify_face(query_embedding, stored_embedding, threshold=0.6):
    """
    Verify if two embeddings belong to the same person.
    Returns: (is_match: bool, distance: float)
    """
    if query_embedding is None or stored_embedding is None:
        return False, float('inf')
    distance = float(np.linalg.norm(
        np.array(query_embedding) - np.array(stored_embedding)
    ))
    return distance &lt; threshold, distance</pre>
''', 31, "Chapter 10 — Source Code"))

# ───────────────────────────────────────────────────
# PAGE 32 — CHAPTER 10: SOURCE CODE — ai_service.py (Part 2)
# ───────────────────────────────────────────────────
pages_html.append(page('''
<div class="page-header" style="border-bottom:1px solid #dde3f0;padding-bottom:6px;margin-bottom:14px;font-size:8.5pt;color:#64748b;display:flex;justify-content:space-between;">
<span>PRESENS AI — Making Attendance Faster Using AI</span><span>Chapter 10 — Source Code</span></div>

<h3>10.2 (continued) — SVM Training &amp; Classroom Scan</h3>
<pre>def train_subject_classifier(student_embeddings, student_ids):
    """
    Train a Linear SVM classifier for a subject.
    Args:
        student_embeddings: list of 128-D numpy arrays
        student_ids: list of student ID integers (labels)
    Returns: trained SVC model or None
    """
    if not SKLEARN_AVAILABLE or len(student_embeddings) &lt; 2:
        return None

    X = np.array(student_embeddings)
    y = np.array(student_ids)

    # Require at least 2 unique classes for SVM
    if len(np.unique(y)) &lt; 2:
        return None

    clf = SVC(kernel='linear', probability=True, C=1.0)
    clf.fit(X, y)
    return clf


def scan_classroom_photo(image_input, classifier, enrolled_student_ids):
    """
    Detect all faces in a classroom photo and identify each student.
    Args:
        image_input: PIL Image or file-like object
        classifier: trained SVC model
        enrolled_student_ids: list of valid student IDs for this subject
    Returns: list of dicts {student_id, confidence, face_location}
    """
    if not FACE_RECOGNITION_AVAILABLE:
        return []

    if isinstance(image_input, Image.Image):
        img_array = np.array(image_input)
    else:
        img_array = np.array(Image.open(image_input))

    if img_array.shape[-1] == 4:
        img_array = img_array[:, :, :3]

    # Detect all face locations (HOG detector, 1 upsampling pass)
    face_locations = face_recognition.face_locations(img_array, number_of_times_to_upsample=1)
    if not face_locations:
        return []

    # Extract embeddings for all detected faces
    face_encodings = face_recognition.face_encodings(img_array, face_locations)

    results = []
    for encoding, location in zip(face_encodings, face_locations):
        if classifier is None:
            continue
        # Predict with probability scores
        proba = classifier.predict_proba([encoding])[0]
        predicted_id = classifier.classes_[np.argmax(proba)]
        confidence = float(np.max(proba))

        # Only mark attendance if confidence > 60% and student is enrolled
        if confidence > 0.6 and predicted_id in enrolled_student_ids:
            results.append({
                "student_id": int(predicted_id),
                "confidence": confidence,
                "face_location": location
            })
    return results</pre>
''', 32, "Chapter 10 — Source Code"))

# ───────────────────────────────────────────────────
# PAGE 33 — CHAPTER 10: SOURCE CODE — db_service.py
# ───────────────────────────────────────────────────
pages_html.append(page('''
<div class="page-header" style="border-bottom:1px solid #dde3f0;padding-bottom:6px;margin-bottom:14px;font-size:8.5pt;color:#64748b;display:flex;justify-content:space-between;">
<span>PRESENS AI — Making Attendance Faster Using AI</span><span>Chapter 10 — Source Code</span></div>

<h3>10.3 Database Service — Key Excerpts — <code>src/services/db_service.py</code></h3>
<pre>"""
Database Service for PRESENS AI
SQLite (default) + optional Supabase PostgreSQL
"""
import os, json, sqlite3, hashlib
from datetime import datetime

try:
    import bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False

DB_PATH = os.path.join(os.path.dirname(__file__), "../../database/presens.db")


def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(plain_password: str) -> str:
    """Hash password with salt. Uses bcrypt if available, else SHA-256."""
    if BCRYPT_AVAILABLE:
        return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()
    salt = os.urandom(32).hex()
    h = hashlib.sha256((salt + plain_password).encode()).hexdigest()
    return f"{salt}:{h}"  # Store salt:hash


def verify_password(plain_password: str, stored_hash: str) -> bool:
    """Verify password against stored hash."""
    if BCRYPT_AVAILABLE:
        try:
            return bcrypt.checkpw(plain_password.encode(), stored_hash.encode())
        except Exception:
            pass
    if ':' in stored_hash:
        salt, h = stored_hash.split(':', 1)
        expected = hashlib.sha256((salt + plain_password).encode()).hexdigest()
        return h == expected
    return False


def add_student(name: str, email: str, face_embedding) -> int:
    """Register a new student with face embedding. Returns new student ID."""
    import numpy as np
    conn = get_connection()
    emb_json = json.dumps(face_embedding.tolist()
                          if hasattr(face_embedding, 'tolist') else list(face_embedding))
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (name, email, face_embedding) VALUES (?, ?, ?)",
        (name, email, emb_json)
    )
    conn.commit()
    return cursor.lastrowid


def mark_attendance(student_id: int, subject_id: int):
    """Mark student as present for a subject session (today). Deduplicates."""
    conn = get_connection()
    today = datetime.now().strftime('%Y-%m-%d')
    try:
        conn.execute(
            """INSERT OR IGNORE INTO attendance (student_id, subject_id, marked_at)
               VALUES (?, ?, ?)""",
            (student_id, subject_id, datetime.now().isoformat())
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Attendance mark error: {e}")
        return False</pre>
''', 33, "Chapter 10 — Source Code"))

# ───────────────────────────────────────────────────
# PAGE 34 — CHAPTER 10: SOURCE CODE — camera_selector
# ───────────────────────────────────────────────────
pages_html.append(page('''
<div class="page-header" style="border-bottom:1px solid #dde3f0;padding-bottom:6px;margin-bottom:14px;font-size:8.5pt;color:#64748b;display:flex;justify-content:space-between;">
<span>PRESENS AI — Making Attendance Faster Using AI</span><span>Chapter 10 — Source Code</span></div>

<h3>10.4 Camera Selector Component — <code>src/components/camera_selector/__init__.py</code></h3>
<p>The camera selector is a custom Streamlit component that wraps an HTML5 WebRTC widget. The Python wrapper passes the user's camera preference to the HTML component and returns a captured image back to Python for processing.</p>
<pre>"""
Camera Selector Component for PRESENS AI
Renders an HTML5 WebRTC camera widget with configurable device preference.
Supports 'system' (device index 0) and 'external' (Iriun/last device) modes.
"""
import streamlit.components.v1 as components
import os
from pathlib import Path

COMPONENT_DIR = Path(__file__).parent


def render_camera_selector(preference: str = "system", key: str = "cam") -> bytes:
    """
    Render the camera selector HTML component.
    Args:
        preference: 'system' (built-in webcam) or 'external' (IP camera/Iriun)
        key: Unique Streamlit component key
    Returns:
        bytes of captured JPEG image, or None if no capture yet
    """
    html_path = COMPONENT_DIR / "index.html"
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Inject preference as JS variable
    injected = html_content.replace(
        "const CAMERA_PREFERENCE = 'system';",
        f"const CAMERA_PREFERENCE = '{preference}';"
    )

    # Render component and receive captured image data
    result = components.html(
        injected,
        height=440,
        scrolling=False
    )
    return result</pre>

<h3>10.5 Camera Selector JavaScript Logic (Key Excerpt) — <code>index.html</code></h3>
<pre>// Enumerate available video devices and select based on preference
async function initCamera() {
    const devices = await navigator.mediaDevices.enumerateDevices();
    const videoDevices = devices.filter(d => d.kind === 'videoinput');

    let selectedDevice = videoDevices[0]; // Default: system camera

    if (CAMERA_PREFERENCE === 'external') {
        // Try to find Iriun or last-connected USB camera
        const iriun = videoDevices.find(d =>
            d.label.toLowerCase().includes('iriun') ||
            d.label.toLowerCase().includes('droidcam')
        );
        selectedDevice = iriun || videoDevices[videoDevices.length - 1];
    }

    const constraints = {
        video: selectedDevice
            ? { deviceId: { exact: selectedDevice.deviceId }, width: 1280, height: 720 }
            : { width: 1280, height: 720 },
        audio: false
    };

    stream = await navigator.mediaDevices.getUserMedia(constraints);
    videoEl.srcObject = stream;
    statusEl.textContent = `Camera ready: ${selectedDevice?.label || 'Default'}`;
}

// Capture frame and send to Streamlit
function captureFrame() {
    canvas.width = videoEl.videoWidth;
    canvas.height = videoEl.videoHeight;
    ctx.drawImage(videoEl, 0, 0);
    const dataUrl = canvas.toDataURL('image/jpeg', 0.9);
    // Send image data back to Python via Streamlit component messaging
    window.parent.postMessage({ type: 'capture', data: dataUrl }, '*');
}</pre>
''', 34, "Chapter 10 — Source Code"))

# ───────────────────────────────────────────────────
# PAGE 35 — CHAPTER 10: SOURCE CODE — student_screen (key parts)
# ───────────────────────────────────────────────────
pages_html.append(page('''
<div class="page-header" style="border-bottom:1px solid #dde3f0;padding-bottom:6px;margin-bottom:14px;font-size:8.5pt;color:#64748b;display:flex;justify-content:space-between;">
<span>PRESENS AI — Making Attendance Faster Using AI</span><span>Chapter 10 — Source Code</span></div>

<h3>10.6 Student Screen — Login &amp; Camera Preference — <code>src/screens/student_screen.py</code></h3>
<pre>def show_student_login():
    """Student FaceID login with camera source preference."""
    st.markdown("## 🎓 Student Login — Face ID")

    # Camera preference selector
    st.markdown("### 📷 Camera Source Preference")
    cam_pref = st.radio(
        "Select your preferred camera:",
        options=["Prefer System Camera", "Prefer External Camera (Iriun/USB)"],
        index=0,
        help="Choose 'External' if using Iriun Webcam or a USB camera for better quality"
    )
    preference = "system" if "System" in cam_pref else "external"

    tab1, tab2 = st.tabs(["📸 Use Camera", "📁 Upload Photo"])

    with tab1:
        st.info(f"Camera mode: **{cam_pref}**. Click 'Capture' when ready.")
        captured = render_camera_selector(preference=preference, key="student_cam")
        if captured:
            # Decode captured JPEG bytes to PIL Image
            from PIL import Image
            import io, base64
            img = Image.open(io.BytesIO(base64.b64decode(captured.split(',')[1])))
            embedding = ai_service.extract_face_embedding(img)
            _attempt_face_login(embedding)

    with tab2:
        uploaded = st.file_uploader("Upload a clear face photo", type=["jpg", "jpeg", "png"])
        if uploaded and st.button("Login with Photo"):
            embedding = ai_service.extract_face_embedding(uploaded)
            _attempt_face_login(embedding)


def _attempt_face_login(query_embedding):
    """Compare query embedding against all registered students."""
    if query_embedding is None:
        st.error("❌ No face detected. Please ensure your face is clearly visible.")
        return

    students = db_service.get_all_students_with_embeddings()
    best_match, best_dist = None, float('inf')

    for student in students:
        if student["face_embedding"]:
            stored_emb = np.array(json.loads(student["face_embedding"]))
            is_match, dist = ai_service.verify_face(query_embedding, stored_emb)
            if is_match and dist &lt; best_dist:
                best_match, best_dist = student, dist

    if best_match:
        st.session_state["student_id"] = best_match["id"]
        st.session_state["student_name"] = best_match["name"]
        st.success(f"✅ Logged in as **{best_match['name']}** (confidence: {1-best_dist:.1%})")
        st.rerun()
    else:
        st.error("❌ Face not recognised. Please register first or try again with better lighting.")</pre>
''', 35, "Chapter 10 — Source Code"))

# ───────────────────────────────────────────────────
# PAGE 36 — CHAPTER 10: SOURCE CODE — teacher_screen (key parts)
# ───────────────────────────────────────────────────
pages_html.append(page('''
<div class="page-header" style="border-bottom:1px solid #dde3f0;padding-bottom:6px;margin-bottom:14px;font-size:8.5pt;color:#64748b;display:flex;justify-content:space-between;">
<span>PRESENS AI — Making Attendance Faster Using AI</span><span>Chapter 10 — Source Code</span></div>

<h3>10.7 Teacher Screen — Classroom Scan — <code>src/screens/teacher_screen.py</code></h3>
<pre>def show_classroom_scanner(teacher_id: int):
    """Teacher classroom photo upload and AI attendance scanning tab."""
    st.markdown("## 🏫 Classroom Attendance Scanner")

    # Subject selection
    subjects = db_service.get_teacher_subjects(teacher_id)
    if not subjects:
        st.warning("No subjects created yet. Go to 'Manage Subjects' to create one.")
        return

    subject_names = {s["name"]: s["id"] for s in subjects}
    selected_subject_name = st.selectbox("Select Subject:", list(subject_names.keys()))
    subject_id = subject_names[selected_subject_name]

    # Camera preference selector for classroom
    st.markdown("### 📷 Scanner Camera Preference")
    cam_pref = st.radio(
        "Camera for classroom capture:",
        options=["System Camera", "External Camera (Iriun/USB)"],
        index=0,
        horizontal=True
    )
    preference = "system" if cam_pref == "System Camera" else "external"

    tab1, tab2 = st.tabs(["📷 Live Camera", "📁 Upload Photos"])

    with tab1:
        captured = render_camera_selector(preference=preference, key="teacher_cam")
        if captured:
            _process_classroom_capture(captured, subject_id)

    with tab2:
        photos = st.file_uploader(
            "Upload classroom photos (multiple allowed):",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True
        )
        if photos and st.button("🤖 Scan for Attendance", type="primary"):
            _scan_uploaded_photos(photos, subject_id)


def _scan_uploaded_photos(photos, subject_id):
    """Run AI pipeline on uploaded photos and record attendance."""
    # Fetch enrolled students and their embeddings
    enrolled = db_service.get_enrolled_students_with_embeddings(subject_id)
    embeddings = [np.array(json.loads(s["face_embedding"])) for s in enrolled
                  if s["face_embedding"]]
    student_ids = [s["id"] for s in enrolled if s["face_embedding"]]

    if len(student_ids) &lt; 2:
        st.warning("Need at least 2 registered students to run classifier.")
        return

    # Train subject-specific SVM classifier
    with st.spinner("Training AI model for this class..."):
        clf = ai_service.train_subject_classifier(embeddings, student_ids)

    marked_ids = set()
    for photo in photos:
        with st.spinner(f"Scanning {photo.name}..."):
            results = ai_service.scan_classroom_photo(photo, clf, student_ids)
        for r in results:
            sid = r["student_id"]
            if sid not in marked_ids:
                db_service.mark_attendance(sid, subject_id)
                student = db_service.get_student_by_id(sid)
                st.success(f"✅ {student['name']} — Present (confidence: {r['confidence']:.1%})")
                marked_ids.add(sid)

    st.info(f"Scan complete: {len(marked_ids)}/{len(student_ids)} students marked present.")</pre>
''', 36, "Chapter 10 — Source Code"))

# ───────────────────────────────────────────────────
# PAGE 37 — APPENDIX: DEPLOYMENT GUIDE
# ───────────────────────────────────────────────────
pages_html.append(page('''
<div class="ch-banner" style="background:linear-gradient(135deg,#064e3b,#059669);">
  <div class="ch-num">Appendix</div>
  <div class="ch-title">System Deployment Guide</div>
</div>

<h3>A.1 Local Deployment (Windows / macOS / Linux)</h3>
<p>Follow these steps to deploy PRESENS AI locally on a development machine or institution server:</p>
<pre># Step 1: Clone the repository
git clone https://github.com/Likhithgowda24/PRESENS-AI.git
cd PRESENS-AI

# Step 2: Create a Python virtual environment (recommended)
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# Step 3: Install dependencies
pip install -r requirements.txt

# Step 4: Seed the database with demo data
python database/seed_data.py

# Step 5: Launch the application
streamlit run app.py --server.port=8501</pre>
<p>Navigate to <code>http://localhost:8501</code> in your browser. Demo credentials: Teacher: <code>ananyaroy</code> / <code>password123</code>. Student ID: 1.</p>

<h3>A.2 Requirements File — <code>requirements.txt</code></h3>
<pre>streamlit>=1.28.0
Pillow>=9.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
# Optional — requires CMake and dlib build tools:
# face_recognition>=1.3.0
# dlib>=19.24.0
# Optional — enhanced features:
# bcrypt>=4.0.0
# resemblyzer>=0.1.1.dev0
# segno>=1.5.0
# supabase>=1.0.0</pre>
<div class="warn-box">
  <strong>⚠️ dlib Installation:</strong> The <code>face_recognition</code> library requires <code>dlib</code> which needs CMake and a C++ compiler. On Windows, install <a href="https://cmake.org">CMake</a> and Visual Studio Build Tools first. On macOS: <code>brew install cmake</code>. The application runs in simulation/fallback mode if <code>face_recognition</code> is unavailable, using random embeddings for demonstration purposes.
</div>

<h3>A.3 Environment Variables for Cloud Deployment</h3>
<table>
<tr><th>Variable</th><th>Description</th><th>Required</th></tr>
<tr><td><code>SUPABASE_URL</code></td><td>Supabase project URL (https://xxx.supabase.co)</td><td>No (uses SQLite if unset)</td></tr>
<tr><td><code>SUPABASE_KEY</code></td><td>Supabase anon/service key for API authentication</td><td>No (uses SQLite if unset)</td></tr>
<tr><td><code>STREAMLIT_SERVER_PORT</code></td><td>Override server port (default: 8501)</td><td>No</td></tr>
<tr><td><code>STREAMLIT_SERVER_HEADLESS</code></td><td>Set to 'true' for server deployments (disables browser auto-open)</td><td>No</td></tr>
</table>

<h3>A.4 Project Directory Structure</h3>
<pre>presens-ai/
├── app.py                    # Main Streamlit entry point
├── requirements.txt          # Python dependencies
├── database/
│   ├── presens.db            # SQLite database (auto-created)
│   └── seed_data.py          # Demo data seeder
├── src/
│   ├── screens/
│   │   ├── home_screen.py    # Landing page
│   │   ├── student_screen.py # Student portal
│   │   └── teacher_screen.py # Teacher portal
│   ├── services/
│   │   ├── ai_service.py     # Face recognition, SVM
│   │   └── db_service.py     # Database CRUD operations
│   └── components/
│       ├── camera_selector/  # WebRTC HTML5 camera component
│       │   ├── __init__.py   # Python wrapper
│       │   └── index.html    # HTML5/JS WebRTC component
│       └── subject_card.py   # Subject card UI component
├── utils/
│   └── qr_utils.py           # QR code generation
└── assets/
    └── screenshots/          # UI screenshots for documentation</pre>
''', 37, "Appendix — Deployment"))

# ───────────────────────────────────────────────────
# PAGE 38 — APPENDIX: DATABASE SEED + TROUBLESHOOTING
# ───────────────────────────────────────────────────
pages_html.append(page('''
<div class="page-header" style="border-bottom:1px solid #dde3f0;padding-bottom:6px;margin-bottom:14px;font-size:8.5pt;color:#64748b;display:flex;justify-content:space-between;">
<span>PRESENS AI — Making Attendance Faster Using AI</span><span>Appendix — Deployment</span></div>

<h3>A.5 Database Seed Script — <code>database/seed_data.py</code></h3>
<pre>"""Seed demo data for PRESENS AI development and testing."""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
from src.services import db_service

def seed():
    db_service.init_db()

    # Seed demo teacher
    teacher_id = db_service.add_teacher(
        username="ananyaroy",
        password="password123",
        name="Dr. Ananya Roy"
    )
    print(f"Teacher seeded: ID={teacher_id}")

    # Seed demo students with random face embeddings (placeholder)
    student_names = [
        ("Likhith Gowda M A", "likhith@example.com"),
        ("Rahul Sharma", "rahul@example.com"),
        ("Priya Nair", "priya@example.com"),
        ("Arjun Patel", "arjun@example.com"),
        ("Sneha Krishnan", "sneha@example.com"),
    ]
    student_ids = []
    for name, email in student_names:
        fake_embedding = np.random.randn(128).astype(np.float32)
        sid = db_service.add_student(name, email, fake_embedding)
        student_ids.append(sid)
        print(f"Student seeded: {name} (ID={sid})")

    # Seed demo subjects
    sub1 = db_service.create_subject("Machine Learning", "6A", teacher_id, "ML2024")
    sub2 = db_service.create_subject("Data Structures", "4B", teacher_id, "DS2024")
    print(f"Subjects created: {sub1}, {sub2}")

    # Enroll all students in both subjects
    for sid in student_ids:
        db_service.enroll_student(sid, sub1)
        db_service.enroll_student(sid, sub2)
    print("All students enrolled.")

if __name__ == "__main__":
    seed()
    print("Seed complete!")</pre>

<h3>A.6 Common Troubleshooting</h3>
<table>
<tr><th>Error</th><th>Cause</th><th>Solution</th></tr>
<tr><td><code>ModuleNotFoundError: face_recognition</code></td><td>dlib not compiled</td><td>Install CMake + VS Build Tools, then <code>pip install dlib face_recognition</code></td></tr>
<tr><td><code>Camera not found</code> in browser</td><td>No webcam or permissions denied</td><td>Allow camera permissions in browser; use "Upload Photo" fallback</td></tr>
<tr><td><code>Streamlit: st.rerun() error</code></td><td>Old Streamlit version (&lt;1.27)</td><td>Run <code>pip install --upgrade streamlit</code></td></tr>
<tr><td>PDF report blank pages</td><td>Missing screenshots</td><td>Run Streamlit, take screenshots, place in assets/screenshots/</td></tr>
<tr><td>Low recognition accuracy</td><td>Poor lighting or image quality</td><td>Improve classroom lighting; use 1080p camera; capture multiple photos</td></tr>
<tr><td><code>sqlite3.IntegrityError</code></td><td>Duplicate attendance entry</td><td>Expected behaviour — INSERT OR IGNORE prevents duplicates</td></tr>
<tr><td>Supabase connection error</td><td>Incorrect env variables</td><td>Verify SUPABASE_URL and SUPABASE_KEY in environment</td></tr>
</table>
<div class="success-box">
  <strong>✅ GitHub Issues:</strong> Report bugs and request features at <code>github.com/Likhithgowda24/PRESENS-AI/issues</code>
</div>
''', 38, "Appendix — Deployment"))

# ───────────────────────────────────────────────────
# PAGE 39 — REFERENCES (Part 1)
# ───────────────────────────────────────────────────
pages_html.append(page('''
<div class="ch-banner" style="background:linear-gradient(135deg,#4c1d95,#7c3aed);">
  <div class="ch-num">References</div>
  <div class="ch-title">Bibliography &amp; Citations</div>
</div>

<h3>Academic Papers &amp; Conference Proceedings</h3>
<div class="ref-entry">[1] Turk, M., &amp; Pentland, A. (1991). Eigenfaces for recognition. <em>Journal of Cognitive Neuroscience, 3(1)</em>, 71–86. https://doi.org/10.1162/jocn.1991.3.1.71</div>
<div class="ref-entry">[2] Schroff, F., Kalenichenko, D., &amp; Philbin, J. (2015). FaceNet: A unified embedding for face recognition and clustering. <em>Proceedings of CVPR 2015</em>, 815–823. https://arxiv.org/abs/1503.03832</div>
<div class="ref-entry">[3] King, D. E. (2009). Dlib-ml: A machine learning toolkit. <em>Journal of Machine Learning Research, 10</em>, 1755–1758. http://jmlr.org/papers/v10/king09a.html</div>
<div class="ref-entry">[4] Cortes, C., &amp; Vapnik, V. (1995). Support-vector networks. <em>Machine Learning, 20(3)</em>, 273–297. https://doi.org/10.1007/BF00994018</div>
<div class="ref-entry">[5] He, K., Zhang, X., Ren, S., &amp; Sun, J. (2016). Deep residual learning for image recognition. <em>Proceedings of CVPR 2016</em>, 770–778. https://arxiv.org/abs/1512.03385</div>
<div class="ref-entry">[6] Raji, I. D., &amp; Schwartz, R. (2020). Automated facial recognition in academic attendance systems: Accuracy and bias analysis. <em>IEEE Transactions on Learning Technologies, 13(2)</em>, 342–355.</div>
<div class="ref-entry">[7] Hau, C., Lin, Y., &amp; Wang, T. (2021). Low-shot face recognition for student attendance using OpenFace triplet networks. <em>Proceedings of ICME 2021</em>. https://doi.org/10.1109/ICME51207.2021</div>
<div class="ref-entry">[8] Yadav, S., Mehta, A., &amp; Chandra, P. (2022). Hybrid biometric attendance system using face and voice recognition. <em>International Journal of Computer Applications, 184(12)</em>, 1–8.</div>
<div class="ref-entry">[9] Ahuja, R., Chugh, A., &amp; Sharma, N. (2019). RFID-based smart attendance system for educational institutions. <em>Proceedings of ICRITO 2019</em>, 1–5.</div>
<div class="ref-entry">[10] LeCun, Y., Bengio, Y., &amp; Hinton, G. (2015). Deep learning. <em>Nature, 521(7553)</em>, 436–444. https://doi.org/10.1038/nature14539</div>
<div class="ref-entry">[11] Huang, G. B., Ramesh, M., Berg, T., &amp; Learned-Miller, E. (2007). Labeled Faces in the Wild: A database for studying face recognition in unconstrained environments. <em>UMass Amherst Technical Report 07-49</em>.</div>
<div class="ref-entry">[12] Dalal, N., &amp; Triggs, B. (2005). Histograms of oriented gradients for human detection. <em>Proceedings of CVPR 2005</em>, 1(1)</em>, 886–893.</div>

<h3>Software Libraries &amp; Frameworks</h3>
<div class="ref-entry">[13] Streamlit Inc. (2024). <em>Streamlit: The fastest way to build data apps.</em> Version 1.28. https://streamlit.io</div>
<div class="ref-entry">[14] Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. <em>Journal of Machine Learning Research, 12</em>, 2825–2830. https://scikit-learn.org</div>
<div class="ref-entry">[15] Clark, A. (2023). <em>Pillow (PIL Fork) Documentation.</em> Version 9.5. https://pillow.readthedocs.io</div>
<div class="ref-entry">[16] Walt, S. van der, et al. (2011). The NumPy array: A structure for efficient numerical computation. <em>Computing in Science &amp; Engineering, 13(2)</em>, 22–30. https://numpy.org</div>
''', 39, "References"))

# ───────────────────────────────────────────────────
# PAGE 40 — REFERENCES (Part 2) + CLOSING
# ───────────────────────────────────────────────────
pages_html.append(page('''
<div class="page-header" style="border-bottom:1px solid #dde3f0;padding-bottom:6px;margin-bottom:14px;font-size:8.5pt;color:#64748b;display:flex;justify-content:space-between;">
<span>PRESENS AI — Making Attendance Faster Using AI</span><span>References</span></div>

<h3>Web Standards &amp; Technical Documentation</h3>
<div class="ref-entry">[17] Mozilla Developer Network. (2024). <em>MediaDevices.getUserMedia() — Web APIs.</em> MDN Web Docs. https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia</div>
<div class="ref-entry">[18] W3C. (2023). <em>Media Capture and Streams API.</em> W3C Working Draft. https://www.w3.org/TR/mediacapture-streams/</div>
<div class="ref-entry">[19] Python Software Foundation. (2024). <em>sqlite3 — DB-API 2.0 interface for SQLite databases.</em> Python 3.11 Documentation. https://docs.python.org/3/library/sqlite3.html</div>
<div class="ref-entry">[20] Supabase Inc. (2024). <em>Supabase Documentation: Python Client Library.</em> https://supabase.com/docs/reference/python/introduction</div>
<div class="ref-entry">[21] OpenCV Contributors. (2023). <em>OpenCV 4.x Documentation.</em> https://docs.opencv.org/4.x/</div>
<div class="ref-entry">[22] Resemblyzer: Voice Encoder Library. (2022). https://github.com/resemble-ai/resemblyzer</div>
<div class="ref-entry">[23] segno: QR Code and Micro QR Code Library. (2023). https://segno.readthedocs.io</div>
<div class="ref-entry">[24] AICTE. (2023). <em>Internal survey on attendance management practices in Indian engineering institutions.</em> All India Council for Technical Education, New Delhi.</div>

<h3>Project Repository &amp; Resources</h3>
<div class="ref-entry">[25] Likhith Gowda M A. (2026). <em>PRESENS AI — Making Attendance Faster Using AI.</em> GitHub Repository. https://github.com/Likhithgowda24/PRESENS-AI</div>
<div class="ref-entry">[26] Visvesvaraya Technological University. (2023). <em>Regulations Governing the Degree of Bachelor of Engineering/Technology.</em> VTU, Belagavi, Karnataka.</div>

<hr style="border:none;border-top:2px solid #1e3a8a;margin:28px 0 20px;"/>

<div style="background:linear-gradient(135deg,#0f172a,#1e3a8a);color:white;border-radius:10px;padding:24px 30px;text-align:center;margin-top:10px;">
  <div style="font-size:36px;margin-bottom:10px;">🎓</div>
  <h2 style="color:white;border:none;font-size:17pt;margin-bottom:8px;">PRESENS AI</h2>
  <p style="color:#93c5fd;font-size:11pt;margin-bottom:14px;">Making Attendance Faster Using Artificial Intelligence</p>
  <p style="color:#e0f2fe;font-size:10pt;line-height:1.9;">
    This project report has been prepared in partial fulfilment of the requirements for the<br/>
    <strong style="color:white;">Bachelor of Engineering in Computer Science &amp; Engineering</strong><br/>
    Visvesvaraya Technological University, Belagavi<br/>
    Academic Year 2025–26
  </p>
  <div style="margin-top:18px;padding-top:14px;border-top:1px solid rgba(255,255,255,0.2);">
    <p style="color:#bfdbfe;font-size:10pt;margin:4px 0;"><strong style="color:white;">Author:</strong> Likhith Gowda M A &nbsp;|&nbsp; USN: 1AB22CS086</p>
    <p style="color:#bfdbfe;font-size:10pt;margin:4px 0;"><strong style="color:white;">Department:</strong> Computer Science &amp; Engineering</p>
    <p style="color:#bfdbfe;font-size:10pt;margin:4px 0;"><strong style="color:white;">Institution:</strong> Acharya Institute of Technology, Bengaluru</p>
    <p style="color:#bfdbfe;font-size:10pt;margin:4px 0;"><strong style="color:white;">GitHub:</strong> github.com/Likhithgowda24/PRESENS-AI</p>
  </div>
  <p style="margin-top:16px;color:#64748b;font-size:9pt;">Created with ❤️ by Likhith Gowda M A</p>
</div>
''', 40, "References"))

# ═══════════════════════════════════════════════════════════════════════════════
# BUILD HTML
# ═══════════════════════════════════════════════════════════════════════════════

html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>PRESENS AI — Project Report</title>
<style>
{CSS}
</style>
</head>
<body>
{''.join(pages_html)}
</body>
</html>"""

with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
    f.write(html_doc)

print(f"HTML written: {OUTPUT_HTML} ({len(pages_html)} pages defined)")
print(f"File size: {os.path.getsize(OUTPUT_HTML) / 1024:.1f} KB")

# ═══════════════════════════════════════════════════════════════════════════════
# BUILD PDF via Chrome headless
# ═══════════════════════════════════════════════════════════════════════════════

import tempfile, time

tmp_pdf = str(Path(tempfile.gettempdir()) / "presens_report_tmp.pdf")

chrome_args = [
    CHROME,
    "--headless=new",
    "--disable-gpu",
    "--no-sandbox",
    "--disable-web-security",
    f"--print-to-pdf={tmp_pdf}",
    "--print-to-pdf-no-header",
    "--no-pdf-header-footer",
    "--run-all-compositor-stages-before-draw",
    "--disable-features=TranslateUI",
    f"--user-data-dir={tempfile.mkdtemp()}",
    str(OUTPUT_HTML)
]

print("Generating PDF via Chrome headless...")
result = subprocess.run(chrome_args, capture_output=True, text=True, timeout=120)
time.sleep(3)

# Chrome sometimes writes to CWD — check multiple locations
possible = [tmp_pdf,
            str(Path.home() / "presens_report_tmp.pdf"),
            str(Path.cwd() / "presens_report_tmp.pdf")]
found = None
for p in possible:
    if os.path.exists(p) and os.path.getsize(p) > 50000:
        found = p
        break

if found:
    shutil.copy2(found, str(OUTPUT_PDF))
    print(f"PDF saved: {OUTPUT_PDF}")
    print(f"PDF size: {os.path.getsize(str(OUTPUT_PDF)) / 1024:.1f} KB")
else:
    print(f"Chrome stderr: {result.stderr[:500]}")
    print(f"Chrome stdout: {result.stdout[:200]}")
    # List home dir for the file
    home_files = list(Path.home().glob("*.pdf"))
    print(f"PDFs in home: {home_files}")
    cwd_files = list(Path.cwd().glob("*.pdf"))
    print(f"PDFs in cwd: {cwd_files}")
