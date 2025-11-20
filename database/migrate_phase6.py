import sys
import os
import re
import unicodedata
from sqlmodel import Session, select

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.connection import engine
from database.models import Word, Text, TextWordLink, Author

def normalize_latin(text):
    """Remove macrons and diacritics for matching"""
    normalized = unicodedata.normalize('NFD', text)
    return ''.join(char for char in normalized if unicodedata.category(char) != 'Mn')

def migrate():
    print("Starting Phase 6 Migration: Lectio Expansion (Hyginus)...")
    
    with Session(engine) as session:
        # 1. Add Author: Hyginus
        hyginus = session.exec(select(Author).where(Author.name == "Hyginus")).first()
        if not hyginus:
            hyginus = Author(
                name="Hyginus",
                full_name="Gaius Julius Hyginus",
                difficulty_level=3,
                period="Augustan",
                description="Author of Fabulae, a collection of myths."
            )
            session.add(hyginus)
            session.commit()
            session.refresh(hyginus)
            print(f"Added Author: {hyginus.name}")

        # 2. Add Vocabulary
        new_words_data = [
            # Nouns (School)
            {"latin": "magister", "translation": "maestro", "pos": "noun", "gen": "magistrī", "gender": "m", "decl": "2", "level": 2},
            {"latin": "discipulus", "translation": "alumno", "pos": "noun", "gen": "discipulī", "gender": "m", "decl": "2", "level": 2},
            {"latin": "discipula", "translation": "alumna", "pos": "noun", "gen": "discipulae", "gender": "f", "decl": "1", "level": 2},
            {"latin": "tabula", "translation": "tablilla", "pos": "noun", "gen": "tabulae", "gender": "f", "decl": "1", "level": 2},
            {"latin": "stilus", "translation": "estilo (punzón)", "pos": "noun", "gen": "stilī", "gender": "m", "decl": "2", "level": 2},
            {"latin": "lūdus", "translation": "escuela, juego", "pos": "noun", "gen": "lūdī", "gender": "m", "decl": "2", "level": 2},
            
            # Nouns (Mythology/Nature)
            {"latin": "deus", "translation": "dios", "pos": "noun", "gen": "deī", "gender": "m", "decl": "2", "level": 2},
            {"latin": "dea", "translation": "diosa", "pos": "noun", "gen": "deae", "gender": "f", "decl": "1", "level": 2, "irr": '{"dat_pl": "deābus", "abl_pl": "deābus"}'},
            {"latin": "caelum", "translation": "cielo", "pos": "noun", "gen": "caelī", "gender": "n", "decl": "2", "level": 2},
            {"latin": "terra", "translation": "tierra", "pos": "noun", "gen": "terrae", "gender": "f", "decl": "1", "level": 1},
            {"latin": "ignis", "translation": "fuego", "pos": "noun", "gen": "ignis", "gender": "m", "decl": "3", "level": 3},
            {"latin": "dōnum", "translation": "regalo", "pos": "noun", "gen": "dōnī", "gender": "n", "decl": "2", "level": 2},
            {"latin": "mulier", "translation": "mujer", "pos": "noun", "gen": "mulieris", "gender": "f", "decl": "3", "level": 3},
            {"latin": "homō", "translation": "hombre, ser humano", "pos": "noun", "gen": "hominis", "gender": "m", "decl": "3", "level": 3},
            {"latin": "saxum", "translation": "roca", "pos": "noun", "gen": "saxī", "gender": "n", "decl": "2", "level": 3},
            {"latin": "poena", "translation": "castigo", "pos": "noun", "gen": "poenae", "gender": "f", "decl": "1", "level": 3},
            {"latin": "aquila", "translation": "águila", "pos": "noun", "gen": "aquilae", "gender": "f", "decl": "1", "level": 3},
            {"latin": "cor", "translation": "corazón", "pos": "noun", "gen": "cordis", "gender": "n", "decl": "3", "level": 3},
            
            # Verbs
            {"latin": "docēre", "translation": "enseñar", "pos": "verb", "pp": "doceō, docēre, docuī, doctum", "conj": "2", "level": 2},
            {"latin": "discere", "translation": "aprender", "pos": "verb", "pp": "discō, discere, didicī", "conj": "3", "level": 2},
            {"latin": "scrībere", "translation": "escribir", "pos": "verb", "pp": "scrībō, scrībere, scrīpsī, scrīptum", "conj": "3", "level": 2},
            {"latin": "lūdere", "translation": "jugar", "pos": "verb", "pp": "lūdō, lūdere, lūsī, lūsum", "conj": "3", "level": 2},
            {"latin": "creāre", "translation": "crear", "pos": "verb", "pp": "creō, creāre, creāvī, creātum", "conj": "1", "level": 3},
            {"latin": "dare", "translation": "dar", "pos": "verb", "pp": "dō, dare, dedī, datum", "conj": "1", "level": 1},
            {"latin": "mittere", "translation": "enviar", "pos": "verb", "pp": "mittō, mittere, mīsī, missum", "conj": "3", "level": 3},
            {"latin": "facere", "translation": "hacer", "pos": "verb", "pp": "faciō, facere, fēcī, factum", "conj": "3", "level": 3},
            {"latin": "vidēre", "translation": "ver", "pos": "verb", "pp": "videō, vidēre, vīdī, vīsum", "conj": "2", "level": 2},
            {"latin": "habēre", "translation": "tener", "pos": "verb", "pp": "habeō, habēre, habuī, habitum", "conj": "2", "level": 1},
            {"latin": "edere", "translation": "comer", "pos": "verb", "pp": "edō, edere, ēdī, ēsum", "conj": "3", "level": 3},
            
            # Adjectives
            {"latin": "bonus", "translation": "bueno", "pos": "adjective", "level": 1},
            {"latin": "malus", "translation": "malo", "pos": "adjective", "level": 1},
            {"latin": "prīmus", "translation": "primero", "pos": "adjective", "level": 2},
            {"latin": "īrātus", "translation": "enojado", "pos": "adjective", "level": 2},
            {"latin": "multus", "translation": "mucho", "pos": "adjective", "level": 1},
            {"latin": "paucus", "translation": "poco", "pos": "adjective", "level": 2},
            
            # Invariables
            {"latin": "autem", "translation": "sin embargo", "pos": "conjunction", "level": 2, "inv": True},
            {"latin": "tum", "translation": "entonces", "pos": "adverb", "level": 2, "inv": True},
            {"latin": "postea", "translation": "después", "pos": "adverb", "level": 3, "inv": True},
            {"latin": "quoque", "translation": "también", "pos": "adverb", "level": 2, "inv": True},
            {"latin": "ē", "translation": "de, desde (ex)", "pos": "preposition", "level": 1, "inv": True},
        ]

        print(f"Processing {len(new_words_data)} words...")
        for w_data in new_words_data:
            # Check if exists
            existing = session.exec(select(Word).where(Word.latin == w_data["latin"])).first()
            if not existing:
                word = Word(
                    latin=w_data["latin"],
                    translation=w_data["translation"],
                    part_of_speech=w_data["pos"],
                    level=w_data["level"],
                    genitive=w_data.get("gen"),
                    gender=w_data.get("gender"),
                    declension=w_data.get("decl"),
                    principal_parts=w_data.get("pp"),
                    conjugation=w_data.get("conj"),
                    is_invariable=w_data.get("inv", False),
                    category=w_data["pos"] if w_data.get("inv") else None,
                    irregular_forms=w_data.get("irr")
                )
                session.add(word)
                print(f"  + Added: {word.latin}")
            else:
                print(f"  . Skipped: {w_data['latin']}")
        
        session.commit()

        # 3. Add Texts
        texts_data = [
            {
                "title": "Schola Rōmāna",
                "content": "In scholā sunt multī discipulī et ūnus magister. Magister in sellā sedet; discipulī in subselliīs sedent. Discipulī tabulās et stilōs habent. Magister puerōs docet: 'Salvēte, puerī!' Puerī respondent: 'Salvē, magister!' Magister linguam Latīnam docet. Puerī litterās scrībunt. Marcus bene scrībit, sed Titus male scrībit. Magister īrātus est: 'Tite! Scrībe bene!' Titus stilum sūmit et iterum scrībit. Nunc bene est.",
                "level": 2,
                "author": None
            },
            {
                "title": "Deīs et Deābus",
                "content": "Rōmānī multōs deōs et multās deās colunt. Iuppiter est rēx deōrum et in caelō habitat. Iūnō est rēgīna deōrum et uxor Iovis. Neptūnus est deus maris. Mars est deus bellī. Venus est dea amōris. Diāna est dea silvārum. Deī Rōmānī potentēs sunt. Hominēs deīs dōna dant et sacrificant. In forō Rōmānō sunt multa templa deōrum.",
                "level": 2,
                "author": None
            },
            {
                "title": "Promētheus",
                "content": "Promētheus, fīlius Īapetī, hominēs ex lutō fīnxit. Sed hominēs ignem nōn habēbant et vītam dūram agēbant. Promētheus hominēs amābat. Itaque in caelum ascendit et ignem ā Iove surripuit. Tum ignem in terrā hominibus dedit. Iuppiter īrātus erat. Promētheum in monte Caucasō alligāvit. Cotīdiē aquila veniēbat et cor Promētheī edēbat. Nocte cor crēscēbat. Haec poena longa et dūra erat.",
                "level": 3,
                "author_id": hyginus.id
            },
            {
                "title": "Pandōra",
                "content": "Iuppiter hominēs pūnīre volēbat, quod ignem habēbant. Itaque Vulcānus, deus ignis, fēminam pulchram fēcit. Deī fēminae multa dōna dedērunt. Nōmen fēminae erat Pandōra. Iuppiter Pandōrae arcam dedit, sed dīxit: 'Nōlī arcam aperīre!' Pandōra in terram vēnit. Epimētheus Pandōram in mātrimōnium dūxit. Sed Pandōra cūriōsa erat. Arcam aperuit. Statim omnia mala ēvolāvērunt: morbī, dolōrēs, bella. Sōla Spēs in arcā mānsit.",
                "level": 3,
                "author_id": hyginus.id
            }
        ]

        print(f"Processing {len(texts_data)} texts...")
        all_words = session.exec(select(Word)).all()
        
        for t_data in texts_data:
            existing = session.exec(select(Text).where(Text.title == t_data["title"])).first()
            if not existing:
                text = Text(
                    title=t_data["title"],
                    content=t_data["content"],
                    difficulty=t_data["level"], # Corrected attribute
                    author_id=t_data.get("author_id")
                )
                session.add(text)
                session.commit()
                session.refresh(text)
                print(f"  + Added Text: {text.title}")
                
                # Link words
                words_in_text = re.findall(r'[a-zA-ZāēīōūĀĒĪŌŪ]+', t_data["content"].lower())
                word_freq = {}
                for w in words_in_text:
                    nw = normalize_latin(w)
                    word_freq[nw] = word_freq.get(nw, 0) + 1
                
                linked_count = 0
                for text_word, freq in word_freq.items():
                    for db_word in all_words:
                        if normalize_latin(db_word.latin.lower()) == text_word:
                            link = TextWordLink(
                                text_id=text.id,
                                word_id=db_word.id,
                                frequency=freq
                            )
                            session.add(link)
                            linked_count += 1
                            break
                print(f"    - Linked {linked_count} words")
            else:
                print(f"  . Skipped Text: {t_data['title']}")
        
        session.commit()
        print("Phase 6 Migration Complete!")

if __name__ == "__main__":
    migrate()
