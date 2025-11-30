"""
Modelos extendidos para el Sistema de Integración Orgánica
Este módulo complementa database/models.py con nuevos modelos para:
- Progreso detallado del usuario por lección
- Vocabulario por lección
- Sistema de desbloqueo
- Motor de recomendaciones
"""

from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship, JSON, Column
from datetime import datetime
import json


class LessonProgress(SQLModel, table=True):
    """Progreso del usuario en cada lección del curso"""
    __tablename__ = "lesson_progress"
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=1, index=True)  # FK a UserProfile
    lesson_number: int = Field(index=True)  # 1-40
    
    # Estado de la lección
    status: str = Field(default="locked")  # "locked", "unlocked", "in_progress", "completed"
    
    # Timestamps
    unlocked_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    last_accessed_at: Optional[datetime] = None
    
    # Tiempos
    total_time_spent: int = Field(default=0)  # Segundos
    
    # Métricas de comprensión (auto-evaluación)
    comprehension_rating: Optional[int] = None  # 1-5 estrellas
    notes: Optional[str] = None  # Notas del usuario


class LessonVocabulary(SQLModel, table=True):
    """Relación entre lecciones y vocabulario esencial"""
    __tablename__ = "lesson_vocabulary"
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    lesson_number: int = Field(index=True)
    word_id: int = Field(foreign_key="word.id", index=True)
    
    # Clasificación
    is_essential: bool = Field(default=True)  # Requerido para pasar el desafío
    is_secondary: bool = Field(default=False)  # Útil pero no esencial
    
    # Orden de presentación
    presentation_order: int = Field(default=0)
    
    # Contexto de la lección
    example_sentence: Optional[str] = None  # Ejemplo de uso en la lección
    notes: Optional[str] = None  # Por qué esta palabra es importante aquí


class UserVocabularyProgress(SQLModel, table=True):
    """Progreso del usuario con cada palabra individual"""
    __tablename__ = "user_vocabulary_progress"
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=1, index=True)
    word_id: int = Field(foreign_key="word.id", index=True)
    
    # Estadísticas de práctica
    times_seen: int = Field(default=0)
    times_correct: int = Field(default=0)
    times_incorrect: int = Field(default=0)
    
    # Nivel de dominio (0.0-1.0)
    mastery_level: float = Field(default=0.0)  # Calculado: correct / (correct + incorrect)
    
    # Sistema de repetición espaciada
    next_review_date: Optional[datetime] = None
    ease_factor: float = Field(default=2.5)  # SM-2 algorithm
    interval_days: int = Field(default=0)
    
    # Timestamps
    first_seen: datetime = Field(default_factory=datetime.utcnow)
    last_reviewed: Optional[datetime] = None
    
    # Estado
    is_learning: bool = Field(default=True)  # False cuando mastery >= 0.95
    is_mature: bool = Field(default=False)  # True cuando interval_days >= 21


class ExerciseAttempt(SQLModel, table=True):
    """Registro de intentos de ejercicios"""
    __tablename__ = "exercise_attempt"
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=1, index=True)
    lesson_number: int = Field(index=True)
    
    # Tipo de ejercicio
    exercise_type: str  # "declension", "conjugation", "translation", "construction", "identification"
    
    # Detalles del ejercicio (JSON)
    # Ejemplo: {"word": "puella", "case_asked": "accusative", "number": "plural"}
    exercise_config: str = Field(sa_column=Column(JSON))
    
    # Respuesta del usuario
    user_answer: str
    correct_answer: str
    is_correct: bool
    
    # Métricas
    time_spent_seconds: int
    hint_used: bool = Field(default=False)
    
    # Timestamp
    attempted_at: datetime = Field(default_factory=datetime.utcnow)


class ReadingProgress(SQLModel, table=True):
    """Progreso del usuario en lecturas"""
    __tablename__ = "reading_progress"
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=1, index=True)
    text_id: int = Field(foreign_key="text.id", index=True)
    
    # Estado
    status: str = Field(default="not_started")  # "not_started", "in_progress", "completed"
    
    # Métricas de comprensión
    words_looked_up: int = Field(default=0)  # Cuántas palabras necesitó buscar
    lookup_rate: float = Field(default=0.0)  # Calculated: lookups / total_words
    
    # Preguntas de comprensión (si aplica)
    comprehension_questions_total: int = Field(default=0)
    comprehension_questions_correct: int = Field(default=0)
    comprehension_score: float = Field(default=0.0)  # correct / total
    
    # Tiempos
    time_spent_reading: int = Field(default=0)  # Segundos
    
    # Timestamps
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    last_accessed_at: Optional[datetime] = None
    
    # Feedback del usuario
    difficulty_rating: Optional[int] = None  # 1-5 (1=muy fácil, 5=muy difícil)


