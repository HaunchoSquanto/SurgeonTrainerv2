"""
Hip Arthroplasty routes - API endpoints for hip arthroplasty case management
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List
from app.db.core import get_session
from app.db.crud import rc_hiparthroplasty as crud
from app.db.schemas.rc_hiparthroplasty import (
    RcHipArthroplastySurgicalCreate,
    RcHipArthroplastySurgicalUpdate,
    RcHipArthroplastySurgicalResponse
)

router = APIRouter()


@router.post("/", response_model=RcHipArthroplastySurgicalResponse, status_code=201)
def create_case(
    case: RcHipArthroplastySurgicalCreate,
    session: Session = Depends(get_session)
):
    """Create a new hip arthroplasty case"""
    # Check if case already exists for this encounter
    existing = crud.get_case_by_encounter(session, case.encounter_id)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Hip arthroplasty case already exists for this encounter"
        )
    
    return crud.create_case(session, case.dict())


@router.get("/", response_model=List[RcHipArthroplastySurgicalResponse])
def list_cases(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: Session = Depends(get_session)
):
    """Get list of hip arthroplasty cases with pagination"""
    return crud.get_cases(session, skip=skip, limit=limit)


@router.get("/{case_id}", response_model=RcHipArthroplastySurgicalResponse)
def get_case(
    case_id: int,
    session: Session = Depends(get_session)
):
    """Get hip arthroplasty case by ID"""
    case = crud.get_case(session, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Hip arthroplasty case not found")
    return case


@router.get("/encounter/{encounter_id}", response_model=RcHipArthroplastySurgicalResponse)
def get_case_by_encounter(
    encounter_id: int,
    session: Session = Depends(get_session)
):
    """Get hip arthroplasty case by encounter ID"""
    case = crud.get_case_by_encounter(session, encounter_id)
    if not case:
        raise HTTPException(status_code=404, detail="Hip arthroplasty case not found for this encounter")
    return case


@router.patch("/{case_id}", response_model=RcHipArthroplastySurgicalResponse)
def update_case(
    case_id: int,
    case_update: RcHipArthroplastySurgicalUpdate,
    session: Session = Depends(get_session)
):
    """Update hip arthroplasty case"""
    case = crud.update_case(
        session,
        case_id,
        case_update.dict(exclude_unset=True)
    )
    if not case:
        raise HTTPException(status_code=404, detail="Hip arthroplasty case not found")
    return case


@router.delete("/{case_id}", status_code=204)
def delete_case(
    case_id: int,
    session: Session = Depends(get_session)
):
    """Delete a hip arthroplasty case"""
    success = crud.delete_case(session, case_id)
    if not success:
        raise HTTPException(status_code=404, detail="Hip arthroplasty case not found")
