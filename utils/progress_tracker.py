"""
Servicio de Seguimiento de Progreso (Progress Tracker)
Registra y actualiza el progreso del usuario en todas las áreas.
"""

from typing import Optional, Dict, List
from sqlmodel import Session, select
from datetime import datetime
import json

from database import (
    LessonProgress, UserVocabularyProgress, ExerciseAttempt,
    ReadingProgress, SyntaxAnalysisProgress, UserProgressSummary,
    get_json_list, set_json_list
)
from utils.unlock_service import get_user_summary, auto_unlock_check


def update_lesson_progress(session: Session, user_id: int, lesson_number: int, 
                           status: str, time_spent: Optional[int] = None):
    """
    Actualiza el progreso de una lección.
    
    Args:
        session: Sesión de BD
        user_id: ID del usuario
        lesson_number: Número de lección (1-40)
        status: "unlocked", "in_progress", "completed"
        time_spent: Segundos adicionales gastados en la lección (opcional)
    """
    # Obtener o crear progreso
    statement = select(LessonProgress).where(
        LessonProgress.user_id == user_id,
        LessonProgress.lesson_number == lesson_number
    )
    progress = session.exec(statement).first()
    
    if not progress:
        progress = LessonProgress(
            user_id=user_id,
            lesson_number=lesson_number,
            status=status,
            unlocked_at=datetime.utcnow() if status != "locked" else None
        )
        session.add(progress)
    
    # Actualizar estado y timestamps
    old_status = progress.status
    progress.status = status
    progress.last_accessed_at = datetime.utcnow()
    
    if old_status == "unlocked" and status == "in_progress":
        progress.started_at = datetime.utcnow()
    
    if status == "completed" and old_status != "completed":
        progress.completed_at = datetime.utcnow()
    
    if time_spent:
        progress.total_time_spent += time_spent
    
    session.commit()
    
    # Actualizar resumen global
    update_user_summary(session, user_id)
    
    # Verificar desbloqueos automáticos
    auto_unlock_check(session, user_id)


def record_exercise_attempt(session: Session, user_id: int, lesson_number: int,
                            exercise_type: str, exercise_config: Dict,
                            user_answer: str, correct_answer: str,
                            is_correct: bool, time_spent_seconds: int,
                            hint_used: bool = False):
    """
    Registra un intento de ejercicio.
    
    Args:
        session: Sesión de BD
        user_id: ID del usuario
        lesson_number: Número de lección
        exercise_type: Tipo de ejercicio ("declension", "conjugation", etc.)
        exercise_config: Configuración del ejercicio (dict convertido a JSON)
        user_answer: Respuesta del usuario
        correct_answer: Respuesta correcta
        is_correct: Si la respuesta fue correcta
        time_spent_seconds: Tiempo en segundos
        hint_used: Si usó ayuda
    """
    attempt = ExerciseAttempt(
        user_id=user_id,
        lesson_number=lesson_number,
        exercise_type=exercise_type,
        exercise_config=json.dumps(exercise_config),
        user_answer=user_answer,
        correct_answer=correct_answer,
        is_correct=is_correct,
        time_spent_seconds=time_spent_seconds,
        hint_used=hint_used,
        attempted_at=datetime.utcnow()
    )
    
    session.add(attempt)
    session.commit()
    
    # Actualizar resumen global
    update_user_summary(session, user_id)
    
    # Verificar desbloqueos
    auto_unlock_check(session, user_id)


