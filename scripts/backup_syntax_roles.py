#!/usr/bin/env python3
"""
Create a backup of the current sentence analysis data (syntax roles).
"""
import json
import sys
import os
import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import get_session
from database import SentenceAnalysis
from sqlmodel import select

def backup_sentences():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data",
        f"syntax_roles_backup_{timestamp}.json"
    )
    
    print(f"Starting backup to {backup_file}...")
    
    with get_session() as session:
        sentences = session.exec(select(SentenceAnalysis)).all()
        
        backup_data = {}
        count = 0
        for sent in sentences:
            if sent.syntax_roles:
                backup_data[sent.id] = {
                    "syntax_roles": sent.syntax_roles,
                    "dependency_json": sent.dependency_json,
                    "latin": sent.latin_text
                }
                count += 1
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)
            
        print(f"✅ Backup completed successfully.")
        print(f"Total sentences backed up: {count}")
        print(f"File saved at: {backup_file}")

if __name__ == "__main__":
    backup_sentences()
