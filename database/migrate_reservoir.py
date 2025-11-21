#!/usr/bin/env python3
"""
Migration script for Reservoir System.

Adds 'status' column to Word table and populates it:
- 'active': Complete words ready for exercises
- 'reservoir': Incomplete words needing manual review
"""

import sqlite3
import sys
from pathlib import Path

def migrate_reservoir(db_path: str = 'lingua_latina.db'):
    """Add status column and classify words."""
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"Migrating database for Reservoir System: {db_path}")
    
    # 1. Add status column if not exists
    cursor.execute("PRAGMA table_info(word)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if 'status' not in columns:
        print("Adding 'status' column...")
        cursor.execute("ALTER TABLE word ADD COLUMN status TEXT DEFAULT 'active'")
    else:
        print("'status' column already exists.")
    
    # 2. Identify and mark incomplete words as 'reservoir'
    print("Classifying words...")
    
    # Reset all to active first
    cursor.execute("UPDATE word SET status = 'active'")
    
    # Criteria for Reservoir (Incomplete):
    # 1. Nouns without declension OR gender
    cursor.execute("""
        UPDATE word 
        SET status = 'reservoir' 
        WHERE part_of_speech = 'noun' 
        AND (declension IS NULL OR gender IS NULL)
    """)
    nouns_moved = cursor.rowcount
    
    # 2. Verbs without conjugation OR principal parts
    cursor.execute("""
        UPDATE word 
        SET status = 'reservoir' 
        WHERE part_of_speech = 'verb' 
        AND (conjugation IS NULL OR principal_parts IS NULL)
    """)
    verbs_moved = cursor.rowcount
    
    # 3. Adjectives without declension
    cursor.execute("""
        UPDATE word 
        SET status = 'reservoir' 
        WHERE part_of_speech = 'adjective' 
        AND declension IS NULL
    """)
    adj_moved = cursor.rowcount
    
    # 4. Unknown/Other parts of speech (optional, maybe keep them active if they have translation)
    # For now, let's keep 'unknown' in reservoir
    cursor.execute("""
        UPDATE word 
        SET status = 'reservoir' 
        WHERE part_of_speech = 'unknown'
    """)
    unknown_moved = cursor.rowcount
    
    conn.commit()
    
    total_reservoir = nouns_moved + verbs_moved + adj_moved + unknown_moved
    
    # Get total active
    cursor.execute("SELECT COUNT(*) FROM word WHERE status = 'active'")
    total_active = cursor.fetchone()[0]
    
    print("-" * 40)
    print(f"Migration Complete!")
    print(f"Moved to Reservoir (Incomplete):")
    print(f"  - Nouns: {nouns_moved}")
    print(f"  - Verbs: {verbs_moved}")
    print(f"  - Adjectives: {adj_moved}")
    print(f"  - Unknown: {unknown_moved}")
    print(f"  TOTAL RESERVOIR: {total_reservoir}")
    print(f"  TOTAL ACTIVE: {total_active}")
    print("-" * 40)
    
    conn.close()

if __name__ == '__main__':
    db_path = sys.argv[1] if len(sys.argv) > 1 else 'lingua_latina.db'
    migrate_reservoir(db_path)
