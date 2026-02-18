from fastapi import APIRouter, Depends
from dependencies import get_current_student
from models.prediction_model import predict_placement

router = APIRouter(prefix="/prediction", tags=["Placement AI"])

@router.post("/placement")
def placement_prediction(avg_marks: int, dsa: int, projects: int, aptitude: int,
                         current_student=Depends(get_current_student)):

    probability = predict_placement(avg_marks, dsa, projects, aptitude)

    return {
        "placement_probability": f"{probability}%",
        "message": "High chance of placement" if probability > 65 else "Need improvement"
    }
