import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

def verify_modules():
    print("Verifying Paradigm Generator and Scriptorium dependencies...")
    
    # 1. Check pycollatinus
    try:
        from utils.collatinus_analyzer import analyzer
        if analyzer.is_ready():
            print("✅ PyCollatinus is ready.")
            # Test generation
            paradigm = analyzer.generate_paradigm("rosa")
            if paradigm and 'forms' in paradigm:
                 print("✅ Paradigm generation for 'rosa' successful.")
            else:
                 print("❌ Paradigm generation failed.")
        else:
            print("❌ PyCollatinus is NOT ready.")
    except ImportError:
        print("❌ Could not import utils.collatinus_analyzer.")
    except Exception as e:
        print(f"❌ Error checking PyCollatinus: {e}")

    # 2. Check Database for Scriptorium
    try:
        from database.connection import get_session
        from database import Word
        from sqlmodel import select, func
        
        with get_session() as session:
            # Check if we can query the database
            reservoir_count = session.exec(select(func.count(Word.id)).where(Word.status == 'reservoir')).one()
            print(f"✅ Database connection successful. Words in reservoir: {reservoir_count}")
            
    except Exception as e:
        print(f"❌ Error checking database: {e}")

if __name__ == "__main__":
    verify_modules()