def record_vocabulary_practice(session: Session, user_id: int, word_id: int,
                               was_correct: bool):
    """
    Registra una práctica de vocabulario (flashcard).
    
    Args:
        session: Sesión de BD
        user_id: ID del usuario
        word_id: ID de la palabra practicada
        was_correct: Si la respuesta fue correcta
    """
    # Obtener o crear progreso
    statement = select(UserVocabularyProgress).where(
        UserVocabularyProgress.user_id == user_id,
        UserVocabularyProgress.word_id == word_id
    )
    progress = session.exec(statement).first()
    
    if not progress:
        progress = UserVocabularyProgress(
            user_id=user_id,
            word_id=word_id,
            first_seen=datetime.utcnow()
        )
        session.add(progress)
    
    # Actualizar estadísticas
    progress.times_seen += 1
    if was_correct:
        progress.times_correct += 1
    else:
        progress.times_incorrect += 1
    
    # Recalcular mastery level
    total_attempts = progress.times_correct + progress.times_incorrect
    if total_attempts > 0:
        progress.mastery_level = progress.times_correct / total_attempts
    
    # Actualizar timestamp
    progress.last_reviewed = datetime.utcnow()
    
    # Actualizar estado
    if progress.mastery_level >= 0.95:
        progress.is_learning = False
    
    session.commit()
    
    # Actualizar resumen global
    update_user_summary(session, user_id)


def record_reading_progress(session: Session, user_id: int, text_id: int,
                            status: str, words_looked_up: Optional[int] = None,
                            comprehension_questions_total: Optional[int] = None,
                            comprehension_questions_correct: Optional[int] = None,
                            time_spent_reading: Optional[int] = None,
                            difficulty_rating: Optional[int] = None):
    """
    Registra el progreso en una lectura.
    
    Args:
        session: Sesión de BD
        user_id: ID del usuario
        text_id: ID del texto
        status: "not_started", "in_progress", "completed"
        words_looked_up: Cuántas palabras buscó
        comprehension_questions_total: Total de preguntas de comprensión
        comprehension_questions_correct: Preguntas correctas
        time_spent_reading: Tiempo en segundos
        difficulty_rating: Calificación de dificultad (1-5)
    """
    # Obtener o crear progreso
    statement = select(ReadingProgress).where(
        ReadingProgress.user_id == user_id,
        ReadingProgress.text_id == text_id
    )
    progress = session.exec(statement).first()
    
    if not progress:
        progress = ReadingProgress(
            user_id=user_id,
            text_id=text_id,
            status=status
        )
        session.add(progress)
    
    # Actualizar estado y timestamps
    old_status = progress.status
    progress.status = status
    progress.last_accessed_at = datetime.utcnow()
    
    if old_status == "not_started" and status == "in_progress":
        progress.started_at = datetime.utcnow()
    
    if status == "completed" and old_status != "completed":
        progress.completed_at = datetime.utcnow()
    
    # Actualizar métricas opcionales
    if words_looked_up is not None:
        progress.words_looked_up = words_looked_up
    
    if comprehension_questions_total is not None:
        progress.comprehension_questions_total = comprehension_questions_total
    
    if comprehension_questions_correct is not None:
        progress.comprehension_questions_correct = comprehension_questions_correct
        if comprehension_questions_total and comprehension_questions_total > 0:
            progress.comprehension_score = comprehension_questions_correct / comprehension_questions_total
    
    if time_spent_reading is not None:
        progress.time_spent_reading += time_spent_reading
    
    if difficulty_rating is not None:
        progress.difficulty_rating = difficulty_rating
    
    session.commit()
    
    # Actualizar resumen global
    update_user_summary(session, user_id)
    
    # Verificar desbloqueos
    auto_unlock_check(session, user_id)


