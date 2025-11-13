"""
Other Surgical schemas - Pydantic models for API request/response validation
"""

from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class RcOtherSurgicalBase(BaseModel):
    """Base 'other' surgical fields (research-focused)"""
    encounter_id: int

    # Core case metadata
    fellow_or_pa: Optional[str] = None
    attending: Optional[str] = None
    mrn: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[date] = None
    surgery_date: Optional[date] = None

    # Procedure type flags
    elbow_procedure_done: Optional[bool] = None
    foot_ankle_procedure_done: Optional[bool] = None
    other_procedure_not_listed_done: Optional[bool] = None


class RcOtherSurgicalCreate(RcOtherSurgicalBase):
    """Schema for creating a new 'other' surgical case"""
    pass


class RcOtherSurgicalUpdate(BaseModel):
    """Schema for updating an 'other' surgical case - all fields optional"""

    fellow_or_pa: Optional[str] = None
    attending: Optional[str] = None
    mrn: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[date] = None
    surgery_date: Optional[date] = None

    elbow_procedure_done: Optional[bool] = None
    foot_ankle_procedure_done: Optional[bool] = None
    other_procedure_not_listed_done: Optional[bool] = None


class RcOtherSurgicalResponse(RcOtherSurgicalBase):
    """Schema for 'other' surgical API response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
