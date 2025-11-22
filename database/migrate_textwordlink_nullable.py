"""
Migración crítica: Recrear TextWordLink con word_id nullable
Necesario para soportar palabras no en vocabulario (análisis LatinCy)
"""

import sys
import os
import sqlite3

if not any('latin-python' in p for p in sys.path):
    sys.path.insert(0, os.getcwd())

def migrate():
    """Recrea TextWordLink con word_id nullable"""
    
    db_path = 'data/latin_learning.db'
    
    print(f"🔧 Migrando base de datos: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. Crear tabla temporal con el nuevo esquema
        print("  1. Creando tabla temporal...")
        cursor.execute("""
            CREATE TABLE textwordlink_new (
                id INTEGER PRIMARY KEY,
                text_id INTEGER NOT NULL,
                word_id INTEGER,  -- NULLABLE ahora
                sentence_number INTEGER DEFAULT 1,
                position_in_sentence INTEGER DEFAULT 1,
                form TEXT,
                morphology_json TEXT,
                syntax_role TEXT,
                notes TEXT,
                FOREIGN KEY (text_id) REFERENCES text (id),
                FOREIGN KEY (word_id) REFERENCES word (id)
            )
        """)
        
        # 2. Copiar datos existentes (si los hay)
        print("  2. Copiando datos existentes...")
        cursor.execute("""
            INSERT INTO textwordlink_new 
            SELECT id, text_id, word_id, sentence_number, position_in_sentence,
                   form, morphology_json, syntax_role, notes
            FROM textwordlink
        """)
        
        # 3. Eliminar tabla vieja
        print("  3. Eliminando tabla antigua...")
        cursor.execute("DROP TABLE textwordlink")
        
        # 4. Renombrar tabla nueva
        print("  4. Renombrando tabla nueva...")
        cursor.execute("ALTER TABLE textwordlink_new RENAME TO textwordlink")
        
        conn.commit()
        print("\n✅ Migración completada exitosamente!")
        print("   word_id ahora es nullable en TextWordLink")
        
    except Exception as e:
        print(f"\n❌ Error en migración: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
