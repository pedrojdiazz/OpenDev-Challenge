from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from src.database import Base

class LeadModel(Base):
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    address = Column(String)
    phone = Column(String, unique=True)
    registration_date = Column(DateTime, default=func.now())
    courses = relationship("CourseModel", back_populates="lead")