class SyntaxAnalysisProgress(SQLModel, table=True):
    """Seguimiento de oraciones analizadas por el usuario"""
    __tablename__ = "syntax_analysis_progress"
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=1, index=True)
    sentence_analysis_id: int = Field(foreign_key="sentenceanalysis.id", index=True)
    lesson_number: Optional[int] = None  # Si la oración pertenece a una lección
    
    # Estado
    viewed: bool = Field(default=False)
    analyzed: bool = Field(default=False)  # El usuario intentó analizar activamente
    
    # Métricas de análisis (si el usuario intentó analizar)
    cases_identified_correct: int = Field(default=0)
    cases_identified_incorrect: int = Field(default=0)
    functions_identified_correct: int = Field(default=0)
    functions_identified_incorrect: int = Field(default=0)
    
    # Tiempo
    time_spent_analyzing: int = Field(default=0)
    
    # Timestamps
    first_viewed_at: Optional[datetime] = None
    analyzed_at: Optional[datetime] = None


class UserProgressSummary(SQLModel, table=True):
    """Resumen global del progreso del usuario (desnormalizado para eficiencia)"""
    __tablename__ = "user_progress_summary"
    __table_args__ = {'extend_existing': True}
    
    user_id: int = Field(primary_key=True, default=1)
    
    # Lecciones
    current_lesson: int = Field(default=1)
    lessons_completed: str = Field(default="[]")  # JSON array: [1, 2, 3]
    lessons_in_progress: str = Field(default="[]")  # JSON array
    
    # Vocabulario global
    total_words_learned: int = Field(default=0)  # mastery >= 0.5
    total_words_mastered: int = Field(default=0)  # mastery >= 0.8
    vocab_mastery_avg: float = Field(default=0.0)
    
    # Ejercicios global
    exercises_completed_total: int = Field(default=0)
    exercises_accuracy_avg: float = Field(default=0.0)
    
    # Lecturas
    texts_read_total: int = Field(default=0)
    comprehension_avg: float = Field(default=0.0)
    
    # Sintaxis
    sentences_analyzed_total: int = Field(default=0)
    
    # Desafíos
    challenges_passed: str = Field(default="[]")  # JSON array: [1, 2, 3, 4]
    challenges_failed_attempts: int = Field(default=0)
    
    # Áreas débiles (detectadas automáticamente)
    weak_areas: str = Field(default="[]")  # JSON array: ["Ablativo Plural", "Construcción activa"]
    
    # Gamificación
    total_xp: int = Field(default=0)
    level: int = Field(default=1)
    badges: str = Field(default="[]")  # JSON array: ["first_steps", "vocab_50"]
    
    # Timestamps
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)


class UnlockCondition(SQLModel, table=True):
    """Condiciones para desbloquear contenido"""
    __tablename__ = "unlock_condition"
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # ¿Qué se desbloquea?
    unlocks_type: str  # "lesson", "vocabulary_set", "reading", "challenge"
    unlocks_id: str  # ID del recurso (ej: "lesson_4", "vocab_l3", "reading_julia")
    
    # Condiciones (JSON array de objetos)
    # Ejemplo: [
    #   {"type": "lesson_completed", "lesson_number": 3},
    #   {"type": "vocab_mastery", "lesson_number": 3, "threshold": 0.8},
    #   {"type": "exercises_completed", "lesson_number": 3, "count": 5}
    # ]
    conditions_json: str = Field(sa_column=Column(JSON))
    
    # Lógica de combinación
    require_all: bool = Field(default=True)  # True = AND, False = OR


class Recommendation(SQLModel, table=True):
    """Recomendaciones generadas para el usuario (histórico)"""
    __tablename__ = " recommendation"
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=1, index=True)
    
    # Tipo de recomendación
    rec_type: str  # "vocabulary", "exercises", "reading", "review", "challenge"
    
    # Acción específica
    action: str  # "practice_vocab", "start_exercises", "review_grammar", "take_challenge"
    
    # Contexto
    lesson_number: Optional[int] = None
    topic: Optional[str] = None  # "Ablativo Plural", "1st Declension"
    
    # Mensaje
    message: str
    
    # Prioridad
    priority: str = Field(default="medium")  # "high", "medium", "low"
    
    # Estado
    status: str = Field(default="pending")  # "pending", "accepted", "dismissed", "completed"
    
    # Timestamps
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    acted_on_at: Optional[datetime] = None


# Helper functions para trabajar con JSON fields

def get_json_list(json_str: str) -> List:
    """Convierte un string JSON a lista"""
    try:
        return json.loads(json_str) if json_str else []
    except:
        return []

def set_json_list(items: List) -> str:
    """Convierte una lista a string JSON"""
    return json.dumps(items)
