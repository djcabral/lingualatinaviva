from database import get_session, Word
from sqlmodel import select

def update_vocabulary():
    updates = {
        # L13 Passives
        "amor": {"principal_parts": "amor, amari, amatus sum", "conjugation": "1 (Pasiva)"},
        "videor": {"principal_parts": "videor, videri, visus sum", "conjugation": "2 (Deponente)"},
        "ducor": {"principal_parts": "ducor, duci, ductus sum", "conjugation": "3 (Pasiva)"},
        "capior": {"principal_parts": "capior, capi, captus sum", "conjugation": "3-io (Pasiva)"},
        
        # L15
        "gero": {"principal_parts": "gero, gerere, gessi, gestum", "conjugation": "3"},
        "moveo": {"principal_parts": "moveo, movere, movi, motum", "conjugation": "2"},
        "teneo": {"principal_parts": "teneo, tenere, tenui, tentum", "conjugation": "2"},
        "peto": {"principal_parts": "peto, petere, petivi, petitum", "conjugation": "3"},
        
        # L16
        "quaero": {"principal_parts": "quaero, quaerere, quaesivi, quaesitum", "conjugation": "3"},
        "invenio": {"principal_parts": "invenio, invenire, inveni, inventum", "conjugation": "4"},
        "relinquo": {"principal_parts": "relinquo, relinquere, reliqui, relictum", "conjugation": "3"},
        "accipio": {"principal_parts": "accipio, accipere, accepi, acceptum", "conjugation": "3-io"},
        
        # L17 Deponents
        "loquor": {"principal_parts": "loquor, loqui, locutus sum", "conjugation": "3 (Deponente)"},
        "sequor": {"principal_parts": "sequor, sequi, secutus sum", "conjugation": "3 (Deponente)"},
        "utor": {"principal_parts": "utor, uti, usus sum", "conjugation": "3 (Deponente)"},
        "patior": {"principal_parts": "patior, pati, passus sum", "conjugation": "3-io (Deponente)"},
        "morior": {"principal_parts": "morior, mori, mortuus sum", "conjugation": "3-io (Deponente)"},
        "nascor": {"principal_parts": "nascor, nasci, natus sum", "conjugation": "3 (Deponente)"},
        "proficiscor": {"principal_parts": "proficiscor, proficisci, profectus sum", "conjugation": "3 (Deponente)"},
        "ingredior": {"principal_parts": "ingredior, ingredi, ingressus sum", "conjugation": "3-io (Deponente)"},
        "egredior": {"principal_parts": "egredior, egredi, egressus sum", "conjugation": "3-io (Deponente)"},
        "progredior": {"principal_parts": "progredior, progredi, progressus sum", "conjugation": "3-io (Deponente)"},
        "audeo": {"principal_parts": "audeo, audere, ausus sum", "conjugation": "2 (Semideponente)"},
        "gaudeo": {"principal_parts": "gaudeo, gaudere, gavisus sum", "conjugation": "2 (Semideponente)"},
        
        # L18
        "volo": {"principal_parts": "volo, velle, volui, -", "conjugation": "Irregular"},
        "nolo": {"principal_parts": "nolo, nolle, nolui, -", "conjugation": "Irregular"},
        "malo": {"principal_parts": "malo, malle, malui, -", "conjugation": "Irregular"},
        "cupio": {"principal_parts": "cupio, cupere, cupivi, cupitum", "conjugation": "3-io"},
        "opto": {"principal_parts": "opto, optare, optavi, optatum", "conjugation": "1"},
        "metuo": {"principal_parts": "metuo, metuere, metui, -", "conjugation": "3"},
        "oportet": {"principal_parts": "oportet, oportere, oportuit", "conjugation": "Impersonal"},
        "licet": {"principal_parts": "licet, licere, licuit", "conjugation": "Impersonal"},
        "decet": {"principal_parts": "decet, decere, decuit", "conjugation": "Impersonal"},
        
        # L19
        "sentio": {"principal_parts": "sentio, sentire, sensi, sensum", "conjugation": "4"},
        "intellego": {"principal_parts": "intellego, intellegere, intellexi, intellectum", "conjugation": "3"},
        "cognosco": {"principal_parts": "cognosco, cognoscere, cognovi, cognitum", "conjugation": "3"},
        
        # L20
        "nego": {"principal_parts": "nego, negare, negavi, negatum", "conjugation": "1"},
        "puto": {"principal_parts": "puto, putare, putavi, putatum", "conjugation": "1"},
        "spero": {"principal_parts": "spero, sperare, speravi, speratum", "conjugation": "1"},
        "promitto": {"principal_parts": "promitto, promittere, promisi, promissum", "conjugation": "3"},
        "constat": {"principal_parts": "constat, constare, constitit", "conjugation": "Impersonal"},
        "apparet": {"principal_parts": "appareo, apparere, apparui, apparitum", "conjugation": "2"},
        "videtur": {"principal_parts": "videor, videri, visus sum", "conjugation": "2 (Deponente)"}
    }
    
    with get_session() as session:
        count = 0
        for latin_word, data in updates.items():
            word = session.exec(select(Word).where(Word.latin == latin_word)).first()
            if word:
                word.principal_parts = data["principal_parts"]
                word.conjugation = data["conjugation"]
                session.add(word)
                count += 1
                print(f"Updated {latin_word}: {data}")
            else:
                print(f"Warning: Word '{latin_word}' not found in database")
        
        session.commit()
        print(f"\nSuccessfully updated {count} words.")

if __name__ == "__main__":
    update_vocabulary()
