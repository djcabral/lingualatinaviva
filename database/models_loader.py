"""
Database Models Loader with Streamlit Cache Support

This module provides cached model loading to prevent SQLAlchemy
'Multiple classes found' errors during Streamlit hot-reloads.

CRITICAL: This ensures models are only imported ONCE per Streamlit session,
even when the application code is reloaded.
"""

import logging
import sys

logger = logging.getLogger(__name__)

# Global cache to prevent reimporting
_models_cache = None


def get_models():
    """
    Get database models using module-level caching.
    Returns dict with 'models', 'integration_models', 'syntax_models'.
    
    This function uses a simple global cache instead of Streamlit's cache
    to avoid conflicts during hot-reloads.
    """
    global _models_cache
    
    # If already imported, return cached version
    if _models_cache is not None:
        logger.debug("Returning cached models")
        return _models_cache
    
    logger.info("Importing database models...")
    
    try:
        # Import all model modules in order
        from database import models
        from database import integration_models
        from database import syntax_models
        
        logger.info("✓ Database models imported successfully")
        
        # Cache and return
        _models_cache = {
            'models': models,
            'integration_models': integration_models,
            'syntax_models': syntax_models
        }
        
        return _models_cache
        
    except Exception as e:
        logger.error(f"✗ Failed to import models: {e}")
        raise
else:
    # Non-Streamlit fallback
    _models_cache = None
    
    def get_models():
        """
        Get database models with manual caching (non-Streamlit version).
        Returns dict with 'models', 'integration_models', 'syntax_models'.
        """
        global _models_cache
        if _models_cache is None:
            _models_cache = _import_models_impl()
        return _models_cache
