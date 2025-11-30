"""
Servicio de Desbloqueo (Unlock Service)
Este módulo implementa la lógica de desbloqueo de contenido basado en condiciones.

Funciones principales:
- check_unlock_conditions: Verifica si un usuario cumple condiciones para desbloquear algo
- unlock_lesson: Desbloquea una lección específica
- unlock_vocabulary: Desbloquea vocabulario de una lección
- auto_unlock_check: Verifica y desbloquea automáticamente todo lo que el usuario pueda acceder
"""

from typing import Optional, Dict, List
from sqlmodel import Session, select
from datetime import datetime
import json

from database import (
    LessonProgress,
    UserVocabularyProgress,
    ExerciseAttempt,
    ReadingProgress,
    SyntaxAnalysisProgress,
    UserProgressSummary,
    UnlockCondition,
    get_json_list
)


def get_user_summary(session: Session, user_id: int = 1) -> UserProgressSummary:
    """Obtiene o crea el resumen de progreso del usuario"""
    statement = select(UserProgressSummary).where(UserProgressSummary.user_id == user_id)
    summary = session.exec(statement).first()
    
    if not summary:
        summary = UserProgressSummary(user_id=user_id, current_lesson=1)
        session.add(summary)
        session.commit()
        session.refresh(summary)
    
    return summary


def get_lesson_progress(session: Session, user_id: int, lesson_number: int) -> Optional[LessonProgress]:
    """Obtiene el progreso de una lección específica"""
    statement = select(LessonProgress).where(
        LessonProgress.user_id == user_id,
        LessonProgress.lesson_number == lesson_number
    )
    return session.exec(statement).first()


def get_vocab_mastery(session: Session, user_id: int, lesson_number: int) -> float:
    """
    Calcula el nivel promedio de dominio de vocabulario de una lección.
    Retorna: 0.0-1.0
    """
    from database import LessonVocabulary
    
    # Obtener palabras esenciales de la lección
    statement = select(LessonVocabulary).where(
        LessonVocabulary.lesson_number == lesson_number,
        LessonVocabulary.is_essential == True
    )
    lesson_words = session.exec(statement).all()
    
    if not lesson_words:
        return 0.0
    
    # Obtener progreso del usuario en esas palabras
    total_mastery = 0.0
    word_count = 0
    
    for lesson_word in lesson_words:
        statement = select(UserVocabularyProgress).where(
            UserVocabularyProgress.user_id == user_id,
            UserVocabularyProgress.word_id == lesson_word.word_id
        )
        progress = session.exec(statement).first()
        
        if progress:
            total_mastery += progress.mastery_level
            word_count += 1
        # Si no tiene progreso, esa palabra cuenta como 0.0
    
    if word_count == 0:
        return 0.0
    
    return total_mastery / len(lesson_words)  # Promedio sobre TODAS las palabras esenciales


def get_exercises_stats(session: Session, user_id: int, lesson_number: int) -> Dict:
    """
    Obtiene estadísticas de ejercicios de una lección.
    Retorna: {'count': int, 'accuracy': float}
    """
    statement = select(ExerciseAttempt).where(
        ExerciseAttempt.user_id == user_id,
        ExerciseAttempt.lesson_number == lesson_number
    )
    attempts = session.exec(statement).all()
    
    if not attempts:
        return {'count': 0, 'accuracy': 0.0}
    
    correct = sum(1 for a in attempts if a.is_correct)
    total = len(attempts)
    
    return {
        'count': total,
        'accuracy': correct / total if total > 0 else 0.0
    }


def is_reading_completed(session: Session, user_id: int, text_id: int) -> bool:
    """Verifica si un usuario completó una lectura específica"""
    statement = select(ReadingProgress).where(
        ReadingProgress.user_id == user_id,
        ReadingProgress.text_id == text_id,
        ReadingProgress.status == "completed"
    )
    return session.exec(statement).first() is not None


