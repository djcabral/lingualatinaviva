from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime


class Author(SQLModel, table=True):
    """Autor clásico latino"""
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)  # "Caesar", "Cicero", etc.
    full_name: Optional[str] = None  # "Gaius Julius Caesar"
    difficulty_level: int  # 1-4
    period: Optional[str] = None  # "Republican", "Imperial"
    description: Optional[str] = None
    
    # Relaciones
    words: List["Word"] = Relationship(back_populates="author")
    texts: List["Text"] = Relationship(back_populates="author")



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
    
    # For 3rd declension nouns: True = parisyllabic (gen_pl -ium), False = imparisyllabic (gen_pl -um)
    parisyllabic: Optional[bool] = None
    
    # NUEVOS CAMPOS - Fase 1
    author_id: Optional[int] = Field(default=None, foreign_key="author.id")
    frequency_rank_global: Optional[int] = None  # Rango de frecuencia general (1 = más frecuente)
    is_invariable: bool = Field(default=False)  # Preposiciones, adverbios, conjunciones
    is_fundamental: bool = Field(default=False)  # Top 100 + invariables importantes
    category: Optional[str] = None  # "preposition", "adverb", "conjunction", etc.
    irregular_forms: Optional[str] = None  # JSON string overriding specific forms e.g. {"dat_pl": "filiābus"}
    
    # Collatinus dictionary integration
    definition_es: Optional[str] = None  # Full Spanish definition from Collatinus
    collatinus_lemma: Optional[str] = None  # Original lemma form from Collatinus
    collatinus_model: Optional[str] = None  # Flexion model (e.g., amo, lupus, rex)
    
    # Reservoir System
    status: str = Field(default="active")     # 'active', 'reservoir', 'hidden'
    
    # Relaciones
    reviews: List["ReviewLog"] = Relationship(back_populates="word")
    text_links: List["TextWordLink"] = Relationship(back_populates="word")
    author: Optional["Author"] = Relationship(back_populates="words")
    frequencies: List["WordFrequency"] = Relationship(back_populates="word")

class ReviewLog(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    word_id: int = Field(foreign_key="word.id")
    review_date: datetime = Field(default_factory=datetime.utcnow)
    quality: int # 0-5 rating
    ease_factor: float = Field(default=2.5)
    interval: int = Field(default=0) # Days until next review
    repetitions: int = Field(default=0)
    
    word: Optional["Word"] = Relationship(back_populates="reviews")

class UserProfile(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    level: int = Field(default=1)
    xp: int = Field(default=0)
    streak: int = Field(default=0)
    last_login: datetime = Field(default_factory=datetime.utcnow)

class Text(SQLModel, table=True):
    """Texto latino para lectura progresiva"""
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    author_id: Optional[int] = Field(default=None, foreign_key="author.id")
    title: str = Field(index=True)
    book_number: Optional[int] = None
    chapter_number: Optional[int] = None
    content: str  # Full Latin text
    difficulty: int = Field(default=1)  # 1-10
    grammar_focus: Optional[str] = None  # JSON array como string
    syntax_focus: Optional[str] = None   # JSON array como string
    min_xp_required: int = Field(default=0)
    is_unlocked_by_default: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relaciones
    author: Optional["Author"] = Relationship(back_populates="texts")
    word_links: List["TextWordLink"] = Relationship(back_populates="text")

class TextWordLink(SQLModel, table=True):
    """Vincula palabras con textos (con anotaciones morfológicas y sintácticas)"""
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    text_id: int = Field(foreign_key="text.id")
    word_id: int = Field(foreign_key="word.id")
    sentence_number: int = Field(default=1)
    position_in_sentence: int = Field(default=1)
    morphology_json: Optional[str] = None  # JSON: {"case": "nom", "number": "sg"}
    syntax_role: Optional[str] = None  # "subject", "direct_object", etc.
    notes: Optional[str] = None  # Explicaciones contextuales
    
    # Relaciones
    text: Optional["Text"] = Relationship(back_populates="word_links")
    word: Optional["Word"] = Relationship(back_populates="text_links")


class WordFrequency(SQLModel, table=True):
    """Frecuencia de palabras en el corpus"""
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    word_id: int = Field(foreign_key="word.id", index=True)
    author_id: Optional[int] = Field(default=None, foreign_key="author.id")
    frequency_rank: int  # 1 = más frecuente
    occurrence_count: int = Field(default=0)  # Veces que aparece
    is_top_100: bool = Field(default=False)
    is_top_500: bool = Field(default=False)
    
    # Relaciones
    word: Optional["Word"] = Relationship(back_populates="frequencies")
    author: Optional["Author"] = Relationship()


class SyntaxPattern(SQLModel, table=True):
    """Patrones sintácticos especiales del latín"""
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)  # "Ablativo absoluto", "Acusativo + infinitivo"
    category: str  # "verbal_construction", "case_usage", etc.
    description: str
    example_latin: Optional[str] = None
    example_translation: Optional[str] = None
    difficulty: int = Field(default=1)  # 1-10


class InflectedForm(SQLModel, table=True):
    """Formas inflectadas generadas automáticamente para análisis reverso (forma → lema)"""
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    form: str = Field(index=True)  # La forma inflectada con macrones, ej: "puellae"
    normalized_form: str = Field(index=True)  # Sin macrones para búsqueda: "puellae"
    
    word_id: int = Field(foreign_key="word.id")
    
    # Análisis morfológico en JSON
    # Para sustantivos: {"case": "gen", "number": "sg"}
    # Para verbos: {"tense": "pres", "person": "1", "number": "sg", "mood": "ind", "voice": "act"}
    morphology: str
    
    # Relación
    word: Optional["Word"] = Relationship()
