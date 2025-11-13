"""
Pydantic schemas for case intake normalization and validation
"""
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import date
from enum import Enum


class ProcedureType(str, Enum):
    """Supported procedure types"""
    ROTATOR_CUFF = "rotator-cuff"
    KNEE_SURGICAL = "knee-surgical"
    SHOULDER_SCOPE = "shoulder-scope"
    SHOULDER_ARTHROPLASTY = "shoulder-arthroplasty"
    HIP_SCOPE = "hip-scope"
    HIP_ARTHROPLASTY = "hip-arthroplasty"
    KNEE_ARTHROPLASTY = "knee-arthroplasty"
    OTHER = "other"


class Laterality(str, Enum):
    """Surgical side"""
    RIGHT = "Right"
    LEFT = "Left"
    BILATERAL = "Bilateral"


class Sex(str, Enum):
    """Biological sex"""
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"


class NormalizedCase(BaseModel):
    """
    Output schema from LLM normalization.
    This is what Studio LM tries to extract from raw text.
    More lenient - allows nulls for most fields.
    """
    # Required patient fields
    mrn: str = Field(..., description="Medical record number")
    first_name: Optional[str] = Field(None, description="Patient first name")
    last_name: Optional[str] = Field(None, description="Patient last name")
    date_of_birth: date = Field(..., description="Patient DOB")
    sex: Sex = Field(..., description="Biological sex")
    
    # Required surgical fields
    surgery_date: date = Field(..., description="Date of surgery")
    procedure_type: ProcedureType = Field(..., description="Type of procedure")
    
    # Optional patient fields
    middle_name: Optional[str] = None
    
    # Optional surgical fields
    laterality: Optional[Laterality] = None
    attending: Optional[str] = Field(None, description="Attending surgeon")
    fellow_or_pa: Optional[str] = Field(None, description="Fellow or PA")
    chief_complaint: Optional[str] = Field(None, description="Reason for visit")
    location: Optional[str] = Field(None, description="Hospital/facility")
    notes: Optional[str] = Field(None, description="Additional clinical notes")
    
    # Metadata
    raw_note: Optional[str] = Field(None, description="Original raw text")


class CaseCreatePayload(BaseModel):
    """
    Strict schema for database creation.
    This is what we send to the API after validation.
    Enforces hard requirements before DB insert.
    """
    # Patient data (MRN required, names optional)
    mrn: str
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: date
    sex: Literal["M", "F", "O"]
    
    # Encounter data
    encounter_type: str = "surgery"
    encounter_date: date
    chief_complaint: Optional[str] = None
    location: Optional[str] = None
    attending_physician: Optional[str] = None
    status: str = "active"
    notes: Optional[str] = None
    
    # Research case data
    procedure_type: str
    laterality: Optional[str] = None
    fellow_or_pa: Optional[str] = None
    
    # Original text for auditing
    raw_note: str


def normalized_to_case_payload(norm: NormalizedCase) -> CaseCreatePayload:
    """
    Convert LLM-normalized case to strict DB-ready payload.
    This is the gatekeeper that enforces hard requirements.
    
    Raises:
        ValueError: If required fields are missing or invalid
    """
    # Validate we have minimum required data (names are optional)
    if not all([norm.mrn, norm.date_of_birth, norm.sex, 
                norm.surgery_date, norm.procedure_type]):
        missing = []
        if not norm.mrn: missing.append("mrn")
        if not norm.date_of_birth: missing.append("date_of_birth")
        if not norm.sex: missing.append("sex")
        if not norm.surgery_date: missing.append("surgery_date")
        if not norm.procedure_type: missing.append("procedure_type")
        raise ValueError(f"Cannot create case - missing required fields: {', '.join(missing)}")
    
    return CaseCreatePayload(
        # Patient
        mrn=norm.mrn,
        first_name=norm.first_name,
        middle_name=norm.middle_name,
        last_name=norm.last_name,
        date_of_birth=norm.date_of_birth,
        sex=norm.sex.value,
        
        # Encounter
        encounter_type="surgery",
        encounter_date=norm.surgery_date,
        chief_complaint=norm.chief_complaint,
        location=norm.location,
        attending_physician=norm.attending,
        status="active",
        notes=norm.notes,
        
        # Research case
        procedure_type=norm.procedure_type.value,
        laterality=norm.laterality.value if norm.laterality else None,
        fellow_or_pa=norm.fellow_or_pa,
        
        # Audit trail
        raw_note=norm.raw_note or ""
    )
