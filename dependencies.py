from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database import SessionLocal
from models.student_model import Student
from auth_utils import SECRET_KEY, ALGORITHM

security = HTTPBearer()


# Base user extractor
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    db = SessionLocal()
    user = db.query(Student).filter(Student.email == email).first()
    db.close()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


# STUDENT ONLY
def get_current_student(user: Student = Depends(get_current_user)):
    if user.role != "student":
        raise HTTPException(status_code=403, detail="Students only")
    return user


# ADMIN ONLY
def get_current_admin(user: Student = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return user
