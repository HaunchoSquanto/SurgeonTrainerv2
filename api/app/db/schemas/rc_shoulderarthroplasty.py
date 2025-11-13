"""
Shoulder Arthroplasty Surgical schemas - Pydantic models for API request/response validation
"""

from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, Literal


class RcShoulderArthroplastySurgicalBase(BaseModel):
    """Base Shoulder Arthroplasty surgical fields (research-focused)"""
    encounter_id: int

    # Core case metadata
    fellow_or_pa: Optional[str] = None
    attending: Optional[str] = None
    mrn: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[date] = None
    surgery_date: Optional[date] = None
    laterality: Optional[Literal["Right", "Left", "Bilateral"]] = None
    
    # Surgical Approach
    approach: Optional[str] = None  # anterior/posterior/lateral/other
    
    # Implant Details
    implant_manufacturer: Optional[str] = None
    implant_system: Optional[str] = None
    cup_type: Optional[str] = None  # Acetabular cup type
    cup_size: Optional[int] = None  # Cup diameter in mm
    cup_fixation: Optional[str] = None  # cemented/uncemented/hybrid
    stem_type: Optional[str] = None
    stem_size: Optional[int] = None
    stem_fixation: Optional[str] = None  # cemented/uncemented
    head_size: Optional[int] = None  # Femoral head size in mm
    neck_length: Optional[str] = None  # short/medium/long/extra-long
    bearing_surface: Optional[str] = None  # e.g., ceramic-on-polyethylene
    
    # Clinical Details
    primary_diagnosis: Optional[str] = None  # OA/AVN/fracture/etc
    bone_quality: Optional[str] = None  # good/fair/poor/osteoporotic
    previous_surgery: Optional[bool] = None  # Prior hip surgery on same side
    
    # Intraoperative
    leg_length_change_mm: Optional[int] = None  # Positive=lengthened, negative=shortened
    complications_intraop: Optional[str] = None
    
    # Postoperative
    complications_postop: Optional[str] = None
    length_of_stay_days: Optional[int] = None
    discharge_disposition: Optional[str] = None  # home/SNF/rehab/etc
    
    # Notes
    notes: Optional[str] = None


class RcShoulderArthroplastySurgicalCreate(RcShoulderArthroplastySurgicalBase):
    """Schema for creating a new Shoulder Arthroplasty surgical case"""
    pass


class RcShoulderArthroplastySurgicalUpdate(BaseModel):
    """Schema for updating a Shoulder Arthroplasty surgical case - all fields optional"""
    
    fellow_or_pa: Optional[str] = None
    attending: Optional[str] = None
    mrn: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[date] = None
    surgery_date: Optional[date] = None
    laterality: Optional[str] = None
    
    approach: Optional[str] = None
    
    implant_manufacturer: Optional[str] = None
    implant_system: Optional[str] = None
    cup_type: Optional[str] = None
    cup_size: Optional[int] = None
    cup_fixation: Optional[str] = None
    stem_type: Optional[str] = None
    stem_size: Optional[int] = None
    stem_fixation: Optional[str] = None
    head_size: Optional[int] = None
    neck_length: Optional[str] = None
    bearing_surface: Optional[str] = None
    
    primary_diagnosis: Optional[str] = None
    bone_quality: Optional[str] = None
    previous_surgery: Optional[bool] = None
    
    leg_length_change_mm: Optional[int] = None
    complications_intraop: Optional[str] = None
    
    complications_postop: Optional[str] = None
    length_of_stay_days: Optional[int] = None
    discharge_disposition: Optional[str] = None
    
    notes: Optional[str] = None


class RcShoulderArthroplastySurgicalResponse(RcShoulderArthroplastySurgicalBase):
    """Schema for Shoulder Arthroplasty API response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

