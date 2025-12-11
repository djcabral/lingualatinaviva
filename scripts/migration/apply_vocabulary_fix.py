"""
Script to apply the vocabulary fix:
1. Clear Word table
2. Import clean vocabulary.csv
3. Re-apply Phase 2 migration
"""
import sys
import os
import csv
from pathlib import Path
from sqlmodel import Session, select, delete

# Add project root to path
sys.path.append(os.getcwd())

from database.connection import engine
from database import Word
import database.migrate_phase2 as phase2

def apply_fix():
    print("🗑️ Clearing Word table...")
    with Session(engine) as session:
        # Delete all words
        statement = delete(Word)
        result = session.exec(statement)
        session.commit()
        print(f"✓ Deleted existing words.")
    
    print("📥 Importing clean vocabulary...")
    csv_path = Path("data/vocabulary.csv")
    
    if not csv_path.exists():
        print(f"❌ Error: {csv_path} not found!")
        return

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        with Session(engine) as session:
            count = 0
            for row in reader:
                # Handle empty fields
                level = int(row['level']) if row['level'] else 1
                
                word = Word(
                    latin=row['latin'],
                    translation=row['translation'],
                    part_of_speech=row['part_of_speech'],
                    level=level,
                    genitive=row['genitive'] or None,
                    gender=row['gender'] or None,
                    declension=row['declension'] or None,
                    principal_parts=row['principal_parts'] or None,
                    conjugation=row['conjugation'] or None
                )
                session.add(word)
                count += 1
            session.commit()
            print(f"✓ Imported {count} words from CSV.")

    print("🔄 Re-applying Phase 2 migration (irregulars)...")
    try:
        phase2.migrate_phase2()
    except Exception as e:
        print(f"⚠️ Warning during migration: {e}")

if __name__ == "__main__":
    apply_fix()
