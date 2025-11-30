"""
SQLAlchemy Model Registry Manager

This module provides centralized control over SQLAlchemy model registration
to prevent the critical "Multiple classes found" error that occurs when models
are registered multiple times during Streamlit reloads.

CRITICAL: This module solves the recurring InvalidRequestError by ensuring
models are only registered once per Python process.
"""

import logging
from sqlalchemy.orm import clear_mappers
from database.exceptions import ModelRegistryError

logger = logging.getLogger(__name__)


class RegistryManager:
    """
    Manages SQLAlchemy model registry to prevent duplication.
    
    This singleton-like class ensures that database models are only
    registered once, even when Streamlit reloads modules.
    """
    
    _initialized = False
    _models_registered = set()
    
    @classmethod
    def ensure_clean_registry(cls):
        """
        Ensure registry is ready for model registration.
        
        This is called before registering models. If models are already
        registered, we skip clearing to avoid breaking SQLAlchemy's mapper registry.
        """
        if cls._initialized:
            logger.debug("Registry already initialized, skipping clean (models already registered)")
    
    @classmethod
    def register_models(cls):
        """
        Import all model modules to register them with SQLAlchemy.
        
        This method imports the model modules in the correct order and
        tracks which models have been registered to prevent duplication.
        
        Raises:
            ModelRegistryError: If model registration fails
        """
        if cls._models_registered:
            logger.debug(f"Models already registered ({len(cls._models_registered)} types), skipping...")
            return
        
        try:
            # Try to use Streamlit cache to prevent re-registration on reload
            import streamlit as st
            # Check if we are running in Streamlit
            if hasattr(st, 'runtime') and st.runtime.exists():
                logger.debug("Using Streamlit cache for model registration")
                _register_models_cached()
                cls._initialized = True
                return
        except (ImportError, AttributeError):
            pass
            
        # Fallback for non-Streamlit or if cache fails
        _register_models_impl(cls)

    @classmethod
    def get_models_module(cls):
        """
        Get the database.models module, using cache if available.
        This prevents re-importing the module and re-defining classes.
        """
        try:
            import streamlit as st
            if hasattr(st, 'runtime') and st.runtime.exists():
                return _get_models_module_cached()
        except (ImportError, AttributeError):
            pass
            
        from database import models
        return models

    @classmethod
    def is_initialized(cls):
        """Check if registry has been initialized"""
        return cls._initialized
    
    @classmethod
    def get_registered_count(cls):
        """Get count of registered model types"""
        return len(cls._models_registered)

def _register_models_impl(cls_ref):
    """Actual implementation of model registration"""
    try:
        logger.info("Registering database models...")
        
        # Import order matters - base models first
        from database import models
        from database import integration_models
        from database import syntax_models
        
        # Track registered model types (representative sample)
        cls_ref._models_registered.add("Word")
        cls_ref._models_registered.add("Author")
        cls_ref._models_registered.add("UserProfile")
        cls_ref._models_registered.add("SentenceAnalysis")
        cls_ref._models_registered.add("LessonProgress")
        
        cls_ref._initialized = True
        logger.info(f"✓ Successfully registered {len(cls_ref._models_registered)} model types")
        
    except ImportError as e:
        logger.error(f"Failed to import model modules: {e}")
        raise ModelRegistryError(f"Failed to import models: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during model registration: {e}")
        raise ModelRegistryError(f"Model registration failed: {e}")

# Define cached version at module level
try:
    import streamlit as st
    
    @st.cache_resource(show_spinner=False)
    def _register_models_cached():
        """Cached wrapper for model registration"""
        class DummyRegistry:
            _models_registered = set()
            _initialized = False
            
        _register_models_impl(DummyRegistry)
        return True
        
    @st.cache_resource(show_spinner=False)
    def _get_models_module_cached():
        """Cached wrapper to get models module"""
        from database import models
        return models
        
except (ImportError, AttributeError):
    def _register_models_cached():
        pass
    def _get_models_module_cached():
        from database import models
        return models
    

