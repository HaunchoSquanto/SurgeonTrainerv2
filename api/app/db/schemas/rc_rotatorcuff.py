"""
Rotator Cuff schemas - Pydantic models for API request/response validation
"""
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, Literal


class RcRotatorCuffBase(BaseModel):
    """Base rotator cuff fields"""
    encounter_id: int
    fellow_or_pa: Optional[str] = None
    attending: Optional[str] = None
    mrn: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[date] = None
    date_of_surgery: Optional[date] = None
    laterality: Optional[Literal["Right", "Left", "Bilateral"]] = None
    tear_type: Optional[str] = None
    procedure_type: Optional[Literal["Primary", "Revision"]] = None
    
    # Subscapularis details
    subscap_tear_present: Optional[bool] = None
    subscap_repair_performed: Optional[bool] = None
    subscap_tissue_quality: Optional[str] = None
    subscap_lafosse_type: Optional[Literal["1", "2", "3", "4", "5"]] = None
    biceps_sling_injury_or_instability: Optional[bool] = None
    subscap_repair_technique: Optional[str] = None
    coracoplasty_performed: Optional[bool] = None
    
    # Tendons torn
    supraspinatus_torn: Optional[bool] = None
    infraspinatus_torn: Optional[bool] = None
    subscapularis_torn: Optional[bool] = None
    teres_minor_torn: Optional[bool] = None
    
    # Muscle quality
    goutallier_supraspinatus: Optional[int] = None
    goutallier_infraspinatus: Optional[int] = None
    goutallier_subscapularis: Optional[int] = None
    goutallier_teres_minor: Optional[int] = None
    
    # Tear characteristics
    tear_size_ap_cm: Optional[float] = None
    retraction_amount: Optional[str] = None
    
    # Repair details
    anchor_manufacturer: Optional[str] = None
    num_rotator_cuff_anchors: Optional[int] = None
    transosseous_tunnels_used: Optional[int] = None
    repair_construct: Optional[str] = None
    
    # Biologic Augmentation
    patch_used_regeneten: Optional[bool] = None
    patch_used_allograft_augmentation: Optional[bool] = None
    patch_used_biceps_patch: Optional[bool] = None
    num_patches_used: Optional[int] = None
    patch_manufacturer: Optional[str] = None
    
    # Superior capsule reconstruction
    scr_performed: Optional[bool] = None
    scr_allograft_dermis_used: Optional[bool] = None
    scr_autograft_fascia_lata_used: Optional[bool] = None
    scr_biceps_used: Optional[bool] = None
    num_glenoid_anchors: Optional[int] = None
    num_humeral_anchors: Optional[int] = None
    posterior_margin_convergence_done: Optional[bool] = None
    anterior_margin_convergence_done: Optional[bool] = None
    graft_thickness_mm: Optional[float] = None
    
    # Additional procedures and OA
    hamada_classification: Optional[int] = None
    chondromalacia_grade: Optional[Literal["1", "2", "3", "4a", "4b", "5"]] = None
    superior_labrum_treatment: Optional[str] = None
    
    # Acromioplasty and distal clavicle
    bar_performed: Optional[bool] = None
    sad_performed: Optional[bool] = None
    dce_performed: Optional[bool] = None
    biceps_procedure_performed: Optional[bool] = None
    
    # Biceps tendon
    biceps_technique: Optional[str] = None
    num_biceps_anchors: Optional[int] = None
    biceps_anchor_size_mm: Optional[float] = None
    biceps_screw_size_mm: Optional[float] = None
    biceps_location: Optional[str] = None
    biceps_onlay_vs_inlay: Optional[Literal["Onlay", "Inlay"]] = None
    
    # Muscle/tendon transfers
    lower_trap_transfer_performed: Optional[bool] = None
    other_tendon_transfer_performed: Optional[bool] = None
    other_tendon_transfer_details: Optional[str] = None
    
    # Capsular releases
    ri_release_performed: Optional[bool] = None
    mghl_release_performed: Optional[bool] = None
    ighl_release_performed: Optional[bool] = None
    
    # Anesthesia
    analgesia_technique: Optional[Literal[
        "Brachial plexus catheter",
        "Brachial plexus single shot",
        "Suprascap nerve block with local infiltration"
    ]] = None
    
    other_comments: Optional[str] = None


