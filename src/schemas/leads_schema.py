from pydantic import BaseModel, EmailStr
from typing import List, Annotated, Optional, Literal
from pydantic.types import StringConstraints
from datetime import datetime
from src.schemas.courses_schema import CourseCreate, CourseOut

class LeadBase(BaseModel):
    full_name: str
    email: EmailStr
    address: str
    phone: Annotated[str, StringConstraints(pattern=r'^\+?1?\d{9,15}$')]
    registration_date: Optional[datetime] = None


class LeadCreate(LeadBase):
    courses: List[CourseCreate] = []

class LeadOut(LeadBase):
    id: int
    courses: List[CourseOut] = []

    class Config:
        from_attributes: Literal[True]