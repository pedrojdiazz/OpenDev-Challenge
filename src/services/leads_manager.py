from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate
from src.models.courses_model import CourseModel    
from src.models.leads_model import LeadModel
from src.exceptions import DatabaseException, NotFoundException, InvalidRequestException
from src.config import logger
from src.schemas.courses_schema import CourseCreate, CourseOut
from src.schemas.leads_schema import LeadCreate, LeadOut
from typing import List, Optional
from fastapi_pagination import Page, Params


class LeadsManager:
    def __init__(self, db: Session):
        self.db = db


    def create_lead(self, lead_data: LeadCreate):
        db_lead = LeadModel(
            full_name = lead_data.full_name,
            email = lead_data.email,
            address = lead_data.address,
            phone = lead_data.phone,
            registration_date = lead_data.registration_date
        )
        
        try:
            self.db.add(db_lead)
            self.db.commit()
            self.db.refresh(db_lead)

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating lead: {e}")
            raise InvalidRequestException(status_code=500, message="Invalid email or phone number")
        
        if lead_data.courses:
            self._add_courses_to_lead(int(db_lead.id), lead_data.courses)
        
        return db_lead


    def _add_courses_to_lead(self, lead_id: int, courses: List[CourseCreate]):
        try:
            for course in courses:
                db_course = CourseModel(
                    subject=course.subject,
                    career=course.career,
                    year_of_enrollment=course.year_of_enrollment,
                    times_taken=course.times_taken,
                    lead_id=lead_id
                )
                self.db.add(db_course)
            self.db.commit()

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating lead: {e}")
            raise DatabaseException(status_code=500, message="An error occurred while adding courses.")


    def get_lead(self, lead_id: int):
        lead: Optional[LeadOut] = self.db.query(LeadModel).filter(LeadModel.id == lead_id).first()
        if lead is None:
            logger.error("Lead Not Found")
            raise NotFoundException(status_code=404, message="Lead not found")
        
        return lead
    
    def get_leads(self, params: Params) -> Page[LeadOut]:
        try:
            query = self.db.query(LeadModel)
            return paginate(query, params=params)
        
        except Exception as e:
            logger.error(f"Error creating lead: {e}")
            raise DatabaseException(status_code=500, message="An error occurred while retrieving paginated leads.")

