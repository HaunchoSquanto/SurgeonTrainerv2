"""
Shoulder Arthroscopy research case model
"""
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, datetime


class RcShoulderScope(SQLModel, table=True):
    """Shoulder arthroscopy research data"""
    __tablename__ = "rc_shoulderscope"
    
    # Primary Key
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Foreign Key
    encounter_id: int = Field(foreign_key="encounter.id", index=True, unique=True)
    
    # Core Case Metadata
    fellow_or_pa: Optional[str] = Field(default=None, max_length=100)
    attending: Optional[str] = Field(default=None, max_length=100)
    mrn: Optional[str] = Field(default=None, max_length=50)
    first_name: Optional[str] = Field(default=None, max_length=100)
    last_name: Optional[str] = Field(default=None, max_length=100)
    dob: Optional[date] = Field(default=None)
    surgery_date: Optional[date] = Field(default=None)
    laterality: Optional[str] = Field(default=None, max_length=20, description="Right/Left")
    procedure_type: Optional[str] = Field(default=None, max_length=50, description="Primary/Revision")
    
    # Analgesic (checkbox style)
    analgesic_brachial_plexus_catheter: Optional[bool] = Field(default=None)
    analgesic_brachial_plexus_single_shot: Optional[bool] = Field(default=None)
    analgesic_suprascap_nerve_block_with_local: Optional[bool] = Field(default=None)
    
    # High-level procedures done
    instability_done: Optional[bool] = Field(default=None)
    capsular_release_done: Optional[bool] = Field(default=None)
    ac_reconstruction_done: Optional[bool] = Field(default=None)
    
    # Instability details
    instability_anterior: Optional[bool] = Field(default=None)
    instability_posterior: Optional[bool] = Field(default=None)
    instability_superior: Optional[bool] = Field(default=None)
    instability_num_anchors: Optional[int] = Field(default=None)
    
    glenoid_bone_loss_present: Optional[bool] = Field(default=None)
    glenoid_bone_loss_estimated_percent: Optional[float] = Field(default=None, description="Percent bone loss")
    
    hill_sachs_present: Optional[bool] = Field(default=None)
    hill_sachs_treatment: Optional[str] = Field(default=None, max_length=255)
    
    mdi_present: Optional[bool] = Field(default=None, description="Multidirectional instability")
    rotator_interval_closed: Optional[bool] = Field(default=None)
    
    # Capsular release details (checkboxes)
    capsular_release_ri: Optional[bool] = Field(default=None, description="Rotator interval")
    capsular_release_mghl: Optional[bool] = Field(default=None, description="Middle glenohumeral ligament")
    capsular_release_ighl: Optional[bool] = Field(default=None, description="Inferior glenohumeral ligament")
    
    # EUA ROM (degrees)
    eua_performed: Optional[bool] = Field(default=None, description="Exam under anesthesia")
    eua_abduction_deg: Optional[float] = Field(default=None)
    eua_forward_flexion_deg: Optional[float] = Field(default=None)
    eua_er_at_side_deg: Optional[float] = Field(default=None, description="External rotation at side")
    eua_er_at_90_deg: Optional[float] = Field(default=None, description="External rotation at 90 degrees")
    eua_ir_at_90_deg: Optional[float] = Field(default=None, description="Internal rotation at 90 degrees")
    
    # Concomitant lesions (global, instability section)
    concomitant_lesions_present: Optional[bool] = Field(default=None)
    concomitant_lesions_treatment: Optional[str] = Field(default=None)
    
    # AC Reconstruction details
    ac_reconstruction_details: Optional[str] = Field(default=None)
    ac_weeks_from_injury: Optional[float] = Field(default=None)
    ac_graft_added: Optional[bool] = Field(default=None)
    
    ac_concomitant_lesion_present: Optional[bool] = Field(default=None)
    ac_concomitant_lesion_treatment: Optional[str] = Field(default=None)
    ac_augmentation_done: Optional[bool] = Field(default=None)
    
    ac_technique_notes: Optional[str] = Field(default=None)
    
    # Other procedures (binary)
    bar_done: Optional[bool] = Field(default=None, description="Bursectomy/acromioplasty/release")
    sad_done: Optional[bool] = Field(default=None, description="Subacromial decompression")
    dce_done: Optional[bool] = Field(default=None, description="Distal clavicle excision")
    biceps_procedure_done: Optional[bool] = Field(default=None)
    
    # Biceps details
    biceps_treatment_type: Optional[str] = Field(default=None, max_length=50, description="Tenotomy/Tenodesis")
    biceps_num_anchors: Optional[int] = Field(default=None)
    biceps_anchor_size_mm: Optional[float] = Field(default=None)
    biceps_screw_size_mm: Optional[float] = Field(default=None)
    biceps_location: Optional[str] = Field(default=None, max_length=100)
    biceps_onlay_vs_inlay: Optional[str] = Field(default=None, max_length=20, description="Onlay/Inlay")
    
    # Free text
    other_comments: Optional[str] = Field(default=None)
    
    # System Fields
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
