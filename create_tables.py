"""
Script simple para crear las tablas de la base de datos.
Ejecutar ANTES de migrate_phase1.py
"""

from database.connection import create_db_and_tables

if __name__ == "__main__":
    print("Creando tablas en la base de datos...")
    create_db_and_tables()
    print("✅ Tablas creadas exitosamente!")
