"""
Script para crear un usuario de demostración con progreso realista.

Este script crea:
- Usuario en Lección 3 (completadas L1-L2)
- Vocabulario de L1-L2 dominado, L3 en progreso
- Ejercicios completados con diferentes niveles de precisión
- Una lectura completada
- Algunas oraciones analizadas
- Recomendaciones generadas

Uso:
    python scripts/create_demo_user.py [--reset]
"""

import sys
import os
from datetime import datetime, timedelta
from random import randint, choice

# Agregar path del proyecto
root_path = os.path.dirname(os.path.dirname(__file__))
if root_path not in sys.path:
    sys.path.append(root_path)

from database.connection import get_session
from database import UserProfile, Word
from database.integration_models import (
    LessonProgress,
    LessonVocabulary,
    UserVocabularyProgress,
    ExerciseAttempt,
    ReadingProgress,
    UserProgressSummary,
    set_json_list
)
from utils.unlock_service import mark_lesson_completed, unlock_vocabulary_for_lesson
from utils.recommendation_service import generate_recommendations, save_recommendations
from sqlmodel import select


def reset_demo_data(session):
    """Elimina todos los datos del usuario de demostración."""
    print("🗑️  Eliminando datos existentes del usuario demo...")
    
    # Eliminar en orden inverso de dependencias
    user = session.exec(select(UserProfile)).first()
    if not user:
        print("No se encontró usuario para eliminar.")
        return
    
    user_id = user.id
    
    # Eliminar todos los registros relacionados
    from database.integration_models import (
        Recommendation, SyntaxAnalysisProgress, ReadingProgress,
        ExerciseAttempt, UserVocabularyProgress, LessonProgress,
        UserProgressSummary
    )
    
    for model in [Recommendation, SyntaxAnalysisProgress, ReadingProgress, 
                  ExerciseAttempt, UserVocabularyProgress, LessonProgress,
                  UserProgressSummary]:
        deleted = 0
        try:
            records = session.exec(select(model).where(model.user_id == user_id)).all()
            for record in records:
                session.delete(record)
                deleted += 1
            if deleted > 0:
                print(f"  ✓ Eliminados {deleted} registros de {model.__tablename__}")
        except Exception as e:
            print(f"  ⚠️  Error eliminando {model.__tablename__}: {e}")
    
    session.commit()
    print("✅ Datos demo eliminados.\n")


