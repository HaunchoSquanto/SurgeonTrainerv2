"""
Hip Arthroplasty research case model
"""
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, datetime


class RcHipArthroplasty(SQLModel, table=True):
    """Hip arthroplasty (replacement) research data"""
    __tablename__ = "rc_hiparthroplasty"
    
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
    laterality: Optional[str] = Field(default=None, max_length=20, description="Right/Left/Bilateral")
    
    # Surgical Approach
    approach: Optional[str] = Field(default=None, max_length=50, description="anterior/posterior/lateral/other")
    
    # Implant Details
    implant_manufacturer: Optional[str] = Field(default=None, max_length=100)
    implant_system: Optional[str] = Field(default=None, max_length=100)
    cup_type: Optional[str] = Field(default=None, max_length=100, description="Acetabular cup type")
    cup_size: Optional[int] = Field(default=None, description="Cup diameter in mm")
    cup_fixation: Optional[str] = Field(default=None, max_length=50, description="cemented/uncemented/hybrid")
    stem_type: Optional[str] = Field(default=None, max_length=100)
    stem_size: Optional[int] = Field(default=None, description="Stem size")
    stem_fixation: Optional[str] = Field(default=None, max_length=50, description="cemented/uncemented")
    head_size: Optional[int] = Field(default=None, description="Femoral head size in mm")
    neck_length: Optional[str] = Field(default=None, max_length=50, description="short/medium/long/extra-long")
    bearing_surface: Optional[str] = Field(default=None, max_length=100, description="e.g., ceramic-on-polyethylene")
    
    # Clinical Details
    primary_diagnosis: Optional[str] = Field(default=None, max_length=255, description="OA/AVN/fracture/etc")
    bone_quality: Optional[str] = Field(default=None, max_length=50, description="good/fair/poor/osteoporotic")
    previous_surgery: Optional[bool] = Field(default=None, description="Prior hip surgery on same side")
    
    # Intraoperative
    leg_length_change_mm: Optional[int] = Field(default=None, description="Positive=lengthened, negative=shortened")
    complications_intraop: Optional[str] = Field(default=None, description="Intraoperative complications")
    
    # Postoperative
    complications_postop: Optional[str] = Field(default=None, description="Postoperative complications")
    length_of_stay_days: Optional[int] = Field(default=None)
    discharge_disposition: Optional[str] = Field(default=None, max_length=100, description="home/SNF/rehab/etc")
    
    # Notes
    notes: Optional[str] = Field(default=None, description="Additional case notes")
    
    # System Fields
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
