"""
Procedure model - CPT coded procedures linked to encounters
"""
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, datetime


class Procedure(SQLModel, table=True):
    """Procedure record with CPT coding"""
    __tablename__ = "procedure"
    
    # Primary Key
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Foreign Keys
    encounter_id: int = Field(foreign_key="encounter.id", index=True)
    
    # Procedure Details
    cpt_code: str = Field(max_length=10, index=True, description="CPT procedure code")
    procedure_description: str = Field(max_length=255, description="Human-readable procedure name")
    
    # Clinical Details
    procedure_date: date
    laterality: Optional[str] = Field(default=None, max_length=20, description="left/right/bilateral/N/A")
    surgeon: Optional[str] = Field(default=None, max_length=100)
    assistant_surgeon: Optional[str] = Field(default=None, max_length=100)
    anesthesia_type: Optional[str] = Field(default=None, max_length=50)
    
    # Duration and Location
    duration_minutes: Optional[int] = Field(default=None, description="Procedure duration")
    location: Optional[str] = Field(default=None, max_length=100, description="OR/clinic/etc")
    
    # Outcomes
    complications: Optional[str] = Field(default=None, description="Any complications during procedure")
    estimated_blood_loss_ml: Optional[int] = Field(default=None)
    
    # Notes
    operative_report: Optional[str] = Field(default=None, description="Full operative report text")
    notes: Optional[str] = Field(default=None, description="Additional procedure notes")
    
    # System Fields
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
