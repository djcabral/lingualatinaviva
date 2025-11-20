"""
Script de verificación - Fase 1: Base de Datos Mejorada

Verifica que:
1. Todas las tablas existen
2. Las relaciones funcionan correctamente
3. Los datos se cargaron correctamente
"""

from database.connection import get_session
from database.models import Author, Word, WordFrequency, SyntaxPattern, Text, TextWordLink
from sqlmodel import select
import sqlite3

def verify_phase1():
    """Ejecuta verificaciones de integridad"""
    
    print("=== Verificación Fase 1: Base de Datos Mejorada ===\n")
    
    # 1. Verificar tablas existen
    print("1. Verificando tablas...")
    conn = sqlite3.connect("lingua_latina.db")
    cursor = conn.cursor()
    
    tables = ["author", "word", "wordfrequency", "syntaxpattern", "text", "textwordlink"]
    for table in tables:
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
        result = cursor.fetchone()
        if result:
            print(f"   ✓ Tabla '{table}' existe")
        else:
            print(f"   ❌ Tabla '{table}' NO existe")
    
    conn.close()
    print()
    
    # 2. Verificar datos
    print("2. Verificando datos...")
    with get_session() as session:
        # Autores
        authors = session.exec(select(Author)).all()
        print(f"   Autores en BD: {len(authors)}")
        for author in authors:
            print(f"      - {author.name} (nivel {author.difficulty_level})")
        
        # Palabras
        total_words = session.exec(select(Word)).all()
        print(f"\n   Total palabras: {len(total_words)}")
        
        invariable_words = session.exec(
            select(Word).where(Word.is_invariable == True)
        ).all()
        print(f"   Palabras invariables: {len(invariable_words)}")
        for word in invariable_words[:5]:  # Mostrar primeras 5
            print(f"      - {word.latin} ({word.category})")
        
        fundamental_words = session.exec(
            select(Word).where(Word.is_fundamental == True)
        ).all()
        print(f"\n   Palabras fundamentales: {len(fundamental_words)}")
        for word in fundamental_words:
            print(f"      - {word.latin} (rank: {word.frequency_rank_global})")
    
    print()
    
    # 3. Verificar relaciones
    print("3. Verificando relaciones...")
    with get_session() as session:
        # Obtener una palabra
        word = session.exec(select(Word).limit(1)).first()
        if word:
            print(f"   Probando relaciones en palabra: {word.latin}")
            
            # Verificar que puede acceder a author (aunque sea None)
            try:
                author = word.author
                print(f"      ✓ Relación Word.author funciona (valor: {author.name if author else 'None'})")
            except Exception as e:
                print(f"      ❌ Error en Word.author: {e}")
            
            # Verificar reviews
            try:
                reviews = word.reviews
                print(f"      ✓ Relación Word.reviews funciona ({len(reviews)} reviews)")
            except Exception as e:
                print(f"      ❌ Error en Word.reviews: {e}")
            
        # Obtener un autor y verificar relación inversa
        author = session.exec(select(Author).limit(1)).first()
        if author:
            print(f"\n   Probando relaciones en autor: {author.name}")
            try:
                words = author.words
                print(f"      ✓ Relación Author.words funciona ({len(words)} words)")
            except Exception as e:
                print(f"      ❌ Error en Author.words: {e}")
            
            try:
                texts = author.texts
                print(f"      ✓ Relación Author.texts funciona ({len(texts)} texts)")
            except Exception as e:
                print(f"      ❌ Error en Author.texts: {e}")
    
    print()
    
    # 4. Verificar columnas nuevas en Word
    print("4. Verificando columnas nuevas en Word...")
    conn = sqlite3.connect("lingua_latina.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(word)")
    columns = [row[1] for row in cursor.fetchall()]
    
    expected_new_columns = [
        "author_id",
        "frequency_rank_global",
        "is_invariable",
        "is_fundamental",
        "category"
    ]
    
    for col in expected_new_columns:
        if col in columns:
            print(f"   ✓ Columna '{col}' existe")
        else:
            print(f"   ❌ Columna '{col}' NO existe")
    
    conn.close()
    print()
    
    print("✅ Verificación completada!")

if __name__ == "__main__":
    verify_phase1()
