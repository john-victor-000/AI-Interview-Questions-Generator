from fastapi import FastAPI, UploadFile, File, Form
import PyPDF2

from backend.model import generate_questions

app = FastAPI()

def extract_text(file):
    pdf = PyPDF2.PdfReader(file.file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text


@app.post("/generate-questions")
async def generate_questions_api(
    resume: UploadFile = File(...),
    jd: str = Form(...)
):
    resume_text = extract_text(resume)

    result = generate_questions(resume_text, jd)

    return result