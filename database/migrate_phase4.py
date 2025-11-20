"""
Script de Migración Fase 4: Adverbios y Expansión de Lectio

1. Inserta adverbios y palabras invariables comunes.
2. Añade textos para el módulo Lectio.
3. Asegura que todo el vocabulario de los textos esté en la base de datos.
"""

from database.connection import get_session
from database.models import Word, Text, TextWordLink
from sqlmodel import select
import re
import unicodedata

def normalize_latin(text):
    """Remove macrons and diacritics for matching"""
    normalized = unicodedata.normalize('NFD', text)
    return ''.join(char for char in normalized if unicodedata.category(char) != 'Mn')

def migrate_phase4():
    print("\n4. Insertando adverbios y textos de Lectio...")
    
    # 1. Adverbios y Palabras Invariables
    invariables = [
        {"latin": "nōn", "translation": "no", "part_of_speech": "adverb", "level": 1, "category": "adverb", "is_invariable": True},
        {"latin": "et", "translation": "y", "part_of_speech": "conjunction", "level": 1, "category": "conjunction", "is_invariable": True},
        {"latin": "sed", "translation": "pero, sino", "part_of_speech": "conjunction", "level": 1, "category": "conjunction", "is_invariable": True},
        {"latin": "in", "translation": "en, dentro de (con abl.); a, hacia (con ac.)", "part_of_speech": "preposition", "level": 1, "category": "preposition", "is_invariable": True},
        {"latin": "cum", "translation": "con (con abl.)", "part_of_speech": "preposition", "level": 1, "category": "preposition", "is_invariable": True},
        {"latin": "sine", "translation": "sin (con abl.)", "part_of_speech": "preposition", "level": 1, "category": "preposition", "is_invariable": True},
        {"latin": "ab", "translation": "de, desde, por (con abl.)", "part_of_speech": "preposition", "level": 1, "category": "preposition", "is_invariable": True},
        {"latin": "ad", "translation": "a, hacia, junto a (con ac.)", "part_of_speech": "preposition", "level": 1, "category": "preposition", "is_invariable": True},
        {"latin": "ex", "translation": "de, desde, fuera de (con abl.)", "part_of_speech": "preposition", "level": 1, "category": "preposition", "is_invariable": True},
        
        {"latin": "semper", "translation": "siempre", "part_of_speech": "adverb", "level": 1, "category": "adverb", "is_invariable": True},
        {"latin": "numquam", "translation": "nunca", "part_of_speech": "adverb", "level": 1, "category": "adverb", "is_invariable": True},
        {"latin": "saepe", "translation": "a menudo", "part_of_speech": "adverb", "level": 1, "category": "adverb", "is_invariable": True},
        {"latin": "nunc", "translation": "ahora", "part_of_speech": "adverb", "level": 1, "category": "adverb", "is_invariable": True},
        {"latin": "tunc", "translation": "entonces", "part_of_speech": "adverb", "level": 1, "category": "adverb", "is_invariable": True},
        {"latin": "hīc", "translation": "aquí", "part_of_speech": "adverb", "level": 1, "category": "adverb", "is_invariable": True},
        {"latin": "ibi", "translation": "allí", "part_of_speech": "adverb", "level": 1, "category": "adverb", "is_invariable": True},
        {"latin": "ubi", "translation": "dónde, donde", "part_of_speech": "adverb", "level": 1, "category": "adverb", "is_invariable": True},
        {"latin": "cūr", "translation": "por qué", "part_of_speech": "adverb", "level": 1, "category": "adverb", "is_invariable": True},
        {"latin": "quōmodo", "translation": "cómo", "part_of_speech": "adverb", "level": 1, "category": "adverb", "is_invariable": True},
        {"latin": "bene", "translation": "bien", "part_of_speech": "adverb", "level": 1, "category": "adverb", "is_invariable": True},
        {"latin": "male", "translation": "mal", "part_of_speech": "adverb", "level": 1, "category": "adverb", "is_invariable": True},
        {"latin": "quoque", "translation": "también", "part_of_speech": "adverb", "level": 1, "category": "adverb", "is_invariable": True},
        {"latin": "etiam", "translation": "también, incluso", "part_of_speech": "adverb", "level": 1, "category": "adverb", "is_invariable": True},
        {"latin": "tam", "translation": "tan", "part_of_speech": "adverb", "level": 1, "category": "adverb", "is_invariable": True},
        {"latin": "quam", "translation": "que, como (comparativo)", "part_of_speech": "adverb", "level": 1, "category": "adverb", "is_invariable": True}
    ]

    # 2. Vocabulario Adicional para Textos
    # Palabras que aparecerán en los textos y necesitamos definir
    text_vocab = [
        {"latin": "Rōma", "translation": "Roma", "part_of_speech": "noun", "genitive": "Rōmae", "gender": "f", "declension": "1", "level": 1},
        {"latin": "Italia", "translation": "Italia", "part_of_speech": "noun", "genitive": "Italiae", "gender": "f", "declension": "1", "level": 1},
        {"latin": "Eurōpa", "translation": "Europa", "part_of_speech": "noun", "genitive": "Eurōpae", "gender": "f", "declension": "1", "level": 1},
        {"latin": "Graecia", "translation": "Grecia", "part_of_speech": "noun", "genitive": "Graeciae", "gender": "f", "declension": "1", "level": 1},
        {"latin": "Hispānia", "translation": "España", "part_of_speech": "noun", "genitive": "Hispāniae", "gender": "f", "declension": "1", "level": 1},
        {"latin": "Aegyptus", "translation": "Egipto", "part_of_speech": "noun", "genitive": "Aegyptī", "gender": "f", "declension": "2", "level": 1}, # Femenino 2da!
        {"latin": "Africa", "translation": "África", "part_of_speech": "noun", "genitive": "Africae", "gender": "f", "declension": "1", "level": 1},
        {"latin": "Gallia", "translation": "Galia (Francia)", "part_of_speech": "noun", "genitive": "Galliae", "gender": "f", "declension": "1", "level": 1},
        {"latin": "Asia", "translation": "Asia", "part_of_speech": "noun", "genitive": "Asiae", "gender": "f", "declension": "1", "level": 1},
        {"latin": "Rhēnus", "translation": "Rin (río)", "part_of_speech": "noun", "genitive": "Rhēnī", "gender": "m", "declension": "2", "level": 1},
        {"latin": "Nīlus", "translation": "Nilo (río)", "part_of_speech": "noun", "genitive": "Nīlī", "gender": "m", "declension": "2", "level": 1},
        {"latin": "fluvius", "translation": "río", "part_of_speech": "noun", "genitive": "fluviī", "gender": "m", "declension": "2", "level": 1},
        {"latin": "īnsula", "translation": "isla", "part_of_speech": "noun", "genitive": "īnsulae", "gender": "f", "declension": "1", "level": 1},
        {"latin": "oppidum", "translation": "ciudad, pueblo fortificado", "part_of_speech": "noun", "genitive": "oppidī", "gender": "n", "declension": "2", "level": 1},
        {"latin": "magnus", "translation": "grande", "part_of_speech": "adjective", "level": 1, "category": "adjective"},
        {"latin": "parvus", "translation": "pequeño", "part_of_speech": "adjective", "level": 1, "category": "adjective"},
        {"latin": "multus", "translation": "mucho", "part_of_speech": "adjective", "level": 1, "category": "adjective"},
        {"latin": "paucus", "translation": "poco", "part_of_speech": "adjective", "level": 1, "category": "adjective"},
        
        # Familia
        {"latin": "Iūlius", "translation": "Julio", "part_of_speech": "noun", "genitive": "Iūliī", "gender": "m", "declension": "2", "level": 1},
        {"latin": "Aemilia", "translation": "Emilia", "part_of_speech": "noun", "genitive": "Aemiliae", "gender": "f", "declension": "1", "level": 1},
        {"latin": "Mārcus", "translation": "Marco", "part_of_speech": "noun", "genitive": "Mārcī", "gender": "m", "declension": "2", "level": 1},
        {"latin": "Quīntus", "translation": "Quinto", "part_of_speech": "noun", "genitive": "Quīntī", "gender": "m", "declension": "2", "level": 1},
        {"latin": "Iūlia", "translation": "Julia", "part_of_speech": "noun", "genitive": "Iūliae", "gender": "f", "declension": "1", "level": 1},
        {"latin": "liberī", "translation": "hijos (plural)", "part_of_speech": "noun", "genitive": "liberōrum", "gender": "m", "declension": "2", "level": 1},
        {"latin": "centum", "translation": "cien", "part_of_speech": "adjective", "level": 1, "category": "numeral", "is_invariable": True},
        {"latin": "ūnus", "translation": "uno", "part_of_speech": "adjective", "level": 1, "category": "numeral"},
        {"latin": "duo", "translation": "dos", "part_of_speech": "adjective", "level": 1, "category": "numeral"},
        {"latin": "trēs", "translation": "tres", "part_of_speech": "adjective", "level": 1, "category": "numeral"}
    ]

    # 3. Textos
    texts = [
        {
            "title": "Imperium Rōmānum",
            "content": """Rōma in Italiā est. Italia in Eurōpā est. Graecia in Eurōpā est. Italia et Graecia in Eurōpā sunt. Hispānia quoque in Eurōpā est. Hispānia et Italia et Graecia in Eurōpā sunt.
Aegyptus in Eurōpā nōn est, Aegyptus in Āfricā est. Gallia nōn in Āfricā est, Gallia est in Eurōpā. Syria nōn est in Eurōpā, sed in Asiā. Arabia quoque in Asiā est. Syria et Arabia in Asiā sunt. Germānia nōn in Asiā, sed in Eurōpā est. Britannia quoque in Eurōpā est. Germānia et Britannia sunt in Eurōpā.
Estne Gallia in Eurōpā? Gallia in Eurōpā est. Estne Rōma in Galliā? Rōma in Galliā nōn est. Ubi est Rōma? Rōma est in Italiā. Ubi est Italia? Italia in Eurōpā est. Ubi sunt Gallia et Hispānia? Gallia et Hispānia in Eurōpā sunt.
Estne Nīlus in Eurōpā? Nīlus in Eurōpā nōn est. Ubi est Nīlus? Nīlus in Āfricā est. Rhēnus ubi est? Rhēnus est in Germāniā. Nīlus fluvius est. Rhēnus fluvius est. Nīlus et Rhēnus fluviī sunt. Dānuvius quoque fluvius est. Rhēnus et Dānuvius sunt fluviī in Germāniā. Tiberis fluvius in Italiā est.
Nīlus fluvius magnus est. Tiberis nōn est fluvius magnus, Tiberis fluvius parvus est. Rhēnus nōn est fluvius parvus, sed fluvius magnus. Nīlus et Rhēnus fluviī magnī sunt. Dānuvius quoque fluvius magnus est.
Corsica īnsula est. Corsica et Sardinia et Sicilia īnsulae sunt. Britannia quoque īnsula est. Italia īnsula nōn est. Sicilia īnsula magna est. Melita est īnsula parva. Britannia nōn īnsula parva, sed īnsula magna est. Sicilia et Sardinia nōn īnsulae parvae, sed īnsulae magnae sunt.
Brundisium oppidum est. Brundisium et Tūsculum oppida sunt. Sparta quoque oppidum est. Brundisium est oppidum magnum. Tūsculum oppidum parvum est. Delphī quoque oppidum parvum est. Tūsculum et Delphī nōn oppida magna, sed oppida parva sunt. Ubi est Sparta? Sparta est in Graeciā. Sparta, Delphī, Athēnae oppida Graeca sunt.""",
            "level": 1,
            "difficulty": 1
        },
        {
            "title": "Familia Rōmāna",
            "content": """Iūlius vir Rōmānus est. Aemilia fēmina Rōmāna est. Mārcus est puer Rōmānus. Quīntus quoque puer Rōmānus est. Iūlia est puella Rōmāna.
Mārcus et Quīntus nōn virī, sed puerī sunt. Virī sunt Iūlius et Mēdus et Dāvus. Aemilia et Dēlia et Syra sunt fēminae. Estne Iūlia fēmina? Nōn fēmina, sed puella est Iūlia.
Iūlius Aemiliam amat. Aemilia Iūlium amat. Iūlius et Aemilia līberōs suōs amant. Mārcus et Quīntus et Iūlia sunt līberī Iūliī et Aemiliae.
In familiā Iūliī sunt trēs līberī: duo puerī et ūna puella. Numerus līberōrum est trēs.
Centum servī in familiā sunt. Iūlius dominus est. Aemilia domina est. Iūlius dominus servōrum est. Dāvus servus est. Mēdus quoque servus est. Dāvus et Mēdus servī sunt. Iūlius dominus Dāvī et Mēdī est. Iūlius dominus servōrum est et pater līberōrum est.
Aemilia domina ancillārum est. Syra ancilla est. Dēlia quoque ancilla est. Syra et Dēlia ancillae sunt. Aemilia domina Syrae et Dēliae est.""",
            "level": 1,
            "difficulty": 1
        }
    ]

    with get_session() as session:
        # 1. Insert Invariables
        count_inv = 0
        for data in invariables:
            existing = session.exec(select(Word).where(Word.latin == data["latin"])).first()
            if not existing:
                word = Word(**data)
                session.add(word)
                count_inv += 1
        
        # 2. Insert Text Vocabulary
        count_vocab = 0
        for data in text_vocab:
            existing = session.exec(select(Word).where(Word.latin == data["latin"])).first()
            if not existing:
                word = Word(**data)
                session.add(word)
                count_vocab += 1
        
        session.commit()
        
        # 3. Insert Texts and Link Words
        count_text = 0
        all_words = session.exec(select(Word)).all()
        
        for text_data in texts:
            existing_text = session.exec(select(Text).where(Text.title == text_data["title"])).first()
            if not existing_text:
                new_text = Text(
                    title=text_data["title"],
                    content=text_data["content"],
                    level=text_data["level"],
                    difficulty=text_data["difficulty"]
                )
                session.add(new_text)
                session.commit()
                session.refresh(new_text)
                count_text += 1
                
                # Auto-link words
                words_in_text = re.findall(r'[a-zA-ZāēīōūĀĒĪŌŪ]+', text_data["content"].lower())
                word_freq = {}
                for w in words_in_text:
                    normalized_w = normalize_latin(w)
                    word_freq[normalized_w] = word_freq.get(normalized_w, 0) + 1
                
                for text_word, freq in word_freq.items():
                    for db_word in all_words:
                        if normalize_latin(db_word.latin.lower()) == text_word:
                            link = TextWordLink(
                                text_id=new_text.id,
                                word_id=db_word.id,
                                frequency=freq
                            )
                            session.add(link)
                            break
                session.commit()

        print(f"\n✅ Migración Fase 4 completada.")
        print(f"   - Adverbios/Invariables: {count_inv}")
        print(f"   - Vocabulario de Textos: {count_vocab}")
        print(f"   - Textos Nuevos: {count_text}")

if __name__ == "__main__":
    migrate_phase4()
