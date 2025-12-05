import sys
import os
from sqlmodel import select

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from database import get_session, Word, LessonVocabulary, SentenceAnalysis

def seed_l6_l10():
    print("Seeding data for Lessons 6-10...")
    
    with get_session() as session:
        # --- LESSON 6: 3rd/4th Conjugation & Adjectives ---
        l6_vocab = [
            # Verbs 3rd
            {"latin": "lego", "translation": "leer", "pos": "verb", "lesson": 6, "cultural_context": "La lectura era fundamental en la educación romana, aunque a menudo se hacía en voz alta. 'Legere' también significa 'recoger' o 'elegir'."},
            {"latin": "dico", "translation": "decir", "pos": "verb", "lesson": 6, "cultural_context": "La oratoria era la habilidad más prestigiosa para un ciudadano romano. 'Dicere' implica hablar formalmente."},
            {"latin": "duco", "translation": "conducir", "pos": "verb", "lesson": 6, "cultural_context": "Término militar clave: el 'dux' es el líder. De aquí viene 'duque' y 'acueducto'."},
            {"latin": "scribo", "translation": "escribir", "pos": "verb", "lesson": 6, "cultural_context": "Se escribía con un 'stylus' sobre tablillas de cera para notas temporales, o con tinta en papiro para documentos permanentes."},
            {"latin": "mitto", "translation": "enviar", "pos": "verb", "lesson": 6},
            {"latin": "vivo", "translation": "vivir", "pos": "verb", "lesson": 6},
            # Verbs 4th
            {"latin": "audio", "translation": "oír", "pos": "verb", "lesson": 6},
            {"latin": "venio", "translation": "venir", "pos": "verb", "lesson": 6},
            {"latin": "dormio", "translation": "dormir", "pos": "verb", "lesson": 6},
            # Adjectives
            {"latin": "bonus", "translation": "bueno", "pos": "adjective", "lesson": 6, "cultural_context": "El ideal romano del 'vir bonus' (hombre bueno) implicaba no solo moralidad, sino utilidad cívica y competencia."},
            {"latin": "magnus", "translation": "grande", "pos": "adjective", "lesson": 6},
            {"latin": "parvus", "translation": "pequeño", "pos": "adjective", "lesson": 6},
            {"latin": "pulcher", "translation": "hermoso", "pos": "adjective", "lesson": 6},
            {"latin": "liber", "translation": "libre", "pos": "adjective", "lesson": 6, "cultural_context": "Ser 'liber' (libre) era la distinción social más importante. Los esclavos podían ser liberados ('manumitidos') y convertirse en libertos."},
            {"latin": "malus", "translation": "malo", "pos": "adjective", "lesson": 6},
        ]
        
        l6_sentences = [
            {"latin": "Puer librum legit.", "translation": "El niño lee el libro.", "analysis": "Puer(Nom) + librum(Ac) + legit(V)", "lesson": 6},
            {"latin": "Magister fabulam narrat.", "translation": "El maestro cuenta una historia.", "analysis": "Magister(Nom) + fabulam(Ac) + narrat(V)", "lesson": 6},
            {"latin": "Milites ducem audiunt.", "translation": "Los soldados oyen al líder.", "analysis": "Milites(Nom) + ducem(Ac) + audiunt(V)", "lesson": 6},
            {"latin": "Puella pulchra venit.", "translation": "La niña hermosa viene.", "analysis": "Puella(Nom) + pulchra(Adj) + venit(V)", "lesson": 6},
            {"latin": "Pueri boni dormiunt.", "translation": "Los niños buenos duermen.", "analysis": "Pueri(Nom) + boni(Adj) + dormiunt(V)", "lesson": 6},
            {"latin": "Romani bella gerunt.", "translation": "Los romanos hacen guerras.", "analysis": "Romani(Nom) + bella(Ac) + gerunt(V)", "lesson": 6},
            {"latin": "Servi aquam portant.", "translation": "Los esclavos llevan agua.", "analysis": "Servi(Nom) + aquam(Ac) + portant(V)", "lesson": 6},
            {"latin": "Poeta verba scribit.", "translation": "El poeta escribe palabras.", "analysis": "Poeta(Nom) + verba(Ac) + scribit(V)", "lesson": 6},
        ]

        # --- LESSON 7: 3rd Declension & Dative ---
        l7_vocab = [
            {"latin": "rex", "translation": "rey", "pos": "noun", "lesson": 7, "cultural_context": "Roma fue una monarquía antes de ser República. La palabra 'rex' se volvió odiosa para los romanos tras la expulsión de Tarquinio el Soberbio."},
            {"latin": "homo", "translation": "hombre", "pos": "noun", "lesson": 7, "cultural_context": "Significa 'ser humano' en general, a diferencia de 'vir' (varón)."},
            {"latin": "mulier", "translation": "mujer", "pos": "noun", "lesson": 7},
            {"latin": "pater", "translation": "padre", "pos": "noun", "lesson": 7, "cultural_context": "El 'Pater Familias' tenía poder absoluto ('patria potestas') sobre todos los miembros de su casa, incluyendo vida y muerte en tiempos arcaicos."},
            {"latin": "mater", "translation": "madre", "pos": "noun", "lesson": 7, "cultural_context": "La 'Matrona' romana gozaba de respeto y dignidad, administrando la casa y educando a los hijos en sus primeros años."},
            {"latin": "frater", "translation": "hermano", "pos": "noun", "lesson": 7},
            {"latin": "civis", "translation": "ciudadano", "pos": "noun", "lesson": 7, "cultural_context": "La ciudadanía romana ('civitas') otorgaba derechos legales y protección. San Pablo apeló a su ciudadanía para evitar ser azotado."},
            {"latin": "urbs", "translation": "ciudad", "pos": "noun", "lesson": 7, "cultural_context": "Para un romano, 'Urbs' (con mayúscula) solía referirse a Roma misma, la Ciudad por excelencia."},
            {"latin": "corpus", "translation": "cuerpo", "pos": "noun", "lesson": 7},
            {"latin": "nomen", "translation": "nombre", "pos": "noun", "lesson": 7, "cultural_context": "Los romanos tenían tres nombres (tria nomina): praenomen (nombre), nomen (gens/familia) y cognomen (rama familiar/apodo)."},
        ]
        
        l7_sentences = [
            {"latin": "Puer puellae rosam dat.", "translation": "El niño da una rosa a la niña.", "analysis": "Puer(Nom) + puellae(Dat) + rosam(Ac) + dat(V)", "lesson": 7},
            {"latin": "Magister discipulis libros dat.", "translation": "El maestro da libros a los discípulos.", "analysis": "Magister(Nom) + discipulis(Dat) + libros(Ac) + dat(V)", "lesson": 7},
            {"latin": "Do tibi donum.", "translation": "Te doy un regalo.", "analysis": "Do(V) + tibi(Dat) + donum(Ac)", "lesson": 7},
            {"latin": "Mihi est liber.", "translation": "Tengo un libro.", "analysis": "Mihi(Dat) + est(V) + liber(Nom) -> Dativo Posesivo", "lesson": 7},
            {"latin": "Caesari sunt multi milites.", "translation": "César tiene muchos soldados.", "analysis": "Caesari(Dat) + sunt(V) + multi milites(Nom) -> Dativo Posesivo", "lesson": 7},
            {"latin": "Rex civibus leges dat.", "translation": "El rey da leyes a los ciudadanos.", "analysis": "Rex(Nom) + civibus(Dat) + leges(Ac) + dat(V)", "lesson": 7},
            {"latin": "Mater filio panem dat.", "translation": "La madre da pan al hijo.", "analysis": "Mater(Nom) + filio(Dat) + panem(Ac) + dat(V)", "lesson": 7},
            {"latin": "Homines urbi muros aedificant.", "translation": "Los hombres construyen muros para la ciudad.", "analysis": "Homines(Nom) + urbi(Dat) + muros(Ac) + aedificant(V)", "lesson": 7},
        ]

        # --- LESSON 8: 4th Declension & Perfect ---
        l8_vocab = [
            {"latin": "manus", "translation": "mano", "pos": "noun", "lesson": 8, "cultural_context": "La 'manus' simbolizaba poder jurídico. 'Manus' era el poder del marido sobre la esposa en ciertos matrimonios."},
            {"latin": "exercitus", "translation": "ejército", "pos": "noun", "lesson": 8, "cultural_context": "El ejército romano evolucionó de una milicia ciudadana a una fuerza profesional formidable que construía carreteras y campamentos."},
            {"latin": "senatus", "translation": "senado", "pos": "noun", "lesson": 8, "cultural_context": "El 'Senatus' (consejo de ancianos) era el cuerpo gobernante supremo de la República, encargado de la política exterior y las finanzas."},
            {"latin": "domus", "translation": "casa", "pos": "noun", "lesson": 8, "cultural_context": "La 'domus' era la casa urbana de una familia rica, con atrio y peristilo. Los pobres vivían en 'insulae' (bloques de pisos)."},
            {"latin": "habui", "translation": "tuve (habeo)", "pos": "verb", "lesson": 8},
            {"latin": "dixi", "translation": "dije (dico)", "pos": "verb", "lesson": 8},
            {"latin": "vidi", "translation": "vi (video)", "pos": "verb", "lesson": 8},
        ]
        
        l8_sentences = [
            {"latin": "Domus patris magna est.", "translation": "La casa del padre es grande.", "analysis": "Domus(Nom) + patris(Gen) + magna(Adj) + est(V)", "lesson": 8},
            {"latin": "Liber pueri est novus.", "translation": "El libro del niño es nuevo.", "analysis": "Liber(Nom) + pueri(Gen) + est(V) + novus(Adj)", "lesson": 8},
            {"latin": "Amor patriae laudabilis est.", "translation": "El amor a la patria es loable.", "analysis": "Amor(Nom) + patriae(Gen) + ...", "lesson": 8},
            {"latin": "Milites iter fecerunt.", "translation": "Los soldados hicieron el viaje.", "analysis": "Milites(Nom) + iter(Ac) + fecerunt(V Perf)", "lesson": 8},
            {"latin": "Vidi urbem magnam.", "translation": "Vi una gran ciudad.", "analysis": "Vidi(V Perf) + urbem(Ac) + magnam(Adj)", "lesson": 8},
            {"latin": "Caesar exercitum duxit.", "translation": "César condujo el ejército.", "analysis": "Caesar(Nom) + exercitum(Ac) + duxit(V Perf)", "lesson": 8},
            {"latin": "Senatus consulem audivit.", "translation": "El senado oyó al cónsul.", "analysis": "Senatus(Nom) + consulem(Ac) + audivit(V Perf)", "lesson": 8},
        ]

        # --- LESSON 9: 5th Declension & Future ---
        l9_vocab = [
            {"latin": "dies", "translation": "día", "pos": "noun", "lesson": 9, "cultural_context": "Los romanos dividían el día en 12 horas de luz, cuya duración variaba según la estación."},
            {"latin": "res", "translation": "cosa", "pos": "noun", "lesson": 9, "cultural_context": "'Res' es una palabra comodín. 'Res Publica' (la cosa pública) es el Estado. 'Res gestae' son hazañas."},
            {"latin": "spes", "translation": "esperanza", "pos": "noun", "lesson": 9},
            {"latin": "fides", "translation": "fe", "pos": "noun", "lesson": 9, "cultural_context": "La 'Fides' era la lealtad y la palabra dada, base de las relaciones sociales y políticas romanas."},
            {"latin": "amabo", "translation": "amaré", "pos": "verb", "lesson": 9},
            {"latin": "legam", "translation": "leeré", "pos": "verb", "lesson": 9},
        ]
        
        l9_sentences = [
            {"latin": "Dies venit.", "translation": "El día viene.", "analysis": "Dies(Nom) + venit(V)", "lesson": 9},
            {"latin": "Res publica est magna.", "translation": "La república es grande.", "analysis": "Res(Nom) + publica(Adj) + est(V) + magna(Adj)", "lesson": 9},
            {"latin": "Cras te videbo.", "translation": "Mañana te veré.", "analysis": "Cras(Adv) + te(Ac) + videbo(V Fut)", "lesson": 9},
            {"latin": "Librum legam.", "translation": "Leeré el libro.", "analysis": "Librum(Ac) + legam(V Fut)", "lesson": 9},
            {"latin": "Semper amicos amabimus.", "translation": "Siempre amaremos a los amigos.", "analysis": "Semper(Adv) + amicos(Ac) + amabimus(V Fut)", "lesson": 9},
            {"latin": "Spes victoriae militibus est.", "translation": "Los soldados tienen esperanza de victoria.", "analysis": "Spes(Nom) + victoriae(Gen) + militibus(Dat Pos) + est(V)", "lesson": 9},
        ]

        # --- LESSON 10: 2nd Class Adjectives ---
        l10_vocab = [
            {"latin": "fortis", "translation": "fuerte", "pos": "adjective", "lesson": 10, "cultural_context": "'Fortitudo' (fortaleza) era una de las cuatro virtudes cardinales, esencial para el soldado y el ciudadano."},
            {"latin": "omnis", "translation": "todo", "pos": "adjective", "lesson": 10},
            {"latin": "ingens", "translation": "enorme", "pos": "adjective", "lesson": 10},
            {"latin": "audax", "translation": "audaz", "pos": "adjective", "lesson": 10},
            {"latin": "celer", "translation": "rápido", "pos": "adjective", "lesson": 10},
            {"latin": "facilis", "translation": "fácil", "pos": "adjective", "lesson": 10},
        ]
        
        l10_sentences = [
            {"latin": "Miles fortis pugnat.", "translation": "El soldado fuerte lucha.", "analysis": "Miles(Nom) + fortis(Adj) + pugnat(V)", "lesson": 10},
            {"latin": "Omnes homines mortales sunt.", "translation": "Todos los hombres son mortales.", "analysis": "Omnes(Adj) + homines(Nom) + mortales(Adj) + sunt(V)", "lesson": 10},
            {"latin": "Urbs ingens est.", "translation": "La ciudad es enorme.", "analysis": "Urbs(Nom) + ingens(Adj) + est(V)", "lesson": 10},
            {"latin": "Puer audax currit.", "translation": "El niño audaz corre.", "analysis": "Puer(Nom) + audax(Adj) + currit(V)", "lesson": 10},
            {"latin": "Iter est facile.", "translation": "El viaje es fácil.", "analysis": "Iter(Nom) + est(V) + facile(Adj)", "lesson": 10},
            {"latin": "Dux militibus fortibus praemia dat.", "translation": "El líder da premios a los soldados valientes.", "analysis": "Dux(Nom) + militibus fortibus(Dat) + praemia(Ac) + dat(V)", "lesson": 10},
        ]

        all_vocab = l6_vocab + l7_vocab + l8_vocab + l9_vocab + l10_vocab
        all_sentences = l6_sentences + l7_sentences + l8_sentences + l9_sentences + l10_sentences

        # Process Vocabulary
        for item in all_vocab:
            # 1. Check if word exists or create it
            word = session.exec(select(Word).where(Word.latin == item["latin"])).first()
            if not word:
                word = Word(
                    latin=item["latin"], 
                    translation=item["translation"], 
                    part_of_speech=item["pos"],
                    cultural_context=item.get("cultural_context")
                )
                session.add(word)
                session.commit()
                session.refresh(word)
            else:
                # Update existing word with cultural context if missing
                if item.get("cultural_context") and not word.cultural_context:
                    word.cultural_context = item.get("cultural_context")
                    session.add(word)
                    session.commit()
            
            # 2. Link to Lesson
            link = session.exec(select(LessonVocabulary).where(
                LessonVocabulary.word_id == word.id,
                LessonVocabulary.lesson_number == item["lesson"]
            )).first()
            
            if not link:
                link = LessonVocabulary(word_id=word.id, lesson_number=item["lesson"], is_core=True)
                session.add(link)
                print(f"Added vocab: {item['latin']} to Lesson {item['lesson']}")

        # Process Sentences
        for item in all_sentences:
            sent = session.exec(select(SentenceAnalysis).where(
                SentenceAnalysis.latin_text == item["latin"],
                SentenceAnalysis.lesson_number == item["lesson"]
            )).first()
            
            if not sent:
                import json
                sent = SentenceAnalysis(
                    latin_text=item["latin"],
                    spanish_translation=item["translation"],
                    syntax_roles=json.dumps({"manual_analysis": item["analysis"]}),
                    lesson_number=item["lesson"],
                    complexity_level=1,
                    usage_type="translation_exercise" # Explicitly set usage type
                )
                session.add(sent)
                print(f"Added sentence: {item['latin']} to Lesson {item['lesson']}")

        session.commit()
        print("Seeding complete!")

if __name__ == "__main__":
    seed_l6_l10()
