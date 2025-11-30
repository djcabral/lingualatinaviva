"""
Database Models Loader with Streamlit Cache Support

This module provides cached model loading to prevent SQLAlchemy
'Multiple classes found' errors during Streamlit hot-reloads.

CRITICAL: This ensures models are only imported ONCE per Streamlit session,
even when the application code is reloaded.
"""

import logging

logger = logging.getLogger(__name__)

# Try to import Streamlit for caching
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False
    logger.debug("Streamlit not available, caching disabled")


def _import_models_impl():
    """
    Internal function that actually imports the model modules.
    This is called by the cached wrapper or directly if no Streamlit.
    """
    logger.info("Importing database models...")
    
    # Import all model modules in order
    from database import models
    from database import integration_models
    from database import syntax_models
    
    logger.info("✓ Database models imported successfully")
    
    return {
        'models': models,
        'integration_models': integration_models,
        'syntax_models': syntax_models
    }


if HAS_STREAMLIT:
    @st.cache_resource(show_spinner=False)
    def _import_models_cached():
        """
        Cached wrapper for model imports (Streamlit version).
        This function is only called ONCE per Streamlit session.
        """
        logger.debug("Using Streamlit cache for model imports")
        return _import_models_impl()
    
    def get_models():
        """
        Get database models using Streamlit cache.
        Returns dict with 'models', 'integration_models', 'syntax_models'.
        """
        return _import_models_cached()
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
