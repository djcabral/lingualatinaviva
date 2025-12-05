"""
Script adicional para completar vocabulario faltante.
L4 (13->15), L8 (13->15), L9 (11->15), L10 (12->15), L15 (13->15), L18 (12->15)
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database import get_session, Word, LessonVocabulary
from sqlmodel import select

EXTRA_VOCABULARY = {
    4: [  # 2ª Declinación - añadir 2 más
        ("campus", "campo/llanura", "noun", "campi", "masculino", "2"),
        ("numerus", "número", "noun", "numeri", "masculino", "2"),
    ],
    8: [  # 4ª Declinación - añadir 2 más
        ("fructus", "fruto/resultado", "noun", "fructus", "masculino", "4"),
        ("portus", "puerto", "noun", "portus", "masculino", "4"),
    ],
    9: [  # 5ª Declinación - añadir 4 más
        ("acies", "filo/línea de batalla", "noun", "aciei", "femenino", "5"),
        ("effigies", "imagen/retrato", "noun", "effigiei", "femenino", "5"),
        ("glacies", "hielo", "noun", "glaciei", "femenino", "5"),
        ("meridies", "mediodía", "noun", "meridiei", "masculino", "5"),
    ],
    10: [  # Adjetivos 2ª Clase - añadir 3 más
        ("gravis", "grave/pesado", "adjective", "gravis, grave", "masculino", "3"),
        ("nobilis", "noble", "adjective", "nobilis, nobile", "masculino", "3"),
        ("utilis", "útil", "adjective", "utilis, utile", "masculino", "3"),
    ],
    15: [  # Pasiva Infectum - añadir 2 más
        ("orno", "adornar/equipar", "verb", "orno, ornare, ornavi, ornatum", "1", None),
        ("narro", "narrar/contar", "verb", "narro, narrare, narravi, narratum", "1", None),
    ],
    18: [  # Subjuntivo I - añadir 3 más
        ("placet", "agrada/parece bien", "verb", "placet, placere, placuit", "2", "impersonal"),
        ("paenitet", "arrepentirse", "verb", "paenitet, paenitere, paenituit", "2", "impersonal"),
        ("pudet", "avergonzarse", "verb", "pudet, pudere, puduit", "2", "impersonal"),
    ],
}

def expand_remaining():
    print("🌱 Añadiendo vocabulario faltante...")
    added = 0
    
    with get_session() as session:
        for lesson_num, words in EXTRA_VOCABULARY.items():
            print(f"\n  📚 Lección {lesson_num}: +{len(words)} palabras")
            
            for i, word_data in enumerate(words):
                latin, trans, pos, gen_or_parts, gender, decl = word_data
                
                word = session.exec(select(Word).where(Word.latin == latin)).first()
                
                if not word:
                    if pos == "verb":
                        word = Word(latin=latin, translation=trans, part_of_speech=pos,
                                   principal_parts=gen_or_parts, conjugation=gender,
                                   definition_es=trans, level=lesson_num // 10 + 1)
                    else:
                        word = Word(latin=latin, translation=trans, part_of_speech=pos,
                                   genitive=gen_or_parts, gender=gender, declension=decl,
                                   definition_es=trans, level=lesson_num // 10 + 1)
                    session.add(word)
                    session.commit()
                    session.refresh(word)
                    print(f"    + {latin}")
                
                link = session.exec(
                    select(LessonVocabulary)
                    .where(LessonVocabulary.lesson_number == lesson_num,
                           LessonVocabulary.word_id == word.id)
                ).first()
                
                if not link:
                    max_order = session.exec(
                        select(LessonVocabulary.presentation_order)
                        .where(LessonVocabulary.lesson_number == lesson_num)
                        .order_by(LessonVocabulary.presentation_order.desc())
                    ).first() or 0
                    
                    link = LessonVocabulary(lesson_number=lesson_num, word_id=word.id,
                                           is_essential=True, presentation_order=max_order + 1 + i)
                    session.add(link)
                    added += 1
        
        session.commit()
    
    print(f"\n✅ Añadidas {added} asociaciones adicionales.")

if __name__ == "__main__":
    expand_remaining()
