"""
Other Procedures research case model - catch-all for procedures not in specific categories
"""
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, datetime


class RcOther(SQLModel, table=True):
    """Other procedures research data (catch-all)"""
    __tablename__ = "rc_other"
    
    # Primary Key
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Foreign Key
    encounter_id: int = Field(foreign_key="encounter.id", index=True, unique=True)
    
    # Core case metadata
    fellow_or_pa: Optional[str] = Field(default=None, max_length=100)
    attending: Optional[str] = Field(default=None, max_length=100)
    mrn: Optional[str] = Field(default=None, max_length=50)
    first_name: Optional[str] = Field(default=None, max_length=100)
    last_name: Optional[str] = Field(default=None, max_length=100)
    dob: Optional[date] = Field(default=None)
    surgery_date: Optional[date] = Field(default=None)
    laterality: Optional[str] = Field(default=None, max_length=20, description="Right/Left/Bilateral/N/A")
    
    # Procedure Category
    procedure_category: Optional[str] = Field(default=None, max_length=100, description="Spine/Trauma/Pediatric/Foot-Ankle/Hand/etc")
    
    # Procedure Details
    procedure_name: Optional[str] = Field(default=None, max_length=255)
    procedure_description: Optional[str] = Field(default=None)
    
    # Surgical Details
    approach: Optional[str] = Field(default=None, max_length=100)
    anesthesia_type: Optional[str] = Field(default=None, max_length=100)
    
    # Implants/Hardware
    implants_used: Optional[bool] = Field(default=None)
    implant_details: Optional[str] = Field(default=None)
    
    # Clinical Details
    primary_diagnosis: Optional[str] = Field(default=None, max_length=255)
    previous_surgery: Optional[bool] = Field(default=None)
    
    # Intraoperative
    complications_intraop: Optional[str] = Field(default=None)
    estimated_blood_loss_ml: Optional[int] = Field(default=None)
    
    # Postoperative
    complications_postop: Optional[str] = Field(default=None)
    length_of_stay_days: Optional[int] = Field(default=None)
    discharge_disposition: Optional[str] = Field(default=None, max_length=100)
    
    # Notes
    notes: Optional[str] = Field(default=None)
    
    # System Fields
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
