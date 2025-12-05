"""
Recommendation Service
Genera recomendaciones de estudio basadas en el progreso del usuario.
"""
from sqlmodel import select
from database import get_session, Recommendation, UserProgressSummary, LessonProgress
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class RecommendationService:
    @staticmethod
    def generate_recommendations(user_id: int) -> list[Recommendation]:
        """
        Analiza el progreso del usuario y genera recomendaciones.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            list[Recommendation]: Lista de recomendaciones generadas
        """
        recommendations = []
        
        with get_session() as session:
            # Obtener resumen de progreso
            summary = session.exec(
                select(UserProgressSummary).where(UserProgressSummary.user_id == user_id)
            ).first()
            
            if not summary:
                # Usuario nuevo: recomendar empezar
                rec = Recommendation(
                    user_id=user_id,
                    rec_type="lesson",
                    action="start_lesson",
                    lesson_number=1,
                    message="¡Bienvenido! Comienza tu viaje con la Lección 1: El Imperio Romano.",
                    priority="high"
                )
                recommendations.append(rec)
                return RecommendationService._save_recommendations(session, recommendations)

            # 1. Verificar lección actual
            current_lesson_num = summary.current_lesson
            current_lesson = session.exec(
                select(LessonProgress)
                .where(LessonProgress.user_id == user_id)
                .where(LessonProgress.lesson_number == current_lesson_num)
            ).first()
            
            if current_lesson and current_lesson.status == "in_progress":
                rec = Recommendation(
                    user_id=user_id,
                    rec_type="lesson",
                    action="continue_lesson",
                    lesson_number=current_lesson_num,
                    message=f"Continúa donde lo dejaste en la Lección {current_lesson_num}.",
                    priority="high"
                )
                recommendations.append(rec)
            elif current_lesson and current_lesson.status == "unlocked":
                 rec = Recommendation(
                    user_id=user_id,
                    rec_type="lesson",
                    action="start_lesson",
                    lesson_number=current_lesson_num,
                    message=f"Es hora de comenzar la Lección {current_lesson_num}.",
                    priority="high"
                )
                 recommendations.append(rec)

            # 2. Verificar vocabulario (si el dominio es bajo)
            if summary.vocab_mastery_avg < 0.5:
                rec = Recommendation(
                    user_id=user_id,
                    rec_type="vocabulary",
                    action="practice_vocab",
                    message="Tu vocabulario necesita refuerzo. ¡Practica 5 minutos hoy!",
                    priority="medium"
                )
                recommendations.append(rec)
                
            # 3. Verificar áreas débiles (simulado por ahora)
            # En el futuro, esto vendría de un análisis real de errores
            
            return RecommendationService._save_recommendations(session, recommendations)

    @staticmethod
    def _save_recommendations(session, new_recs: list[Recommendation]) -> list[Recommendation]:
        """Guarda las recomendaciones en la BD, evitando duplicados recientes"""
        saved_recs = []
        for rec in new_recs:
            # Verificar si ya existe una recomendación similar pendiente
            existing = session.exec(
                select(Recommendation)
                .where(Recommendation.user_id == rec.user_id)
                .where(Recommendation.action == rec.action)
                .where(Recommendation.lesson_number == rec.lesson_number)
                .where(Recommendation.status == "pending")
            ).first()
            
            if not existing:
                session.add(rec)
                saved_recs.append(rec)
            else:
                saved_recs.append(existing)
        
        session.commit()
        return saved_recs

    @staticmethod
    def get_active_recommendations(user_id: int) -> list[Recommendation]:
        """Obtiene las recomendaciones pendientes para mostrar en el dashboard"""
        with get_session() as session:
            recs = session.exec(
                select(Recommendation)
                .where(Recommendation.user_id == user_id)
                .where(Recommendation.status == "pending")
                .order_by(Recommendation.generated_at.desc())
                .limit(3)
            ).all()
            return recs
