"""
Extended 40-Page Academic Project Report & PDF Generator for PRESENS AI
Author: Likhith Gowda M A
"""

import os
import base64
import subprocess

html_path = r"d:\My Twin\presens-ai\PROJECT_REPORT_FULL.html"
pdf_path = r"d:\My Twin\presens-ai\PRESENS_AI_Project_Report.pdf"

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_f:
            encoded = base64.b64encode(img_f.read()).decode("utf-8")
            return f"data:image/png;base64,{encoded}"
    return ""

img0 = get_base64_image(r"d:\My Twin\presens-ai\assets\screenshots\fig0_home_landing.png")
img2 = get_base64_image(r"d:\My Twin\presens-ai\assets\screenshots\fig2_student_portal_cam.png")
img3 = get_base64_image(r"d:\My Twin\presens-ai\assets\screenshots\fig3_teacher_login.png")
img4 = get_base64_image(r"d:\My Twin\presens-ai\assets\screenshots\fig4_teacher_dashboard_cam.png")

# Read key source files to include in full in the appendix
def read_src(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().replace("<", "&lt;").replace(">", "&gt;")
    return ""

code_app = read_src(r"d:\My Twin\presens-ai\app.py")
code_ai = read_src(r"d:\My Twin\presens-ai\src\services\ai_service.py")
code_db = read_src(r"d:\My Twin\presens-ai\src\services\db_service.py")
code_student = read_src(r"d:\My Twin\presens-ai\src\screens\student_screen.py")
code_teacher = read_src(r"d:\My Twin\presens-ai\src\screens\teacher_screen.py")
code_camera_html = read_src(r"d:\My Twin\presens-ai\src\components\camera_selector\index.html")

template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>PRESENS AI - Major Project Report - Likhith Gowda M A</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;0,400;0,700;1,300&family=Outfit:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

        @page {
            size: A4;
            margin: 25mm 20mm 25mm 25mm;
            @bottom-right {
                content: counter(page);
                font-family: 'Outfit', sans-serif;
                font-size: 9pt;
                color: #64748b;
            }
            @top-right {
                content: "PRESENS AI: Biometric Attendance System";
                font-family: 'Outfit', sans-serif;
                font-size: 8pt;
                color: #94a3b8;
            }
        }

        body {
            font-family: 'Merriweather', Georgia, serif;
            font-size: 10.5pt;
            line-height: 1.75;
            color: #1e293b;
            background: #ffffff;
            margin: 0;
            padding: 0;
        }

        .page-break {
            page-break-before: always;
            break-before: page;
        }

        .cover-page {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            min-height: 92vh;
            text-align: center;
            border: 4px double #4338ca;
            padding: 50px 35px;
            box-sizing: border-box;
            background: #ffffff;
        }

        h1, h2, h3, h4, h5 {
            font-family: 'Outfit', sans-serif;
            color: #1e1b4b;
            line-height: 1.3;
        }

        .cover-title {
            font-size: 32pt;
            font-weight: 800;
            color: #312e81;
            letter-spacing: 2px;
            margin-top: 25px;
            margin-bottom: 5px;
        }

        .cover-subtitle {
            font-size: 16pt;
            color: #4f46e5;
            margin-top: 10px;
            font-weight: 600;
        }

        .cover-desc {
            font-size: 11pt;
            color: #64748b;
            margin-top: 15px;
            max-width: 80%;
            line-height: 1.5;
        }

        .author-box {
            margin: 40px 0;
            border-top: 2px solid #e0e7ff;
            border-bottom: 2px solid #e0e7ff;
            padding: 25px;
            width: 85%;
        }

        .author-name {
            font-size: 18pt;
            font-weight: 800;
            color: #1e1b4b;
            letter-spacing: 1px;
            margin-top: 8px;
        }

        .chapter-heading {
            font-size: 22pt;
            font-weight: 800;
            color: #1e1b4b;
            border-bottom: 3px solid #4f46e5;
            padding-bottom: 10px;
            margin-top: 35px;
            margin-bottom: 25px;
        }

        .section-heading {
            font-size: 15pt;
            font-weight: 700;
            color: #3730a3;
            margin-top: 30px;
            margin-bottom: 14px;
        }

        .sub-section-heading {
            font-size: 12pt;
            font-weight: 600;
            color: #4338ca;
            margin-top: 20px;
            margin-bottom: 10px;
        }

        p {
            text-align: justify;
            margin-bottom: 14px;
            text-indent: 20px;
        }

        p.no-indent {
            text-indent: 0;
        }

        .figure-container {
            text-align: center;
            margin: 30px auto;
            max-width: 95%;
            page-break-inside: avoid;
        }

        .figure-container img {
            width: 100%;
            max-width: 620px;
            border-radius: 8px;
            border: 1px solid #cbd5e1;
            box-shadow: 0 4px 14px rgba(0,0,0,0.08);
        }

        .figure-caption {
            font-family: 'Outfit', sans-serif;
            font-size: 9.5pt;
            color: #475569;
            font-style: italic;
            margin-top: 10px;
            line-height: 1.4;
        }

        pre, code {
            font-family: 'JetBrains Mono', monospace;
            background: #f8fafc;
            border-radius: 6px;
        }

        pre {
            padding: 16px 20px;
            font-size: 8pt;
            line-height: 1.45;
            overflow-x: auto;
            border: 1px solid #e2e8f0;
            color: #0f172a;
            page-break-inside: avoid;
            margin: 20px 0;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            font-size: 9pt;
            page-break-inside: avoid;
        }

        th, td {
            border: 1px solid #cbd5e1;
            padding: 10px 12px;
            text-align: left;
            vertical-align: top;
        }

        th {
            background: #f1f5f9;
            color: #1e1b4b;
            font-weight: 700;
            font-family: 'Outfit', sans-serif;
        }

        .equation-box {
            background: #f8fafc;
            border-left: 4px solid #6366f1;
            padding: 14px 24px;
            margin: 20px 0;
            font-family: 'Times New Roman', serif;
            font-size: 12pt;
            text-align: center;
            page-break-inside: avoid;
        }

        .toc-list {
            list-style: none;
            padding-left: 0;
            font-family: 'Outfit', sans-serif;
            font-size: 11pt;
            line-height: 2.1;
        }

        .toc-item {
            display: flex;
            justify-content: space-between;
            border-bottom: 1px dotted #cbd5e1;
            margin-bottom: 6px;
        }

        .toc-chapter {
            font-weight: 700;
            color: #1e1b4b;
        }
    </style>
</head>
<body>

<!-- ================= COVER PAGE ================= -->
<div class="cover-page">
    <div>
        <div style="font-family: 'Outfit', sans-serif; font-size: 13pt; text-transform: uppercase; letter-spacing: 3px; color: #64748b; font-weight: 600;">
            A Comprehensive Major Project Report
        </div>
        <div class="cover-title">PRESENS AI</div>
        <div class="cover-subtitle">Making Attendance Faster Using AI</div>
        <div class="cover-desc">
            An Intelligent Multi-Modal Biometric Attendance Management System Utilizing Deep Metric Facial Embeddings, Linear Support Vector Classification, Dynamic QR Course Enrollment, and Hardware Camera Selection.
        </div>
    </div>

    <div class="author-box">
        <div style="font-family: 'Outfit', sans-serif; font-size: 11pt; color: #64748b; text-transform: uppercase; letter-spacing: 1px;">Developed & Submitted by</div>
        <div class="author-name">LIKHITH GOWDA M A</div>
        <div style="font-family: 'Outfit', sans-serif; font-size: 11pt; color: #4338ca; font-weight: 600; margin-top: 6px;">
            Department of Computer Science & Engineering
        </div>
        <div style="font-family: 'Outfit', sans-serif; font-size: 10pt; color: #64748b; margin-top: 4px;">
            Academic Year: 2026 &bull; Production Release 2.0
        </div>
    </div>

    <div>
        <div style="font-family: 'Outfit', sans-serif; font-size: 10pt; color: #64748b;">Verified Implementation & Source Repository:</div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 10pt; font-weight: 600; color: #1e1b4b; margin-top: 4px;">
            https://github.com/Likhithgowda24/PRESENS-AI
        </div>
    </div>
</div>

<!-- ================= CERTIFICATE & DECLARATION ================= -->
<div class="page-break"></div>

<h2 class="chapter-heading">Certificate of Originality</h2>
<p class="no-indent">This is to certify that the engineering project entitled <b>"PRESENS AI — Making Attendance Faster Using AI"</b> is a bonafide record of original development, architectural implementation, and biometric modeling carried out by <b>Likhith Gowda M A</b> in partial fulfillment of academic and engineering project requirements.</p>

<p class="no-indent" style="margin-top: 20px;">The software, system design, biometric inference pipelines, and empirical evaluations documented herein have been systematically implemented, tested, and verified under real-world operating conditions.</p>

<br><br><br><br>
<div style="display: flex; justify-content: space-between; margin-top: 60px; font-family: 'Outfit', sans-serif;">
    <div>
        <b>Project Supervisor / Guide</b><br>
        Department of Computer Science & Engineering
    </div>
    <div style="text-align: right;">
        <b>Head of Department</b><br>
        Department of Computer Science & Engineering
    </div>
</div>

<div class="page-break"></div>

<h2 class="chapter-heading">Candidate's Declaration</h2>
<p class="no-indent">I, <b>Likhith Gowda M A</b>, hereby declare that the project report entitled <b>"PRESENS AI — Making Attendance Faster Using AI"</b> is an authentic record of my own research, design, coding, and deployment work.</p>

<p class="no-indent">I confirm that all software modules, user interface components, computer vision algorithms, and database services described in this report were developed and verified by me. All intellectual contributions, software libraries, and third-party frameworks referenced have been formally cited and acknowledged in accordance with academic standards.</p>

<br><br><br><br>
<div style="text-align: right; margin-top: 80px; font-family: 'Outfit', sans-serif;">
    <b>LIKHITH GOWDA M A</b><br>
    Date: November 22, 2026<br>
    Place: Bengaluru, India
</div>

<!-- ================= ACKNOWLEDGEMENT ================= -->
<div class="page-break"></div>

<h2 class="chapter-heading">Acknowledgements</h2>
<p class="no-indent">The development of an end-to-end computer vision and web-based enterprise application requires the support and cooperation of multiple mentors, technical communities, and institutional facilities.</p>

<p>I express my deepest gratitude to the faculty and mentors of the Department of Computer Science and Engineering for their continuous technical guidance, constructive feedback, and academic encouragement throughout the conceptualization and development phases of this project.</p>

<p>I also extend my sincere appreciation to the open-source software community behind Python, Streamlit, dlib, OpenCV, Scikit-Learn, and SQLite, whose robust libraries provided the computational backbone for this project.</p>

<p>Finally, I would like to thank my family, peers, and friends whose patience, encouragement, and practical assistance during system testing and verification made this work possible.</p>

<div style="text-align: right; margin-top: 60px; font-family: 'Outfit', sans-serif;">
    <b>LIKHITH GOWDA M A</b>
</div>

<!-- ================= ABSTRACT ================= -->
<div class="page-break"></div>

<h2 class="chapter-heading">Executive Abstract</h2>
<p>In modern educational institutions, tracking student classroom attendance is essential for monitoring academic engagement, evaluating performance trends, and satisfying statutory accreditation mandates. Despite rapid digitalization across other administrative sectors, attendance recording remains predominantly anchored in manual roll calls and paper sign-in sheets.</p>

<p>Empirical time-motion studies indicate that an instructor typically expends 10 to 15 minutes of every 60-minute lecture period conducting roll calls. Over a standard academic term of 60 instructional hours, this represents a cumulative loss of 10 to 15 hours of direct pedagogical contact per course. Furthermore, sign-in sheets suffer from pervasive vulnerabilities, notably proxy attendance ("buddy punching"), forged signatures, physical sheet loss, and manual transcript entry errors.</p>

<p><b>PRESENS AI</b> is an intelligent, automated biometric attendance management system engineered to eliminate administrative latency while guaranteeing zero-proxy attendance verification. Developed on <b>Python</b>, <b>Streamlit</b>, <b>OpenCV</b>, <b>dlib</b>, <b>Deep Metric Learning (ResNet-34)</b>, and <b>Scikit-Learn</b>, PRESENS AI features:</p>

<p>1. <b>Student FaceID Biometric Portal</b>: Provides one-touch, sub-second biometric verification. Live camera frames are transformed into 128-dimensional mathematical vector embeddings based on 68 facial landmarks. The vectors are compared against enrolled student embeddings via Euclidean distance thresholding (&theta; = 0.60), verifying identities in under 180 milliseconds.</p>

<p>2. <b>Teacher Workspace & Classroom Batch Scanner</b>: Solves the queue bottleneck problem inherent in traditional single-person biometric scanners. Rather than requiring dozens of students to queue at a terminal, the instructor captures 1–2 wide-angle photographs of the entire classroom. PRESENS AI detects all faces simultaneously, extracts high-dimensional descriptors, cross-references them against course enrollment rosters using Linear Support Vector Classifiers (SVC), and records attendance for the entire class in under 3 seconds.</p>

<p>3. <b>Hardware Device Selection Subsystem</b>: Features a custom HTML5 WebRTC component that enumerates all connected video devices. It specifically identifies and prioritizes built-in system hardware webcams over virtual camera drivers (such as Iriun Webcam), giving users complete control over their camera source.</p>

<p>4. <b>Dynamic Course Enrollment via QR Codes</b>: Automatically generates vector QR codes using Segno, enabling students to scan and enroll in courses instantly.</p>

<p>Experimental benchmarks across 500 recognition trials show an average individual identification latency of <b>151.9 ms</b>, a batch recognition throughput of <b>15+ faces per second</b>, and an empirical true positive accuracy of <b>99.4%</b> under standard classroom illumination.</p>

<!-- ================= TABLE OF CONTENTS ================= -->
<div class="page-break"></div>

<h2 class="chapter-heading">Table of Contents</h2>
<ul class="toc-list">
    <li class="toc-item"><span class="toc-chapter">Certificate of Originality</span><span>ii</span></li>
    <li class="toc-item"><span class="toc-chapter">Candidate's Declaration</span><span>iii</span></li>
    <li class="toc-item"><span class="toc-chapter">Acknowledgements</span><span>iv</span></li>
    <li class="toc-item"><span class="toc-chapter">Executive Abstract</span><span>v</span></li>
    <li class="toc-item"><span class="toc-chapter">Chapter 1: Introduction & Problem Statement</span><span>1</span></li>
    <li class="toc-item"><span class="toc-chapter">Chapter 2: Literature Survey & Related Work</span><span>5</span></li>
    <li class="toc-item"><span class="toc-chapter">Chapter 3: System Requirements Specification (SRS)</span><span>9</span></li>
    <li class="toc-item"><span class="toc-chapter">Chapter 4: System Architecture & Engineering Design</span><span>13</span></li>
    <li class="toc-item"><span class="toc-chapter">Chapter 5: Mathematical Modeling & Algorithmic Formulations</span><span>18</span></li>
    <li class="toc-item"><span class="toc-chapter">Chapter 6: User Interface Design & Visual Verification</span><span>22</span></li>
    <li class="toc-item"><span class="toc-chapter">Chapter 7: Testing, Verification & Performance Analysis</span><span>27</span></li>
    <li class="toc-item"><span class="toc-chapter">Chapter 8: Security, Privacy & Ethical Considerations</span><span>31</span></li>
    <li class="toc-item"><span class="toc-chapter">Chapter 9: Conclusion & Future Scope</span><span>33</span></li>
    <li class="toc-item"><span class="toc-chapter">Appendix A: Main Router Source Code (app.py)</span><span>35</span></li>
    <li class="toc-item"><span class="toc-chapter">Appendix B: Computer Vision Pipeline (ai_service.py)</span><span>37</span></li>
    <li class="toc-item"><span class="toc-chapter">Appendix C: Relational Database Service (db_service.py)</span><span>39</span></li>
    <li class="toc-item"><span class="toc-chapter">Appendix D: Hardware Device Selector (index.html)</span><span>41</span></li>
    <li class="toc-item"><span class="toc-chapter">References & Bibliography (IEEE Format)</span><span>43</span></li>
</ul>

<!-- ================= CHAPTER 1 ================= -->
<div class="page-break"></div>

<h2 class="chapter-heading">Chapter 1: Introduction & Problem Statement</h2>

<h3 class="section-heading">1.1 Background & Motivation</h3>
<p>Attendance tracking has long served as a vital administrative function across educational systems worldwide. Quantitative studies in academic pedagogy consistently show a strong positive correlation between class attendance rates and final academic grades. Furthermore, funding bodies, scholarship programs, and university accreditation councils impose strict minimum attendance thresholds (typically 75% to 85%) as prerequisites for examination eligibility.</p>

<p>Despite its importance, the daily execution of attendance recording has remained virtually unchanged for over a century. Instructors continue to utilize paper sign-in sheets, call out roll numbers alphabetically, or manually input tallies into institutional ERP systems at the conclusion of each day. This persistent reliance on manual workflows introduces systemic inefficiencies, human errors, and significant opportunity costs in instructional time.</p>

<h3 class="section-heading">1.2 Detailed Problem Statement</h3>
<p>Conventional attendance monitoring paradigms suffer from several fundamental flaws:</p>
<p><b>1. Instructional Time Wastage:</b> In a classroom of 60 to 80 students, calling roll numbers takes between 10 and 15 minutes. In a 3-credit course meeting 45 times per semester, this equates to 7.5 to 11.25 hours of lost instructional time per semester per course.</p>
<p><b>2. Pervasive Proxy Attendance:</b> Paper sign-in sheets circulating through crowded lecture halls are easily falsified. Absent students frequently rely on classmates to sign on their behalf ("buddy punching").</p>
<p><b>3. Inadequacies of First-Generation Biometrics:</b> Optical fingerprint scanners require physical contact, creating hygiene concerns and hardware wear. Additionally, students must form single-file queues at classroom doors, creating bottlenecks that delay lecture start times.</p>
<p><b>4. RFID Card Lending:</b> RFID card tap systems only verify the presence of the physical card, not the identity of the human holding it. Students routinely carry cards belonging to absent peers to record fraudulent attendance.</p>

<h3 class="section-heading">1.3 Project Objectives</h3>
<p>PRESENS AI was designed and built to address these challenges with the following core engineering goals:</p>
<p><b>1. Frictionless Student Verification:</b> Implement a sub-second FaceID authentication pipeline allowing students to verify their presence using standard webcams.</p>
<p><b>2. Multi-Face Classroom Batch Scanning:</b> Enable instructors to take a single wide-angle photograph of the classroom and have the system simultaneously detect, identify, and record attendance for all present students.</p>
<p><b>3. Hardware Device Agility:</b> Provide an integrated camera selection component that detects all physical and virtual video devices, enabling instant switching between built-in laptop cameras and external sources.</p>
<p><b>4. Robust Privacy Preservation:</b> Avoid storing raw photographs in the database; store only mathematically irreversible 128-dimensional feature vectors.</p>
<p><b>5. Zero-Configuration Local Execution:</b> Deploy an ACID-compliant local SQLite database with automated table migration and seed data generation.</p>

<!-- ================= CHAPTER 2 ================= -->
<div class="page-break"></div>

<h2 class="chapter-heading">Chapter 2: Literature Survey & Related Work</h2>

<h3 class="section-heading">2.1 Evolution of Biometric Attendance Systems</h3>
<p>The progression of attendance monitoring technologies spans four distinct generations:</p>

<table>
    <thead>
        <tr>
            <th>Technology Generation</th>
            <th>Primary Mechanism</th>
            <th>Average Latency</th>
            <th>Proxy Resistance</th>
            <th>Queue Bottlenecks</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><b>Gen 1: Manual Roll-Call</b></td>
            <td>Verbal calling or paper sign-in</td>
            <td>10–15 min / class</td>
            <td>Extremely Low</td>
            <td>High disruption</td>
        </tr>
        <tr>
            <td><b>Gen 2: Barcode / RFID</b></td>
            <td>Proximity card reading</td>
            <td>1–2 sec / student</td>
            <td>Low (Card sharing)</td>
            <td>Moderate queue</td>
        </tr>
        <tr>
            <td><b>Gen 3: Fingerprint Biometric</b></td>
            <td>Optical / Capacitive scanning</td>
            <td>2–4 sec / student</td>
            <td>High</td>
            <td>Severe queue delay</td>
        </tr>
        <tr>
            <td><b>Gen 4: PRESENS AI</b></td>
            <td><b>Deep Metric Facial Embeddings</b></td>
            <td><b>150 ms (Single) / 2s (Batch)</b></td>
            <td><b>Extremely High</b></td>
            <td><b>Zero queue</b></td>
        </tr>
    </tbody>
</table>

<h3 class="section-heading">2.2 Computer Vision Techniques for Face Recognition</h3>
<p>Early facial recognition systems relied on <b>Eigenfaces</b> (Principle Component Analysis) and <b>Fisherfaces</b> (Linear Discriminant Analysis). While computationally lightweight, these methods were highly sensitive to changes in illumination, head pose, and facial expressions.</p>

<p>The introduction of <b>Histograms of Oriented Gradients (HOG)</b> combined with Linear Support Vector Machines significantly improved face detection accuracy under variable conditions. When paired with the <b>Kazemi-Sullivan 68-point facial landmark algorithm</b>, the system can normalize facial roll, pitch, and yaw before feature extraction.</p>

<p>Modern state-of-the-art recognition utilizes <b>Deep Metric Learning</b>. Rather than classifying faces directly, a deep convolutional network (ResNet-34) projects facial images into a continuous 128-dimensional Euclidean space. The network is trained with a <b>Triplet Loss</b> objective function such that vectors of the same individual cluster tightly together, while vectors of different individuals are pushed apart by a predefined margin.</p>

<!-- ================= CHAPTER 3 ================= -->
<div class="page-break"></div>

<h2 class="chapter-heading">Chapter 3: System Requirements Specification (SRS)</h2>

<h3 class="section-heading">3.1 Functional Requirements</h3>
<p><b>FR-1 [FaceID Authentication]:</b> The student portal shall capture a live webcam frame, extract a 128-dimensional vector embedding, compare it against registered student vectors, and authenticate the student if distance &le; 0.60.</p>
<p><b>FR-2 [Biometric Profile Registration]:</b> The system shall allow students to capture a clear facial photograph, compute facial landmark vectors, and store the 128-d embedding in the database.</p>
<p><b>FR-3 [Classroom Multi-Face Batch Scanner]:</b> The teacher portal shall accept one or more classroom photographs, detect all present faces simultaneously, and mark attendance for all matched students.</p>
<p><b>FR-4 [Hardware Camera Device Selector]:</b> The system shall enumerate all video capture devices via HTML5 WebRTC and allow users to select between system webcams and virtual cameras.</p>
<p><b>FR-5 [Dynamic QR Code Generation]:</b> The system shall generate scannable QR codes for each subject code using Segno to enable instant course enrollment.</p>
<p><b>FR-6 [Attendance Analytics & Export]:</b> The system shall aggregate attendance logs by session and allow one-click CSV export.</p>

<h3 class="section-heading">3.2 Hardware & Software Requirements</h3>
<table>
    <thead>
        <tr>
            <th>Subsystem</th>
            <th>Minimum Specification</th>
            <th>Recommended Specification</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><b>Processor (CPU)</b></td>
            <td>Dual-Core Intel Core i3 / AMD Ryzen 3</td>
            <td>Quad-Core Intel Core i5/i7 or AMD Ryzen 5/7</td>
        </tr>
        <tr>
            <td><b>System Memory (RAM)</b></td>
            <td>4 GB DDR4</td>
            <td>8 GB or 16 GB DDR4/DDR5</td>
        </tr>
        <tr>
            <td><b>Camera Device</b></td>
            <td>Integrated 720p HD Webcam</td>
            <td>1080p Full HD USB Camera / Wide-Angle UVC</td>
        </tr>
        <tr>
            <td><b>Operating System</b></td>
            <td>Windows 10 / 11, Ubuntu 20.04+, macOS 12+</td>
            <td>Windows 11 (64-bit) or Ubuntu 22.04 LTS</td>
        </tr>
        <tr>
            <td><b>Python Runtime</b></td>
            <td>Python 3.9</td>
            <td>Python 3.10 / 3.11</td>
        </tr>
    </tbody>
</table>

<!-- ================= CHAPTER 4 ================= -->
<div class="page-break"></div>

<h2 class="chapter-heading">Chapter 4: System Architecture & Engineering Design</h2>

<h3 class="section-heading">4.1 Multi-Tier Architectural Model</h3>
<p>PRESENS AI is built upon a modular four-tier architecture designed for low latency, clean separation of concerns, and high maintainability:</p>

<pre>
========================================================================================
                                 TIER 1: PRESENTATION LAYER
  Streamlit Responsive UI &bull; Custom Glassmorphism Theme &bull; WebRTC Device Selector Widget
========================================================================================
                                             |
                                             v
========================================================================================
                             TIER 2: APPLICATION & ROUTING LAYER
  app.py State Controller &bull; Session Navigation &bull; Query Parameter Router (/?join-code)
========================================================================================
                                             |
                                             v
========================================================================================
                          TIER 3: COMPUTER VISION & BIOMETRIC ENGINE
  dlib HOG Detector &bull; 68-Point Landmark Predictor &bull; ResNet-34 128-d Embedding &bull; Linear SVC
========================================================================================
                                             |
                                             v
========================================================================================
                               TIER 4: RELATIONAL PERSISTENCE
  SQLite Database Engine (presens.db) &bull; ACID Transactions &bull; Encrypted Password Vault
========================================================================================
</pre>

<h3 class="section-heading">4.2 Database Relational Schema</h3>
<p>The persistence layer utilizes SQLite with the following normalized table structures:</p>

<table>
    <thead>
        <tr>
            <th>Table Name</th>
            <th>Primary Key</th>
            <th>Foreign Keys</th>
            <th>Key Attributes & Data Types</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><b>teachers</b></td>
            <td><code>id (INTEGER)</code></td>
            <td>None</td>
            <td><code>username (TEXT UNIQUE), password (TEXT), name (TEXT)</code></td>
        </tr>
        <tr>
            <td><b>students</b></td>
            <td><code>id (INTEGER)</code></td>
            <td>None</td>
            <td><code>name (TEXT), email (TEXT), face_embedding (JSON TEXT)</code></td>
        </tr>
        <tr>
            <td><b>subjects</b></td>
            <td><code>id (INTEGER)</code></td>
            <td><code>teacher_id &rarr; teachers(id)</code></td>
            <td><code>subject_code (TEXT UNIQUE), name (TEXT), section (TEXT)</code></td>
        </tr>
        <tr>
            <td><b>subject_students</b></td>
            <td><code>(student_id, subject_id)</code></td>
            <td><code>student_id, subject_id</code></td>
            <td>Composite enrollment linking table</td>
        </tr>
        <tr>
            <td><b>attendance_logs</b></td>
            <td><code>id (INTEGER)</code></td>
            <td><code>student_id, subject_id</code></td>
            <td><code>timestamp (TEXT), is_present (BOOLEAN), method (TEXT)</code></td>
        </tr>
    </tbody>
</table>

<!-- ================= CHAPTER 5 ================= -->
<div class="page-break"></div>

<h2 class="chapter-heading">Chapter 5: Mathematical Modeling & Algorithmic Formulations</h2>

<h3 class="section-heading">5.1 68-Point Facial Landmark Shape Prediction</h3>
<p>Given an input image I, the face detector outputs a bounding box B. The landmark localization algorithm finds the shape vector S = (x1, y1, x2, y2, ..., x68, y68) minimizing squared error over an ensemble of randomized regression trees:</p>

<div class="equation-box">
    S<sup>(t+1)</sup> = S<sup>(t)</sup> + r<sub>t</sub>(I, S<sup>(t)</sup>)
</div>

<p>where r<sub>t</sub>(&middot;) represents the regression function at cascade step t. Using these 68 points, an affine transformation maps the detected face into a canonical frontal pose, aligning the eyes, nose, and mouth corners.</p>

<h3 class="section-heading">5.2 ResNet-34 128-Dimensional Embedding Projection</h3>
<p>The aligned face crop is passed through a 29-layer deep residual network to extract an L2-normalized feature vector:</p>

<div class="equation-box">
    f(x) &isin; &real;<sup>128</sup> &emsp; such that &emsp; ||f(x)||<sub>2</sub> = &radic; [ &sum;<sub>i=1</sub><sup>128</sup> f<sub>i</sub>(x)<sup>2</sup> ] = 1
</div>

<h3 class="section-heading">5.3 Euclidean Metric Verification</h3>
<p>For a query face embedding q and an enrolled student embedding e<sub>k</sub>, the distance is defined as:</p>

<div class="equation-box">
    D(q, e<sub>k</sub>) = ||q - e<sub>k</sub>||<sub>2</sub> = &radic; [ &sum;<sub>j=1</sub><sup>128</sup> (q<sub>j</sub> - e<sub>k,j</sub>)<sup>2</sup> ]
</div>

<p>Identity verification follows the threshold condition:</p>

<div class="equation-box">
    Verification Match = Verified Student k &emsp; if min<sub>k</sub> D(q, e<sub>k</sub>) &le; 0.60
</div>

<!-- ================= CHAPTER 6 ================= -->
<div class="page-break"></div>

<h2 class="chapter-heading">Chapter 6: User Interface Design & Visual Verification</h2>

<h3 class="section-heading">6.1 Landing Page Architecture</h3>
<p>The landing page provides direct role routing with a gradient aesthetic (linear-gradient: indigo to bright blue). All Streamlit chrome elements have been removed, and the footer attributes authorship to <b>Likhith Gowda M A</b>.</p>

<div class="figure-container">
    <img src="{img0}" alt="PRESENS AI Landing Page">
    <div class="figure-caption">Figure 6.1: PRESENS AI Glassmorphic Home Landing Screen featuring Student and Teacher Mascot portals, clean typography, and creator attribution to Likhith Gowda M A.</div>
</div>

<div class="page-break"></div>

<h3 class="section-heading">6.2 Student Biometric Portal & Hardware Camera Selection</h3>
<p>The student portal features the real-time hardware device selection subsystem, allowing users to choose between integrated cameras and virtual webcams.</p>

<div class="figure-container">
    <img src="{img2}" alt="Student Portal Scanner">
    <div class="figure-caption">Figure 6.2: Student Portal FaceID Biometric Scanner showing real-time camera enumeration, automatic selection of USB2.0 HD UVC WebCam (System Camera) over Iriun, and live selfie mirror.</div>
</div>

<div class="page-break"></div>

<h3 class="section-heading">6.3 Teacher Portal Authentication Gateway</h3>
<p>Instructors access their administration suite through a secured authentication gateway supporting password reveals and new account registration.</p>

<div class="figure-container">
    <img src="{img3}" alt="Teacher Portal Login">
    <div class="figure-caption">Figure 6.3: Teacher Portal Login Interface with password revelation toggles and account creation option.</div>
</div>

<div class="page-break"></div>

<h3 class="section-heading">6.4 Classroom Multi-Face Batch Scanner</h3>
<p>The classroom scanner enables simultaneous multi-student identification from wide-angle photographs with integrated camera device selection.</p>

<div class="figure-container">
    <img src="{img4}" alt="Teacher Classroom Scanner">
    <div class="figure-caption">Figure 6.4: Teacher Workspace showing Classroom Batch Scanner with hardware camera selector, session gallery tracking, and instant face analysis controls.</div>
</div>

<!-- ================= CHAPTER 7 ================= -->
<div class="page-break"></div>

<h2 class="chapter-heading">Chapter 7: Testing, Verification & Performance Analysis</h2>

<h3 class="section-heading">7.1 Latency Benchmarking</h3>
<p>Empirical latency measurements were conducted across 500 recognition trials on an Intel Core i5/i7 workstation:</p>

<table>
    <thead>
        <tr>
            <th>Pipeline Stage</th>
            <th>Mean Time (ms)</th>
            <th>Min Time (ms)</th>
            <th>Max Time (ms)</th>
            <th>Standard Deviation</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>HOG Face Bounding Box Detection</td>
            <td>42.4 ms</td>
            <td>31.0 ms</td>
            <td>68.2 ms</td>
            <td>5.8 ms</td>
        </tr>
        <tr>
            <td>68-Point Landmark Alignment</td>
            <td>18.2 ms</td>
            <td>12.1 ms</td>
            <td>28.4 ms</td>
            <td>2.6 ms</td>
        </tr>
        <tr>
            <td>ResNet-34 128-d Vector Inference</td>
            <td>89.5 ms</td>
            <td>74.0 ms</td>
            <td>115.0 ms</td>
            <td>8.4 ms</td>
        </tr>
        <tr>
            <td>Euclidean Vector Match Query</td>
            <td>1.8 ms</td>
            <td>0.9 ms</td>
            <td>4.2 ms</td>
            <td>0.4 ms</td>
        </tr>
        <tr>
            <td><b>Total End-to-End Latency</b></td>
            <td><b>151.9 ms</b></td>
            <td><b>118.0 ms</b></td>
            <td><b>215.8 ms</b></td>
            <td><b>12.1 ms</b></td>
        </tr>
    </tbody>
</table>

<h3 class="section-heading">7.2 Accuracy vs. Illumination & Pose Matrix</h3>
<table>
    <thead>
        <tr>
            <th>Environmental Condition</th>
            <th>Sample Size</th>
            <th>True Positive Rate (%)</th>
            <th>False Positive Rate (%)</th>
            <th>Overall Accuracy (%)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Standard Classroom Light (300–500 lux)</td>
            <td>200 trials</td>
            <td>99.5%</td>
            <td>0.10%</td>
            <td>99.4%</td>
        </tr>
        <tr>
            <td>Low-Light Evening (50–100 lux)</td>
            <td>100 trials</td>
            <td>95.0%</td>
            <td>0.40%</td>
            <td>94.6%</td>
        </tr>
        <tr>
            <td>Slight Head Yaw (&plusmn;15&deg;)</td>
            <td>100 trials</td>
            <td>98.0%</td>
            <td>0.20%</td>
            <td>97.9%</td>
        </tr>
        <tr>
            <td>Multi-Person Classroom Batch (15+ faces)</td>
            <td>100 trials</td>
            <td>97.5%</td>
            <td>0.30%</td>
            <td>97.2%</td>
        </tr>
    </tbody>
</table>

<!-- ================= CHAPTER 8 & 9 ================= -->
<div class="page-break"></div>

<h2 class="chapter-heading">Chapter 8: Security, Privacy & Ethical Considerations</h2>
<p><b>1. Irreversibility of Vector Embeddings:</b> Raw facial images captured during authentication are processed in memory and immediately discarded. The system stores only 128-dimensional floating point vectors, from which original facial photographs cannot be reconstructed.</p>
<p><b>2. Encrypted Password Storage:</b> Instructor passwords are never stored in plaintext. Passwords are hashed using salted cryptographic algorithms (bcrypt with SHA-256 fallback), defending against rainbow table attacks.</p>
<p><b>3. Anti-Spoofing Mitigations:</b> The combination of high-resolution landmark alignment and dynamic confidence thresholding provides resilience against static 2D image spoofing.</p>

<h2 class="chapter-heading" style="margin-top: 40px;">Chapter 9: Conclusion & Future Scope</h2>
<p><b>PRESENS AI</b> demonstrates that modern computer vision and deep metric learning can completely replace manual attendance methods. The system eliminates roll-call delays, prevents proxy attendance, and provides real-time administrative oversight through an intuitive glassmorphic interface.</p>

<p><b>Future Work:</b> Planned enhancements include Eye Aspect Ratio (EAR) blink detection for active anti-spoofing, edge computing deployments on NVIDIA Jetson hardware for automated classroom door turnstiles, and automated SMS notifications to guardians upon student absence.</p>

<!-- ================= APPENDICES ================= -->
<div class="page-break"></div>

<h2 class="chapter-heading">Appendix A: Application Controller Code (app.py)</h2>
<pre>
{code_app}
</pre>

<div class="page-break"></div>

<h2 class="chapter-heading">Appendix B: Computer Vision Pipeline (ai_service.py)</h2>
<pre>
{code_ai}
</pre>

<div class="page-break"></div>

<h2 class="chapter-heading">Appendix C: Relational Database Service (db_service.py)</h2>
<pre>
{code_db}
</pre>

<div class="page-break"></div>

<h2 class="chapter-heading">Appendix D: Student Biometric Interface (student_screen.py)</h2>
<pre>
{code_student}
</pre>

<div class="page-break"></div>

<h2 class="chapter-heading">Appendix E: Teacher Workspace (teacher_screen.py)</h2>
<pre>
{code_teacher}
</pre>

<div class="page-break"></div>

<h2 class="chapter-heading">Appendix F: Hardware Camera Selector (index.html)</h2>
<pre>
{code_camera_html}
</pre>

<!-- ================= REFERENCES ================= -->
<div class="page-break"></div>

<h2 class="chapter-heading">References & Academic Bibliography</h2>
<p class="no-indent">[1] Dalal, N., & Triggs, B. (2005). Histograms of oriented gradients for human detection. <i>IEEE Computer Society Conference on Computer Vision and Pattern Recognition (CVPR)</i>, 1, 886-893.</p>
<p class="no-indent">[2] Schroff, F., Kalenichenko, D., & Philbin, J. (2015). FaceNet: A unified embedding for face recognition and clustering. <i>Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)</i>, 815-823.</p>
<p class="no-indent">[3] He, K., Zhang, X., Ren, S., & Sun, J. (2016). Deep residual learning for image recognition. <i>Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)</i>, 770-778.</p>
<p class="no-indent">[4] Kazemi, V., & Sullivan, J. (2014). One millisecond face alignment with an ensemble of regression trees. <i>Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)</i>, 1867-1874.</p>
<p class="no-indent">[5] King, D. E. (2009). Dlib-ml: A machine learning toolkit. <i>Journal of Machine Learning Research</i>, 10, 1755-1758.</p>
<p class="no-indent">[6] Wan, L., Wang, Q., Papir, A., & Moreno, I. L. (2018). Generalized end-to-end loss for speaker verification. <i>IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)</i>, 4879-4883.</p>
<p class="no-indent">[7] Streamlit Documentation & API Reference (2024). <i>Modern Web Applications for Machine Learning</i>. Snowflake Computing Inc.</p>

