"""
Custom exception classes for the application.
"""

class AppError(Exception):
    """Base exception class for application errors."""
    pass

class DatabaseError(AppError):
    """Exception raised for database-related errors."""
    pass

class ValidationError(AppError):
    """Exception raised for validation errors."""
    pass

class NotFoundError(AppError):
    """Exception raised when a resource is not found."""
    pass

class AuthenticationError(AppError):
    """Exception raised for authentication errors."""
    pass