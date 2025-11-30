"""
Script para encontrar palabras con traducciones en inglés en el vocabulario
"""

import sys
import os

# Add project root to path
if not any('latin-python' in p for p in sys.path):
    sys.path.insert(0, os.getcwd())

from database.connection import get_session
from database import Word
from sqlmodel import select

# Palabras comunes en inglés que indican traducción no española
ENGLISH_INDICATORS = [
    'the', 'and', 'or', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
    'can', 'could', 'may', 'might', 'must', 'shall',
    'to', 'of', 'in', 'on', 'at', 'by', 'with', 'from', 'as', 'for',
    'kiss', 'love', 'girl', 'boy', 'man', 'woman', 'rose', 'father', 'mother',
    'brother', 'sister', 'friend', 'house', 'city', 'water', 'earth', 'sky',
    'big', 'small', 'good', 'bad', 'beautiful', 'ugly', 'happy', 'sad'
]

def find_english_words():
    """Encuentra palabras con traducciones probablemente en inglés"""
    
    with get_session() as session:
        all_words = session.exec(select(Word)).all()
        
        english_words = []
        
        for word in all_words:
            translation_lower = word.translation.lower()
            
            # Buscar indicadores de inglés
            for indicator in ENGLISH_INDICATORS:
                # Check for exact word match or start/end of string
                if f' {indicator} ' in f' {translation_lower} ' or \
                   translation_lower == indicator:
                    english_words.append(word)
                    break
        
        return english_words

def main():
    print("🔍 Buscando palabras con traducciones en inglés...\n")
    
    english_words = find_english_words()
    
    print(f"Encontradas {len(english_words)} palabras con posible traducción en inglés:\n")
    
    # Agrupar por primera letra para facilitar lectura
    by_letter = {}
    for word in english_words:
        if not word.latin: continue
        first = word.latin[0].upper()
        if first not in by_letter:
            by_letter[first] = []
        by_letter[first].append(word)
    
    # Mostrar agrupadas
    for letter in sorted(by_letter.keys()):
        print(f"\n{'='*60}")
        print(f"Letra {letter}:")
        print(f"{'='*60}")
        for word in by_letter[letter]:
            print(f"  ID {word.id:5d} | {word.latin:20s} | {word.translation}")
    
    print(f"\n\n{'='*60}")
    print(f"TOTAL: {len(english_words)} palabras")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
