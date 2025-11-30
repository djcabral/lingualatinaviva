"""
Script de Migración para Modelos de Integración
Crea las tablas necesarias para el sistema de integración orgánica.
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlmodel import SQLModel, create_engine
from database.connection import engine
from database.integration_models import (
    LessonProgress,
    LessonVocabulary,
    UserVocabularyProgress,
    ExerciseAttempt,
    ReadingProgress,
    SyntaxAnalysisProgress,
    UserProgressSummary,
    UnlockCondition,
    Recommendation
)

def migrate_integration_tables():
    """
    Crea todas las tablas de integration_models.py en la base de datos.
    """
    print("🔄 Iniciando migración de tablas de integración...")
    
    try:
        # Crear todas las tablas
        SQLModel.metadata.create_all(engine)
        
        print("✅ Tablas creadas exitosamente:")
        print("  - lesson_progress")
        print("  - lesson_vocabulary")
        print("  - user_vocabulary_progress")
        print("  - exercise_attempt")
        print("  - reading_progress")
        print("  - syntax_analysis_progress")
        print("  - user_progress_summary")
        print("  - unlock_condition")
        print("  - recommendation")
        
        # Inicializar UserProgressSummary para user_id=1 si no existe
        from database.connection import get_session
        from sqlmodel import select
        
        with get_session() as session:
            statement = select(UserProgressSummary).where(UserProgressSummary.user_id == 1)
            summary = session.exec(statement).first()
            
            if not summary:
                print("\n🔄 Inicializando UserProgressSummary para usuario 1...")
                summary = UserProgressSummary(user_id=1)
                session.add(summary)
                session.commit()
                print("✅ UserProgressSummary inicializado")
            else:
                print("\n✅ UserProgressSummary ya existe")
        
        print("\n✅ Migración completada exitosamente")
        return True
        
    except Exception as e:
        print(f"\n❌ Error durante la migración: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = migrate_integration_tables()
    sys.exit(0 if success else 1)
