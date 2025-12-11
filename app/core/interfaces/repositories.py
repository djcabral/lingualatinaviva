"""
Repository interfaces defining the contract for data access.
These abstract the actual database implementation from the business logic.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from app.core.models.entities import Word, Author, User, ReviewLog, Lesson, Challenge, UserProgress, Text


class WordRepository(ABC):
    """Interface for word data access operations."""
    
    @abstractmethod
    def get_by_id(self, word_id: int) -> Optional[Word]:
        pass
    
    @abstractmethod
    def get_by_latin(self, latin: str) -> Optional[Word]:
        pass
    
    @abstractmethod
    def search(self, term: str, limit: int = 50) -> List[Word]:
        pass
    
    @abstractmethod
    def get_words_for_lesson(self, lesson_id: int) -> List[Word]:
        pass
    
    @abstractmethod
    def get_words_due_for_review(self, user_id: int) -> List[Word]:
        pass
    
    @abstractmethod
    def save(self, word: Word) -> Word:
        pass
    
    @abstractmethod
    def update(self, word: Word) -> Word:
        pass
    
    @abstractmethod
    def delete(self, word_id: int) -> bool:
        pass


class AuthorRepository(ABC):
    """Interface for author data access operations."""
    
    @abstractmethod
    def get_by_id(self, author_id: int) -> Optional[Author]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[Author]:
        pass
    
    @abstractmethod
    def save(self, author: Author) -> Author:
        pass


class UserRepository(ABC):
    """Interface for user data access operations."""
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        pass
    
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def save(self, user: User) -> User:
        pass
    
    @abstractmethod
    def update(self, user: User) -> User:
        pass


class LessonRepository(ABC):
    """Interface for lesson data access operations."""
    
    @abstractmethod
    def get_by_id(self, lesson_id: int) -> Optional[Lesson]:
        pass
    
    @abstractmethod
    def get_by_number(self, lesson_number: int) -> Optional[Lesson]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[Lesson]:
        pass
    
    @abstractmethod
    def get_published(self) -> List[Lesson]:
        pass
    
    @abstractmethod
    def save(self, lesson: Lesson) -> Lesson:
        pass


class TextRepository(ABC):
    """Interface for text data access operations."""
    
    @abstractmethod
    def get_by_id(self, text_id: int) -> Optional[Text]:
        pass
    
    @abstractmethod
    def get_by_difficulty(self, min_difficulty: int, max_difficulty: int) -> List[Text]:
        pass
    
    @abstractmethod
    def search(self, query: str) -> List[Text]:
        pass
    
    @abstractmethod
    def save(self, text: Text) -> Text:
        pass


class ChallengeRepository(ABC):
    """Interface for challenge data access operations."""
    
    @abstractmethod
    def get_by_id(self, challenge_id: int) -> Optional[Challenge]:
        pass
    
    @abstractmethod
    def get_all_ordered(self) -> List[Challenge]:
        pass
    
    @abstractmethod
    def get_available_for_user(self, user_id: int) -> List[Challenge]:
        pass
    
    @abstractmethod
    def save(self, challenge: Challenge) -> Challenge:
        pass


class ProgressRepository(ABC):
    """Interface for progress tracking operations."""
    
    @abstractmethod
    def get_user_progress(self, user_id: int, activity_type: str, activity_id: int) -> Optional[UserProgress]:
        pass
    
    @abstractmethod
    def get_user_progress_list(self, user_id: int, activity_type: str) -> List[UserProgress]:
        pass
    
    @abstractmethod
    def save_progress(self, progress: UserProgress) -> UserProgress:
        pass
    
    @abstractmethod
    def update_progress(self, progress: UserProgress) -> UserProgress:
        pass


class RepositoryProvider(ABC):
    """Provider interface for accessing all repositories."""
    
    @property
    @abstractmethod
    def words(self) -> WordRepository:
        pass
    
    @property
    @abstractmethod
    def authors(self) -> AuthorRepository:
        pass
    
    @property
    @abstractmethod
    def users(self) -> UserRepository:
        pass
    
    @property
    @abstractmethod
    def lessons(self) -> LessonRepository:
        pass
    
    @property
    @abstractmethod
    def texts(self) -> TextRepository:
        pass
    
    @property
    @abstractmethod
    def challenges(self) -> ChallengeRepository:
        pass
    
    @property
    @abstractmethod
    def progress(self) -> ProgressRepository:
        pass