"""
Script para forzar sincronización de metadata de SQLModel con la base de datos
Útil cuando el schema de DB cambia manualmente
"""

import sys
import os

if not any('latin-python' in p for p in sys.path):
    sys.path.insert(0, os.getcwd())

def sync_metadata():
    """Fuerza SQLModel a leer schema actual desde DB"""
    
    print("🔄 Sincronizando metadata de SQLModel con base de datos...")
    
    # Import modelos y engine
    from database import *
    from database.connection import engine
    from sqlmodel import SQLModel
    
    # Limpiar metadata vieja
    SQLModel.metadata.clear()
    
    # Reflejar schema actual desde DB
    SQLModel.metadata.reflect(bind=engine)
    
    print("✅ Metadata sincronizada correctamente")
    
    # Verificar con query de prueba
    from database.connection import get_session
    from sqlmodel import select
    
    with get_session() as session:
        links = session.exec(select(TextWordLink)).all()
        print(f"   TextWordLink: {len(links)} registros encontrados")

if __name__ == "__main__":
    sync_metadata()
