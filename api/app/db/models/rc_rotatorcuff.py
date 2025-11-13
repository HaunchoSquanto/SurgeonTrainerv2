"""
Rotator Cuff Repair research case model
"""
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, datetime


class RcRotatorCuff(SQLModel, table=True):
    """Rotator cuff repair research data"""
    __tablename__ = "rc_rotatorcuff"
    
    # Primary Key
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Foreign Key
    encounter_id: int = Field(foreign_key="encounter.id", index=True, unique=True)
    
    # Basic Case Info
    fellow_or_pa: Optional[str] = Field(default=None, max_length=100)
    attending: Optional[str] = Field(default=None, max_length=100)
    mrn: Optional[str] = Field(default=None, max_length=50)
    first_name: Optional[str] = Field(default=None, max_length=100)
    last_name: Optional[str] = Field(default=None, max_length=100)
    dob: Optional[date] = Field(default=None)
    date_of_surgery: Optional[date] = Field(default=None)
    laterality: Optional[str] = Field(default=None, max_length=20, description="Right/Left")
    tear_type: Optional[str] = Field(default=None, max_length=50, description="Partial/Complete")
    procedure_type: Optional[str] = Field(default=None, max_length=50, description="Primary/Revision")
    
    # Subscapularis Details
    subscap_tear_present: Optional[bool] = Field(default=None)
    subscap_repair_performed: Optional[bool] = Field(default=None)
    subscap_tissue_quality: Optional[str] = Field(default=None, max_length=20, description="good/fair/poor")
    subscap_lafosse_type: Optional[str] = Field(default=None, max_length=10, description="1/2/3/4/5")
    biceps_sling_injury_or_instability: Optional[bool] = Field(default=None)
    subscap_repair_technique: Optional[str] = Field(default=None, max_length=100)
    coracoplasty_performed: Optional[bool] = Field(default=None)
    
    # Tendons Torn
    supraspinatus_torn: Optional[bool] = Field(default=None)
    infraspinatus_torn: Optional[bool] = Field(default=None)
    subscapularis_torn: Optional[bool] = Field(default=None)
    teres_minor_torn: Optional[bool] = Field(default=None)
    
    # Muscle Quality (Goutallier)
    goutallier_supraspinatus: Optional[int] = Field(default=None)
    goutallier_infraspinatus: Optional[int] = Field(default=None)
    goutallier_subscapularis: Optional[int] = Field(default=None)
    goutallier_teres_minor: Optional[int] = Field(default=None)
    
    # Tear Characteristics
    tear_size_ap_cm: Optional[float] = Field(default=None, description="Anterior-posterior dimension in cm")
    retraction_amount: Optional[str] = Field(default=None, max_length=100)
    
    # Repair Details
    anchor_manufacturer: Optional[str] = Field(default=None, max_length=100)
    num_rotator_cuff_anchors: Optional[int] = Field(default=None)
    transosseous_tunnels_used: Optional[int] = Field(default=None)
    repair_construct: Optional[str] = Field(default=None, max_length=50, description="Single row/Double row/PASTA Repair")
    
    # Biologic Augmentation
    patch_used_regeneten: Optional[bool] = Field(default=None)
    patch_used_allograft_augmentation: Optional[bool] = Field(default=None)
    patch_used_biceps_patch: Optional[bool] = Field(default=None)
    num_patches_used: Optional[int] = Field(default=None)
    patch_manufacturer: Optional[str] = Field(default=None, max_length=100)
    
    # Superior Capsule Reconstruction
    scr_performed: Optional[bool] = Field(default=None)
    scr_allograft_dermis_used: Optional[bool] = Field(default=None)
    scr_autograft_fascia_lata_used: Optional[bool] = Field(default=None)
    scr_biceps_used: Optional[bool] = Field(default=None)
    num_glenoid_anchors: Optional[int] = Field(default=None)
    num_humeral_anchors: Optional[int] = Field(default=None)
    posterior_margin_convergence_done: Optional[bool] = Field(default=None)
    anterior_margin_convergence_done: Optional[bool] = Field(default=None)
    graft_thickness_mm: Optional[float] = Field(default=None)
    
    # Additional Procedures and OA
    hamada_classification: Optional[int] = Field(default=None)
    chondromalacia_grade: Optional[str] = Field(default=None, max_length=10, description="1/2/3/4a/4b/5")
    superior_labrum_treatment: Optional[str] = Field(default=None, max_length=50, description="Resection/Retained")
    
    # Acromioplasty and Distal Clavicle
    bar_performed: Optional[bool] = Field(default=None, description="Bursectomy/Acromioplasty/Release")
    sad_performed: Optional[bool] = Field(default=None, description="Subacromial Decompression")
    dce_performed: Optional[bool] = Field(default=None, description="Distal Clavicle Excision")
    biceps_procedure_performed: Optional[bool] = Field(default=None)
    
    # Biceps Tendon
    biceps_technique: Optional[str] = Field(default=None, max_length=50, description="Tenotomy/Tenodesis")
    num_biceps_anchors: Optional[int] = Field(default=None)
    biceps_anchor_size_mm: Optional[float] = Field(default=None)
    biceps_screw_size_mm: Optional[float] = Field(default=None)
    biceps_location: Optional[str] = Field(default=None, max_length=100)
    biceps_onlay_vs_inlay: Optional[str] = Field(default=None, max_length=20, description="Onlay/Inlay")
    
    # Muscle/Tendon Transfers
    lower_trap_transfer_performed: Optional[bool] = Field(default=None)
    other_tendon_transfer_performed: Optional[bool] = Field(default=None)
    other_tendon_transfer_details: Optional[str] = Field(default=None, max_length=500)
    
    # Capsular Releases
    ri_release_performed: Optional[bool] = Field(default=None, description="Rotator Interval")
    mghl_release_performed: Optional[bool] = Field(default=None, description="Middle Glenohumeral Ligament")
    ighl_release_performed: Optional[bool] = Field(default=None, description="Inferior Glenohumeral Ligament")
    
    # Anesthesia
    analgesia_technique: Optional[str] = Field(default=None, max_length=100)
    
    # Notes
    other_comments: Optional[str] = Field(default=None)
    
    # System Fields
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
