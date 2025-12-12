"""
Progression Engine - Sistema de progresión orgánica de lecciones

Inspirado en el learningEngine.ts del proyecto TSX.
Implementa un flujo pedagógico de 5 pasos que se desbloquean secuencialmente:

1. GRAMÁTICA (Teoría) → 2. VOCABULARIO (50%) → 3. EJERCICIOS (3x) → 4. LECTURA → 5. DESAFÍO

El estudiante progresa a través de cada lección de forma guiada,
desbloqueando cada paso solo cuando completa el anterior.
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
from sqlmodel import Session, select
# Import from database package to avoid duplicate registration
from database import UserProfile, Word, ReviewLog
from database.models import UserLessonProgressV2V2
import logging

logger = logging.getLogger(__name__)

# Configuración del sistema de progresión
VOCAB_MASTERY_THRESHOLD = 0.5  # 50% del vocabulario debe dominarse
EXERCISES_REQUIRED = 3  # Número de sesiones de ejercicios requeridas


def get_lesson_status(session: Session, user_id: int, lesson_id: int) -> Dict:
    """
    Obtiene el estado completo de una lección para un usuario.
    
    Returns:
        {
            'theory_completed': bool,
            'vocab': {
                'unlocked': bool,
                'mastery': float (0-1),
                'completed': bool (>= 50%)
            },
            'exercises': {
                'unlocked': bool,
                'count': int,
                'completed': bool (>= 3)
            },
            'reading': {
                'unlocked': bool,
                'completed': bool
            },
            'challenge': {
                'unlocked': bool,
                'completed': bool
            },
            'overall_progress': float (0-1)  # Progreso general de la lección
        }
    """
    # Obtener o crear progreso de lección
    progress = session.exec(
        select(UserLessonProgressV2).where(
            UserLessonProgressV2.user_id == user_id,
            UserLessonProgressV2.lesson_id == lesson_id
        )
    ).first()
    
    if not progress:
        # Crear registro nuevo
        progress = UserLessonProgressV2(
            user_id=user_id,
            lesson_id=lesson_id,
            theory_completed=False,
            vocab_mastery=0.0,
            exercises_count=0,
            reading_completed=False,
            challenge_passed=False
        )
        session.add(progress)
        session.commit()
        session.refresh(progress)
    
    # Calcular estado de cada paso
    theory_completed = progress.theory_completed
    
    # Vocabulario: calcular mastery actual
    vocab_mastery = progress.vocab_mastery
    vocab_completed = vocab_mastery >= VOCAB_MASTERY_THRESHOLD
    vocab_unlocked = theory_completed
    
    # Ejercicios
    exercises_count = progress.exercises_count
    exercises_completed = exercises_count >= EXERCISES_REQUIRED
    exercises_unlocked = vocab_completed
    
    # Lectura
    reading_completed = progress.reading_completed
    reading_unlocked = exercises_completed
    
    # Desafío
    challenge_completed = progress.challenge_passed
    challenge_unlocked = reading_completed
    
    # Progreso general (cada paso vale 20%)
    overall_progress = 0.0
    if theory_completed:
        overall_progress += 0.2
    overall_progress += vocab_mastery * 0.2  # Contribución proporcional
    overall_progress += min(exercises_count / EXERCISES_REQUIRED, 1.0) * 0.2
    if reading_completed:
        overall_progress += 0.2
    if challenge_completed:
        overall_progress += 0.2
    
    return {
        'theory_completed': theory_completed,
        'vocab': {
            'unlocked': vocab_unlocked,
            'mastery': vocab_mastery,
            'completed': vocab_completed
        },
        'exercises': {
            'unlocked': exercises_unlocked,
            'count': exercises_count,
            'completed': exercises_completed
        },
        'reading': {
            'unlocked': reading_unlocked,
            'completed': reading_completed
        },
        'challenge': {
            'unlocked': challenge_unlocked,
            'completed': challenge_completed
        },
        'overall_progress': overall_progress
    }


def get_next_step_recommendation(session: Session, user_id: int, lesson_id: int) -> Optional[Dict]:
    """
    Retorna la siguiente acción recomendada para el usuario en una lección.
    
    Returns:
        {
            'step': str ('theory' | 'vocab' | 'exercises' | 'reading' | 'challenge'),
            'priority': str ('high' | 'medium' | 'low'),
            'title': str,
            'message': str,
            'action_page': str (nombre de la página Streamlit),
            'action_params': dict (parámetros para la acción)
        }
        
        None si la lección está completada
    """
    status = get_lesson_status(session, user_id, lesson_id)
    
    # Prioridad 1: Teoría
    if not status['theory_completed']:
        return {
            'step': 'theory',
            'priority': 'high',
            'title': 'Paso 1: Estudia la Teoría',
            'message': f'📖 Lee el contenido de la Lección {lesson_id} para comprender los conceptos gramaticales.',
            'action_page': 'Curso',
            'action_params': {'lesson_id': lesson_id}
        }
    
    # Prioridad 2: Vocabulario
    if not status['vocab']['completed']:
        mastery_pct = int(status['vocab']['mastery'] * 100)
        return {
            'step': 'vocab',
            'priority': 'high',
            'title': 'Paso 2: Domina el Vocabulario',
            'message': f'🧠 Practica las palabras clave hasta alcanzar 50% de dominio. Progreso actual: {mastery_pct}%',
            'action_page': 'Memorización',
            'action_params': {'lesson_id': lesson_id, 'mode': 'srs'}
        }
    
    # Prioridad 3: Ejercicios
    if not status['exercises']['completed']:
        count = status['exercises']['count']
        return {
            'step': 'exercises',
            'priority': 'high',
            'title': 'Paso 3: Practica con Ejercicios',
            'message': f'✍️ Completa sesiones de ejercicios para reforzar lo aprendido ({count}/{EXERCISES_REQUIRED}).',
            'action_page': 'Práctica',
            'action_params': {'lesson_id': lesson_id}
        }
    
    # Prioridad 4: Lectura
    if not status['reading']['completed']:
        return {
            'step': 'reading',
            'priority': 'high',
            'title': 'Paso 4: Lee Textos Auténticos',
            'message': f'📜 Aplica tus conocimientos leyendo textos latinos de la Lección {lesson_id}.',
            'action_page': 'Lecturas',
            'action_params': {'lesson_id': lesson_id}
        }
    
    # Prioridad 5: Desafío Final
    if not status['challenge']['completed']:
        return {
            'step': 'challenge',
            'priority': 'high',
            'title': '🏆 Paso 5: Supera el Desafío Final',
            'message': f'¡Demuestra tu dominio de la Lección {lesson_id}! Completa el desafío para desbloquear la siguiente lección.',
            'action_page': 'Juegos',
            'action_params': {'challenge_id': lesson_id}
        }
    
    # Lección completada
    return None


def update_theory_completion(session: Session, user_id: int, lesson_id: int) -> None:
    """Marca la teoría de una lección como completada."""
    progress = _get_or_create_progress(session, user_id, lesson_id)
    progress.theory_completed = True
    progress.theory_completed_at = datetime.utcnow()
    session.add(progress)
    session.commit()
    logger.info(f"User {user_id} completed theory for lesson {lesson_id}")


def update_vocab_mastery(session: Session, user_id: int, lesson_id: int) -> float:
    """
    Calcula y actualiza el dominio de vocabulario para una lección.
    
    Returns:
        float: Nivel de dominio (0.0 - 1.0)
    """
    # Obtener todas las palabras de la lección
    lesson_words = session.exec(
        select(Word).where(Word.level == lesson_id)
    ).all()
    
    if not lesson_words:
        return 0.0
    
    # Calcular mastery promedio basado en ReviewLog (SM-2)
    total_mastery = 0.0
    for word in lesson_words:
        # Obtener último review
        last_review = session.exec(
            select(ReviewLog)
            .where(ReviewLog.word_id == word.id)
            .order_by(ReviewLog.review_date.desc())
        ).first()
        
        if last_review:
            # Mastery basado en intervalo y facilidad
            # Intervalo alto + facilidad alta = mayor dominio
            word_mastery = min(
                (last_review.interval / 30.0) * (last_review.ease_factor / 2.5),
                1.0
            )
        else:
            word_mastery = 0.0
        
        total_mastery += word_mastery
    
    avg_mastery = total_mastery / len(lesson_words)
    
    # Actualizar progreso
    progress = _get_or_create_progress(session, user_id, lesson_id)
    progress.vocab_mastery = avg_mastery
    session.add(progress)
    session.commit()
    
    return avg_mastery


def increment_exercises_count(session: Session, user_id: int, lesson_id: int) -> int:
    """
    Incrementa el contador de ejercicios completados.
    
    Returns:
        int: Número actualizado de ejercicios
    """
    progress = _get_or_create_progress(session, user_id, lesson_id)
    progress.exercises_count += 1
    session.add(progress)
    session.commit()
    logger.info(f"User {user_id} completed exercise {progress.exercises_count} for lesson {lesson_id}")
    return progress.exercises_count


def mark_reading_completed(session: Session, user_id: int, lesson_id: int) -> None:
    """Marca la lectura de una lección como completada."""
    progress = _get_or_create_progress(session, user_id, lesson_id)
    progress.reading_completed = True
    progress.reading_completed_at = datetime.utcnow()
    session.add(progress)
    session.commit()
    logger.info(f"User {user_id} completed reading for lesson {lesson_id}")


def mark_challenge_passed(session: Session, user_id: int, lesson_id: int, stars: int = 3) -> None:
    """
    Marca el desafío de una lección como superado.
    Desbloquea la siguiente lección.
    """
    progress = _get_or_create_progress(session, user_id, lesson_id)
    progress.challenge_passed = True
    progress.challenge_stars = stars
    progress.challenge_passed_at = datetime.utcnow()
    session.add(progress)
    
    # Actualizar perfil de usuario (lección actual)
    user_profile = session.exec(
        select(UserProfile).where(UserProfile.id == user_id)
    ).first()
    
    if user_profile:
        # Avanzar a siguiente lección si es la actual
        if user_profile.level == lesson_id:
            user_profile.level = lesson_id + 1
            session.add(user_profile)
    
    session.commit()
    logger.info(f"User {user_id} passed challenge for lesson {lesson_id} with {stars} stars")


def get_overall_progress(session: Session, user_id: int, total_lessons: int = 30) -> Dict:
    """
    Obtiene el progreso general del usuario a través de todas las lecciones.
    
    Returns:
        {
            'current_lesson': int,
            'lessons_completed': int,
            'total_progress': float (0-1),
            'total_xp': int,
            'streak': int,
            'level': int
        }
    """
    user_profile = session.exec(
        select(UserProfile).where(UserProfile.id == user_id)
    ).first()
    
    if not user_profile:
        return {
            'current_lesson': 1,
            'lessons_completed': 0,
            'total_progress': 0.0,
            'total_xp': 0,
            'streak': 0,
            'level': 1
        }
    
    # Contar lecciones completadas (challenge passed)
    completed_lessons = session.exec(
        select(UserLessonProgressV2).where(
            UserLessonProgressV2.user_id == user_id,
            UserLessonProgressV2.challenge_passed == True
        )
    ).all()
    
    lessons_completed_count = len(completed_lessons)
    total_progress = lessons_completed_count / total_lessons
    
    return {
        'current_lesson': user_profile.level,
        'lessons_completed': lessons_completed_count,
        'total_progress': total_progress,
        'total_xp': user_profile.xp,
        'streak': user_profile.streak,
        'level': user_profile.level
    }


def _get_or_create_progress(session: Session, user_id: int, lesson_id: int) -> UserLessonProgressV2:
    """Obtiene o crea el registro de progreso de lección."""
    progress = session.exec(
        select(UserLessonProgressV2).where(
            UserLessonProgressV2.user_id == user_id,
            UserLessonProgressV2.lesson_id == lesson_id
        )
    ).first()
    
    if not progress:
        progress = UserLessonProgressV2(
            user_id=user_id,
            lesson_id=lesson_id
        )
        session.add(progress)
        session.commit()
        session.refresh(progress)
    
    return progress
