from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from dependencies import get_current_student
from models.marks_model import Marks
from groq import Groq
import os, json, re
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

router = APIRouter(prefix="/roadmap", tags=["AI Roadmap"])


# ---------- DB ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- SUBJECT DETECTOR ----------
def detect_subject(text):
    text = text.lower()

    if "math" in text:
        return "Maths"
    if "dbms" in text:
        return "DBMS"
    if "dsa" in text:
        return "DSA"
    if "os" in text:
        return "Operating System"

    return "General Study"


# ---------- WEAKNESS DETECTOR ----------
def detect_weakness(text):
    text = text.lower()

    if "revise" in text or "review" in text or "weak" in text:
        return "HIGH", "Concept revision required"

    if "practice" in text or "problem" in text:
        return "MODERATE", "Needs practice"

    return "STRONG", "Good understanding"


# ---------- API ----------
@router.get("/")
def generate_roadmap(current_student=Depends(get_current_student),
                     db: Session = Depends(get_db)):

    marks = db.query(Marks).filter(
        Marks.student_email == current_student.email
    ).all()

    if not marks:
        return [{
            "day": "No Data",
            "subject": "No subjects found",
            "weakness": "UNKNOWN",
            "reason": "Student has not added marks yet",
            "improvement_plan": ["Add marks first"]
        }]

    # simple summary for AI
    summary = [{ "subject": m.subject, "score": m.score } for m in marks]

    prompt = f"""
Create a 7 day study plan.
Return JSON array:
[{{"day":"Day 1","tasks":["task1","task2"]}}]

Student performance:
{summary}
"""

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    content = chat_completion.choices[0].message.content.strip()

    # ---- extract json ----
    match = re.search(r'\[.*\]', content, re.S)
    if match:
        content = match.group(0)

    try:
        ai_data = json.loads(content)
    except:
        ai_data = []

    # ---------- CONVERT TO FRONTEND FORMAT ----------
    final_output = []

    for item in ai_data:
        tasks = item.get("tasks", [])
        text = " ".join(tasks)

        subject = detect_subject(text)
        weakness, reason = detect_weakness(text)

        final_output.append({
            "day": item.get("day", "Day"),
            "subject": subject,
            "weakness": weakness,
            "reason": reason,
            "improvement_plan": tasks
        })

    return final_output
