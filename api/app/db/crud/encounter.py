"""
Encounter CRUD operations
"""
from sqlmodel import Session, select
from typing import Optional
from datetime import datetime
from app.db.models.encounter import Encounter


def create_encounter(session: Session, encounter_data: dict) -> Encounter:
    """Create a new encounter"""
    encounter = Encounter(**encounter_data)
    session.add(encounter)
    session.commit()
    session.refresh(encounter)
    return encounter


def get_encounter(session: Session, encounter_id: int) -> Optional[Encounter]:
    """Get encounter by ID"""
    statement = select(Encounter).where(Encounter.id == encounter_id)
    return session.exec(statement).first()


def get_encounters(
    session: Session,
    skip: int = 0,
    limit: int = 100
) -> list[Encounter]:
    """Get list of encounters with pagination"""
    statement = select(Encounter).offset(skip).limit(limit)
    return session.exec(statement).all()


def get_patient_encounters(
    session: Session,
    patient_id: int,
    skip: int = 0,
    limit: int = 100
) -> list[Encounter]:
    """Get all encounters for a specific patient"""
    statement = select(Encounter).where(
        Encounter.patient_id == patient_id
    ).offset(skip).limit(limit)
    return session.exec(statement).all()


def update_encounter(
    session: Session,
    encounter_id: int,
    update_data: dict
) -> Optional[Encounter]:
    """Update encounter record"""
    encounter = get_encounter(session, encounter_id)
    if not encounter:
        return None
    
    for key, value in update_data.items():
        if value is not None:
            setattr(encounter, key, value)
    
    encounter.updated_at = datetime.utcnow()
    session.add(encounter)
    session.commit()
    session.refresh(encounter)
    return encounter


def delete_encounter(session: Session, encounter_id: int) -> bool:
    """Delete an encounter"""
    encounter = get_encounter(session, encounter_id)
    if not encounter:
        return False
    
    session.delete(encounter)
    session.commit()
    return True
