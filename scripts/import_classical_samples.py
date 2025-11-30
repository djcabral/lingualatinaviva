import sys
import os
import json
import spacy
from sqlmodel import Session, select

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.connection import engine
from database.syntax_models import SentenceAnalysis
from utils.syntax_analyzer import LatinSyntaxAnalyzer

def import_classical_samples():
    json_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'texts', 'classical_samples_translated.json')
    
    if not os.path.exists(json_path):
        print(f"Error: File not found at {json_path}")
        return

    print("Loading LatinCy model...")
    try:
        # Initialize analyzer with string name as fixed in previous step
        analyzer = LatinSyntaxAnalyzer("la_core_web_lg")
    except Exception as e:
        print(f"Error loading analyzer: {e}")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    print(f"Found {len(data)} sentences to import.")
    
    with Session(engine) as session:
        success_count = 0
        skip_count = 0
        
        for item in data:
            latin_text = item['latin']
            translation = item['translation']
            source = item['source']
            
            # Check if already exists
            existing = session.exec(select(SentenceAnalysis).where(SentenceAnalysis.latin_text == latin_text)).first()
            if existing:
                print(f"Skipping existing: {latin_text[:30]}...")
                skip_count += 1
                continue
                
            try:
                print(f"Analyzing: {latin_text[:50]}...")
                analysis = analyzer.analyze_sentence(latin_text)
                
                # Inject manual translation
                analysis.spanish_translation = translation
                analysis.source = source
                analysis.verified = True # We manually verified these
                
                # Validation
                if not analysis.tree_diagram_svg or len(analysis.tree_diagram_svg) < 100:
                    print(f"  [WARNING] SVG generation failed for: {latin_text[:30]}")
                    continue
                    
                session.add(analysis)
                success_count += 1
                
            except Exception as e:
                print(f"  [ERROR] Failed to analyze: {e}")
                
        session.commit()
        print(f"\nImport complete.")
        print(f"Successfully imported: {success_count}")
        print(f"Skipped (already existed): {skip_count}")

if __name__ == "__main__":
    import_classical_samples()
