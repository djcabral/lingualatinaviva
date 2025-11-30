"""
Servicio de Recomendaciones (Recommendation Service)
Este módulo implementa el motor de recomendaciones que sugiere próximos pasos al usuario.

Funciones principales:
- generate_recommendations: Genera lista de recomendaciones personalizadas
- identify_weak_areas: Detecta áreas donde el usuario tiene dificultades
- suggest_next_action: Sugiere la próxima acción más apropiada
"""

from typing import List, Dict, Optional
from sqlmodel import Session
from datetime import datetime, timedelta
import json

from database import (
    Recommendation,
    UserProgressSummary,
    get_json_list,
    set_json_list
)
from utils.unlock_service import (
    get_user_summary,
    get_lesson_progress,
    get_vocab_mastery,
    get_exercises_stats,
    get_sentences_analyzed_count,
    check_unlock_conditions
)


def identify_weak_areas(session: Session, user_id: int) -> List[str]:
    """
    Analiza el progreso del usuario e identifica áreas débiles.
    
    Detecta:
    - Ejercicios con baja precisión por tipo
    - Vocabulario con bajo dominio
    - Casos gramaticales problemáticos
    
    Retorna: Lista de strings describiendo áreas débiles
    """
    from database import ExerciseAttempt, UserVocabularyProgress, LessonVocabulary
    from sqlmodel import select
    
    weak_areas = []
    summary = get_user_summary(session, user_id)
    current = summary.current_lesson
    
    # 1. Analizar ejercicios de las últimas 3 lecciones
    for lesson_num in range(max(1, current - 2), current + 1):
        stats = get_exercises_stats(session, user_id, lesson_num)
        
        if stats['count'] >= 5 and stats['accuracy'] < 0.7:
            weak_areas.append(f"Ejercicios de Lección {lesson_num}")
        
        # Analizar por tipo de ejercicio
        statement = select(ExerciseAttempt).where(
            ExerciseAttempt.user_id == user_id,
            ExerciseAttempt.lesson_number == lesson_num
        )
        attempts = session.exec(statement).all()
        
        # Agrupar por tipo
        by_type = {}
        for attempt in attempts:
            ex_type = attempt.exercise_type
            if ex_type not in by_type:
                by_type[ex_type] = {'correct': 0, 'total': 0}
            by_type[ex_type]['total'] += 1
            if attempt.is_correct:
                by_type[ex_type]['correct'] += 1
        
        # Identificar tipos problemáticos
        for ex_type, data in by_type.items():
            if data['total'] >= 3:
                accuracy = data['correct'] / data['total']
                if accuracy < 0.65:
                    type_name = {
                        'declension': 'Declinación',
                        'conjugation': 'Conjugación',
                        'translation': 'Traducción',
                        'construction': 'Construcción activa',
                        'identification': 'Identificación de casos'
                    }.get(ex_type, ex_type)
                    weak_areas.append(type_name)
    
    # 2. Analizar vocabulario con bajo dominio
    for lesson_num in range(max(1, current - 2), current + 1):
        mastery = get_vocab_mastery(session, user_id, lesson_num)
        if mastery > 0 and mastery < 0.6:  # Ha practicado pero le va mal
            weak_areas.append(f"Vocabulario de Lección {lesson_num}")
    
    # 3. Analizar palabras específicas difíciles
    statement = select(UserVocabularyProgress).where(
        UserVocabularyProgress.user_id == user_id,
        UserVocabularyProgress.times_seen >= 5  # Vistas al menos 5 veces
    )
    vocab_progress = session.exec(statement).all()
    
    difficult_words_count = sum(1 for vp in vocab_progress if vp.mastery_level < 0.5)
    if difficult_words_count >= 10:
        weak_areas.append("Retención de vocabulario general")
    
    # 4. TODO: Analizar errores en casos específicos (requiere más datos)
    # Por ahora, detectar patrón genérico
    
    # Actualizar summary
    summary = get_user_summary(session, user_id)
    summary.weak_areas = set_json_list(list(set(weak_areas)))  # Eliminar duplicados
    session.commit()
    
    return weak_areas


