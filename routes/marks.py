from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from dependencies import get_current_student
from models.marks_model import Marks

router = APIRouter(prefix="/marks", tags=["Marks"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/add")
def add_marks(subject: str, score: int, current_student=Depends(get_current_student), db: Session = Depends(get_db)):
    new_mark = Marks(
        student_email=current_student.email,
        subject=subject,
        score=score
    )

    db.add(new_mark)
    db.commit()

    return {"message": "Marks added successfully"}

@router.get("/my")
def get_my_marks(current_student=Depends(get_current_student), db: Session = Depends(get_db)):
    marks = db.query(Marks).filter(Marks.student_email == current_student.email).all()

    return marks
