"""
Knee Surgical routes - API endpoints for knee surgical case management
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List
from app.db.core import get_session
from app.db.crud import rc_kneescope as crud
from app.db.schemas.rc_kneescope import (
    RcKneeSurgicalCreate,
    RcKneeSurgicalUpdate,
    RcKneeSurgicalResponse
)

router = APIRouter()


@router.post("/", response_model=RcKneeSurgicalResponse, status_code=201)
def create_case(
    case: RcKneeSurgicalCreate,
    session: Session = Depends(get_session)
):
    """Create a new knee surgical case"""
    # Check if case already exists for this encounter
    existing = crud.get_case_by_encounter(session, case.encounter_id)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Knee surgical case already exists for this encounter"
        )
    
    return crud.create_case(session, case.dict())


@router.get("/", response_model=List[RcKneeSurgicalResponse])
def list_cases(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: Session = Depends(get_session)
):
    """Get list of knee surgical cases with pagination"""
    return crud.get_cases(session, skip=skip, limit=limit)


@router.get("/{case_id}", response_model=RcKneeSurgicalResponse)
def get_case(
    case_id: int,
    session: Session = Depends(get_session)
):
    """Get knee surgical case by ID"""
    case = crud.get_case(session, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Knee surgical case not found")
    return case


@router.get("/encounter/{encounter_id}", response_model=RcKneeSurgicalResponse)
def get_case_by_encounter(
    encounter_id: int,
    session: Session = Depends(get_session)
):
    """Get knee surgical case by encounter ID"""
    case = crud.get_case_by_encounter(session, encounter_id)
    if not case:
        raise HTTPException(status_code=404, detail="Knee surgical case not found for this encounter")
    return case


@router.patch("/{case_id}", response_model=RcKneeSurgicalResponse)
def update_case(
    case_id: int,
    case_update: RcKneeSurgicalUpdate,
    session: Session = Depends(get_session)
):
    """Update knee surgical case"""
    case = crud.update_case(
        session,
        case_id,
        case_update.dict(exclude_unset=True)
    )
    if not case:
        raise HTTPException(status_code=404, detail="Knee surgical case not found")
    return case


@router.delete("/{case_id}", status_code=204)
def delete_case(
    case_id: int,
    session: Session = Depends(get_session)
):
    """Delete a knee surgical case"""
    success = crud.delete_case(session, case_id)
    if not success:
        raise HTTPException(status_code=404, detail="Knee surgical case not found")