def generate_recommendations(session: Session, user_id: int) -> List[Dict]:
    """
    Genera recomendaciones personalizadas para el usuario.
    
    Retorna lista de diccionarios con estructura:
    {
        'type': 'vocabulary' | 'exercises' | 'reading' | 'review' | 'challenge',
        'action': 'practice_vocab' | 'start_exercises' | ...,
        'lesson': int (opcional),
        'topic': str (opcional),
        'message': str,
        'priority': 'high' | 'medium' | 'low'
    }
    """
    recommendations = []
    summary = get_user_summary(session, user_id)
    current = summary.current_lesson
    
    # 1. ¿Acabó de completar una lección? → Practicar vocabulario
    lesson_prog = get_lesson_progress(session, user_id, current - 1)
    if lesson_prog and lesson_prog.status == 'completed':
        # Verificar si ya practica el vocabulario
        vocab_mastery = get_vocab_mastery(session, user_id, current - 1)
        if vocab_mastery < 0.8:
            recommendations.append({
                'type': 'vocabulary',
                'action': 'practice_vocab',
                'lesson': current - 1,
                'message': f'¡Nuevo vocabulario disponible para Lección {current - 1}! Practícalo con flashcards.',
                'priority': 'high'
            })
    
    # 2. ¿Tiene vocabulario suficiente pero no ha hecho ejercicios?
    for lesson_num in [current - 1, current]:
        if lesson_num < 1:
            continue
        
        vocab_mastery = get_vocab_mastery(session, user_id, lesson_num)
        stats = get_exercises_stats(session, user_id, lesson_num)
        
        if 0.5 <= vocab_mastery < 0.9 and stats['count'] < 10:
            recommendations.append({
                'type': 'exercises',
                'action': 'start_exercises',
                'lesson': lesson_num,
                'message': f'Ya dominas el 50%+ del vocabulario de L{lesson_num}. ¡Comienza los ejercicios!',
                'priority': 'high'
            })
            break  # Solo una recomendación de ejercicios
    
    # 3. ¿Tiene áreas débiles? → Repasar
    weak_areas = identify_weak_areas(session, user_id)
    for weak_area in weak_areas[:2]:  # Máximo 2 recomendaciones de repaso
        # Intentar extraer número de lección si está en el nombre
        lesson_num = None
        if "Lección" in weak_area:
            try:
                lesson_num = int(weak_area.split("Lección")[1].strip().split()[0])
            except:
                pass
        
        recommendations.append({
            'type': 'review',
            'action': 'review_grammar',
            'lesson': lesson_num,
            'topic': weak_area,
            'message': f'Pareces tener dificultades con {weak_area}. Repasa el material.',
            'priority': 'medium'
        })
    
    # 4. ¿Está listo para el desafío?
    if check_unlock_conditions(session, user_id, f'challenge_l{current - 1}'):
        # Verificar que no haya pasado ya este desafío
        passed = get_json_list(summary.challenges_passed)
        if (current - 1) not in passed:
            recommendations.append({
                'type': 'challenge',
                'action': 'take_challenge',
                'lesson': current - 1,
                'message': f'¡Estás listo para el Desafío de Lección {current - 1}!',
                'priority': 'high'
            })
    
    # 5. ¿Lleva varios días sin practicar vocabulario? → Repaso espaciado
    from database import UserVocabularyProgress
    from sqlmodel import select
    
    statement = select(UserVocabularyProgress).where(
        UserVocabularyProgress.user_id == user_id,
        UserVocabularyProgress.next_review_date <= datetime.utcnow()
    )
    due_reviews = session.exec(statement).all()
    
    if len(due_reviews) >= 20:
        recommendations.append({
            'type': 'vocabulary',
            'action': 'review_vocab',
            'message': f'Tienes {len(due_reviews)} palabras pendientes de repaso. ¡No las olvides!',
            'priority': 'medium'
        })
    elif len(due_reviews) >= 10:
        recommendations.append({
            'type': 'vocabulary',
            'action': 'review_vocab',
            'message': f'Tienes {len(due_reviews)} palabras para repasar. Un repaso rápido refrescará tu memoria.',
            'priority': 'low'
        })
    
    # 6. ¿Ha analizado pocas oraciones? → Sugerir análisis sintáctico
    analyzed = get_sentences_analyzed_count(session, user_id)
    if analyzed < 10 and current >= 3:
        recommendations.append({
            'type': 'syntax',
            'action': 'analyze_sentences',
            'message': 'Practica análisis sintáctico para consolidar tu comprensión gramatical.',
            'priority': 'low'
        })
    
    # Ordenar por prioridad
    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    recommendations.sort(key=lambda r: priority_order[r['priority']])
    
    return recommendations[:5]  # Máximo 5 recomendaciones


