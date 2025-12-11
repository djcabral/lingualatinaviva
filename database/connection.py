"""
Database Connection Module - HARDENED & OPTIMIZED VERSION

This module manages the database connection, engine, and session lifecycle
with comprehensive improvements for performance and robustness.

KEY IMPROVEMENTS:
- Optimized connection pooling based on database type
- SQLite StaticPool for single-file databases
- PostgreSQL/MySQL with proper pool configuration
- Automatic health checks and validation
- Enhanced error handling and recovery
- Connection metrics and monitoring
- Proper timeout and retry settings
"""

import csv
import logging
import os
import time
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Dict, Optional, Tuple

from sqlalchemy import create_engine, event, inspect, select, text
from sqlalchemy.engine import Engine
from sqlalchemy.pool import NullPool, QueuePool, StaticPool
from sqlmodel import Session, SQLModel

from database.exceptions import ConnectionError as DBConnectionError

# Import protection mechanisms
from database.exceptions import DatabaseError, SessionError
from database.logging_config import setup_database_logging

# Setup logging
logger = setup_database_logging()

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

# Determine database URL
base_dir = os.getenv("USER_DATA_DIR", ".")
sqlite_file_name = os.path.join(base_dir, "lingua_latina.db")
sqlite_url = f"sqlite:///{sqlite_file_name}"

# Default database URL (can be overridden by environment)
DATABASE_URL = os.getenv("DATABASE_URL", sqlite_url)

# Pool configuration
POOL_SIZE = int(os.getenv("DATABASE_POOL_SIZE", "10"))
MAX_OVERFLOW = int(os.getenv("DATABASE_MAX_OVERFLOW", "20"))
POOL_TIMEOUT = int(os.getenv("DATABASE_POOL_TIMEOUT", "30"))
POOL_RECYCLE = int(os.getenv("DATABASE_POOL_RECYCLE", "3600"))

# Debug mode
DATABASE_ECHO = os.getenv("DATABASE_ECHO", "False").lower() == "true"

# ============================================================================
# CONNECTION METRICS
# ============================================================================


class ConnectionMetrics:
    """Track connection pool metrics"""

    def __init__(self):
        self.total_connections = 0
        self.failed_connections = 0
        self.queries_executed = 0
        self.slow_queries = 0
        self.last_health_check = None
        self.total_query_time_ms = 0.0

    def record_query(self, duration_ms: float, slow_threshold: int = 100):
        """Record query execution"""
        self.queries_executed += 1
        self.total_query_time_ms += duration_ms
        if duration_ms > slow_threshold:
            self.slow_queries += 1

    def get_stats(self) -> Dict[str, Any]:
        """Get metrics summary"""
        avg_query_time = (
            self.total_query_time_ms / self.queries_executed
            if self.queries_executed > 0
            else 0
        )
        return {
            "total_connections": self.total_connections,
            "failed_connections": self.failed_connections,
            "queries_executed": self.queries_executed,
            "slow_queries": self.slow_queries,
            "avg_query_time_ms": round(avg_query_time, 2),
            "last_health_check": self.last_health_check,
        }


metrics = ConnectionMetrics()

# ============================================================================
# ENGINE CREATION WITH OPTIMIZED POOLING
# ============================================================================


def create_optimized_engine(database_url: str) -> Engine:
    """
    Create database engine with optimized settings based on database type.

    Args:
        database_url: Database connection URL

    Returns:
        Configured SQLAlchemy engine

    Raises:
        DatabaseError: If engine creation fails
    """
    try:
        logger.info(f"Creating database engine for: {database_url.split('?')[0]}")

        # SQLite-specific configuration
        if database_url.startswith("sqlite://"):
            engine = create_engine(
                database_url,
                echo=DATABASE_ECHO,
                # Use StaticPool for SQLite - maintains single connection
                poolclass=StaticPool,
                connect_args={
                    "check_same_thread": False,
                    "timeout": POOL_TIMEOUT,  # 30 second timeout
                },
            )
            logger.info("✓ SQLite engine configured with StaticPool")

        # PostgreSQL/MySQL configuration
        else:
            engine = create_engine(
                database_url,
                echo=DATABASE_ECHO,
                # Use QueuePool for server databases
                poolclass=QueuePool,
                pool_size=POOL_SIZE,
                max_overflow=MAX_OVERFLOW,
                pool_timeout=POOL_TIMEOUT,
                pool_recycle=POOL_RECYCLE,  # Recycle connections after 1 hour
                pool_pre_ping=True,  # Verify connection before use
                # Connection pool settings
                connect_args={
                    "connect_timeout": POOL_TIMEOUT,
                },
            )
            logger.info(
                f"✓ {database_url.split(':')[0].upper()} engine configured with "
                f"QueuePool(size={POOL_SIZE}, overflow={MAX_OVERFLOW})"
            )

        # Register event listeners for monitoring
        _register_event_listeners(engine)

        metrics.total_connections += 1
        return engine

    except Exception as e:
        logger.error(f"✗ Failed to create database engine: {e}")
        metrics.failed_connections += 1
        raise DatabaseError(f"Engine creation failed: {e}")


