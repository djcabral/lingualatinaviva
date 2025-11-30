import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlmodel import create_engine, SQLModel

# Importar TODOS los modelos (tanto existentes como nuevos)
# Para que SQLAlchemy pueda resolver las foreign keys
from database import (
    Word, Author, Text, UserProfile, Challenge, UserChallengeProgress,
    ReviewLog, TextWordLink, WordFrequency, SyntaxPattern, InflectedForm
)
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


def create_tables(database_path: str = 'data/lexicon.db'):
    """
    Crea todas las tablas de integración en la base de datos.
    """
    print(f"📊 Creando tablas de integración en: {database_path}")
    
    # Crear engine
    database_url = f"sqlite:///{database_path}"
    engine = create_engine(database_url, echo=True)
    
    # Crear todas las tablas definidas en integration_models
    print("\n🔨 Creando tablas...")
    SQLModel.metadata.create_all(engine)
    
    print("\n✅ ¡Tablas creadas exitosamente!")
    print("\nTablas creadas:")
    print("  - lesson_progress")
    print("  - lesson_vocabulary")
    print("  - user_vocabulary_progress")
    print("  - exercise_attempt")
    print("  - reading_progress")
    print("  - syntax_analysis_progress")
    print("  - user_progress_summary")
    print("  - unlock_condition")
    print("  - recommendation")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Crear tablas de integración')
    parser.add_argument('--db', default='data/lexicon.db',
                        help='Ruta a la base de datos SQLite')
    
    args = parser.parse_args()
    
    create_tables(args.db)
