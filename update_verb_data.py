"""
Script para corregir las partes principales de los verbos en la base de datos
"""

from database.connection import get_session
from database import Word
from sqlmodel import select

# Partes principales completas de verbos comunes
VERB_PRINCIPAL_PARTS = {
    "amo": "amo, amare, amavi, amatum",
    "moneo": "moneo, monere, monui, monitum",
    "rego": "rego, regere, rexi, rectum",
    "audio": "audio, audire, audivi, auditum",
    "capio": "capio, capere, cepi, captum",
    "sum": "sum, esse, fui, futurus",
    "possum": "possum, posse, potui, —",
    "facio": "facio, facere, feci, factum",
    "dico": "dico, dicere, dixi, dictum",
    "video": "video, videre, vidi, visum",
    "venio": "venio, venire, veni, ventum",
    "do": "do, dare, dedi, datum",
}

def fix_verb_parts():
    """Corrige las partes principales de verbos en la BD"""
    
    print("=== Corrigiendo partes principales de verbos ===\n")
    
    with get_session() as session:
        verbs = session.exec(select(Word).where(Word.part_of_speech == "verb")).all()
        
        updated_count = 0
        for verb in verbs:
            if verb.latin in VERB_PRINCIPAL_PARTS:
                old_parts = verb.principal_parts
                new_parts = VERB_PRINCIPAL_PARTS[verb.latin]
                
                if old_parts != new_parts:
                    verb.principal_parts = new_parts
                    session.add(verb)
                    updated_count += 1
                    print(f"✓ {verb.latin}")
                    print(f"  Anterior: {old_parts}")
                    print(f"  Nuevo:    {new_parts}\n")
        
        session.commit()
        
        print(f"✅ {updated_count} verbos actualizados")

if __name__ == "__main__":
    fix_verb_parts()
