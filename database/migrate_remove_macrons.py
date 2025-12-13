#!/usr/bin/env python3
"""
Migration: Remove Macrons from Database

This script normalizes all Latin text by removing macrons (long vowel marks).
Converts: ā→a, ē→e, ī→i, ō→o, ū→u (and uppercase versions)

Affected tables:
- Word: latin, collatinus_lemma, genitive, principal_parts
- Text: content
- TextWordLink: form

Usage:
    python database/migrate_remove_macrons.py [--dry-run]
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session, select
from database import engine, Word, Text, TextWordLink

# Macron mapping
MACRON_MAP = {
    'ā': 'a', 'ē': 'e', 'ī': 'i', 'ō': 'o', 'ū': 'u',
    'Ā': 'A', 'Ē': 'E', 'Ī': 'I', 'Ō': 'O', 'Ū': 'U',
}

def remove_macrons(text: str) -> str:
    """Remove all macrons from a string."""
    if not text:
        return text
    result = text
    for macron, plain in MACRON_MAP.items():
        result = result.replace(macron, plain)
    return result

def migrate_words(session: Session, dry_run: bool = False) -> int:
    """Normalize Word table fields."""
    words = session.exec(select(Word)).all()
    updated = 0
    
    for word in words:
        changed = False
        
        # Check and update latin field
        if word.latin and word.latin != remove_macrons(word.latin):
            if not dry_run:
                word.latin = remove_macrons(word.latin)
            changed = True
        
        # Check and update collatinus_lemma
        if word.collatinus_lemma and word.collatinus_lemma != remove_macrons(word.collatinus_lemma):
            if not dry_run:
                word.collatinus_lemma = remove_macrons(word.collatinus_lemma)
            changed = True
        
        # Check and update genitive
        if word.genitive and word.genitive != remove_macrons(word.genitive):
            if not dry_run:
                word.genitive = remove_macrons(word.genitive)
            changed = True
        
        # Check and update principal_parts
        if word.principal_parts and word.principal_parts != remove_macrons(word.principal_parts):
            if not dry_run:
                word.principal_parts = remove_macrons(word.principal_parts)
            changed = True
        
        if changed:
            updated += 1
            if not dry_run:
                session.add(word)
    
    return updated

def migrate_texts(session: Session, dry_run: bool = False) -> int:
    """Normalize Text table content field."""
    texts = session.exec(select(Text)).all()
    updated = 0
    
    for text in texts:
        if text.content and text.content != remove_macrons(text.content):
            if not dry_run:
                text.content = remove_macrons(text.content)
            updated += 1
            if not dry_run:
                session.add(text)
    
    return updated

def migrate_text_word_links(session: Session, dry_run: bool = False) -> int:
    """Normalize TextWordLink form field."""
    links = session.exec(select(TextWordLink)).all()
    updated = 0
    
    for link in links:
        if link.form and link.form != remove_macrons(link.form):
            if not dry_run:
                link.form = remove_macrons(link.form)
            updated += 1
            if not dry_run:
                session.add(link)
    
    return updated

def main():
    dry_run = '--dry-run' in sys.argv
    
    print("=" * 60)
    print("MIGRATION: Remove Macrons from Database")
    print("=" * 60)
    
    if dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
    else:
        print("⚠️  This will permanently modify the database!")
        confirm = input("Type 'YES' to continue: ")
        if confirm != 'YES':
            print("Aborted.")
            return
    
    print()
    
    with Session(engine) as session:
        # Migrate Words
        print("📝 Processing Word table...")
        words_updated = migrate_words(session, dry_run)
        print(f"   → {words_updated} words {'would be' if dry_run else ''} updated")
        
        # Migrate Texts
        print("📖 Processing Text table...")
        texts_updated = migrate_texts(session, dry_run)
        print(f"   → {texts_updated} texts {'would be' if dry_run else ''} updated")
        
        # Migrate TextWordLinks
        print("🔗 Processing TextWordLink table...")
        links_updated = migrate_text_word_links(session, dry_run)
        print(f"   → {links_updated} links {'would be' if dry_run else ''} updated")
        
        if not dry_run:
            session.commit()
            print()
            print("✅ Migration completed successfully!")
        else:
            print()
            print("🔍 Dry run completed. Run without --dry-run to apply changes.")
    
    print()
    print(f"Total records affected: {words_updated + texts_updated + links_updated}")

if __name__ == "__main__":
    main()
