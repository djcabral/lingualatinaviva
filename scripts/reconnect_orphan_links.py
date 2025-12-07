"""
Script para reconectar TextWordLinks huérfanos después de la consolidación.

Busca palabras correctas para asignar a links que perdieron su word_id.
"""

import sys
import os
sys.path.append(os.getcwd())

from database.connection import get_session
from database import Word, TextWordLink
from sqlmodel import select
import unicodedata

def normalize_latin(word: str) -> str:
    """Normaliza una palabra latina para comparación"""
    if not word:
        return ""
    word = unicodedata.normalize("NFD", word)
    word = "".join(c for c in word if unicodedata.category(c) != "Mn")
    word = word.lower().replace("v", "u").replace("j", "i")
    return word


def reconnect_orphan_links(dry_run=True):
    """Reconecta links huérfanos a palabras del vocabulario"""
    
    print("=" * 80)
    print("🔗 RECONNECT ORPHAN LINKS")
    print("=" * 80)
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print()
    
    with get_session() as session:
        # Find orphan links (non-punctuation with null word_id)
        punctuation = set('.,;:!?\'"()[]')
        
        all_orphans = session.exec(
            select(TextWordLink).where(TextWordLink.word_id == None)
        ).all()
        
        orphans = [l for l in all_orphans if l.form and l.form not in punctuation and not l.form.startswith("'")]
        
        print(f"Found {len(orphans)} orphan word links\n")
        
        # Get all vocabulary words with translations
        all_words = session.exec(select(Word)).all()
        
        # Build lookup by normalized form
        word_lookup = {}
        for w in all_words:
            norm = normalize_latin(w.latin)
            # Prefer words with translations
            if norm not in word_lookup or (w.translation and w.translation != "[PENDING]"):
                word_lookup[norm] = w
        
        reconnected = 0
        not_found = []
        
        for link in orphans:
            form_norm = normalize_latin(link.form)
            
            # Try direct match
            match = word_lookup.get(form_norm)
            
            # If not found, try some common variations
            if not match:
                # Try removing common endings
                for ending in ['m', 's', 'rum', 'bus', 'is', 'os', 'as', 'a', 'i', 'ae', 'am', 'um', 'nt']:
                    if form_norm.endswith(ending) and len(form_norm) > len(ending) + 2:
                        stem = form_norm[:-len(ending)]
                        for w in all_words:
                            w_norm = normalize_latin(w.latin)
                            if w_norm.startswith(stem) or stem.startswith(w_norm[:3]):
                                match = w
                                break
                    if match:
                        break
            
            if match:
                if not dry_run:
                    link.word_id = match.id
                    session.add(link)
                print(f"  {link.form} (T{link.text_id}) → {match.latin} ({match.translation or 'no trans'})")
                reconnected += 1
            else:
                not_found.append((link.text_id, link.form))
        
        if not dry_run:
            session.commit()
        
        print()
        print("=" * 80)
        print(f"Reconnected: {reconnected}")
        print(f"Not found: {len(not_found)}")
        
        if not_found:
            print("\nWords not matched:")
            for tid, form in not_found:
                print(f"  T{tid}: {form}")
        
        if dry_run:
            print("\nRun with --live to apply changes")


if __name__ == "__main__":
    dry_run = "--live" not in sys.argv
    reconnect_orphan_links(dry_run=dry_run)
