#!/usr/bin/env python3
"""
Script de Migración - Etapa 2: Arquitectura de Datos
Aplica los cambios de esquema necesarios para el sistema Lección-Céntrico.
"""

import sys
import os
import sqlite3

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.connection import engine
from sqlmodel import SQLModel
from database import (
    SentenceAnalysis, 
    LessonRequirement,
    # Import all models to ensure tables are created
    Word, Author, ReviewLog, UserProfile, Text, TextWordLink,
    WordFrequency, SyntaxPattern, InflectedForm, Challenge,
    UserChallengeProgress, Lesson, LessonProgress, LessonVocabulary,
    UserVocabularyProgress, ExerciseAttempt, ReadingProgress,
    SyntaxAnalysisProgress, UserProgressSummary, UnlockCondition,
    Recommendation, SyntaxCategory, SentenceCategoryLink,
    TokenAnnotation, SentenceStructure
)

def migrate_schema():
    print("🔧 Iniciando migración de esquema - Etapa 2...")
    
    # Get database path from engine
    db_path = str(engine.url).replace('sqlite:///', '')
    
    print(f"📂 Base de datos: {db_path}")
    
    # Connect to SQLite directly for schema inspection
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Check if usage_type column exists in sentenceanalysis
    cursor.execute("PRAGMA table_info(sentenceanalysis)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if 'usage_type' not in columns:
        print("➕ Añadiendo columna 'usage_type' a 'sentenceanalysis'...")
        cursor.execute("""
            ALTER TABLE sentenceanalysis 
            ADD COLUMN usage_type VARCHAR DEFAULT 'analysis'
        """)
        conn.commit()
        print("   ✅ Columna 'usage_type' añadida")
    else:
        print("   ℹ️  Columna 'usage_type' ya existe")
    
    conn.close()
    
    # 2. Create new tables using SQLModel (will create lesson_requirement if it doesn't exist)
    print("🏗️  Creando tablas nuevas (si no existen)...")
    SQLModel.metadata.create_all(engine)
    print("   ✅ Tablas verificadas/creadas")
    
    print("\n✅ Migración de esquema completada exitosamente!")
    print("\nCambios aplicados:")
    print("  - SentenceAnalysis.usage_type (nuevo campo)")
    print("  - LessonRequirement (nueva tabla)")

if __name__ == "__main__":
    migrate_schema()
