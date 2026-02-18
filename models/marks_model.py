from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Marks(Base):
    __tablename__ = "marks"

    id = Column(Integer, primary_key=True, index=True)
    student_email = Column(String, ForeignKey("students.email"))
    subject = Column(String)
    score = Column(Integer)
