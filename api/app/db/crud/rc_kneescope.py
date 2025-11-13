"""
Knee Surgical CRUD operations
"""
from sqlmodel import Session, select
from typing import Optional
from datetime import datetime
from app.db.models.rc_kneescope import RcKneeScope


def create_case(session: Session, case_data: dict) -> RcKneeScope:
    """Create a new knee surgical case"""
    case = RcKneeScope(**case_data)
    session.add(case)
    session.commit()
    session.refresh(case)
    return case


def get_case(session: Session, case_id: int) -> Optional[RcKneeScope]:
    """Get knee surgical case by ID"""
    statement = select(RcKneeScope).where(RcKneeScope.id == case_id)
    return session.exec(statement).first()


def get_case_by_encounter(session: Session, encounter_id: int) -> Optional[RcKneeScope]:
    """Get knee surgical case by encounter ID"""
    statement = select(RcKneeScope).where(RcKneeScope.encounter_id == encounter_id)
    return session.exec(statement).first()


def get_cases(
    session: Session,
    skip: int = 0,
    limit: int = 100
) -> list[RcKneeScope]:
    """Get list of knee surgical cases with pagination"""
    statement = select(RcKneeScope).offset(skip).limit(limit)
    return session.exec(statement).all()


def update_case(
    session: Session,
    case_id: int,
    update_data: dict
) -> Optional[RcKneeScope]:
    """Update knee surgical case"""
    case = get_case(session, case_id)
    if not case:
        return None
    
    for key, value in update_data.items():
        if value is not None:
            setattr(case, key, value)
    
    case.updated_at = datetime.utcnow()
    session.add(case)
    session.commit()
    session.refresh(case)
    return case


def delete_case(session: Session, case_id: int) -> bool:
    """Delete a knee surgical case"""
    case = get_case(session, case_id)
    if not case:
        return False
    
    session.delete(case)
    session.commit()
    return True
