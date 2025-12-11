
import sys
import os
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.content_loader import ContentLoader
from database.connection import get_session
from database import SentenceAnalysis
from sqlmodel import select

def test_loader():
    print("="*60)
    print("TESTING CONTENT LOADER")
    print("="*60)
    
    loader = ContentLoader()
    
    if not loader.nlp:
        print("❌ Failed to load NLP model. Aborting test.")
        return

    # Test Sentence
    latin = "Alea iacta est."
    translation = "La suerte está echada."
    source = "Suetonio"
    
    print(f"\n🔄 Processing: {latin}")
    
    sentence = loader.process_sentence(
        latin_text=latin,
        translation=translation,
        source=source,
        lesson=99, # Test lesson
        complexity=2,
        constructions=["passive"]
    )
    
    if not sentence:
        print("❌ Failed to process sentence.")
        return

    print("\n✅ Sentence Processed!")
    
    # Verify fields
    print(f"  - Latin: {sentence.latin_text}")
    print(f"  - Translation: {sentence.spanish_translation}")
    
    print("\n🔍 Dependency Analysis (JSON):")
    if sentence.dependency_json:
        deps = json.loads(sentence.dependency_json)
        print(f"    - Tokens: {len(deps)}")
        for t in deps:
            print(f"      [{t['id']}] {t['text']} ({t['pos']}) -> {t['dep']}")
    else:
        print("    ❌ Missing dependency_json")

    print("\n🎨 Visual Tree (SVG):")
    if sentence.tree_diagram_svg:
        print(f"    - SVG generated ({len(sentence.tree_diagram_svg)} bytes)")
    else:
        print("    ❌ Missing tree_diagram_svg")

    print("\n🏷️ Syntax Roles (JSON):")
    if sentence.syntax_roles:
        roles = json.loads(sentence.syntax_roles)
        print(f"    - Roles mapped: {roles}")
    else:
        print("    ❌ Missing syntax_roles")

if __name__ == "__main__":
    test_loader()
