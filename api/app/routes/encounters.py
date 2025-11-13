"""
Encounter routes - API endpoints for encounter management
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List
from app.db.core import get_session
from app.db.crud import encounter as crud
from app.db.schemas.encounter import EncounterCreate, EncounterUpdate, EncounterResponse

router = APIRouter(prefix="/api/v1/encounters", tags=["Encounters"])


@router.post("/", response_model=EncounterResponse, status_code=201)
def create_encounter(
    encounter: EncounterCreate,
    session: Session = Depends(get_session)
):
    """Create a new encounter"""
    return crud.create_encounter(session, encounter.dict())


@router.get("/", response_model=List[EncounterResponse])
def list_encounters(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: Session = Depends(get_session)
):
    """Get list of encounters with pagination"""
    return crud.get_encounters(session, skip=skip, limit=limit)


@router.get("/patient/{patient_id}", response_model=List[EncounterResponse])
def get_patient_encounters(
    patient_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: Session = Depends(get_session)
):
    """Get all encounters for a specific patient"""
    return crud.get_patient_encounters(session, patient_id, skip=skip, limit=limit)


@router.get("/{encounter_id}", response_model=EncounterResponse)
def get_encounter(
    encounter_id: int,
    session: Session = Depends(get_session)
):
    """Get encounter by ID"""
    encounter = crud.get_encounter(session, encounter_id)
    if not encounter:
        raise HTTPException(status_code=404, detail="Encounter not found")
    return encounter


@router.patch("/{encounter_id}", response_model=EncounterResponse)
def update_encounter(
    encounter_id: int,
    encounter_update: EncounterUpdate,
    session: Session = Depends(get_session)
):
    """Update encounter information"""
    encounter = crud.update_encounter(
        session,
        encounter_id,
        encounter_update.dict(exclude_unset=True)
    )
    if not encounter:
        raise HTTPException(status_code=404, detail="Encounter not found")
    return encounter


@router.delete("/{encounter_id}", status_code=204)
def delete_encounter(
    encounter_id: int,
    session: Session = Depends(get_session)
):
    """Delete an encounter"""
    success = crud.delete_encounter(session, encounter_id)
    if not success:
        raise HTTPException(status_code=404, detail="Encounter not found")
