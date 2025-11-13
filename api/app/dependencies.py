"""FastAPI dependency injection functions."""

from typing import Generator
from sqlmodel import Session
from .database import get_session

# Database session dependency
def get_db() -> Generator[Session, None, None]:
    """
    Dependency for getting a database session.
    Usage: db: Session = Depends(get_db)
    """
    yield from get_session()
