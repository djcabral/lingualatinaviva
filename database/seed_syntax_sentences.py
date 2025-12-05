
import sys
import os
import json
from sqlmodel import select

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database import SentenceAnalysis, get_session

def seed_syntax_sentences():
    sentences_data = [
        # Lección 25: Coordinación
        {
            "latin_text": "Vincere aut mori.",
            "spanish_translation": "Vencer o morir.",
            "complexity_level": 2,
            "sentence_type": "compound",
            "source": "Lema Histórico",
            "lesson_number": 25,
            "constructions": json.dumps(["coordination"]),
            "dependency_json": json.dumps([
                {"id": 1, "text": "Vincere", "lemma": "vinco", "pos": "VERB", "dep": "ROOT", "head": 0},
                {"id": 2, "text": "aut", "lemma": "aut", "pos": "CCONJ", "dep": "cc", "head": 1},
                {"id": 3, "text": "mori", "lemma": "morior", "pos": "VERB", "dep": "conj", "head": 1},
                {"id": 4, "text": ".", "lemma": ".", "pos": "PUNCT", "dep": "punct", "head": 1}
            ])
        },
        {
            "latin_text": "Cogito, ergo sum.",
            "spanish_translation": "Pienso, luego existo.",
            "complexity_level": 3,
            "sentence_type": "compound",
            "source": "Descartes",
            "lesson_number": 25,
            "constructions": json.dumps(["coordination", "illative"]),
            "dependency_json": json.dumps([
                {"id": 1, "text": "Cogito", "lemma": "cogito", "pos": "VERB", "dep": "ROOT", "head": 0},
                {"id": 2, "text": ",", "lemma": ",", "pos": "PUNCT", "dep": "punct", "head": 1},
                {"id": 3, "text": "ergo", "lemma": "ergo", "pos": "ADV", "dep": "advmod", "head": 4},
                {"id": 4, "text": "sum", "lemma": "sum", "pos": "VERB", "dep": "conj", "head": 1},
                {"id": 5, "text": ".", "lemma": ".", "pos": "PUNCT", "dep": "punct", "head": 1}
            ])
        },
        # Lección 26: Sustantivas
        {
            "latin_text": "Dico te venire.",
            "spanish_translation": "Digo que vienes.",
            "complexity_level": 4,
            "sentence_type": "complex",
            "source": "Gramática",
            "lesson_number": 26,
            "constructions": json.dumps(["accusative_infinitive"]),
            "dependency_json": json.dumps([
                {"id": 1, "text": "Dico", "lemma": "dico", "pos": "VERB", "dep": "ROOT", "head": 0},
                {"id": 2, "text": "te", "lemma": "tu", "pos": "PRON", "dep": "nsubj", "head": 3},
                {"id": 3, "text": "venire", "lemma": "venio", "pos": "VERB", "dep": "ccomp", "head": 1},
                {"id": 4, "text": ".", "lemma": ".", "pos": "PUNCT", "dep": "punct", "head": 1}
            ])
        },
        {
            "latin_text": "Timeo ne pluat.",
            "spanish_translation": "Temo que llueva.",
            "complexity_level": 5,
            "sentence_type": "complex",
            "source": "Gramática",
            "lesson_number": 26,
            "constructions": json.dumps(["substantive_clause", "fear_clause"]),
            "dependency_json": json.dumps([
                {"id": 1, "text": "Timeo", "lemma": "timeo", "pos": "VERB", "dep": "ROOT", "head": 0},
                {"id": 2, "text": "ne", "lemma": "ne", "pos": "SCONJ", "dep": "mark", "head": 3},
                {"id": 3, "text": "pluat", "lemma": "pluo", "pos": "VERB", "dep": "ccomp", "head": 1},
                {"id": 4, "text": ".", "lemma": ".", "pos": "PUNCT", "dep": "punct", "head": 1}
            ])
        },
        # Lección 27: Condicionales
        {
            "latin_text": "Si vis pacem, para bellum.",
            "spanish_translation": "Si quieres la paz, prepara la guerra.",
            "complexity_level": 4,
            "sentence_type": "complex",
            "source": "Vegecio",
            "lesson_number": 27,
            "constructions": json.dumps(["conditional"]),
            "dependency_json": json.dumps([
                {"id": 1, "text": "Si", "lemma": "si", "pos": "SCONJ", "dep": "mark", "head": 2},
                {"id": 2, "text": "vis", "lemma": "volo", "pos": "VERB", "dep": "advcl", "head": 4},
                {"id": 3, "text": "pacem", "lemma": "pax", "pos": "NOUN", "dep": "obj", "head": 2},
                {"id": 4, "text": "para", "lemma": "paro", "pos": "VERB", "dep": "ROOT", "head": 0},
                {"id": 5, "text": "bellum", "lemma": "bellum", "pos": "NOUN", "dep": "obj", "head": 4},
                {"id": 6, "text": ".", "lemma": ".", "pos": "PUNCT", "dep": "punct", "head": 4}
            ])
        },
        # Lección 28: Relativas
        {
            "latin_text": "Puer, quem vides, amicus meus est.",
            "spanish_translation": "El niño, al cual ves, es mi amigo.",
            "complexity_level": 3,
            "sentence_type": "complex",
            "source": "Gramática",
            "lesson_number": 28,
            "constructions": json.dumps(["relative_clause"]),
            "dependency_json": json.dumps([
                {"id": 1, "text": "Puer", "lemma": "puer", "pos": "NOUN", "dep": "nsubj", "head": 6},
                {"id": 2, "text": ",", "lemma": ",", "pos": "PUNCT", "dep": "punct", "head": 4},
                {"id": 3, "text": "quem", "lemma": "qui", "pos": "PRON", "dep": "obj", "head": 4},
                {"id": 4, "text": "vides", "lemma": "video", "pos": "VERB", "dep": "acl:relcl", "head": 1},
                {"id": 5, "text": ",", "lemma": ",", "pos": "PUNCT", "dep": "punct", "head": 4},
                {"id": 6, "text": "amicus", "lemma": "amicus", "pos": "NOUN", "dep": "ROOT", "head": 0},
                {"id": 7, "text": "meus", "lemma": "meus", "pos": "ADJ", "dep": "amod", "head": 6},
                {"id": 8, "text": "est", "lemma": "sum", "pos": "VERB", "dep": "cop", "head": 6},
                {"id": 9, "text": ".", "lemma": ".", "pos": "PUNCT", "dep": "punct", "head": 6}
            ])
        },
        # Lección 29: Estilo Indirecto
        {
            "latin_text": "Dicit se Romanum esse.",
            "spanish_translation": "Dice que él es romano.",
            "complexity_level": 4,
            "sentence_type": "complex",
            "source": "Gramática",
            "lesson_number": 29,
            "constructions": json.dumps(["indirect_speech", "accusative_infinitive"]),
            "dependency_json": json.dumps([
                {"id": 1, "text": "Dicit", "lemma": "dico", "pos": "VERB", "dep": "ROOT", "head": 0},
                {"id": 2, "text": "se", "lemma": "se", "pos": "PRON", "dep": "nsubj", "head": 4},
                {"id": 3, "text": "Romanum", "lemma": "romanus", "pos": "ADJ", "dep": "obj", "head": 4},
                {"id": 4, "text": "esse", "lemma": "sum", "pos": "VERB", "dep": "ccomp", "head": 1},
                {"id": 5, "text": ".", "lemma": ".", "pos": "PUNCT", "dep": "punct", "head": 1}
            ])
        }
    ]

    with get_session() as session:
        count = 0
        for data in sentences_data:
            # Check if exists
            existing = session.exec(select(SentenceAnalysis).where(SentenceAnalysis.latin_text == data["latin_text"])).first()
            if not existing:
                sentence = SentenceAnalysis(**data)
                session.add(sentence)
                count += 1
                print(f"Added: {data['latin_text']}")
            else:
                # Update lesson number if missing
                if existing.lesson_number is None:
                    existing.lesson_number = data["lesson_number"]
                    session.add(existing)
                    print(f"Updated lesson for: {data['latin_text']}")
        
        session.commit()
        print(f"✓ Successfully processed {count} new sentences")

if __name__ == "__main__":
    seed_syntax_sentences()
