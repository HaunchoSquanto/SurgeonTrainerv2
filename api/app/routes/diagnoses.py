"""
Diagnosis routes - API endpoints for diagnosis management
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List
from app.db.core import get_session
from app.db.crud import diagnosis as crud
from app.db.schemas.diagnosis import DiagnosisCreate, DiagnosisUpdate, DiagnosisResponse

router = APIRouter(tags=["Diagnoses"])


@router.post("/", response_model=DiagnosisResponse, status_code=201)
def create_diagnosis(
    diagnosis: DiagnosisCreate,
    session: Session = Depends(get_session)
):
    """Add a new diagnosis to an encounter"""
    return crud.create_diagnosis(session, diagnosis.dict())


@router.get("/", response_model=List[DiagnosisResponse])
def list_diagnoses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: Session = Depends(get_session)
):
    """Get list of diagnoses with pagination"""
    return crud.get_diagnoses(session, skip=skip, limit=limit)


@router.get("/encounter/{encounter_id}", response_model=List[DiagnosisResponse])
def get_encounter_diagnoses(
    encounter_id: int,
    session: Session = Depends(get_session)
):
    """Get all diagnoses for a specific encounter"""
    return crud.get_encounter_diagnoses(session, encounter_id)


@router.get("/{diagnosis_id}", response_model=DiagnosisResponse)
def get_diagnosis(
    diagnosis_id: int,
    session: Session = Depends(get_session)
):
    """Get diagnosis by ID"""
    diagnosis = crud.get_diagnosis(session, diagnosis_id)
    if not diagnosis:
        raise HTTPException(status_code=404, detail="Diagnosis not found")
    return diagnosis


@router.patch("/{diagnosis_id}", response_model=DiagnosisResponse)
def update_diagnosis(
    diagnosis_id: int,
    diagnosis_update: DiagnosisUpdate,
    session: Session = Depends(get_session)
):
    """Update diagnosis information"""
    diagnosis = crud.update_diagnosis(
        session,
        diagnosis_id,
        diagnosis_update.dict(exclude_unset=True)
    )
    if not diagnosis:
        raise HTTPException(status_code=404, detail="Diagnosis not found")
    return diagnosis


@router.delete("/{diagnosis_id}", status_code=204)
def delete_diagnosis(
    diagnosis_id: int,
    session: Session = Depends(get_session)
):
    """Delete a diagnosis"""
    success = crud.delete_diagnosis(session, diagnosis_id)
    if not success:
        raise HTTPException(status_code=404, detail="Diagnosis not found")
