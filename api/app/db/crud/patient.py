"""
Patient CRUD operations
"""
from sqlmodel import Session, select
from typing import Optional
from datetime import datetime
from app.db.models.patient import Patient


def create_patient(session: Session, patient_data: dict) -> Patient:
    """Create a new patient"""
    patient = Patient(**patient_data)
    session.add(patient)
    session.commit()
    session.refresh(patient)
    return patient


def get_patient(session: Session, patient_id: int) -> Optional[Patient]:
    """Get patient by ID (excluding soft-deleted)"""
    statement = select(Patient).where(
        Patient.id == patient_id,
        Patient.is_deleted == False
    )
    return session.exec(statement).first()


def get_patient_by_mrn(session: Session, mrn: str) -> Optional[Patient]:
    """Get patient by MRN"""
    statement = select(Patient).where(
        Patient.mrn == mrn,
        Patient.is_deleted == False
    )
    return session.exec(statement).first()


def get_patients(
    session: Session,
    skip: int = 0,
    limit: int = 100,
    include_deleted: bool = False
) -> list[Patient]:
    """Get list of patients with pagination"""
    statement = select(Patient).offset(skip).limit(limit)
    if not include_deleted:
        statement = statement.where(Patient.is_deleted == False)
    return session.exec(statement).all()


def search_patients(
    session: Session,
    search_term: str,
    skip: int = 0,
    limit: int = 100
) -> list[Patient]:
    """Search patients by name or MRN"""
    search_pattern = f"%{search_term}%"
    statement = select(Patient).where(
        (Patient.first_name.contains(search_term)) |
        (Patient.last_name.contains(search_term)) |
        (Patient.mrn.contains(search_term)),
        Patient.is_deleted == False
    ).offset(skip).limit(limit)
    return session.exec(statement).all()


def update_patient(
    session: Session,
    patient_id: int,
    update_data: dict
) -> Optional[Patient]:
    """Update patient record"""
    patient = get_patient(session, patient_id)
    if not patient:
        return None
    
    for key, value in update_data.items():
        if value is not None:
            setattr(patient, key, value)
    
    patient.updated_at = datetime.utcnow()
    session.add(patient)
    session.commit()
    session.refresh(patient)
    return patient


def delete_patient(session: Session, patient_id: int) -> bool:
    """Soft delete a patient"""
    patient = get_patient(session, patient_id)
    if not patient:
        return False
    
    patient.is_deleted = True
    patient.deleted_at = datetime.utcnow()
    session.add(patient)
    session.commit()
    return True


def restore_patient(session: Session, patient_id: int) -> Optional[Patient]:
    """Restore a soft-deleted patient"""
    statement = select(Patient).where(Patient.id == patient_id)
    patient = session.exec(statement).first()
    if not patient:
        return None
    
    patient.is_deleted = False
    patient.deleted_at = None
    session.add(patient)
    session.commit()
    session.refresh(patient)
    return patient
