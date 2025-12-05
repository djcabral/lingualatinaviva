"""
Seeder para Lecciones 11-20
Pobla vocabulario esencial y oraciones de traducción.
"""
from database import get_session, Word, LessonVocabulary, SentenceAnalysis
from sqlmodel import select

# Vocabulario por lección
# (latin, translation, part_of_speech, genitive, gender, declension/conjugation)
LESSON_VOCABULARY = {
    11: [ # Comparativos
        ("altus", "alto", "adjective", None, "masculino", "1/2"),
        ("fortis", "fuerte", "adjective", None, "masculino", "3"),
        ("celer", "rápido", "adjective", None, "masculino", "3"),
        ("facilis", "fácil", "adjective", None, "masculino", "3"),
        ("difficilis", "difícil", "adjective", None, "masculino", "3"),
        ("pulcher", "hermoso", "adjective", None, "masculino", "1/2"),
        ("longus", "largo", "adjective", None, "masculino", "1/2"),
        ("brevis", "breve/corto", "adjective", None, "masculino", "3"),
        ("melior", "mejor", "adjective", None, "masculino", "comparativo"),
        ("pejor", "peor", "adjective", None, "masculino", "comparativo"),
        ("maior", "mayor", "adjective", None, "masculino", "comparativo"),
        ("minor", "menor", "adjective", None, "masculino", "comparativo"),
    ],
    12: [ # Pronombres
        ("ego", "yo", "pronoun", None, None, None),
        ("tu", "tú", "pronoun", None, None, None),
        ("nos", "nosotros", "pronoun", None, None, None),
        ("vos", "vosotros", "pronoun", None, None, None),
        ("hic", "este", "pronoun", None, "masculino", None),
        ("ille", "aquel", "pronoun", None, "masculino", None),
        ("ipse", "él mismo", "pronoun", None, "masculino", None),
        ("quis", "quién", "pronoun", None, "masculino", None),
        ("aliquis", "alguien", "pronoun", None, "masculino", None),
        ("nemo", "nadie", "pronoun", None, "masculino", None),
        ("nihil", "nada", "pronoun", None, "neutro", None),
        ("omnis", "todo", "adjective", None, "masculino", "3"),
        ("alius", "otro", "pronoun", None, "masculino", None),
    ],
    13: [ # Pasiva y Ablativo
        ("consilium", "consejo/plan", "noun", "consilii", "neutro", "2"),
        ("amor", "ser amado", "verb", "amari, amatus sum", "1", "pasiva"),
        ("videor", "parecer/ser visto", "verb", "videri, visus sum", "2", "pasiva"),
        ("ducor", "ser conducido", "verb", "duci, ductus sum", "3", "pasiva"),
        ("capior", "ser capturado", "verb", "capi, captus sum", "3io", "pasiva"),
        ("sine", "sin", "preposition", None, None, None),
        ("pro", "en favor de", "preposition", None, None, None),
    ],
    14: [ # Pluscuamperfecto
        ("iam", "ya", "adverb", None, None, None),
        ("nondum", "todavía no", "adverb", None, None, None),
        ("antea", "antes", "adverb", None, None, None),
        ("postea", "después", "adverb", None, None, None),
        ("olim", "antiguamente", "adverb", None, None, None),
        ("mox", "pronto", "adverb", None, None, None),
        ("statim", "inmediatamente", "adverb", None, None, None),
        ("tum", "entonces", "adverb", None, None, None),
        ("semper", "siempre", "adverb", None, None, None),
        ("numquam", "nunca", "adverb", None, None, None),
    ],
    15: [ # Pasiva Infectum
        ("ago", "hacer/actuar", "verb", "agere, egi, actum", "3", None),
        ("gero", "llevar a cabo", "verb", "gerere, gessi, gestum", "3", None),
        ("moveo", "mover", "verb", "movere, movi, motum", "2", None),
        ("teneo", "tener/sostener", "verb", "tenere, tenui, tentum", "2", None),
        ("peto", "pedir/buscar", "verb", "petere, petivi, petitum", "3", None),
    ],
    16: [ # Pasiva Perfectum
        ("quaero", "buscar/preguntar", "verb", "quaerere, quaesivi, quaesitum", "3", None),
        ("invenio", "encontrar", "verb", "invenire, inveni, inventum", "4", None),
        ("relinquo", "dejar/abandonar", "verb", "relinquere, reliqui, relictum", "3", None),
        ("accipio", "recibir", "verb", "accipere, accepi, acceptum", "3io", None),
        ("mitto", "enviar", "verb", "mittere, misi, missum", "3", None),
    ],
    17: [ # Deponentes
        ("loquor", "hablar", "verb", "loqui, locutus sum", "3", "deponente"),
        ("sequor", "seguir", "verb", "sequi, secutus sum", "3", "deponente"),
        ("utor", "usar", "verb", "uti, usus sum", "3", "deponente"),
        ("patior", "sufrir/soportar", "verb", "pati, passus sum", "3io", "deponente"),
        ("morior", "morir", "verb", "mori, mortuus sum", "3io", "deponente"),
        ("nascor", "nacer", "verb", "nasci, natus sum", "3", "deponente"),
        ("proficiscor", "partir/salir", "verb", "proficisci, profectus sum", "3", "deponente"),
        ("ingredior", "entrar", "verb", "ingredi, ingressus sum", "3io", "deponente"),
        ("egredior", "salir", "verb", "egredi, egressus sum", "3io", "deponente"),
        ("progredior", "avanzar", "verb", "progredi, progressus sum", "3io", "deponente"),
        ("audeo", "atreverse", "verb", "audere, ausus sum", "2", "semideponente"),
        ("gaudeo", "alegrarse", "verb", "gaudere, gavisus sum", "2", "semideponente"),
    ],
    18: [ # Subjuntivo
        ("volo", "querer", "verb", "velle, volui", "irregular", None),
        ("nolo", "no querer", "verb", "nolle, nolui", "irregular", None),
        ("malo", "preferir", "verb", "malle, malui", "irregular", None),
        ("cupio", "desear", "verb", "cupere, cupivi, cupitum", "3io", None),
        ("opto", "desear/escoger", "verb", "optare, optavi, optatum", "1", None),
        ("timeo", "temer", "verb", "timere, timui", "2", None),
        ("metuo", "temer", "verb", "metuere, metui", "3", None),
        ("oportet", "es necesario", "verb", "oportere, oportuit", "2", "impersonal"),
        ("licet", "es permitido", "verb", "licere, licuit", "2", "impersonal"),
        ("decet", "conviene", "verb", "decere, decuit", "2", "impersonal"),
    ],
    19: [ # Consecutio
        ("postquam", "después de que", "conjunction", None, None, None),
        ("simulac", "tan pronto como", "conjunction", None, None, None),
        ("priusquam", "antes de que", "conjunction", None, None, None),
        ("sentio", "sentir/percibir", "verb", "sentire, sensi, sensum", "4", None),
        ("intellego", "entender", "verb", "intellegere, intellexi, intellectum", "3", None),
        ("scio", "saber", "verb", "scire, scivi, scitum", "4", None),
        ("nescio", "no saber", "verb", "nescire, nescivi, nescitum", "4", None),
        ("cognosco", "conocer", "verb", "cognoscere, cognovi, cognitum", "3", None),
    ],
    20: [ # Infinitivos
        ("dico", "decir", "verb", "dicere, dixi, dictum", "3", None),
        ("nego", "negar", "verb", "negare, negavi, negatum", "1", None),
        ("puto", "pensar", "verb", "putare, putavi, putatum", "1", None),
        ("credo", "creer", "verb", "credere, credidi, creditum", "3", None),
        ("spero", "esperar", "verb", "sperare, speravi, speratum", "1", None),
        ("promitto", "prometer", "verb", "promittere, promisi, promissum", "3", None),
        ("constat", "consta/es evidente", "verb", "constare, constitit", "1", "impersonal"),
        ("apparet", "aparece/es claro", "verb", "apparere, apparuit", "2", "impersonal"),
        ("videtur", "parece", "verb", "videri, visus sum", "2", "pasiva"),
        ("veritas", "verdad", "noun", "veritatis", "femenino", "3"),
        ("mendacium", "mentira", "noun", "mendacii", "neutro", "2"),
        ("opinio", "opinión", "noun", "opinionis", "femenino", "3"),
    ]
}

