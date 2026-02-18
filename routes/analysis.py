from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from dependencies import get_current_student
from models.marks_model import Marks
from models.recommendation_engine import analyze_performance, generate_study_plan

router = APIRouter(prefix="/analysis", tags=["AI Analysis"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/report")
def get_report(current_student=Depends(get_current_student), db: Session = Depends(get_db)):
    marks = db.query(Marks).filter(Marks.student_email == current_student.email).all()

    weak, avg, strong = analyze_performance(marks)
    plan = generate_study_plan(weak, avg, strong)

    return {
        "weak_subjects": weak,
        "average_subjects": avg,
        "strong_subjects": strong,
        "study_plan": plan
    }
