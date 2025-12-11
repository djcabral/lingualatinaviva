from sqlmodel import Session, select
from database import engine, Word, InflectedForm, TextWordLink

def consolidate_venio():
    with Session(engine) as session:
        # ID 69 (victim, old) -> ID 633 (target, new with macrons)
        victim_id = 69
        target_id = 633
        
        victim = session.get(Word, victim_id)
        target = session.get(Word, target_id)
        
        if not victim or not target:
            print("❌ One of the words not found. Aborting.")
            return

        print(f"🔄 Consolidating '{victim.latin}' ({victim_id}) -> '{target.latin}' ({target_id})")
        
        # 1. Update InflectedForms
        forms = session.exec(select(InflectedForm).where(InflectedForm.word_id == victim_id)).all()
        print(f"   Moving {len(forms)} forms...")
        for f in forms:
            f.word_id = target_id
            session.add(f)
            
        # 2. Update TextWordLinks
        links = session.exec(select(TextWordLink).where(TextWordLink.word_id == victim_id)).all()
        print(f"   Moving {len(links)} text links...")
        for l in links:
            l.word_id = target_id
            session.add(l)

        # 2.1 Update ReviewLogs (Critical Fix)
        # We need to import ReviewLog dynamically or use raw SQL if not easily available,
        # but let's try to fetch it from the database module or just use SQL for safety.
        # Using raw SQL for ReviewLog to avoid Import errors if it's not exported in __init__
        from sqlalchemy import text
        print("   Moving ReviewLog entries...")
        session.exec(text(f"UPDATE reviewlog SET word_id = {target_id} WHERE word_id = {victim_id}"))
            
        # 3. Merge Metadata (preserve crucial info from victim)
        if victim.is_fundamental:
            target.is_fundamental = True
        if victim.level and (not target.level or victim.level < target.level):
            target.level = victim.level
        if not target.principal_parts and victim.principal_parts:
            target.principal_parts = victim.principal_parts
            
        session.add(target)
        
        # 4. Delete Victim
        session.delete(victim)
        
        session.commit()
        print("✅ Consolidation complete.")

if __name__ == "__main__":
    consolidate_venio()
