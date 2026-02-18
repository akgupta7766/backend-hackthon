from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.student_model import Student
from passlib.hash import bcrypt
from auth_utils import create_access_token
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ---------------- DB ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- SCHEMAS ----------------
class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    branch: str
    semester: str
    role: str = "student"


class LoginRequest(BaseModel):
    email: str
    password: str


# ---------------- REGISTER ----------------
@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):

    existing = db.query(Student).filter(Student.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = bcrypt.hash(data.password)

    student = Student(
        name=data.name,
        email=data.email,
        password=hashed_password,
        branch=data.branch,
        semester=data.semester,
        role=data.role
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    return {"message": f"{data.role} registered successfully"}


# ---------------- LOGIN ----------------
@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):

    student = db.query(Student).filter(Student.email == data.email).first()

    if not student or not bcrypt.verify(data.password, student.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({
        "sub": student.email,
        "role": student.role
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": student.role,
        "name": student.name
    }
