"""
Script de Migración Fase 3: Verbos Irregulares y Expansión Masiva

1. Inserta verbos irregulares (sum, possum, fero, eo, volo, nolo, malo).
2. Expande significativamente el vocabulario general (sustantivos, adjetivos, verbos regulares).
"""

from database.connection import get_session
from database import Word
from sqlmodel import select
import json

def migrate_phase3():
    print("\n3. Insertando verbos irregulares y vocabulario masivo...")
    
    irregular_verbs = [
        {
            "latin": "sum",
            "translation": "ser, estar, existir",
            "part_of_speech": "verb",
            "principal_parts": "sum, esse, fuī, futūrus",
            "conjugation": "irregular", # Special marker
            "level": 1,
            "irregular_forms": json.dumps({
                "pres_1sg": "sum", "pres_2sg": "es", "pres_3sg": "est",
                "pres_1pl": "sumus", "pres_2pl": "estis", "pres_3pl": "sunt",
                "imp_1sg": "eram", "imp_2sg": "erās", "imp_3sg": "erat",
                "imp_1pl": "erāmus", "imp_2pl": "erātis", "imp_3pl": "erant"
            }),
            "category": "verb"
        },
        {
            "latin": "possum",
            "translation": "poder, ser capaz",
            "part_of_speech": "verb",
            "principal_parts": "possum, posse, potuī, —",
            "conjugation": "irregular",
            "level": 1,
            "irregular_forms": json.dumps({
                "pres_1sg": "possum", "pres_2sg": "potes", "pres_3sg": "potest",
                "pres_1pl": "possumus", "pres_2pl": "potestis", "pres_3pl": "possunt",
                "imp_1sg": "poteram", "imp_2sg": "poterās", "imp_3sg": "poterat",
                "imp_1pl": "poterāmus", "imp_2pl": "poterātis", "imp_3pl": "poterant"
            }),
            "category": "verb"
        },
        {
            "latin": "ferō",
            "translation": "llevar, portar, soportar",
            "part_of_speech": "verb",
            "principal_parts": "ferō, ferre, tulī, lātum",
            "conjugation": "irregular", # 3rd irregular
            "level": 2,
            "irregular_forms": json.dumps({
                "pres_1sg": "ferō", "pres_2sg": "fers", "pres_3sg": "fert",
                "pres_1pl": "ferimus", "pres_2pl": "fertis", "pres_3pl": "ferunt",
                # Imperfect is regular (ferēbam) but let's be safe
                "imp_1sg": "ferēbam", "imp_2sg": "ferēbās", "imp_3sg": "ferēbat",
                "imp_1pl": "ferēbāmus", "imp_2pl": "ferēbātis", "imp_3pl": "ferēbant"
            }),
            "category": "verb"
        },
        {
            "latin": "eō",
            "translation": "ir",
            "part_of_speech": "verb",
            "principal_parts": "eō, īre, iī/īvī, itum",
            "conjugation": "irregular",
            "level": 1,
            "irregular_forms": json.dumps({
                "pres_1sg": "eō", "pres_2sg": "īs", "pres_3sg": "it",
                "pres_1pl": "īmus", "pres_2pl": "ītis", "pres_3pl": "eunt",
                "imp_1sg": "ībam", "imp_2sg": "ībās", "imp_3sg": "ībat",
                "imp_1pl": "ībāmus", "imp_2pl": "ībātis", "imp_3pl": "ībant"
            }),
            "category": "verb"
        },
        {
            "latin": "volō",
            "translation": "querer, desear",
            "part_of_speech": "verb",
            "principal_parts": "volō, velle, voluī, —",
            "conjugation": "irregular",
            "level": 2,
            "irregular_forms": json.dumps({
                "pres_1sg": "volō", "pres_2sg": "vīs", "pres_3sg": "vult",
                "pres_1pl": "volumus", "pres_2pl": "vultis", "pres_3pl": "volunt",
                "imp_1sg": "volēbam", "imp_2sg": "volēbās", "imp_3sg": "volēbat",
                "imp_1pl": "volēbāmus", "imp_2pl": "volēbātis", "imp_3pl": "volēbant"
            }),
            "category": "verb"
        }
    ]

    new_vocab = [
        # Verbs (Regular)
        {"latin": "amō", "translation": "amar", "part_of_speech": "verb", "principal_parts": "amō, amāre, amāvī, amātum", "conjugation": "1", "level": 1},
        {"latin": "laudō", "translation": "alabrar", "part_of_speech": "verb", "principal_parts": "laudō, laudāre, laudāvī, laudātum", "conjugation": "1", "level": 1},
        {"latin": "portō", "translation": "llevar", "part_of_speech": "verb", "principal_parts": "portō, portāre, portāvī, portātum", "conjugation": "1", "level": 1},
        {"latin": "pugnō", "translation": "luchar", "part_of_speech": "verb", "principal_parts": "pugnō, pugnāre, pugnāvī, pugnātum", "conjugation": "1", "level": 1},
        {"latin": "vocō", "translation": "llamar", "part_of_speech": "verb", "principal_parts": "vocō, vocāre, vocāvī, vocātum", "conjugation": "1", "level": 1},
        
        {"latin": "habeō", "translation": "tener", "part_of_speech": "verb", "principal_parts": "habeō, habēre, habuī, habitum", "conjugation": "2", "level": 1},
        {"latin": "videō", "translation": "ver", "part_of_speech": "verb", "principal_parts": "videō, vidēre, vīdī, vīsum", "conjugation": "2", "level": 1},
        {"latin": "moneō", "translation": "advertir, aconsejar", "part_of_speech": "verb", "principal_parts": "moneō, monēre, monuī, monitum", "conjugation": "2", "level": 2},
        {"latin": "moveō", "translation": "mover", "part_of_speech": "verb", "principal_parts": "moveō, movēre, mōvī, mōtum", "conjugation": "2", "level": 2},
        {"latin": "doceō", "translation": "enseñar", "part_of_speech": "verb", "principal_parts": "doceō, docēre, docuī, doctum", "conjugation": "2", "level": 2},
        
        {"latin": "dīcō", "translation": "decir", "part_of_speech": "verb", "principal_parts": "dīcō, dīcere, dīxī, dictum", "conjugation": "3", "level": 1},
        {"latin": "dūcō", "translation": "guiar, liderar", "part_of_speech": "verb", "principal_parts": "dūcō, dūcere, dūxī, ductum", "conjugation": "3", "level": 1},
        {"latin": "mittō", "translation": "enviar", "part_of_speech": "verb", "principal_parts": "mittō, mittere, mīsī, missum", "conjugation": "3", "level": 1},
        {"latin": "scrībō", "translation": "escribir", "part_of_speech": "verb", "principal_parts": "scrībō, scrībere, scrīpsī, scrīptum", "conjugation": "3", "level": 1},
        {"latin": "vīvō", "translation": "vivir", "part_of_speech": "verb", "principal_parts": "vīvō, vīvere, vīxī, vīctum", "conjugation": "3", "level": 1},
        
        {"latin": "audiō", "translation": "oír, escuchar", "part_of_speech": "verb", "principal_parts": "audiō, audīre, audīvī, audītum", "conjugation": "4", "level": 1},
        {"latin": "veniō", "translation": "venir", "part_of_speech": "verb", "principal_parts": "veniō, venīre, vēnī, ventum", "conjugation": "4", "level": 1},
        {"latin": "sciō", "translation": "saber", "part_of_speech": "verb", "principal_parts": "sciō, scīre, scīvī, scītum", "conjugation": "4", "level": 2},
        {"latin": "sentiō", "translation": "sentir", "part_of_speech": "verb", "principal_parts": "sentiō, sentīre, sēnsī, sēnsum", "conjugation": "4", "level": 2},
        
        # Nouns (More vocabulary)
        {"latin": "agricola", "translation": "agricultor", "genitive": "agricolae", "gender": "m", "declension": "1", "level": 1, "part_of_speech": "noun"},
        {"latin": "epistula", "translation": "carta", "genitive": "epistulae", "gender": "f", "declension": "1", "level": 1, "part_of_speech": "noun"},
        {"latin": "patria", "translation": "patria", "genitive": "patriae", "gender": "f", "declension": "1", "level": 1, "part_of_speech": "noun"},
        {"latin": "pecūnia", "translation": "dinero", "genitive": "pecūniae", "gender": "f", "declension": "1", "level": 1, "part_of_speech": "noun"},
        {"latin": "vīta", "translation": "vida", "genitive": "vītae", "gender": "f", "declension": "1", "level": 1, "part_of_speech": "noun"},
        
        {"latin": "ager", "translation": "campo", "genitive": "agrī", "gender": "m", "declension": "2", "level": 1, "part_of_speech": "noun"},
        {"latin": "puer", "translation": "niño", "genitive": "puerī", "gender": "m", "declension": "2", "level": 1, "part_of_speech": "noun"},
        {"latin": "fīlius", "translation": "hijo", "genitive": "fīliī", "gender": "m", "declension": "2", "level": 1, "part_of_speech": "noun"},
        {"latin": "servus", "translation": "esclavo, sirviente", "genitive": "servī", "gender": "m", "declension": "2", "level": 1, "part_of_speech": "noun"},
        {"latin": "verbum", "translation": "palabra", "genitive": "verbī", "gender": "n", "declension": "2", "level": 1, "part_of_speech": "noun"},
        
        {"latin": "dux", "translation": "líder, general", "genitive": "ducis", "gender": "m", "declension": "3", "level": 2, "part_of_speech": "noun"},
        {"latin": "lēx", "translation": "ley", "genitive": "lēgis", "gender": "f", "declension": "3", "level": 2, "part_of_speech": "noun"},
        {"latin": "mīles", "translation": "soldado", "genitive": "mīlitis", "gender": "m", "declension": "3", "level": 2, "part_of_speech": "noun"},
        {"latin": "nōmen", "translation": "nombre", "genitive": "nōminis", "gender": "n", "declension": "3", "level": 1, "part_of_speech": "noun"},
        {"latin": "tempus", "translation": "tiempo", "genitive": "temporis", "gender": "n", "declension": "3", "level": 1, "part_of_speech": "noun"},
        
        {"latin": "manus", "translation": "mano, banda", "genitive": "manūs", "gender": "f", "declension": "4", "level": 3, "part_of_speech": "noun"},
        {"latin": "diēs", "translation": "día", "genitive": "diēī", "gender": "m", "declension": "5", "level": 3, "part_of_speech": "noun"}
    ]

    with get_session() as session:
        # Insert irregular verbs
        count_irr = 0
        for data in irregular_verbs:
            existing = session.exec(select(Word).where(Word.latin == data["latin"])).first()
            if not existing:
                word = Word(**data)
                session.add(word)
                count_irr += 1
                print(f"   + Insertado verbo irregular: {data['latin']}")
            else:
                # Update existing
                existing.irregular_forms = data["irregular_forms"]
                existing.principal_parts = data["principal_parts"]
                existing.conjugation = data["conjugation"]
                session.add(existing)
                print(f"   ~ Actualizado verbo irregular: {data['latin']}")

        # Insert new vocabulary
        count_new = 0
        for data in new_vocab:
            existing = session.exec(select(Word).where(Word.latin == data["latin"])).first()
            if not existing:
                word = Word(
                    latin=data["latin"],
                    translation=data["translation"],
                    part_of_speech=data["part_of_speech"],
                    genitive=data.get("genitive"),
                    gender=data.get("gender"),
                    declension=data.get("declension"),
                    principal_parts=data.get("principal_parts"),
                    conjugation=data.get("conjugation"),
                    level=data["level"],
                    category=data["part_of_speech"]
                )
                session.add(word)
                count_new += 1
        
        session.commit()
        print(f"\n✅ Migración Fase 3 completada.")
        print(f"   - Verbos irregulares: {count_irr}")
        print(f"   - Vocabulario nuevo: {count_new}")

if __name__ == "__main__":
    migrate_phase3()
