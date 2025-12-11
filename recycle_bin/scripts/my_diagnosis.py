
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from database.connection import get_session
from utils.text_analyzer import LatinTextAnalyzer

def test_analyzer():
    try:
        with get_session() as session:
            print("Testing analysis for 'Rōma'...")
            results = LatinTextAnalyzer.analyze_text("Rōma in Italiā est.", session)
            
            for item in results:
                print(f"Form: {item['form']}")
                if not item.get('is_punctuation'):
                    analyses = item.get('analyses', [])
                    lemma = item.get('lemma')
                    morphology = item.get('morphology', {})
                    pos = item.get('pos')
                    
                    # Logic from readings_view.py
                    if not lemma and analyses:
                        primary = analyses[0]
                        lemma = primary.get('lemma')
                        morphology = primary.get('morphology')
                        pos = primary.get('pos')
                    
                    formatted_morph = LatinTextAnalyzer.format_morphology(morphology or {}, pos)
                    print(f"  Lemma: {lemma}")
                    print(f"  Morphology: {formatted_morph}")
                    print(f"  POS: {pos}")
                print("-" * 20)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_analyzer()
