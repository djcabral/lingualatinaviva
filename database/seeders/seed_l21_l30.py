"""
Seeder para Lecciones 21-30
Pobla vocabulario esencial y oraciones de traducción para temas avanzados.
"""
from database import get_session, Word, LessonVocabulary, SentenceAnalysis
from sqlmodel import select

# Vocabulario por lección
# (latin, translation, part_of_speech, genitive, gender, declension/conjugation)
LESSON_VOCABULARY = {
    21: [ # Participios
        ("currens", "corriendo/que corre", "participle", "currentis", "masculino", "3"),
        ("legens", "leyendo/que lee", "participle", "legentis", "masculino", "3"),
        ("amans", "amante/que ama", "participle", "amantis", "masculino", "3"),
        ("capto", "capturar/tomar", "verb", "capere, cepi, captum", "3io", None),
        ("incendo", "incendiar/quemar", "verb", "incendere, incendi, incensum", "3", None),
        ("cado", "caer", "verb", "cadere, cecidi, casum", "3", None),
        ("saluto", "saludar", "verb", "salutare, salutavi, salutatum", "1", None),
        ("gladiator", "gladiador", "noun", "gladiatoris", "masculino", "3"),
        ("nuntius", "mensajero/mensaje", "noun", "nuntii", "masculino", "2"),
        ("venturus", "que va a venir (fut. activo)", "participle", None, "masculino", "1/2"),
    ],
    22: [ # Ablativo Absoluto
        ("orior", "salir/levantarse", "verb", "oriri, ortus sum", "4", "deponente"),
        ("dux", "jefe/general", "noun", "ducis", "masculino", "3"),
        ("taceo", "callar", "verb", "tacere, tacui, tacitum", "2", None),
        ("cognosco", "conocer/enterarse", "verb", "cognoscere, cognovi, cognitum", "3", None),
        ("exercitus", "ejército", "noun", "exercitus", "masculino", "4"),
        ("eloquens", "elocuente", "adjective", "eloquentis", "masculino", "3"),
        ("rex", "rey", "noun", "regis", "masculino", "3"),
        ("hostis", "enemigo", "noun", "hostis", "masculino", "3"),
        ("audiens", "escuchando/oyente", "participle", "audientis", "masculino", "3"),
        ("mortuus", "muerto", "participle", None, "masculino", "1/2"),
    ],
    23: [ # Gerundio y Gerundivo
        ("cupidus", "deseoso", "adjective", None, "masculino", "1/2"),
        ("peritus", "experto/hábil", "adjective", None, "masculino", "1/2"),
        ("causa", "causa/razón", "noun", "causae", "femenino", "1"),
        ("gratia", "gracia/favor", "noun", "gratiae", "femenino", "1"),
        ("studium", "estudio/empeño", "noun", "studii", "neutro", "2"),
        ("virtus", "virtud/valor", "noun", "virtutis", "femenino", "3"),
        ("labor", "trabajo/esfuerzo", "noun", "laboris", "masculino", "3"),
        ("petitio", "petición", "noun", "petitionis", "femenino", "3"),
        ("paratus", "preparado", "adjective", None, "masculino", "1/2"),
        ("idoneus", "idóneo/apto", "adjective", None, "masculino", "1/2"),
    ],
    24: [ # Conjugaciones Perifrásticas
        ("gero", "llevar a cabo", "verb", "gerere, gessi, gestum", "3", None),
        ("servo", "guardar/conservar", "verb", "servare, servavi, servatum", "1", None),
        ("colo", "cultivar/honrar", "verb", "colere, colui, cultum", "3", None),
        ("deleo", "destruir", "verb", "delere, delevi, deletum", "2", None),
        ("debeo", "deber", "verb", "debere, debui, debitum", "2", None),
        ("necesse", "necesario", "adjective", None, "neutro", "indeclinable"),
        ("opus", "obra/trabajo", "noun", "operis", "neutro", "3"),
        ("lex", "ley", "noun", "legis", "femenino", "3"),
        ("religio", "religión/escrúpulo", "noun", "religionis", "femenino", "3"),
        ("fugio", "huir", "verb", "fugere, fugi, fugitum", "3io", None),
    ],
    25: [ # Coordinación y Subordinadas
        ("atque", "y además", "conjunction", None, None, None),
        ("neque", "y no/ni", "conjunction", None, None, None),
        ("autem", "pero/en cambio", "conjunction", None, None, None),
        ("ergo", "por tanto/luego", "conjunction", None, None, None),
        ("igitur", "así pues", "conjunction", None, None, None),
        ("nam", "pues/porque", "conjunction", None, None, None),
        ("enim", "pues/en efecto", "conjunction", None, None, None),
        ("postquam", "después de que", "conjunction", None, None, None),
        ("quod", "porque", "conjunction", None, None, None),
        ("quia", "porque", "conjunction", None, None, None),
        ("quoniam", "porque/puesto que", "conjunction", None, None, None),
        ("corrompo", "corromper", "verb", "corrumpere, corrupi, corruptum", "3", None),
    ],
    26: [ # Completivas y Finales
        ("impero", "mandar/ordenar", "verb", "imperare, imperavi, imperatum", "1", None),
        ("oro", "rogar/orar", "verb", "orare, oravi, oratum", "1", None),
        ("metuo", "temer", "verb", "metuere, metui", "3", None),
        ("defendo", "defender", "verb", "defendere, defendi, defensum", "3", None),
        ("claudo", "cerrar", "verb", "claudere, clausi, clausum", "3", None),
        ("intro", "entrar", "verb", "intrare, intravi, intratum", "1", None),
        ("oppugno", "atacar", "verb", "oppugnare, oppugnavi, oppugnatum", "1", None),
        ("ardor", "calor/ardor", "noun", "ardoris", "masculino", "3"),
        ("herba", "hierba", "noun", "herbae", "femenino", "1"),
        ("aresco", "secarse", "verb", "arescere, arui", "3", None),
    ],
    27: [ # Condicionales
        ("nisi", "si no/a menos que", "conjunction", None, None, None),
        ("dummodo", "con tal que", "conjunction", None, None, None),
        ("sin", "pero si", "conjunction", None, None, None),
        ("memini", "acordarse", "verb", "meminisse", "defectivo", None),
        ("odi", "odiar", "verb", "odisse", "defectivo", None),
        ("novi", "conocer", "verb", "novisse", "defectivo", None),
        ("eventus", "resultado/evento", "noun", "eventus", "masculino", "4"),
        ("conditio", "condición", "noun", "conditionis", "femenino", "3"),
        ("sapiens", "sabio", "adjective", "sapientis", "masculino", "3"),
        ("prudens", "prudente", "adjective", "prudentis", "masculino", "3"),
    ],
    28: [ # Concesivas y Relativas
        ("quamquam", "aunque", "conjunction", None, None, None),
        ("quamvis", "aunque/por más que", "conjunction", None, None, None),
        ("etsi", "aunque", "conjunction", None, None, None),
        ("licet", "aunque", "conjunction", None, None, None),
        ("antecedo", "preceder/superar", "verb", "antecedere, antecessi, antecessum", "3", None),
        ("cedo", "ceder/retirarse", "verb", "cedere, cessi, cessum", "3", None),
        ("vinculum", "vínculo/cadena", "noun", "vinculi", "neutro", "2"),
        ("impedimentum", "impedimento", "noun", "impedimenti", "neutro", "2"),
        ("obstaculum", "obstáculo", "noun", "obstaculi", "neutro", "2"),
    ],
    29: [ # Estilo Indirecto
        ("fama", "fama/rumor", "noun", "famae", "femenino", "1"),
        ("nuntio", "anunciar", "verb", "nuntiare, nuntiavi, nuntiatum", "1", None),
        ("refero", "referir/informar", "verb", "referre, rettuli, relatum", "irregular", None),
        ("inquit", "dice", "verb", "inquit (defectivo)", "defectivo", None),
        ("respondeo", "responder", "verb", "respondere, respondi, responsum", "2", None),
        ("interrogo", "preguntar", "verb", "interrogare, interrogavi, interrogatum", "1", None),
        ("certus", "cierto/seguro", "adjective", None, "masculino", "1/2"),
        ("dubius", "dudoso", "adjective", None, "masculino", "1/2"),
        ("legatus", "legado/embajador", "noun", "legati", "masculino", "2"),
    ],
    30: [ # Verbos Irregulares Avanzados
        ("fio", "ser hecho/convertirse", "verb", "fieri, factus sum", "irregular", "pasiva de facio"),
        ("fero", "llevar/soportar", "verb", "ferre, tuli, latum", "irregular", None),
        ("eo", "ir", "verb", "ire, ii/ivi, itum", "irregular", None),
        ("redeo", "regresar", "verb", "redire, redii, reditum", "irregular", None),
        ("exeo", "salir", "verb", "exire, exii, exitum", "irregular", None),
        ("pereo", "perecer", "verb", "perire, perii, peritum", "irregular", None),
        ("tollo", "levantar/quitar", "verb", "tollere, sustuli, sublatum", "3", "irregular"),
        ("affero", "traer/llevar a", "verb", "afferre, attuli, allatum", "irregular", None),
        ("confero", "reunir/comparar", "verb", "conferre, contuli, collatum", "irregular", None),
    ]
}

