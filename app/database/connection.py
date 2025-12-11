"""
Database connection management.
"""
import logging
from contextlib import contextmanager
from sqlmodel import create_engine, Session
from app.config.settings import settings

# Setup logging
logger = logging.getLogger(__name__)

# Create engine with optimized settings
engine = create_engine(
    settings.db_url,
    echo=False,
    connect_args={
        "check_same_thread": False,
        "timeout": 30
    },
    pool_pre_ping=True,
    pool_recycle=3600
)

def get_engine():
    """Get the database engine."""
    return engine

def create_db_and_tables():
    """Create database tables."""
    from app.models import SQLModel
    logger.info("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    logger.info("Database tables created successfully")

def init_db():
    """Initialize the database."""
    try:
        create_db_and_tables()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

@contextmanager
def get_session():
    """Context manager for database sessions."""
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Session error: {e}")
        raise
    finally:
        session.close()