"""
Shoulder Arthroplasty research case model
"""
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, datetime


class RcShoulderArthroplasty(SQLModel, table=True):
    """Shoulder arthroplasty research data"""
    __tablename__ = "rc_shoulderarthroplasty"
    
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
    laterality: Optional[str] = Field(default=None, max_length=20, description="Right/Left")
    primary_revision: Optional[str] = Field(default=None, max_length=20, description="Primary/Revision")
    
    # Indication for arthroplasty (primary)
    indication_for_arthroplasty: Optional[str] = Field(
        default=None, 
        max_length=100,
        description="Cuff tear arthropathy/Massive cuff tear/Primary osteoarthritis/Fracture/Malunion/AVN"
    )
    
    # Arthroplasty type
    arthroplasty_type: Optional[str] = Field(
        default=None, 
        max_length=50, 
        description="Anatomic/Reverse/Hemiarthroplasty"
    )
    
    # Implant (free text – vendor/system)
    implant: Optional[str] = Field(default=None, max_length=255)
    
    # Skin prep
    prep_hydrogen_peroxide: Optional[bool] = Field(default=None)
    prep_chloroprep: Optional[bool] = Field(default=None)
    prep_betadine: Optional[bool] = Field(default=None)
    
    # Pre-op wash
    preop_benzoyl_peroxide: Optional[bool] = Field(default=None)
    preop_hibiclens: Optional[bool] = Field(default=None)
    
    # Intra-op betadine wash
    betadine_wash_intraop: Optional[bool] = Field(default=None)
    
    # Subscap approach
    subscap_approach: Optional[str] = Field(
        default=None, 
        max_length=50, 
        description="Tenotomy/Peel/LTO"
    )
    
    # Stem length
    stem_length: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Stemless/Short/Standard/Revision long stem/Fracture stem"
    )
    
    # Glenoid augment (global)
    glenoid_augment_used: Optional[bool] = Field(default=None)
    
    # Anesthesia details (free text)
    anesthesia_details: Optional[str] = Field(default=None)
    
    # Arthrex registry flag (global)
    arthrex_registry_patient: Optional[bool] = Field(default=None)
    
    # REVERSE-SPECIFIC DETAILS
    
    # Reverse fixation
    reverse_fixation: Optional[str] = Field(default=None, max_length=50, description="Cement/Pressfit")
    
    # Indications for reverse (checkboxes)
    reverse_indication_fracture: Optional[bool] = Field(default=None)
    reverse_indication_arthritis: Optional[bool] = Field(default=None)
    reverse_indication_rotator_cuff_arthropathy: Optional[bool] = Field(default=None)
    reverse_indication_massive_irreparable_cuff_tear: Optional[bool] = Field(default=None)
    reverse_indication_failed_tsa_rsa: Optional[bool] = Field(default=None)
    reverse_indication_instability: Optional[bool] = Field(default=None)
    reverse_indication_infection: Optional[bool] = Field(default=None)
    reverse_indication_aseptic_loosening: Optional[bool] = Field(default=None)
    reverse_indication_mechanical_complication: Optional[bool] = Field(default=None)
    reverse_indication_other: Optional[bool] = Field(default=None)
    reverse_indication_other_details: Optional[str] = Field(default=None)
    
    # Suture details (tuberosity reconstruction / repair pattern)
    suture_tuberosities_to_humeral_shaft_vertical: Optional[bool] = Field(default=None)
    suture_tuberosities_to_stem_horizontal: Optional[bool] = Field(default=None)
    suture_lt_to_gt: Optional[bool] = Field(default=None, description="Lesser to greater tuberosity")
    suture_cerclage_tuberosities_around_shell: Optional[bool] = Field(default=None)
    
    # Glenoid offset (mm)
    glenoid_offset_mm: Optional[float] = Field(default=None)
    
    # Screw / cage details (free text)
    screw_cage_details: Optional[str] = Field(default=None)
    
    # Screw counts
    num_peripheral_screws: Optional[int] = Field(default=None)
    num_bicortical_screws: Optional[int] = Field(default=None)
    num_unicortical_screws: Optional[int] = Field(default=None)
    
    # Implant sizes
    glenosphere_size_mm: Optional[float] = Field(default=None)
    poly_liner_size_mm: Optional[float] = Field(default=None, description="Polyethylene liner size")
    
    # Superior screw, augmented baseplate
    superior_screw_used: Optional[bool] = Field(default=None)
    augmented_baseplate_used: Optional[bool] = Field(default=None)
    
    # Subscap repair status
    subscap_repaired: Optional[bool] = Field(default=None)
    
    # Optional future: Glenoid-specific notes
    glenoid_notes: Optional[str] = Field(default=None)
    
    # System Fields
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
