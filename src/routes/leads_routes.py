from fastapi import APIRouter, HTTPException, Depends, status
from src.schemas import leads_schema
from sqlalchemy.orm import Session 
from src.services.leads_manager import LeadsManager
from src.database import get_db
from src.exceptions import DatabaseException, NotFoundException
from src.config import logger
from typing import List
from fastapi_pagination import Page, Params


router = APIRouter(
    prefix="/api/leads",
    tags=["leads"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=leads_schema.LeadOut)
def create_lead(lead: leads_schema.LeadCreate, db: Session = Depends(get_db)):
    manager = LeadsManager(db)
    return manager.create_lead(lead)
    


@router.get("/", response_model=Page[leads_schema.LeadOut])
def read_leads(db: Session = Depends(get_db), params: Params = Depends()):
    manager = LeadsManager(db)
    return manager.get_leads(params)
    


@router.get("/{lead_id}", response_model=leads_schema.LeadOut)
def read_lead(lead_id: int, db: Session = Depends(get_db)):
        manager = LeadsManager(db)
        return manager.get_lead(lead_id)
    
    