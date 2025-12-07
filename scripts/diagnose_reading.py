"""
Diagnóstico de TextWordLink para identificar problemas de sincronización
"""
import sys
import os
sys.path.append(os.getcwd())

from database.connection import get_session
from database import Text, TextWordLink, Word
from sqlmodel import select

def diagnose_text(title_search: str = "Roma"):
    """Diagnostica los TextWordLinks de un texto específico"""
    
    with get_session() as session:
        # Find the text
        text = session.exec(
            select(Text).where(Text.title.contains(title_search))
        ).first()
        
        if not text:
            print(f"❌ No se encontró texto con '{title_search}' en el título")
            return
        
        print(f"📖 Texto: {text.title} (ID: {text.id})")
        print(f"📝 Contenido:\n{text.content}\n")
        print("-" * 80)
        
        # Get tokenized words from content
        import re
        content_tokens = re.findall(r"[\w']+|[.,!?;:]", text.content)
        print(f"🔤 Tokens en el contenido: {len(content_tokens)}")
        print(f"   {content_tokens[:20]}... \n")
        
        # Get TextWordLinks
        links = session.exec(
            select(TextWordLink)
            .where(TextWordLink.text_id == text.id)
            .order_by(TextWordLink.sentence_number, TextWordLink.position_in_sentence)
        ).all()
        
        print(f"🔗 TextWordLinks encontrados: {len(links)}\n")
        
        if not links:
            print("❌ No hay TextWordLinks para este texto!")
            return
        
        print("=" * 100)
        print(f"{'#':>3} | {'Sent':>4} | {'Pos':>3} | {'Form (in link)':<15} | {'Word.latin':<15} | {'Word.translation':<25} | {'Match?'}")
        print("=" * 100)
        
        mismatches = []
        
        for i, link in enumerate(links):
            form_in_link = link.form if link.form else "(none)"
            
            if link.word_id:
                word = link.word
                word_latin = word.latin if word else "(NO WORD)"
                word_trans = (word.translation[:22] + "...") if word and word.translation and len(word.translation) > 25 else (word.translation if word else "-")
                
                # Check if form matches lemma (approximately)
                form_lower = form_in_link.lower()
                latin_lower = word_latin.lower() if word_latin else ""
                
                # Forms should be related (either same or derived)
                match = "✓" if form_lower == latin_lower or form_lower.startswith(latin_lower[:3]) or latin_lower.startswith(form_lower[:3]) else "⚠️"
                
                if match == "⚠️":
                    mismatches.append((form_in_link, word_latin, word_trans))
            else:
                word_latin = "(no word_id)"
                word_trans = "-"
                match = "?"
            
            print(f"{i+1:>3} | {link.sentence_number:>4} | {link.position_in_sentence:>3} | {form_in_link:<15} | {word_latin:<15} | {word_trans:<25} | {match}")
        
        print("=" * 100)
        
        if mismatches:
            print(f"\n⚠️ POSIBLES DESAJUSTES DETECTADOS ({len(mismatches)}):")
            for form, latin, trans in mismatches:
                print(f"   - Form '{form}' → Word.latin '{latin}' ({trans})")
        else:
            print("\n✅ No se detectaron desajustes obvios.")


if __name__ == "__main__":
    import sys
    search = sys.argv[1] if len(sys.argv) > 1 else "Roma"
    diagnose_text(search)
