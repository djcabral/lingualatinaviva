"""
Script para traducir en lote las palabras en inglés encontradas
"""

import sys
import os

if not any('latin-python' in p for p in sys.path):
    sys.path.insert(0, os.getcwd())

from database.connection import get_session
from database.models import Word
from sqlmodel import select

# Diccionario de correcciones: ID -> Nueva traducción
CORRECTIONS = {
    61: "amar",
    93: "amigo",
    111: "feliz, dichoso",
    17: "los demás",
    125: "casa",
    48: "ser; al inicio de frase: hay",  # est
    51: "y",
    4: "mujer",
    70: "tener",
    6: "madre",
    36: "grande",
    115: "triste",
    110: "beso",  # oscilum (probablemente osculum)
    1: "niña",
    2: "niño",
    5: "padre",
    37: "pequeño",
    107: "rosa",
    49: "ser; al inicio de frase: hay",  # sunt
    3: "hombre",
    # Añadir más si es necesario
}

def batch_translate():
    print("🔧 Aplicando traducciones al español...\n")
    
    with get_session() as session:
        count = 0
        for word_id, new_translation in CORRECTIONS.items():
            word = session.get(Word, word_id)
            if word:
                print(f"  ID {word_id}: {word.latin}")
                print(f"    Old: {word.translation}")
                print(f"    New: {new_translation}")
                word.translation = new_translation
                session.add(word)
                count += 1
            else:
                print(f"  ⚠️ ID {word_id} no encontrado")
        
        session.commit()
        print(f"\n✅ {count} palabras actualizadas.")

if __name__ == "__main__":
    batch_translate()
