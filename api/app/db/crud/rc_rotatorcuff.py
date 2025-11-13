"""
Rotator Cuff CRUD operations
"""
from sqlmodel import Session, select
from typing import Optional
from datetime import datetime
from app.db.models.rc_rotatorcuff import RcRotatorCuff


def create_case(session: Session, case_data: dict) -> RcRotatorCuff:
    """Create a new rotator cuff case"""
    case = RcRotatorCuff(**case_data)
    session.add(case)
    session.commit()
    session.refresh(case)
    return case


def get_case(session: Session, case_id: int) -> Optional[RcRotatorCuff]:
    """Get rotator cuff case by ID"""
    statement = select(RcRotatorCuff).where(RcRotatorCuff.id == case_id)
    return session.exec(statement).first()


def get_case_by_encounter(session: Session, encounter_id: int) -> Optional[RcRotatorCuff]:
    """Get rotator cuff case by encounter ID"""
    statement = select(RcRotatorCuff).where(RcRotatorCuff.encounter_id == encounter_id)
    return session.exec(statement).first()


def get_cases(
    session: Session,
    skip: int = 0,
    limit: int = 100
) -> list[RcRotatorCuff]:
    """Get list of rotator cuff cases with pagination"""
    statement = select(RcRotatorCuff).offset(skip).limit(limit)
    return session.exec(statement).all()


def update_case(
    session: Session,
    case_id: int,
    update_data: dict
) -> Optional[RcRotatorCuff]:
    """Update rotator cuff case"""
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
    """Delete a rotator cuff case"""
    case = get_case(session, case_id)
    if not case:
        return False
    
    session.delete(case)
    session.commit()
    return True
