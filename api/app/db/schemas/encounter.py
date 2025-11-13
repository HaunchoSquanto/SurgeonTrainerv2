"""
Encounter schemas - Pydantic models for API request/response validation
"""
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class EncounterBase(BaseModel):
    """Base encounter fields"""
    patient_id: int
    encounter_type: str
    encounter_date: date
    encounter_end_date: Optional[date] = None
    chief_complaint: Optional[str] = None
    location: Optional[str] = None
    attending_physician: Optional[str] = None
    referring_physician: Optional[str] = None
    status: str = "active"
    notes: Optional[str] = None


class EncounterCreate(EncounterBase):
    """Schema for creating a new encounter"""
    pass


class EncounterUpdate(BaseModel):
    """Schema for updating encounter - all fields optional"""
    encounter_type: Optional[str] = None
    encounter_date: Optional[date] = None
    encounter_end_date: Optional[date] = None
    chief_complaint: Optional[str] = None
    location: Optional[str] = None
    attending_physician: Optional[str] = None
    referring_physician: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class EncounterResponse(EncounterBase):
    """Schema for encounter API response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
