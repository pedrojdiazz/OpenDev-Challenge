from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base


class CourseModel(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String)
    career = Column(String)
    times_taken = Column(Integer)
    year_of_enrollment = Column(Integer)
    lead_id = Column(Integer, ForeignKey('leads.id'))
    lead = relationship("LeadModel", back_populates="courses")
