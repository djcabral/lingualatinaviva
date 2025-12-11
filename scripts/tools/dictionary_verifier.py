from database.connection import get_session
from database import Word
from sqlmodel import select
from utils.latin_logic import LatinMorphology

def verify_dictionary():
    print("Testing Dictionary Logic...")
    
    try:
        # Test 1: Database Connection
        with get_session() as session:
            print("✅ Database connection successful")
            
            # Test 2: Search Query
            search_term = "amo"
            results = session.exec(
                select(Word).where(Word.latin == search_term)
            ).all()
            print(f"✅ Search for '{search_term}' returned {len(results)} results")
            
            # Test 3: Morphology
            morphology = LatinMorphology()
            if results:
                word = results[0]
                if word.part_of_speech == 'verb':
                    forms = morphology.conjugate_verb(word.latin, word.conjugation, word.principal_parts)
                    print(f"✅ Conjugation generated: {len(forms)} forms")
                elif word.part_of_speech == 'noun':
                    forms = morphology.decline_noun(word.latin, word.declension, word.gender, word.genitive)
                    print(f"✅ Declension generated: {len(forms)} forms")
                    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify_dictionary()
