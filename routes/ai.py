from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.marks_model import Marks
from models.student_model import Student
from dependencies import get_current_student

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/roadmap")
def generate_roadmap(student=Depends(get_current_student), db: Session = Depends(get_db)):

    # get student marks
    marks = db.query(Marks).filter(Marks.student_email == student.email).all()

    if not marks:
        return {"roadmap": "No academic data found. Please add your marks first."}

    weak_subjects = []
    strong_subjects = []

    for m in marks:
        if m.score < 40:
            weak_subjects.append(m.subject)
        else:
            strong_subjects.append(m.subject)

    roadmap = f"""
Your Personalized Study Plan:

Focus More On:
{', '.join(weak_subjects) if weak_subjects else 'None'}

Maintain Strength:
{', '.join(strong_subjects) if strong_subjects else 'None'}

Daily Plan:
- 2 hrs weak subject practice
- 1 hr revision
- 1 aptitude practice
- 1 coding practice
"""

    return {"roadmap": roadmap}
