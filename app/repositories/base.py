"""
Base Repository Class
Provides common database operations for all repositories.
"""
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional
from sqlalchemy.orm import Session

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """
    Abstract base class for all repositories.
    Provides common CRUD operations.
    """
    
    def __init__(self, session: Session):
        self.session = session

    @abstractmethod
    def create(self, entity: T) -> T:
        """Create a new entity."""
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        """Retrieve an entity by its ID."""
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        """Retrieve all entities."""
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        """Update an existing entity."""
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        """Delete an entity by its ID."""
        pass