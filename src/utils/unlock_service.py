"""
Unlock Service
Maneja la lógica de desbloqueo de lecciones y contenido.
"""
from sqlmodel import select
from database import get_session, LessonProgress, UserProgressSummary, LessonRequirement, UserLessonProgress
import logging

logger = logging.getLogger(__name__)

class UnlockService:
    @staticmethod
    def check_unlock_conditions(user_id: int, lesson_number: int) -> bool:
        """
        Verifica si una lección debe desbloquearse.
        
        Args:
            user_id: ID del usuario
            lesson_number: Número de la lección a verificar
            
        Returns:
            bool: True si la lección está desbloqueada o se acaba de desbloquear
        """
        # La lección 1 siempre está desbloqueada
        if lesson_number == 1:
            return True
            
        with get_session() as session:
            # Verificar estado actual
            progress = session.exec(
                select(LessonProgress)
                .where(LessonProgress.user_id == user_id)
                .where(LessonProgress.lesson_number == lesson_number)
            ).first()
            
            if progress and progress.status != "locked":
                return True
                
            # Verificar si la lección anterior está completada
            prev_lesson = lesson_number - 1
            prev_progress = session.exec(
                select(LessonProgress)
                .where(LessonProgress.user_id == user_id)
                .where(LessonProgress.lesson_number == prev_lesson)
            ).first()
            
            if not prev_progress or prev_progress.status != "completed":
                return False
                
            # Si llegamos aquí, la lección anterior está completada, así que desbloqueamos esta
            if not progress:
                progress = LessonProgress(
                    user_id=user_id,
                    lesson_number=lesson_number,
                    status="unlocked"
                )
                session.add(progress)
            else:
                progress.status = "unlocked"
                session.add(progress)
                
            session.commit()
            logger.info(f"Lección {lesson_number} desbloqueada para usuario {user_id}")
            return True

    @staticmethod
    def mark_lesson_completed(user_id: int, lesson_number: int) -> bool:
        """
        Marca una lección como completada si se cumplen los requisitos.
        """
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
                    status="in_progress"
                )
                session.add(progress)
            
            # Aquí iría la lógica real de verificación de requisitos
            # Por ahora, simplemente la marcamos como completada
            progress.status = "completed"
            session.add(progress)
            session.commit()
            
            # Intentar desbloquear la siguiente
            UnlockService.check_unlock_conditions(user_id, lesson_number + 1)
            
            return True
