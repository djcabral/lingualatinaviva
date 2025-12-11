"""
User Service
Handles user-related business logic and operations.
"""
from typing import Optional
from app.models.core import User
from app.repositories.base import BaseRepository
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import UserProfile


class UserService:
    """Service for handling user-related operations."""
    
    def __init__(self, session: Session):
        self.session = session

    def get_or_create_user(self, username: str) -> User:
        """
        Get existing user or create a new one.
        
        Args:
            username: Username to lookup or create
            
        Returns:
            User instance
        """
        # Try to find existing user
        db_user = self.session.exec(select(UserProfile).where(UserProfile.username == username)).first()
        
        if db_user:
            # Convert database model to domain model
            return User(
                id=db_user.id,
                username=db_user.username,
                level=db_user.level,
                xp=db_user.xp,
                streak=db_user.streak
            )
        
        # Create new user
        db_user = UserProfile(
            username=username,
            level=1,
            xp=0,
            streak=0
        )
        
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        
        return User(
            id=db_user.id,
            username=db_user.username,
            level=db_user.level,
            xp=db_user.xp,
            streak=db_user.streak
        )

    def update_user_progress(self, user_id: int, xp_gain: int = 0) -> User:
        """
        Update user progress with XP gain.
        
        Args:
            user_id: ID of the user
            xp_gain: Amount of XP to add
            
        Returns:
            Updated User instance
        """
        db_user = self.session.exec(select(UserProfile).where(UserProfile.id == user_id)).first()
        
        if not db_user:
            raise ValueError(f"User with id {user_id} not found")
            
        db_user.xp += xp_gain
        
        # Update level based on XP (simplified)
        db_user.level = max(db_user.level, xp_gain // 100 + 1)
        
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        
        return User(
            id=db_user.id,
            username=db_user.username,
            level=db_user.level,
            xp=db_user.xp,
            streak=db_user.streak
        )

    def get_user_stats(self, user_id: int) -> dict:
        """
        Get user statistics.
        
        Args:
            user_id: ID of the user
            
        Returns:
            Dictionary with user statistics
        """
        db_user = self.session.exec(select(UserProfile).where(UserProfile.id == user_id)).first()
        
        if not db_user:
            raise ValueError(f"User with id {user_id} not found")
            
        return {
            "level": db_user.level,
            "xp": db_user.xp,
            "streak": db_user.streak
        }