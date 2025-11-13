"""
Knee Arthroplasty Surgical schemas - Pydantic models for API request/response validation
"""

from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, Literal


class RcKneeArthroplastySurgicalBase(BaseModel):
    """Base knee arthroplasty surgical fields (research-focused)"""
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
    
    # Procedure Type
    procedure_type: Optional[str] = None  # TKA/UKA/Revision TKA/Revision UKA/Patellofemoral
    
    # Surgical Approach
    approach: Optional[str] = None  # medial parapatellar/subvastus/midvastus/lateral
    
    # Implant Details
    implant_manufacturer: Optional[str] = None
    implant_system: Optional[str] = None
    femoral_component_size: Optional[str] = None
    tibial_component_size: Optional[str] = None
    patella_resurfaced: Optional[bool] = None
    patellar_component_size: Optional[str] = None
    poly_insert_thickness: Optional[int] = None  # in mm
    
    # Fixation
    fixation_type: Optional[str] = None  # cemented/uncemented/hybrid
    
    # Alignment & Technique
    alignment_technique: Optional[str] = None  # mechanical/kinematic/adjusted mechanical
    navigation_used: Optional[bool] = None
    robotics_used: Optional[bool] = None
    
    # Ligament Management
    pcl_retained: Optional[bool] = None  # Posterior cruciate ligament
    pcl_substituting: Optional[bool] = None
    
    # Constraint Level
    constraint_level: Optional[str] = None  # CR/PS/CCK/hinge
    
    # Augments & Stems
    augments_used: Optional[bool] = None
    augment_details: Optional[str] = None
    stems_used: Optional[bool] = None
    stem_details: Optional[str] = None
    
    # Clinical Details
    primary_diagnosis: Optional[str] = None  # OA/RA/post-traumatic/AVN/etc
    bone_quality: Optional[str] = None  # good/fair/poor/osteoporotic
    previous_surgery: Optional[bool] = None
    
    # Intraoperative
    complications_intraop: Optional[str] = None
    
    # Postoperative
    complications_postop: Optional[str] = None
    length_of_stay_days: Optional[int] = None
    discharge_disposition: Optional[str] = None  # home/SNF/rehab/etc
    
    # Notes
    notes: Optional[str] = None


class RcKneeArthroplastySurgicalCreate(RcKneeArthroplastySurgicalBase):
    """Schema for creating a new knee arthroplasty surgical case"""
    pass


class RcKneeArthroplastySurgicalUpdate(BaseModel):
    """Schema for updating a knee arthroplasty surgical case - all fields optional"""
    
    fellow_or_pa: Optional[str] = None
    attending: Optional[str] = None
    mrn: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[date] = None
    surgery_date: Optional[date] = None
    laterality: Optional[str] = None
    
    procedure_type: Optional[str] = None
    approach: Optional[str] = None
    
    implant_manufacturer: Optional[str] = None
    implant_system: Optional[str] = None
    femoral_component_size: Optional[str] = None
    tibial_component_size: Optional[str] = None
    patella_resurfaced: Optional[bool] = None
    patellar_component_size: Optional[str] = None
    poly_insert_thickness: Optional[int] = None
    
    fixation_type: Optional[str] = None
    
    alignment_technique: Optional[str] = None
    navigation_used: Optional[bool] = None
    robotics_used: Optional[bool] = None
    
    pcl_retained: Optional[bool] = None
    pcl_substituting: Optional[bool] = None
    
    constraint_level: Optional[str] = None
    
    augments_used: Optional[bool] = None
    augment_details: Optional[str] = None
    stems_used: Optional[bool] = None
    stem_details: Optional[str] = None
    
    primary_diagnosis: Optional[str] = None
    bone_quality: Optional[str] = None
    previous_surgery: Optional[bool] = None
    
    complications_intraop: Optional[str] = None
    
    complications_postop: Optional[str] = None
    length_of_stay_days: Optional[int] = None
    discharge_disposition: Optional[str] = None
    
    notes: Optional[str] = None


class RcKneeArthroplastySurgicalResponse(RcKneeArthroplastySurgicalBase):
    """Schema for knee arthroplasty API response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