# Oraciones de traducción (latin, spanish, complexity)
TRANSLATION_SENTENCES = {
    11: [
        ("Marcus altior quam Iulius est.", "Marco es más alto que Julio.", 1),
        ("Roma maior quam Athenae est.", "Roma es mayor que Atenas.", 2),
        ("Nihil est melius quam pax.", "Nada es mejor que la paz.", 2),
        ("Haec via longissima omnium est.", "Este camino es el más largo de todos.", 3),
        ("Fortissimi milites victoriam petunt.", "Los soldados más valientes buscan la victoria.", 3),
        ("Facilius est dicere quam facere.", "Es más fácil decir que hacer.", 2),
        ("Iulia pulcherrima puella est.", "Julia es una niña hermosísima.", 2),
        ("Hic liber difficilior illo est.", "Este libro es más difícil que aquel.", 3),
        ("Plures homines in urbe habitant.", "Más hombres habitan en la ciudad.", 2),
        ("Optimum consilium sequimur.", "Seguimos el mejor consejo.", 2),
    ],
    12: [
        ("Ego te amo.", "Yo te amo.", 1),
        ("Hic liber meus est, ille tuus.", "Este libro es mío, aquel es tuyo.", 2),
        ("Quis est ille vir?", "¿Quién es aquel hombre?", 1),
        ("Nemo hoc scit.", "Nadie sabe esto.", 1),
        ("Omnes cives pacem desiderant.", "Todos los ciudadanos desean la paz.", 2),
        ("Qui venit, amicus meus est.", "Quien viene es mi amigo.", 3),
        ("Ipse imperator milites ducit.", "El emperador mismo conduce a los soldados.", 2),
        ("Aliquis ianuam pulsat.", "Alguien golpea la puerta.", 2),
        ("Nihil novi sub sole.", "Nada nuevo bajo el sol.", 2),
        ("Uter consul victoriam reportavit?", "¿Cuál cónsul reportó la victoria?", 3),
    ],
    13: [
        ("Puella ab omnibus amatur.", "La niña es amada por todos.", 2),
        ("Urbs a militibus oppugnabatur.", "La ciudad era atacada por los soldados.", 3),
        ("Roma a Romulo condita est.", "Roma fue fundada por Rómulo.", 3),
        ("Liber cum diligentia legitur.", "El libro es leído con diligencia.", 2),
        ("Sine aqua vivere non possumus.", "No podemos vivir sin agua.", 2),
        ("De pace loquebantur.", "Hablaban acerca de la paz.", 2),
        ("Ex urbe profecti sunt.", "Partieron de la ciudad.", 2),
        ("Pro patria pugnant.", "Luchan por la patria.", 1),
        ("In bello multi cadunt.", "Muchos caen en la guerra.", 2),
        ("A Caesare consilium captum est.", "El plan fue tomado por César.", 3),
    ],
    14: [
        ("Antequam veni, iam discesserat.", "Antes de que vine, ya se había marchado.", 3),
        ("Cum puer fueram, ludebam.", "Cuando había sido niño, jugaba.", 2),
        ("Postquam epistulam legero, respondebo.", "Después de que habré leído la carta, responderé.", 3),
        ("Si hoc dixeris, errabis.", "Si hubieres dicho esto, te equivocarás.", 3),
        ("Olim Roma parva oppidum fuerat.", "Antiguamente Roma había sido un pueblo pequeño.", 2),
        ("Nondum cibum ceperant.", "Todavía no habían tomado alimento.", 2),
        ("Statim ad te venero.", "Inmediatamente habré venido a ti.", 2),
        ("Semper te amaveram.", "Siempre te había amado.", 1),
        ("Mox omnia confecero.", "Pronto habré terminado todo.", 2),
        ("Tum iam domum redierat.", "Entonces ya había regresado a casa.", 2),
    ],
    15: [
        ("Bellum a Romanis geritur.", "La guerra es llevada a cabo por los romanos.", 2),
        ("Castra moventur.", "El campamento es movido.", 1),
        ("Consilium bonum capitur.", "Un buen plan es tomado.", 2),
        ("Veritas quaeritur.", "La verdad es buscada.", 1),
        ("Puer a magistro docetur.", "El niño es enseñado por el maestro.", 2),
        ("Fabula narratur.", "La historia es narrada.", 1),
        ("Hostes videntur.", "Los enemigos son vistos.", 1),
        ("Voces audiuntur.", "Las voces son oídas.", 1),
        ("Librum legi.", "El libro es leído.", 1),
        ("Urbs defenditur.", "La ciudad es defendida.", 1),
    ],
    16: [
        ("Urbs capta est.", "La ciudad fue capturada.", 2),
        ("Hostes victi sunt.", "Los enemigos fueron vencidos.", 2),
        ("Epistula missa est.", "La carta fue enviada.", 2),
        ("Verba audita sunt.", "Las palabras fueron oídas.", 2),
        ("Consilium inventum est.", "El plan fue encontrado.", 2),
        ("Caesar occisus est.", "César fue asesinado.", 2),
        ("Milites laudati sunt.", "Los soldados fueron alabados.", 2),
        ("Opus confectum est.", "La obra fue terminada.", 2),
        ("Libri scripti sunt.", "Los libros fueron escritos.", 2),
        ("Porta aperta est.", "La puerta fue abierta.", 2),
    ],
    17: [
        ("Milites profecti sunt.", "Los soldados partieron.", 2),
        ("Hostes secuti sumus.", "Seguimos a los enemigos.", 2),
        ("Pueri in horto ludere gaudent.", "Los niños se alegran de jugar en el jardín.", 3),
        ("Nemo mori vult.", "Nadie quiere morir.", 2),
        ("Veritatem loquor.", "Hablo la verdad.", 1),
        ("Gladio usus est.", "Usó la espada.", 2),
        ("In urbem ingressi sunt.", "Entraron en la ciudad.", 2),
        ("Multa passus sum.", "Sufrí muchas cosas.", 2),
        ("Sole oriente proficiscemur.", "Partiremos al salir el sol.", 3),
        ("Aude sapere.", "Atrévete a saber.", 2),
    ],
    18: [
        ("Volo ut venias.", "Quiero que vengas.", 2),
        ("Timeo ne cadam.", "Temo caer.", 2),
        ("Oportet ut studeas.", "Es necesario que estudies.", 2),
        ("Cum sis bonus, te laudo.", "Como eres bueno, te alabo.", 3),
        ("Dum spiro, spero.", "Mientras respiro, espero.", 2),
        ("Opto ut sis felix.", "Deseo que seas feliz.", 2),
        ("Nolo ut discedas.", "No quiero que te marches.", 2),
        ("Licet tibi ire.", "Te es permitido ir.", 1),
        ("Metuo ut veniat.", "Temo que no venga.", 3),
        ("Cupio ut me ames.", "Deseo que me ames.", 2),
    ],
    19: [
        ("Scio te bonum esse.", "Sé que eres bueno.", 2),
        ("Dicit se venisse.", "Dice que ha venido.", 2),
        ("Putabam te dormire.", "Pensaba que dormías.", 2),
        ("Credo Deum esse.", "Creo que Dios existe.", 2),
        ("Audivi te aegrotare.", "Oí que estabas enfermo.", 3),
        ("Postquam venit, gaudebam.", "Después de que vino, me alegraba.", 2),
        ("Priusquam eas, dic mihi.", "Antes de que vayas, dime.", 3),
        ("Simulac vidit, credidit.", "Tan pronto como vio, creyó.", 2),
        ("Intellexi quid faceres.", "Entendí qué hacías.", 3),
        ("Nescio quis sis.", "No sé quién eres.", 2),
    ],
    20: [
        ("Errare humanum est.", "Errar es humano.", 1),
        ("Vincere scis, Hannibal.", "Sabes vencer, Aníbal.", 2),
        ("Dulce et decorum est pro patria mori.", "Dulce y decoroso es morir por la patria.", 3),
        ("Constat terram rotundam esse.", "Consta que la tierra es redonda.", 3),
        ("Promittit se venturum esse.", "Promete que vendrá.", 3),
        ("Spero te valere.", "Espero que estés bien.", 2),
        ("Videtur esse verum.", "Parece ser verdad.", 2),
        ("Negat se pecuniam cepisse.", "Niega haber tomado el dinero.", 3),
        ("Apparet eum mentiri.", "Aparece que él miente.", 2),
        ("Opinionem meam mutare nolo.", "No quiero cambiar mi opinión.", 2),
    ]
}

