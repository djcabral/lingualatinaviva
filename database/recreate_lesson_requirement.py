"""
Script para recrear la tabla lesson_requirement con el nuevo esquema
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.connection import engine
from sqlalchemy import text

def recreate_table():
    """Drop and recreate lesson_requirement table"""
    print("=" * 60)
    print("Recreando tabla lesson_requirement")
    print("=" * 60)
    
    with engine.begin() as conn:
        # Drop existing table
        print("\n🗑️  Eliminando tabla antigua...")
        conn.execute(text("DROP TABLE IF EXISTS lesson_requirement"))
        conn.execute(text("DROP TABLE IF EXISTS user_lesson_progress"))
        print("✅ Tablas eliminadas")
        
        # Create new tables
        print("\n📦 Creando tablas nuevas...")
        from database.integration_models import LessonRequirement, UserLessonProgress
        from database.connection import create_db_and_tables
        
        create_db_and_tables()
        print("✅ Tablas creadas con nuevo esquema")
    
    print("\n" + "=" * 60)
    print("✅ RECREACIÓN COMPLETADA")
    print("=" * 60)
    print("\n💡 Ahora ejecuta: .venv/bin/python database/migrate_lesson_requirements.py")

if __name__ == "__main__":
    recreate_table()
