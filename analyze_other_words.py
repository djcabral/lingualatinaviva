"""
Script para identificar y corregir palabras con tipo 'other' o tipos incorrectos
"""

from database.connection import get_session
from database.models import Word
from sqlmodel import select

def analyze_other_words():
    """Analiza palabras con tipo 'other' y sugiere correcciones"""
    
    with get_session() as session:
        # Buscar todas las palabras con 'other'
        other_words = session.exec(
            select(Word)
            .where(Word.part_of_speech == 'other')
            .order_by(Word.frequency_rank_global)
        ).all()
        
        print(f"\n📊 Encontradas {len(other_words)} palabras con tipo 'other'\n")
        print("="*80)
        
        # Clasificar automáticamente algunas basándose en patrones
        suggestions = {
            'verb': [],
            'noun': [],
            'adjective': [],
           'adverb': [],
            'preposition': [],
            'conjunction': [],
            'pronoun': [],
            'numeral': [],
            'interjection': []
        }
        
        for word in other_words[:50]:  # Analizar primeras 50
            latin = word.latin.lower()
            
            # Patrones para detectar tipo
            suggested_type = None
            
            # Verbos: tienen partes principales o conjugación
            if word.principal_parts or word.conjugation:
                suggested_type = 'verb'
            
            # Sustantivos: tienen genitivo o declinación
            elif word.genitive or word.declension:
                suggested_type = 'noun'
            
            # Adverbios: terminaciones típicas
            elif any(latin.endswith(suffix) for suffix in ['e', 'ter', 'iter', 'im']):
                if not word.genitive:  # No es sustantivo
                    suggested_type = 'adverb'
            
            # Preposiciones comunes
            elif latin in ['ad', 'ab', 'de', 'ex', 'in', 'cum', 'pro', 'per', 'inter', 'sub', 'super']:
                suggested_type = 'preposition'
            
            # Conjunciones comunes
            elif latin in ['et', 'sed', 'aut', 'vel', 'si', 'nisi', 'quia', 'quod', 'ut', 'ne', 'dum']:
                suggested_type = 'conjunction'
            
            # Pronombres comunes
            elif latin in ['ego', 'tu', 'is', 'qui', 'quis', 'hic', 'ille', 'ipse', 'se']:
                suggested_type = 'pronoun'
            
            # Numerales
            elif latin in ['unus', 'duo', 'tres', 'primus', 'secundus'] or any(c.isdigit() for c in latin):
                suggested_type = 'numeral'
            
            # Interjecciones
            elif latin in ['o', 'heu', 'eia', 'ecce']:
                suggested_type = 'interjection'
            
            if suggested_type:
                suggestions[suggested_type].append((word.id, word.latin, word.translation))
        
        # Mostrar sugerencias
        print("\n🔍 SUGERENCIAS DE RECLASIFICACIÓN:\n")
        for pos_type, words in suggestions.items():
            if words:
                print(f"\n{pos_type.upper()}:")
                for wid, latin, trans in words[:10]:
                    print(f"  [{wid:5}] {latin:20} → {trans[:40]}")
        
        # Palabras que necesitan revisión manual
        print("\n\n⚠️  PALABRAS QUE NECESITAN REVISIÓN MANUAL:\n")
        print("(Primeras 20 por frecuencia)\n")
        
        for word in other_words[:20]:
            has_info = []
            if word.principal_parts:
                has_info.append(f"parts: {word.principal_parts}")
            if word.genitive:
                has_info.append(f"gen: {word.genitive}")
            if word.declension:
                has_info.append(f"decl: {word.declension}")
            if word.conjugation:
                has_info.append(f"conj: {word.conjugation}")
            
            info_str = " | ".join(has_info) if has_info else "sin info morfológica"
            
            print(f"[{word.id:5}] {word.latin:20} → {word.translation[:30]:30} | {info_str}")

def fix_word_type(word_id: int, new_type: str):
    """Corrige el tipo de una palabra específica"""
    valid_types = ['noun', 'verb', 'adjective', 'adverb', 'preposition', 
                   'conjunction', 'pronoun', 'numeral', 'interjection', 'particle']
    
    if new_type not in valid_types:
        print(f"❌ Tipo inválido: {new_type}")
        print(f"   Tipos válidos: {', '.join(valid_types)}")
        return
    
    with get_session() as session:
        word = session.get(Word, word_id)
        if word:
            old_type = word.part_of_speech
            word.part_of_speech = new_type
            session.add(word)
            session.commit()
            print(f"✅ Actualizado: {word.latin} ({old_type} → {new_type})")
        else:
            print(f"❌ Palabra no encontrada: ID {word_id}")

def batch_fix(word_ids: list, new_type: str):
    """Corrige múltiples palabras a la vez"""
    with get_session() as session:
        for word_id in word_ids:
            word = session.get(Word, word_id)
            if word:
                word.part_of_speech = new_type
                session.add(word)
        session.commit()
    
    print(f"✅ Actualizadas {len(word_ids)} palabras a tipo '{new_type}'")

if __name__ == "__main__":
    print("🔧 Analizador de Palabras 'Other'\n")
    analyze_other_words()
    
    print("\n\n" + "="*80)
    print("\n📝 CÓMO USAR ESTE SCRIPT:\n")
    print("1. Ejecuta este script para ver sugerencias")
    print("2. Para corregir una palabra:")
    print("   from analyze_other_words import fix_word_type")
    print("   fix_word_type(123, 'adverb')  # ID, nuevo_tipo")
    print("\n3. Para correcciones en lote:")
    print("   from analyze_other_words import batch_fix")
    print("   batch_fix([1, 2, 3, 4], 'preposition')")
    print("\n")