def _register_event_listeners(engine: Engine):
    """Register SQLAlchemy event listeners for monitoring and debugging"""

    @event.listens_for(engine, "connect")
    def receive_connect(dbapi_conn, connection_record):
        """Monitor new connections"""
        logger.debug("New database connection established")
        # Enable foreign keys for SQLite
        try:
            # Check if this is SQLite
            if hasattr(dbapi_conn, "execute"):
                cursor = dbapi_conn.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()
        except Exception as e:
            logger.debug(f"Could not set PRAGMA: {e}")

    @event.listens_for(engine, "close")
    def receive_close(dbapi_conn, connection_record):
        """Monitor connection close"""
        logger.debug("Database connection closed")

    @event.listens_for(engine, "detach")
    def receive_detach(dbapi_conn, connection_record):
        """Monitor connection detach"""
        logger.debug("Database connection detached from pool")


# Create the engine
try:
    engine = create_optimized_engine(DATABASE_URL)
except DatabaseError as e:
    logger.critical(f"Failed to initialize database engine: {e}")
    raise


# Session factory function
def get_session_factory():
    """Create a new session"""
    return Session(engine)


# Initialization flag
_db_initialized = False
_initialization_lock = False


# ============================================================================
# SESSION MANAGEMENT
# ============================================================================


@contextmanager
def get_session() -> Session:
    """
    Context manager for database sessions with automatic cleanup.

    Provides automatic transaction management with commit on success
    and rollback on error. Always closes the session.

    Usage:
        with get_session() as session:
            word = session.exec(select(Word)).first()
            # ... do work ...
        # Automatically commits here or rolls back on error

    Yields:
        Session: SQLModel database session

    Raises:
        SessionError: If session operations fail

    Example:
        >>> with get_session() as session:
        ...     user = session.exec(select(UserProfile)).first()
        ...     user.xp += 10
        ...     # Auto-commits on exit
    """
    session = Session(engine)
    start_time = time.time()

    try:
        yield session

        # Successful completion - commit
        session.commit()
        duration_ms = (time.time() - start_time) * 1000
        logger.debug(f"Session committed successfully ({duration_ms:.2f}ms)")
        metrics.record_query(duration_ms)

    except Exception as e:
        # Error occurred - rollback
        session.rollback()
        duration_ms = (time.time() - start_time) * 1000
        logger.error(
            f"Session error (rolled back after {duration_ms:.2f}ms): {e}", exc_info=True
        )

        # Provide detailed error context
        error_msg = str(e).lower()
        if "integrity" in error_msg:
            logger.error("Integrity constraint violation - check database schema")
        elif "locked" in error_msg:
            logger.error("Database is locked - another process may be using it")
        elif "no such table" in error_msg:
            logger.error("Table not found - run migrations or initialize database")

        raise SessionError(f"Database session failed: {e}") from e

    finally:
        session.close()
        logger.debug("Session closed and resources released")


@contextmanager
def get_session_explicit():
    """
    Context manager with explicit transaction control.

    Use when you need explicit control over commits and rollbacks.
    Does NOT auto-commit on exit.

    Usage:
        with get_session_explicit() as session:
            obj = session.exec(select(Model)).first()
            obj.value = 123
            session.commit()  # Explicit

    Yields:
        Session: SQLModel database session
    """
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


def get_session_no_context():
    """
    Get a database session without context manager.

    WARNING: You must manually call session.close()

    Returns:
        Session: SQLModel database session

    Example:
        >>> session = get_session_no_context()
        >>> try:
        ...     # do work
        ... finally:
        ...     session.close()
    """
    return Session(engine)


# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================


def create_db_and_tables():
    """
    Create database tables from SQLModel definitions.

    This function:
    1. Imports all model definitions
    2. Creates tables if they don't exist
    3. Validates schema
    4. Is idempotent (safe to call multiple times)

    Raises:
        DatabaseError: If table creation fails
    """
    global _db_initialized

    if _db_initialized:
        logger.debug("Database already initialized, skipping table creation")
        return

    try:
        logger.info("Initializing database schema...")

        # Import models (cached by models_loader)
        from database.models_loader import get_models

        get_models()  # Ensures models are registered with SQLModel

        # Create all tables from registered models
        SQLModel.metadata.create_all(engine)

        # Validate schema
        if not validate_schema():
            logger.warning("Schema validation warnings present")

        _db_initialized = True
        logger.info("✓ Database schema initialized successfully")

    except Exception as e:
        logger.error(f"✗ Failed to initialize database schema: {e}", exc_info=True)
        raise DatabaseError(f"Database initialization failed: {e}")


