"""
Procedure schemas - Pydantic models for API request/response validation
"""
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class ProcedureBase(BaseModel):
    """Base procedure fields"""
    encounter_id: int
    cpt_code: str
    procedure_description: str
    procedure_date: date
    laterality: Optional[str] = None
    surgeon: Optional[str] = None
    assistant_surgeon: Optional[str] = None
    anesthesia_type: Optional[str] = None
    duration_minutes: Optional[int] = None
    location: Optional[str] = None
    complications: Optional[str] = None
    estimated_blood_loss_ml: Optional[int] = None
    operative_report: Optional[str] = None
    notes: Optional[str] = None


class ProcedureCreate(ProcedureBase):
    """Schema for creating a new procedure"""
    pass


class ProcedureUpdate(BaseModel):
    """Schema for updating procedure - all fields optional"""
    cpt_code: Optional[str] = None
    procedure_description: Optional[str] = None
    procedure_date: Optional[date] = None
    laterality: Optional[str] = None
    surgeon: Optional[str] = None
    assistant_surgeon: Optional[str] = None
    anesthesia_type: Optional[str] = None
    duration_minutes: Optional[int] = None
    location: Optional[str] = None
    complications: Optional[str] = None
    estimated_blood_loss_ml: Optional[int] = None
    operative_report: Optional[str] = None
    notes: Optional[str] = None


class ProcedureResponse(ProcedureBase):
    """Schema for procedure API response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
