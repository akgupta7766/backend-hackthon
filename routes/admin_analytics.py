from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from collections import defaultdict

from database import SessionLocal
from models.student_model import Student
from models.marks_model import Marks
from dependencies import get_current_admin


# router
router = APIRouter(prefix="/admin", tags=["Admin Analytics"])


# database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------ CLASS ANALYTICS ------------------

@router.get("/analytics")
def class_analytics(
    admin: Student = Depends(get_current_admin), 
    db: Session = Depends(get_db)
):

    # all students
    students = db.query(Student).filter(Student.role == "student").all()
    marks = db.query(Marks).all()

    if len(students) == 0 or len(marks) == 0:
        return {"message": "Not enough data to analyze"}

    # ---------- class average ----------
    total_marks = sum(m.score for m in marks)
    class_average = round(total_marks / len(marks), 2)

    # ---------- topper ----------
    student_scores = defaultdict(list)

    for m in marks:
        student_scores[m.student_email].append(m.score)

    topper_email = max(
        student_scores,
        key=lambda email: sum(student_scores[email]) / len(student_scores[email])
    )

    topper_student = db.query(Student).filter(Student.email == topper_email).first()
    topper_name = topper_student.name if topper_student else "Unknown"

    # ---------- weak students ----------
    weak_students = 0
    for email, scores in student_scores.items():
        avg = sum(scores) / len(scores)
        if avg < 40:
            weak_students += 1

    # ---------- subject wise average ----------
    subject_map = defaultdict(list)

    for m in marks:
        subject_map[m.subject].append(m.score)

    subject_average = {
        subject: round(sum(scores)/len(scores), 2)
        for subject, scores in subject_map.items()
    }

    return {
        "class_average": class_average,
        "topper": topper_name,
        "weak_students": weak_students,
        "total_students": len(students),
        "subject_average": subject_average
    }
