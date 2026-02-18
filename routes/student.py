from fastapi import APIRouter, Depends
from dependencies import get_current_student

router = APIRouter(prefix="/student", tags=["Student"])

@router.get("/me")
def get_my_profile(current_student = Depends(get_current_student)):
    return {
        "name": current_student.name,
        "email": current_student.email,
        "branch": current_student.branch,
        "semester": current_student.semester
    }
