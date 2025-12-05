import sys
import os
from sqlmodel import select

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.connection import get_session
from database.models import Word

def apply_fixes():
    """
    Applies manual fixes to incomplete vocabulary entries identified in Dec 2025 audit.
    Targeting verbs with missing principal parts/conjugation and nouns with missing details.
    """
    
    # Map: latin_lemma -> {field: value, ...}
    fixes = {
        # Verbs (L18 Impersonals & others)
        "oportet": {"principal_parts": "oportet, oportere, oportuit", "conjugation": "2 (Impersonal)"},
        "licet": {"principal_parts": "licet, licere, licuit", "conjugation": "2 (Impersonal)"},
        "decet": {"principal_parts": "decet, decere, decuit", "conjugation": "2 (Impersonal)"},
        "iuvat": {"principal_parts": "iuvat, iuvare, iuvit", "conjugation": "1 (Impersonal)"},
        "placet": {"principal_parts": "placet, placere, placuit", "conjugation": "2 (Impersonal)"},
        "paenitet": {"principal_parts": "paenitet, paenitere, paenituit", "conjugation": "2 (Impersonal)"},
        "pudet": {"principal_parts": "pudet, pudere, puduit", "conjugation": "2 (Impersonal)"},
        "taedet": {"principal_parts": "taedet, taedere, taeduit", "conjugation": "2 (Impersonal)"},
        "miseret": {"principal_parts": "miseret, miserere, miseruit", "conjugation": "2 (Impersonal)"},
        
        # Verbs (Standard missing)
        "timeo": {"principal_parts": "timeo, timere, timui", "conjugation": "2"},
        "metuo": {"principal_parts": "metuo, metuere, metui", "conjugation": "3"},
        "sentio": {"principal_parts": "sentio, sentire, sensi, sensum", "conjugation": "4"},
        "intellego": {"principal_parts": "intellego, intellegere, intellexi, intellectum", "conjugation": "3"},
        "scio": {"principal_parts": "scio, scire, scivi, scitum", "conjugation": "4"},
        "nescio": {"principal_parts": "nescio, nescire, nescivi, nescitum", "conjugation": "4"},
        "cognosco": {"principal_parts": "cognosco, cognoscere, cognovi, cognitum", "conjugation": "3"},
        "concedo": {"principal_parts": "concedo, concedere, concessi, concessum", "conjugation": "3"},
        "accido": {"principal_parts": "accido, accidere, accidi", "conjugation": "3"},
        "contendo": {"principal_parts": "contendo, contendere, contendi, contentum", "conjugation": "3"},
        "dubito": {"principal_parts": "dubito, dubitare, dubitavi, dubitatum", "conjugation": "1"},
        "sino": {"principal_parts": "sino, sinere, sivi, situm", "conjugation": "3"},
        "cogo": {"principal_parts": "cogo, cogere, coegi, coactum", "conjugation": "3"},
        "dico": {"principal_parts": "dico, dicere, dixi, dictum", "conjugation": "3"},
        "nego": {"principal_parts": "nego, negare, negavi, negatum", "conjugation": "1"},
        "puto": {"principal_parts": "puto, putare, putavi, putatum", "conjugation": "1"},
        "credo": {"principal_parts": "credo, credere, credidi, creditum", "conjugation": "3"},
        "spero": {"principal_parts": "spero, sperare, speravi, speratum", "conjugation": "1"},
        "promitto": {"principal_parts": "promitto, promittere, promisi, promissum", "conjugation": "3"},
        
        # Verbs (Defective/Deponent/Special)
        "constat": {"principal_parts": "constat, constare, constitit", "conjugation": "1 (Impersonal)"},
        "apparet": {"principal_parts": "appareo, apparere, apparui, apparitum", "conjugation": "2", "latin": "appareo"}, # Correct lemma if needed
        "videtur": {"principal_parts": "videor, videri, visus sum", "conjugation": "2 (Deponent)"},
        "arbitror": {"principal_parts": "arbitror, arbitrari, arbitratus sum", "conjugation": "1 (Deponent)"},
        "existimo": {"principal_parts": "existimo, existimare, existimavi, existimatum", "conjugation": "1"},
        "orior": {"principal_parts": "orior, oriri, ortus sum", "conjugation": "4 (Deponent)"},
        "polliceor": {"principal_parts": "polliceor, polliceri, pollicitus sum", "conjugation": "2 (Deponent)"},
        "testor": {"principal_parts": "testor, testari, testatus sum", "conjugation": "1 (Deponent)"},
        "mentior": {"principal_parts": "mentior, mentiri, mentitus sum", "conjugation": "4 (Deponent)"},
        "memini": {"principal_parts": "memini, meminisse", "conjugation": "Defective"},
        "odi": {"principal_parts": "odi, odisse", "conjugation": "Defective"},
        "novi": {"principal_parts": "novi, novisse", "conjugation": "Defective (Preterite-Present)"},
        "aio": {"principal_parts": "aïo (defectivo)", "conjugation": "Irregular"},
        "inquit": {"principal_parts": "inquit (defectivo)", "conjugation": "Irregular"},
        "fio": {"principal_parts": "fio, fieri, factus sum", "conjugation": "Irregular"},
        "fero": {"principal_parts": "fero, ferre, tuli, latum", "conjugation": "Irregular"},
        "eo": {"principal_parts": "eo, ire, ii (ivi), itum", "conjugation": "Irregular"},
        "redeo": {"principal_parts": "redeo, redire, redii, reditum", "conjugation": "Irregular"},
        "exeo": {"principal_parts": "exeo, exire, exii, exitum", "conjugation": "Irregular"},
        "pereo": {"principal_parts": "pereo, perire, perii, peritum", "conjugation": "Irregular"},
        "adeo": {"principal_parts": "adeo, adire, adii, aditum", "conjugation": "Irregular"},
        "abeo": {"principal_parts": "abeo, abire, abii, abitum", "conjugation": "Irregular"},
        "ineo": {"principal_parts": "ineo, inire, inii, initum", "conjugation": "Irregular"},
        "transeo": {"principal_parts": "transeo, transire, transii, transitum", "conjugation": "Irregular"},
        "tollo": {"principal_parts": "tollo, tollere, sustuli, sublatum", "conjugation": "3"},
        "affero": {"principal_parts": "affero, afferre, attuli, allatum", "conjugation": "Irregular"},
        "confero": {"principal_parts": "confero, conferre, contuli, collatum", "conjugation": "Irregular"},
        "aufero": {"principal_parts": "aufero, auferre, abstuli, ablatum", "conjugation": "Irregular"},
        "effero": {"principal_parts": "effero, efferre, extuli, elatum", "conjugation": "Irregular"},
        
        # Missing L21+ verbs
        "capto": {"principal_parts": "capto, captare, captavi, captatum", "conjugation": "1"},
        "incendo": {"principal_parts": "incendo, incendere, incendi, incensum", "conjugation": "3"},
        "cado": {"principal_parts": "cado, cadere, cecidi, casum", "conjugation": "3"},
        "saluto": {"principal_parts": "saluto, salutare, salutavi, salutatum", "conjugation": "1"},
        "taceo": {"principal_parts": "taceo, tacere, tacui, tacitum", "conjugation": "2"},
        "gero": {"principal_parts": "gero, gerere, gessi, gestum", "conjugation": "3"},
        "servo": {"principal_parts": "servo, servare, servavi, servatum", "conjugation": "1"},
        "colo": {"principal_parts": "colo, colere, colui, cultum", "conjugation": "3"},
        "deleo": {"principal_parts": "deleo, delere, delevi, deletum", "conjugation": "2"},
        "debeo": {"principal_parts": "debeo, debere, debui, debitum", "conjugation": "2"},
        "fugio": {"principal_parts": "fugio, fugere, fugi, fugitum", "conjugation": "3-io"},
        "corrompo": {"principal_parts": "corrumpo, corrumpere, corrupi, corruptum", "conjugation": "3"},
        "impero": {"principal_parts": "impero, imperare, imperavi, imperatum", "conjugation": "1"},
        "oro": {"principal_parts": "oro, orare, oravi, oratum", "conjugation": "1"},
        "defendo": {"principal_parts": "defendo, defendere, defendi, defensum", "conjugation": "3"},
        "claudo": {"principal_parts": "claudo, claudere, clausi, clausum", "conjugation": "3"},
        "intro": {"principal_parts": "intro, intrare, intravi, intratum", "conjugation": "1"},
        "oppugno": {"principal_parts": "oppugno, oppugnare, oppugnavi, oppugnatum", "conjugation": "1"},
        "aresco": {"principal_parts": "aresco, arescere, arui", "conjugation": "3 (Inchoative)"},
        "cupio": {"principal_parts": "cupio, cupere, cupivi, cupitum", "conjugation": "3-io"},
        "cedo": {"principal_parts": "cedo, cedere, cessi, cessum", "conjugation": "3"},
        "antecedo": {"principal_parts": "antecedo, antecedere, antecessi, antecessum", "conjugation": "3"},
        "nuntio": {"principal_parts": "nuntio, nuntiare, nuntiavi, nuntiatum", "conjugation": "1"},
        "refero": {"principal_parts": "refero, referre, rettuli, relatum", "conjugation": "Irregular"},
        "respondeo": {"principal_parts": "respondeo, respondere, respondi, responsum", "conjugation": "2"},
        "interrogo": {"principal_parts": "interrogo, interrogare, interrogavi, interrogatum", "conjugation": "1"},
        "affirmo": {"principal_parts": "affirmo, affirmare, affirmavi, affirmatum", "conjugation": "1"},
        "demonstro": {"principal_parts": "demonstro, demonstrare, demonstravi, demonstratum", "conjugation": "1"},
        "divido": {"principal_parts": "divido, dividere, divisi, divisum", "conjugation": "3"},
        "incolo": {"principal_parts": "incolo, incolere, incolui", "conjugation": "3"},
        "abutor": {"principal_parts": "abutor, abutere, abusus sum", "conjugation": "3 (Deponent)"},
        "eludo": {"principal_parts": "eludo, eludere, elusi, elusum", "conjugation": "3"},
        "requiro": {"principal_parts": "requiro, requirere, requisivi, requisitum", "conjugation": "3"},
        "excrucior": {"principal_parts": "excrucio, excruciare, excruciavi, excruciatum", "conjugation": "1"}, # Lemma is active usually
        "cano": {"principal_parts": "cano, canere,cecini, cantum", "conjugation": "3"},
        "carpo": {"principal_parts": "carpo, carpere, carpsi, carptum", "conjugation": "3"},
        "amor": {"principal_parts": "amo, amare, amavi, amatum", "conjugation": "1"}, # Passive form
        "muto": {"principal_parts": "muto, mutare, mutavi, mutatum", "conjugation": "1"},
        
        # Nouns (L20+)
        "fluvius": {"genitive": "fluvii", "gender": "Masc", "declension": "2"},
        "imperium": {"genitive": "imperii", "gender": "Neut", "declension": "2"},
        "provincia": {"genitive": "provinciae", "gender": "Fem", "declension": "1"},
        "insula": {"genitive": "insulae", "gender": "Fem", "declension": "1"},
        "oppidum": {"genitive": "oppidi", "gender": "Neut", "declension": "2"},
    }

    with get_session() as session:
        count = 0
        for latin, updates in fixes.items():
            # Find word(s)
            words = session.exec(select(Word).where(Word.latin == latin)).all()
            
            for word in words:
                changed = False
                for field, val in updates.items():
                    current_val = getattr(word, field)
                    if not current_val or current_val == 'N/A' or current_val == 'None':
                        setattr(word, field, val)
                        changed = True
                    elif field == 'conjugation' and current_val in ['None', 'N/A', '3ª', '1ª', '2ª', '4ª']:
                        # Update simplified conjugation strings to standardized ones
                        setattr(word, field, val)
                        changed = True
                
                if changed:
                    session.add(word)
                    count += 1
                    print(f"Updated {latin}: {updates}")
        
        session.commit()
        print(f"\n✅ Successfully updated {count} words.")

if __name__ == "__main__":
    apply_fixes()
