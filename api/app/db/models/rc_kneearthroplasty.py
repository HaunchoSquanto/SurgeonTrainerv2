"""
Knee Arthroplasty research case model
"""
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, datetime


class RcKneeArthroplasty(SQLModel, table=True):
    """Knee arthroplasty (replacement) research data"""
    __tablename__ = "rc_kneearthroplasty"
    
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
    
    # Procedure Type
    procedure_type: Optional[str] = Field(default=None, max_length=50, description="TKA/UKA/Revision TKA/Revision UKA/Patellofemoral")
    
    # Surgical Approach
    approach: Optional[str] = Field(default=None, max_length=100, description="medial parapatellar/subvastus/midvastus/lateral")
    
    # Implant Details
    implant_manufacturer: Optional[str] = Field(default=None, max_length=100)
    implant_system: Optional[str] = Field(default=None, max_length=100)
    femoral_component_size: Optional[str] = Field(default=None, max_length=50)
    tibial_component_size: Optional[str] = Field(default=None, max_length=50)
    patella_resurfaced: Optional[bool] = Field(default=None)
    patellar_component_size: Optional[str] = Field(default=None, max_length=50)
    poly_insert_thickness: Optional[int] = Field(default=None, description="Insert thickness in mm")
    
    # Fixation
    fixation_type: Optional[str] = Field(default=None, max_length=50, description="cemented/uncemented/hybrid")
    
    # Alignment & Technique
    alignment_technique: Optional[str] = Field(default=None, max_length=100, description="mechanical/kinematic/adjusted mechanical")
    navigation_used: Optional[bool] = Field(default=None)
    robotics_used: Optional[bool] = Field(default=None)
    
    # Ligament Management
    pcl_retained: Optional[bool] = Field(default=None, description="Posterior cruciate ligament")
    pcl_substituting: Optional[bool] = Field(default=None)
    
    # Constraint Level
    constraint_level: Optional[str] = Field(default=None, max_length=50, description="CR/PS/CCK/hinge")
    
    # Augments & Stems
    augments_used: Optional[bool] = Field(default=None)
    augment_details: Optional[str] = Field(default=None)
    stems_used: Optional[bool] = Field(default=None)
    stem_details: Optional[str] = Field(default=None)
    
    # Clinical Details
    primary_diagnosis: Optional[str] = Field(default=None, max_length=255, description="OA/RA/post-traumatic/AVN/etc")
    bone_quality: Optional[str] = Field(default=None, max_length=50, description="good/fair/poor/osteoporotic")
    previous_surgery: Optional[bool] = Field(default=None)
    
    # Intraoperative
    complications_intraop: Optional[str] = Field(default=None)
    
    # Postoperative
    complications_postop: Optional[str] = Field(default=None)
    length_of_stay_days: Optional[int] = Field(default=None)
    discharge_disposition: Optional[str] = Field(default=None, max_length=100, description="home/SNF/rehab/etc")
    
    # Notes
    notes: Optional[str] = Field(default=None)
    
    # System Fields
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
