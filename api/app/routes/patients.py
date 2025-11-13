"""
Patient routes - API endpoints for patient management
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List
from app.db.core import get_session
from app.db.crud import patient as crud
from app.db.schemas.patient import PatientCreate, PatientUpdate, PatientResponse

router = APIRouter()


@router.post("/", response_model=PatientResponse, status_code=201)
def create_patient(
    patient: PatientCreate,
    session: Session = Depends(get_session)
):
    """Create a new patient"""
    # Check if MRN already exists
    existing = crud.get_patient_by_mrn(session, patient.mrn)
    if existing:
        raise HTTPException(status_code=400, detail="Patient with this MRN already exists")
    
    return crud.create_patient(session, patient.dict())


@router.get("/", response_model=List[PatientResponse])
def list_patients(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    include_deleted: bool = Query(False),
    session: Session = Depends(get_session)
):
    """Get list of patients with pagination"""
    return crud.get_patients(session, skip=skip, limit=limit, include_deleted=include_deleted)


@router.get("/search", response_model=List[PatientResponse])
def search_patients(
    q: str = Query(..., min_length=1, description="Search term (name or MRN)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: Session = Depends(get_session)
):
    """Search patients by name or MRN"""
    return crud.search_patients(session, search_term=q, skip=skip, limit=limit)


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(
    patient_id: int,
    session: Session = Depends(get_session)
):
    """Get patient by ID"""
    patient = crud.get_patient(session, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.patch("/{patient_id}", response_model=PatientResponse)
def update_patient(
    patient_id: int,
    patient_update: PatientUpdate,
    session: Session = Depends(get_session)
):
    """Update patient information"""
    patient = crud.update_patient(
        session,
        patient_id,
        patient_update.dict(exclude_unset=True)
    )
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.delete("/{patient_id}", status_code=204)
def delete_patient(
    patient_id: int,
    session: Session = Depends(get_session)
):
    """Soft delete a patient"""
    success = crud.delete_patient(session, patient_id)
    if not success:
        raise HTTPException(status_code=404, detail="Patient not found")


@router.post("/{patient_id}/restore", response_model=PatientResponse)
def restore_patient(
    patient_id: int,
    session: Session = Depends(get_session)
):
    """Restore a soft-deleted patient"""
    patient = crud.restore_patient(session, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient
