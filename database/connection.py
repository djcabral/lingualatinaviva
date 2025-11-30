"""
Database Connection Module - HARDENED VERSION

This module manages the database connection, engine, and session lifecycle
with protection against model registry duplication and improved error handling.

CRITICAL FIXES:
- Uses RegistryManager to prevent "Multiple classes found" errors
- Proper logging for debugging
- Automatic session rollback on errors
- Connection validation
- Enhanced timeout and pooling settings
"""

import logging
import os
import csv
from contextlib import contextmanager
from sqlmodel import create_engine, SQLModel, Session, select

# Import our protection mechanisms
from database.exceptions import DatabaseError, SessionError, ConnectionError
from database.logging_config import setup_database_logging

# Setup logging
logger = setup_database_logging()

# Database configuration
# Database configuration
# Use USER_DATA_DIR if set (by installer), otherwise current directory
base_dir = os.getenv("USER_DATA_DIR", ".")
sqlite_file_name = os.path.join(base_dir, "lingua_latina.db")
sqlite_url = f"sqlite:///{sqlite_file_name}"

# Engine with improved settings for stability
engine = create_engine(
    sqlite_url,
    echo=False,  # Set to True for SQL query debugging
    connect_args={
        "check_same_thread": False,
        "timeout": 30  # 30 second timeout instead of default 5
    },
    pool_pre_ping=True,  # Verify connections before using them
    pool_recycle=3600  # Recycle connections after 1 hour
)

# Initialization flag
_db_initialized = False


def create_db_and_tables():
    """
    Create database tables only once with cached model imports.
    
    This function ensures that:
    1. Models are loaded from cache (prevents duplication)
    2. Tables are created in correct order
    3. Errors are properly logged
    
    Raises:
        DatabaseError: If table creation fails
    """
    global _db_initialized
    
    if _db_initialized:
        logger.debug("Database already initialized, skipping...")
        return
    
    try:
        logger.info("Initializing database...")
        
        # Import models using cached loader (this is safe to call multiple times)
        from database.models_loader import get_models
        get_models()  # Ensures models are loaded
        
        # Create all tables from registered models
        SQLModel.metadata.create_all(engine)
        
        _db_initialized = True
        logger.info("✓ Database initialized successfully")
        
    except Exception as e:
        logger.error(f"✗ Failed to initialize database: {e}")
        raise DatabaseError(f"Database initialization failed: {e}")


@contextmanager
def get_session():
    """
    Context manager for database sessions with automatic cleanup.
    
    This replaces the old get_session() function with a context manager
    that automatically commits on success and rolls back on error.
    
    Usage:
        with get_session() as session:
            word = session.exec(select(Word)).first()
            # ... do work ...
        # Automatically commits here
    
    Yields:
        Session: SQLModel database session
        
    Raises:
        SessionError: If session operations fail
    """
    session = Session(engine)
    try:
        yield session
        session.commit()
        logger.debug("Session committed successfully")
    except Exception as e:
        session.rollback()
        logger.error(f"Session error, rolled back: {e}")
        raise SessionError(f"Database session failed: {e}")
    finally:
        session.close()
        logger.debug("Session closed")


def validate_connection():
    """
    Validate that database connection is working.
    
    Returns:
        bool: True if connection is valid, False otherwise
    """
    try:
        with get_session() as session:
            # Simple query to test connection
            session.execute(select(1))
        logger.debug("Database connection validated")
        return True
    except Exception as e:
        logger.error(f"Database connection validation failed: {e}")
        return False


def init_db():
    """
    Initialize database, create tables, and ensure user profile exists.
    
    This is typically called once at application startup.
    
    Raises:
        DatabaseError: If initialization fails critically
    """
    try:
        # Create tables with registry protection
        create_db_and_tables()
        logger.info("✓ Database initialization complete")
        
        # Note: User profile creation is handled by the application
        # on first use if needed. No need to force it here.
            
    except Exception as e:
        logger.error(f"Critical error during database initialization: {e}")
        raise DatabaseError(f"Failed to initialize database: {e}")


def import_seed_data(session: Session):
    """
    Import seed vocabulary data from CSV file.
    
    Args:
        session: Active database session
        
    Note:
        This assumes running from project root
    """
    from database import Word
    
    # Use PROJECT_ROOT if set, otherwise current directory
    project_root = os.getenv("PROJECT_ROOT", ".")
    
    # Check for seed_data.csv first (cleaned data)
    csv_path = os.path.join(project_root, "data", "seed_data.csv")
    if not os.path.exists(csv_path):
        csv_path = os.path.join(project_root, "data", "vocabulary.csv")
    
    if not os.path.exists(csv_path):
        logger.warning(f"No seed data found at {csv_path}")
        return

    try:
        logger.info(f"Importing seed data from {csv_path}...")
        imported_count = 0
        
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                word = Word(
                    latin=row['latin'],
                    translation=row['translation'],
                    part_of_speech=row['part_of_speech'],
                    level=int(row['level']),
                    genitive=row.get('genitive'),
                    gender=row.get('gender'),
                    declension=row.get('declension'),
                    principal_parts=row.get('principal_parts'),
                    conjugation=row.get('conjugation')
                )
                session.add(word)
                imported_count += 1
        
        session.commit()
        logger.info(f"✓ Imported {imported_count} words from seed data")
        
    except Exception as e:
        logger.error(f"Failed to import seed data: {e}")
        raise DatabaseError(f"Seed data import failed: {e}")