def record_syntax_analysis(session: Session, user_id: int, sentence_analysis_id: int,
                           lesson_number: Optional[int] = None,
                           viewed: bool = True, analyzed: bool = False,
                           cases_identified_correct: int = 0,
                           cases_identified_incorrect: int = 0,
                           functions_identified_correct: int = 0,
                           functions_identified_incorrect: int = 0,
                           time_spent_analyzing: int = 0):
    """
    Registra el análisis de una oración.
    
    Args:
        session: Sesión de BD
        user_id: ID del usuario
        sentence_analysis_id: ID del análisis de oración
        lesson_number: Número de lección (opcional)
        viewed: Si solo vio el análisis
        analyzed: Si intentó analizar activamente
        cases_identified_correct: Casos identificados correctamente
        cases_identified_incorrect: Casos identificados incorrectamente
        functions_identified_correct: Funciones identificadas correctamente
        functions_identified_incorrect: Funciones identificadas incorrectamente
        time_spent_analyzing: Tiempo en segundos
    """
    # Obtener o crear progreso
    statement = select(SyntaxAnalysisProgress).where(
        SyntaxAnalysisProgress.user_id == user_id,
        SyntaxAnalysisProgress.sentence_analysis_id == sentence_analysis_id
    )
    progress = session.exec(statement).first()
    
    if not progress:
        progress = SyntaxAnalysisProgress(
            user_id=user_id,
            sentence_analysis_id=sentence_analysis_id,
            lesson_number=lesson_number,
            first_viewed_at=datetime.utcnow() if viewed else None
        )
        session.add(progress)
    
    # Actualizar datos
    if viewed and not progress.viewed:
        progress.viewed = True
        if not progress.first_viewed_at:
            progress.first_viewed_at = datetime.utcnow()
    
    if analyzed:
        progress.analyzed = True
        progress.analyzed_at = datetime.utcnow()
        progress.cases_identified_correct += cases_identified_correct
        progress.cases_identified_incorrect += cases_identified_incorrect
        progress.functions_identified_correct += functions_identified_correct
        progress.functions_identified_incorrect += functions_identified_incorrect
        progress.time_spent_analyzing += time_spent_analyzing
    
    session.commit()
    
    # Actualizar resumen global
    update_user_summary(session, user_id)


def update_user_summary(session: Session, user_id: int):
    """
    Actualiza el resumen global de progreso del usuario.
    Esta función recalcula todas las métricas agregadas.
    """
    summary = get_user_summary(session, user_id)
    
    # Actualizar lecciones
    statement = select(LessonProgress).where(LessonProgress.user_id == user_id)
    all_lessons = session.exec(statement).all()
    
    completed_lessons = [l.lesson_number for l in all_lessons if l.status == "completed"]
    in_progress_lessons = [l.lesson_number for l in all_lessons if l.status == "in_progress"]
    
    summary.lessons_completed = set_json_list(sorted(completed_lessons))
    summary.lessons_in_progress = set_json_list(sorted(in_progress_lessons))
    
    # Actualizar current_lesson (la más alta completada + 1, o la más alta en progreso)
    if completed_lessons:
        summary.current_lesson = max(completed_lessons) + 1
    elif in_progress_lessons:
        summary.current_lesson = max(in_progress_lessons)
    else:
        summary.current_lesson = 1
    
    # Actualizar vocabulario
    statement = select(UserVocabularyProgress).where(UserVocabularyProgress.user_id == user_id)
    vocab_progress = session.exec(statement).all()
    
    if vocab_progress:
        learned = [v for v in vocab_progress if v.mastery_level >= 0.5]
        mastered = [v for v in vocab_progress if v.mastery_level >= 0.8]
        
        summary.total_words_learned = len(learned)
        summary.total_words_mastered = len(mastered)
        summary.vocab_mastery_avg = sum(v.mastery_level for v in vocab_progress) / len(vocab_progress)
    
    # Actualizar ejercicios
    statement = select(ExerciseAttempt).where(ExerciseAttempt.user_id == user_id)
    exercises = session.exec(statement).all()
    
    if exercises:
        summary.exercises_completed_total = len(exercises)
        correct = sum(1 for e in exercises if e.is_correct)
        summary.exercises_accuracy_avg = correct / len(exercises)
    
    # Actualizar lecturas
    statement = select(ReadingProgress).where(
        ReadingProgress.user_id == user_id,
        ReadingProgress.status == "completed"
    )
    readings = session.exec(statement).all()
    
    if readings:
        summary.texts_read_total = len(readings)
        scores = [r.comprehension_score for r in readings if r.comprehension_score > 0]
        if scores:
            summary.comprehension_avg = sum(scores) / len(scores)
    
    # Actualizar sintaxis
    statement = select(SyntaxAnalysisProgress).where(
        SyntaxAnalysisProgress.user_id == user_id,
        SyntaxAnalysisProgress.analyzed == True
    )
    syntax_analyses = session.exec(statement).all()
    summary.sentences_analyzed_total = len(syntax_analyses)
    
    # Actualizar timestamps
    summary.last_updated = datetime.utcnow()
    summary.last_activity = datetime.utcnow()
    
    session.commit()
