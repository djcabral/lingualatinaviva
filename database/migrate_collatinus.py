#!/usr/bin/env python3
"""
Migration script to add Collatinus dictionary fields to Word table.

Adds:
- definition_es: Full Spanish definition
- collatinus_lemma: Original lemma from Collatinus
- collatinus_model: Flexion model name
"""

import sqlite3
import sys
from pathlib import Path

def migrate_database(db_path: str = 'lingua_latina.db'):
    """Add Collatinus fields to Word table."""
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"Migrating database: {db_path}")
    
    # Check if columns already exist
    cursor.execute("PRAGMA table_info(word)")
    columns = [row[1] for row in cursor.fetchall()]
    
    migrations_needed = []
    
    if 'definition_es' not in columns:
        migrations_needed.append(
            "ALTER TABLE word ADD COLUMN definition_es TEXT"
        )
    
    if 'collatinus_lemma' not in columns:
        migrations_needed.append(
            "ALTER TABLE word ADD COLUMN collatinus_lemma TEXT"
        )
    
    if 'collatinus_model' not in columns:
        migrations_needed.append(
            "ALTER TABLE word ADD COLUMN collatinus_model TEXT"
        )
    
    if not migrations_needed:
        print("✅ Database already up to date!")
        conn.close()
        return
    
    print(f"Adding {len(migrations_needed)} new columns...")
    
    for migration in migrations_needed:
        print(f"  Executing: {migration}")
        cursor.execute(migration)
    
    conn.commit()
    conn.close()
    
    print("✅ Migration complete!")

if __name__ == '__main__':
    db_path = sys.argv[1] if len(sys.argv) > 1 else 'lingua_latina.db'
    migrate_database(db_path)
