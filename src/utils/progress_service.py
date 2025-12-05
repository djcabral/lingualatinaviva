"""
Progress Service
Maneja la actualización y seguimiento del progreso global del usuario.
"""
from sqlmodel import select
from database import get_session, UserProgressSummary, LessonProgress, UserVocabularyProgress, ExerciseAttempt
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class ProgressService:
    @staticmethod
    def update_user_progress_summary(user_id: int) -> UserProgressSummary:
        """
        Recalcula y actualiza el resumen de progreso del usuario.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            UserProgressSummary: El objeto actualizado
        """
        with get_session() as session:
            # 1. Obtener o crear el resumen
            summary = session.exec(
                select(UserProgressSummary).where(UserProgressSummary.user_id == user_id)
            ).first()
            
            if not summary:
                summary = UserProgressSummary(user_id=user_id)
                session.add(summary)
            
            # 2. Calcular lección actual (la más alta desbloqueada o en progreso)
            latest_lesson = session.exec(
                select(LessonProgress)
                .where(LessonProgress.user_id == user_id)
                .where(LessonProgress.status.in_(["unlocked", "in_progress"]))
                .order_by(LessonProgress.lesson_number.desc())
            ).first()
            
            if latest_lesson:
                summary.current_lesson = latest_lesson.lesson_number
            
            # 3. Calcular estadísticas de vocabulario
            vocab_stats = session.exec(
                select(UserVocabularyProgress)
                .where(UserVocabularyProgress.user_id == user_id)
            ).all()
            
            if vocab_stats:
                total_words = len(vocab_stats)
                mastered_words = sum(1 for w in vocab_stats if w.mastery_level >= 0.8)
                avg_mastery = sum(w.mastery_level for w in vocab_stats) / total_words
                
                summary.total_words_learned = total_words
                summary.total_words_mastered = mastered_words
                summary.vocab_mastery_avg = avg_mastery
            
            # 4. Calcular estadísticas de ejercicios
            exercises = session.exec(
                select(ExerciseAttempt)
                .where(ExerciseAttempt.user_id == user_id)
            ).all()
            
            if exercises:
                summary.exercises_completed_total = len(exercises)
                correct_exercises = sum(1 for e in exercises if e.is_correct)
                summary.exercises_accuracy_avg = correct_exercises / len(exercises)
            
            # 5. Actualizar timestamp
            summary.last_updated = datetime.utcnow()
            session.add(summary)
            session.commit()
            session.refresh(summary)
            
            return summary

    @staticmethod
    def track_lesson_view(user_id: int, lesson_number: int):
        """Registra que el usuario ha visto una lección"""
        with get_session() as session:
            progress = session.exec(
                select(LessonProgress)
                .where(LessonProgress.user_id == user_id)
                .where(LessonProgress.lesson_number == lesson_number)
            ).first()
            
            if not progress:
                progress = LessonProgress(
                    user_id=user_id,
                    lesson_number=lesson_number,
                    status="in_progress",
                    started_at=datetime.utcnow()
                )
                session.add(progress)
            
            progress.last_accessed_at = datetime.utcnow()
            session.add(progress)
            session.commit()