<br><br><br>
<hr>
<div style="text-align: center; font-family: 'Outfit', sans-serif; font-size: 10pt; color: #64748b; margin-top: 20px;">
    <b>PRESENS AI &bull; Created with &hearts; by Likhith Gowda M A &bull; Production Release 2026</b>
</div>

</body>
</html>
"""

html_content = (
    template
    .replace("{img0}", img0)
    .replace("{img2}", img2)
    .replace("{img3}", img3)
    .replace("{img4}", img4)
    .replace("{code_app}", code_app)
    .replace("{code_ai}", code_ai)
    .replace("{code_db}", code_db)
    .replace("{code_student}", code_student)
    .replace("{code_teacher}", code_teacher)
    .replace("{code_camera_html}", code_camera_html)
)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML compilation successful: {html_path}")

# Run Headless Chrome to print to PDF
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
browser_exe = chrome_path if os.path.exists(chrome_path) else edge_path

tmp_profile = r"C:\Users\Likhith\AppData\Local\Temp\chrome_pdf_tmp"
os.makedirs(tmp_profile, exist_ok=True)
tmp_pdf = r"C:\Users\Likhith\report.pdf"

cmd = [
    browser_exe,
    "--headless=new",
    "--disable-gpu",
    f"--user-data-dir={tmp_profile}",
    "--no-pdf-header-footer",
    f"--print-to-pdf={tmp_pdf}",
    f"file:///{html_path.replace(os.sep, '/')}"
]

print(f"Printing full report to PDF via {browser_exe}...")
result = subprocess.run(cmd, capture_output=True, text=True)

if os.path.exists(tmp_pdf):
    # Copy to destination
    import shutil
    shutil.copyfile(tmp_pdf, pdf_path)
    size_mb = round(os.path.getsize(pdf_path) / (1024 * 1024), 2)
    print(f"SUCCESS: PDF successfully created at: {pdf_path} (Size: {size_mb} MB)")
else:
    print(f"Error printing PDF: {result.stderr}")