def get_sentences_analyzed_count(session: Session, user_id: int, lesson_number: Optional[int] = None) -> int:
    """Cuenta oraciones analizadas, opcionalmente filtradas por lección"""
    statement = select(SyntaxAnalysisProgress).where(
        SyntaxAnalysisProgress.user_id == user_id,
        SyntaxAnalysisProgress.analyzed == True
    )
    
    if lesson_number is not None:
        statement = statement.where(SyntaxAnalysisProgress.lesson_number == lesson_number)
    
    analyses = session.exec(statement).all()
    return len(analyses)


def evaluate_condition(session: Session, user_id: int, condition: Dict) -> bool:
    """
    Evalúa una sola condición.
    
    Tipos de condiciones soportadas:
    - lesson_completed: {"type": "lesson_completed", "lesson_number": 3}
    - vocab_mastery: {"type": "vocab_mastery", "lesson_number": 3, "threshold": 0.8}
    - exercises_completed: {"type": "exercises_completed", "lesson_number": 3, "count": 5}
    - exercises_accuracy: {"type": "exercises_accuracy", "lesson_number": 3, "threshold": 0.7}
    - reading_completed: {"type": "reading_completed", "text_id": 1}
    - sentences_analyzed: {"type": "sentences_analyzed", "lesson_number": 3, "count": 3}
    - challenge_passed: {"type": "challenge_passed", "challenge_id": 3}
    """
    cond_type = condition.get('type')
    
    if cond_type == 'lesson_completed':
        lesson_num = condition['lesson_number']
        lesson_prog = get_lesson_progress(session, user_id, lesson_num)
        return lesson_prog is not None and lesson_prog.status == 'completed'
    
    elif cond_type == 'vocab_mastery':
        lesson_num = condition['lesson_number']
        threshold = condition['threshold']
        mastery = get_vocab_mastery(session, user_id, lesson_num)
        return mastery >= threshold
    
    elif cond_type == 'exercises_completed':
        lesson_num = condition['lesson_number']
        required_count = condition['count']
        stats = get_exercises_stats(session, user_id, lesson_num)
        return stats['count'] >= required_count
    
    elif cond_type == 'exercises_accuracy':
        lesson_num = condition['lesson_number']
        threshold = condition['threshold']
        stats = get_exercises_stats(session, user_id, lesson_num)
        return stats['count'] > 0 and stats['accuracy'] >= threshold
    
    elif cond_type == 'reading_completed':
        text_id = condition['text_id']
        return is_reading_completed(session, user_id, text_id)
    
    elif cond_type == 'sentences_analyzed':
        lesson_num = condition.get('lesson_number')
        required_count = condition['count']
        analyzed = get_sentences_analyzed_count(session, user_id, lesson_num)
        return analyzed >= required_count
    
    elif cond_type == 'challenge_passed':
        challenge_id = condition['challenge_id']
        summary = get_user_summary(session, user_id)
        passed_challenges = get_json_list(summary.challenges_passed)
        return challenge_id in passed_challenges
    
    else:
        # Tipo de condición desconocido
        return False


def check_unlock_conditions(session: Session, user_id: int, target: str) -> bool:
    """
    Verifica si un usuario cumple las condiciones para desbloquear un recurso.
    
    Args:
        session: Sesión de BD
        user_id: ID del usuario
        target: ID del recurso a desbloquear (ej: 'lesson_4', 'vocab_l3', 'reading_julia')
    
    Returns:
        True si cumple las condiciones, False en caso contrario
    """
    # Buscar condiciones de desbloqueo para este target
    statement = select(UnlockCondition).where(UnlockCondition.unlocks_id == target)
    unlock_rule = session.exec(statement).first()
    
    if not unlock_rule:
        # Si no hay reglas explícitas, está desbloqueado por defecto
        return True
    
    # Parsear condiciones JSON
    try:
        conditions = json.loads(unlock_rule.conditions_json)
    except:
        return False
    
    # Evaluar cada condición
    results = [evaluate_condition(session, user_id, cond) for cond in conditions]
    
    # Aplicar lógica AND/OR
    if unlock_rule.require_all:
        return all(results)  # Todas deben cumplirse
    else:
        return any(results)  # Al menos una debe cumplirse