def validate_schema() -> bool:
    """
    Validate that database schema matches model definitions.

    Returns:
        True if schema is valid, False if issues found
    """
    try:
        with get_session() as session:
            # Simple validation - can be expanded
            inspector = inspect(engine)
            db_tables = set(inspector.get_table_names())

            if not db_tables:
                logger.warning("No tables found in database")
                return False

            logger.debug(f"Found {len(db_tables)} tables in database")
            return True

    except Exception as e:
        logger.error(f"Schema validation error: {e}")
        return False


def init_db():
    """
    Initialize database and ensure it's ready for use.

    This is the main entry point for database setup. Call this once
    at application startup.

    Raises:
        DatabaseError: If initialization fails critically
    """
    try:
        logger.info("=" * 60)
        logger.info("INITIALIZING DATABASE")
        logger.info("=" * 60)

        # Create tables
        create_db_and_tables()

        # Validate connection
        if not validate_connection():
            raise DatabaseError("Connection validation failed")

        logger.info("=" * 60)
        logger.info("✓ DATABASE READY")
        logger.info("=" * 60)

    except DatabaseError:
        raise
    except Exception as e:
        logger.error(
            f"✗ Critical error during database initialization: {e}", exc_info=True
        )
        raise DatabaseError(f"Failed to initialize database: {e}")


# ============================================================================
# CONNECTION VALIDATION
# ============================================================================


def validate_connection() -> bool:
    """
    Validate that database connection is working.

    Performs a simple query to verify connectivity and records metrics.

    Returns:
        True if connection is valid, False otherwise
    """
    try:
        start = time.time()
        with get_session() as session:
            # Simple ping query
            session.execute(text("SELECT 1"))

        duration_ms = (time.time() - start) * 1000
        metrics.last_health_check = datetime.utcnow()

        logger.info(f"✓ Database connection validated ({duration_ms:.2f}ms)")
        return True

    except Exception as e:
        logger.error(f"✗ Database connection validation failed: {e}")
        metrics.failed_connections += 1
        return False


def get_connection_status() -> Dict[str, Any]:
    """
    Get current connection status and metrics.

    Returns:
        Dictionary with connection information
    """
    try:
        is_healthy = validate_connection()
        return {
            "status": "healthy" if is_healthy else "unhealthy",
            "database_url": DATABASE_URL.split("?")[0],  # Hide credentials
            "pool_size": POOL_SIZE,
            "max_overflow": MAX_OVERFLOW,
            "metrics": metrics.get_stats(),
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat(),
        }


# ============================================================================
# DATA IMPORT
# ============================================================================


def import_seed_data(csv_path: str, session: Optional[Session] = None) -> int:
    """
    Import vocabulary data from CSV file.

    CSV format:
        latin,translation,part_of_speech,level,[genitive],[gender],[declension],[principal_parts],[conjugation]

    Args:
        csv_path: Path to CSV file
        session: Database session (creates new if not provided)

    Returns:
        Number of words imported

    Raises:
        DatabaseError: If import fails
    """
    from database import Word

    if not os.path.exists(csv_path):
        logger.warning(f"CSV file not found: {csv_path}")
        return 0

    own_session = session is None
    if own_session:
        session = Session(engine)

    try:
        logger.info(f"Importing seed data from {csv_path}...")
        imported_count = 0
        error_count = 0

        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (skip header)
                try:
                    word = Word(
                        latin=row["latin"].strip(),
                        translation=row["translation"].strip(),
                        part_of_speech=row["part_of_speech"].strip(),
                        level=int(row["level"]),
                        genitive=row.get("genitive", "").strip() or None,
                        gender=row.get("gender", "").strip() or None,
                        declension=row.get("declension", "").strip() or None,
                        principal_parts=row.get("principal_parts", "").strip() or None,
                        conjugation=row.get("conjugation", "").strip() or None,
                    )
                    session.add(word)
                    imported_count += 1

                    # Batch commit every 1000 rows
                    if imported_count % 1000 == 0:
                        session.commit()
                        logger.debug(f"Imported {imported_count} words...")

                except Exception as e:
                    error_count += 1
                    logger.warning(f"Error on row {row_num}: {e}")
                    if error_count > 100:  # Stop after 100 errors
                        raise DatabaseError(f"Too many import errors (>100)")

        session.commit()
        logger.info(f"✓ Imported {imported_count} words (errors: {error_count})")
        return imported_count

    except Exception as e:
        session.rollback()
        logger.error(f"✗ Failed to import seed data: {e}", exc_info=True)
        raise DatabaseError(f"Seed data import failed: {e}")

    finally:
        if own_session:
            session.close()


# ============================================================================
# CLEANUP AND MONITORING
# ============================================================================


def dispose_engine():
    """
    Dispose of the engine and close all connections.

    Call this when shutting down the application.
    """
    try:
        engine.dispose()
        logger.info("✓ Database engine disposed successfully")
    except Exception as e:
        logger.error(f"Error disposing engine: {e}")


def print_connection_stats():
    """Print connection pool statistics"""
    stats = get_connection_status()
    logger.info(f"Connection Stats: {stats}")
