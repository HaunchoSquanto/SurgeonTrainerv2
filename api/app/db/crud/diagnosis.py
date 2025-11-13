"""
Diagnosis CRUD operations
"""
from sqlmodel import Session, select
from typing import Optional
from datetime import datetime
from app.db.models.diagnosis import Diagnosis


def create_diagnosis(session: Session, diagnosis_data: dict) -> Diagnosis:
    """Create a new diagnosis"""
    diagnosis = Diagnosis(**diagnosis_data)
    session.add(diagnosis)
    session.commit()
    session.refresh(diagnosis)
    return diagnosis


def get_diagnosis(session: Session, diagnosis_id: int) -> Optional[Diagnosis]:
    """Get diagnosis by ID"""
    statement = select(Diagnosis).where(Diagnosis.id == diagnosis_id)
    return session.exec(statement).first()


def get_diagnoses(
    session: Session,
    skip: int = 0,
    limit: int = 100
) -> list[Diagnosis]:
    """Get list of diagnoses with pagination"""
    statement = select(Diagnosis).offset(skip).limit(limit)
    return session.exec(statement).all()


def get_encounter_diagnoses(
    session: Session,
    encounter_id: int
) -> list[Diagnosis]:
    """Get all diagnoses for a specific encounter"""
    statement = select(Diagnosis).where(Diagnosis.encounter_id == encounter_id)
    return session.exec(statement).all()


def update_diagnosis(
    session: Session,
    diagnosis_id: int,
    update_data: dict
) -> Optional[Diagnosis]:
    """Update diagnosis record"""
    diagnosis = get_diagnosis(session, diagnosis_id)
    if not diagnosis:
        return None
    
    for key, value in update_data.items():
        if value is not None:
            setattr(diagnosis, key, value)
    
    diagnosis.updated_at = datetime.utcnow()
    session.add(diagnosis)
    session.commit()
    session.refresh(diagnosis)
    return diagnosis


def delete_diagnosis(session: Session, diagnosis_id: int) -> bool:
    """Delete a diagnosis"""
    diagnosis = get_diagnosis(session, diagnosis_id)
    if not diagnosis:
        return False
    
    session.delete(diagnosis)
    session.commit()
    return True
