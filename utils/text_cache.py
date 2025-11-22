"""
Nuevo analizador de texto para Lectio que prioriza análisis CLTK cacheado
"""

from database.models import TextWordLink, Word
from sqlmodel import select
import json


def get_text_analysis_from_cache(session, text_id: int):
    """
    Obtiene el análisis de un texto desde TextWordLink (si existe análisis CLTK)
    
    Returns:
        List[Dict] o None si no hay análisis cachillado
    """
    links = session.exec(
        select(TextWordLink)
        .where(TextWordLink.text_id == text_id)
        .order_by(TextWordLink.position_in_sentence)
    ).all()
    
    if not links:
        return None
    
    analyses = []
    for link in links:
        # Construir análisis desde TextWordLink
        analysis = {
            "form": link.form,
            "position": link.position_in_sentence,
            "is_punctuation": is_punctuation(link.form) if link.form else False
        }
        
        # Si tiene word_id, obtener datos del vocabulario
        if link.word_id:
            word = link.word
            analysis["word_id"] = word.id
            analysis["lemma"] = word.latin
            analysis["translation"] = word.translation
            analysis["pos"] = word.part_of_speech
            
            # Morfología desde JSON o vacío
            if link.morphology_json:
                analysis["morphology"] = json.loads(link.morphology_json)
            else:
                analysis["morphology"] = {}
        else:
            # Palabra no en vocabulario - leer desde notes (análisis CLTK)
            if link.notes:
                try:
                    notes_data = json.loads(link.notes)
                    analysis["lemma"] = notes_data.get("lemma", link.form)
                    analysis["pos"] = notes_data.get("pos", "unknown")
                    analysis["translation"] = f"({notes_data.get('lemma', link.form)})"
                    analysis["word_id"] = None
                except:
                    analysis["lemma"] = link.form
                    analysis["pos"] = "unknown"
                    analysis["translation"] = "(?)"
                    analysis["word_id"] = None
            else:
                analysis["lemma"] = link.form
                analysis["pos"] = "unknown"
                analysis["translation"] = "(?)"
                analysis["word_id"] = None
            
            # Morfología desde JSON
            if link.morphology_json:
                analysis["morphology"] = json.loads(link.morphology_json)
            else:
                analysis["morphology"] = {}
        
        analyses.append(analysis)
    
    return analyses


def is_punctuation(text: str) -> bool:
    """Verifica si el texto es puntuación"""
    if not text:
        return False
    return text.strip() in '.,;:!?-—()[]{}""\'\'«»'
