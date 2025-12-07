
import sys
import os
from sqlmodel import select

sys.path.append(os.getcwd())

from database.connection import get_session
from database.models import Text, TextWordLink

def debug_structure(text_id=1):
    with get_session() as session:
        text = session.get(Text, text_id)
        if not text:
            print(f"Text {text_id} not found.")
            return
            
        print(f"DEBUGGING TEXT: {text.title}")
        
        links = session.exec(
            select(TextWordLink)
            .where(TextWordLink.text_id == text_id)
            .order_by(TextWordLink.sentence_number, TextWordLink.position_in_sentence)
        ).all()
        
        current_sent = -1
        current_line = []
        
        print("\n--- RECONSTRUCTED STRUCTURE ---")
        for link in links:
            if link.sentence_number != current_sent:
                if current_sent != -1:
                    print(f"[Sent {current_sent}]: {' '.join(current_line)}")
                current_sent = link.sentence_number
                current_line = []
            
            current_line.append(f"{link.form}({link.position_in_sentence})")
            
        if current_line:
             print(f"[Sent {current_sent}]: {' '.join(current_line)}")

if __name__ == "__main__":
    debug_structure(1)
