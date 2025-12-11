"""
User management service.
Handles user-related business logic.
"""

from typing import Optional
from app.core.models.entities import User
from app.core.interfaces.repositories import RepositoryProvider


class UserService:
    """Service for managing user-related operations."""
    
    def __init__(self, repositories: RepositoryProvider):
        self._repos = repositories
    
    def get_or_create_user(self, username: str) -> User:
        """Get existing user or create a new one."""
        user = self._repos.users.get_by_username(username)
        if not user:
            user = User(
                id=None,
                username=username,
                level=1,
                xp=0,
                streak=0
            )
            user = self._repos.users.save(user)
        return user
    
    def update_user_progress(self, user_id: int, xp_gain: int = 0) -> User:
        """Update user XP and level progression."""
        user = self._repos.users.get_by_id(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        
        user.xp += xp_gain
        
        # Simple leveling system - 100 XP per level
        new_level = user.xp // 100 + 1
        if new_level > user.level:
            user.level = new_level
            
        return self._repos.users.update(user)
    
    def update_user_streak(self, user_id: int) -> User:
        """Update user daily streak."""
        user = self._repos.users.get_by_id(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        
        user.streak += 1
        return self._repos.users.update(user)