def create_demo_user(session):
    """Crea o actualiza el usuario de demostración."""
    print("👤 Creando/actualizando usuario demo...")
    
    user = session.exec(select(UserProfile)).first()
    if not user:
        user = UserProfile(
            username="Marcus Discipulus",
            level=3,
            xp=450,
            streak=7
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        print(f"  ✓ Usuario creado: {user.username} (ID: {user.id})")
    else:
        user.username = "Marcus Discipulus"
        user.level = 3
        user.xp = 450
        user.streak = 7
        session.add(user)
        session.commit()
        print(f"  ✓ Usuario actualizado: {user.username} (ID: {user.id})")
    
    return user


def populate_lesson_progress(session, user_id):
    """Crea progreso de lecciones: L1-L2 completadas, L3 en progreso."""
    print("\n📚 Poblando progreso de lecciones...")
    
    # Lección 1: Completada hace 14 días
    lesson1 = LessonProgress(
        user_id=user_id,
        lesson_number=1,
        status="completed",
        started_at=datetime.utcnow() - timedelta(days=14),
        completed_at=datetime.utcnow() - timedelta(days=12),
        total_time_spent=3600,  # 1 hora
        comprehension_rating=5
    )
    session.add(lesson1)
    
    # Lección 2: Completada hace 7 días
    lesson2 = LessonProgress(
        user_id=user_id,
        lesson_number=2,
        status="completed",
        started_at=datetime.utcnow() - timedelta(days=10),
        completed_at=datetime.utcnow() - timedelta(days=7),
        total_time_spent=4200,  # 1.2 horas
        comprehension_rating=4
    )
    session.add(lesson2)
    
    # Lección 3: En progreso
    lesson3 = LessonProgress(
        user_id=user_id,
        lesson_number=3,
        status="in_progress",
        started_at=datetime.utcnow() - timedelta(days=5),
        last_accessed_at=datetime.utcnow() - timedelta(hours=2),
        total_time_spent=2400,  # 40 minutos
    )
    session.add(lesson3)
    
    session.commit()
    print("  ✓ Creadas 3 lecciones (2 completadas, 1 en progreso)")


def populate_vocabulary_progress(session, user_id):
    """Crea progreso de vocabulario para L1-L3."""
    print("\n📖 Poblando progreso de vocabulario...")
    
    # Obtener palabras de la base de datos
    words = session.exec(select(Word).limit(50)).all()
    
    if not words:
        print("  ⚠️  No se encontraron palabras en la BD. Saltando vocabulario.")
        return
    
    words_created = 0
    
    # L1: 15 palabras bien dominadas
    for i, word in enumerate(words[:15]):
        progress = UserVocabularyProgress(
            user_id=user_id,
            word_id=word.id,
            lesson_number=1,
            mastery_level=randint(70, 100) / 100.0,
            times_seen=randint(10, 20),
            times_correct=randint(8, 18),
            times_incorrect=randint(0, 3),
            interval_days=randint(5, 14),
            first_seen=datetime.utcnow() - timedelta(days=14),
            last_reviewed=datetime.utcnow() - timedelta(days=randint(1, 7)),
            next_review_date=datetime.utcnow() + timedelta(days=randint(1, 14)),
            is_learning=False,
            is_mature=True
        )
        session.add(progress)
        words_created += 1
    
    # L2: 12 palabras moderadamente dominadas
    for i, word in enumerate(words[15:27]):
        progress = UserVocabularyProgress(
            user_id=user_id,
            word_id=word.id,
            lesson_number=2,
            mastery_level=randint(50, 85) / 100.0,
            times_seen=randint(5, 12),
            times_correct=randint(4, 10),
            times_incorrect=randint(1, 4),
            interval_days=randint(2, 7),
            first_seen=datetime.utcnow() - timedelta(days=10),
            last_reviewed=datetime.utcnow() - timedelta(days=randint(1, 5)),
            next_review_date=datetime.utcnow() + timedelta(days=randint(0, 7)),
            is_learning=True,
            is_mature=False
        )
        session.add(progress)
        words_created += 1
    
    # L3: 10 palabras en fase inicial (algunas necesitan repaso HOY)
    for i, word in enumerate(words[27:37]):
        days_until_review = choice([-1, 0, 1, 2, 3])  # Algunas vencidas
        progress = UserVocabularyProgress(
            user_id=user_id,
            word_id=word.id,
            lesson_number=3,
            mastery_level=randint(20, 60) / 100.0,
            times_seen=randint(2, 6),
            times_correct=randint(1, 4),
            times_incorrect=randint(1, 3),
            interval_days=randint(1, 3),
            first_seen=datetime.utcnow() - timedelta(days=5),
            last_reviewed=datetime.utcnow() - timedelta(days=randint(1, 3)),
            next_review_date=datetime.utcnow() + timedelta(days=days_until_review),
            is_learning=True,
            is_mature=False
        )
        session.add(progress)
        words_created += 1
    
    session.commit()
    print(f"  ✓ Creadas {words_created} palabras de vocabulario (L1: 15, L2: 12, L3: 10)")


def populate_exercises(session, user_id):
    """Crea intentos de ejercicios con diferentes niveles de precisión."""
    print("\n✍️  Poblando ejercicios completados...")
    
    exercise_types = ['declension', 'conjugation', 'translation', 'multiple_choice']
    exercises_created = 0
    
    # L1: 12 ejercicios con alta precisión
    for i in range(12):
        is_correct = randint(1, 100) <= 85  # 85% precisión
        attempt = ExerciseAttempt(
            user_id=user_id,
            lesson_number=1,
            exercise_type=choice(exercise_types),
            exercise_config='{"difficulty": "easy"}',
            user_answer=f"respuesta_{i}",
            correct_answer=f"respuesta_{i}" if is_correct else f"otra_respuesta",
            is_correct=is_correct,
            time_spent_seconds=randint(30, 120),
            hint_used=False,
            attempted_at=datetime.utcnow() - timedelta(days=randint(8, 14))
        )
        session.add(attempt)
        exercises_created += 1
    
    # L2: 10 ejercicios con precisión media
    for i in range(10):
        is_correct = randint(1, 100) <= 70  # 70% precisión
        attempt = ExerciseAttempt(
            user_id=user_id,
            lesson_number=2,
            exercise_type=choice(exercise_types),
            exercise_config='{"difficulty": "medium"}',
            user_answer=f"respuesta_{i}",
            correct_answer=f"respuesta_{i}" if is_correct else f"otra_respuesta",
            is_correct=is_correct,
            time_spent_seconds=randint(45, 180),
            hint_used=randint(1, 100) <= 20,  # 20% usó pista
            attempted_at=datetime.utcnow() - timedelta(days=randint(3, 10))
        )
        session.add(attempt)
        exercises_created += 1
    
    # L3: 5 ejercicios con precisión variable (comenzando)
    for i in range(5):
        is_correct = randint(1, 100) <= 60  # 60% precisión
        attempt = ExerciseAttempt(
            user_id=user_id,
            lesson_number=3,
            exercise_type=choice(exercise_types),
            exercise_config='{"difficulty": "medium"}',
            user_answer=f"respuesta_{i}",
            correct_answer=f"respuesta_{i}" if is_correct else f"otra_respuesta",
            is_correct=is_correct,
            time_spent_seconds=randint(60, 240),
            hint_used=randint(1, 100) <= 30,  # 30% usó pista
            attempted_at=datetime.utcnow() - timedelta(days=randint(0, 5))
        )
        session.add(attempt)
        exercises_created += 1
    
    session.commit()
    print(f"  ✓ Creados {exercises_created} intentos de ejercicios (L1: 12, L2: 10, L3: 5)")


def populate_readings(session, user_id):
    """Crea progreso de lecturas."""
    print("\n📜 Poblando progreso de lecturas...")
    
    # Lectura 1: Completada
    reading1 = ReadingProgress(
        user_id=user_id,
        text_id=1,  # Asumimos que existe texto ID 1
        lesson_number=1,
        status="completed",
        words_read=45,
        words_looked_up=8,
        comprehension_score=0.85,
        time_spent_reading=900,  # 15 minutos
        started_at=datetime.utcnow() - timedelta(days=9),
        completed_at=datetime.utcnow() - timedelta(days=9),
        difficulty_rating=3
    )
    session.add(reading1)
    
    # Lectura 2: En progreso
    reading2 = ReadingProgress(
        user_id=user_id,
        text_id=2,
        lesson_number=2,
        status="in_progress",
        words_read=32,
        words_looked_up=12,
        time_spent_reading=450,  # 7.5 minutos
        started_at=datetime.utcnow() - timedelta(days=4),
        last_accessed_at=datetime.utcnow() - timedelta(days=1)
    )
    session.add(reading2)
    
    session.commit()
    print("  ✓ Creadas 2 lecturas (1 completada, 1 en progreso)")


def create_progress_summary(session, user_id):
    """Crea el resumen de progreso del usuario."""
    print("\n📊 Creando resumen de progreso...")
    
    summary = UserProgressSummary(
        user_id=user_id,
        current_lesson=3,
        lessons_completed=set_json_list([1, 2]),
        lessons_in_progress=set_json_list([3]),
        total_words_learned=27,  # L1 + L2
        total_words_mastered=15,  # Solo L1 bien dominada
        vocab_mastery_avg=0.68,
        exercises_completed_total=27,
        exercises_accuracy_avg=0.72,
        texts_read_total=1,
        comprehension_avg=0.85,
        sentences_analyzed_total=0,
        challenges_passed=set_json_list([]),
        challenges_failed_attempts=0,
        weak_areas=set_json_list(["Conjugación 3ra declinación", "Genitivo plural"]),
        total_xp=450,
        level=3,
        badges=set_json_list(["first_lesson", "vocab_master_10"]),
        last_updated=datetime.utcnow(),
        last_activity=datetime.utcnow() - timedelta(hours=2)
    )
    session.add(summary)
    session.commit()
    print("  ✓ Resumen de progreso creado")


def generate_demo_recommendations(session, user_id):
    """Genera recomendaciones para el usuario demo."""
    print("\n💡 Generando recomendaciones...")
    
    recommendations = generate_recommendations(session, user_id)
    
    if recommendations:
        save_recommendations(session, user_id, recommendations)
        print(f"  ✓ Generadas {len(recommendations)} recomendaciones")
        for rec in recommendations:
            print(f"    - [{rec['priority'].upper()}] {rec['message']}")
    else:
        print("  ⚠️  No se generaron recomendaciones")


def main():
    """Función principal."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Crear usuario de demostración")
    parser.add_argument('--reset', action='store_true', 
                       help='Eliminar datos existentes antes de crear')
    args = parser.parse_args()
    
    print("=" * 70)
    print("🎭 CREACIÓN DE USUARIO DE DEMOSTRACIÓN")
    print("=" * 70)
    
    with get_session() as session:
        if args.reset:
            reset_demo_data(session)
        
        user = create_demo_user(session)
        populate_lesson_progress(session, user.id)
        populate_vocabulary_progress(session, user.id)
        populate_exercises(session, user.id)
        populate_readings(session, user.id)
        create_progress_summary(session, user.id)
        generate_demo_recommendations(session, user.id)
    
    print("\n" + "=" * 70)
    print("✅ USUARIO DEMO CREADO EXITOSAMENTE")
    print("=" * 70)
    print(f"\n🎯 Próximos pasos:")
    print(f"   1. Ejecuta: streamlit run 00_🏠_Home.py")
    print(f"   2. Navega al Dashboard de Inicio")
    print(f"   3. Verifica que se muestre el progreso del usuario 'Marcus Discipulus'")
    print()


if __name__ == "__main__":
    main()
