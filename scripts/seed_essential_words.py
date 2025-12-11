
import sys
import os
from sqlmodel import Session, select

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.connection import get_session
from database import Word

def populate_essential_data():
    print("🌱 Populating essential verbs and nouns...")
    
    with get_session() as session:
        # 1. Verbs (Essential for Conjugation Module)
        verbs = [
            # 1st Conjugation
            {"latin": "amo", "translation": "amar", "principal_parts": "amo, amare, amavi, amatum", "conjugation": "1", "level": 1, "is_fundamental": True},
            {"latin": "laudo", "translation": "alabrar", "principal_parts": "laudo, laudare, laudavi, laudatum", "conjugation": "1", "level": 1, "is_fundamental": True},
            {"latin": "porto", "translation": "llevar", "principal_parts": "porto, portare, portavi, portatum", "conjugation": "1", "level": 1, "is_fundamental": True},
            {"latin": "pugno", "translation": "luchar", "principal_parts": "pugno, pugnare, pugnavi, pugnatum", "conjugation": "1", "level": 1, "is_fundamental": True},
            {"latin": "voco", "translation": "llamar", "principal_parts": "voco, vocare, vocavi, vocatum", "conjugation": "1", "level": 1, "is_fundamental": True},
            {"latin": "do", "translation": "dar", "principal_parts": "do, dare, dedi, datum", "conjugation": "1", "level": 1, "is_fundamental": True},
            
            # 2nd Conjugation
            {"latin": "moneo", "translation": "advertir", "principal_parts": "moneo, monere, monui, monitum", "conjugation": "2", "level": 1, "is_fundamental": True},
            {"latin": "habeo", "translation": "tener", "principal_parts": "habeo, habere, habui, habitum", "conjugation": "2", "level": 1, "is_fundamental": True},
            {"latin": "video", "translation": "ver", "principal_parts": "video, videre, vidi, visum", "conjugation": "2", "level": 1, "is_fundamental": True},
            {"latin": "timeo", "translation": "temer", "principal_parts": "timeo, timere, timui, -", "conjugation": "2", "level": 1, "is_fundamental": True},
            {"latin": "debeo", "translation": "deber", "principal_parts": "debeo, debere, debui, debitum", "conjugation": "2", "level": 1, "is_fundamental": True},
            
            # 3rd Conjugation
            {"latin": "rego", "translation": "gobernar", "principal_parts": "rego, regere, rexi, rectum", "conjugation": "3", "level": 2, "is_fundamental": True},
            {"latin": "duco", "translation": "conducir", "principal_parts": "duco, ducere, duxi, ductum", "conjugation": "3", "level": 2, "is_fundamental": True},
            {"latin": "mitto", "translation": "enviar", "principal_parts": "mitto, mittere, misi, missum", "conjugation": "3", "level": 2, "is_fundamental": True},
            {"latin": "pono", "translation": "poner", "principal_parts": "pono, ponere, posui, positum", "conjugation": "3", "level": 2, "is_fundamental": True},
            {"latin": "scribo", "translation": "escribir", "principal_parts": "scribo, scribere, scripsi, scriptum", "conjugation": "3", "level": 2, "is_fundamental": True},
            
            # 3rd -io
            {"latin": "capio", "translation": "tomar", "principal_parts": "capio, capere, cepi, captum", "conjugation": "3", "level": 2, "is_fundamental": True},
            {"latin": "facio", "translation": "hacer", "principal_parts": "facio, facere, feci, factum", "conjugation": "3", "level": 2, "is_fundamental": True},
            
            # 4th Conjugation
            {"latin": "audio", "translation": "oír", "principal_parts": "audio, audire, audivi, auditum", "conjugation": "4", "level": 2, "is_fundamental": True},
            {"latin": "venio", "translation": "venir", "principal_parts": "venio, venire, veni, ventum", "conjugation": "4", "level": 2, "is_fundamental": True},
            {"latin": "scio", "translation": "saber", "principal_parts": "scio, scire, scivi, scitum", "conjugation": "4", "level": 2, "is_fundamental": True},
            
            # Irregular
            {"latin": "sum", "translation": "ser/estar", "principal_parts": "sum, esse, fui, futurum", "conjugation": "sum", "level": 1, "is_fundamental": True},
            {"latin": "possum", "translation": "poder", "principal_parts": "possum, posse, potui, -", "conjugation": "sum", "level": 1, "is_fundamental": True},
            
            # New Verbs for L6-10
            {"latin": "vinco", "translation": "vencer", "principal_parts": "vinco, vincere, vici, victum", "conjugation": "3", "level": 2, "is_fundamental": True},
            {"latin": "credo", "translation": "creer", "principal_parts": "credo, credere, credidi, creditum", "conjugation": "3", "level": 2, "is_fundamental": True},
            {"latin": "paro", "translation": "preparar", "principal_parts": "paro, parare, paravi, paratum", "conjugation": "1", "level": 2, "is_fundamental": True},
            {"latin": "ago", "translation": "hacer/actuar", "principal_parts": "ago, agere, egi, actum", "conjugation": "3", "level": 2, "is_fundamental": True},
            {"latin": "dico", "translation": "decir", "principal_parts": "dico, dicere, dixi, dictum", "conjugation": "3", "level": 2, "is_fundamental": True},
        ]
        
        # 2. Nouns (Essential for Declension Module)
        nouns = [
            # 1st Declension
            {"latin": "rosa", "translation": "rosa", "genitive": "rosae", "gender": "feminine", "declension": "1", "level": 1, "is_fundamental": True},
            {"latin": "puella", "translation": "niña", "genitive": "puellae", "gender": "feminine", "declension": "1", "level": 1, "is_fundamental": True},
            {"latin": "femina", "translation": "mujer", "genitive": "feminae", "gender": "feminine", "declension": "1", "level": 1, "is_fundamental": True},
            {"latin": "nauta", "translation": "marinero", "genitive": "nautae", "gender": "masculine", "declension": "1", "level": 1, "is_fundamental": True},
            {"latin": "poeta", "translation": "poeta", "genitive": "poetae", "gender": "masculine", "declension": "1", "level": 1, "is_fundamental": True},
            
            # 2nd Declension (Masculine)
            {"latin": "dominus", "translation": "señor", "genitive": "domini", "gender": "masculine", "declension": "2", "level": 1, "is_fundamental": True},
            {"latin": "servus", "translation": "esclavo", "genitive": "servi", "gender": "masculine", "declension": "2", "level": 1, "is_fundamental": True},
            {"latin": "puer", "translation": "niño", "genitive": "pueri", "gender": "masculine", "declension": "2", "level": 1, "is_fundamental": True},
            {"latin": "ager", "translation": "campo", "genitive": "agri", "gender": "masculine", "declension": "2", "level": 1, "is_fundamental": True},
            
            # 2nd Declension (Neuter)
            {"latin": "bellum", "translation": "guerra", "genitive": "belli", "gender": "neuter", "declension": "2", "level": 1, "is_fundamental": True},
            {"latin": "templum", "translation": "templo", "genitive": "templi", "gender": "neuter", "declension": "2", "level": 1, "is_fundamental": True},
            
            # 3rd Declension
            {"latin": "rex", "translation": "rey", "genitive": "regis", "gender": "masculine", "declension": "3", "level": 2, "is_fundamental": True},
            {"latin": "miles", "translation": "soldado", "genitive": "militis", "gender": "masculine", "declension": "3", "level": 2, "is_fundamental": True},
            {"latin": "corpus", "translation": "cuerpo", "genitive": "corporis", "gender": "neuter", "declension": "3", "level": 2, "is_fundamental": True},
            {"latin": "urbs", "translation": "ciudad", "genitive": "urbis", "gender": "feminine", "declension": "3", "level": 2, "is_fundamental": True, "parisyllabic": True},
            
            # New Nouns for L6-10
            # 1st Declension
            {"latin": "victoria", "translation": "victoria", "genitive": "victoriae", "gender": "feminine", "declension": "1", "level": 2, "is_fundamental": True},
            {"latin": "gloria", "translation": "gloria", "genitive": "gloriae", "gender": "feminine", "declension": "1", "level": 2, "is_fundamental": True},
            {"latin": "memoria", "translation": "memoria", "genitive": "memoriae", "gender": "feminine", "declension": "1", "level": 2, "is_fundamental": True},
            {"latin": "fortuna", "translation": "fortuna", "genitive": "fortunae", "gender": "feminine", "declension": "1", "level": 2, "is_fundamental": True},
            
            # 3rd Declension
            {"latin": "lex", "translation": "ley", "genitive": "legis", "gender": "feminine", "declension": "3", "level": 2, "is_fundamental": True},
            {"latin": "pax", "translation": "paz", "genitive": "pacis", "gender": "feminine", "declension": "3", "level": 2, "is_fundamental": True},
            {"latin": "dux", "translation": "líder", "genitive": "ducis", "gender": "masculine", "declension": "3", "level": 2, "is_fundamental": True},
            {"latin": "lux", "translation": "luz", "genitive": "lucis", "gender": "feminine", "declension": "3", "level": 2, "is_fundamental": True},
            {"latin": "nox", "translation": "noche", "genitive": "noctis", "gender": "feminine", "declension": "3", "level": 2, "is_fundamental": True},
            
            # 4th Declension
            {"latin": "manus", "translation": "mano", "genitive": "manus", "gender": "feminine", "declension": "4", "level": 2, "is_fundamental": True},
            {"latin": "exercitus", "translation": "ejército", "genitive": "exercitus", "gender": "masculine", "declension": "4", "level": 2, "is_fundamental": True},
            {"latin": "domus", "translation": "casa", "genitive": "domus", "gender": "feminine", "declension": "4", "level": 2, "is_fundamental": True},
            {"latin": "fructus", "translation": "fruto", "genitive": "fructus", "gender": "masculine", "declension": "4", "level": 2, "is_fundamental": True},
            
            # 5th Declension
            {"latin": "res", "translation": "cosa", "genitive": "rei", "gender": "feminine", "declension": "5", "level": 2, "is_fundamental": True},
            {"latin": "dies", "translation": "día", "genitive": "diei", "gender": "masculine", "declension": "5", "level": 2, "is_fundamental": True},
            {"latin": "spes", "translation": "esperanza", "genitive": "spei", "gender": "feminine", "declension": "5", "level": 2, "is_fundamental": True},
            {"latin": "fides", "translation": "fe", "genitive": "fidei", "gender": "feminine", "declension": "5", "level": 2, "is_fundamental": True},
        ]
        
        # 3. Adjectives (New Section)
        adjectives = [
            # 1st Class (2-1-2)
            {"latin": "bonus", "translation": "bueno", "genitive": "boni", "gender": "m", "declension": "1/2", "level": 1, "is_fundamental": True},
            {"latin": "magnus", "translation": "grande", "genitive": "magni", "gender": "m", "declension": "1/2", "level": 1, "is_fundamental": True},
            {"latin": "pulcher", "translation": "hermoso", "genitive": "pulchri", "gender": "m", "declension": "1/2", "level": 1, "is_fundamental": True},
            {"latin": "liber", "translation": "libre", "genitive": "liberi", "gender": "m", "declension": "1/2", "level": 1, "is_fundamental": True},
            
            # 2nd Class (3rd Declension)
            {"latin": "tristis", "translation": "triste", "genitive": "tristis", "gender": "m/f", "declension": "3", "level": 2, "is_fundamental": True},
            {"latin": "fortis", "translation": "fuerte", "genitive": "fortis", "gender": "m/f", "declension": "3", "level": 2, "is_fundamental": True},
            {"latin": "brevis", "translation": "breve", "genitive": "brevis", "gender": "m/f", "declension": "3", "level": 2, "is_fundamental": True},
            {"latin": "acer", "translation": "agudo", "genitive": "acris", "gender": "m", "declension": "3", "level": 2, "is_fundamental": True},
            {"latin": "facilis", "translation": "fácil", "genitive": "facilis", "gender": "m/f", "declension": "3", "level": 2, "is_fundamental": True},
        ]

        added_count = 0
        updated_count = 0

        # Process Verbs
        for v_data in verbs:
            existing = session.exec(select(Word).where(Word.latin == v_data["latin"], Word.part_of_speech == "verb")).first()
            if existing:
                # Update fields if needed
                existing.principal_parts = v_data["principal_parts"]
                existing.conjugation = v_data["conjugation"]
                existing.is_fundamental = True
                session.add(existing)
                updated_count += 1
            else:
                new_word = Word(**v_data, part_of_speech="verb")
                session.add(new_word)
                added_count += 1
        
        # Process Nouns
        for n_data in nouns:
            existing = session.exec(select(Word).where(Word.latin == n_data["latin"], Word.part_of_speech == "noun")).first()
            if existing:
                existing.genitive = n_data["genitive"]
                existing.declension = n_data["declension"]
                existing.gender = n_data["gender"]
                existing.is_fundamental = True
                session.add(existing)
                updated_count += 1
            else:
                new_word = Word(**n_data, part_of_speech="noun")
                session.add(new_word)
                added_count += 1

        # Process Adjectives
        for a_data in adjectives:
            existing = session.exec(select(Word).where(Word.latin == a_data["latin"], Word.part_of_speech == "adjective")).first()
            if existing:
                existing.genitive = a_data["genitive"]
                existing.declension = a_data["declension"]
                existing.gender = a_data["gender"]
                existing.is_fundamental = True
                session.add(existing)
                updated_count += 1
            else:
                new_word = Word(**a_data, part_of_speech="adjective")
                session.add(new_word)
                added_count += 1

        session.commit()
        print(f"✅ Success! Added {added_count} new words, updated {updated_count} existing words.")
        
        # Verification
        total_verbs = len(session.exec(select(Word).where(Word.part_of_speech == "verb")).all())
        total_nouns = len(session.exec(select(Word).where(Word.part_of_speech == "noun")).all())
        total_adjs = len(session.exec(select(Word).where(Word.part_of_speech == "adjective")).all())
        print(f"📊 Current Database Status:")
        print(f"   - Verbs: {total_verbs}")
        print(f"   - Nouns: {total_nouns}")
        print(f"   - Adjectives: {total_adjs}")

if __name__ == "__main__":
    populate_essential_data()
