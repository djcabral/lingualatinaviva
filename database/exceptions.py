"""
Custom exceptions for database operations.
Provides specific exception types for different database error scenarios.
"""


class DatabaseError(Exception):
    """Base exception for all database-related errors"""
    pass


class ModelRegistryError(DatabaseError):
    """Error in SQLAlchemy model registry management"""
    pass


class SessionError(DatabaseError):
    """Error in database session management"""
    pass


class MigrationError(DatabaseError):
    """Error during database migration"""
    pass


class ValidationError(DatabaseError):
    """Data validation error before database operation"""
    pass


class ConnectionError(DatabaseError):
    """Database connection error"""
    pass
