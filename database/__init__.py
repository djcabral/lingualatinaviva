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
import sys

logger = logging.getLogger(__name__)

logger.debug("Initializing database package...")

# Check if models are already loaded to prevent re-registration
if 'database.models' not in sys.modules:
    # Import models directly (only happens once)
    from database import models
    from database import integration_models
    from database import syntax_models
else:
    # Models already imported, get references
    models = sys.modules['database.models']
    integration_models = sys.modules['database.integration_models']
    syntax_models = sys.modules['database.syntax_models']

# Re-export core models
Word = models.Word
Author = models.Author
ReviewLog = models.ReviewLog
UserProfile = models.UserProfile
Text = models.Text
TextWordLink = models.TextWordLink
WordFrequency = models.WordFrequency
SyntaxPattern = models.SyntaxPattern
InflectedForm = models.InflectedForm
Challenge = models.Challenge
UserChallengeProgress = models.UserChallengeProgress
Lesson = models.Lesson
Feedback = models.Feedback
SystemSetting = models.SystemSetting

# Integration models (learning progress system)
LessonProgress = integration_models.LessonProgress
LessonVocabulary = integration_models.LessonVocabulary
UserVocabularyProgress = integration_models.UserVocabularyProgress
ExerciseAttempt = integration_models.ExerciseAttempt
ReadingProgress = integration_models.ReadingProgress
SyntaxAnalysisProgress = integration_models.SyntaxAnalysisProgress
UserProgressSummary = integration_models.UserProgressSummary
UnlockCondition = integration_models.UnlockCondition
Recommendation = integration_models.Recommendation
LessonRequirement = integration_models.LessonRequirement
UserLessonProgress = integration_models.UserLessonProgress

# Syntax analysis models
SentenceAnalysis = syntax_models.SentenceAnalysis
SyntaxCategory = syntax_models.SyntaxCategory
SentenceCategoryLink = syntax_models.SentenceCategoryLink
TokenAnnotation = syntax_models.TokenAnnotation
SentenceStructure = syntax_models.SentenceStructure

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
