"""
Diagnosis model - ICD-10 diagnoses linked to encounters
"""
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Diagnosis(SQLModel, table=True):
    """Diagnosis record with ICD-10 coding"""
    __tablename__ = "diagnosis"
    
    # Primary Key
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Foreign Keys
    encounter_id: int = Field(foreign_key="encounter.id", index=True)
    
    # Diagnosis Details
    icd10_code: str = Field(max_length=10, index=True, description="ICD-10 diagnosis code")
    diagnosis_description: str = Field(max_length=255, description="Human-readable diagnosis")
    
    # Classification
    diagnosis_type: str = Field(max_length=50, default="primary", description="primary/secondary/complication")
    
    # Clinical Context
    onset_date: Optional[datetime] = Field(default=None, description="When diagnosis was first identified")
    resolved_date: Optional[datetime] = Field(default=None, description="When condition resolved")
    status: str = Field(default="active", max_length=50, description="active/resolved/chronic")
    
    # Notes
    notes: Optional[str] = Field(default=None, description="Additional diagnosis notes")
    
    # System Fields
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
