from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# CRITICAL: Prevent duplicate model registration
# This module should only be loaded ONCE per Python process
# If you see this warning, it indicates a potential registry duplication issue
if '__MODELS_MODULE_LOADED__' in globals():
    logger.warning("⚠️  WARNING: database.models is being reloaded! This may cause 'Multiple classes found' errors.")
    logger.warning("    Check your imports - models should only be imported through database/__init__.py")
else:
    globals()['__MODELS_MODULE_LOADED__'] = True
    logger.debug("database.models loaded successfully")

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
    
    # Pluralia tantum: solo existe en plural (e.g., castra, arma, divitiae)
    is_plurale_tantum: bool = Field(default=False)
    
    # Singularia tantum: solo existe en singular
    is_singulare_tantum: bool = Field(default=False)
    
    # NUEVOS CAMPOS - Fase 1
    author_id: Optional[int] = Field(default=None, foreign_key="author.id")
    frequency_rank_global: Optional[int] = None  # Rango de frecuencia general (1 = más frecuente)
    is_invariable: bool = Field(default=False)  # Preposiciones, adverbios, conjunciones
    is_fundamental: bool = Field(default=False)  # Top 100 + invariables importantes
    category: Optional[str] = None  # "preposition", "adverb", "conjunction", etc.
    irregular_forms: Optional[str] = None  # JSON string overriding specific forms e.g. {"dat_pl": "filiābus"}
    cultural_context: Optional[str] = None  # Cultural note related to the word (e.g., "Patria Potestas" for "pater")
    
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
    
    # Campos gamificados (Sistema de Desafíos)
    total_stars: int = Field(default=0)
    challenges_completed: int = Field(default=0)
    perfect_challenges: int = Field(default=0)  # Con 3 estrellas
    current_challenge_id: Optional[int] = None
    badges_json: Optional[str] = None  # JSON: ["declension_master", "speed_demon", ...]
    
    # Preferencias de usuario
    preferences_json: Optional[str] = None  # JSON: {"font_size": 1.3, "theme": "dark", ...}


class UserLessonProgressV2(SQLModel, table=True):
    """
    Progreso del usuario en el sistema de aprendizaje orgánico de 5 pasos (V2).
    
    Flujo: TEORÍA → VOCABULARIO (50%) → EJERCICIOS (3x) → LECTURA → DESAFÍO
    
    Nota: Este modelo es distinto a integration_models.UserLessonProgress
    que está vinculado a LessonRequirement. Este modelo V2 implementa
    el sistema de progresión orgánica de 5 pasos.
    """
    __tablename__ = "user_lesson_progress_v2"
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=1, index=True)
    lesson_id: int = Field(index=True)
    
    # Paso 1: Teoría
    theory_completed: bool = Field(default=False)
    theory_completed_at: Optional[datetime] = None
    
    # Paso 2: Vocabulario (mastery basado en ReviewLog)
    vocab_mastery: float = Field(default=0.0)  # 0.0 - 1.0 (50% para desbloquear ejercicios)
    
    # Paso 3: Ejercicios
    exercises_count: int = Field(default=0)  # Número de sesiones completadas (3 para desbloquear lectura)
    
    # Paso 4: Lectura
    reading_completed: bool = Field(default=False)
    reading_completed_at: Optional[datetime] = None
    
    # Paso 5: Desafío Final
    challenge_passed: bool = Field(default=False)
    challenge_stars: int = Field(default=0)  # 0-3
    challenge_passed_at: Optional[datetime] = None
    
    # Metadatos
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


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
    word_id: Optional[int] = Field(default=None, foreign_key="word.id")  # NULL para palabras no en vocabulario
    sentence_number: int = Field(default=1)
    position_in_sentence: int = Field(default=1)
    form: Optional[str] = None  # Forma exacta como aparece en el texto (para CLTK)
    morphology_json: Optional[str] = None  # JSON: {"case": "nom", "number": "sg"}
    syntax_role: Optional[str] = None  # "subject", "direct_object", etc.
    notes: Optional[str] = None  # Explicaciones contextuales o análisis CLTK adicional
    
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


class Challenge(SQLModel, table=True):
    """Desafío gamificado del mapa de aprendizaje"""
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    order: int = Field(index=True, unique=True)  # Posición en el mapa (1, 2, 3...)
    title: str  # "Rosa: Nominativo y Acusativo"
    description: str  # Descripción completa del desafío
    
    # Tipo de desafío
    challenge_type: str  # "declension", "conjugation", "multiple_choice", "translation", "syntax"
    
    # Configuración del desafío (JSON)
    # Ejemplo declension: {"word": "rosa", "cases": ["nominative", "accusative"], "numbers": ["singular", "plural"]}
    # Ejemplo conjugation: {"verb": "amo", "tense": "present", "mood": "indicative"}
    # Ejemplo multiple_choice: {"questions": [{"text": "...", "options": [...], "correct": 0}]}
    config_json: str
    
    # Recompensas
    xp_reward: int = Field(default=10)
    
    # Prerequisites (IDs de desafíos previos que deben completarse)
    requires_challenge_ids: Optional[str] = None  # NULL o "1,2,3"
    
    # Metadatos educativos
    grammar_topic: Optional[str] = None  # "1st_declension", "present_indicative"
    difficulty_level: int = Field(default=1)  # 1-10
    
    # Relaciones
    progress: List["UserChallengeProgress"] = Relationship(back_populates="challenge")


class UserChallengeProgress(SQLModel, table=True):
    """Progreso del usuario en cada desafío"""
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=1)  # Por ahora usuario único
    challenge_id: int = Field(foreign_key="challenge.id", index=True)
    
    # Estado
    status: str = Field(default="locked")  # "locked", "unlocked", "in_progress", "completed"
    stars: int = Field(default=0)  # 0-3 estrellas
    attempts: int = Field(default=0)
    
    # Métricas
    best_score: float = Field(default=0.0)  # 0.0-100.0 (porcentaje de aciertos)
    total_errors: int = Field(default=0)
    completion_time: Optional[int] = None  # Segundos (NULL si no completado)
    
    # Timestamps
    unlocked_at: Optional[datetime] = None
    first_attempt_at: Optional[datetime] = None
    last_attempt_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # Relación
    challenge: Optional["Challenge"] = Relationship(back_populates="progress")


class Lesson(SQLModel, table=True):
    """Lección del curso de gramática latina"""
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    lesson_number: int = Field(index=True, unique=True)  # 1-40+
    title: str  # "Primeros Pasos", "El Sujeto (Nominativo)", etc.
    level: str  # "basico", "avanzado", "experto"
    
    # Content
    content_markdown: str  # Full markdown content of the lesson
    image_path: Optional[str] = None  # Path to main lesson image (relative to static/)
    
    # Metadata
    is_published: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Display order within level (for custom sorting)
    order_in_level: int = Field(default=0)




class Feedback(SQLModel, table=True):
    """Feedback, comentarios y sugerencias de los usuarios"""
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=1) # Por ahora usuario único, pero preparado para multi-usuario
    name: str
    email: str
    message: str
    feedback_type: str = Field(default="general") # "general", "bug", "feature_request", "content_issue"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_read: bool = Field(default=False)


class SystemSetting(SQLModel, table=True):
    """Configuración global del sistema (key-value)"""
    __table_args__ = {'extend_existing': True}
    
    key: str = Field(primary_key=True)
    value: str
    description: Optional[str] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)