class RcRotatorCuffCreate(RcRotatorCuffBase):
    """Schema for creating a new rotator cuff case"""
    pass


class RcRotatorCuffUpdate(BaseModel):
    """Schema for updating rotator cuff - all fields optional"""
    fellow_or_pa: Optional[str] = None
    attending: Optional[str] = None
    mrn: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[date] = None
    date_of_surgery: Optional[date] = None
    laterality: Optional[Literal["Right", "Left", "Bilateral"]] = None
    tear_type: Optional[Literal["Partial", "Complete"]] = None
    procedure_type: Optional[Literal["Primary", "Revision"]] = None
    subscap_tear_present: Optional[bool] = None
    subscap_repair_performed: Optional[bool] = None
    subscap_tissue_quality: Optional[str] = None
    subscap_lafosse_type: Optional[Literal["1", "2", "3", "4", "5"]] = None
    biceps_sling_injury_or_instability: Optional[bool] = None
    subscap_repair_technique: Optional[str] = None
    coracoplasty_performed: Optional[bool] = None
    supraspinatus_torn: Optional[bool] = None
    infraspinatus_torn: Optional[bool] = None
    subscapularis_torn: Optional[bool] = None
    teres_minor_torn: Optional[bool] = None
    goutallier_supraspinatus: Optional[int] = None
    goutallier_infraspinatus: Optional[int] = None
    goutallier_subscapularis: Optional[int] = None
    goutallier_teres_minor: Optional[int] = None
    tear_size_ap_cm: Optional[float] = None
    retraction_amount: Optional[str] = None
    anchor_manufacturer: Optional[str] = None
    num_rotator_cuff_anchors: Optional[int] = None
    transosseous_tunnels_used: Optional[int] = None
    repair_construct: Optional[str] = None
    patch_used_regeneten: Optional[bool] = None
    patch_used_allograft_augmentation: Optional[bool] = None
    patch_used_biceps_patch: Optional[bool] = None
    num_patches_used: Optional[int] = None
    patch_manufacturer: Optional[str] = None
    scr_performed: Optional[bool] = None
    scr_allograft_dermis_used: Optional[bool] = None
    scr_autograft_fascia_lata_used: Optional[bool] = None
    scr_biceps_used: Optional[bool] = None
    num_glenoid_anchors: Optional[int] = None
    num_humeral_anchors: Optional[int] = None
    posterior_margin_convergence_done: Optional[bool] = None
    anterior_margin_convergence_done: Optional[bool] = None
    graft_thickness_mm: Optional[float] = None
    hamada_classification: Optional[int] = None
    chondromalacia_grade: Optional[str] = None
    superior_labrum_treatment: Optional[str] = None
    bar_performed: Optional[bool] = None
    sad_performed: Optional[bool] = None
    dce_performed: Optional[bool] = None
    biceps_procedure_performed: Optional[bool] = None
    biceps_technique: Optional[str] = None
    num_biceps_anchors: Optional[int] = None
    biceps_anchor_size_mm: Optional[float] = None
    biceps_screw_size_mm: Optional[float] = None
    biceps_location: Optional[str] = None
    biceps_onlay_vs_inlay: Optional[Literal["Onlay", "Inlay"]] = None
    lower_trap_transfer_performed: Optional[bool] = None
    other_tendon_transfer_performed: Optional[bool] = None
    other_tendon_transfer_details: Optional[str] = None
    ri_release_performed: Optional[bool] = None
    mghl_release_performed: Optional[bool] = None
    ighl_release_performed: Optional[bool] = None
    analgesia_technique: Optional[str] = None
    other_comments: Optional[str] = None


class RcRotatorCuffResponse(RcRotatorCuffBase):
    """Schema for rotator cuff API response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
