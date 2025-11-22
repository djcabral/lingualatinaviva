"""
Migración: Crear tabla InflectedForm para análisis morfológico reverso
"""

import sys
import os

if not any('latin-python' in p for p in sys.path):
    sys.path.insert(0, os.getcwd())

from database.connection import engine
from database.models import SQLModel, InflectedForm

def create_inflected_form_table():
    """Crea la tabla InflectedForm en la base de datos"""
    print("🔄 Creando tabla InflectedForm...")
    
    # Crear tabla
    SQLModel.metadata.create_all(engine, tables=[InflectedForm.__table__])
    
    print("✅ Tabla InflectedForm creada exitosamente!")
    print("   La tabla está lista para ser poblada con formas inflectadas.")

if __name__ == "__main__":
    create_inflected_form_table()
