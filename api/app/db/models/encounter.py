"""
Encounter model - Tracks patient visits/admissions
"""
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, datetime


class Encounter(SQLModel, table=True):
    """Patient encounter/visit record"""
    __tablename__ = "encounter"
    
    # Primary Key
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Foreign Keys
    patient_id: int = Field(foreign_key="patient.id", index=True)
    
    # Encounter Details
    encounter_type: str = Field(max_length=50, description="outpatient/surgery/admission/emergency")
    encounter_date: date
    encounter_end_date: Optional[date] = Field(default=None, description="Discharge date if applicable")
    
    # Clinical Information
    chief_complaint: Optional[str] = Field(default=None, description="Primary reason for visit")
    location: Optional[str] = Field(default=None, max_length=100, description="Facility/department")
    attending_physician: Optional[str] = Field(default=None, max_length=100)
    referring_physician: Optional[str] = Field(default=None, max_length=100)
    
    # Status
    status: str = Field(default="active", max_length=50, description="active/completed/cancelled")
    
    # Notes
    notes: Optional[str] = Field(default=None, description="Additional encounter notes")
    
    # System Fields
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
