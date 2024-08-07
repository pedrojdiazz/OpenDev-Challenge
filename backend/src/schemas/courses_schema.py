from pydantic import BaseModel
from typing import Literal


class CourseBase(BaseModel):
    subject: str
    career: str
    year_of_enrollment: int
    times_taken: int


class CourseCreate(CourseBase):
    pass


class CourseOut(CourseBase):
    id: int
    lead_id: int

    class Config:
        from_attributes: Literal[True]
