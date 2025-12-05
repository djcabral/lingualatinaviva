from database import get_session, Word, LessonVocabulary
from sqlmodel import select
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def check_incomplete_words():
    with get_session() as session:
        # Buscar palabras en TODAS las lecciones con datos incompletos
        statement = (
            select(Word, LessonVocabulary)
            .join(LessonVocabulary, Word.id == LessonVocabulary.word_id)
            .order_by(LessonVocabulary.lesson_number, LessonVocabulary.presentation_order)
        )
        
        results = session.exec(statement).all()
        
        print(f'Total palabras en base de datos: {len(results)}\n')
        
        incomplete = []
        
        for word, vocab in results:
            issues = []
            
            if word.part_of_speech == 'verb':
                if not word.principal_parts or word.principal_parts == 'N/A':
                    issues.append('sin partes principales')
                if not word.conjugation or word.conjugation == 'N/A':
                    issues.append('sin conjugación')
            elif word.part_of_speech == 'noun':
                if not word.genitive or word.genitive == 'N/A':
                    issues.append('sin genitivo')
                if not word.gender or word.gender == 'N/A':
                    issues.append('sin género')
                if not word.declension or word.declension == 'N/A':
                    issues.append('sin declinación')
            elif word.part_of_speech == 'adjective':
                if not word.declension or word.declension == 'N/A':
                    issues.append('sin declinación')
            
            if issues:
                incomplete.append({
                    'lesson': vocab.lesson_number,
                    'word': word.latin,
                    'pos': word.part_of_speech,
                    'translation': word.translation,
                    'issues': issues
                })
        
        if incomplete:
            print('PALABRAS CON INFORMACIÓN INCOMPLETA:\n')
            for item in incomplete:
                print(f"L{item['lesson']}: {item['word']} ({item['pos']}) - {item['translation']}")
                print(f"  Falta: {', '.join(item['issues'])}\n")
        else:
            print('✓ Todas las palabras están completas according to the check.')
            
        # Debug: Print ALL verbs to find the culprit
        print("\nDEBUG: LISTADO COMPLETO DE VERBOS (L1-L5):")
        verbs = [w for w, v in results if w.part_of_speech == 'verb']
        for v in verbs:
            print(f"L{next(vocab.lesson_number for w, vocab in results if w.id == v.id)}: {v.latin} ({v.translation})")
            print(f"   -> PP: '{v.principal_parts}' | Conj: '{v.conjugation}'")
            
        print("\nDEBUG: Muestra de sustantivos:")
        nouns = [w for w, v in results if w.part_of_speech == 'noun'][:5]
        for n in nouns:
            print(f"Sustantivo: {n.latin}")
            print(f"  Genitive: '{n.genitive}'")
            print(f"  Gender: '{n.gender}'")
            print(f"  Declension: '{n.declension}'")

if __name__ == "__main__":
    check_incomplete_words()
