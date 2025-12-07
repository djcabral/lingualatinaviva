
import sys
import os
import json
from sqlmodel import select

# Add project root to path
sys.path.append(os.getcwd())

from database.connection import get_session
from database import Word

def seed_readings_vocab():
    print("🌱 Seeding vocabulary for readings...")
    
    with get_session() as session:
        # 1. Update SUM (irregular forms)
        sum_word = session.exec(select(Word).where(Word.latin == "sum")).first()
        if sum_word:
            print("Updating 'sum' with irregular forms...")
            forms = {
                # Present Indicative
                "pres_1sg": "sum", "pres_2sg": "es", "pres_3sg": "est",
                "pres_1pl": "sumus", "pres_2pl": "estis", "pres_3pl": "sunt",
                # Imperfect Indicative
                "imp_1sg": "eram", "imp_2sg": "erās", "imp_3sg": "erat",
                "imp_1pl": "erāmus", "imp_2pl": "erātis", "imp_3pl": "erant",
                # Future Indicative
                "fut_1sg": "erō", "fut_2sg": "eris", "fut_3sg": "erit",
                "fut_1pl": "erimus", "fut_2pl": "eritis", "fut_3pl": "erunt",
                # Perfect Indicative
                "perf_1sg": "fuī", "perf_2sg": "fuistī", "perf_3sg": "fuit",
                "perf_1pl": "fuimus", "perf_2pl": "fuistis", "perf_3pl": "fuērunt",
                # Infinitive
                "inf_pres": "esse"
            }
            sum_word.irregular_forms = json.dumps(forms)
            session.add(sum_word)
        else:
            print("❌ Word 'sum' not found! Please run seed_essential_words.py first.")

        # 2. Add Missing Words
        new_words = [
            {"latin": "Rōma", "translation": "Roma", "part_of_speech": "noun", "declension": "1", "gender": "f", "genitive": "Rōmae", "level": 1, "is_fundamental": True},
            {"latin": "Italia", "translation": "Italia", "part_of_speech": "noun", "declension": "1", "gender": "f", "genitive": "Italiae", "level": 1, "is_fundamental": True},
            {"latin": "Eurōpa", "translation": "Europa", "part_of_speech": "noun", "declension": "1", "gender": "f", "genitive": "Eurōpae", "level": 1, "is_fundamental": True},
            {"latin": "Graecia", "translation": "Grecia", "part_of_speech": "noun", "declension": "1", "gender": "f", "genitive": "Graeciae", "level": 1, "is_fundamental": True},
            {"latin": "Gallia", "translation": "Galia", "part_of_speech": "noun", "declension": "1", "gender": "f", "genitive": "Galliae", "level": 1, "is_fundamental": True},
            {"latin": "Hispania", "translation": "Hispania", "part_of_speech": "noun", "declension": "1", "gender": "f", "genitive": "Hispaniae", "level": 1, "is_fundamental": True},
            {"latin": "Aegyptus", "translation": "Egipto", "part_of_speech": "noun", "declension": "2", "gender": "f", "genitive": "Aegypti", "level": 1, "is_fundamental": True}, # Aegyptus is feminine 2nd declension!
             # Prepositions
            {"latin": "in", "translation": "en/hacia", "part_of_speech": "preposition", "is_invariable": True, "level": 1, "is_fundamental": True},
            {"latin": "sed", "translation": "pero/sino", "part_of_speech": "conjunction", "is_invariable": True, "level": 1, "is_fundamental": True},
            {"latin": "et", "translation": "y", "part_of_speech": "conjunction", "is_invariable": True, "level": 1, "is_fundamental": True},
            {"latin": "ubi", "translation": "dónde", "part_of_speech": "adverb", "is_invariable": True, "level": 1, "is_fundamental": True},
             # Nilus, Rhenus, Danuvius (Rivers - masc 2nd)
            {"latin": "Nīlus", "translation": "Nilo", "part_of_speech": "noun", "declension": "2", "gender": "m", "genitive": "Nīlī", "level": 1},
            {"latin": "Rhēnus", "translation": "Rin", "part_of_speech": "noun", "declension": "2", "gender": "m", "genitive": "Rhēnī", "level": 1},
            {"latin": "Dānuvius", "translation": "Danubio", "part_of_speech": "noun", "declension": "2", "gender": "m", "genitive": "Dānuviī", "level": 1},
        ]
        
        count = 0
        for w_data in new_words:
            existing = session.exec(select(Word).where(Word.latin == w_data["latin"])).first()
            if not existing:
                word = Word(**w_data)
                session.add(word)
                count += 1
                print(f"Added {w_data['latin']}")
            else:
                 # Update if needed (e.g. set invariable)
                if w_data.get("is_invariable") and not existing.is_invariable:
                    existing.is_invariable = True
                    session.add(existing)
                    print(f"Updated {existing.latin} (invariable)")
        
        session.commit()
        print(f"✅ Updates complete. Added {count} new words.")

if __name__ == "__main__":
    seed_readings_vocab()
