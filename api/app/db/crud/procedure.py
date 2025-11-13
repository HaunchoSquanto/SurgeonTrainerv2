"""
Procedure CRUD operations
"""
from sqlmodel import Session, select
from typing import Optional
from datetime import datetime
from app.db.models.procedure import Procedure


def create_procedure(session: Session, procedure_data: dict) -> Procedure:
    """Create a new procedure"""
    procedure = Procedure(**procedure_data)
    session.add(procedure)
    session.commit()
    session.refresh(procedure)
    return procedure


def get_procedure(session: Session, procedure_id: int) -> Optional[Procedure]:
    """Get procedure by ID"""
    statement = select(Procedure).where(Procedure.id == procedure_id)
    return session.exec(statement).first()


def get_procedures(
    session: Session,
    skip: int = 0,
    limit: int = 100
) -> list[Procedure]:
    """Get list of procedures with pagination"""
    statement = select(Procedure).offset(skip).limit(limit)
    return session.exec(statement).all()


def get_encounter_procedures(
    session: Session,
    encounter_id: int
) -> list[Procedure]:
    """Get all procedures for a specific encounter"""
    statement = select(Procedure).where(Procedure.encounter_id == encounter_id)
    return session.exec(statement).all()


def update_procedure(
    session: Session,
    procedure_id: int,
    update_data: dict
) -> Optional[Procedure]:
    """Update procedure record"""
    procedure = get_procedure(session, procedure_id)
    if not procedure:
        return None
    
    for key, value in update_data.items():
        if value is not None:
            setattr(procedure, key, value)
    
    procedure.updated_at = datetime.utcnow()
    session.add(procedure)
    session.commit()
    session.refresh(procedure)
    return procedure


def delete_procedure(session: Session, procedure_id: int) -> bool:
    """Delete a procedure"""
    procedure = get_procedure(session, procedure_id)
    if not procedure:
        return False
    
    session.delete(procedure)
    session.commit()
    return True
