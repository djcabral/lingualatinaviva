import sys
import os
from sqlmodel import Session, select, text
from database import engine, Text, InflectedForm, TextWordLink, Word

# Ensure utils import
sys.path.append(os.getcwd())

def fix_systemic_issues():
    print("🛠️ Starting Systemic Fix...\n")
    
    with Session(engine) as session:
        # 1. Clean Orphans
        print("--- 1. Cleaning Orphans ---")
        
        # InflectedForms
        orphaned_forms = session.exec(select(InflectedForm).where(
            InflectedForm.word_id != None,
            InflectedForm.word_id.not_in(select(Word.id))
        )).all()
        print(f"Deleting {len(orphaned_forms)} orphaned InflectedForms...")
        for f in orphaned_forms:
            session.delete(f)
            
        # TextWordLinks
        orphaned_links = session.exec(select(TextWordLink).where(
            TextWordLink.word_id != None,
            TextWordLink.word_id.not_in(select(Word.id))
        )).all()
        print(f"Deleting {len(orphaned_links)} orphaned TextWordLinks...")
        for l in orphaned_links:
            session.delete(l)
            
        session.commit()
        print("✅ Orphans cleaned.")
        
        # 2. Re-analyze specific texts found
        print("\n--- 2. Re-analyzing texts with Romae/Romani ---")
        target_ids = [1, 5, 9, 14, 26]
        target_texts = session.exec(select(Text).where(Text.id.in_(target_ids))).all()
        
        print(f"Found {len(target_texts)} texts to re-analyze.")
        
        for text_obj in target_texts:
            print(f"Re-analyzing Text ID {text_obj.id}: {text_obj.title}...")
            try:
                from utils.stanza_analyzer import analyze_and_save_text
                # Using the utility function to re-analyze using Stanza and DB
                # Note: analyze_and_save_text commits internally
                analyze_and_save_text(text_obj.id, text_obj.content, session)
                print(f"✅ Text {text_obj.id} re-analyzed.")
            except Exception as e:
                print(f"❌ Error analyzing text {text_obj.id}: {e}")

if __name__ == "__main__":
    fix_systemic_issues()
