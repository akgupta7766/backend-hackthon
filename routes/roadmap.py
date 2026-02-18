from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from dependencies import get_current_student
from models.marks_model import Marks
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

router = APIRouter(prefix="/roadmap", tags=["AI Roadmap"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def generate_roadmap(current_student=Depends(get_current_student), db: Session = Depends(get_db)):

    marks = db.query(Marks).filter(Marks.student_email == current_student.email).all()

    weak = [m.subject for m in marks if m.score < 40]
    average = [m.subject for m in marks if 40 <= m.score <= 70]
    strong = [m.subject for m in marks if m.score > 70]

    prompt = f"""
Create a 7 day study plan.
Return ONLY JSON array format like:
[
  {{ "day": "Day 1", "tasks": ["task1","task2"] }},
  {{ "day": "Day 2", "tasks": ["task1","task2"] }}
]

Weak: {weak}
Average: {average}
Strong: {strong}
"""

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
    )

    content = chat_completion.choices[0].message.content

    import json
    try:
        parsed = json.loads(content)
    except:
        parsed = [{"day": "Error", "tasks": [content]}]

    return parsed
