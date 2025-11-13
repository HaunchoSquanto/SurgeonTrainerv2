"""Database connection and session management."""

from sqlmodel import create_engine, Session, SQLModel
from .config import settings

# Create database engine with optimizations
engine_config = {
    "echo": settings.debug,
}

# SQLite-specific optimizations
if "sqlite" in settings.database_url:
    engine_config["connect_args"] = {
        "check_same_thread": False,
        "timeout": 30,
    }
    engine_config["pool_size"] = 10
    engine_config["max_overflow"] = 20
    engine_config["pool_pre_ping"] = True
    engine_config["pool_recycle"] = 3600
    
# PostgreSQL-specific optimizations
elif "postgresql" in settings.database_url:
    engine_config["pool_size"] = 20
    engine_config["max_overflow"] = 40
    engine_config["pool_pre_ping"] = True
    engine_config["pool_recycle"] = 3600

# Create engine
engine = create_engine(settings.database_url, **engine_config)


def create_db_and_tables():
    """
    Create database tables.
    For production, use Alembic migrations instead.
    """
    from .db.models.models import Patient, PatientVisit, PatientDocument
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get database session for dependency injection."""
    with Session(engine) as session:
        yield session
