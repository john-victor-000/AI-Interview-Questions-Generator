import streamlit as st
import requests

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI Interview Generator",
    page_icon="🤖",
    layout="centered"
)

def create_pdf(data):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("AI Interview Questions", styles["Title"]))
    elements.append(Spacer(1, 12))

    # Technical
    elements.append(Paragraph("Technical Questions", styles["Heading2"]))
    for i, q in enumerate(data.get("technical_questions", []), 1):
        elements.append(Paragraph(f"{i}. {q}", styles["Normal"]))
        elements.append(Spacer(1, 8))

    # HR
    elements.append(Paragraph("HR Questions", styles["Heading2"]))
    for i, q in enumerate(data.get("hr_questions", []), 1):
        elements.append(Paragraph(f"{i}. {q}", styles["Normal"]))
        elements.append(Spacer(1, 8))

    # Project
    elements.append(Paragraph("Project Questions", styles["Heading2"]))
    for i, q in enumerate(data.get("project_questions", []), 1):
        elements.append(Paragraph(f"{i}. {q}", styles["Normal"]))
        elements.append(Spacer(1, 8))

    doc.build(elements)

    buffer.seek(0)
    return buffer

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
.main {
    padding: 2rem;
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
    font-size: 16px;
}
.card {
    padding: 20px;
    border-radius: 10px;
    background-color: #1e1e1e;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.title("🤖 AI Interview Question Generator")
st.write("Generate smart interview questions based on your resume & job description")

# ---------- INPUT SECTION ----------
with st.container():
    st.subheader("📄 Upload Resume")
    uploaded_file = st.file_uploader("", type=["pdf"])

    st.subheader("📝 Job Description")
    jd = st.text_area("Paste Job Description here...", height=150)

# ---------- BUTTON ----------
if st.button("🚀 Generate Questions"):

    if uploaded_file and jd:

        with st.spinner("Analyzing resume and generating questions..."):

            files = {"resume": uploaded_file}
            data = {"jd": jd}

            response = requests.post(
                "http://127.0.0.1:8000/generate-questions",
                files=files,
                data=data
            )

        # ---------- RESPONSE HANDLING ----------
        if response.status_code == 200:
            try:
                result = response.json()
            except Exception:
                st.error("Invalid response from backend")
                st.write(response.text)
                st.stop()
        else:
            st.error(f"Backend Error: {response.status_code}")
            st.write(response.text)
            st.stop()

        # ---------- OUTPUT SECTION ----------
        st.success("✅ Questions Generated Successfully!")

        tab1, tab2, tab3 = st.tabs([
            "💻 Technical",
            "🧑‍💼 HR",
            "📂 Project"
        ])

        pdf_file = create_pdf(result)

        st.download_button(
            label="📄 Download as PDF",
            data=pdf_file,
            file_name="interview_questions.pdf",
            mime="application/pdf"
        )
        
        # ---------- TECHNICAL ----------
        with tab1:
            for i, q in enumerate(result.get("technical_questions", []), 1):
                st.markdown(f"""
                <div class="card">
                <b>Q{i}:</b> {q}
                </div>
                """, unsafe_allow_html=True)

        # ---------- HR ----------
        with tab2:
            for i, q in enumerate(result.get("hr_questions", []), 1):
                st.markdown(f"""
                <div class="card">
                <b>Q{i}:</b> {q}
                </div>
                """, unsafe_allow_html=True)

        # ---------- PROJECT ----------
        with tab3:
            for i, q in enumerate(result.get("project_questions", []), 1):
                st.markdown(f"""
                <div class="card">
                <b>Q{i}:</b> {q}
                </div>
                """, unsafe_allow_html=True)

    else:
        st.warning("⚠️ Please upload resume and enter job description")

