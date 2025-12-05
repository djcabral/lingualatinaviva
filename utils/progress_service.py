"""
Servicio de Progreso (Progress Service)
Este módulo gestiona el seguimiento del progreso del usuario y el registro de actividad.

Funciones principales:
- update_user_progress_summary: Actualiza el resumen global del usuario
- record_lesson_view: Registra la visualización de una lección
- get_user_progress: Obtiene el resumen de progreso actual
"""

from typing import Optional, Dict, Any
from sqlmodel import Session, select
from datetime import datetime

from database import (
    UserProgressSummary,
    LessonProgress,
    UserVocabularyProgress,
    UserProfile,
    LessonVocabulary
)

def get_user_progress(session: Session, user_id: int) -> UserProgressSummary:
    """
    Obtiene o crea el resumen de progreso del usuario.
    """
    summary = session.exec(
        select(UserProgressSummary).where(UserProgressSummary.user_id == user_id)
    ).first()
    
    if not summary:
        summary = UserProgressSummary(
            user_id=user_id,
            current_lesson=1,
            vocab_mastery_avg=0.0,
            total_xp=0,
            streak_days=0,
            last_active=datetime.utcnow()
        )
        session.add(summary)
        session.commit()
        session.refresh(summary)
        
    return summary

def update_user_progress_summary(session: Session, user_id: int):
    """
    Recalcula y actualiza el resumen de progreso del usuario.
    """
    summary = get_user_progress(session, user_id)
    
    # 1. Calcular XP Total
    user_profile = session.exec(select(UserProfile).where(UserProfile.id == user_id)).first()
    if user_profile:
        summary.total_xp = user_profile.total_xp
    
    # 2. Calcular Promedio de Vocabulario
    # Solo consideramos palabras que el usuario ha empezado a estudiar
    vocab_progress = session.exec(
        select(UserVocabularyProgress).where(UserVocabularyProgress.user_id == user_id)
    ).all()
    
    if vocab_progress:
        total_mastery = sum(vp.mastery_level for vp in vocab_progress)
        summary.vocab_mastery_avg = total_mastery / len(vocab_progress)
    else:
        summary.vocab_mastery_avg = 0.0
        
    # 3. Actualizar última actividad
    summary.last_active = datetime.utcnow()
    
    session.add(summary)
    session.commit()

def record_lesson_view(session: Session, user_id: int, lesson_number: int):
    """
    Registra que un usuario ha visto una lección.
    Si es la primera vez, crea el registro.
    Actualiza el timestamp de último acceso.
    """
    # Buscar registro existente
    progress = session.exec(
        select(LessonProgress).where(
            LessonProgress.user_id == user_id,
            LessonProgress.lesson_number == lesson_number
        )
    ).first()
    
    now = datetime.utcnow()
    
    if not progress:
        # Crear nuevo registro
        progress = LessonProgress(
            user_id=user_id,
            lesson_number=lesson_number,
            status='in_progress',
            started_at=now,
            last_accessed_at=now,
            total_time_spent=0 # TODO: Implementar tracking de tiempo real
        )
        session.add(progress)
    else:
        # Actualizar existente
        progress.last_accessed_at = now
        session.add(progress)
        
    # Actualizar lección actual en el resumen si es mayor a la actual
    summary = get_user_progress(session, user_id)
    if lesson_number > summary.current_lesson:
        # Solo avanzamos si la lección anterior está completada o si es la siguiente lógica
        # Por ahora, permitimos avanzar libremente para no bloquear
        summary.current_lesson = lesson_number
        session.add(summary)
        
    session.commit()

def record_exercise_attempt(
    session: Session,
    user_id: int,
    lesson_number: int,
    exercise_type: str,
    is_correct: bool,
    user_answer: str = "",
    correct_answer: str = "",
    xp_earned: int = 0,
    time_spent_seconds: int = 0
):
    """
    Records an exercise attempt using the ExerciseAttempt model.
    
    Args:
        session: Database session
        user_id: User ID
        lesson_number: Lesson number where exercise was attempted
        exercise_type: "mc" | "vocab" | "fill" | "syntax"
        is_correct: Whether the answer was correct
        user_answer: What the user answered
        correct_answer: The correct answer
        xp_earned: XP earned (default 10 for correct, 0 for wrong)
        time_spent_seconds: Time spent on the exercise
    """
    from database import ExerciseAttempt, UserProfile
    
    # 1. Record the attempt
    attempt = ExerciseAttempt(
        user_id=user_id,
        lesson_number=lesson_number,
        exercise_type=exercise_type,
        exercise_config="{}",  # Simplified - can be expanded
        user_answer=user_answer,
        correct_answer=correct_answer,
        is_correct=is_correct,
        time_spent_seconds=time_spent_seconds,
        attempted_at=datetime.utcnow()
    )
    session.add(attempt)
    
    # 2. Award XP if correct
    if is_correct and xp_earned == 0:
        xp_earned = 10  # Default XP for correct answer
    
    if xp_earned > 0:
        user = session.exec(select(UserProfile).where(UserProfile.id == user_id)).first()
        if user:
            user.xp = (user.xp or 0) + xp_earned
            session.add(user)
    
    session.commit()


