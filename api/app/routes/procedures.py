"""
Procedure routes - API endpoints for procedure management
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List
from app.db.core import get_session
from app.db.crud import procedure as crud
from app.db.schemas.procedure import ProcedureCreate, ProcedureUpdate, ProcedureResponse

router = APIRouter(tags=["Procedures"])


@router.post("/", response_model=ProcedureResponse, status_code=201)
def create_procedure(
    procedure: ProcedureCreate,
    session: Session = Depends(get_session)
):
    """Add a new procedure to an encounter"""
    return crud.create_procedure(session, procedure.dict())


@router.get("/", response_model=List[ProcedureResponse])
def list_procedures(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: Session = Depends(get_session)
):
    """Get list of procedures with pagination"""
    return crud.get_procedures(session, skip=skip, limit=limit)


@router.get("/encounter/{encounter_id}", response_model=List[ProcedureResponse])
def get_encounter_procedures(
    encounter_id: int,
    session: Session = Depends(get_session)
):
    """Get all procedures for a specific encounter"""
    return crud.get_encounter_procedures(session, encounter_id)


@router.get("/{procedure_id}", response_model=ProcedureResponse)
def get_procedure(
    procedure_id: int,
    session: Session = Depends(get_session)
):
    """Get procedure by ID"""
    procedure = crud.get_procedure(session, procedure_id)
    if not procedure:
        raise HTTPException(status_code=404, detail="Procedure not found")
    return procedure


@router.patch("/{procedure_id}", response_model=ProcedureResponse)
def update_procedure(
    procedure_id: int,
    procedure_update: ProcedureUpdate,
    session: Session = Depends(get_session)
):
    """Update procedure information"""
    procedure = crud.update_procedure(
        session,
        procedure_id,
        procedure_update.dict(exclude_unset=True)
    )
    if not procedure:
        raise HTTPException(status_code=404, detail="Procedure not found")
    return procedure


@router.delete("/{procedure_id}", status_code=204)
def delete_procedure(
    procedure_id: int,
    session: Session = Depends(get_session)
):
    """Delete a procedure"""
    success = crud.delete_procedure(session, procedure_id)
    if not success:
        raise HTTPException(status_code=404, detail="Procedure not found")
