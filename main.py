from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from database import engine, Base

# models
from models.student_model import Student
from models.marks_model import Marks

# routers
from routes.auth import router as auth_router
from routes.student import router as student_router
from routes.marks import router as marks_router
from routes.analysis import router as analysis_router
from routes.ai_chat import router as ai_router
from routes.prediction import router as prediction_router
from routes.admin import router as admin_router
from routes.admin_analytics import router as admin_analytics_router
from routes.roadmap import router as roadmap_router   # ✅ correct one

app = FastAPI(title="AI Academic Assistant")


# CORS (only once)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# create tables automatically
Base.metadata.create_all(bind=engine)

# register routers
app.include_router(auth_router)
app.include_router(student_router)
app.include_router(marks_router)
app.include_router(analysis_router)
app.include_router(ai_router)
app.include_router(prediction_router)
app.include_router(admin_router)
app.include_router(admin_analytics_router)
app.include_router(roadmap_router)   # final roadmap


@app.get("/")
def home():
    return {"message": "AI Academic Assistant Running 🚀"}
