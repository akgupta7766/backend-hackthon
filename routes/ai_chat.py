from fastapi import APIRouter, Depends
from groq import Groq
from dotenv import load_dotenv
import os

from dependencies import get_current_student
from sqlalchemy.orm import Session
from database import SessionLocal
from models.marks_model import Marks

load_dotenv()

router = APIRouter(prefix="/ai", tags=["AI Chatbot"])

# API key load
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/ask")
def ask_ai(question: str,
           current_student = Depends(get_current_student),
           db: Session = Depends(get_db)):

    # student's weak subjects
    marks = db.query(Marks).filter(Marks.student_email == current_student.email).all()
    weak_subjects = [m.subject for m in marks if m.score < 40]

    context = f"""
    Student Branch: {current_student.branch}
    Semester: {current_student.semester}
    Weak Subjects: {weak_subjects}
    """

    prompt = f"""
    You are a helpful college academic assistant.
    Explain in simple language.
    Personalize advice based on student data.

    {context}

    Question: {question}
    """

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
    )

    return {"answer": chat_completion.choices[0].message.content}
