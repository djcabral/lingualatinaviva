"""
Script para expandir vocabulario de lecciones L3-L30.
Objetivo: Asegurar que todas las lecciones tengan >= 15 palabras de vocabulario.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database import get_session, Word, LessonVocabulary
from sqlmodel import select

# Vocabulario adicional por lección - DATOS COMPLETOS
# Sustantivos: (latin, translation, pos, genitive, gender, declension)
# Verbos: (latin, translation, pos, principal_parts, conjugation, notes)
# Adjetivos: (latin, translation, pos, genitive/form, gender, declension)
EXPANSION_VOCABULARY = {
    3: [  # 1ª Declinación - añadir 7 (actual: 8) - Sustantivos femeninos en -a
        ("silva", "bosque/selva", "noun", "silvae", "femenino", "1"),
        ("patria", "patria", "noun", "patriae", "femenino", "1"),
        ("terra", "tierra", "noun", "terrae", "femenino", "1"),
        ("aqua", "agua", "noun", "aquae", "femenino", "1"),
        ("nauta", "marinero", "noun", "nautae", "masculino", "1"),  # Masc. en -a
        ("poeta", "poeta", "noun", "poetae", "masculino", "1"),  # Masc. en -a
        ("incola", "habitante", "noun", "incolae", "masculino", "1"),  # Masc. en -a
    ],
    4: [  # 2ª Declinación - añadir 5 (actual: 10) - Sustantivos masculinos en -us
        ("amicus", "amigo", "noun", "amici", "masculino", "2"),
        ("servus", "esclavo/siervo", "noun", "servi", "masculino", "2"),
        ("filius", "hijo", "noun", "filii", "masculino", "2"),
        ("populus", "pueblo", "noun", "populi", "masculino", "2"),
        ("animus", "ánimo/alma", "noun", "animi", "masculino", "2"),
    ],
    5: [  # Neutro - añadir 2 (actual: 14) - Neutros en -um
        ("signum", "señal/estandarte", "noun", "signi", "neutro", "2"),
        ("regnum", "reino", "noun", "regni", "neutro", "2"),
    ],
    8: [  # 4ª Declinación - añadir 4 (actual: 12)
        ("manus", "mano", "noun", "manus", "femenino", "4"),
        ("domus", "casa", "noun", "domus", "femenino", "4"),  # Irregular
        ("cornu", "cuerno", "noun", "cornus", "neutro", "4"),
        ("genu", "rodilla", "noun", "genus", "neutro", "4"),
    ],
    9: [  # 5ª Declinación - añadir 6 (actual: 9)
        ("dies", "día", "noun", "diei", "masculino", "5"),
        ("res", "cosa/asunto", "noun", "rei", "femenino", "5"),
        ("spes", "esperanza", "noun", "spei", "femenino", "5"),
        ("fides", "fe/fidelidad", "noun", "fidei", "femenino", "5"),
        ("facies", "cara/aspecto", "noun", "faciei", "femenino", "5"),
        ("species", "aspecto/especie", "noun", "speciei", "femenino", "5"),
    ],
    10: [  # Adjetivos 2ª Clase (3ª decl.) - añadir 6 (actual: 9)
        ("brevis", "breve/corto", "adjective", "brevis, breve", "masculino", "3"),
        ("levis", "leve/ligero", "adjective", "levis, leve", "masculino", "3"),
        ("dulcis", "dulce", "adjective", "dulcis, dulce", "masculino", "3"),
        ("felix", "feliz/afortunado", "adjective", "felicis", "masculino", "3"),
        ("ingens", "enorme", "adjective", "ingentis", "masculino", "3"),
        ("audax", "audaz", "adjective", "audacis", "masculino", "3"),
    ],
    11: [  # Comparación - añadir 3 (actual: 13)
        ("longior", "más largo", "adjective", "longioris", "masculino", "3"),
        ("brevior", "más breve", "adjective", "brevioris", "masculino", "3"),
        ("celerior", "más rápido", "adjective", "celerioris", "masculino", "3"),
    ],
    13: [  # Voz Pasiva y Ablativo - añadir 8 verbos transitivos (actual: 7)
        ("rego", "gobernar/dirigir", "verb", "rego, regere, rexi, rectum", "3", None),
        ("vinco", "vencer", "verb", "vinco, vincere, vici, victum", "3", None),
        ("traho", "arrastrar/llevar", "verb", "traho, trahere, traxi, tractum", "3", None),
        ("condo", "fundar/guardar", "verb", "condo, condere, condidi, conditum", "3", None),
        ("neco", "matar", "verb", "neco, necare, necavi, necatum", "1", None),
        ("laboro", "trabajar", "verb", "laboro, laborare, laboravi, laboratum", "1", None),
        ("duco", "conducir/guiar", "verb", "duco, ducere, duxi, ductum", "3", None),
        ("capio", "capturar/tomar", "verb", "capio, capere, cepi, captum", "3io", None),
    ],
    14: [  # Pluscuamperfecto - añadir 4 (actual: 11)
        ("coepi", "empezar (defectivo)", "verb", "coepi, coepisse, coeptum", "defectivo", None),
        ("desino", "cesar/dejar de", "verb", "desino, desinere, desii, desitum", "3", None),
        ("reddo", "devolver/hacer", "verb", "reddo, reddere, reddidi, redditum", "3", None),
        ("trado", "entregar/transmitir", "verb", "trado, tradere, tradidi, traditum", "3", None),
    ],
    15: [  # Pasiva Infectum - añadir 10 verbos regulares (actual: 5)
        ("curo", "cuidar", "verb", "curo, curare, curavi, curatum", "1", None),
        ("paro", "preparar", "verb", "paro, parare, paravi, paratum", "1", None),
        ("monstro", "mostrar", "verb", "monstro, monstrare, monstravi, monstratum", "1", None),
        ("libero", "liberar", "verb", "libero, liberare, liberavi, liberatum", "1", None),
        ("servo", "guardar/salvar", "verb", "servo, servare, servavi, servatum", "1", None),
        ("terreo", "aterrorizar", "verb", "terreo, terrere, terrui, territum", "2", None),
        ("doceo", "enseñar", "verb", "doceo, docere, docui, doctum", "2", None),
        ("moveo", "mover", "verb", "moveo, movere, movi, motum", "2", None),
        ("teneo", "tener/sostener", "verb", "teneo, tenere, tenui, tentum", "2", None),
        ("iubeo", "ordenar/mandar", "verb", "iubeo, iubere, iussi, iussum", "2", None),
    ],
    16: [  # Pasiva Perfectum - añadir 10 verbos (actual: 5)
        ("facio", "hacer", "verb", "facio, facere, feci, factum", "3io", None),
        ("rapio", "arrebatar", "verb", "rapio, rapere, rapui, raptum", "3io", None),
        ("iacio", "lanzar/arrojar", "verb", "iacio, iacere, ieci, iactum", "3io", None),
        ("fugio", "huir", "verb", "fugio, fugere, fugi, fugitum", "3io", None),
        ("audio", "oír/escuchar", "verb", "audio, audire, audivi, auditum", "4", None),
        ("venio", "venir", "verb", "venio, venire, veni, ventum", "4", None),
        ("punio", "castigar", "verb", "punio, punire, punivi, punitum", "4", None),
        ("finio", "terminar/limitar", "verb", "finio, finire, finivi, finitum", "4", None),
        ("aperio", "abrir", "verb", "aperio, aperire, aperui, apertum", "4", None),
        ("sentio", "sentir", "verb", "sentio, sentire, sensi, sensum", "4", None),
    ],
    17: [  # Deponentes - añadir 3 (actual: 12)
        ("conor", "intentar", "verb", "conor, conari, conatus sum", "1", "deponente"),
        ("imitor", "imitar", "verb", "imitor, imitari, imitatus sum", "1", "deponente"),
        ("precor", "rogar/rezar", "verb", "precor, precari, precatus sum", "1", "deponente"),
    ],
    18: [  # Subjuntivo I - añadir 4 impersonales (actual: 11)
        ("iuvat", "agrada", "verb", "iuvat, iuvare, iuvit (impersonal)", "1", "impersonal"),
        ("oportet", "es necesario", "verb", "oportet, oportere, oportuit", "2", "impersonal"),
        ("licet", "es lícito/permitido", "verb", "licet, licere, licuit", "2", "impersonal"),
        ("decet", "es conveniente", "verb", "decet, decere, decuit", "2", "impersonal"),
    ],
    19: [  # Subjuntivo II - añadir 7 (actual: 8)
        ("concedo", "conceder/ceder", "verb", "concedo, concedere, concessi, concessum", "3", None),
        ("accido", "suceder/caer", "verb", "accido, accidere, accidi", "3", None),
        ("contendo", "esforzarse/competir", "verb", "contendo, contendere, contendi, contentum", "3", None),
        ("expecto", "esperar", "verb", "expecto, expectare, expectavi, expectatum", "1", None),
        ("dubito", "dudar", "verb", "dubito, dubitare, dubitavi, dubitatum", "1", None),
        ("sino", "permitir", "verb", "sino, sinere, sivi, situm", "3", None),
        ("cogo", "obligar/reunir", "verb", "cogo, cogere, coegi, coactum", "3", None),
    ],
    20: [  # Infinitivos - añadir 2 (actual: 13)
        ("arbitror", "opinar/juzgar", "verb", "arbitror, arbitrari, arbitratus sum", "1", "deponente"),
        ("existimo", "considerar/pensar", "verb", "existimo, existimare, existimavi, existimatum", "1", None),
    ],
    21: [  # Participios - añadir 5 (actual: 10)
        ("videns", "viendo/que ve", "participle", "videntis", "masculino", "3"),
        ("scribens", "escribiendo", "participle", "scribentis", "masculino", "3"),
        ("auditus", "oído (part. perf. pas.)", "participle", None, "masculino", "1/2"),
        ("monitus", "advertido", "participle", None, "masculino", "1/2"),
        ("missus", "enviado", "participle", None, "masculino", "1/2"),
    ],
    22: [  # Ablativo Absoluto - añadir 5 participios perfectos (actual: 10)
        ("captus", "capturado", "participle", None, "masculino", "1/2"),
        ("victus", "vencido", "participle", None, "masculino", "1/2"),
        ("finitus", "terminado", "participle", None, "masculino", "1/2"),
        ("interfectus", "matado", "participle", None, "masculino", "1/2"),
        ("profectus", "partido/habiendo partido", "participle", None, "masculino", "1/2"),
    ],
    23: [  # Gerundio y Gerundivo - añadir 5 (actual: 10)
        ("legendus", "que debe leerse", "gerundive", None, "masculino", "1/2"),
        ("audiendus", "que debe oírse", "gerundive", None, "masculino", "1/2"),
        ("scribendus", "que debe escribirse", "gerundive", None, "masculino", "1/2"),
        ("petendus", "que debe buscarse", "gerundive", None, "masculino", "1/2"),
        ("docendus", "que debe enseñarse", "gerundive", None, "masculino", "1/2"),
    ],
    24: [  # Perifrásticas - añadir 5 participios futuros activos (actual: 10)
        ("scripturus", "que va a escribir", "participle", None, "masculino", "1/2"),
        ("dicturus", "que va a decir", "participle", None, "masculino", "1/2"),
        ("facturus", "que va a hacer", "participle", None, "masculino", "1/2"),
        ("pugnaturus", "que va a luchar", "participle", None, "masculino", "1/2"),
        ("auditurus", "que va a oír", "participle", None, "masculino", "1/2"),
    ],
    25: [  # Coordinación - añadir 3 conjunciones (actual: 12)
        ("vel", "o (alternativa suave)", "conjunction", None, None, None),
        ("sive", "o si / ya sea que", "conjunction", None, None, None),
        ("itaque", "así pues/por tanto", "conjunction", None, None, None),
    ],
    26: [  # Completivas - añadir 5 verbos de cabeza (actual: 10)
        ("credo", "creer", "verb", "credo, credere, credidi, creditum", "3", None),
        ("promitto", "prometer", "verb", "promitto, promittere, promisi, promissum", "3", None),
        ("spero", "esperar", "verb", "spero, sperare, speravi, speratum", "1", None),
        ("cupio", "desear", "verb", "cupio, cupere, cupivi, cupitum", "3io", None),
        ("timeo", "temer", "verb", "timeo, timere, timui", "2", None),
    ],
    27: [  # Condicionales - añadir 5 conjunciones (actual: 10)
        ("modo", "con tal que", "conjunction", None, None, None),
        ("siquidem", "puesto que", "conjunction", None, None, None),
        ("quandoquidem", "puesto que", "conjunction", None, None, None),
        ("velut", "como si", "conjunction", None, None, None),
        ("tamquam", "como si", "conjunction", None, None, None),
    ],
    28: [  # Adverbiales - añadir 6 conjunciones temporales/causales (actual: 9)
        ("cum", "cuando/puesto que", "conjunction", None, None, None),
        ("ubi", "cuando/donde", "conjunction", None, None, None),
        ("antequam", "antes de que", "conjunction", None, None, None),
        ("priusquam", "antes de que", "conjunction", None, None, None),
        ("donec", "hasta que/mientras", "conjunction", None, None, None),
        ("dum", "mientras/hasta que", "conjunction", None, None, None),
    ],
    29: [  # Estilo Indirecto - añadir 6 verbos de decir/pensar (actual: 9)
        ("affirmo", "afirmar", "verb", "affirmo, affirmare, affirmavi, affirmatum", "1", None),
        ("demonstro", "demostrar", "verb", "demonstro, demonstrare, demonstravi, demonstratum", "1", None),
        ("polliceor", "prometer", "verb", "polliceor, polliceri, pollicitus sum", "2", "deponente"),
        ("testor", "atestiguar", "verb", "testor, testari, testatus sum", "1", "deponente"),
        ("aio", "decir/afirmar (defect.)", "verb", "aio, ait (defectivo)", "defectivo", None),
        ("mentior", "mentir", "verb", "mentior, mentiri, mentitus sum", "4", "deponente"),
    ],
    30: [  # Verbos Irregulares - añadir 6 compuestos de eo/fero (actual: 9)
        ("adeo", "acercarse/ir a", "verb", "adeo, adire, adii, aditum", "irregular", None),
        ("abeo", "irse/alejarse", "verb", "abeo, abire, abii, abitum", "irregular", None),
        ("ineo", "entrar/comenzar", "verb", "ineo, inire, inii, initum", "irregular", None),
        ("transeo", "cruzar/pasar", "verb", "transeo, transire, transii, transitum", "irregular", None),
        ("aufero", "llevarse/quitar", "verb", "aufero, auferre, abstuli, ablatum", "irregular", None),
        ("effero", "sacar/elevar", "verb", "effero, efferre, extuli, elatum", "irregular", None),
    ],
}


def expand_vocabulary():
    """Añade vocabulario faltante a las lecciones deficitarias."""
    print("🌱 Iniciando expansión de vocabulario L3-L30...")
    
    added_count = 0
    skipped_count = 0
    
    with get_session() as session:
        for lesson_num, words in EXPANSION_VOCABULARY.items():
            print(f"\n  📚 Lección {lesson_num}: procesando {len(words)} palabras...")
            
            for i, word_data in enumerate(words):
                latin, trans, pos, gen_or_parts, gender, decl = word_data
                
                # Buscar si ya existe
                word = session.exec(select(Word).where(Word.latin == latin)).first()
                
                if not word:
                    # Determinar campos según tipo de palabra
                    if pos == "verb":
                        word = Word(
                            latin=latin,
                            translation=trans,
                            part_of_speech=pos,
                            principal_parts=gen_or_parts,
                            conjugation=gender,  # En verbos, el 5to campo es la conjugación
                            definition_es=trans,
                            level=lesson_num // 10 + 1  # Nivel aproximado
                        )
                    elif pos in ["noun", "adjective", "participle", "gerundive"]:
                        word = Word(
                            latin=latin,
                            translation=trans,
                            part_of_speech=pos,
                            genitive=gen_or_parts,
                            gender=gender,
                            declension=decl,
                            definition_es=trans,
                            level=lesson_num // 10 + 1
                        )
                    elif pos == "conjunction":
                        word = Word(
                            latin=latin,
                            translation=trans,
                            part_of_speech=pos,
                            is_invariable=True,
                            category="conjunction",
                            definition_es=trans,
                            level=lesson_num // 10 + 1
                        )
                    else:
                        word = Word(
                            latin=latin,
                            translation=trans,
                            part_of_speech=pos,
                            definition_es=trans,
                            level=lesson_num // 10 + 1
                        )
                    
                    session.add(word)
                    session.commit()
                    session.refresh(word)
                    print(f"    + Añadida: {latin}")
                else:
                    # Actualizar campos vacíos si existen
                    updated = False
                    if not word.definition_es:
                        word.definition_es = trans
                        updated = True
                    if pos == "verb" and not word.principal_parts and gen_or_parts:
                        word.principal_parts = gen_or_parts
                        updated = True
                    if updated:
                        session.add(word)
                        session.commit()
                
                # Vincular a la lección
                link = session.exec(
                    select(LessonVocabulary)
                    .where(
                        LessonVocabulary.lesson_number == lesson_num,
                        LessonVocabulary.word_id == word.id
                    )
                ).first()
                
                if not link:
                    # Obtener el máximo orden actual para esta lección
                    existing_max = session.exec(
                        select(LessonVocabulary.presentation_order)
                        .where(LessonVocabulary.lesson_number == lesson_num)
                        .order_by(LessonVocabulary.presentation_order.desc())
                    ).first() or 0
                    
                    link = LessonVocabulary(
                        lesson_number=lesson_num,
                        word_id=word.id,
                        is_essential=True,
                        presentation_order=existing_max + 1 + i
                    )
                    session.add(link)
                    added_count += 1
                else:
                    skipped_count += 1
        
        session.commit()
    
    print(f"\n✅ Expansión completada:")
    print(f"   - Nuevas asociaciones: {added_count}")
    print(f"   - Ya existentes (omitidas): {skipped_count}")
    print(f"\n🔍 Ejecuta 'python database/utils/auditor_contenido.py' para verificar.")


if __name__ == "__main__":
    expand_vocabulary()
