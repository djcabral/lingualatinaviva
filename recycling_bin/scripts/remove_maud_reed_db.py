import os
import sys
from sqlmodel import select, delete

# Add project root to path
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_path not in sys.path:
    sys.path.append(root_path)

from database.connection import get_session
from database.syntax_models import SentenceAnalysis

def main():
    print("Cleaning up Maud Reed entries from database...")
    with get_session() as session:
        # Delete Julia entries
        statement = delete(SentenceAnalysis).where(SentenceAnalysis.source.like("julia%"))
        result = session.exec(statement)
        print(f"Deleted {result.rowcount} Julia entries.")
        
        # Delete Camilla entries
        statement = delete(SentenceAnalysis).where(SentenceAnalysis.source.like("camilla%"))
        result = session.exec(statement)
        print(f"Deleted {result.rowcount} Camilla entries.")
        
        session.commit()
    print("Cleanup complete.")

if __name__ == "__main__":
    main()