# Oraciones de traducción (latin, spanish, complexity)
TRANSLATION_SENTENCES = {
    21: [
        ("Puer currens cecidit.", "El niño corriendo cayó.", 2),
        ("Video puellam legentem.", "Veo a la niña que lee.", 2),
        ("Milites pugnantes vicerunt.", "Los soldados que luchaban vencieron.", 3),
        ("Urbs capta incensa est.", "La ciudad capturada fue quemada.", 3),
        ("Poeta laudatus felix erat.", "El poeta alabado era feliz.", 2),
        ("Ave, Caesar, morituri te salutant.", "Salve, César, los que van a morir te saludan.", 3),
        ("Nuntii venturi sunt.", "Los mensajeros están por llegar.", 2),
        ("Liber lectus bonus est.", "El libro leído es bueno.", 2),
        ("Consul urbem videns laetus erat.", "El cónsul viendo la ciudad estaba contento.", 3),
        ("Hostes fugientes victi sunt.", "Los enemigos que huían fueron vencidos.", 3),
    ],
    22: [
        ("Sole oriente, aves canunt.", "Al salir el sol, las aves cantan.", 3),
        ("Urbe capta, hostes redierunt.", "Capturada la ciudad, los enemigos regresaron.", 3),
        ("Me consule, pax erat.", "Siendo yo cónsul, había paz.", 3),
        ("Caesare duce, Romani vincebant.", "Siendo César el jefe, los romanos vencían.", 3),
        ("Me tacente, tu loquebaris.", "Callando yo, tú hablabas.", 3),
        ("His rebus cognitis, Caesar exercitum movit.", "Conocidas estas cosas, César movió el ejército.", 4),
        ("Vivo patre, felix sum.", "Viviendo el padre, soy feliz.", 2),
        ("Romanis pugnantibus, hostes fugerunt.", "Luchando los romanos, los enemigos huyeron.", 3),
        ("Caesare mortuo, Marcus consul factus est.", "Muerto César, Marco fue hecho cónsul.", 3),
        ("Omnibus audientibus, orator dixit.", "Escuchando todos, el orador habló.", 3),
    ],
    23: [
        ("Ars amandi difficilis est.", "El arte de amar es difícil.", 2),
        ("Paratus ad pugnandum est.", "Está preparado para luchar.", 2),
        ("Discimus legendo.", "Aprendemos leyendo.", 1),
        ("Cupidus videndi urbem est.", "Está deseoso de ver la ciudad.", 2),
        ("Ad pacem petendam venerunt.", "Vinieron para pedir la paz.", 3),
        ("Tempus legendi est.", "Es tiempo de leer.", 1),
        ("Studiorum causa Romam venit.", "Vino a Roma por causa de los estudios.", 3),
        ("Virtus laudanda est.", "La virtud debe ser alabada.", 2),
        ("Liber legendus est.", "El libro debe ser leído.", 2),
        ("Peritus dicendi orator erat.", "Era un orador experto en hablar.", 3),
    ],
    24: [
        ("Pax agenda est.", "La paz debe ser hecha.", 2),
        ("Leges servandae sunt.", "Las leyes deben ser guardadas.", 2),
        ("Carthago delenda est.", "Cartago debe ser destruida.", 2),
        ("Legatus missurus est.", "El legado está por enviar.", 2),
        ("Puer scripturus erat.", "El niño iba a escribir.", 2),
        ("Dei colendi sunt.", "Los dioses deben ser honrados.", 2),
        ("Opus perfectum est.", "La obra está terminada.", 1),
        ("Hostes fugiendi sunt.", "Los enemigos deben ser evitados.", 2),
        ("Bellum gerendum erat.", "La guerra debía ser llevada a cabo.", 3),
        ("Moriendum est omnibus.", "Todos deben morir.", 2),
    ],
    25: [
        ("Venit et vidit et vicit.", "Vino y vio y venció.", 1),
        ("Senatus Populusque Romanus.", "El Senado y el Pueblo Romano.", 2),
        ("Non vivere sed valere vita est.", "La vida no es vivir sino estar sanos.", 3),
        ("Cogito, ergo sum.", "Pienso, luego existo.", 2),
        ("Cum Caesar in Galliam venisset, Romani laeti erant.", "Cuando César hubo llegado a la Galia, los romanos estaban contentos.", 4),
        ("Postquam urbs capta est, milites redierunt.", "Después de que la ciudad fue tomada, los soldados regresaron.", 3),
        ("Dum Romae sum, multos libros lego.", "Mientras estoy en Roma, leo muchos libros.", 2),
        ("Quod vales, gaudeo.", "Porque estás bien, me alegro.", 2),
        ("Socrates accusatus est quod corrumperet juventutem.", "Sócrates fue acusado porque corrompía a la juventud.", 4),
        ("Vincunt neque cedunt.", "Vencen y no ceden.", 2),
    ],
    26: [
        ("Impero tibi ut venias.", "Te ordeno que vengas.", 2),
        ("Oro te ne eas.", "Te ruego que no vayas.", 2),
        ("Edo ut vivam.", "Como para vivir.", 1),
        ("Tam stultus est ut nihil intelligat.", "Es tan tonto que no entiende nada.", 3),
        ("Milites pugnant ut urbem defendant.", "Los soldados luchan para defender la ciudad.", 3),
        ("Portas clausit ne hostes intrarent.", "Cerró las puertas para que no entraran los enemigos.", 3),
        ("Timeo ne hostes veniant.", "Temo que los enemigos vengan.", 2),
        ("Solis ardor tam magnus est ut herba arescat.", "El calor del sol es tan grande que la hierba se seca.", 4),
        ("Legatos misit ut pacem peterent.", "Envió embajadores para pedir la paz.", 3),
        ("Ita locutus est ut omnes flerent.", "Habló de tal modo que todos lloraban.", 3),
    ],
    27: [
        ("Si hoc faceres, felix esses.", "Si hicieras esto, serías feliz.", 3),
        ("Nisi pluat, ibimus.", "Si no llueve, iremos.", 2),
        ("Si me amavisti, laetus sum.", "Si me amaste, soy feliz.", 2),
        ("Si vivam, te videbo.", "Si viviere, te veré.", 2),
        ("Memento mori.", "Acuérdate de morir.", 2),
        ("Si sapiens esses, hoc non faceres.", "Si fueras sabio, no harías esto.", 3),
        ("Dummodo adsint, vincere possumus.", "Con tal que estén presentes, podemos vencer.", 3),
        ("Sin autem discesseris, dolebo.", "Pero si te hubieres marchado, me dolerá.", 3),
        ("Novi hominem.", "Conozco al hombre.", 1),
        ("Odi et amo.", "Odio y amo.", 1),
    ],
    28: [
        ("Quamquam pauper est, felix est.", "Aunque es pobre, es feliz.", 2),
        ("Quamvis fortis sit, non vincet.", "Aunque sea fuerte, no vencerá.", 3),
        ("Etsi tardus est, pervenit.", "Aunque es lento, llega.", 2),
        ("Licet pluat, ibo.", "Aunque llueva, iré.", 2),
        ("Qui bene amat, bene castigat.", "Quien bien ama, bien castiga.", 2),
        ("Quae utilitas, ea honestas.", "Lo que es útil, es honesto.", 3),
        ("Quod natura negat, nemo dare potest.", "Lo que la naturaleza niega, nadie puede dar.", 3),
        ("Vinculum amoris fortius est quam ferro.", "El vínculo del amor es más fuerte que el hierro.", 3),
        ("Etsi difficile est, facere debeo.", "Aunque es difícil, debo hacerlo.", 2),
        ("Quamquam multi impedimenta sunt, vincere volumus.", "Aunque hay muchos impedimentos, queremos vencer.", 3),
    ],
    29: [
        ("Caesar respondit se venturum esse.", "César respondió que vendría.", 3),
        ("Fama est Romam aeternam esse.", "Se dice que Roma es eterna.", 3),
        ("Nuntiat hostes appropinquare.", "Anuncia que los enemigos se acercan.", 2),
        ("Legatus refert milites vicisse.", "El legado informa que los soldados vencieron.", 3),
        ("Interrogavit quis esset.", "Preguntó quién era.", 2),
        ("Certum est eum mentiri.", "Es cierto que él miente.", 2),
        ("Dubium non est quin victor sit.", "No hay duda de que es el vencedor.", 3),
        ("Caesar inquit se non fugere.", "César dice que él no huye.", 3),
        ("Nuntiaverunt urbem captam esse.", "Anunciaron que la ciudad había sido capturada.", 3),
        ("Respondeo me hoc non fecisse.", "Respondo que yo no hice esto.", 2),
    ],
    30: [
        ("Omnia fieri possunt.", "Todo puede hacerse.", 2),
        ("Eo Romam.", "Voy a Roma.", 1),
        ("Redeo domum.", "Regreso a casa.", 1),
        ("Hostes perierunt.", "Los enemigos perecieron.", 2),
        ("Fero et ferior.", "Golpeo y soy golpeado.", 2),
        ("Tolle, lege.", "Toma, lee.", 1),
        ("Auxilium afferte!", "¡Traed ayuda!", 2),
        ("Confer haec cum illis.", "Compara estas cosas con aquellas.", 2),
        ("Exeunt omnes.", "Salen todos.", 1),
        ("Fiat lux.", "Hágase la luz.", 2),
    ]
}