# Oraciones para Análisis Sintáctico (latin, spanish, complexity, syntax_roles_map)
# syntax_roles_map: Diccionario con palabras clave para buscar sus índices
ANALYSIS_SENTENCES = {
    11: [
        {
            "latin": "Frater meus est altior quam ego, sed ego sum celerior.",
            "spanish": "Mi hermano es más alto que yo, pero yo soy más rápido.",
            "complexity": 2,
            "roles": {
                "subject": ["Frater", "ego"],
                "verb": ["est", "sum"],
                "attribute": ["altior", "celerior"],
                "coordinator": ["sed"]
            }
        }
    ],
    12: [
        {
            "latin": "Ille, qui fortis est, non timet.",
            "spanish": "Aquel, que es fuerte, no teme.",
            "complexity": 2,
            "roles": {
                "subject": ["Ille", "qui"],
                "verb": ["est", "timet"],
                "attribute": ["fortis"],
                "negative": ["non"]
            }
        }
    ],
    13: [
        {
            "latin": "Milites a duce laudantur, quod fortiter pugnaverunt.",
            "spanish": "Los soldados son alabados por el líder, porque lucharon valientemente.",
            "complexity": 3,
            "roles": {
                "subject": ["Milites"],
                "verb": ["laudantur", "pugnaverunt"],
                "agent": ["a", "duce"],
                "conjunction": ["quod"],
                "adverb": ["fortiter"]
            }
        }
    ],
    14: [
        {
            "latin": "Postquam hostes fugerant, Caesar castra movit.",
            "spanish": "Después de que los enemigos habían huido, César movió el campamento.",
            "complexity": 3,
            "roles": {
                "subject": ["hostes", "Caesar"],
                "verb": ["fugerant", "movit"],
                "direct_object": ["castra"],
                "conjunction": ["Postquam"]
            }
        }
    ],
    15: [
        {
            "latin": "Dum libri leguntur, pueri silent.",
            "spanish": "Mientras los libros son leídos, los niños callan.",
            "complexity": 2,
            "roles": {
                "subject": ["libri", "pueri"],
                "verb": ["leguntur", "silent"],
                "conjunction": ["Dum"]
            }
        }
    ],
    16: [
        {
            "latin": "Urbe capta, milites gaudebant.",
            "spanish": "Capturada la ciudad, los soldados se alegraban.",
            "complexity": 3,
            "roles": {
                "subject": ["milites"],
                "verb": ["gaudebant"],
                "ablative_absolute": ["Urbe", "capta"]
            }
        }
    ],
    17: [
        {
            "latin": "Proficiscamur ad urbem ut amicos videamus.",
            "spanish": "Partamos a la ciudad para ver a los amigos.",
            "complexity": 3,
            "roles": {
                "verb": ["Proficiscamur", "videamus"],
                "direct_object": ["amicos"],
                "prepositional_phrase": ["ad", "urbem"],
                "conjunction": ["ut"]
            }
        }
    ],
    18: [
        {
            "latin": "Impero tibi ut venias.",
            "spanish": "Te ordeno que vengas.",
            "complexity": 2,
            "roles": {
                "verb": ["Impero", "venias"],
                "indirect_object": ["tibi"],
                "conjunction": ["ut"]
            }
        }
    ],
    19: [
        {
            "latin": "Nesciebam quis hoc fecisset.",
            "spanish": "No sabía quién había hecho esto.",
            "complexity": 3,
            "roles": {
                "verb": ["Nesciebam", "fecisset"],
                "subject": ["quis"],
                "direct_object": ["hoc"]
            }
        }
    ],
    20: [
        {
            "latin": "Dico te bonum amicum esse.",
            "spanish": "Digo que tú eres un buen amigo.",
            "complexity": 3,
            "roles": {
                "verb": ["Dico"],
                "subject_accusative": ["te"],
                "attribute_accusative": ["bonum", "amicum"],
                "infinitive": ["esse"]
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
    
    # Tokenización simple que conserva puntuación para coincidir con visualización si es necesario,
    # pero para índices necesitamos las palabras limpias o coincidencia exacta.
    # Vamos a asumir tokenización por espacios y limpiar puntuación para búsqueda
    
    # Mejor estrategia: split por espacios y limpiar puntuación de cada token para comparar
    tokens = latin_text.split()
    clean_tokens = [re.sub(r'[.,;?!]', '', t).lower() for t in tokens]
    
    result_indices = {}
    
    for role, words in roles_map.items():
        indices = []
        for word in words:
            target = word.lower()
            # Buscar todas las ocurrencias
            for idx, token in enumerate(clean_tokens):
                if token == target:
                    indices.append(idx)
        
        if indices:
            result_indices[role] = list(set(indices)) # Eliminar duplicados
            
    return json.dumps(result_indices)

def seed_lessons_11_20():
    print("🌱 Iniciando población de Lecciones 11-20...")
    
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
                        declension=decl if pos == "noun" or pos == "adjective" else None,
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
                        sentence_type="simple" # Default, se detectará luego
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
                        usage_type="analysis", # Tipo específico para el nuevo widget
                        sentence_type="complex",
                        syntax_roles=roles_json
                    )
                    session.add(sentence)
                    print(f"    + Agregada análisis: {latin[:30]}...")

        session.commit()
        print("✅ Población completada exitosamente.")

if __name__ == "__main__":
    seed_lessons_11_20()