def unlock_lesson(session: Session, user_id: int, lesson_number: int) -> bool:
    """
    Desbloquea una lección para un usuario.
    Retorna True si se desbloqueó exitosamente, False si ya estaba desbloqueada.
    """
    # Verificar si ya existe progreso
    lesson_prog = get_lesson_progress(session, user_id, lesson_number)
    
    if lesson_prog:
        if lesson_prog.status == 'locked':
            lesson_prog.status = 'unlocked'
            lesson_prog.unlocked_at = datetime.utcnow()
            session.commit()
            return True
        else:
            return False  # Ya estaba desbloqueada
    else:
        # Crear nuevo progreso
        new_progress = LessonProgress(
            user_id=user_id,
            lesson_number=lesson_number,
            status='unlocked',
            unlocked_at=datetime.utcnow()
        )
        session.add(new_progress)
        session.commit()
        return True


def unlock_vocabulary_for_lesson(session: Session, user_id: int, lesson_number: int) -> int:
    """
    Desbloquea el vocabulario de una lección.
    Esto significa marcar en el sistema que el usuario puede ver este vocabulario.
    
    Retorna: número de palabras nuevas desbloqueadas
    """
    from database import LessonVocabulary
    
    # Obtener todas las palabras de la lección
    statement = select(LessonVocabulary).where(
        LessonVocabulary.lesson_number == lesson_number
    )
    lesson_words = session.exec(statement).all()
    
    new_unlocks = 0
    
    for lesson_word in lesson_words:
        # Verificar si ya tiene progreso
        statement = select(UserVocabularyProgress).where(
            UserVocabularyProgress.user_id == user_id,
            UserVocabularyProgress.word_id == lesson_word.word_id
        )
        existing = session.exec(statement).first()
        
        if not existing:
            # Crear entrada de progreso (con mastery 0.0)
            new_progress = UserVocabularyProgress(
                user_id=user_id,
                word_id=lesson_word.word_id,
                mastery_level=0.0,
                times_seen=0
            )
            session.add(new_progress)
            new_unlocks += 1
    
    if new_unlocks > 0:
        session.commit()
    
    return new_unlocks


def auto_unlock_check(session: Session, user_id: int) -> Dict[str, List[str]]:
    """
    Verifica todas las posibles condiciones de desbloqueo y desbloquea automáticamente
    lo que el usuario ya puede acceder.
    
    Retorna un diccionario con los recursos desbloqueados:
    {
        'lessons': [4, 5],
        'vocabulary': ['vocab_l4'],
        'readings': ['reading_caesar_1'],
        'challenges': ['challenge_l3']
    }
    """
    unlocked = {
        'lessons': [],
        'vocabulary': [],
        'readings': [],
        'challenges': []
    }
    
    summary = get_user_summary(session, user_id)
    current = summary.current_lesson
    
    # Verificar lecciones (hasta 3 lecciones adelante)
    for lesson_num in range(1, min(current + 4, 41)):
        target = f'lesson_{lesson_num}'
        if check_unlock_conditions(session, user_id, target):
            if unlock_lesson(session, user_id, lesson_num):
                unlocked['lessons'].append(lesson_num)
    
    # Verificar vocabulario de lecciones desbloqueadas
    for lesson_num in range(1, current + 2):
        target = f'vocab_l{lesson_num}'
        if check_unlock_conditions(session, user_id, target):
            count = unlock_vocabulary_for_lesson(session, user_id, lesson_num)
            if count > 0:
                unlocked['vocabulary'].append(target)
    
    # TODO: Agregar lógica para readings y challenges cuando estén implementados
    
    return unlocked