# Oraciones para Análisis Sintáctico (latin, spanish, complexity, syntax_roles_map)
ANALYSIS_SENTENCES = {
    21: [
        {
            "latin": "Consul, urbem videns, laetus erat.",
            "spanish": "El cónsul, viendo la ciudad, estaba contento.",
            "complexity": 3,
            "roles": {
                "subject": ["Consul"],
                "verb": ["erat"],
                "participle": ["videns"],
                "direct_object": ["urbem"],
                "attribute": ["laetus"]
            }
        }
    ],
    22: [
        {
            "latin": "Sole oriente, consul laetus erat.",
            "spanish": "Al salir el sol, el cónsul estaba contento.",
            "complexity": 3,
            "roles": {
                "ablative_absolute": ["Sole", "oriente"],
                "subject": ["consul"],
                "verb": ["erat"],
                "attribute": ["laetus"]
            }
        }
    ],
    23: [
        {
            "latin": "Cupidus urbis videndae sum.",
            "spanish": "Estoy deseoso de ver la ciudad.",
            "complexity": 3,
            "roles": {
                "subject": ["Cupidus"],
                "verb": ["sum"],
                "genitive_gerundive": ["urbis", "videndae"]
            }
        }
    ],
    24: [
        {
            "latin": "Pugnandum est pro patria.",
            "spanish": "Se debe luchar por la patria.",
            "complexity": 3,
            "roles": {
                "gerundive_impersonal": ["Pugnandum"],
                "verb": ["est"],
                "prepositional_phrase": ["pro", "patria"]
            }
        }
    ],
    25: [
        {
            "latin": "Cum Caesar venisset, omnes gaudebant.",
            "spanish": "Cuando César hubo llegado, todos se alegraban.",
            "complexity": 3,
            "roles": {
                "conjunction": ["Cum"],
                "subject": ["Caesar", "omnes"],
                "verb": ["venisset", "gaudebant"]
            }
        }
    ],
    26: [
        {
            "latin": "Milites pugnabant ut urbem defenderent.",
            "spanish": "Los soldados luchaban para defender la ciudad.",
            "complexity": 3,
            "roles": {
                "subject": ["Milites"],
                "verb": ["pugnabant", "defenderent"],
                "conjunction": ["ut"],
                "direct_object": ["urbem"]
            }
        }
    ],
    27: [
        {
            "latin": "Si hoc dixisses, erravisses.",
            "spanish": "Si hubieras dicho esto, te habrías equivocado.",
            "complexity": 3,
            "roles": {
                "conjunction": ["Si"],
                "verb": ["dixisses", "erravisses"],
                "direct_object": ["hoc"]
            }
        }
    ],
    28: [
        {
            "latin": "Quamquam pauper est, felix est.",
            "spanish": "Aunque es pobre, es feliz.",
            "complexity": 2,
            "roles": {
                "conjunction": ["Quamquam"],
                "verb": ["est", "est"],
                "attribute": ["pauper", "felix"]
            }
        }
    ],
    29: [
        {
            "latin": "Caesar dixit se Romam iturum esse.",
            "spanish": "César dijo que él iría a Roma.",
            "complexity": 4,
            "roles": {
                "subject": ["Caesar"],
                "verb": ["dixit"],
                "accusative_subject": ["se"],
                "future_infinitive": ["iturum", "esse"],
                "direct_object": ["Romam"]
            }
        }
    ],
    30: [
        {
            "latin": "Fiat voluntas tua.",
            "spanish": "Hágase tu voluntad.",
            "complexity": 2,
            "roles": {
                "verb": ["Fiat"],
                "subject": ["voluntas"],
                "possessive": ["tua"]
            }
        }
    ]
}

