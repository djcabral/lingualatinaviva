#!/usr/bin/env python3
"""
Script de Población - Etapa 3: Vocabulario por Lección
Mapea el vocabulario esencial a las Lecciones 1-5.
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.connection import get_session
from database import Word, LessonVocabulary
from sqlmodel import select

def seed_lesson_vocabulary():
    print("🌱 Mapeando vocabulario esencial a Lecciones 1-10...")
    
    # Vocabulario organizado por lección
    # Usamos las palabras latinas para buscarlas en la BD
    vocab_mapping = {
        # LECCIÓN 1: 1ª y 2ª Declinación básica
        1: {
            "nouns": ["rosa", "puella", "femina", "dominus", "servus", "puer", "templum", "bellum"],
            "verbs": ["amo", "sum"],
        },
        
        # LECCIÓN 2: Genitivo y Dativo
        2: {
            "nouns": ["nauta", "poeta"],
            "verbs": ["do", "laudo", "habeo"],
        },
        
        # LECCIÓN 3: Ablativo
        3: {
            "nouns": ["ager"],
            "verbs": ["porto", "voco"],
        },
        
        # LECCIÓN 4: Presente Indicativo
        4: {
            "nouns": [],
            "verbs": ["moneo", "video", "timeo", "debeo", "pugno"],
        },
        
        # LECCIÓN 5: 3ª Declinación
        5: {
            "nouns": ["rex", "miles", "corpus", "urbs"],
            "verbs": ["rego", "duco", "mitto"],
        },
        
        # LECCIÓN 6: Consolidación y Adjetivos
        6: {
            "nouns": ["victoria", "gloria", "fortuna", "memoria"],
            "verbs": ["vinco", "credo", "paro"],
            "adjectives": ["bonus", "magnus", "pulcher", "liber"],
        },
        
        # LECCIÓN 7: 3ª Declinación y Dativo
        7: {
            "nouns": ["lex", "pax", "dux", "lux", "nox"],
            "verbs": ["ago", "dico", "facio", "capio"],
        },
        
        # LECCIÓN 8: 4ª Declinación y Pasado
        8: {
            "nouns": ["manus", "exercitus", "domus", "fructus"],
            "verbs": ["sum", "habeo", "venio"], # Usamos lemas, no formas conjugadas (fui, habui, veni)
        },
        
        # LECCIÓN 9: 5ª Declinación y Futuro
        9: {
            "nouns": ["res", "dies", "spes", "fides"],
            "verbs": ["sum", "habeo", "venio"], # Usamos lemas (ero, habebo, veniam)
        },
        
        # LECCIÓN 10: Adjetivos de 2ª Clase
        10: {
            "adjectives": ["tristis", "fortis", "brevis", "acer", "facilis"],
        },
    }
    
    with get_session() as session:
        added = 0
        skipped = 0
        
        for lesson_num, vocab in vocab_mapping.items():
            presentation_order = 1
            
            # Process nouns
            for latin_word in vocab.get("nouns", []):
                word = session.exec(
                    select(Word).where(
                        Word.latin == latin_word,
                        Word.part_of_speech == "noun"
                    )
                ).first()
                
                if word:
                    # Check if already mapped
                    existing = session.exec(
                        select(LessonVocabulary).where(
                            LessonVocabulary.lesson_number == lesson_num,
                            LessonVocabulary.word_id == word.id
                        )
                    ).first()
                    
                    if not existing:
                        lesson_vocab = LessonVocabulary(
                            lesson_number=lesson_num,
                            word_id=word.id,
                            is_essential=True,
                            is_secondary=False,
                            presentation_order=presentation_order,
                            notes=f"Vocabulario esencial de Lección {lesson_num}"
                        )
                        session.add(lesson_vocab)
                        added += 1
                        presentation_order += 1
                    else:
                        skipped += 1
                else:
                    print(f"   ⚠️  Palabra no encontrada: {latin_word} (noun)")
            
            # Process verbs
            for latin_word in vocab.get("verbs", []):
                word = session.exec(
                    select(Word).where(
                        Word.latin == latin_word,
                        Word.part_of_speech == "verb"
                    )
                ).first()
                
                if word:
                    # Check if already mapped
                    existing = session.exec(
                        select(LessonVocabulary).where(
                            LessonVocabulary.lesson_number == lesson_num,
                            LessonVocabulary.word_id == word.id
                        )
                    ).first()
                    
                    if not existing:
                        lesson_vocab = LessonVocabulary(
                            lesson_number=lesson_num,
                            word_id=word.id,
                            is_essential=True,
                            is_secondary=False,
                            presentation_order=presentation_order,
                            notes=f"Vocabulario esencial de Lección {lesson_num}"
                        )
                        session.add(lesson_vocab)
                        added += 1
                        presentation_order += 1
                    else:
                        skipped += 1
                else:
                    print(f"   ⚠️  Palabra no encontrada: {latin_word} (verb)")
            
            # Process adjectives (if present)
            if "adjectives" in vocab:
                for latin_word in vocab["adjectives"]:
                    word = session.exec(
                        select(Word).where(
                            Word.latin == latin_word,
                            Word.part_of_speech == "adjective"
                        )
                    ).first()
                    
                    if word:
                        # Check if already mapped
                        existing = session.exec(
                            select(LessonVocabulary).where(
                                LessonVocabulary.lesson_number == lesson_num,
                                LessonVocabulary.word_id == word.id
                            )
                        ).first()
                        
                        if not existing:
                            lesson_vocab = LessonVocabulary(
                                lesson_number=lesson_num,
                                word_id=word.id,
                                is_essential=True,
                                is_secondary=False,
                                presentation_order=presentation_order,
                                notes=f"Vocabulario esencial de Lección {lesson_num}"
                            )
                            session.add(lesson_vocab)
                            added += 1
                            presentation_order += 1
                        else:
                            skipped += 1
                    else:
                        print(f"   ⚠️  Palabra no encontrada: {latin_word} (adjective)")
        
        session.commit()
        
        print(f"✅ Mapeos de vocabulario creados: {added}")
        print(f"ℹ️  Mapeos ya existentes: {skipped}")
        
        # Summary by lesson
        print("\n📊 Resumen por Lección:")
        for lesson_num in range(1, 11):
            count = len(session.exec(
                select(LessonVocabulary).where(
                    LessonVocabulary.lesson_number == lesson_num
                )
            ).all())
            print(f"   Lección {lesson_num}: {count} palabras esenciales")

if __name__ == "__main__":
    seed_lesson_vocabulary()