def save_recommendations(session: Session, user_id: int, recommendations: List[Dict]):
    """
    Guarda las recomendaciones generadas en la base de datos.
    """
    for rec in recommendations:
        new_rec = Recommendation(
            user_id=user_id,
            rec_type=rec['type'],
            action=rec['action'],
            lesson_number=rec.get('lesson'),
            topic=rec.get('topic'),
            message=rec['message'],
            priority=rec['priority'],
            status='pending'
        )
        session.add(new_rec)
    
    session.commit()


def get_active_recommendations(session: Session, user_id: int, max_age_days: int = 7) -> List[Recommendation]:
    """
    Obtiene recomendaciones activas (pendientes o aceptadas) generadas recientemente.
    """
    from sqlmodel import select
    
    cutoff_date = datetime.utcnow() - timedelta(days=max_age_days)
    
    statement = select(Recommendation).where(
        Recommendation.user_id == user_id,
        Recommendation.status.in_(['pending', 'accepted']),
        Recommendation.generated_at >= cutoff_date
    ).order_by(Recommendation.generated_at.desc())  # Más recientes primero
    
    return list(session.exec(statement))


def mark_recommendation_completed(session: Session, recommendation_id: int):
    """Marca una recomendación como completada"""
    from sqlmodel import select
    
    statement = select(Recommendation).where(Recommendation.id == recommendation_id)
    rec = session.exec(statement).first()
    
    if rec:
        rec.status = 'completed'
        rec.acted_on_at = datetime.utcnow()
        session.commit()


def suggest_next_action(session: Session, user_id: int) -> Optional[Dict]:
    """
    Sugiere la MEJOR acción individual que el usuario debería hacer ahora.
    Retorna UN solo diccionario de recomendación o None.
    """
    recs = generate_recommendations(session, user_id)
    return recs[0] if recs else None


def get_vocab_due_for_review(session: Session, user_id: int) -> List[Dict]:
    """
    Obtiene palabras que necesitan repaso hoy basado en repetición espaciada.
    
    Args:
        session: Sesión de BD
        user_id: ID del usuario
    
    Returns:
        Lista de dict con estructura:
        {'word': Word object, 'mastery_level': float, 'days_overdue': int}
    """
    from database import UserVocabularyProgress
    from database import Word
    from sqlmodel import select
    
    # Obtener palabras con repaso pendiente
    statement = select(UserVocabularyProgress).where(
        UserVocabularyProgress.user_id == user_id,
        UserVocabularyProgress.next_review_date <= datetime.utcnow()
    ).order_by(UserVocabularyProgress.next_review_date)  # Más vencidas primero
    
    vocab_progress = session.exec(statement).all()
    
    # Enriquecer con datos de las palabras
    due_words = []
    for vp in vocab_progress:
        word = session.exec(select(Word).where(Word.id == vp.word_id)).first()
        if word:
            days_overdue = (datetime.utcnow() - vp.next_review_date).days if vp.next_review_date else 0
            due_words.append({
                'word': word,
                'mastery_level': vp.mastery_level,
                'days_overdue': max(0, days_overdue),
                'lesson_number': vp.lesson_number
            })
    
    return due_words
