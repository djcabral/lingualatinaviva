"""
User Entity

Domain entity representing a user of the application with their learning progress.
"""

from typing import Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class UserProfile:
    """Core domain entity representing a user's profile and progress"""
    id: Optional[int] = None
    username: str = "discipulus"
    level: int = 1
    xp: int = 0
    streak: int = 0
    last_login: datetime = datetime.now()
    total_stars: int = 0
    challenges_completed: int = 0
    perfect_challenges: int = 0
    current_challenge_id: Optional[int] = None
    badges_json: Optional[str] = None
    preferences_json: Optional[str] = None

@dataclass
class UserProgress:
    """Entity representing detailed user progress metrics"""
    user_id: int = 0
    words_learned: int = 0
    words_mastered: int = 0
    exercises_completed: int = 0
    exercises_accuracy: float = 0.0
    texts_read: int = 0
    comprehension_rate: float = 0.0
    last_updated: datetime = datetime.now()