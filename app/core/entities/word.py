"""
Word Entity

Domain entity representing a Latin word with its properties and behaviors.
"""

from typing import Optional, List
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Word:
    """Core domain entity representing a Latin word"""
    id: Optional[int] = None
    latin: str = ""
    translation: str = ""
    part_of_speech: str = ""
    level: int = 1
    genitive: Optional[str] = None
    gender: Optional[str] = None
    declension: Optional[str] = None
    principal_parts: Optional[str] = None
    conjugation: Optional[str] = None
    parisyllabic: Optional[bool] = None
    is_plurale_tantum: bool = False
    is_singulare_tantum: bool = False
    author_id: Optional[int] = None
    frequency_rank_global: Optional[int] = None
    is_invariable: bool = False
    is_fundamental: bool = False
    category: Optional[str] = None
    irregular_forms: Optional[str] = None
    cultural_context: Optional[str] = None
    definition_es: Optional[str] = None
    collatinus_lemma: Optional[str] = None
    collatinus_model: Optional[str] = None
    status: str = "active"

@dataclass
class ReviewLog:
    """Entity representing a vocabulary review session"""
    id: Optional[int] = None
    word_id: int = 0
    review_date: datetime = datetime.now()
    quality: int = 0  # 0-5 rating
    ease_factor: float = 2.5
    interval: int = 0  # Days until next review
    repetitions: int = 0

@dataclass
class Author:
    """Entity representing a classical Latin author"""
    id: Optional[int] = None
    name: str = ""
    full_name: Optional[str] = None
    difficulty_level: int = 1
    period: Optional[str] = None
    description: Optional[str] = None