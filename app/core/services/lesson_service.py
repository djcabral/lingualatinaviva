"""
Lesson service.
Handles lesson-related operations.
"""

from typing import List, Optional
from app.core.models.entities import Lesson, UserProgress
from app.core.interfaces.repositories import RepositoryProvider


class LessonService:
    """Service for managing lesson-related operations."""
    
    def __init__(self, repositories: RepositoryProvider):
        self._repos = repositories
    
    def get_all_lessons(self) -> List[Lesson]:
        """Get all published lessons."""
        return self._repos.lessons.get_published()
    
    def get_lesson_by_number(self, lesson_number: int) -> Optional[Lesson]:
        """Get a lesson by its number."""
        return self._repos.lessons.get_by_number(lesson_number)
    
    def get_user_progress(self, user_id: int, lesson_id: int) -> Optional[UserProgress]:
        """Get user's progress for a specific lesson."""
        return self._repos.progress.get_user_progress(user_id, "lesson", lesson_id)
    
    def get_next_lesson(self, user_id: int) -> Optional[Lesson]:
        """Get the next lesson for a user based on their progress."""
        # Get all lessons ordered by number
        lessons = self._repos.lessons.get_published()
        if not lessons:
            return None
            
        # Get user's completed lessons
        progress_list = self._repos.progress.get_user_progress_list(user_id, "lesson")
        completed_lesson_ids = {
            p.activity_id for p in progress_list 
            if p.status == "completed"
        }
        
        # Find the first incomplete lesson
        for lesson in lessons:
            if lesson.id not in completed_lesson_ids:
                return lesson
                
        # If all lessons are completed, return the last one
        return lessons[-1] if lessons else None