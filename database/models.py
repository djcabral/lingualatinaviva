from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime



class Word(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    latin: str = Field(index=True)
    translation: str
    part_of_speech: str  # noun, verb, adjective, etc.
    level: int = Field(default=1)
    
    # Morphological info (JSON stored as string or separate fields)
    genitive: Optional[str] = None # For nouns
    gender: Optional[str] = None # m, f, n
    declension: Optional[str] = None # 1, 2, 3, 4, 5
    
    principal_parts: Optional[str] = None # For verbs: amo, amare, amavi, amatum
    conjugation: Optional[str] = None # 1, 2, 3, 4, mixed
    
    reviews: List["ReviewLog"] = Relationship(back_populates="word")
    text_links: List["TextWordLink"] = Relationship(back_populates="word")

class ReviewLog(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    word_id: int = Field(foreign_key="word.id")
    review_date: datetime = Field(default_factory=datetime.utcnow)
    quality: int # 0-5 rating
    ease_factor: float = Field(default=2.5)
    interval: int = Field(default=0) # Days until next review
    repetitions: int = Field(default=0)
    
    word: Word = Relationship(back_populates="reviews")

class UserProfile(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    level: int = Field(default=1)
    xp: int = Field(default=0)
    streak: int = Field(default=0)
    last_login: datetime = Field(default_factory=datetime.utcnow)

class Text(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    author: Optional[str] = None
    content: str  # Full Latin text
    level: int = Field(default=1)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    word_links: List["TextWordLink"] = Relationship(back_populates="text")

class TextWordLink(SQLModel, table=True):
    """Many-to-many relationship between Text and Word"""
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    text_id: int = Field(foreign_key="text.id")
    word_id: int = Field(foreign_key="word.id")
    frequency: int = Field(default=1)  # How many times the word appears in the text
    
    text: Text = Relationship(back_populates="word_links")
    word: Word = Relationship(back_populates="text_links")
