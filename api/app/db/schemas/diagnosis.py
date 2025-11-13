"""
Diagnosis schemas - Pydantic models for API request/response validation
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DiagnosisBase(BaseModel):
    """Base diagnosis fields"""
    encounter_id: int
    icd10_code: str
    diagnosis_description: str
    diagnosis_type: str = "primary"
    onset_date: Optional[datetime] = None
    resolved_date: Optional[datetime] = None
    status: str = "active"
    notes: Optional[str] = None


class DiagnosisCreate(DiagnosisBase):
    """Schema for creating a new diagnosis"""
    pass


class DiagnosisUpdate(BaseModel):
    """Schema for updating diagnosis - all fields optional"""
    icd10_code: Optional[str] = None
    diagnosis_description: Optional[str] = None
    diagnosis_type: Optional[str] = None
    onset_date: Optional[datetime] = None
    resolved_date: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class DiagnosisResponse(DiagnosisBase):
    """Schema for diagnosis API response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