def mark_lesson_completed(session: Session, user_id: int, lesson_number: int):
    """
    Marca una lección como completada.
    Esto dispara auto-unlock de contenido relacionado.
    """
    lesson_prog = get_lesson_progress(session, user_id, lesson_number)
    
    if not lesson_prog:
        # Crear progreso si no existe
        lesson_prog = LessonProgress(
            user_id=user_id,
            lesson_number=lesson_number,
            status='completed',
            unlocked_at=datetime.utcnow(),
            started_at=datetime.utcnow(),
            completed_at=datetime.utcnow()
        )
        session.add(lesson_prog)
    else:
        lesson_prog.status = 'completed'
        lesson_prog.completed_at = datetime.utcnow()
        if not lesson_prog.started_at:
            lesson_prog.started_at = datetime.utcnow()
    
    # Actualizar summary
    summary = get_user_summary(session, user_id)
    completed = get_json_list(summary.lessons_completed)
    if lesson_number not in completed:
        completed.append(lesson_number)
        summary.lessons_completed = json.dumps(completed)
    
    # Actualizar current_lesson si es mayor
    if lesson_number >= summary.current_lesson:
        summary.current_lesson = lesson_number + 1
    
    session.commit()
    
    # Disparar auto-unlock
    auto_unlock_check(session, user_id)


def get_recent_unlocks(session: Session, user_id: int = 1, hours: int = 24) -> List[Dict]:
    """
    Obtiene los desbloqueos recientes del usuario.
    
    Args:
        session: Sesión de BD
        user_id: ID del usuario
        hours: Horas hacia atrás para buscar (default: 24)
    
    Returns:
        Lista de dicts con formato:
        {'type': 'vocabulary'|'exercises'|'reading'|'lesson',
         'item_name': str,
         'unlocked_at': datetime,
         'icon': str}
    """
    from datetime import datetime, timedelta
    
    since = datetime.utcnow() - timedelta(hours=hours)
    unlocks = []
    
    # Vocabulario recién desbloqueado
    from database import LessonVocabulary

    results = session.exec(
        select(UserVocabularyProgress, LessonVocabulary.lesson_number)
        .join(LessonVocabulary, UserVocabularyProgress.word_id == LessonVocabulary.word_id)
        .where(UserVocabularyProgress.user_id == user_id)
        .where(UserVocabularyProgress.first_seen >= since)
    ).all()
    
    if results:
        # Agrupar por lección
        lessons_with_new_vocab = set(l_num for _, l_num in results)
        for lesson in lessons_with_new_vocab:
            # Filtrar resultados para esta lección
            lesson_results = [r for r in results if r[1] == lesson]
            count = len(lesson_results)
            
            # Encontrar fecha más antigua
            unlocked_at = min(prog.first_seen for prog, _ in lesson_results)
            
            unlocks.append({
                'type': 'vocabulary',
                'item_name': f'Vocabulario de Lección {lesson}',
                'detail': f'{count} palabras nuevas',
                'unlocked_at': unlocked_at,
                'icon': '📖'
            })
    
    # Lecciones recién iniciadas/completadas
    recent_lessons = session.exec(
        select(LessonProgress)
        .where(LessonProgress.user_id == user_id)
        .where(LessonProgress.started_at >= since)
    ).all()
    
    for lesson in recent_lessons:
        if lesson.status == 'completed' and lesson.completed_at and lesson.completed_at >= since:
            unlocks.append({
                'type': 'lesson_completed',
                'item_name': f'Lección {lesson.lesson_number}',
                'detail': 'Completada',
                'unlocked_at': lesson.completed_at,
                'icon': '✅'
            })
        else:
            unlocks.append({
                'type': 'lesson_started',
                'item_name': f'Lección {lesson.lesson_number}',
                'detail': 'Iniciada',
                'unlocked_at': lesson.started_at,
                'icon': '📘'
            })
    
    # Ordenar por fecha (más reciente primero)
    unlocks.sort(key=lambda x: x['unlocked_at'], reverse=True)
    
    return unlocks

