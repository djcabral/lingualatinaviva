"""
Vocabulary service.
Handles vocabulary-related operations including spaced repetition.
"""

from typing import List
from app.core.models.entities import Word, ReviewLog
from app.core.interfaces.repositories import RepositoryProvider


class VocabularyService:
    """Service for managing vocabulary-related operations."""
    
    def __init__(self, repositories: RepositoryProvider):
        self._repos = repositories
    
    def get_vocabulary_for_review(self, user_id: int) -> List[Word]:
        """Get vocabulary items that are due for review."""
        return self._repos.words.get_words_due_for_review(user_id)
    
    def search_vocabulary(self, term: str, limit: int = 50) -> List[Word]:
        """Search vocabulary by term."""
        return self._repos.words.search(term, limit)
    
    def get_word_by_latin(self, latin: str) -> Word:
        """Get a word by its Latin form."""
        word = self._repos.words.get_by_latin(latin)
        if not word:
            raise ValueError(f"Word '{latin}' not found")
        return word
    
    def record_review(self, word_id: int, user_id: int, quality: int) -> ReviewLog:
        """Record a vocabulary review using spaced repetition algorithm."""
        # Simplified SM-2 algorithm implementation
        # In a real implementation, this would be more sophisticated
        
        review_log = ReviewLog(
            id=None,
            word_id=word_id,
            review_date=None,  # Will be set to current time
            quality=quality,
            ease_factor=2.5,
            interval=0,
            repetitions=0
        )
        
        # TODO: Implement proper spaced repetition algorithm
        # This is a simplified version for demonstration
        
        return review_log
    
    def get_word_mastery(self, word_id: int, user_id: int) -> float:
        """
        Calculate mastery level for a specific word
        
        Args:
            word_id: ID of the word
            user_id: ID of the user
            
        Returns:
            Mastery level (0.0 to 1.0)
        """
        # TODO: Implement mastery calculation
        return 0.0
    
    def get_vocabulary_stats(self, user_id: int) -> dict:
        """
        Get vocabulary statistics for a user
        
        Args:
            user_id: ID of the user
            
        Returns:
            Dictionary with vocabulary statistics
        """
        # TODO: Implement stats calculation
        return {
            "learned": 0,
            "mastered": 0,
            "due_for_review": 0,
            "total": 0
        }