def get_indices_for_roles(latin_text, roles_map):
    """
    Helper para mapear palabras a sus índices en la oración.
    Retorna un diccionario JSON-serializable con los índices.
    """
    import json
    import re
    
    tokens = latin_text.split()
    clean_tokens = [re.sub(r'[.,;?!]', '', t).lower() for t in tokens]
    
    result_indices = {}
    
    for role, words in roles_map.items():
        indices = []
        for word in words:
            target = word.lower()
            for idx, token in enumerate(clean_tokens):
                if token == target:
                    indices.append(idx)
        
        if indices:
            result_indices[role] = list(set(indices))
            
    return json.dumps(result_indices)

def seed_lessons_21_30():
    print("🌱 Iniciando población de Lecciones 21-30...")
    
    with get_session() as session:
        # 1. Poblar Vocabulario
        for lesson_num, words in LESSON_VOCABULARY.items():
            print(f"  Procesando vocabulario Lección {lesson_num}...")
            
            for i, word_data in enumerate(words):
                latin, trans, pos, gen, gender, decl = word_data
                
                # Buscar si ya existe
                word = session.exec(select(Word).where(Word.latin == latin)).first()
                
                if not word:
                    # Crear nueva palabra
                    word = Word(
                        latin=latin,
                        translation=trans,
                        part_of_speech=pos,
                        genitive=gen,
                        gender=gender,
                        declension=decl if pos in ["noun", "adjective", "participle"] else None,
                        conjugation=decl if pos == "verb" else None,
                        definition_es=trans
                    )
                    session.add(word)
                    session.commit()
                    session.refresh(word)
                else:
                    # Actualizar si faltan datos
                    if not word.definition_es:
                        word.definition_es = trans
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
                    link = LessonVocabulary(
                        lesson_number=lesson_num,
                        word_id=word.id,
                        is_essential=True,
                        presentation_order=i
                    )
                    session.add(link)
        
        # 2. Poblar Oraciones de Traducción
        for lesson_num, sentences in TRANSLATION_SENTENCES.items():
            print(f"  Procesando oraciones Lección {lesson_num}...")
            
            for latin, spanish, complexity in sentences:
                # Verificar existencia
                exists = session.exec(
                    select(SentenceAnalysis)
                    .where(SentenceAnalysis.latin_text == latin)
                ).first()
                
                if not exists:
                    sentence = SentenceAnalysis(
                        latin_text=latin,
                        spanish_translation=spanish,
                        complexity_level=complexity,
                        lesson_number=lesson_num,
                        usage_type="translation_exercise",
                        sentence_type="simple"
                    )
                    session.add(sentence)
        
        # 3. Poblar Oraciones de Análisis
        print("  Procesando oraciones de Análisis Sintáctico...")
        for lesson_num, analysis_data in ANALYSIS_SENTENCES.items():
            for data in analysis_data:
                latin = data["latin"]
                
                exists = session.exec(
                    select(SentenceAnalysis)
                    .where(SentenceAnalysis.latin_text == latin)
                ).first()
                
                if not exists:
                    # Generar JSON de roles
                    roles_json = get_indices_for_roles(latin, data["roles"])
                    
                    sentence = SentenceAnalysis(
                        latin_text=latin,
                        spanish_translation=data["spanish"],
                        complexity_level=data["complexity"],
                        lesson_number=lesson_num,
                        usage_type="analysis",
                        sentence_type="complex",
                        syntax_roles=roles_json
                    )
                    session.add(sentence)
                    print(f"    + Agregada análisis: {latin[:30]}...")

        session.commit()
        print("✅ Población completada exitosamente.")

if __name__ == "__main__":
    seed_lessons_21_30()
