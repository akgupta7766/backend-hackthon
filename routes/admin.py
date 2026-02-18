from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.student_model import Student
from models.marks_model import Marks
from dependencies import get_current_admin




# IMPORTANT — router sabse pehle define hona chahiye
router = APIRouter(prefix="/admin", tags=["Admin Panel"])


# DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# 1. All students
# =========================
@router.get("/students")
def all_students(admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    students = db.query(Student).all()

    return [
        {
            "name": s.name,
            "email": s.email,
            "branch": s.branch,
            "semester": s.semester,
            "role": s.role
        }
        for s in students
    ]


# =========================
# 2. Add marks
# =========================
@router.post("/add-marks")
def add_marks(email: str, subject: str, score: int,
              admin=Depends(get_current_admin),
              db: Session = Depends(get_db)):

    student = db.query(Student).filter(Student.email == email).first()

    if not student:
        return {"error": "Student not found"}

    mark = Marks(student_email=email, subject=subject, score=score)
    db.add(mark)
    db.commit()

    return {"message": f"Marks added to {student.name}"}


# =========================
# 3. Weak students
# =========================
@router.get("/weak-students")
def weak_students(admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    students = db.query(Student).all()
    result = []

    for s in students:
        marks = db.query(Marks).filter(Marks.student_email == s.email).all()

        if len(marks) == 0:
            continue

        avg = sum(m.score for m in marks) / len(marks)

        if avg < 50:
            result.append({
                "name": s.name,
                "email": s.email,
                "average": round(avg, 2)
            })

    return result
