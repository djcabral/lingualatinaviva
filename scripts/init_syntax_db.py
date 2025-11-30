"""
Script para inicializar las tablas de sintaxis en la base de datos
"""
import sys
import os
from sqlmodel import SQLModel

# Add project root to path
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_path not in sys.path:
    sys.path.append(root_path)

from database.connection import engine
# Importar modelos para que SQLModel los registre
from database.syntax_models import SentenceAnalysis, SyntaxCategory, SentenceCategoryLink

def init_syntax_tables():
    print("Inicializando tablas de sintaxis...")
    SQLModel.metadata.create_all(engine)
    print("✅ Tablas creadas exitosamente")

if __name__ == "__main__":
    init_syntax_tables()
