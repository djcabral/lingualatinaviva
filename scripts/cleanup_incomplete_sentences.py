import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlmodel import Session, select, delete
from database.connection import engine
from database.syntax_models import SentenceAnalysis

def cleanup_incomplete_sentences():
    """
    Elimina oraciones que no cumplen con los criterios de calidad:
    1. Traducción faltante o vacía.
    2. Diagrama SVG faltante o vacío.
    """
    with Session(engine) as session:
        # 1. Check for missing translations
        statement_trans = select(SentenceAnalysis).where(
            (SentenceAnalysis.spanish_translation == None) | 
            (SentenceAnalysis.spanish_translation == "")
        )
        results_trans = session.exec(statement_trans).all()
        count_trans = len(results_trans)
        
        # 2. Check for missing SVG
        statement_svg = select(SentenceAnalysis).where(
            (SentenceAnalysis.tree_diagram_svg == None) | 
            (SentenceAnalysis.tree_diagram_svg == "")
        )
        results_svg = session.exec(statement_svg).all()
        count_svg = len(results_svg)
        
        print(f"Found {count_trans} sentences with missing translation.")
        print(f"Found {count_svg} sentences with missing SVG.")
        
        # Delete them
        # We can do this in one delete statement or iterate. 
        # For safety and reporting, let's select IDs first then delete.
        
        ids_to_delete = set()
        for s in results_trans:
            ids_to_delete.add(s.id)
        for s in results_svg:
            ids_to_delete.add(s.id)
            
        if not ids_to_delete:
            print("No incomplete sentences found. Database is clean.")
            return

        print(f"Total unique sentences to delete: {len(ids_to_delete)}")
        
        # Execute deletion
        statement_delete = delete(SentenceAnalysis).where(SentenceAnalysis.id.in_(ids_to_delete))
        session.exec(statement_delete)
        session.commit()
        
        print("Cleanup complete.")

if __name__ == "__main__":
    cleanup_incomplete_sentences()
