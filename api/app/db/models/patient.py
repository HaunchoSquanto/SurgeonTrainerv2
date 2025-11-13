"""
Patient model - Core EMR table for patient demographics and medical history
"""
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, datetime


class Patient(SQLModel, table=True):
    """Patient demographic and medical information"""
    __tablename__ = "patient"
    
    # Primary Key
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Identifiers
    mrn: str = Field(unique=True, index=True, description="Medical Record Number")
    
    # Demographics
    first_name: str = Field(max_length=100)
    middle_name: Optional[str] = Field(default=None, max_length=100)
    last_name: str = Field(max_length=100)
    date_of_birth: date
    sex: str = Field(max_length=1, description="M/F/O")
    
    # Contact Information
    email: Optional[str] = Field(default=None, max_length=255)
    phone: Optional[str] = Field(default=None, max_length=20)
    address_line1: Optional[str] = Field(default=None, max_length=255)
    address_line2: Optional[str] = Field(default=None, max_length=255)
    city: Optional[str] = Field(default=None, max_length=100)
    state: Optional[str] = Field(default=None, max_length=2)
    zip_code: Optional[str] = Field(default=None, max_length=10)
    
    # Insurance
    insurance_provider: Optional[str] = Field(default=None, max_length=255)
    insurance_policy_number: Optional[str] = Field(default=None, max_length=100)
    insurance_group_number: Optional[str] = Field(default=None, max_length=100)
    
    # Medical History
    allergies: Optional[str] = Field(default=None, description="Comma-separated list")
    medications: Optional[str] = Field(default=None, description="Comma-separated list")
    medical_history: Optional[str] = Field(default=None, description="Free text")
    surgical_history: Optional[str] = Field(default=None, description="Free text")
    family_history: Optional[str] = Field(default=None, description="Free text")
    social_history: Optional[str] = Field(default=None, description="Free text")
    
    # System Fields
    is_deleted: bool = Field(default=False, description="Soft delete flag")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    deleted_at: Optional[datetime] = Field(default=None)
