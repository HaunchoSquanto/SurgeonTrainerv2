"""
Hip Arthroscopy research case model
"""
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, datetime


class RcHipScope(SQLModel, table=True):
    """Hip arthroscopy research data"""
    __tablename__ = "rc_hipscope"
    
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
    
    # Laterality
    laterality: Optional[str] = Field(default=None, max_length=20, description="Right/Left")
    
    # Position
    position: Optional[str] = Field(default=None, max_length=20, description="Post/Postless")
    
    # Anesthesia & traction
    traction_time_min: Optional[float] = Field(default=None)
    anesthesia_details: Optional[str] = Field(default=None)
    
    # FAI / LABRUM SECTION
    fai_labrum_case_present: Optional[bool] = Field(default=None)
    fai_labrum_primary_or_revision: Optional[str] = Field(default=None, max_length=20, description="Primary/Revision")
    
    # Diagnosis
    fai_labrum_diagnosis: Optional[str] = Field(default=None, max_length=50, description="FAI/Hip Dysplasia")
    
    # Procedures (checkboxes)
    fai_labrum_repaired: Optional[bool] = Field(default=None)
    fai_labrum_debridement: Optional[bool] = Field(default=None)
    fai_labrum_reconstruction: Optional[bool] = Field(default=None)
    fai_cam_resection_done: Optional[bool] = Field(default=None)
    fai_pincer_resection_done: Optional[bool] = Field(default=None)
    
    # Cartilage
    fai_chondromalacia_grade: Optional[str] = Field(default=None, max_length=50)
    fai_unstable_cartilage_width_mm: Optional[float] = Field(default=None)
    
    # Capsulotomy
    fai_capsulotomy_type: Optional[str] = Field(default=None, max_length=50, description="Interportal/T-type")
    fai_capsule_repaired: Optional[str] = Field(default=None, max_length=50, description="Yes/No/Only T-type")
    
    # Anchors (labral)
    fai_num_anchors: Optional[int] = Field(default=None)
    fai_anchor_brand: Optional[str] = Field(default=None, max_length=100)
    fai_anchor_type: Optional[str] = Field(default=None, max_length=100)
    
    # Iliopsoas
    iliopsoas_released: Optional[bool] = Field(default=None)
    
    # GLUTEUS REPAIRS SECTION
    gluteus_repairs_case_present: Optional[bool] = Field(default=None)
    gluteus_primary_or_revision: Optional[str] = Field(default=None, max_length=20, description="Primary/Revision")
    
    gluteus_approach: Optional[str] = Field(default=None, max_length=50, description="Arthroscopic/Open")
    gluteus_row_config: Optional[str] = Field(default=None, max_length=50, description="Single Row/Double Row")
    
    # Tendons repaired
    gluteus_tendons_repaired: Optional[str] = Field(default=None, max_length=50, description="Medius/Minimus/Both")
    
    # Amount of retraction (cm)
    gluteus_retraction_cm: Optional[float] = Field(default=None)
    
    # Goutallier grading
    gluteus_goutallier_grade: Optional[str] = Field(default=None, max_length=20)
    
    # Tissue quality
    gluteus_tissue_quality: Optional[str] = Field(default=None, max_length=20, description="Poor/Fair/Good")
    
    # Augmentation
    gluteus_augmentation_used: Optional[bool] = Field(default=None)
    
    # Anchors (gluteus)
    gluteus_num_anchors_used: Optional[int] = Field(default=None)
    gluteus_anchor_brand: Optional[str] = Field(default=None, max_length=100)
    gluteus_anchor_type: Optional[str] = Field(default=None, max_length=100)
    
    # System Fields
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
