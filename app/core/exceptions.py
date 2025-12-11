"""
Application Core Exceptions

Custom exceptions for the application core layer.
"""

class LinguaLatinaError(Exception):
    """Base exception for Lingua Latina Viva application"""
    pass

class VocabularyError(LinguaLatinaError):
    """Exception related to vocabulary operations"""
    pass

class UserError(LinguaLatinaError):
    """Exception related to user operations"""
    pass

class DatabaseError(LinguaLatinaError):
    """Exception related to database operations"""
    pass

class ServiceError(LinguaLatinaError):
    """Exception related to service operations"""
    pass