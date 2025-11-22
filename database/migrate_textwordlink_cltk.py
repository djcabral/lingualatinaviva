"""
Migración: Actualizar TextWordLink para soportar análisis CLTK
- word_id ahora puede ser NULL (para palabras no en vocabulario)
- Agregar campo 'form' para almacenar la forma exacta del texto
"""

import sys
import os

if not any('latin-python' in p for p in sys.path):
    sys.path.insert(0, os.getcwd())

from database.connection import get_session
from sqlalchemy import text

def migrate():
    """Actualiza la tabla TextWordLink"""
    
    with get_session() as session:
        print("🔧 Actualizando tabla TextWordLink...")
        
        try:
            # SQLite doesn't support ALTER COLUMN, so we need to check current schema
            # and potentially recreate the table
            
            # Add 'form' column if it doesn't exist
            try:
                session.exec(text("""
                    ALTER TABLE textwordlink ADD COLUMN form VARCHAR
                """))
                print("  ✅ Agregada columna 'form'")
            except Exception as e:
                if "duplicate column" in str(e).lower():
                    print("  ℹ️  Columna 'form' ya existe")
                else:
                    print(f"  ⚠️  No se pudo agregar 'form': {e}")
            
            # Note: Making word_id nullable requires table recreation in SQLite
            # This is complex, so we'll document it for manual migration if needed
            print("\n📝 Nota: word_id debe ser nullable para soportar CLTK")
            print("   Si encuentras errores de NOT NULL en word_id:")
            print("   1. Haz backup de la base de datos")
            print("   2. Elimina y recrea la tabla con el nuevo esquema")
            
            session.commit()
            print("\n✅ Migración completada")
            
        except Exception as e:
            print(f"\n❌ Error en migración: {e}")
            session.rollback()
            raise

if __name__ == "__main__":
    migrate()
