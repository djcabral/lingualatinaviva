"""
Script para corregir palabras duplicadas en la base de datos.

El motor NLP creó entradas duplicadas con [PENDING] que deben consolidarse
con las entradas correctas existentes.

Ejemplo:
- ID 580: ciuis (adjective) [PENDING] ← Incorrecto
- ID 148: civis (noun) = ciudadano ← Correcto

El script:
1. Encuentra pares de palabras duplicadas
2. Actualiza TextWordLinks para apuntar a la entrada correcta
3. Elimina las entradas duplicadas con [PENDING]
"""

import sys
import os
sys.path.append(os.getcwd())

from database.connection import get_session
from database import Word, TextWordLink
from sqlmodel import select
import unicodedata

# Mapeo de variantes ortográficas latinas (u/v, i/j)
def normalize_latin(word: str) -> str:
    """Normaliza una palabra latina para comparación (u/v, i/j, macrones)"""
    if not word:
        return ""
    # Remove macrons
    word = unicodedata.normalize("NFD", word)
    word = "".join(c for c in word if unicodedata.category(c) != "Mn")
    # Normalize u/v and i/j
    word = word.lower().replace("v", "u").replace("j", "i")
    return word


def find_duplicates(session):
    """Encuentra pares de palabras donde una tiene [PENDING] y otra tiene traducción real"""
    
    # Get all words with [PENDING]
    pending_words = session.exec(
        select(Word).where(Word.translation == "[PENDING]")
    ).all()
    
    duplicates = []
    
    for pending in pending_words:
        pending_norm = normalize_latin(pending.latin)
        
        # Find a matching word with real translation
        all_words = session.exec(
            select(Word).where(
                Word.id != pending.id,
                Word.translation != "[PENDING]",
                Word.translation != None,
                Word.translation != ""
            )
        ).all()
        
        for real_word in all_words:
            real_norm = normalize_latin(real_word.latin)
            
            if pending_norm == real_norm:
                duplicates.append({
                    "pending": pending,
                    "real": real_word,
                    "normalized": pending_norm
                })
                break
    
    return duplicates


def consolidate_duplicates(dry_run=True):
    """Corrige las palabras duplicadas"""
    
    print("=" * 80)
    print("🔧 CONSOLIDATE DUPLICATE WORDS SCRIPT")
    print("=" * 80)
    print(f"Mode: {'DRY RUN (no changes)' if dry_run else 'LIVE (will modify database)'}")
    print()
    
    with get_session() as session:
        duplicates = find_duplicates(session)
        
        print(f"📊 Found {len(duplicates)} duplicate pairs\n")
        
        if not duplicates:
            print("✅ No duplicates found. Database is clean.")
            return
        
        # Show duplicates
        print("Duplicate pairs found:")
        print("-" * 80)
        for dup in duplicates:
            p = dup["pending"]
            r = dup["real"]
            print(f"  '{p.latin}' (ID {p.id}, {p.part_of_speech}, [PENDING])")
            print(f"    → '{r.latin}' (ID {r.id}, {r.part_of_speech}, '{r.translation}')")
            print()
        
        if dry_run:
            print("=" * 80)
            print("DRY RUN complete. Run with --live to apply changes.")
            return
        
        # Apply fixes
        print("=" * 80)
        print("Applying fixes...")
        print("-" * 80)
        
        total_links_updated = 0
        total_words_deleted = 0
        
        for dup in duplicates:
            pending = dup["pending"]
            real = dup["real"]
            
            # Find all TextWordLinks pointing to the pending word
            links = session.exec(
                select(TextWordLink).where(TextWordLink.word_id == pending.id)
            ).all()
            
            if links:
                print(f"Updating {len(links)} links from '{pending.latin}' (ID {pending.id}) → '{real.latin}' (ID {real.id})")
                for link in links:
                    link.word_id = real.id
                    session.add(link)
                total_links_updated += len(links)
            
            # Delete the pending word
            print(f"Deleting duplicate: '{pending.latin}' (ID {pending.id})")
            session.delete(pending)
            total_words_deleted += 1
        
        session.commit()
        
        print()
        print("=" * 80)
        print(f"✅ Fix complete!")
        print(f"   - Links updated: {total_links_updated}")
        print(f"   - Duplicate words deleted: {total_words_deleted}")
        print("=" * 80)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--live":
        consolidate_duplicates(dry_run=False)
    else:
        consolidate_duplicates(dry_run=True)
        print("\n💡 To apply changes, run: python scripts//home/diego/Projects/latin-python/test_debug_scripts/consolidate_word_duplicates.py --live")
