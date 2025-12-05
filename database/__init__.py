"""
Database Package - Centralized Import Point

This module serves as the single source of truth for all database models.
All application code should import from this module to ensure consistency
and prevent model registry duplication.

USAGE:
    # CORRECT - Import from database package
    from database import Word, Author, UserProfile
    
    # INCORRECT - Don't import directly from submodules
    from database.models import Word  # ❌ Avoid this
    
CRITICAL: This ensures models are only registered once in SQLAlchemy's global registry.
"""

import logging

logger = logging.getLogger(__name__)

logger.debug("Initializing database package...")

# CRITICAL: Use cached loader to prevent duplicate model registration
from database.models_loader import get_models

# Get models from cache (will only import once per session)
_models_dict = get_models()
models_module = _models_dict['models']
integration_models_module = _models_dict['integration_models']
syntax_models_module = _models_dict['syntax_models']

# Re-export core models from cached modules
Word = models_module.Word
Author = models_module.Author
ReviewLog = models_module.ReviewLog
UserProfile = models_module.UserProfile
Text = models_module.Text
TextWordLink = models_module.TextWordLink
WordFrequency = models_module.WordFrequency
SyntaxPattern = models_module.SyntaxPattern
InflectedForm = models_module.InflectedForm
Challenge = models_module.Challenge
UserChallengeProgress = models_module.UserChallengeProgress
Lesson = models_module.Lesson
Feedback = models_module.Feedback
SystemSetting = models_module.SystemSetting

# Integration models (learning progress system)
LessonProgress = integration_models_module.LessonProgress
LessonVocabulary = integration_models_module.LessonVocabulary
UserVocabularyProgress = integration_models_module.UserVocabularyProgress
ExerciseAttempt = integration_models_module.ExerciseAttempt
ReadingProgress = integration_models_module.ReadingProgress
SyntaxAnalysisProgress = integration_models_module.SyntaxAnalysisProgress
UserProgressSummary = integration_models_module.UserProgressSummary
UnlockCondition = integration_models_module.UnlockCondition
Recommendation = integration_models_module.Recommendation
LessonRequirement = integration_models_module.LessonRequirement
UserLessonProgress = integration_models_module.UserLessonProgress

# Syntax analysis models
SentenceAnalysis = syntax_models_module.SentenceAnalysis
SyntaxCategory = syntax_models_module.SyntaxCategory
SentenceCategoryLink = syntax_models_module.SentenceCategoryLink
TokenAnnotation = syntax_models_module.TokenAnnotation
SentenceStructure = syntax_models_module.SentenceStructure

# Connection utilities
from database.connection import (
    get_session,
    init_db,
    engine
)

# Helper functions
from database.utils import (
    get_json_list,
    set_json_list
)

# Export all for "from database import *" (though explicit imports are preferred)
__all__ = [
    # Core models
    'Word',
    'Author',
    'ReviewLog',
    'UserProfile',
    'Text',
    'TextWordLink',
    'WordFrequency',
    'SyntaxPattern',
    'InflectedForm',
    'Challenge',
    'UserChallengeProgress',
    'Lesson',
    'Feedback',
    'SystemSetting',
    
    # Integration models
    'LessonProgress',
    'LessonVocabulary',
    'UserVocabularyProgress',
    'ExerciseAttempt',
    'ReadingProgress',
    'SyntaxAnalysisProgress',
    'UserProgressSummary',
    'UnlockCondition',
    'Recommendation',
    'LessonRequirement',
    'UserLessonProgress',
    
    # Syntax models
    'SentenceAnalysis',
    'SyntaxCategory',
    'SentenceCategoryLink',
    'TokenAnnotation',
    'SentenceStructure',
    
    # Connection utilities
    'get_session',
    'init_db',
    'engine',
    
    # Helper functions
    'get_json_list',
    'set_json_list',
]

logger.info(f"✓ Database package initialized with {len(__all__)} exported items")
