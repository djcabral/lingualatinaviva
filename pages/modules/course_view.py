import streamlit as st
import os
import sys
from datetime import datetime


from utils.ui_helpers import load_css, render_page_header, render_sidebar_footer, render_styled_table
from utils.ui_components import render_lesson_practice_section
from utils.mermaid_helper import render_mermaid
from database.connection import get_session
from utils.unlock_service import check_unlock_conditions
from utils.progress_tracker import update_lesson_progress

def get_lesson_context(lesson_number: int):
    """Returns the practice context for a specific lesson"""
    context = {
        "lesson_id": lesson_number,
        "active": True,
        "timestamp": datetime.now().isoformat()
    }
    
    # Define specific filters per lesson
    if lesson_number == 1:
        context.update({
            "description": "Lección 1: Primeros Pasos",
            "filters": {"pos": ["noun"], "declension": ["1"], "gender": ["f"]}, # Aproximación
            "relevant_challenges": [1, 2] # Intro challenges
        })
    elif lesson_number == 2:
        context.update({
            "description": "Lección 2: El Sujeto",
            "filters": {"pos": ["noun"], "declension": ["1", "2"], "case": ["nom"]},
            "relevant_challenges": [3, 4]
        })
    elif lesson_number == 3:
        context.update({
            "description": "Lección 3: Primera Declinación",
            "filters": {"pos": ["noun"], "declension": ["1"]},
            "relevant_challenges": [5, 6, 7]
        })
    elif lesson_number == 4:
        context.update({
            "description": "Lección 4: Segunda Declinación",
            "filters": {"pos": ["noun"], "declension": ["2"]},
            "relevant_challenges": [8, 9, 10]
        })
    elif lesson_number == 5:
        context.update({
            "description": "Lección 5: El Neutro",
            "filters": {"pos": ["noun"], "gender": ["n"]},
            "relevant_challenges": [11, 12]
        })
    # Add more lessons as needed
    
    return context

def render_practice_section(lesson_number: int, lesson_title: str):
    """Renderiza la sección PRACTICA ESTA LECCIÓN con enlaces contextuales"""
    
    # Marcar lección como vista
    try:
        with get_session() as session:
            update_lesson_progress(session, user_id=1, lesson_number=lesson_number, 
                                 status="in_progress")
    except Exception as e:
        pass  # Si falla, continuar sin bloquear la UI
    
    st.markdown(f"## 🎯 Practica esta Lección")
    st.markdown(f"Has completado la teoría de **Lección {lesson_number}: {lesson_title}**.")
    st.markdown("Ahora es momento de aplicar lo aprendido:")
    
    # Verificar qué está desbloqueado
    try:
        with get_session() as session:
            vocab_unlocked = check_unlock_conditions(session, 1, f"vocab_l{lesson_number}")
            exercises_unlocked = check_unlock_conditions(session, 1, f"exercises_l{lesson_number}")
            reading_unlocked = check_unlock_conditions(session, 1, f"reading_l{lesson_number}")
            challenge_unlocked = check_unlock_conditions(session, 1, f"challenge_l{lesson_number}")
    except Exception:
        # Si falla, asumir que todo está desbloqueado por defecto
        vocab_unlocked = True
        exercises_unlocked = False
        reading_unlocked = False
        challenge_unlocked = False
    
    # Vocabulario
    st.markdown("### 📚 Vocabulario Esencial")
    if vocab_unlocked:
        st.markdown("Las palabras clave para dominar esta lección.")
        if st.button(f"📚 Ver Vocabulario de Lección {lesson_number}", key=f"vocab_l{lesson_number}"):
            st.switch_page("pages/03_🧠_Memorización.py")
    else:
        st.info("🔒 Se desbloqueará al completar la lección anterior")
    
    st.markdown("")
    
    # Ejercicios
    st.markdown("### 📜 Ejercicios de Práctica")
    if exercises_unlocked:
        st.markdown("Practica declinaciones, conjugaciones y análisis de esta lección.")
        col1, col2, col3 = st.columns(3)
        
        # Prepare context
        context = get_lesson_context(lesson_number)
        
        with col1:
            if st.button("📜 Declinaciones", key=f"decl_l{lesson_number}"):
                st.session_state.practice_context = context
                st.session_state.active_tab = 0 # Tab index for Declensions
                st.switch_page("pages/04_⚔️_Práctica.py")
        with col2:
            if st.button("⚔️ Conjugaciones", key=f"conj_l{lesson_number}"):
                st.session_state.practice_context = context
                st.session_state.active_tab = 1 # Tab index for Conjugations
                st.switch_page("pages/04_⚔️_Práctica.py")
        with col3:
            if st.button("🔍 Análisis", key=f"anal_l{lesson_number}"):
                st.session_state.practice_context = context
                st.switch_page("pages/05_🔍_Análisis.py")
                
    else:
        st.warning("🔒 Se desbloqueará cuando domines el 50% del vocabulario")
    
    st.markdown("")
    
    # Lecturas
    st.markdown("### 📖 Lectura Aplicada")
    if reading_unlocked:
        st.markdown("Lee textos que usan el vocabulario y gramática de esta lección.")
        if st.button("📖 Ver Lecturas", key=f"reading_l{lesson_number}"):
            st.switch_page("pages/02_📘_Lecciones.py")
    else:
        st.info("🔒 Se desbloqueará al completar 5 ejercicios con 70%+ de precisión")
    
    st.markdown("")
    
    # Desafío
    st.markdown("### 🎯 Desafío Final")
    if challenge_unlocked:
        st.markdown("Demuestra tu dominio completo de esta lección.")
        if st.button("🎯 Tomar Desafío", key=f"challenge_l{lesson_number}"):
            st.session_state.practice_context = context
            st.session_state.go_to_challenge = True # Flag to switch tab
            st.switch_page("pages/04_⚔️_Práctica.py")
    else:
        st.info("🔒 Se desbloqueará al completar: Vocabulario 80% + Ejercicios + Lectura + Análisis sintáctico")

def render_course_content():
    # Page config and header are handled by the parent page
    
    # Sidebar Navigation
    st.sidebar.title("📚 Lecciones")
    
    # Organize lessons by level
    basico = {
        "intro": "Introducción",
        "l1": "1. Primeros Pasos",
        "l2": "2. El Sujeto (Nominativo)",
        "l3": "3. Primera Declinación y Sum",
        "l4": "4. Segunda Declinación y Objeto",
        "l5": "5. El Neutro",
        "l6": "6. Consolidación y Adjetivos",
        "l7": "7. Tercera Declinación y Dativo",
        "l8": "8. Cuarta Declinación y Pasado",
        "l9": "9. Quinta Declinación y Futuro",
        "l10": "10. Adjetivos de 2ª Clase",
        "l11": "11. Comparación",
        "l12": "12. Pronombres",
        "l13": "13. Voz Pasiva y Ablativo",
    }
    
    avanzado = {
        "l14": "14. Pluscuamperf. y Fut. Perfecto",
        "l15": "15. Voz Pasiva - Infectum",
        "l16": "16. Voz Pasiva - Perfectum",
        "l17": "17. Verbos Deponentes",
        "l18": "18. Subjuntivo I",
        "l19": "19. Subjuntivo II y Consecutio",
        "l20": "20. Infinitivos y AcI",
        "l21": "21. Participios",
        "l22": "22. Ablativo Absoluto",
        "l23": "23. Gerundio y Gerundivo",
        "l24": "24. Perifrásticas",
        "l25": "25. Sintaxis I: Coordinación y Causales",
        "l26": "26. Sintaxis II: Completivas y Finales",
        "l27": "27. Subordinadas III: Condicionales",
        "l28": "28. Subordinadas IV: Relativas",
        "l29": "29. Estilo Indirecto",
        "l30": "30. Métrica y Poesía",
    }
    
    experto = {
        "l31": "31. César y Prosa Militar",
        "l32": "32. Cicerón y Retórica",
        "l33": "33. Salustio y Historiografía",
        "l34": "34. Catulo y Lírica",
        "l35": "35. Virgilio y Épica",
        "l36": "36. Horacio y Odas",
        "l37": "37. Ovidio y Metamorfosis",
        "l38": "38. Latín Medieval",
        "l39": "39. Latín Eclesiástico",
        "l40": "40. Latín Renacentista"
    }
    
    # Session state for current lesson
    if 'current_lesson' not in st.session_state:
        st.session_state.current_lesson = "intro"
    
    # Determine which level the current lesson belongs to
    current_level = None
    if st.session_state.current_lesson in basico:
        current_level = "basico"
    elif st.session_state.current_lesson in avanzado:
        current_level = "avanzado"
    elif st.session_state.current_lesson in experto:
        current_level = "experto"
    
    # Render level sections with expanders
    with st.sidebar:
        # BÁSICO
        basic_label = "📗 BÁSICO (Intro + Lec. 1-13)" + (" " if current_level == "basico" else "")
        with st.expander(basic_label, expanded=(current_level == "basico")):
            for lesson_id, lesson_name in basico.items():
                if st.button(
                    lesson_name,
                    key=f"btn_{lesson_id}",
                    use_container_width=True,
                    type="primary" if st.session_state.current_lesson == lesson_id else "secondary"
                ):
                    st.session_state.current_lesson = lesson_id
                    st.rerun()
        
        # AVANZADO
        adv_label = "📘 AVANZADO (Lec. 14-30)" + (" " if current_level == "avanzado" else "")
        with st.expander(adv_label, expanded=(current_level == "avanzado")):
            for lesson_id, lesson_name in avanzado.items():
                if st.button(
                    lesson_name,
                    key=f"btn_{lesson_id}",
                    use_container_width=True,
                    type="primary" if st.session_state.current_lesson == lesson_id else "secondary"
                ):
                    st.session_state.current_lesson = lesson_id
                    st.rerun()
        
        # EXPERTO
        exp_label = "📕 EXPERTO (Lec. 31-40)" + (" " if current_level == "experto" else "")
        with st.expander(exp_label, expanded=(current_level == "experto")):
            for lesson_id, lesson_name in experto.items():
                if st.button(
                    lesson_name,
                    key=f"btn_{lesson_id}",
                    use_container_width=True,
                    type="primary" if st.session_state.current_lesson == lesson_id else "secondary"
                ):
                    st.session_state.current_lesson = lesson_id
                    st.rerun()
    
    # Render Content
    render_lesson_content(st.session_state.current_lesson)
    
    # Footer handled by parent page


def render_database_lesson(lesson):
    """Render a lesson loaded from the database"""
    # Display image if available
    if lesson.image_path and os.path.exists(lesson.image_path):
        st.image(lesson.image_path, use_container_width=True)
    
    # Render markdown content
    st.markdown(lesson.content_markdown)
    
    # Add practice section for basic lessons (1-13)
    if lesson.level == "basico" and lesson.lesson_number <= 13:
        st.markdown("---")
        render_practice_section(lesson.lesson_number, lesson.title)


def render_lesson_content(lesson_id):
    """Render lesson content - checks database first, then falls back to hardcoded functions"""
    
    # Try to load from database first
    if lesson_id.startswith("l") and lesson_id[1:].isdigit():
        lesson_number = int(lesson_id[1:])
        
        try:
            from database import Lesson
            from sqlmodel import select
            
            with get_session() as session:
                db_lesson = session.exec(
                    select(Lesson).where(
                        Lesson.lesson_number == lesson_number,
                        Lesson.is_published == True
                    )
                ).first()
                
                if db_lesson:
                    render_database_lesson(db_lesson)
                    return
        except Exception as e:
            # If database fails, continue to hardcoded fallback
            pass
    
    # Fallback to hardcoded functions
    if lesson_id == "intro":
        render_intro()
    elif lesson_id == "l1":
        render_lesson_1()
    elif lesson_id == "l2":
        render_lesson_2()
    elif lesson_id == "l3":
        render_lesson_3()
    elif lesson_id == "l4":
        render_lesson_4()
    elif lesson_id == "l5":
        render_lesson_5()
    elif lesson_id == "l6":
        render_lesson_6()
    elif lesson_id == "l7":
        render_lesson_7()
    elif lesson_id == "l8":
        render_lesson_8()
    elif lesson_id == "l9":
        render_lesson_9()
    elif lesson_id == "l10":
        render_lesson_10()
    elif lesson_id == "l11":
        render_lesson_11()
    elif lesson_id == "l12":
        render_lesson_12()
    elif lesson_id == "l13":
        render_lesson_13()
    elif lesson_id == "sep1":
        st.info("🔸 Nivel Avanzado: Sistema verbal completo y sintaxis compleja")
    elif lesson_id == "l14":
        render_lesson_14()
    elif lesson_id == "l15":
        render_lesson_15()
    elif lesson_id == "l16":
        render_lesson_16()
    elif lesson_id == "l17":
        render_lesson_17()
    elif lesson_id == "l18":
        render_lesson_18()
    elif lesson_id == "l19":
        render_lesson_19()
    elif lesson_id == "l20":
        render_lesson_20()
    elif lesson_id == "l21":
        render_lesson_21()
    elif lesson_id == "l22":
        render_lesson_22()
    elif lesson_id == "l23":
        render_lesson_23()
    elif lesson_id == "l24":
        render_lesson_24()
    elif lesson_id == "l25":
        render_lesson_25()
    elif lesson_id == "l26":
        render_lesson_26()
    elif lesson_id == "l27":
        render_lesson_27()
    elif lesson_id == "l28":
        render_lesson_28()
    elif lesson_id == "l29":
        render_lesson_29()
    elif lesson_id == "l30":
        render_lesson_30()
    elif lesson_id == "sep2":
        st.info("🎓 Nivel Experto: Autores, Estilística y Evolución del Latín")
    elif lesson_id == "l31":
        render_lesson_31()
    elif lesson_id == "l32":
        render_lesson_32()
    elif lesson_id == "l33":
        render_lesson_33()
    elif lesson_id == "l34":
        render_lesson_34()
    elif lesson_id == "l35":
        render_lesson_35()
    elif lesson_id == "l36":
        render_lesson_36()
    elif lesson_id == "l37":
        render_lesson_37()
    elif lesson_id == "l38":
        render_lesson_38()
    elif lesson_id == "l39":
        render_lesson_39()
    elif lesson_id == "l40":
        render_lesson_40()
    else:
        st.info(f"Contenido de la lección {lesson_id} en construcción.")

def render_intro():
    st.image("static/images/intro_course_summary.png", caption="Los Cuatro Pilares del Aprendizaje: Lección, Memorización, Práctica y Análisis", use_container_width=True)

    st.markdown("""
    ## Aprende Latín: Un Enfoque Progresivo
    
    Bienvenido al curso de gramática latina. Este curso está diseñado para guiarte paso a paso 
    desde los conceptos más básicos hasta las estructuras complejas, siguiendo el enfoque pedagógico 
    del profesor **Fernando Nieto Mesa**.
    
    ### ¿Por qué estudiar Latín?
    
    *   **Origen**: Es la madre del español y de las lenguas romances (francés, italiano, portugués, etc.).
    *   **Cultura**: Nos conecta con el origen de nuestra civilización, leyes y costumbres.
    *   **Etimología**: Más del 60% del vocabulario español proviene del latín.
    
    ### Estructura del Curso
    
    El curso consta de **13 lecciones** que combinan gramática y sintaxis de forma gradual.
    En lugar de memorizar tablas interminables de golpe, aprenderás cada declinación y conjugación 
    en su contexto de uso.
    
    ¡Comencemos! Selecciona la **Lección 1** en el menú lateral.
    """)

def render_lesson_1():
    st.image("static/images/curso_gramatica/leccion1_mapa_imperio.png", 
             caption="El Imperio Romano en su máxima extensión, con el Lacio (Latium) y Roma destacados",
             use_container_width=True)
    
    st.markdown("""
    ## Lección 1: Primeros Pasos
    
    ### 1. El Alfabeto Latino
    
    El alfabeto latino constaba originalmente de 23 letras. Persiste en el español, pero sin la **ñ**. 
    Algunas letras tenían pronunciación distinta a la nuestra.
    
    > **Importante**: En latín clásico no existían los acentos escritos ni signos de cantidad. 
    > Los gramáticos modernos los añaden para facilitar el aprendizaje.
    
    ### 2. Reglas de Pronunciación Clásica
    
    Vamos a aprender la **pronunciación restituta** (restituida), que intenta reconstruir cómo 
    hablaban los romanos cultos en el siglo I a.C.
    """)
    
    st.image("static/images/curso_gramatica/leccion1_alfabeto.png",
             caption="Guía de pronunciación del alfabeto latino clásico",
             use_container_width=True)
    
    st.markdown("""
    
    **Consonantes especiales:**
    """)
    
    render_styled_table(
        ["Letra(s)", "Pronunciación", "Ejemplo", "Se dice"],
        [
            ["**c**", "Siempre /k/ (como 'casa')", "*Cicero*", "/Kíkero/"],
            ["**ch**", "/k/ (no /ch/)", "*chorus*", "/kórus/"],
            ["**g**", "Siempre /g/ suave (como 'gato')", "*genus*", "/guénus/"],
            ["**ge, gi**", "/gue/, /gui/", "*genui*, *gigno*", "/guénui/, /guígno/"],
            ["**j**", "Como /i/ consonántica (inglés 'y')", "*janua*", "/iánua/"],
            ["**ph**", "Como /f/", "*philosophia*", "/filosofía/"],
            ["**que, qui**", "/kue/, /kui/", "*atque*, *quidem*", "/átkue/, /kúidem/"],
            ["**v**", "Como /u/ semiconsonántica (inglés 'w')", "*vivere*", "/wíwere/"]
        ]
    )

    st.markdown("""
    
    **Diptongos:**
    *   **ae** = /ai/: *rosae* se dice /rósai/
    *   **oe** = /oi/: *poena* se dice /póina/
    *   **au** = /au/ (como en español): *aurum* se dice /áurum/
    
    > **Nota sobre la doble L**: En latín no existía el sonido /ll/ español. 
    > Se pronuncian las dos eles separadas: *ille* = /il-le/, *puella* = /puel-la/, *ancilla* = /an-kil-la/.
    
    ### 3. Acentuación
    
    En latín **no hay palabras agudas**, solo llanas (graves) o esdrújulas.
    
    **Reglas:**
    1.  Todas las palabras de **dos sílabas** son llanas: *ro-sa*, *do-mus*, *pa-ter*.
    2.  Las palabras de **tres o más sílabas**:
        *   Si la penúltima sílaba es **larga**: acento en la penúltima -> *musá-rum*, *candó-ris*.
        *   Si la penúltima sílaba es **breve**: acento en la antepenúltima -> *cón-sules*, *fí-li-o-lus*.
    
    **¿Cómo saber si una sílaba es larga o breve?**
    *   Es **larga** si forma diptongo, o si la vocal va seguida de **x, z, o dos consonantes**.
    *   Es **breve** si la vocal va seguida de otra vocal.
    
    ### 4. Conceptos Fundamentales: Flexión
    
    El latín es una lengua **flexiva**. Esto significa que las palabras cambian su terminación (desinencia) 
    para indicar su función en la oración, no el orden de las palabras.
    
    **Comparación con el español:**
    """)
    
    render_styled_table(
        ["Español", "Latín"],
        [
            ["El agricultor llama a la criada.", "*Agricola ancillam vocat.*"],
            ["La criada llama al agricultor.", "*Agricolam ancilla vocat.*"]
        ]
    )

    st.markdown("""
    
    > Observa que *agricola* y *ancilla* cambian de forma (*-a* / *-am*) para indicar quién es el sujeto 
    > y quién el objeto, sin importar el orden.
    
    **Características de la flexión:**
    *   **Declinación**: Cambios que experimentan sustantivos, adjetivos y pronombres.
    *   **Conjugación**: Cambios que experimentan los verbos.
    
    ### 5. Categorías Gramaticales
    
    Las palabras latinas tienen:
    *   **Género**: Masculino, Femenino, **Neutro** (ni uno ni otro).
    *   **Número**: Singular, Plural.
    *   **Caso**: Indica la función sintáctica (Sujeto, Objeto, Posesión, etc.).
    
    > **Sobre los artículos**: El latín **no tiene artículos** (el, la, un, una). 
    > Al traducir, debemos añadirlos según el contexto. *Puella* puede ser "la niña", "una niña" o simplemente "niña".
    
    ### 6. Partes de la Oración
    
    En latín hay ocho clases de palabras:
    """)
    
    render_styled_table(
        ["Palabra", "Ejemplo", "Traducción"],
        [
            ["Nombre (sustantivo)", "*ancilla*", "criada"],
            ["Adjetivo", "*sedula*", "activa"],
            ["Pronombre", "*ego*", "yo"],
            ["Verbo", "*voco*", "llamo"],
            ["Adverbio", "*bene*", "bien"],
            ["Preposición", "*cum*", "con"],
            ["Conjunción", "*et*", "y"],
            ["Interjección", "*o!*", "¡oh!"]
        ]
    )

    st.markdown("""
    
    ### Ejercicio de Pronunciación
    
    Intenta leer en voz alta estas palabras aplicando las reglas:
    *   *Cicero philosophus* (Cicerón el filósofo) -> /Kíkero filósofus/
    *   *Julius Caesar* (Julio César) -> /Iúlius Káisar/
    *   *Via longa* (El camino largo) -> /Wía lónga/
    *   *Aqua vitae* (Agua de vida) -> /Ákua wítai/
    """)

def render_lesson_2():
    st.image("static/images/curso_gramatica/leccion2_foro_romano.png",
             caption="El Foro Romano, centro de la vida pública en la antigua Roma",
             use_container_width=True)
    
    st.markdown("""
    ## Lección 2: Los Casos y el Nominativo
    
    ### ¿Qué son los Casos?
    
    En español, usamos el **orden de las palabras** y las **preposiciones** para indicar la función de cada palabra:
    *   "El padre ama **al hijo**" (hijo = objeto directo, marcado con "a")
    *   "El regalo **del padre**" (padre = posesión, marcado con "de")
    *   "Hablo **al maestro**" (maestro = objeto indirecto, marcado con "a")
    
    En latín, usamos los **casos**: terminaciones especiales que cambian según la función sintáctica.
    
    ### Los Seis Casos del Latín
    """)
    
    render_styled_table(
        ["Caso", "Función Principal", "Pregunta Clave"],
        [
            ["**Nominativo**", "Sujeto / Atributo", "¿Quién?"],
            ["**Vocativo**", "Invocación/Llamada", "¡...!"],
            ["**Acusativo**", "Objeto Directo", "¿A quién/qué?"],
            ["**Genitivo**", "Posesión/Pertenencia", "¿De quién?"],
            ["**Dativo**", "Objeto Indirecto", "¿A/Para quién?"],
            ["**Ablativo**", "Circunstancia (Lugar, Modo, Instrumento)", "¿Con/Por/Desde qué?"]
        ]
    )

    st.markdown("""
    """)
    
    st.image("static/images/curso_gramatica/casos_latinos_diagram.png",
             caption="Rueda de los 6 Casos Latinos y sus funciones",
             use_container_width=True)
             
    st.markdown("""
    
    > **Clave de aprendizaje**: Aprenderemos los casos progresivamente. 
    > Empezaremos con el Nominativo (Sujeto) y el Acusativo (Objeto Directo).
    
    ### El Caso Nominativo: El Sujeto
    
    El **Nominativo** es el caso fundamental. Responde a la pregunta **¿Quién?** realiza la acción.
    
    **Usos:**
    1.  **Sujeto de un verbo**: *Puella cantat* (La niña canta)
    2.  **Atributo** (con verbos copulativos como *sum*): *Puella est pulchra* (La niña es hermosa)
    
    ### La Oración Simple en Latín
    
    **Orden flexible:**
    El latín permite gran libertad en el orden de las palabras porque los casos marcan la función.
    Sin embargo, el orden más elegante y común es:
    
    **SUJETO + COMPLEMENTOS + VERBO**
    
    *   *Puella rosam amat.* (La niña ama la rosa)
    *   *Rosam puella amat.* (La niña ama la rosa) ← Mismo significado, énfasis distinto
    *   *Amat puella rosam.* (La niña ama la rosa) ← Menos elegante pero correcto
    
    > **Nota crucial**: En latín **NO hay artículos** (el, la, un, una). Al traducir, los añadimos según el contexto.
    
    ### Ejemplos de Análisis
    """)
    
    render_styled_table(
        ["Oración Latina", "Análisis", "Traducción"],
        [
            ["*Deus est bonus.*", "Deus (Nom, Suj) + est (verbo) + bonus (Nom, Atributo)", "Dios es bueno."],
            ["*Puella cantat.*", "Puella (Nom, Suj) + cantat (verbo)", "La niña canta."],
            ["*Roma magna est.*", "Roma (Nom, Suj) + magna (Nom, Atributo) + est (verbo)", "Roma es grande."]
        ]
    )

    st.markdown("""
    """)

def render_lesson_3():
    st.image("static/images/curso_gramatica/leccion3_declinaciones.png",
             caption="Diagrama visual del sistema de declinaciones latinas",
             width=750)
    
    st.markdown("""
    ## Lección 3: Primera Declinación y Verbos Fundamentales
    
    ### 1. Primera Declinación (Temas en -a): Sustantivos Femeninos
    
    La Primera Declinación agrupa sustantivos mayoritariamente **femeninos** que terminan en **-a** en Nominativo Singular.
    
    **Enunciado**: Los sustantivos se enuncian con el Nominativo y el Genitivo Singular:
    *   *Rosa, rosae* (la rosa, de la rosa) -> indica que es 1ª Declinación
    
    **Paradigma completo: Rosa, -ae (La rosa)**
    
    **Paradigma completo: Rosa, -ae (La rosa)**
    """)
    
    render_styled_table(
        ["Caso", "Singular", "Terminación", "Plural", "Terminación", "Función"],
        [
            ["**Nominativo**", "ros-**a**", "**-a**", "ros-**ae**", "**-ae**", "Sujeto / Atributo"],
            ["**Vocativo**", "ros-**a**", "**-a**", "ros-**ae**", "**-ae**", "¡Oh rosa!"],
            ["**Acusativo**", "ros-**am**", "**-am**", "ros-**as**", "**-as**", "Objeto Directo"],
            ["**Genitivo**", "ros-**ae**", "**-ae**", "ros-**arum**", "**-arum**", "De la rosa (posesión)"],
            ["**Dativo**", "ros-**ae**", "**-ae**", "ros-**is**", "**-is**", "A/Para la rosa"],
            ["**Ablativo**", "ros-**ā**", "**-ā**", "ros-**is**", "**-is**", "Con/Por la rosa"]
        ]
    )

    st.markdown("""
    
    > **Nota sobre el Ablativo Sg**: La terminación **-ā** es larga (aunque se escribe igual que el Nominativo).
    
    **Otros ejemplos de 1ª Declinación:**
    *   *Puella, puellae* (niña)
    *   *Femina, feminae* (mujer)
    *   *Via, viae* (camino)
    *   *Aqua, aquae* (agua)
    *   *Terra, terrae* (tierra)
    *   *Patria, patriae* (patria)
    *   *Agricola, agricolae* (agricultor) ← **¡Masculino!** (excepción por su profesión)
    
    ### 2. El Verbo SUM (Ser/Estar) - Presente de Indicativo
    
    El verbo **sum** (ser/estar) es **irregular** pero absolutamente fundamental. 
    Se usa para formar el atributo y aparece en innumerables expresiones.
    
    **Conjugación completa:**
    """)
    
    render_styled_table(
        ["Persona", "Forma", "Traducción 1", "Traducción 2"],
        [
            ["1ª Sg", "**sum**", "yo soy", "yo estoy"],
            ["2ª Sg", "**es**", "tú eres", "tú estás"],
            ["3ª Sg", "**est**", "él/ella es", "él/ella está"],
            ["1ª Pl", "**sumus**", "nosotros somos", "nosotros estamos"],
            ["2ª Pl", "**estis**", "vosotros sois", "vosotros estáis"],
            ["3ª Pl", "**sunt**", "ellos/ellas son", "ellos/ellas están"]
        ]
    )

    st.markdown("""
    
    **Ejemplos de uso:**
    *   *Sum Romanus.* (Soy romano)
    *   *Puella est pulchra.* (La niña es hermosa)
    *   *Rosae sunt pulchrae.* (Las rosas son hermosas)
    *   *Ubi es?* (¿Dónde estás?)
    
    ### 3. Primera Conjugación (verbos en -ARE): AMARE (Amar)
    
    Los verbos cuyo infinitivo termina en **-are** pertenecen a la 1ª Conjugación.
    Son los más regulares y numerosos.
    
    **Presente de Indicativo - Voz Activa:**
    """)
    
    render_styled_table(
        ["Persona", "Raíz", "Desinencia", "Forma completa", "Español"],
        [
            ["1ª Sg", "am-", "**-o**", "am-**o**", "yo amo"],
            ["2ª Sg", "am-", "**-as**", "am-**as**", "tú amas"],
            ["3ª Sg", "am-", "**-at**", "am-**at**", "él/ella ama"],
            ["1ª Pl", "am-", "**-amus**", "am-**amus**", "nosotros amamos"],
            ["2ª Pl", "am-", "**-atis**", "am-**atis**", "vosotros amáis"],
            ["3ª Pl", "am-", "**-ant**", "am-**ant**", "ellos/ellas aman"]
        ]
    )

    st.markdown("""
    
    **Otros verbos de 1ª Conjugación:**
    *   *Laudo, laudare* (alabar)
    *   *Voco, vocare* (llamar)
    *   *Narro, narrare* (narrar, contar)
    *   *Oro, orare* (rogar, rezar)
    *   *Ambulo, ambulare* (caminar)
    *   *Habito, habitare* (habitar)
    
    ### Ejemplos de Frases Completas
    """)
    
    render_styled_table(
        ["Latín", "Análisis", "Traducción"],
        [
            ["*Puella rosam amat.*", "Puella (Nom, Suj) + rosam (Ac, OD) + amat (verbo)", "La niña ama la rosa."],
            ["*Feminae aquam portant.*", "Feminae (Nom Pl, Suj) + aquam (Ac, OD) + portant (verbo)", "Las mujeres llevan agua."],
            ["*Puella est bona.*", "Puella (Nom, Suj) + est (verbo) + bona (Nom, Atrib)", "La niña es buena."],
            ["*Agricola patriam laudat.*", "Agricola (Nom, Suj) + patriam (Ac, OD) + laudat (verbo)", "El agricultor alaba la patria."],
            ["*Puellae cantant.*", "Puellae (Nom Pl, Suj) + cantant (verbo)", "Las niñas cantan."]
        ]
    )

    st.markdown("""
    
    ### Vocabulario Esencial
    
    Aprende estas palabras fundamentales:
    *   **Puella, -ae** (f): niña
    *   **Rosa, -ae** (f): rosa
    *   **Femina, -ae** (f): mujer
    *   **Aqua, -ae** (f): agua
    *   **Terra, -ae** (f): tierra
    *   **Vita, -ae** (f): vida
    *   **Amo, amare**: amar
    *   **Laudo, laudare**: alabar
    *   **Voco, vocare**: llamar
    """) # Closing parenthesis for st.markdown
    
    # SECCIÓN DE PRÁCTICA INTEGRADA
    st.markdown("---")
    render_practice_section(lesson_number=3, lesson_title="Primera Declinación y Sum")

def render_lesson_4():
    st.image("static/images/curso_gramatica/leccion4_vida_cotidiana.png",
             caption="La vida cotidiana en una domus romana",
             use_container_width=True)
    
    st.markdown("""
    ## Lección 4: Segunda Declinación (Masculinos) y el Acusativo
    
    ### 1. Segunda Declinación: Sustantivos Masculinos en -US
    
    La Segunda Declinación agrupa sustantivos mayoritariamente **masculinos** que terminan en **-us** en Nominativo.
    El Genitivo Singular termina en **-i**.
    
    **Enunciado estándar**: *Dominus, domini* (el señor, del señor)
    
    **Paradigma completo: Dominus, -i (El señor)**
    """)
    
    render_styled_table(
        ["Caso", "Singular", "Terminación", "Plural", "Terminación", "Función"],
        [
            ["**Nominativo**", "domin-**us**", "**-us**", "domin-**i**", "**-i**", "Sujeto"],
            ["**Vocativo**", "domin-**e**", "**-e**", "domin-**i**", "**-i**", "¡Oh señor!"],
            ["**Acusativo**", "domin-**um**", "**-um**", "domin-**os**", "**-os**", "Objeto Directo"],
            ["**Genitivo**", "domin-**i**", "**-i**", "domin-**orum**", "**-orum**", "Del señor"],
            ["**Dativo**", "domin-**o**", "**-o**", "domin-**is**", "**-is**", "Al señor"],
            ["**Ablativo**", "domin-**o**", "**-o**", "domin-**is**", "**-is**", "Con/Por el señor"]
        ]
    )

    st.markdown("""
    
    > **¡Atención al Vocativo!** El Vocativo Singular de los sustantivos en **-us** es **-e**. 
    > Es la única diferencia con el Nominativo. *Domine!* = ¡Señor!
    
    **Sustantivos en -ER (menos frecuentes):**
    Algunos masculinos de 2ª Declinación terminan en **-er** en Nominativo:
    *   *Puer, pueri* (niño) - Mantiene la **e**
    *   *Ager, agri* (campo) - Pierde la **e** en los demás casos
    
    **Otros ejemplos de 2ª Declinación Masculina:**
    *   *Servus, -i*: esclavo, siervo
    *   *Amicus, -i*: amigo
    *   *Filius, -i*: hijo (Vocativo: *fili*, no *filie*)
    *   *Deus, -i*: dios (Vocativo: *Deus*, irregular)
    *   *Populus, -i*: pueblo
    *   *Animus, -i*: ánimo, alma
    *   *Liber, libri*: libro
    *   *Magister, magistri*: maestro
    
    ### 2. El Caso Acusativo: El Objeto Directo
    
    El **Acusativo** es el caso del **Objeto Directo**. Responde a la pregunta **¿A quién?** o **¿Qué?** recibe la acción.
    
    **Equivale en español a**: "a" + sustantivo (cuando es persona), o simplemente el sustantivo (cuando es cosa).
    
    **Ejemplos:**
    *   *Dominus servum vocat.* (El señor llama al siervo)
        - *Dominus*: Nominativo (Sujeto) = ¿Quién llama?
        - *servum*: Acusativo (Objeto Directo) = ¿A quién llama?
    *   *Puella rosam amat.* (La niña ama la rosa)
        - *Puella*: Nominativo (Sujeto)
        - *rosam*: Acusativo (Objeto Directo)
    
    ### 3. Pretérito Imperfecto de Indicativo
    
    El **Pretérito Imperfecto** expresa una acción pasada que:
    - Era continua o habitual: "amaba", "solía amar"
    - No tiene un final definido en el tiempo
    
    **Formación**: Se añade el sufijo temporal **-ba-** (1ª/2ª conj.) a la raíz del presente.
    
    **Verbo SUM (Irregular):**
    """)
    
    render_styled_table(
        ["Persona", "Forma", "Traducción"],
        [
            ["1ª Sg", "**eram**", "yo era / estaba"],
            ["2ª Sg", "**eras**", "tú eras / estabas"],
            ["3ª Sg", "**erat**", "él/ella era / estaba"],
            ["1ª Pl", "**eramus**", "nosotros éramos / estábamos"],
            ["2ª Pl", "**eratis**", "vosotros erais / estabais"],
            ["3ª Pl", "**erant**", "ellos eran / estaban"]
        ]
    )

    st.markdown("""
    
    **Primera Conjugación (AMARE):**
    """)
    
    render_styled_table(
        ["Persona", "Raíz + Sufijo", "Forma", "Traducción"],
        [
            ["1ª Sg", "ama + ba + m", "**amabam**", "yo amaba"],
            ["2ª Sg", "ama + ba + s", "**amabas**", "tú amabas"],
            ["3ª Sg", "ama + ba + t", "**amabat**", "él/ella amaba"],
            ["1ª Pl", "ama + ba + mus", "**amabamus**", "nosotros amábamos"],
            ["2ª Pl", "ama + ba + tis", "**amabatis**", "vosotros amabais"],
            ["3ª Pl", "ama + ba + nt", "**amabant**", "ellos/ellas amaban"]
        ]
    )

    st.markdown("""
    
    **Ejemplos de uso:**
    *   *Dominus servos vocabat.* (El señor llamaba a los siervos)
    *   *Puella rosam amabat.* (La niña amaba la rosa)
    *   *Eram puer.* (Yo era un niño)
    *   *Magistri discipulos laudabant.* (Los maestros alababan a los discípulos)
    
    ### Vocabulario Esencial
    *   **Dominus, -i** (m): señor, amo
    *   **Servus, -i** (m): esclavo, siervo
    *   **Amicus, -i** (m): amigo
    *   **Puer, pueri** (m): niño
    *   **Magister, magistri** (m): maestro
    *   **Deus, -i** (m): dios
    *   **Voco, vocare**: llamar
    *   **Porto, portare**: llevar
    """)

def render_lesson_5():
    st.markdown("""
    ## Lección 5: El Neutro y Segunda Conjugación
    """)
    
    st.image("static/images/curso_gramatica/leccion5_neutro_diagram.png",
             caption="Diagrama del Género Neutro y sus reglas fundamentales",
             use_container_width=True)
             
    st.markdown("""
    
    ### 1. Segunda Declinación: Sustantivos Neutros en -UM
    
    El género **Neutro** (neuter = ni uno ni otro) se usa principalmente para cosas inanimadas, 
    aunque no todas las cosas son neutras.
    
    **Las Reglas de Oro del Neutro** (válidas para TODAS las declinaciones):
    1.  El **Nominativo, Vocativo y Acusativo** son **siempre iguales** entre sí.
    2.  En el **Plural**, estos tres casos terminan siempre en **-a**.
    
    **Paradigma completo: Templum, -i (El templo)**
    """)
    
    render_styled_table(
        ["Caso", "Singular", "Terminación", "Plural", "Terminación", "Función"],
        [
            ["**Nom/Voc/Ac**", "templ-**um**", "**-um**", "templ-**a**", "**-a**", "Suj/OD"],
            ["**Genitivo**", "templ-**i**", "**-i**", "templ-**orum**", "**-orum**", "Del templo"],
            ["**Dativo**", "templ-**o**", "**-o**", "templ-**is**", "**-is**", "Al templo"],
            ["**Ablativo**", "templ-**o**", "**-o**", "templ-**is**", "**-is**", "Con el templo"]
        ]
    )

    st.markdown("""
    
    > **Observación**: Los casos Genitivo, Dativo y Ablativo son idénticos a los masculinos de 2ª Declinación.
    > La única diferencia está en Nom/Voc/Ac.
    
    **Otros ejemplos de Neutros en -UM:**
    *   *Bellum, -i*: guerra
    *   *Donum, -i*: regalo, don
    *   *Verbum, -i*: palabra
    *   *Caelum, -i*: cielo
    *   *Oppidum, -i*: ciudad, plaza fuerte
    *   *Auxilium, -i*: ayuda, auxilio
    *   *Forum, -i*: foro, plaza pública
    
    **¡Importante sobre concordancia!**
    Cuando el sujeto es neutro plural (*templa*, *bella*), el verbo va en **singular**:
    *   *Templa sunt pulchra.* ❌ (Incorrecto)
    *   *Templa est pulchrum.* ❌ (Incorrecto)
    *   *Templa pulchra sunt.* ✓ (Correcto) - Los templos son hermosos
    
    ### 2. Segunda Conjugación: Verbos en -ĒRE
    
    Los verbos cuyo infinitivo termina en **-ēre** (con **e larga**) pertenecen a la 2ª Conjugación.
    
    **Modelo: Monere (Aconsejar, Advertir)**
    
    **Presente de Indicativo:**
    """)
    
    render_styled_table(
        ["Persona", "Raíz", "Desinencia", "Forma", "Español"],
        [
            ["1ª Sg", "mone-", "**-o**", "**moneo**", "yo aconsejo"],
            ["2ª Sg", "mone-", "**-s**", "**mones**", "tú aconsejas"],
            ["3ª Sg", "mone-", "**-t**", "**monet**", "él/ella aconseja"],
            ["1ª Pl", "mone-", "**-mus**", "**monemus**", "nosotros aconsejamos"],
            ["2ª Pl", "mone-", "**-tis**", "**monetis**", "vosotros aconsejáis"],
            ["3ª Pl", "mone-", "**-nt**", "**monent**", "ellos/ellas aconsejan"]
        ]
    )

    st.markdown("""
    
    **Pretérito Imperfecto:**
    Sufijo temporal: **-eba-** (no -ba- como en la 1ª)
    """)
    
    render_styled_table(
        ["Persona", "Forma", "Traducción"],
        [
            ["1ª Sg", "**monebam**", "yo aconsejaba"],
            ["2ª Sg", "**monebas**", "tú aconsejabas"],
            ["3ª Sg", "**monebat**", "él/ella aconsejaba"],
            ["1ª Pl", "**monebamus**", "nosotros aconsejábamos"],
            ["2ª Pl", "**monebatis**", "vosotros aconsejabais"],
            ["3ª Pl", "**monebant**", "ellos/ellas aconsejaban"]
        ]
    )

    st.markdown("""
    
    **Otros verbos de 2ª Conjugación:**
    *   *Habeo, habere*: tener, poseer
    *   *Video, videre*: ver
    *   *Timeo, timere*: temer
    *   *Debeo, debere*: deber
    *   *Teneo, tenere*: tener, sostener
    *   *Doceo, docere*: enseñar
    
    ### Ejemplos de Frases
    """)

    render_styled_table(
        ["Latín", "Análisis", "Traducción"],
        [
            ["*Puer templum videt.*", "Puer (Nom, Suj) + templum (Ac, OD) + videt (verbo)", "El niño ve el templo."],
            ["*Templum pulchrum est.*", "Templum (Nom, Suj) + pulchrum (Nom, Atrib) + est", "El templo es hermoso."],
            ["*Templa pulchra sunt.*", "Templa (Nom Pl Neut, Suj) + pulchra (Nom Pl Neut, Atrib) + sunt", "Los templos son hermosos."],
            ["*Magister pueros monet.*", "Magister (Nom, Suj) + pueros (Ac, OD) + monet (verbo)", "El maestro aconseja a los niños."],
            ["*Bellum timebamus.*", "Bellum (Ac, OD) + timebamus (verbo 1ª Pl)", "Temíamos la guerra."]
        ]
    )

    st.markdown("""
    
    ### Vocabulario Esencial
    *   **Templum, -i** (n): templo
    *   **Bellum, -i** (n): guerra
    *   **Donum, -i** (n): regalo
    *   **Verbum, -i** (n): palabra
    *   **Moneo, monere**: aconsejar
    *   **Habeo, habere**: tener
    *   **Video, videre**: ver
    *   **Timeo, timere**: temer
    """)

def render_lesson_6():
    st.image("static/images/curso_gramatica/leccion6_arquitectura.png",
             caption="Arquitectura romana icónica: Coliseo, Panteón, acueductos y columnas",
             use_container_width=True)
    
    st.markdown("""
    ## Lección 6: Consolidación, 3ª/4ª Conjugación y Adjetivos
    """)
    
    st.image("static/images/curso_gramatica/conjugaciones_overview.png",
             caption="Resumen visual de las 4 conjugaciones latinas",
             use_container_width=True)
             
    st.markdown("""
    
    ### Revisión: Lo que hemos aprendido hasta ahora
    
    **Declinaciones:**
    *   1ª Declinación: Femeninos en **-a** (*rosa, puella*)
    *   2ª Declinación: Masculinos en **-us/-er** (*dominus, puer*) y Neutros en **-um** (*templum*)
    
    **Casos dominados:**
    *   **Nominativo**: Sujeto
    *   **Acusativo**: Objeto Directo
    
    **Verbos:**
    *   *Sum* (irregular): Presente e Imperfecto
    *   1ª Conjugación (*amare*): Presente e Imperfecto
    *   2ª Conjugación (*monere*): Presente e Imperfecto
    
    ### 1. Tercera Conjugación: Verbos en -ERE (e breve)
    
    Los verbos cuyo infinitivo termina en **-ere** (con **e breve**, no larga) pertenecen a la 3ª Conjugación.
    Son más irregulares que la 1ª y 2ª.
    
    **Modelo: Legere (Leer)**
    
    **Presente de Indicativo:**
    """)

    render_styled_table(
        ["Persona", "Forma", "Español"],
        [
            ["1ª Sg", "**lego**", "yo leo"],
            ["2ª Sg", "**legis**", "tú lees"],
            ["3ª Sg", "**legit**", "él/ella lee"],
            ["1ª Pl", "**legimus**", "nosotros leemos"],
            ["2ª Pl", "**legitis**", "vosotros leéis"],
            ["3ª Pl", "**legunt**", "ellos/ellas leen"]
        ]
    )

    st.markdown("""
    
    **Pretérito Imperfecto:**
    Sufijo: **-eba-** (igual que la 2ª)
    *   *legebam, legebas, legebat, legebamus, legebatis, legebant*
    
    **Otros verbos de 3ª Conjugación:**
    *   *Dico, dicere*: decir
    *   *Duco, ducere*: conducir, guiar
    *   *Scribo, scribere*: escribir
    *   *Mitto, mittere*: enviar
    *   *Vivo, vivere*: vivir
    
    ### 2. Cuarta Conjugación: Verbos en -IRE
    
    Los verbos cuyo infinitivo termina en **-ire** pertenecen a la 4ª Conjugación.
    
    **Modelo: Audire (Oír, Escuchar)**
    
    **Presente de Indicativo:**
    """)

    render_styled_table(
        ["Persona", "Forma", "Español"],
        [
            ["1ª Sg", "**audio**", "yo oigo"],
            ["2ª Sg", "**audis**", "tú oyes"],
            ["3ª Sg", "**audit**", "él/ella oye"],
            ["1ª Pl", "**audimus**", "nosotros oímos"],
            ["2ª Pl", "**auditis**", "vosotros oís"],
            ["3ª Pl", "**audiunt**", "ellos/ellas oyen"]
        ]
    )

    st.markdown("""
    
    **Pretérito Imperfecto:**
    Sufijo: **-ieba-**
    *   *audiebam, audiebas, audiebat, audiebamus, audiebatis, audiebant*
    
    **Otros verbos de 4ª Conjugación:**
    *   *Venio, venire*: venir
    *   *Dormio, dormire*: dormir
    *   *Sentio, sentire*: sentir
    
    ### 3. Adjetivos de Primera Clase (Sistema 2-1-2)
    
    Los adjetivos de 1ª Clase se declinan como los sustantivos de **1ª y 2ª Declinación**.
    
    **Modelo: Bonus, -a, -um (Bueno)**
    
    *   **Masculino**: *bonus* (se declina como *dominus*)
    *   **Femenino**: *bona* (se declina como *rosa*)
    *   **Neutro**: *bonum* (se declina como *templum*)
    
    **Principio de CONCORDANCIA**:
    El adjetivo debe concordar con el sustantivo en **Género, Número y Caso**.
    
    **Ejemplos:**
    *   *Puer bonus* (Niño bueno) - Masculino, Singular, Nominativo
    *   *Puella bona* (Niña buena) - Femenino, Singular, Nominativo
    *   *Templum bonum* (Templo bueno) - Neutro, Singular, Nominativo
    *   *Puellam bonam* (A la niña buena) - Femenino, Singular, Acusativo
    *   *Templa bona* (Los templos buenos) - Neutro, Plural, Nom/Ac
    
    **Otros adjetivos de 1ª Clase:**
    *   *Magnus, -a, -um*: grande
    *   *Parvus, -a, -um*: pequeño
    *   *Pulcher, pulchra, pulchrum*: hermoso
    *   *Liber, libera, liberum*: libre
    *   *Malus, -a, -um*: malo
    
    ### 4. El Caso Vocativo: La Invocación
    
    El **Vocativo** se usa para **invocar, llamar o dirigirse** a alguien.
    
    **Reglas:**
    *   En 1ª Declinación: **igual al Nominativo**
    *   En 2ª Declinación (-us): termina en **-e**
    *   En 2ª Declinación (-um): **igual al Nominativo**
    
    **Ejemplos:**
    *   *Domine!* (¡Señor!)
    *   *Puella!* (¡Niña!)
    *   *Fili!* (¡Hijo!) - Excepción: *filius* hace *fili*, no *filie*
    *   *Mi amice!* (¡Amigo mío!)
    """)

def render_lesson_7():
    st.markdown("""
    ## Lección 7: Tercera Declinación y el Dativo
    """)
    
    st.image("static/images/curso_gramatica/leccion7_third_declension.png",
             caption="Esquema de la Tercera Declinación: Imparísílabos y Parisísílabos",
             use_container_width=True)
             
    st.markdown("""
    
    ### 1. Tercera Declinación: La Más Compleja
    
    La 3ª Declinación es la más amplia y compleja. Agrupa sustantivos de **los tres géneros**.
    
    **Característica identificadora**: Genitivo Singular en **-is**.
    
    **Dos grandes grupos:**
    
    #### A. Imparísílabos (Temas en consonante)
    
    Tienen **diferente número de sílabas** en Nominativo y Genitivo.
    
    **Modelo: Rex, regis (El rey) - Masculino**
    
    """
    )

    render_styled_table(
        ["Caso", "Singular", "Plural"],
        [
            ["**Nominativo**", "rex", "reg-**es**"],
            ["**Vocativo**", "rex", "reg-**es**"],
            ["**Acusativo**", "reg-**em**", "reg-**es**"],
            ["**Genitivo**", "reg-**is**", "reg-**um**"],
            ["**Dativo**", "reg-**i**", "reg-**ibus**"],
            ["**Ablativo**", "reg-**e**", "reg-**ibus**"]
        ]
    )

    st.markdown("""
    
    **Otros ejemplos de Imparísílabos:**
    *   *Homo, hominis* (m): hombre
    *   *Mulier, mulieris* (f): mujer
    *   *Pater, patris* (m): padre
    *   *Mater, matris* (f): madre
    *   *Frater, fratris* (m): hermano
    *   *Consul, consulis* (m): cónsul
    *   *Virtus, virtutis* (f): virtud
    *   *Amor, amoris* (m): amor
    
    #### B. Parisísílabos (Temas en -i)
    
    Tienen **igual número de sílabas** en Nom. y Gen. (o terminan en dos consonantes en Nom.).
    
    **Modelo: Civis, civis (El ciudadano) - Masculino/Femenino**
    
    """
    )

    render_styled_table(
        ["Caso", "Singular", "Plural"],
        [
            ["**Nominativo**", "civis", "civ-**es**"],
            ["**Acusativo**", "civ-**em**", "civ-**es**"],
            ["**Genitivo**", "civ-**is**", "civ-**ium**"],
            ["**Dativo**", "civ-**i**", "civ-**ibus**"],
            ["**Ablativo**", "civ-**e/i**", "civ-**ibus**"]
        ]
    )

    st.markdown("""
    
    > **Diferencia clave**: Los parisísílabos tienen Genitivo Plural en **-ium** (no -um).
    
    **Ejemplos de Parisísílabos:**
    *   *Urbs, urbis* (f): ciudad
    *   *Mons, montis* (m): monte
    *   *Fons, fontis* (m): fuente
    *   *Navis, navis* (f): nave
    
    **Neutros de 3ª Declinación:**
    Siguen la **regla de oro del neutro** (Nom/Voc/Ac iguales, plural en -a).
    
    *   *Corpus, corporis* (n): cuerpo
    *   *Opus, operis* (n): obra
    *   *Nomen, nominis* (n): nombre
    
    ### 2. El Caso Dativo: Objeto Indirecto
    
    El **Dativo** marca el **Objeto Indirecto** o el **Destinatario** de la acción.
    Responde a **¿A quién?** o **¿Para quién?**
    
    **En español se traduce con**: "a" o "para" + persona.
    
    **Ejemplos:**
    *   *Puer puellae rosam dat.* (El niño da una rosa a la niña)
        - *Puer*: Nominativo (Sujeto)
        - *puellae*: **Dativo** (Objeto Indirecto) = a quién da
        - *rosam*: Acusativo (Objeto Directo) = qué da
    *   *Magister discipulis libros dat.* (El maestro da libros a los discípulos)
    *   *Do tibi donum.* (Te doy un regalo)
    
    **Terminaciones de Dativo:**
    *   1ª Declinación: Sg **-ae**, Pl **-is**
    *   2ª Declinación: Sg **-o**, Pl **-is**
    *   3ª Declinación: Sg **-i**, Pl **-ibus**
    """)

def render_lesson_8():
    st.markdown("""
    ## Lección 8: Cuarta Declinación, Pretérito Perfecto y Genitivo
    """)
    
    st.image("static/images/curso_gramatica/leccion8_perfect_tense.png",
             caption="El Pretérito Perfecto: Formación y Uso",
             use_container_width=True)
             
    st.markdown("""
    
    ### 1. Cuarta Declinación: Temas en -U
    
    Sustantivos mayoritariamente **masculinos** (aunque hay algunos femeninos y neutros).
    Terminan en **-us** en Nominativo y **-us** en Genitivo (no confundir con la 2ª).
    
    **Modelo: Manus, -us (La mano) - FEMENINO (Excepción)**
    
    """
    )

    render_styled_table(
        ["Caso", "Singular", "Plural"],
        [
            ["**Nominativo**", "man-**us**", "man-**us**"],
            ["**Vocativo**", "man-**us**", "man-**us**"],
            ["**Acusativo**", "man-**um**", "man-**us**"],
            ["**Genitivo**", "man-**us**", "man-**uum**"],
            ["**Dativo**", "man-**ui**", "man-**ibus**"],
            ["**Ablativo**", "man-**u**", "man-**ibus**"]
        ]
    )

    st.markdown("""
    
    **Otros ejemplos de 4ª Declinación:**
    *   *Exercitus, -us* (m): ejército
    *   *Fructus, -us* (m): fruto
    *   *Senatus, -us* (m): senado
    *   *Portus, -us* (m): puerto
    *   *Domus, -us* (f): casa (irregular, mezcla 2ª y 4ª)
    
    **Neutros de 4ª Declinación** (muy raros):
    *   *Cornu, -us* (n): cuerno
    *   *Genu, -us* (n): rodilla
    
    ### 2. Pretérito Perfecto (Perfectum): El Pasado Acabado
    
    El **Pretérito Perfecto** expresa una acción **completada en el pasado**.
    Equivale a "amé", "he amado" en español.
    
    **Formación**: Se construye sobre el **tema de perfecto** (3ª forma del enunciado del verbo).
    
    **Enunciado completo de un verbo**: Siempre se dan 4 formas:
    1.  Presente 1ª Sg: *amo*
    2.  Infinitivo: *amare*
    3.  **Perfecto 1ª Sg**: *amavi*
    4.  Supino: *amatum*
    
    **Terminaciones del Perfecto** (IGUALES para todas las conjugaciones):
    
    """
    )

    render_styled_table(
        ["Persona", "Desinencia", "Ejemplo (AMARE)", "Traducción"],
        [
            ["1ª Sg", "**-i**", "amav-**i**", "yo amé / he amado"],
            ["2ª Sg", "**-isti**", "amav-**isti**", "tú amaste"],
            ["3ª Sg", "**-it**", "amav-**it**", "él/ella amó"],
            ["1ª Pl", "**-imus**", "amav-**imus**", "nosotros amamos"],
            ["2ª Pl", "**-istis**", "amav-**istis**", "vosotros amasteis"],
            ["3ª Pl", "**-erunt/-ere**", "amav-**erunt**", "ellos/ellas amaron"]
        ]
    )

    st.markdown("""
    
    **Ejemplos de otros verbos:**
    *   *Habeo, habere, **habui**, habitum* (tener) -> *habui* (tuve)
    *   *Dico, dicere, **dixi**, dictum* (decir) -> *dixi* (dije)
    *   *Lego, legere, **legi**, lectum* (leer) -> *legi* (leí)
    *   *Video, videre, **vidi**, visum* (ver) -> *vidi* (vi)
    
    ### 3. El Caso Genitivo: Posesión y Pertenencia
    
    El **Genitivo** expresa **posesión**, **pertenencia** o **especificación**.
    Responde a **¿De quién?** o **¿De qué?**
    
    **En español se traduce con**: "de" + sustantivo.
    
    **Ejemplos:**
    *   *Domus patris* (La casa del padre)
        - *Domus*: Nominativo
        - *patris*: **Genitivo** (de quién es la casa)
    *   *Liber pueri* (El libro del niño)
    *   *Amor patriae* (El amor a la patria / de la patria)
    *   *Corona rosarum* (Una corona de rosas)
    
    **Terminaciones de Genitivo:**
    *   1ª Declinación: Sg **-ae**, Pl **-arum**
    *   2ª Declinación: Sg **-i**, Pl **-orum**
    *   3ª Declinación: Sg **-is**, Pl **-um/-ium**
    *   4ª Declinación: Sg **-us**, Pl **-uum**
    """)

def render_lesson_9():
    st.markdown("""
    ## Lección 9: Quinta Declinación y Futuro
    """)
    
    st.image("static/images/curso_gramatica/leccion9_fifth_declension.png",
             caption="La Quinta Declinación: Temas en -E",
             use_container_width=True)
             
    st.markdown("""
    
    ### 1. Quinta Declinación: Temas en -E (La más pequeña)
    
    Sustantivos **femeninos** que terminan en **-es** en Nominativo y **-ei** en Genitivo.
    Es la declinación más pequeña (solo unas 50 palabras).
    
    **Modelo: Dies, diei (El día) - Masc/Fem**
    
    """
    )

    render_styled_table(
        ["Caso", "Singular", "Plural"],
        [
            ["**Nominativo**", "di-**es**", "di-**es**"],
            ["**Vocativo**", "di-**es**", "di-**es**"],
            ["**Acusativo**", "di-**em**", "di-**es**"],
            ["**Genitivo**", "di-**ei**", "di-**erum**"],
            ["**Dativo**", "di-**ei**", "di-**ebus**"],
            ["**Ablativo**", "di-**e**", "di-**ebus**"]
        ]
    )

    st.markdown("""
    
    **Palabra más importante de 5ª Declinación:**
    *   **Res, rei** (f): cosa, asunto, hecho
        - *Res publica* = La cosa pública = La república
    
    **Otras palabras de 5ª Declinación:**
    *   *Spes, spei* (f): esperanza
    *   *Fides, fidei* (f): fe, confianza
    *   *Species, speciei* (f): aspecto, especie
    
    ### 2. Futuro Imperfecto: El Tiempo Venidero
    
    El **Futuro Imperfecto** expresa una acción que **ocurrirá en el futuro**.
    
    **¡Atención!** La formación es **diferente** en 1ª/2ª conj. y 3ª/4ª conj.
    
    #### A. Primera y Segunda Conjugación: Sufijo -BO-
    
    **Modelo: AMARE**
    
    """
    )

    render_styled_table(
        ["Persona", "Forma", "Traducción"],
        [
            ["1ª Sg", "ama-**bo**", "yo amaré"],
            ["2ª Sg", "ama-**bis**", "tú amarás"],
            ["3ª Sg", "ama-**bit**", "él/ella amará"],
            ["1ª Pl", "ama-**bimus**", "nosotros amaremos"],
            ["2ª Pl", "ama-**bitis**", "vosotros amaréis"],
            ["3ª Pl", "ama-**bunt**", "ellos/ellas amarán"]
        ]
    )

    st.markdown("""
    
    **Modelo: MONERE**
    *   *Monebo, monebis, monebit...* (Aconsejaré, aconsejarás...)
    
    #### B. Tercera y Cuarta Conjugación: Vocal -A- / -E-
    
    **Modelo: LEGERE**
    
    """
    )

    render_styled_table(
        ["Persona", "Forma", "Traducción"],
        [
            ["1ª Sg", "leg-**am**", "yo leeré"],
            ["2ª Sg", "leg-**es**", "tú leerás"],
            ["3ª Sg", "leg-**et**", "él/ella leerá"],
            ["1ª Pl", "leg-**emus**", "nosotros leeremos"],
            ["2ª Pl", "leg-**etis**", "vosotros leeréis"],
            ["3ª Pl", "leg-**ent**", "ellos/ellas leerán"]
        ]
    )

    st.markdown("""
    
    **Modelo: AUDIRE**
    *   *Audiam, audies, audiet...* (Oiré, oirás...)
    
    **Futuro de SUM (Irregular):**
    *   *Ero, eris, erit, erimus, eritis, erunt* (Seré, serás...)
    
    ### Resumen de Tiempos Verbales Aprendidos
    
    """
    )

    render_styled_table(
        ["Tiempo", "Significado", "1ª/2ª Conj", "3ª/4ª Conj"],
        [
            ["**Presente**", "amo", "-o, -as, -at", "-o, -is, -it"],
            ["**Imperfecto**", "amaba", "-**ba**m, -**ba**s", "-**eba**m, -**eba**s"],
            ["**Perfecto**", "amé", "-**vi**, -v**isti**", "Varía según verbo"],
            ["**Futuro**", "amaré", "-**bo**, -**bis**", "-**am**, -**es**"]
        ]
    )

    st.markdown("""
    """)

def render_lesson_10():
    st.markdown("""
    ## Lección 10: Adjetivos de Segunda Clase y Sintaxis
    """)
    
    if os.path.exists("static/images/curso_gramatica/leccion10_adjetivos_2clase.png"):
        st.image("static/images/curso_gramatica/leccion10_adjetivos_2clase.png",
                 caption="Clasificación de Adjetivos de 3ª Declinación (2ª Clase)",
                 use_container_width=True)
                 
    st.markdown("""
    
    ### Revisión: Las Cinco Declinaciones y los Casos
    
    Ya hemos cubierto **todas las declinaciones del latín**:
    *   1ª: Femeninos en -a (*rosa, puella*)
    *   2ª: Masculinos en -us/er (*dominus, puer*) y Neutros en -um (*templum*)
    *   3ª: Los tres géneros (*rex, urbs, corpus*)
    *   4ª: Masculinos/Femeninos en -us (*manus, senatus*)
    *   5ª: Femeninos en -es (*res, dies*)
    
    Y **todos los seis casos**: Nominativo, Vocativo, Acusativo, Genitivo, Dativo, Ablativo.
    
    ### 1. Adjetivos de Segunda Clase (3ª Declinación)
    
    Los adjetivos de 2ª Clase se declinan como sustantivos de **3ª Declinación** (temas en -i).
    
    **Tres tipos según el número de terminaciones:**
    
    #### A. Tres Terminaciones (M / F / N)
    
    **Modelo: Acer, acris, acre (Agudo, penetrante)**
    *   Masc: *acer* (como *puer* pero con casos de 3ª)
    *   Fem: *acris*
    *   Neut: *acre*
    
    **Otro ejemplo:**
    *   *Celer, celeris, celere* (rápido)
    
    #### B. Dos Terminaciones (M/F | N)
    
    **Modelo: Omnis, omne (Todo, cada)**
    *   Masc/Fem: *omnis*
    *   Neut: *omne*
    
    **Otros ejemplos:**
    *   *Brevis, breve* (breve, corto)
    *   *Fortis, forte* (fuerte, valiente)
    *   *Tristis, triste* (triste)
    *   *Dulcis, dulce* (dulce)
    
    #### C. Una Terminación (M/F/N)
    
    **Modelo: Felix, felicis (Feliz, afortunado)**
    Solo hay una forma para los tres géneros en Nominativo.
    El género se determina por concordancia con el sustantivo.
    
    **Otros ejemplos:**
    *   *Sapiens, sapientis* (sabio)
    *   *Prudens, prudentis* (prudente)
    *   *Audax, audacis* (audaz)
    *   *Velox, velocis* (veloz)
    
    **Paradigma de Felix**:
    
    """
    )

    render_styled_table(
        ["Caso", "Singular", "Plural"],
        [
            ["Nom (m/f/n)", "felix", "felic-**es** / felic-**ia** (n)"],
            ["Ac (m/f)", "felic-**em**", "felic-**es**"],
            ["Ac (n)", "felix", "felic-**ia**"],
            ["Gen", "felic-**is**", "felic-**ium**"],
            ["Dat/Abl", "felic-**i/-e**", "felic-**ibus**"]
        ]
    )

    st.markdown("""
    
    ### 2. La Aposición: Complemento Nominal
    
    La **aposición** es un sustantivo que explica o determina a otro sustantivo.
    Ambos deben estar en el **mismo caso**.
    
    **Ejemplos:**
    *   *Cicero, consul, dicit.* (Cicerón, el cónsul, dice)
        - *Cicero*: Nominativo
        - *consul*: Nominativo (en aposición)
    *   *Roma, urbs magna, est.* (Roma, la gran ciudad, existe)
    *   *Homerus, poeta Graecus, carmina scripsit.* (Homero, el poeta griego, escribió poemas)
    """)

def render_lesson_11():
    st.markdown("""
    ## Lección 11: Comparación de Adjetivos y Numerales
    """)
    
    if os.path.exists("static/images/curso_gramatica/leccion11_comparison_degrees.png"):
        st.image("static/images/curso_gramatica/leccion11_comparison_degrees.png",
                 caption="Los Grados del Adjetivo: Positivo, Comparativo y Superlativo",
                 use_container_width=True)
                 
    st.markdown("""
    
    ### 1. Grados del Adjetivo
    
    Los adjetivos latinos tienen **tres grados**:
    
    #### A. Positivo (Grado Normal)
    Es la forma básica: *altus* (alto)
    
    #### B. Comparativo (Más que...)
    
    **Formación**: Raíz + **-ior** (m/f) / **-ius** (n)
    
    **Modelo: Altior, altius (Más alto)**
    Se declina como 3ª Declinación.
    
    """
    )

    render_styled_table(
        ["Caso", "Masc/Fem Sg", "Neutro Sg"],
        [
            ["**Nom**", "alt-**ior**", "alt-**ius**"],
            ["**Ac**", "alt-**iorem**", "alt-**ius**"],
            ["**Gen**", "alt-**ioris**", "alt-**ioris**"]
        ]
    )

    st.markdown("""
    
    **Ejemplos:**
    *   *fortis* -> *fortior, fortius* (más fuerte)
    *   *celer* -> *celerior, celerius* (más rápido)
    *   *felix* -> *felicior, felicius* (más feliz)
    
    #### C. Superlativo (El más... / Muy...)
    
    **Formación regular**: Raíz + **-issimus, -a, -um**
    
    **Modelo: Altissimus, -a, -um**
    Se declina como adjetivo de 1ª Clase (2-1-2).
    
    *   *altissimus* = el más alto / altísimo / muy alto
    *   *fortissimus* = el más fuerte / fortísimo
    *   *felicissimus* = el más feliz / felicísimo
    
    **Superlativos irregulares importantes:**
    
    """
    )

    render_styled_table(
        ["Positivo", "Comparativo", "Superlativo"],
        [
            ["*bonus* (bueno)", "*melior* (mejor)", "*optimus* (el mejor / óptimo)"],
            ["*malus* (malo)", "*peior* (peor)", "*pessimus* (el peor / pésimo)"],
            ["*magnus* (grande)", "*maior* (mayor)", "*maximus* (el mayor / máximo)"],
            ["*parvus* (pequeño)", "*minor* (menor)", "*minimus* (el menor / mínimo)"]
        ]
    )

    st.markdown("""
    
    **Construcción del comparativo:**
    - El segundo término va en **Ablativo** (sin preposición): *Petrus altior Paulo est* (Pedro es más alto que Pablo)
    - O con *quam* + mismo caso: *Petrus altior quam Paulus est*
    
    ### 2. Numerales Cardinales y Ordinales
    
    **Cardinales** (cuántos): uno, dos, tres...
    **Ordinales** (en qué orden): primero, segundo, tercero...
    
    """
    )

    render_styled_table(
        ["Número", "Cardinal", "Ordinal"],
        [
            ["1", "*unus, -a, -um*", "*primus, -a, -um*"],
            ["2", "*duo, duae, duo*", "*secundus / alter*"],
            ["3", "*tres, tria*", "*tertius*"],
            ["4", "*quattuor*", "*quartus*"],
            ["5", "*quinque*", "*quintus*"],
            ["6", "*sex*", "*sextus*"],
            ["7", "*septem*", "*septimus*"],
            ["8", "*octo*", "*octavus*"],
            ["9", "*novem*", "*nonus*"],
            ["10", "*decem*", "*decimus*"],
            ["100", "*centum*", "*centesimus*"],
            ["1000", "*mille*", "*millesimus*"]
        ]
    )

    st.markdown("""
    
    > **Nota**: Los cardinales del 4 al 100 son **indeclinables**.
    > *Unus, duo, tres* sí se declinan.
    """)

def render_lesson_12():
    st.markdown("""
    ## Lección 12: Los Pronombres
    """)
    
    if os.path.exists("static/images/curso_gramatica/leccion12_pronouns_demonstratives.png"):
        st.image("static/images/curso_gramatica/leccion12_pronouns_demonstratives.png",
                 caption="Pronombres Demostrativos: Hic, Ille, Is",
                 use_container_width=True)
                 
    st.markdown("""
    
    ### 1. Pronombres Personales
    
    Los pronombres personales se usan para referirse a personas sin nombrarlas.
    
    **Primera y Segunda Persona:**
    
    """
    )

    render_styled_table(
        ["Caso", "1ª Sg (Yo)", "2ª Sg (Tú)", "1ª Pl (Nosotros)", "2ª Pl (Vosotros)"],
        [
            ["**Nom**", "ego", "tu", "nos", "vos"],
            ["**Ac**", "me", "te", "nos", "vos"],
            ["**Gen**", "mei", "tui", "nostrum/nostri", "vestrum/vestri"],
            ["**Dat**", "mihi", "tibi", "nobis", "vobis"],
            ["**Abl**", "me", "te", "nobis", "vobis"]
        ]
    )

    st.markdown("""
    
    > **Nota**: Los pronombres personales en Nominativo **raramente se usan** excepto para énfasis,
    > porque el verbo ya indica la persona.
    
    **Tercera Persona**: Se usa el pronombre demostrativo *is, ea, id* (ver más abajo).
    
    ### 2. Pronombre Reflexivo (SE)
    
    El pronombre reflexivo **se refiere al sujeto de la oración**.
    Solo existe para 3ª persona (no hay formas de 1ª y 2ª, se usan *me, te*).
    
    """
    )

    render_styled_table(
        ["Caso", "Forma", "Significado"],
        [
            ["**Ac**", "**se**", "a sí mismo/a"],
            ["**Gen**", "**sui**", "de sí mismo"],
            ["**Dat**", "**sibi**", "a/para sí mismo"],
            ["**Abl**", "**se**", "consigo mismo"]
        ]
    )

    st.markdown("""
    
    *   *Se amat.* (Él se ama a sí mismo)
    *   *Sibi dicit.* (Se dice a sí mismo)
    
    ### 3. Pronombres-Adjetivos Posesivos
    
    Indican posesión. Se declinan como adjetivos de 1ª Clase.
    
    """
    )

    render_styled_table(
        ["Poseedor", "Singular (cosa poseída)", "Plural (cosas poseídas)"],
        [
            ["Mi(s)", "*meus, -a, -um*", "*mei, -ae, -a*"],
            ["Tu(s)", "*tuus, -a, -um*", "*tui, -ae, -a*"],
            ["Su(s) (de él/ella)", "*suus, -a, -um*", "*sui, -ae, -a*"],
            ["Nuestro(s)", "*noster, nostra, nostrum*", "*nostri, -ae, -a*"],
            ["Vuestro(s)", "*vester, vestra, vestrum*", "*vestri, -ae, -a*"]
        ]
    )

    st.markdown("""
    
    *   *Meus pater* (Mi padre)
    *   *Tua mater* (Tu madre)
    *   *Nostrum oppidum* (Nuestra ciudad)
    
    ### 4. Pronombres-Adjetivos Demostrativos
    
    Señalan personas o cosas en el espacio o en el discurso.
    
    #### A. Hic, haec, hoc (Este, esta, esto)
    Indica **cercanía** al hablante.
    
    *   *Hic puer* (Este niño)
    *   *Haec puella* (Esta niña)
    *   *Hoc templum* (Este templo)
    
    #### B. Ille, illa, illud (Aquel, aquella, aquello)
    Indica **lejanía** del hablante.
    
    *   *Ille rex* (Aquel rey)
    *   *Illa regina* (Aquella reina)
    
    #### C. Is, ea, id (Él, ella, ello / Ese, esa, eso)
    Es el demostrativo **neutro** y también se usa como pronombre personal de 3ª persona.
    
    *   *Is vir* (Este/Ese hombre / Él, el hombre)
    *   *Ea femina* (Ésa mujer / Ella, la mujer)
    
    ### 5. Pronombres Interrogativos
    
    Se usan para hacer preguntas.
    
    *   **Quis? Quid?** (¿Quién? ¿Qué?) - Para personas/cosas
    *   **Qui, quae, quod?** (¿Qué? ¿Cuál?) - Como adjetivo
    *   **Ubi?** (¿Dónde?)
    *   **Quando?** (¿Cuándo?)
    *   **Cur?** (¿Por qué?)
    
    ### 6. Pronombres Relativos
    
    Introducen **oraciones subordinadas adjetivas** (que modifican un sustantivo).
    
    **Qui, quae, quod** (Que, el cual, la cual, lo cual)
    
    *   *Puella quae cantat* (La niña que canta)
    *   *Liber quem lego* (El libro que leo)
    *   *Vir cuius filium video* (El hombre cuyo hijo veo)
    
    **Concordancia**: El relativo concuerda en **género y número** con su antecedente,
    pero su **caso** depende de su función en la oración subordinada.
    """)

def render_lesson_13():
    st.markdown("""
    ## Lección 13: Voz Pasiva y el Ablativo
    """)
    
    st.image("static/images/curso_gramatica/passive_voice_diagram.png",
             caption="La Voz Pasiva: Estructura y Formación",
             use_container_width=True)
             
    st.markdown("""
    
    ### 1. Voz Pasiva: El Sujeto Recibe la Acción
    
    En la **voz activa**, el sujeto **realiza** la acción: *Puer puellam amat* (El niño ama a la niña).
    En la **voz pasiva**, el sujeto **recibe** la acción: *Puella a puero amatur* (La niña es amada por el niño).
    
    **Formación**: Se cambian las **desinencias personales**.
    
    #### Desinencias Personales Pasivas (Sistema de Infectum)
    
    """
    )

    render_styled_table(
        ["Persona", "Activa", "Pasiva"],
        [
            ["1ª Sg", "-o/-m", "**-r**"],
            ["2ª Sg", "-s", "**-ris**"],
            ["3ª Sg", "-t", "**-tur**"],
            ["1ª Pl", "-mus", "**-mur**"],
            ["2ª Pl", "-tis", "**-mini**"],
            ["3ª Pl", "-nt", "**-ntur**"]
        ]
    )

    st.markdown("""
    
    #### Presente Pasivo - Ejemplo: AMARE
    
    """
    )

    render_styled_table(
        ["Persona", "Activa", "Pasiva", "Traducción"],
        [
            ["1ª Sg", "amo", "amo**r**", "yo soy amado"],
            ["2ª Sg", "amas", "ama**ris**", "tú eres amado"],
            ["3ª Sg", "amat", "ama**tur**", "él/ella es amado/a"],
            ["1ª Pl", "amamus", "ama**mur**", "nosotros somos amados"],
            ["2ª Pl", "amatis", "ama**mini**", "vosotros sois amados"],
            ["3ª Pl", "amant", "ama**ntur**", "ellos/ellas son amados/as"]
        ]
    )

    st.markdown("""
    
    #### Imperfecto Pasivo
    *   *Amabar, amabaris, amabatur...* (Yo era amado, tú eras amado...)
    
    #### Futuro Pasívo (1ª/2ª Conj)
    *   *Amabor, amaberis, amabitur...* (Yo seré amado...)
    
    ### 2. Verbos Deponentes: Pasivos en Forma, Activos en Significado
    
    Los **verbos deponentes** tienen forma pasiva pero significado activo.
    (¡Se conjugan como pasivos pero se traducen como activos!)
    
    **Ejemplos importantes:**
    *   **Sequor, sequi, secutus sum** (seguir)
        - *Sequor te* = Te sigo (no "soy seguido por ti")
    *   **Loquor, loqui, locutus sum** (hablar)
    *   **Patior, pati, passus sum** (sufrir, padecer)
    *   **Morior, mori, mortuus sum** (morir)
    *   **Nascor, nasci, natus sum** (nacer)
    
    ### 3. El Caso Ablativo: El Más Versátil
    
    El **Ablativo** es el caso de las **circunstancias**. Es el caso más versátil del latín, 
    con una enorme variedad de usos. Vamos a explorar los complementos circunstanciales en detalle.
    
    ---
    
    ## COMPLEMENTOS CIRCUNSTANCIALES DE LUGAR
    
    Los complementos de lugar expresan dónde ocurre la acción. El latín distingue cuatro tipos fundamentales:
    
    """)
    
    st.image("static/images/curso_gramatica/leccion13_complementos_lugar.png",
             caption="Esquema de los Complementos de Lugar en Latín",
             use_container_width=True)
    
    st.markdown("""
    
    ### 3.1 ¿A DÓNDE? - Movimiento hacia un lugar (Acusativo)
    
    Para expresar **movimiento hacia** un lugar se usa **Acusativo** con preposiciones:
    
    **AD + Acusativo**: "hacia, a" (dirección general)
    *   *Miles ad urbem it.* (El soldado va hacia la ciudad)
    *   *Venit ad Caesarem.* (Viene hacia César)
    *   *Ad forum ambulamus.* (Caminamos hacia el foro)
    
    **IN + Acusativo**: "hacia dentro de, a" (entrada a un espacio cerrado)
    *   *Puer in silvam currit.* (El niño corre hacia el bosque)
    *   *In scholam venio.* (Vengo a la escuela)
    *   *Equus in aquam descendit.* (El caballo desciende al agua)
    
    """)
    
    render_styled_table(
        ["Preposición", "Caso", "Significado", "Ejemplo Latino", "Traducción"],
        [
            ["**AD**", "Acusativo", "hacia, a", "*ad urbem*", "hacia la ciudad"],
            ["**IN**", "Acusativo", "hacia dentro de", "*in silvam*", "hacia el bosque"],
            ["**PER**", "Acusativo", "a través de", "*per viam*", "por el camino"]
        ]
    )
    
    st.markdown("""
    
    ### 3.2 ¿DE DÓNDE? - Procedencia u origen (Ablativo)
    
    Para expresar **procedencia** se usa **Ablativo** con preposiciones:
    
    **A/AB + Ablativo**: "desde, de" (punto de partida, alejamiento)
    *   *Ab urbe venio.* (Vengo desde la ciudad)
    *   *A porta discedunt.* (Se alejan de la puerta)
    *   *A Roma proficiscitur.* (Parte desde Roma)
    
    **DE + Ablativo**: "de, desde" (bajada, descenso)
    *   *De monte descendit.* (Desciende del monte)
    *   *De caelo cadit.* (Cae del cielo)
    *   *De nave exit.* (Sale de la nave)
    
    **EX/E + Ablativo**: "de, fuera de, desde" (salida del interior)
    *   *Ex oppido exeunt.* (Salen de la ciudad)
    *   *E silva veniunt.* (Vienen del bosque)
    *   *Ex urbe fugit.* (Huye de la ciudad)
    
    **Matices importantes**:
    *   *AB*: Énfasis en el alejamiento o punto de partida
    *   *DE*: Énfasis en bajada o descenso
    *   *EX*: Énfasis en salida del interior
    
    """)
    
    render_styled_table(
        ["Preposición", "Caso", "Matiz", "Ejemplo Latino", "Traducción"],
        [
            ["**A/AB**", "Ablativo", "alejamiento", "*ab urbe*", "desde la ciudad"],
            ["**DE**", "Ablativo", "descenso", "*de monte*", "desde el monte"],
            ["**EX/E**", "Ablativo", "salida interior", "*ex oppido*", "fuera de la ciudad"]
        ]
    )
    
    st.markdown("""
    
    ### 3.3 ¿DÓNDE? - Ubicación estática (Ablativo)
    
    Para expresar **ubicación en un lugar** se usa **Ablativo** con preposiciones:
    
    **IN + Ablativo**: "en, dentro de"
    *   *In urbe habito.* (Habito en la ciudad)
    *   *In silva sunt.* (Están en el bosque)
    *   *In templo orat.* (Ora en el templo)
    
    **SUB + Ablativo**: "bajo, debajo de"
    *   *Sub arbore sedet.* (Se sienta bajo el árbol)
    *   *Sub terra latent.* (Se esconden bajo tierra)
    
    **SUPER + Ablativo**: "sobre, encima de"
    *   *Super montem stat.* (Está sobre el monte)
    
    > **¡ATENCIÓN!** La preposición **IN** cambia de significado según el caso:
    > *   **IN + Acusativo** = hacia dentro de (movimiento)
    > *   **IN + Ablativo** = en, dentro de (ubicación estática)
    
    ### 3.4 ¿POR DÓNDE? - Tránsito o paso (Acusativo)
    
    **PER + Acusativo**: "por, a través de"
    *   *Per viam ambulat.* (Camina por el camino)
    *   *Per silvam iter faciunt.* (Hacen el viaje a través del bosque)
    *   *Per forum transit.* (Pasa por el foro)
    
    """)
    
    st.image("static/images/curso_gramatica/leccion13_preposiciones_casos.png",
             caption="Preposiciones de Lugar con sus Casos Gramaticales",
             use_container_width=True)
    
    st.image("static/images/curso_gramatica/leccion13_decision_preposiciones.png",
             caption="Diagrama de Decisión: ¿Qué Preposición Usar?",
             use_container_width=True)
    
    st.markdown("""
    
    ### 3.5 EL LOCATIVO: Caso Especial para Ciudades
    
    El **Locativo** es un caso arcaico que sobrevive SOLO para:
    *   Nombres de **ciudades** y **pueblos**
    *   Nombres de **islas pequeñas**
    *   Las palabras **domus** (casa) y **rus** (campo)
    
    """)
    
    st.image("static/images/curso_gramatica/leccion13_locativo.png",
             caption="El Locativo: Nombres de Ciudades e Islas Pequeñas",
             use_container_width=True)
    
    st.markdown("""
    
    **Terminaciones del Locativo:**
    
    """)
    
    render_styled_table(
        ["Declinación", "Singular", "Plural", "Ejemplos"],
        [
            ["**1ª Decl**", "-ae", "-is", "*Romae* (en Roma), *Athenis* (en Atenas)"],
            ["**2ª Decl**", "-i", "-is", "*Corinthi* (en Corinto), *Delphi* (en Delfos)"],
            ["**3ª Decl**", "-i / -e", "-ibus", "*Carthagine* (en Cartago)"]
        ]
    )
    
    st.markdown("""
    
    **Ejemplos con ciudades:**
    *   **Ubicación**: *Romae vivit.* (Vive en Roma) - Locativo
    *   **Dirección**: *Romam it.* (Va a Roma) - Acusativo sin preposición
    *   **Procedencia**: *Roma venit.* (Viene de Roma) - Ablativo sin preposición
    
    **Palabras especiales:**
    *   *Domi* (en casa): *Domi maneo.* (Me quedo en casa)
    *   *Domum* (a casa): *Domum eo.* (Voy a casa)
    *   *Domo* (de casa): *Domo venio.* (Vengo de casa)
    
    > **Nota**: Las ciudades grandes a veces usan *in + Ablativo* en lugar del locativo.
    
    ---
    
    ## COMPLEMENTOS CIRCUNSTANCIALES DE TIEMPO
    """)
    
    st.image("static/images/curso_gramatica/leccion13_complementos_tiempo.png",
             caption="Esquema de los Complementos de Tiempo en Latín",
             use_container_width=True)
    
    st.markdown("""
    
    ### 4.1 ¿CUÁNDO? - Momento determinado (Ablativo sin preposición)
    
    Para expresar **en qué momento** ocurre algo, se usa **Ablativo SIN preposición**:
    
    *   *Prima hora venio.* (Vengo en la primera hora)
    *   *Aestate* (En verano)
    *   *Hieme* (En invierno)
    *   *Nocte* (De noche)
    *   *Die* (De día)
    *   *Hora sexta* (A la hora sexta)
    *   *Tertio die* (Al tercer día)
    
    **Ejemplos en contexto:**
    *   *Nocte stellae lucent.* (De noche brillan las estrellas)
    *   *Prima luce proficiscuntur.* (Parten al amanecer)
    *   *Aestate in agris laborant.* (En verano trabajan en los campos)
    
    ### 4.2 ¿DESDE CUÁNDO? - Punto de partida temporal (Ablativo con preposición)
    
    **A/AB + Ablativo**: "desde"
    *   *A prima luce laborat.* (Trabaja desde el amanecer)
    *   *Ab illo tempore* (Desde aquel tiempo)
    *   *A pueritia* (Desde la infancia)
    
    **EX + Ablativo**: "desde, a partir de"
    *   *Ex eo tempore* (Desde ese tiempo)
    *   *Ex hoc die* (A partir de este día)
    
    ### 4.3 ¿HASTA CUÁNDO? - Límite temporal (Acusativo)
    
    **AD + Acusativo**: "hasta"
    *   *Ad vesperum manet.* (Permanece hasta la tarde)
    *   *Ad noctem pugnaverunt.* (Lucharon hasta la noche)
    
    **USQUE AD + Acusativo**: "hasta" (con énfasis)
    *   *Usque ad mortem fidelis.* (Fiel hasta la muerte)
    *   *Usque ad noctem* (Hasta la noche)
    
    ### 4.4 ¿CUÁNTO TIEMPO? - Duración (Acusativo sin preposición)
    
    Para expresar **duración** se usa **Acusativo SIN preposición**:
    
    *   *Tres dies maneo.* (Permanezco tres días)
    *   *Multos annos vixit.* (Vivió muchos años)
    *   *Totam noctem vigilat.* (Vigila toda la noche)
    *   *Decem annos regnavit.* (Reinó diez años)
    
    **PER + Acusativo**: Duración con énfasis en la continuidad
    *   *Per decem annos* (Durante diez años [continuamente])
    *   *Per totam vitam* (Durante toda la vida)
    
    """)
    
    render_styled_table(
        ["Pregunta", "Construcción", "Ejemplo Latino", "Traducción"],
        [
            ["**¿Cuándo?**", "Ablativo solo", "*nocte*", "de noche"],
            ["**¿Desde cuándo?**", "A/AB + Abl", "*a prima luce*", "desde el amanecer"],
            ["**¿Hasta cuándo?**", "AD + Acus", "*ad vesperum*", "hasta la tarde"],
            ["**¿Cuánto tiempo?**", "Acusativo solo", "*tres dies*", "tres días"]
        ]
    )
    
    st.markdown("""
    
    ---
    
    ## OTROS COMPLEMENTOS CIRCUNSTANCIALES
    """)
    
    st.image("static/images/curso_gramatica/leccion13_otros_complementos.png",
             caption="Otros Complementos Circunstanciales: Modo, Causa, Instrumento, etc.",
             use_container_width=True)
    
    st.markdown("""
    
    ### 5.1 Modo (¿Cómo?)
    
    **CUM + Ablativo**: Con + cualidad
    *   *Cum gaudio venit.* (Viene con alegría)
    *   *Cum studio laborat.* (Trabaja con empeño)
    *   *Magna cum laude* (Con gran alabanza)
    
    **Ablativo de cualidad solo** (sin preposición):
    *   *Magna voce clamat.* (Grita en voz alta)
    *   *Summa celeritate* (Con suma rapidez)
    
    ### 5.2 Causa (¿Por qué?)
    
    **OB/PROPTER + Acusativo**: "a causa de, por"
    *   *Propter bellum fugiunt.* (Huyen a causa de la guerra)
    *   *Ob metum tacet.* (Calla por miedo)
    
    **Ablativo de causa** (sin preposición):
    *   *Metu fugiunt.* (Huyen por miedo)
    *   *Amore patriae pugnat.* (Lucha por amor a la patria)
    
    ### 5.3 Medio o Instrumento (¿Con qué?)
    
    **Ablativo SIN preposición** (cosas):
    *   *Gladio pugnat.* (Lucha con la espada)
    *   *Oculis videt.* (Ve con los ojos)
    *   *Navibus veniunt.* (Vienen en barcos)
    
    **PER + Acusativo** (medio, intermediario):
    *   *Per nuntium dicit.* (Dice mediante un mensajero)
    *   *Per epistulam scribit.* (Escribe por carta)
    
    ### 5.4 Compañía (¿Con quién?)
    
    **CUM + Ablativo**:
    *   *Cum amicis ambulo.* (Camino con los amigos)
    *   *Cum patre venit.* (Viene con el padre)
    *   *Cum militibus pugnat.* (Lucha con los soldados)
    
    ### 5.5 Complemento Agente (con Pasiva)
    
    **A/AB + Ablativo** (persona que realiza la acción en voz pasiva):
    *   *Urbs a Romanis capitur.* (La ciudad es tomada por los romanos)
    *   *Puella a patre amatur.* (La niña es amada por el padre)
    *   *Liber a Marco legitur.* (El libro es leído por Marco)
    
    ### 5.6 Materia (¿De qué está hecho?)
    
    **EX/DE + Ablativo**:
    *   *Statua ex auro est.* (La estatua es de oro)
    *   *Domus de ligno* (Casa de madera)
    
    ---
    
    ## RESUMEN DE USOS DEL ABLATIVO
    
    El Ablativo es el caso más versátil. Resumen de sus principales funciones:
    
    """)
    
    render_styled_table(
        ["Uso", "Construcción", "Ejemplo", "Traducción"],
        [
            ["**Agente**", "a/ab + Abl", "*a patre*", "por el padre"],
            ["**Instrumento**", "Abl solo", "*gladio*", "con la espada"],
            ["**Compañía**", "cum + Abl", "*cum amicis*", "con los amigos"],
            ["**Modo**", "cum + Abl / Abl solo", "*magna voce*", "en voz alta"],
            ["**Causa**", "Abl solo / propter + Ac", "*metu*", "por miedo"],
            ["**Lugar ¿dónde?**", "in + Abl", "*in urbe*", "en la ciudad"],
            ["**Lugar ¿de dónde?**", "ab/ex/de + Abl", "*ab urbe*", "desde la ciudad"],
            ["**Tiempo ¿cuándo?**", "Abl solo", "*nocte*", "de noche"],
            ["**Materia**", "ex/de + Abl", "*ex auro*", "de oro"]
        ]
    )
    
    st.markdown("""
    
    ### Vocabulario Esencial de Lugar y Tiempo
    
    **Lugares:**
    *   *urbs, urbis* (f): ciudad
    *   *oppidum, -i* (n): ciudad, plaza fuerte
    *   *silva, -ae* (f): bosque
    *   *mons, montis* (m): monte
    *   *via, -ae* (f): camino
    *   *forum, -i* (n): foro
    *   *templum, -i* (n): templo
    *   *porta, -ae* (f): puerta
    
    **Tiempo:**
    *   *hora, -ae* (f): hora
    *   *dies, diei* (m/f): día
    *   *nox, noctis* (f): noche
    *   *annus, -i* (m): año
    *   *aestas, aestatis* (f): verano
    *   *hiems, hiemis* (f): invierno
    *   *tempus, temporis* (n): tiempo
    *   *lux, lucis* (f): luz (prima luce = al amanecer)
    
    ### Resumen Final: ¡Has Completado el Curso!
    
    ¡Felicidades! Ahora conoces:
    *   ✓ Las **5 declinaciones** del latín
    *   ✓ Los **6 casos** y sus funciones
    *   ✓ Las **4 conjugaciones** verbales
    *   ✓ Los **4 tiempos principales**: Presente, Imperfecto, Perfecto, Futuro
    *   ✓ La **voz pasiva** y los verbos deponentes
    *   ✓ Los **pronombres** personales, demostrativos y relativos
    *   ✓ Los **grados del adjetivo**: positivo, comparativo, superlativo
    
    ¡Ahora estás listo para leer textos latinos originales!
    """)

def render_lesson_14():
    st.markdown("""
    ## Lección 14: Pluscuamperfecto y Futuro Perfecto
    """)
    
    if os.path.exists("static/images/curso_gramatica/leccion14_pluperfect_futureperfect.png"):
        st.image("static/images/curso_gramatica/leccion14_pluperfect_futureperfect.png",
                 caption="Línea de tiempo del Sistema de Perfectum",
                 use_container_width=True)
                 
    st.markdown("""
    
    ### Nivel Avanzado: Completando el Sistema de Perfectum
    
    Ya conoces el **Pretérito Perfecto** (amavi = amé / he amado). Ahora aprenderemos los dos tiempos 
    restantes del **Sistema de Perfectum** que se forman sobre el mismo tema.
    
    ### 1. Pretérito Pluscuamperfecto: El Pasado Anterior
    
    El **Pretérito Pluscuamperfecto** expresa una acción pasada **anterior a otra acción pasada**.
    Equivale a "había amado" en español.
    
    **Formación**: Tema de Perfecto + **-eram, -eras, -erat, -eramus, -eratis, -erant**
    
    > Observa que las terminaciones son **idénticas al Imperfecto de SUM** (eram, eras, erat...)
    
    #### Paradigma: AMARE (Tema de perfecto: amav-)
    
    """
    )

    render_styled_table(
        ["Persona", "Forma", "Traducción"],
        [
            ["1ª Sg", "amav-**eram**", "yo había amado"],
            ["2ª Sg", "amav-**eras**", "tú habías amado"],
            ["3ª Sg", "amav-**erat**", "él/ella había amado"],
            ["1ª Pl", "amav-**eramus**", "nosotros habíamos amado"],
            ["2ª Pl", "amav-**eratis**", "vosotros habíais amado"],
            ["3ª Pl", "amav-**erant**", "ellos/ellas habían amado"]
        ]
    )

    st.markdown("""
    
    #### Otros ejemplos con verbos irregulares:
    
    """
    )

    render_styled_table(
        ["Verbo", "Perfecto (3ª Sg)", "Pluscuamperfecto (3ª Sg)", "Traducción"],
        [
            ["*Habeo*", "*habuit*", "*habu**erat***", "había tenido"],
            ["*Dico*", "*dixit*", "*dix**erat***", "había dicho"],
            ["*Lego*", "*legit*", "*leg**erat***", "había leído"],
            ["*Sum*", "*fuit*", "*fu**erat***", "había sido/estado"],
            ["*Venio*", "*venit*", "*ven**erat***", "había venido"]
        ]
    )

    st.markdown("""
    
    **Ejemplos en contexto**:
    *   *Caesar, antequam Romani venerunt, ad Galliam pervener**at**.* 
        (César **había llegado** a la Galia antes de que los romanos vinieran)
    *   *Puella rosam, quam puer dederat, amabat.*
        (La niña amaba la rosa que el niño **le había dado**)
    *   *Milites, qui diu pugav**erant**, fessi erant.*
        (Los soldados, que **habían luchado** mucho tiempo, estaban cansados)
    
    ### 2. Futuro Perfecto: El Pasado en el Futuro
    
    El **Futuro Perfecto** expresa una acción que **estará completada en el futuro**.
    Equivale a "habré amado" en español.
    
    **Formación**: Tema de Perfecto + **-ero, -eris, -erit, -erimus, -eritis, -erint**
    
    > ¡Atención! Las terminaciones son casi idénticas al **Futuro de SUM** (ero, eris, erit...)
    > excepto en la 3ª persona plural: -erint (no -erunt)
    
    #### Paradigma: AMARE
    
    """
    )

    render_styled_table(
        ["Persona", "Forma", "Traducción"],
        [
            ["1ª Sg", "amav-**ero**", "yo habré amado"],
            ["2ª Sg", "amav-**eris**", "tú habrás amado"],
            ["3ª Sg", "amav-**erit**", "él/ella habrá amado"],
            ["1ª Pl", "amav-**erimus**", "nosotros habremos amado"],
            ["2ª Pl", "amav-**eritis**", "vosotros habréis amado"],
            ["3ª Pl", "amav-**erint**", "ellos/ellas habrán amado"]
        ]
    )

    st.markdown("""
    
    **Uso típico**: En oraciones temporales con *cum, ubi, postquam, simul atque*
    
    *   *Cum hoc fec**eris**, felix eris.*
        (Cuando **hayas hecho** esto, serás feliz)
    *   *Simul atque ven**eris**, tibi dicam.*
        (Tan pronto como **hayas venido**, te diré)
    *   *Si hoc leg**erit**, intelleget.*
        (Si **hubiere leído** esto, lo entenderá)
    
    ### 3. Resumen: Sistema Completo de Perfectum (Activo)
    
    """
    )

    render_styled_table(
        ["Tiempo", "Terminaciones", "Ejemplo (AMARE)", "Significado"],
        [
            ["**Perfecto**", "-i, -isti, -it, -imus, -istis, -erunt", "amav**i**", "amé / he amado"],
            ["**Pluscuamperfecto**", "-eram, -eras, -erat, -eramus, -eratis, -erant", "amav**eram**", "había amado"],
            ["**Futuro Perfecto**", "-ero, -eris, -erit, -erimus, -eritis, -erint", "amav**ero**", "habré amado"]
        ]
    )

    st.markdown("""
    
    > **Clave**: Los tres tiempos se forman sobre el **mismo tema de perfecto**, 
    > solo cambian las terminaciones.
    
    ### 4. Ejercicio de Conjugación
    
    Conjuga en los tres tiempos los siguientes verbos (3ª persona singular):
    
    """
    )

    render_styled_table(
        ["Verbo", "Perfecto", "Pluscuamperfecto", "Futuro Perfecto"],
        [
            ["*Porto, portare, portavi, portatum*", "*portavit*", "*portav**erat***", "*portav**erit***"],
            ["*Moneo, monere, monui, monitum*", "*monuit*", "*monu**erat***", "*monu**erit***"],
            ["*Mitto, mittere, misi, missum*", "*misit*", "*mis**erat***", "*mis**erit***"],
            ["*Audio, audire, audivi, auditum*", "*audivit*", "*audiv**erat***", "*audiv**erit***"]
        ]
    )

    st.markdown("""
    
    ### Vocabulario Esencial
    *   **antequam**: antes de que
    *   **postquam**: después de que
    *   **ubi**: cuando (tan pronto como)
    *   **simul atque / simul ac**: tan pronto como
    *   **priusquam**: antes de que
    *   **cum primum**: apenas, en cuanto
    """)

def render_lesson_15():
    st.markdown("""
    ## Lección 15: Voz Pasiva - Sistema de Infectum
    """)
    
    if os.path.exists("static/images/curso_gramatica/leccion15_passive_conjugation_chart.png"):
        st.image("static/images/curso_gramatica/leccion15_passive_conjugation_chart.png",
                 caption="Tabla completa de la Voz Pasiva (Infectum)",
                 use_container_width=True)
                 
    st.markdown("""
    
    ### Completando la Voz Pasiva
    
    En la Lección 13 viste una introducción a la voz pasiva. Ahora vamos a dominarla completamente 
    para el **Sistema de Infectum** (Presente, Imperfecto, Futuro).
    
    ### 1. Recordatorio: ¿Qué es la Voz Pasiva?
    
    **Voz Activa**: El sujeto **realiza** la acción
    *   *Puer puellam amat.* (El niño ama a la niña)
    
    **Voz Pasiva**: El sujeto **recibe** la acción
    *   *Puella a puero amatur.* (La niña es amada por el niño)
    
    ### 2. Desinencias Personales Pasivas
    
    Las desinencias activas se reemplazan por desinencias pasivas:
    
    """
    )

    render_styled_table(
        ["Persona", "Activa", "Pasiva"],
        [
            ["1ª Sg", "-o / -m", "**-r** / **-or**"],
            ["2ª Sg", "-s", "**-ris** / **-re**"],
            ["3ª Sg", "-t", "**-tur**"],
            ["1ª Pl", "-mus", "**-mur**"],
            ["2ª Pl", "-tis", "**-mini**"],
            ["3ª Pl", "-nt", "**-ntur**"]
        ]
    )

    st.markdown("""
    
    ### 3. Presente Pasivo - Las Cuatro Conjugaciones
    
    #### Primera Conjugación: AMARE
    
    """
    )

    render_styled_table(
        ["Persona", "Activa", "Pasiva", "Traducción"],
        [
            ["1ª Sg", "amo", "am**or**", "yo soy amado/a"],
            ["2ª Sg", "amas", "ama**ris** / ama**re**", "tú eres amado/a"],
            ["3ª Sg", "amat", "ama**tur**", "él/ella es amado/a"],
            ["1ª Pl", "amamus", "ama**mur**", "nosotros somos amados/as"],
            ["2ª Pl", "amatis", "ama**mini**", "vosotros sois amados/as"],
            ["3ª Pl", "amant", "ama**ntur**", "ellos/ellas son amados/as"]
        ]
    )

    st.markdown("""
    
    #### Segunda Conjugación: MONERE
    
    """
    )

    render_styled_table(
        ["Persona", "Pasiva", "Traducción"],
        [
            ["1ª Sg", "mone**or**", "yo soy aconsejado/a"],
            ["2ª Sg", "mone**ris**", "tú eres aconsejado/a"],
            ["3ª Sg", "mone**tur**", "él/ella es aconsejado/a"],
            ["1ª Pl", "mone**mur**", "nosotros somos aconsejados/as"],
            ["2ª Pl", "mone**mini**", "vosotros sois aconsejados/as"],
            ["3ª Pl", "mone**ntur**", "ellos/ellas son aconsejados/as"]
        ]
    )

    st.markdown("""
    
    #### Tercera Conjugación: LEGERE
    
    """
    )

    render_styled_table(
        ["Persona", "Pasiva", "Traducción"],
        [
            ["1ª Sg", "leg**or**", "yo soy leído/a"],
            ["2ª Sg", "lege**ris**", "tú eres leído/a"],
            ["3ª Sg", "legi**tur**", "él/ella es leído/a"],
            ["1ª Pl", "legi**mur**", "nosotros somos leídos/as"],
            ["2ª Pl", "legi**mini**", "vosotros sois leídos/as"],
            ["3ª Pl", "leg**untur**", "ellos/ellas son leídos/as"]
        ]
    )

    st.markdown("""
    
    #### Cuarta Conjugación: AUDIRE
    
    """
    )

    render_styled_table(
        ["Persona", "Pasiva", "Traducción"],
        [
            ["1ª Sg", "audi**or**", "yo soy oído/a"],
            ["2ª Sg", "audi**ris**", "tú eres oído/a"],
            ["3ª Sg", "audi**tur**", "él/ella es oído/a"],
            ["1ª Pl", "audi**mur**", "nosotros somos oídos/as"],
            ["2ª Pl", "audi**mini**", "vosotros sois oídos/as"],
            ["3ª Pl", "audi**untur**", "ellos/ellas son oídos/as"]
        ]
    )

    st.markdown("""
    
    ### 4. Imperfecto Pasivo
    
    **Formación**: Raíz + **vocal temática + -ba- + desinencias pasivas**
    
    #### Las Cuatro Conjugaciones:
    
    """
    )

    render_styled_table(
        ["Conjugación", "1ª Sg", "2ª Sg", "3ª Sg", "Ejemplo"],
        [
            ["**1ª**", "ama**bar**", "ama**baris**", "ama**batur**", "yo era amado"],
            ["**2ª**", "mone**bar**", "mone**baris**", "mone**batur**", "yo era aconsejado"],
            ["**3ª**", "lege**bar**", "lege**baris**", "lege**batur**", "yo era leído"],
            ["**4ª**", "audie**bar**", "audie**baris**", "audie**batur**", "yo era oído"]
        ]
    )

    st.markdown("""
    
    **Ejemplos**:
    *   *Liber a discipulis legebatur.* (El libro era leído por los discípulos)
    *   *Urbs ab hostibus oppugnabatur.* (La ciudad era atacada por los enemigos)
    
    ### 5. Futuro Pasivo
    
    #### Primera y Segunda Conjugación: Sufijo -B-
    
    """
    )

    render_styled_table(
        ["Conjugación", "1ª Sg", "2ª Sg", "3ª Sg"],
        [
            ["**1ª**", "ama**bor**", "ama**beris**", "ama**bitur**"],
            ["**2ª**", "mone**bor**", "mone**beris**", "mone**bitur**"]
        ]
    )

    st.markdown("""
    
    #### Tercera y Cuarta Conjugación: Vocal -E-/-I- 
    
    """
    )

    render_styled_table(
        ["Conjugación", "1ª Sg", "2ª Sg", "3ª Sg"],
        [
            ["**3ª**", "leg**ar**", "leg**eris**", "leg**etur**"],
            ["**4ª**", "audi**ar**", "audi**eris**", "audi**etur**"]
        ]
    )

    st.markdown("""
    
    **Ejemplos**:
    *   *Cras laudabor.* (Mañana seré alabado)
    *   *Epistula cras legetur.* (La carta será leída mañana)
    
    ### 6. Complemento Agente vs. Instrumento
    
    **Complemento Agente** (persona que realiza la acción):
    *   Preposición **a/ab** + Ablativo
    *   *Urbs a Romanis capitur.* (La ciudad es tomada **por los romanos**)
    
    **Complemento Instrumento** (medio por el cual se realiza):
    *   Ablativo **sin preposición**
    *   *Milites gladiis pugnant.* (Los soldados luchan **con espadas**)
    *   *Urbs armis capitur.* (La ciudad es tomada **con armas**)
    
    ### Vocabulario Esencial
    Verbos transitivos frecuentes en pasiva:
    *   **Laudo, laudare**: alabar
    *   **Pugno, pugnare**: luchar
    *   **Capio, capere, cepi, captum**: tomar, capturar
    *   **Vincio, vincire, vinxi, vinctum**: atar, encadenar
    *   **Oppugno, oppugnare**: atacar
    *   **Deligo, deligere, delegi, delectum**: elegir
    """)

def render_lesson_16():
    st.markdown("""
    ## Lección 16: Voz Pasiva - Sistema de Perfectum
    """)
    
    if os.path.exists("static/images/curso_gramatica/leccion16_passive_perfect_system.png"):
        st.image("static/images/curso_gramatica/leccion16_passive_perfect_system.png",
                 caption="Formación del Sistema de Perfectum Pasivo",
                 use_container_width=True)
                 
    st.markdown("""
    
    ### El Participio Perfecto Pasivo
    
    La voz pasiva del Sistema de Perfectum se forma de manera **completamente diferente** 
    al Sistema de Infectum. No usa desinencias especiales, sino una **construcción perifrástica** 
    con el Participio Perfecto Pasivo.
    
    ### 1. El Participio Perfecto Pasivo (PPP)
    
    El **Participio Perfecto Pasivo** es un **adjetivo verbal** que se declina como 
    los adjetivos de 1ª clase (*bonus, -a, -um*).
    
    **Formación**: Se forma sobre el **tema de supino** (4ª forma del enunciado del verbo).
    
    #### Ejemplos:
    
    """
    )

    render_styled_table(
        ["Verbo", "Supino", "PPP (m/f/n)", "Traducción"],
        [
            ["*Amo, amare, amavi, **amatum***", "amat-", "amat**us, -a, -um**", "amado/a"],
            ["*Moneo, monere, monui, **monitum***", "monit-", "monit**us, -a, -um**", "aconsejado/a"],
            ["*Lego, legere, legi, **lectum***", "lect-", "lect**us, -a, -um**", "leído/a"],
            ["*Audio, audire, audivi, **auditum***", "audit-", "audit**us, -a, -um**", "oído/a"],
            ["*Capio, capere, cepi, **captum***", "capt-", "capt**us, -a, -um**", "capturado/a"],
            ["*Vinco, vincere, vici, **victum***", "vict-", "vict**us, -a, -um**", "vencido/a"]
        ]
    )

    st.markdown("""
    
    **Concordancia**: El PPP concuerda en **género, número y caso** con el sujeto.
    
    ### 2. Pretérito Perfecto Pasivo
    
    **Fórmula**: **Participio Perfecto Pasivo + Presente de SUM**
    
    #### Paradigma: AMARE (Masculino)
    
    """
    )

    render_styled_table(
        ["Persona", "Forma", "Traducción"],
        [
            ["1ª Sg", "amat**us sum**", "yo fui amado / he sido amado"],
            ["2ª Sg", "amat**us es**", "tú fuiste amado"],
            ["3ª Sg", "amat**us est**", "él fue amado"],
            ["1ª Pl", "amat**i sumus**", "nosotros fuimos amados"],
            ["2ª Pl", "amat**i estis**", "vosotros fuisteis amados"],
            ["3ª Pl", "amat**i sunt**", "ellos fueron amados"]
        ]
    )

    st.markdown("""
    
    #### Femenino y Neutro:
    *   Femenino Sg: *amata sum, amata es, amata est*
    *   Neutro Sg: *amatum est* (solo 3ª persona, cosas)
    *   Femenino Pl: *amatae sumus, amatae estis, amatae sunt*
    *   Neutro Pl: *amata sunt*
    
    **Ejemplos**:
    *   *Urbs a Romanis capt**a est**.* (La ciudad fue capturada por los romanos)
    *   *Epistola lect**a est**.* (La carta fue leída)
    *   *Milites vinct**i sunt**.* (Los soldados fueron encadenados)
    
    ### 3. Pretérito Pluscuamperfecto Pasivo
    
    **Fórmula**: **Participio Perfecto Pasivo + Imperfecto de SUM** (eram, eras, erat...)
    
    #### Paradigma: AMARE (Masculino)
    
    """
    )

    render_styled_table(
        ["Persona", "Forma", "Traducción"],
        [
            ["1ª Sg", "amat**us eram**", "yo había sido amado"],
            ["2ª Sg", "amat**us eras**", "tú habías sido amado"],
            ["3ª Sg", "amat**us erat**", "él había sido amado"],
            ["1ª Pl", "amat**i eramus**", "nosotros habíamos sido amados"],
            ["2ª Pl", "amat**i eratis**", "vosotros habíais sido amados"],
            ["3ª Pl", "amat**i erant**", "ellos habían sido amados"]
        ]
    )

    st.markdown("""
    
    **Ejemplos**:
    *   *Urbs iam capt**a erat** cum Caesar advenit.*
        (La ciudad **ya había sido capturada** cuando César llegó)
    *   *Liber antea lect**us erat**.*
        (El libro **había sido leído** antes)
    
    ### 4. Futuro Perfecto Pasivo
    
    **Fórmula**: **Participio Perfecto Pasivo + Futuro de SUM** (ero, eris, erit...)
    
    #### Paradigma: AMARE (Masculino)
    
    """
    )

    render_styled_table(
        ["Persona", "Forma", "Traducción"],
        [
            ["1ª Sg", "amat**us ero**", "yo habré sido amado"],
            ["2ª Sg", "amat**us eris**", "tú habrás sido amado"],
            ["3ª Sg", "amat**us erit**", "él habrá sido amado"],
            ["1ª Pl", "amat**i erimus**", "nosotros habremos sido amados"],
            ["2ª Pl", "amat**i eritis**", "vosotros habréis sido amados"],
            ["3ª Pl", "amat**i erunt**", "ellos habrán sido amados"]
        ]
    )

    st.markdown("""
    
    **Ejemplos**:
    *   *Cum hoc factum **erit**, gaudebo.*
        (Cuando esto **haya sido hecho**, me alegraré)
    
    ### 5. Participios Perfectos Pasivos Irregulares Importantes
    
    Muchos verbos tienen PPP irregular. Memoriza estos frecuentes:
    
    """
    )

    render_styled_table(
        ["Verbo", "PPP", "Traducción"],
        [
            ["*Dico, dicere, dixi, **dictum***", "dict**us**", "dicho"],
            ["*Scribo, scribere, scripsi, **scriptum***", "script**us**", "escrito"],
            ["*Facio, facere, feci, **factum***", "fact**us**", "hecho"],
            ["*Video, videre, vidi, **visum***", "vis**us**", "visto"],
            ["*Mitto, mittere, misi, **missum***", "miss**us**", "enviado"],
            ["*Pono, ponere, posui, **positum***", "posit**us**", "puesto"],
            ["*Rego, regere, rexi, **rectum***", "rect**us**", "regido"],
            ["*Duco, ducere, duxi, **ductum***", "duct**us**", "conducido"]
        ]
    )

    st.markdown("""
    
    ### 6. Resumen: Sistema Completo de Voz Pasiva
    
    """
    )

    render_styled_table(
        ["Tiempo", "Sistema Infectum", "Sistema Perfectum"],
        [
            ["**Presente**", "am**or**", "—"],
            ["**Imperfecto**", "ama**bar**", "—"],
            ["**Futuro**", "ama**bor** / leg**ar**", "—"],
            ["**Perfecto**", "—", "amat**us sum**"],
            ["**Pluscuamperfecto**", "—", "amat**us eram**"],
            ["**Futuro Perfecto**", "—", "amat**us ero**"]
        ]
    )

    st.markdown("""
    
    ### 7. Usos del Participio Perfecto Pasivo
    
    El PPP no solo se usa en tiempos verbales, sino también como:
    
    1. **Adjetivo atributivo**:
       *   *Liber **lectus*** (El libro leído)
       *   *Urbs **capta*** (La ciudad capturada)
    
    2. **Ablativo Absoluto** (veremos en Lección 25):
       *   ***His rebus cognitis***, Caesar consilium cepit.
           (Conocidas estas cosas, César tomó una decisión)
    
    ### Vocabulario Esencial
    Verbos con PPP irregular frecuente:
    *   **Facio, facere, feci, factum**: hacer
    *   **Dico, dicere, dixi, dictum**: decir
    *   **Scribo, scribere, scripsi, scriptum**: escribir
    *   **Mitto, mittere, misi, missum**: enviar
    *   **Capio, capere, cepi, captum**: tomar
    *   **Video, videre, vidi, visum**: ver
    """)

def render_lesson_17():
    st.markdown("""
    ## Lección 17: Verbos Deponentes y Semideponentes
    """)
    
    if os.path.exists("static/images/curso_gramatica/leccion17_deponent_verbs.png"):
        st.image("static/images/curso_gramatica/leccion17_deponent_verbs.png",
                 caption="Verbos Deponentes: Forma Pasiva, Significado Activo",
                 use_container_width=True)
                 
    st.markdown("""
    
    ### Una Particularidad del Latín
    
    Los **verbos deponentes** son una característica única del latín que a menudo confunde a los estudiantes,
    pero una vez comprendidos, se vuelven fascinantes.
    
    ### 1. ¿Qué son los Verbos Deponentes?
    
    **Deponente** viene de *deponere* (deponer, dejar de lado). Estos verbos "depusieron" su forma activa
    y solo se conjugan en **voz pasiva**, pero conservan **significado activo**.
    
    **Regla de oro**:
    > Forma pasiva + Significado activo = Verbo Deponente
    
    **Ejemplos**:
    *   *Sequor* (sigo) - Forma: sequor (soy seguido) - Significado: "yo sigo" (activo)
    *   *Loquor* (hablo) - Forma: loquor (soy hablado) - Significado: "yo hablo" (activo)
    
    ### 2. Las Cuatro Conjugaciones de Deponentes
    
    Los deponentes se conjugan como verbos pasivos de su conjugación correspondiente.
    
    #### Primera Conjugación: HORTOR, HORTARI, HORTATUS SUM (exhortar, animar)
    
    **Enunciado**: *Hortor, hortari, hortatus sum*
    - 1ª forma: Presente Indicativo (1ª persona singular)
    - 2ª forma: Infinitivo Presente
    - 3ª forma: Perfecto (PPP + sum)
    
    **Presente Indicativo**:
    
    """
    )

    render_styled_table(
        ["Persona", "Forma", "Traducción"],
        [
            ["1ª Sg", "hort**or**", "yo exhorto"],
            ["2ª Sg", "hort**āris** / hort**āre**", "tú exhortas"],
            ["3ª Sg", "hort**ātur**", "él/ella exhorta"],
            ["1ª Pl", "hort**āmur**", "nosotros exhortamos"],
            ["2ª Pl", "hort**āmini**", "vosotros exhortáis"],
            ["3ª Pl", "hort**antur**", "ellos/ellas exhortan"]
        ]
    )

    st.markdown("""
    
    #### Segunda Conjugación: VEREOR, VERERI, VERITUS SUM (temer, respetar)
    
    """
    )

    render_styled_table(
        ["Persona", "Presente", "Imperfecto", "Futuro"],
        [
            ["1ª Sg", "vere**or**", "verē**bar**", "verē**bor**"],
            ["2ª Sg", "verē**ris**", "verē**bāris**", "verē**beris**"],
            ["3ª Sg", "verē**tur**", "verē**bātur**", "verē**bitur**"]
        ]
    )

    st.markdown("""
    
    #### Tercera Conjugación: SEQUOR, SEQUI, SECUTUS SUM (seguir)
    
    """
    )

    render_styled_table(
        ["Persona", "Presente", "Imperfecto", "Futuro"],
        [
            ["1ª Sg", "sequ**or**", "sequē**bar**", "sequ**ar**"],
            ["2ª Sg", "seque**ris**", "sequē**bāris**", "sequē**ris**"],
            ["3ª Sg", "sequi**tur**", "sequē**bātur**", "sequē**tur**"]
        ]
    )

    st.markdown("""
    
    #### Cuarta Conjugación: LARGIOR, LARGIRI, LARGITUS SUM (regalar, conceder)
    
    """
    )

    render_styled_table(
        ["Persona", "Presente", "Imperfecto", "Futuro"],
        [
            ["1ª Sg", "largi**or**", "largiē**bar**", "largi**ar**"],
            ["2ª Sg", "largī**ris**", "largiē**bāris**", "largiē**ris**"],
            ["3ª Sg", "largī**tur**", "largiē**bātur**", "largiē**tur**"]
        ]
    )

    st.markdown("""
    
    ### 3. Formación de Tiempos en Deponentes
    
    #### Sistema de Infectum (igual que pasiva regular):
    - **Presente**: Terminaciones pasivas
    - **Imperfecto**: -bar (pasivo)
    - **Futuro**: -bor (1ª/2ª conj) o -ar (3ª/4ª conj)
    
    #### Sistema de Perfectum (PPP + sum, como pasiva):
    - **Perfecto**: PPP + sum → *secutus sum* (he seguido)
    - **Pluscuamperfecto**: PPP + eram → *secutus eram* (había seguido)
    - **Futuro Perfecto**: PPP + ero → *secutus ero* (habré seguido)
    
    ### 4. Deponentes Frecuentes e Importantes
    
    #### 1ª Conjugación (-or, -ari, -atus sum):
    """
    )

    render_styled_table(
        ["Verbo", "Significado"],
        [
            ["*hortor, hortari, hortatus sum*", "exhortar, animar"],
            ["*moror, morari, moratus sum*", "demorar, tardar"],
            ["*opinor, opinari, opinatus sum*", "opinar, creer"]
        ]
    )

    st.markdown("""
    
    #### 2ª Conjugación (-eor, -eri, -itus sum):
    """
    )

    render_styled_table(
        ["Verbo", "Significado"],
        [
            ["*vereor, vereri, veritus sum*", "temer, respetar"],
            ["*confiteor, confiteri, confessus sum*", "confesar"],
            ["*misereor, misereri, miseritus sum*", "compadecerse"]
        ]
    )

    st.markdown("""
    
    #### 3ª Conjugación (-or, -i, -us sum):
    """
    )

    render_styled_table(
        ["Verbo", "Significado"],
        [
            ["***sequor, sequi, secutus sum***", "seguir"],
            ["***loquor, loqui, locutus sum***", "hablar"],
            ["***patior, pati, passus sum***", "sufrir, permitir"],
            ["***morior, mori, mortuus sum***", "morir"],
            ["***nascor, nasci, natus sum***", "nacer"],
            ["*utor, uti, usus sum*", "usar (+ ablativo)"],
            ["*fruor, frui, fructus sum*", "disfrutar (+ ablativo)"],
            ["*fungor, fungi, functus sum*", "desempeñar (+ ablativo)"],
            ["*potior, potiri, potitus sum*", "apoderarse (+ ablativo/genitivo)"]
        ]
    )

    st.markdown("""
    
    #### 4ª Conjugación (-ior, -iri, -itus sum):
    """
    )

    render_styled_table(
        ["Verbo", "Significado"],
        [
            ["*largior, largiri, largitus sum*", "regalar, conceder"],
            ["*partior, partiri, partitus sum*", "partir, dividir"]
        ]
    )

    st.markdown("""
    
    ### 5. Formas Nominales de los Deponentes
    
    Los deponentes tienen formas especiales que son **activas en significado** pero **pasivas en forma**:
    
    #### Participios:
    1. **Participio Presente**: Activo en forma y significado
       - *sequens, -entis* (que sigue, siguiendo)
       - *loquens, -entis* (que habla, hablando)
    
    2. **Participio Futuro**: Activo en significado
       - *secuturus, -a, -um* (que va a seguir)
    
    3. **Participio Perfecto Pasivo**: ¡ACTIVO en significado!
       - *secutus, -a, -um* (habiendo seguido) - NO "habiendo sido seguido"
       - *locutus, -a, -um* (habiendo hablado)
    
    #### Gerundio y Gerundivo:
    - **Gerundio**: *sequendi* (de seguir)
    - **Gerundivo**: *sequendus* (que debe ser seguido) - Pasivo en significado
    
    ### 6. Verbos Semideponentes
    
    Los **semideponentes** tienen forma activa en el Sistema de Infectum, pero **pasiva en el Perfectum**.
    
    """
    )

    render_styled_table(
        ["Verbo", "Infectum (Activo)", "Perfectum (Deponente)", "Significado"],
        [
            ["*audeo, audere*", "aude**o**, audē**s**, aude**t**", "**ausus sum**", "atreverse"],
            ["*gaudeo, gaudere*", "gaude**o**, audē**s**, gaude**t**", "**gavisus sum**", "alegrarse"],
            ["*soleo, solere*", "sole**o**, solē**s**, sole**t**", "**solitus sum**", "soler, acostumbrar"],
            ["*fido, fidere*", "fid**o**, fidī**s**, fidi**t**", "**físus sum**", "confiar"]
        ]
    )

    st.markdown("""
    
    **Ejemplo**:
    *   Presente: *Audeo dicere* (Me atrevo a decir)
    *   Perfecto: *Ausus sum dicere* (Me atreví a decir) - Forma pasiva, significado activo
    
    ### 7. Construcciones Especiales con Deponentes
    
    Algunos deponentes rigen **ablativo** (y NO acusativo):
    
    *   ***Utor* armis** (Uso las armas) - NO *uto armas*
    *   ***Fruor* vita** (Disfruto de la vida)
    *   ***Fungor* officio** (Desempeño el deber)
    *   ***Potior* urbe** (Me apodero de la ciudad)
    
    ### 8. Ejercicio de Traducción
    
    Traduce al español (fíjate en la forma pasiva pero significado activo):
    
    1. *Milites ducem **sequuntur**.* 
       → Los soldados **siguen** al jefe.
    
    2. *Cives de pace **loquebantur**.*
       → Los ciudadanos **hablaban** sobre la paz.
    
    3. *Multi in bello **passi sunt**.*
       → Muchos **sufrieron** en la guerra.
    
    4. *Philosophus sapienter **loquitur**.*
       → El filósofo **habla** sabiamente.
    
    5. *Populus libertate **utitur**.*
       → El pueblo **usa** la libertad.
    
    ### Vocabulario Esencial de Deponentes
    *   **sequor, sequi, secutus sum**: seguir
    *   **loquor, loqui, locutus sum**: hablar
    *   **patior, pati, passus sum**: sufrir
    *   **morior, mori, mortuus sum**: morir
    *   **nascor, nasci, natus sum**: nacer
    *   **utor, uti, usus sum** (+ abl): usar
    *   **audeo, audere, ausus sum**: atreverse
    *   **gaudeo, gaudere, gavisus sum**: alegrarse
    """)

def render_lesson_18():
    st.image("static/images/lesson_18_subjunctive.png", caption="El Orador: Expresando deseos y posibilidades con el Subjuntivo", use_container_width=True)

    st.markdown("""
    ## Lección 18: Modo Subjuntivo - Presente e Imperfecto
    
    ### Introducción al Subjuntivo
    
    El **Modo Subjuntivo** expresa acciones **no reales, posibles, deseadas o dependientes**.
    A diferencia del Indicativo (que expresa hechos), el Subjuntivo expresa:
    - **Posibilidad**: "Tal vez venga"
    - **Deseo**: "Ojalá vengas"
    - **Irrealidad**: "Si vinieras..."
    - **Dependencia**: "Quiero que vengas"
    
    """)

    st.image("static/images/lesson_18_vowels.png", caption="Cambios Vocálicos en el Subjuntivo", use_container_width=True)

    st.markdown("""
    ### 1. Formación del Subjuntivo Presente

    **Regla general**: Cambiar la vocal temática
    
    #### 1ª Conjugación: A → E
    - Indicativo: am**a**-o, am**a**-s
    - Subjuntivo: am**e**-m, am**e**-s
    
    """
    )

    render_styled_table(
        ["Persona", "Indicativo", "Subjuntivo", "Traducción"],
        [
            ["1ª Sg", "am**o**", "am**em**", "(que) yo ame"],
            ["2ª Sg", "am**as**", "am**es**", "(que) tú ames"],
            ["3ª Sg", "am**at**", "am**et**", "(que) él/ella ame"],
            ["1ª Pl", "am**amus**", "am**emus**", "(que) nosotros amemos"],
            ["2ª Pl", "am**atis**", "am**etis**", "(que) vosotros améis"],
            ["3ª Pl", "am**ant**", "am**ent**", "(que) ellos/ellas amen"]
        ]
    )

    st.markdown("""
    
    #### 2ª Conjugación: E → EA
    - Indicativo: mon**e**-o, mon**e**-s
    - Subjuntivo: mon**ea**-m, mon**ea**-s
    
    """
    )

    render_styled_table(
        ["Persona", "Indicativo", "Subjuntivo"],
        [
            ["1ª Sg", "mone**o**", "mone**am**"],
            ["2ª Sg", "mone**s**", "mone**as**"],
            ["3ª Sg", "mone**t**", "mone**at**"]
        ]
    )

    st.markdown("""
    
    #### 3ª Conjugación: Consonante/E → A
    - Indicativo: leg-**o**, leg-i**s**
    - Subjuntivo: leg-**a**-m, leg-**a**-s
    
    """
    )

    render_styled_table(
        ["Persona", "Indicativo", "Subjuntivo"],
        [
            ["1ª Sg", "leg**o**", "leg**am**"],
            ["2ª Sg", "leg**is**", "leg**as**"],
            ["3ª Sg", "leg**it**", "leg**at**"]
        ]
    )

    st.markdown("""
    
    #### 4ª Conjugación: I → IA
    - Indicativo: aud**i**-o, aud**i**-s
    - Subjuntivo: aud**ia**-m, aud**ia**-s
    
    """
    )

    render_styled_table(
        ["Persona", "Indicativo", "Subjuntivo"],
        [
            ["1ª Sg", "audi**o**", "audi**am**"],
            ["2ª Sg", "audi**s**", "audi**as**"],
            ["3ª Sg", "audi**t**", "audi**at**"]
        ]
    )

    st.markdown("""
    
    ### 2. Sub juntivo de SUM
    
    **SUM** (ser/estar) tiene subjuntivo irregular:
    
    """
    )

    render_styled_table(
        ["Persona", "Indicativo", "Subjuntivo Presente"],
        [
            ["1ª Sg", "sum", "**sim**"],
            ["2ª Sg", "es", "**sis**"],
            ["3ª Sg", "est", "**sit**"],
            ["1ª Pl", "sumus", "**simus**"],
            ["2ª Pl", "estis", "**sitis**"],
            ["3ª Pl", "sunt", "**sint**"]
        ]
    )

    st.markdown("""
    
    ### 3. Formación del Subjuntivo Imperfecto
    
    **Regla universal**: Infinitivo presente + terminaciones personales activas (-m, -s, -t, -mus, -tis, -nt)
    
    #### Las Cuatro Conjugaciones:
    
    """
    )

    render_styled_table(
        ["Conjugación", "Infinitivo", "1ª Sg", "2ª Sg", "3ª Sg"],
        [
            ["**1ª**", "am**āre**", "amāre**m**", "amāre**s**", "amāre**t**"],
            ["**2ª**", "mon**ēre**", "monēre**m**", "monēre**s**", "monēre**t**"],
            ["**3ª**", "leg**ĕre**", "legĕre**m**", "legĕre**s**", "legĕre**t**"],
            ["**4ª**", "aud**īre**", "audīre**m**", "audīre**s**", "audīre**t**"]
        ]
    )

    st.markdown("""
    
    **Paradigma completo de AMARE**:
    
    """
    )

    render_styled_table(
        ["Persona", "Subjuntivo Imperfecto", "Traducción"],
        [
            ["1ª Sg", "amāre**m**", "(si) yo amara/amase"],
            ["2ª Sg", "amāre**s**", "(si) tú amaras"],
            ["3ª Sg", "amāre**t**", "(si) él amara"],
            ["1ª Pl", "amārē**mus**", "(si) nosotros amáramos"],
            ["2ª Pl", "amārē**tis**", "(si) vosotros amarais"],
            ["3ª Pl", "amāre**nt**", "(si) ellos amaran"]
        ]
    )

    st.markdown("""
    
    ### 4. Subjuntivo Imperfecto de SUM
    
    Infinitivo *esse* + terminaciones:
    
    """
    )

    render_styled_table(
        ["Persona", "Forma", "Traducción"],
        [
            ["1ª Sg", "**essem**", "(si) yo fuera/fuese"],
            ["2ª Sg", "**esses**", "(si) tú fueras"],
            ["3ª Sg", "**esset**", "(si) él fuera"],
            ["1ª Pl", "**essemus**", "(si) nosotros fuéramos"],
            ["2ª Pl", "**essetis**", "(si) vosotros fuerais"],
            ["3ª Pl", "**essent**", "(si) ellos fueran"]
        ]
    )

    st.markdown("""
    
    ### 5. Usos del Subjuntivo Independiente
    
    El subjuntivo puede aparecer en **oraciones principales** (no subordinadas) con varios usos:
    
    #### A. Subjuntivo Optativo (Deseo)
    Expresa un deseo. Normalmente con ***utinam*** (ojalá).
    
    *   ***Utinam venias!*** (¡Ojalá vengas!)
    *   ***Utinam ne hoc faceret!*** (¡Ojalá no hiciera esto!)
    *   ***Di te servent!*** (¡Que los dioses te guarden!)
    
    **Negación**: *ne*
    
    #### B. Subjuntivo Yusivo / Exhortativo
    Expresa una **orden o exhortación** en 1ª o 3ª persona.
    
    *   ***Gaudeamus igitur!*** (¡Alegrémonos, pues!)
    *   ***Veniat!*** (¡Que venga!)
    *   ***Ne timeas!*** (¡No temas!)
    
    **Negación**: *ne*
    
    #### C. Subjuntivo Dubitativo (Deliberativo)
    Expresa **duda** en forma interrogativa.
    
    *   ***Quid faciam?*** (¿Qué debo hacer? / ¿Qué haga?)
    *   ***Quo eam?*** (¿A dónde voy? / ¿A dónde vaya?)
    
    """)

    st.image("static/images/lesson_18_potential.png", caption="El Subjuntivo Potencial: Imaginando posibilidades", use_container_width=True)

    st.markdown("""
    #### D. Subjuntivo Potencial
    Expresa **posibilidad** (normalmente con Presente de Subjuntivo).
    
    *   ***Hoc dicas.*** (Podrías decir esto / Dirías esto)
    *   ***Credas te in caelo esse.*** (Creerías que estás en el cielo)
    
    ### 6. Tabla Comparativa de Usos
    
    """
    )

    render_styled_table(
        ["Uso", "Tiempo", "Ejemplo", "Traducción"],
        [
            ["**Optativo**", "Presente", "*Utinam veniat*", "Ojalá venga"],
            ["**Optativo**", "Imperfecto", "*Utinam venīret*", "Ojalá viniera"],
            ["**Yusivo**", "Presente", "*Veniat!*", "¡Que venga!"],
            ["**Exhortativo**", "Presente", "*Eamus!*", "¡Vayamos!"],
            ["**Dubitativo**", "Presente/Imp", "*Quid faciam?*", "¿Qué debo hacer?"],
            ["**Potencial**", "Presente", "*Dicas*", "Podrías decir"]
        ]
    )

    st.markdown("""
    
    ### 7. Ejercicios de Conjugación
    
    Conjuga en Subjuntivo Presente y luego en Imperfecto:
    
    """
    )

    render_styled_table(
        ["Verbo", "Presente (3ª Sg)", "Imperfecto (3ª Sg)"],
        [
            ["*amo*", "am**et**", "amāre**t**"],
            ["*moneo*", "mone**at**", "monēre**t**"],
            ["*lego*", "leg**at**", "legĕre**t**"],
            ["*audio*", "audi**at**", "audīre**t**"],
            ["*sum*", "**sit**", "**esset**"]
        ]
    )

    st.markdown("""
    
    ### 8. Traducción de Expresiones
    
    1. *Utinam viveres!*
       → ¡Ojalá vivieras!
    
    2. *Gaudeamus omnes!*
       → ¡Alegrémonos todos!
    
    3. *Veniat Caesar.*
       → Que venga César.
    
    4. *Quid agam?*
       → ¿Qué debo hacer?
    
    5. *Ne timeas.*
       → No temas.
    
    ### Vocabulario Esencial
    *   **utinam**: ojalá
    *   **ne**: no (en subjuntivo)
    *   **quid**: qué
    *   **quo**: a dónde
    *   **cur**: por qué
    *   **ut**: que (afirmativo)
    """)

def render_lesson_19():
    st.markdown("""
    ## Lección 19: Subjuntivo Perfecto/Pluscuamperfecto y Consecutio Temporum
    
    ### Completando el Sistema de Subjuntivo
    
    Ya conoces el Subjuntivo Presente e Imperfecto. Ahora aprenderemos los **dos tiempos del Perfectum**
    y la regla fundamental que gobierna su uso: la **consecutio temporum** (concordancia de tiempos).
    
    ### 1. Subjuntivo Perfecto
    
    **Formación**: Tema de perfecto + **-eri-** + terminaciones activas
    
    #### Paradigma: AMARE (Tema perfecto: amav-)
    
    """
    )

    render_styled_table(
        ["Persona", "Subjuntivo Perfecto", "Traducción"],
        [
            ["1ª Sg", "amav**erim**", "(que) yo haya amado"],
            ["2ª Sg", "amav**eris**", "(que) tú hayas amado"],
            ["3ª Sg", "amav**erit**", "(que) él haya amado"],
            ["1ª Pl", "amav**erimus**", "(que) nosotros hayamos amado"],
            ["2ª Pl", "amav**eritis**", "(que) vosotros hayáis amado"],
            ["3ª Pl", "amav**erint**", "(que) ellos hayan amado"]
        ]
    )

    st.markdown("""
    
    > **Nota**: Es casi idéntico al Futuro Perfecto Indicativo, excepto en 1ª Sg: 
    > - Fut. Perfecto: amav**ero**
    > - Subj. Perfecto: amav**erim**
    
    #### Otras Conjugaciones (3ª persona singular):
    
    """
    )

    render_styled_table(
        ["Verbo", "Perfecto Ind", "Subj. Perfecto"],
        [
            ["*moneo*", "monu**it**", "monu**erit**"],
            ["*lego*", "lēg**it**", "lēg**erit**"],
            ["*audio*", "audīv**it**", "audīv**erit**"],
            ["*sum*", "fu**it**", "fu**erit**"]
        ]
    )

    st.markdown("""
    
    ### 2. Subjuntivo Pluscuamperfecto
    
    **Formación**: Infinitivo Perfecto Activo + terminaciones activas
    
    **Infinitivo Perfecto**: amav**isse**, monu**isse**, lēg**isse**, audīv**isse**
    
    #### Paradigma: AMARE
    
    """
    )

    render_styled_table(
        ["Persona", "Subjuntivo Pluscuamperfecto", "Traducción"],
        [
            ["1ª Sg", "amavisse**m**", "(si) yo hubiera/hubiese amado"],
            ["2ª Sg", "amavisse**s**", "(si) tú hubieras amado"],
            ["3ª Sg", "amavisse**t**", "(si) él hubiera amado"],
            ["1ª Pl", "amavisē**mus**", "(si) nosotros hubiéramos amado"],
            ["2ª Pl", "amavisē**tis**", "(si) vosotros hubierais amado"],
            ["3ª Pl", "amavisse**nt**", "(si) ellos hubieran amado"]
        ]
    )

    st.markdown("""
    
    #### Otras Conjugaciones (3ª Sg):
    
    """
    )

    render_styled_table(
        ["Verbo", "Inf. Perfecto", "Subj. Pluscuamperfecto"],
        [
            ["*moneo*", "monu**isse**", "monuisse**t**"],
            ["*lego*", "lēg**isse**", "lēgisse**t**"],
            ["*sum*", "fu**isse**", "fuisse**t**"]
        ]
    )

    st.markdown("""
    
    ### 3. Resumen: Los Cuatro Tiempos del Subjuntivo
    
    """
    )

    render_styled_table(
        ["Tiempo", "Formación", "Ejemplo (1ª Sg)", "Traducción"],
        [
            ["**Presente**", "Vocal temática cambiada", "am**em**", "(que) yo ame"],
            ["**Imperfecto**", "Infinitivo presente + -m", "amāre**m**", "(si) yo amara"],
            ["**Perfecto**", "Tema perfecto + -erim", "amav**erim**", "(que) yo haya amado"],
            ["**Pluscuamperfecto**", "Inf. perfecto + -m", "amavisse**m**", "(si) yo hubiera amado"]
        ]
    )

    st.markdown("""
    
    """)

    st.image("static/images/lesson_19_timeline.png", caption="Línea Temporal: La relación entre tiempos verbales", use_container_width=True)

    st.markdown("""
    ### 4. Consecutio Temporum (Concordancia de Tiempos)

    Esta es **LA REGLA MÁS IMPORTANTE** del subjuntivo en oraciones subordinadas.
    
    **Principio**: El tiempo del subjuntivo en la subordinada depende de:
    1. El tiempo del verbo principal
    2. La relación temporal (simultaneidad, anterioridad, posterioridad)
    
    #### Regla Simplificada:
    
    **A. Oración Principal en Tiempo Primario** (Presente, Fut., Fut. Perf., Imperativo):
    - **Simultaneidad/Posterioridad**: Subjuntivo **Presente**
    - **Anterioridad**: Subjuntivo **Perfecto**
    
    **B. Oración Principal en Tiempo Histórico** (Imperfecto, Perfecto, Pluscuamperfecto):
    - **Simultaneidad/Posterioridad**: Subjuntivo **Imperfecto**
    - **Anterioridad**: Subjuntivo **Pluscuamperfecto**
    
    #### Tabla Completa de Consecutio Temporum:
    
    """
    )

    render_styled_table(
        ["Principal", "Relación", "Subordinada", "Ejemplo"],
        [
            ["**Presente**", "Simult.", "Pres. Subj.", "*Timeo **ut veniat*** (Temo que venga)"],
            ["**Presente**", "Ant.", "Perf. Subj.", "*Timeo **ut venerit*** (Temo que haya venido)"],
            ["**Imperfecto**", "Simult.", "Imp. Subj.", "*Timebam **ut venīret*** (Temía que viniera)"],
            ["**Imperfecto**", "Ant.", "Plusc. Subj.", "*Timebam **ut venisset*** (Temía que hubiera venido)"]
        ]
    )

    st.markdown("""
    
    ### 5. Ejemplos Detallados de Consecutio Temporum
    
    #### Ejemplo 1: Subordinada Completiva con UT
    
    **Principal Primaria**:
    *   *Rogo **ut venias**.* (Te pido que vengas) - Simultaneidad → Pres. Subj.
    *   *Rogo **ut veneris**.* (Te pido que hayas venido) - Anterioridad → Perf. Subj.
    
    **Principal Histórica**:
    *   *Rogavi **ut venīres**.* (Te pedí que vinieras) - Simultaneidad → Imp. Subj.
    *   *Rogavi **ut venisses**.* (Te pedí que hubieras venido) - Anterioridad → Plusc. Subj.
    
    #### Ejemplo 2: Subordinada Final
    
    **Principal Primaria**:
    *   *Venio **ut te videam**.* (Vengo para verte) - Presente Subj.
    
    **Principal Histórica**:
    *   *Veni **ut te viderem**.* (Vine para verte) - Imperfecto Subj.
    
    #### Ejemplo 3: Subordinada Consecutiva
    
    **Principal Primaria**:
    *   *Tam fortis est **ut vincere possit**.* (Es tan fuerte que puede vencer) - Pres. Subj.
    
    **Principal Histórica**:
    *   *Tam fortis erat **ut vincere posset**.* (Era tan fuerte que podía vencer) - Imp. Subj.
    
    ### 6. Excepciones y Casos Especiales
    
    #### A. Perfecto con valor de Presente
    Cuando el Perfecto tiene valor de presente (perfecto resultativo), usa tiempos primarios:
    
    *   *Audivi **quid dicas**.* (He oído lo que dices) - Pres. Subj.
    
    #### B. Imperfecto/Pluscuamperfecto de Indicativo
    Siempre usan tiempos históricos del subjuntivo:
    
    *   *Nesciebam **quid faceret**.* (No sabía qué hacía)
    
    #### C. Condicionales Irreales
    En condicionales irreales, se rompe la consecutio normal:
    
    *   *Si hoc **faceres**, felix **esses**.* (Si hicieras esto, serías feliz)
       - Ambas: Imperfecto Subjuntivo (irrealidad presente)
    
    """)

    st.image("static/images/lesson_19_structure.png", caption="Estructura de la Consecutio Temporum", use_container_width=True)

    st.markdown("""
    """)

    st.info("📊 **Pendiente**: Esta sección debe incluir un infograma visual interactivo que muestre la **Tabla Maestra de Consecutio Temporum** con los tiempos primarios e históricos y sus relaciones de concordancia temporal.")

    st.markdown("""
    ### 8. Ejercicios de Aplicación
    
    Completa con el tiempo correcto del subjuntivo:
    
    1. *Rogo ut ______ (venire).*
       → **venias** (Principal presente → Pres. Subj.)
    
    2. *Rogavi ut ______ (venire).*
       → **venīres** (Principal perfecto → Imp. Subj.)
    
    3. *Timeo ne hoc ______ (facere) iam.*
       → **fecerit** (Anterioridad + Principal pres. → Perf. Subj.)
    
    4. *Si hoc ______ (facere), felix ______ (esse).*
       → **faceres**, **esses** (Condicional irreal presente)
    
    5. *Tam sapienter loquitur ut omnes eum ______ (audire).*
       → **audiant** (Consecutiva + Principal pres. → Pres. Subj.)
    
    ### 9. Resumen Final: Dominio del Subjuntivo
    
    ¡Felicidades! Ahora dominas:
    
    ✓ **4 tiempos** del Subjuntivo (Pres, Imp, Perf, Plusc)
    ✓ **Usos independientes** (Optativo, Yusivo, Dubitativo, Potencial)
    ✓ **Consecutio Temporum** (la regla de oro de las subordinadas)
    ✓ **Verbos irregulares** en subjuntivo (sum, possum)
    
    Estás listo para enfrentar cualquier texto latino con subjuntivo.
    
    ### Vocabulario Esencial
    *   **ut**: que, para que (+ subjuntivo)
    *   **ne**: que no, para que no
    *   **cum**: cuando, como quiera que
    *   **si**: si
    *   **nisi**: si no, a menos que
    *   **quamquam**: aunque (+ indicativo)
    *   **quamvis**: aunque (+ subjuntivo)
    """)

def render_lesson_20():
    st.markdown("""
    ## Lección 20: Infinitivos y Oraciones de Infinitivo (AcI)
    
    ### 1. El Infinitivo: Sustantivo Verbal
    
    El **infinitivo** es una forma nominal del verbo. Funciona como un sustantivo neutro.
    En español tenemos formas simples (amar, haber amado). En latín, el sistema es más rico y preciso.
    
    ### 2. Morfología de los Infinitivos
    """)

    if os.path.exists("static/images/curso_gramatica/leccion20_infinitivos.png"):
        st.image("static/images/curso_gramatica/leccion20_infinitivos.png",
                 caption="Tabla de Infinitivos Latinos",
                 use_container_width=True)

    st.markdown("""
    El latín tiene infinitivos para **tres tiempos** (Presente, Perfecto, Futuro) y **dos voces** (Activa, Pasiva).
    
    #### A. Infinitivo Presente (Simultaneidad)
    """)
    
    render_styled_table(
        ["Conjugación", "Activa", "Pasiva", "Traducción (Act/Pas)"],
        [
            ["**1ª (amare)**", "amā**re**", "amā**ri**", "amar / ser amado"],
            ["**2ª (monere)**", "monē**re**", "monē**ri**", "aconsejar / ser aconsejado"],
            ["**3ª (legere)**", "leg**ĕre**", "leg**i**", "leer / ser leído"],
            ["**4ª (audire)**", "audī**re**", "audī**ri**", "oír / ser oído"],
            ["**Mixta (capere)**", "cap**ĕre**", "cap**i**", "tomar / ser tomado"]
        ]
    )

    st.markdown("""
    
    > **¡Ojo a la 3ª conjugación pasiva!** Termina en **-i** (no -eri). *Legi*, *duci*, *mitti*.
    
    #### B. Infinitivo Perfecto (Anterioridad)
    """)
    
    render_styled_table(
        ["Voz", "Formación", "Ejemplo", "Traducción"],
        [
            ["**Activa**", "Tema Perf. + **-isse**", "*amavisse*", "haber amado"],
            ["**Pasiva**", "PPP (Acusativo) + **esse**", "*amatum, -am, -um esse*", "haber sido amado"]
        ]
    )

    st.markdown("""
    
    #### C. Infinitivo Futuro (Posterioridad)
    """)
    
    render_styled_table(
        ["Voz", "Formación", "Ejemplo", "Traducción"],
        [
            ["**Activa**", "PFA (Acusativo) + **esse**", "*amaturum, -am, -um esse*", "haber de amar / que amará"],
            ["**Pasiva**", "Supino + **iri**", "*amatum iri*", "(raro) que será amado"]
        ]
    )

    st.markdown("""
    
    ### 3. La Construcción de Acusativo con Infinitivo (AcI)
    
    Esta es una de las estructuras más características del latín. Se usa tras verbos de **lengua, entendimiento y sentido** (*verba dicendi, sentiendi et affectuum*).
    
    En español usamos una subordinada con "que" + verbo personal:
    *   "Dico **que tú vienes**."
    
    En latín, el sujeto de la subordinada va en **ACUSATIVO** y el verbo en **INFINITIVO**:
    *   *Dico **te venire**.* (Literalmente: "Digo te venir")
    
    #### Reglas de la AcI:
    1.  El **Sujeto** de la subordinada se pone en **Acusativo**.
    2.  El **Verbo** de la subordinada se pone en **Infinitivo**.
    3.  Si hay **Atributo** o predicativo, también va en **Acusativo** (concordando con el sujeto).
    
    #### Ejemplos:
    """)
    
    render_styled_table(
        ["Latín (AcI)", "Traducción Literal", "Traducción Correcta"],
        [
            ["*Video **puerum currere**.*", "Veo al niño correr", "Veo **que el niño corre**."],
            ["*Scio **terram rotundam esse**.*", "Sé la tierra redonda ser", "Sé **que la tierra es redonda**."],
            ["*Credo **Deum bonum esse**.*", "Creo a Dios bueno ser", "Creo **que Dios es bueno**."],
            ["*Dicit **se Romanum esse**.*", "Dice se romano ser", "Dice **que él (mismo) es romano**."]
        ]
    )

    st.markdown("""
    
    > **Nota sobre el reflexivo 'se'**: Si el sujeto de la subordinada es el mismo que el de la principal, se usa el acusativo **se**.
    > *   *Caesar dicit **se** vincere.* (César dice que él [César] vence)
    > *   *Caesar dicit **eum** vincere.* (César dice que él [otro] vence)
    
    ### 4. Concordancia de Tiempos en AcI
    
    El tiempo del infinitivo es **relativo** al verbo principal:
    
    *   **Inf. Presente** = Acción simultánea (al mismo tiempo que el verbo principal).
    *   **Inf. Perfecto** = Acción anterior (antes del verbo principal).
    *   **Inf. Futuro** = Acción posterior (después del verbo principal).
    
    #### Tabla de Relatividad Temporal:
    """)
    
    render_styled_table(
        ["Verbo Principal", "Infinitivo", "Traducción", "Relación"],
        [
            ["*Dico* (Digo)", "*te **venire***", "...que vienes", "Simultaneidad (Presente)"],
            ["*Dico* (Digo)", "*te **venisse***", "...que viniste / has venido", "Anterioridad (Pasado)"],
            ["*Dico* (Digo)", "*te **venturum esse***", "...que vendrás", "Posterioridad (Futuro)"],
            ["", "", "", ""],
            ["*Dixi* (Dije)", "*te **venire***", "...que venías", "Simultaneidad (Pasado)"],
            ["*Dixi* (Dije)", "*te **venisse***", "...que habías venido", "Anterioridad (Pluscuamperfecto)"],
            ["*Dixi* (Dije)", "*te **venturum esse***", "...que vendrías", "Posterioridad (Condicional)"]
        ]
    )

    st.markdown("""
    
    ### 5. Ejercicios de Análisis
    
    Analiza y traduce:
    
    1.  *Thales dixit aquam initium omnium rerum esse.*
        *   **Thales dixit**: Tales dijo (Verbo principal)
        *   **aquam** (Ac, Suj): que el agua
        *   **initium** (Ac, Atrib): el principio
        *   **omnium rerum** (Gen Pl): de todas las cosas
        *   **esse** (Inf Pres): era (simultaneidad con 'dijo')
        *   → **Tales dijo que el agua era el principio de todas las cosas.**
    
    2.  *Sentio vos laetos esse.*
        *   → Siento que vosotros estáis contentos.
    
    3.  *Credimus Romam aeternam fore (= futuram esse).*
        *   → Creemos que Roma será eterna.
    
    ### Vocabulario Esencial
    *   **Dico, dicere, dixi, dictum**: decir
    *   **Scio, scire, scivi, scitum**: saber
    *   **Credo, credere, credidi, creditum**: creer
    *   **Puto, putare**: pensar
    *   **Video, videre, vidi, visum**: ver
    *   **Audio, audire**: oír
    *   **Sentio, sentire**: sentir, darse cuenta
    *   **Spero, sperare**: esperar (que algo suceda)
    *   **Nego, negare**: negar (decir que no)
    """)

def render_lesson_21():
    st.markdown("""
    ## Lección 21: Los Participios
    
    ### 1. ¿Qué es un Participio?
    
    El participio es un **adjetivo verbal**.
    *   Como **adjetivo**: concuerda en Género, Número y Caso con un sustantivo.
    *   Como **verbo**: tiene Tiempo y Voz, y puede regir complementos (OD, etc.).
    
    ### 2. El Sistema de Participios Latino
    """)

    if os.path.exists("static/images/curso_gramatica/leccion21_participios.png"):
        st.image("static/images/curso_gramatica/leccion21_participios.png",
                 caption="Sistema de Participios",
                 use_container_width=True)

    st.markdown("""
    A diferencia del español (que solo tiene "amado" y "amante"), el latín tiene un sistema más completo:
    
    """
    )

    render_styled_table(
        ["Tiempo", "Voz Activa", "Voz Pasiva"],
        [
            ["**Presente**", "**Amans, amantis** (que ama / amante)", "*(No existe)*"],
            ["**Pasado**", "*(No existe)*", "**Amatus, -a, -um** (amado / habiendo sido amado)"],
            ["**Futuro**", "**Amaturus, -a, -um** (que amará / que va a amar)", "*Amandus, -a, -um* (Gerundivo - ver Lección 23)"]
        ]
    )

    st.markdown("""
    
    ### 3. Visualización Temporal
    
    El tiempo del participio es **relativo** al verbo principal de la oración.
    """)
    
    # Diagrama Mermaid para explicar la relatividad temporal
    render_mermaid(r"""
    timeline
        title Relatividad Temporal de los Participios
        section Verbo Principal
            Acción Principal : El momento de referencia
        section Participios
            Anterioridad : Participio PERFECTO (Pasivo)
            Simultaneidad : Participio PRESENTE (Activo)
            Posterioridad : Participio FUTURO (Activo)
    """)
    
    st.markdown("""
    ### 4. Formación y Declinación
    
    #### A. Participio de Presente Activo
    **Formación**: Tema de presente + **-ns** (Nom), **-ntis** (Gen).
    **Declinación**: Como un adjetivo de la 3ª declinación (tema en -i).
    
    *   *Amare* -> **Amans, amantis**
    *   *Monere* -> **Monens, monentis**
    *   *Legere* -> **Legens, legentis**
    *   *Audire* -> **Audiens, audientis**
    
    > **Traducción**: "el que ama", "amando", "al amar", "mientras ama".
    
    #### B. Participio de Perfecto Pasivo (PPP)
    **Formación**: Es la 4ª forma del enunciado del verbo (Supino) declinada como *bonus, -a, -um*.
    
    *   *Amo, amare, amavi, **amatum*** -> **Amatus, -a, -um**
    *   *Video, videre, vidi, **visum*** -> **Visus, -a, -um**
    *   *Capio, capere, cepi, **captum*** -> **Captus, -a, -um**
    
    > **Traducción**: "amado", "habiendo sido amado", "una vez amado".
    
    #### C. Participio de Futuro Activo (PFA)
    **Formación**: Tema de supino + **-urus, -ura, -urum**.
    
    *   *Amatum* -> **Amaturus, -a, -um**
    *   *Visum* -> **Visurus, -a, -um**
    
    > **Traducción**: "que va a amar", "dispuesto a amar", "a punto de amar".
    
    ### 5. Uso Sintáctico: El Participio Concertado
    
    El participio concuerda con un sustantivo de la oración (Sujeto, OD, etc.).
    
    #### Ejemplos:
    
    **1. Participio Presente (Simultaneidad)**
    *   *Puer **currens** cadit.*
        *   El niño, **corriendo**, cae. / El niño, **que corre**, cae.
    *   *Vocem **cantantis** audio.*
        *   Oigo la voz **del que canta**.
    
    **2. Participio Perfecto (Anterioridad)**
    *   *Urbs, ab hostibus **capta**, incensa est.*
        *   La ciudad, **capturada** por los enemigos, fue incendiada.
        *   (= La ciudad, **después de ser capturada**...)
    
    **3. Participio Futuro (Posterioridad / Intención)**
    *   *Ave, Caesar, **morituri** te salutant.*
        *   Ave, César, **los que van a morir** te saludan.
    
    ### 6. Ejercicio de Análisis
    
    Analiza los participios en estas frases:
    
    1.  *Video canem **dormientem**.*
        *   *Dormientem*: Part. Pres. Activo, Acusativo Singular. Concuerda con *canem*.
        *   → Veo al perro **durmiendo** (o "que duerme").
    
    2.  *Milites, a duce **laudati**, gaudebant.*
        *   *Laudati*: Part. Perf. Pasivo, Nom. Plural. Concuerda con *milites*.
        *   → Los soldados, **alabados** por el líder, se alegraban.
    
    3.  *Scripturus sum.*
        *   *Scripturus*: Part. Fut. Activo + sum (Perifrástica activa).
        *   → **Voy a escribir** / Tengo intención de escribir.
    
    ### Vocabulario Esencial
    *   **Curro, currere**: correr
    *   **Cado, cadere**: caer
    *   **Capio, capere, cepi, captum**: capturar, tomar
    *   **Incendo, incendere, incendi, incensum**: incendiar
    *   **Morior, mori, mortuus sum**: morir
    """)

def render_lesson_22():
    st.markdown("""
    ## Lección 22: El Ablativo Absoluto
    
    ### 1. La Construcción Reina del Latín
    
    El **Ablativo Absoluto** es una construcción sintáctica fundamental y muy frecuente en latín.
    Equivale a una **oración subordinada circunstancial** (temporal, causal, concesiva, etc.).
    
    Se llama "absoluto" (*absolutus* = desatado, suelto) porque gramaticalmente está **desligado** de la oración principal:
    *   Su sujeto no es el sujeto de la principal.
    *   Su sujeto no es el objeto de la principal.
    
    ### 2. Estructura
    
    Se compone de dos elementos básicos en caso **ABLATIVO**:
    
    1.  **Sujeto** (Sustantivo o Pronombre)
    2.  **Predicado** (Participio, Adjetivo o Sustantivo)
    
    """)
    
    if os.path.exists("static/images/curso_gramatica/leccion22_ablativo_absoluto.png"):
        st.image("static/images/curso_gramatica/leccion22_ablativo_absoluto.png",
                 caption="Estructura y Tipos de Ablativo Absoluto",
                 use_container_width=True)
    else:
        render_mermaid(r"""
    timeline
        title Relatividad Temporal de los Participios
        section Verbo Principal
            Acción Principal : El momento de referencia
        section Participios
            Anterioridad : Participio PERFECTO (Pasivo)
            Simultaneidad : Participio PRESENTE (Activo)
            Posterioridad : Participio FUTURO (Activo)
    """)
    
    st.markdown("""
    ### 3. Tipos de Ablativo Absoluto
    
    #### A. Con Participio de Presente (Simultaneidad)
    *   **Estructura**: Sustantivo (Abl) + Part. Presente (Abl)
    *   **Traducción**: "Haciendo...", "Mientras hace...", "Al hacer..."
    
    *   *Sole **oriente**, fugiunt tenebrae.*
        *   *Sole* (Sol, Abl) + *oriente* (saliendo, Abl)
        *   → **Saliendo el sol**, huyen las tinieblas.
        *   → **Al salir el sol**, huyen las tinieblas.
        *   → **Mientras sale el sol**, huyen las tinieblas.
    
    #### B. Con Participio de Perfecto (Anterioridad)
    *   **Estructura**: Sustantivo (Abl) + Part. Perfecto (Abl)
    *   **Traducción**: "Hecho...", "Una vez hecho...", "Después de hacer..."
    
    *   *Urbe **capta**, hostes redierunt.*
        *   *Urbe* (Ciudad, Abl) + *capta* (capturada, Abl)
        *   → **Capturada la ciudad**, los enemigos regresaron.
        *   → **Una vez capturada la ciudad**, los enemigos regresaron.
        *   → **Después de capturar la ciudad**, los enemigos regresaron.
    
    #### C. Tipo Nominal (Sin Participio)
    Como el verbo *sum* no tiene participio de presente, a veces se omite.
    Se entiende "siendo..." o "estando...".
    
    *   *Cicerone **consule**...*
        *   *Cicerone* (Cicerón, Abl) + *consule* (cónsul, Abl)
        *   → **Siendo cónsul Cicerón**... / **Bajo el consulado de Cicerón**...
    
    *   *Hannibale **duce**...*
        *   → **Siendo líder Aníbal**... / **Bajo el mando de Aníbal**...
    
    *   *Me **invito**...*
        *   → **Estando yo reacio**... / **Contra mi voluntad**...
    
    ### 4. Cómo Traducir el Ablativo Absoluto
    
    No te limites a traducir literalmente. Busca la traducción más natural en español:
    
    1.  **Literal**: *Urbe capta* → Capturada la ciudad.
    2.  **Temporal**: *Urbe capta* → Cuando la ciudad fue capturada.
    3.  **Causal**: *Urbe capta* → Porque la ciudad fue capturada.
    4.  **Concesiva**: *Urbe capta* → Aunque la ciudad fue capturada.
    
    ### 5. Ejercicios de Análisis
    
    Analiza y traduce:
    
    1.  *Pythagoras, **Tarquinio Superbo regnante**, in Italiam venit.*
        *   *Tarquinio Superbo* (Abl) + *regnante* (Part. Pres. Abl)
        *   → Pitágoras llegó a Italia **reinando Tarquinio el Soberbio** (durante el reinado de...).
    
    2.  *His rebus **auditis**, omnes timuerunt.*
        *   *His rebus* (Estas cosas, Abl Pl) + *auditis* (oídas, Part. Perf. Abl Pl)
        *   → **Oídas estas cosas** (Al oír esto), todos temieron.
    
    3.  *Romani, **Hannibale vivo**, numquam securi erant.*
        *   *Hannibale* (Abl) + *vivo* (Adj. Abl) [Tipo Nominal]
        *   → Los romanos, **estando vivo Aníbal** (mientras Aníbal vivía), nunca estaban seguros.

    4.  ***Nullo hoste prohibente**, legionem duxit.*
        *   *Nullo hoste* (Ningún enemigo) + *prohibente* (impidiéndolo)
        *   → **Sin que ningún enemigo lo impidiera**, condujo la legión. (Matiz circunstancial/concesivo)

    5.  ***Caesare duce**, nihil timebimus.*
        *   *Caesare* (César) + *duce* (líder) [Tipo Nominal]
        *   → **Siendo César nuestro líder** (Bajo el mando de César), nada temeremos. (Matiz Causal/Condicional)
    
    ### Vocabulario Esencial
    *   **Oriens, -entis**: naciente, que sale (Sol)
    *   **Occidens, -entis**: poniente, que se pone
    *   **Regno, regnare**: reinar
    *   **Audio, audire, audivi, auditum**: oír
    *   **Securus, -a, -um**: seguro, sin preocupaciones
    *   **Vivus, -a, -um**: vivo
    *   **Prohibeo, prohibere**: impedir, prohibir
    *   **Dux, ducis**: líder, general
    """)

def render_lesson_23():
    st.markdown("""
    ## Lección 23: Gerundio y Gerundivo
    
    ### 1. Dos Caras de la Misma Moneda
    
    El latín tiene dos formas verbales que a menudo se confunden pero tienen funciones distintas:
    
    1.  **Gerundio**: Es un **Sustantivo Verbal** Activo. (Equivale a "el acto de amar").
    2.  **Gerundivo**: Es un **Adjetivo Verbal** Pasivo. (Equivale a "que debe ser amado").
    
    """)
    
    if os.path.exists("static/images/curso_gramatica/leccion23_gerundio_gerundivo.png"):
        st.image("static/images/curso_gramatica/leccion23_gerundio_gerundivo.png",
                 caption="Diferencias clave: Gerundio vs Gerundivo",
                 use_container_width=True)
    
    st.markdown("""
    ### 2. El Gerundio (Sustantivo Verbal)
    
    El Gerundio sirve para **declinar el infinitivo**.
    El infinitivo (*amare*) se usa como Nominativo. Para los demás casos, usamos el Gerundio.
    
    **Formación**: Tema de presente + **-nd-** + terminaciones de 2ª declinación neutra singular.
    
    """
    )

    render_styled_table(
        ["Caso", "Forma", "Traducción", "Uso"],
        [
            ["**Nom**", "*(Amare)*", "El amar", "Sujeto"],
            ["**Gen**", "Ama**ndi**", "De amar / Del amar", "Complemento de nombre/adjetivo"],
            ["**Dat**", "Ama**ndo**", "Para amar", "Finalidad (poco usado)"],
            ["**Ac**", "*(Amare)* / ad ama**ndum**", "A amar / Para amar", "Objeto / Finalidad (con *ad*)"],
            ["**Abl**", "Ama**ndo**", "Amando / Por amar", "Modo / Instrumento"]
        ]
    )

    st.markdown("""
    
    **Ejemplos**:
    *   *Ars **amandi*** (El arte **de amar**).
    *   *Paratus ad **pugnandum*** (Preparado **para luchar**).
    *   *Discimus **legendo*** (Aprendemos **leyendo**).
    
    ### 3. El Gerundivo (Adjetivo Verbal)
    
    El Gerundivo es un **adjetivo de la 1ª clase** (*-ndus, -nda, -ndum*).
    Indica **necesidad u obligación pasiva**.
    
    **Concordancia**: Como adjetivo, **concuerda** con un sustantivo en género, número y caso.
    
    **Ejemplos**:
    *   *Liber **legendus*** (Un libro **que debe ser leído** / Un libro **para leer**).
    *   *Virtus **laudanda*** (Una virtud **que debe ser alabada** / digna de alabanza).
    
    ### 4. La Construcción de Gerundivo (Sustitución)
    
    En latín clásico, se prefiere usar el **Gerundivo** en lugar del Gerundio cuando hay un Objeto Directo.
    
    **Transformación**:
    1.  **Gerundio + OD**: *Cupidus **videndi** (Gen) **urbem** (Ac)* -> "Deseoso de ver la ciudad".
    2.  **Gerundivo (Concertado)**: *Cupidus **urbis** (Gen) **videndae** (Gen)* -> "Deseoso de la ciudad que debe ser vista".
    
    > **Regla**: El sustantivo toma el caso del gerundio, y el gerundivo concuerda con el sustantivo.
    
    ### 5. Ejercicios de Análisis
    
    Distingue si es Gerundio o Gerundivo:
    
    1.  *Tempus **legendī**.*
        *   **Gerundio** (Genitivo). No concuerda con nada.
        *   → Tiempo **de leer**.
    
    2.  *Ad **pacem petendam** venerunt.*
        *   **Gerundivo**. *Petendam* concuerda con *pacem* (Acusativo Fem. Sing).
        *   → Vinieron **para pedir la paz**.
    
    3.  *In **libro legendo**.*
        *   **Gerundivo**. *Legendo* concuerda con *libro* (Ablativo Masc. Sing).
        *   → **Al leer el libro** (En el libro que debe ser leído).
    
    ### Vocabulario Esencial
    *   **Cupidus, -a, -um**: deseoso (+ Gen)
    *   **Peritus, -a, -um**: experto (+ Gen)
    *   **Ad**: para (+ Acusativo)
    *   **Causa / Gratia**: por causa de, para (+ Genitivo)
    """)

def render_lesson_24():
    st.markdown("""
    ## Lección 24: Conjugaciones Perifrásticas
    
    ### 1. ¿Qué es una Perifrástica?
    
    Una conjugación perifrástica es un rodeo ("perífrasis") para expresar matices que los tiempos normales no tienen, como **intención** o **obligación**.
    
    Se forman con un **Participio** + el verbo **SUM**.
    
    """)
    
    if os.path.exists("static/images/curso_gramatica/leccion24_perifrastica.png"):
        st.image("static/images/curso_gramatica/leccion24_perifrastica.png",
                 caption="Conjugaciones Perifrásticas: Activa vs Pasiva",
                 use_container_width=True)
    
    st.markdown("""
    ### 2. Perifrástica Activa (Intención)
    
    Expresa **intención** de hacer algo o un **futuro inminente**.
    
    **Fórmula**: Participio de Futuro Activo (*-urus, -a, -um*) + *SUM*.
    
    *   **Presente**: *Amaturus sum* -> **Voy a amar** / Tengo intención de amar.
    *   **Imperfecto**: *Amaturus eram* -> **Iba a amar** / Tenía intención de amar.
    *   **Futuro**: *Amaturus ero* -> **Estaré a punto de amar**.
    *   **Subjuntivo**: *Amaturus sim* -> (Que) vaya a amar.
    
    > **Ejemplo clásico**: *Ave, Caesar, **morituri sumus**.* (Los que vamos a morir...).
    
    ### 3. Perifrástica Pasiva (Obligación)
    
    Expresa **obligación** o **necesidad**. Es muy común y potente.
    
    **Fórmula**: Gerundivo (*-ndus, -a, -um*) + *SUM*.
    
    #### A. Construcción Personal (con Sujeto)
    El sujeto "debe ser" algo.
    
    *   *Hic liber **legendus est**.*
        *   Este libro **debe ser leído** (por alguien).
        *   → **Hay que leer** este libro.
    *   *Virtus **colenda est**.*
        *   La virtud **debe ser cultivada**.
    
    #### B. Construcción Impersonal (sin Sujeto, verbos intransitivos)
    Se usa el neutro singular (*-ndum est*).
    
    *   ***Nunc est bibendum**.* (Horacio)
        *   Ahora **se debe beber** / Ahora **hay que beber**.
    *   ***Pugnandum est**.*
        *   **Hay que luchar**.
    
    ### 4. El Dativo Agente
    
    En la Perifrástica Pasiva, la persona QUE tiene la obligación no va en Ablativo (con *a/ab*), sino en **DATIVO**.
    
    *   *Liber **mihi** legendus est.*
        *   Literal: El libro debe ser leído **para mí**.
        *   Traducción: **Yo debo leer** el libro. / **Tengo que leer** el libro.
    
    *   *Carthago **nobis** delenda est.*
        *   Cartago debe ser destruida **por nosotros**.
        *   → **Debemos destruir** Cartago.
    
    ### 5. Ejercicios de Traducción
    
    Traduce estas oraciones con matiz de obligación o intención:
    
    1.  *Bellum **gesturi sumus**.*
        *   Perifrástica Activa (Part. Futuro).
        *   → **Vamos a hacer** la guerra / Tenemos intención de hacer la guerra.
    
    2.  *Pacta **servanda sunt**.*
        *   Perifrástica Pasiva (Gerundivo).
        *   → Los pactos **deben ser cumplidos** (o conservados).
    
    3.  *Hoc **tibi faciendum est**.*
        *   Perifrástica Pasiva + Dativo Agente (*tibi*).
        *   → Esto debe ser hecho **por ti**.
        *   → **Tú tienes que hacer** esto.

    4.  ***Scripturus sum** epistulam.*
        *   Perifrástica Activa.
        *   → **Voy a escribir** una carta / Estoy a punto de escribir una carta.

    5.  ***Delenda est Carthago**.* (Catón el Viejo)
        *   Perifrástica Pasiva.
        *   → Cartago **debe ser destruida**.

    6.  ***Nunc est bibendum**.* (Horacio)
        *   Perifrástica Pasiva Impersonal.
        *   → Ahora **hay que beber** (es momento de celebrar).
    
    ### Vocabulario Esencial
    *   **Gero, gerere**: llevar a cabo, hacer (guerra)
    *   **Servo, servare**: guardar, cumplir, conservar
    *   **Colo, colere**: cultivar, honrar
    *   **Deleo, delere**: destruir
    """)

def render_lesson_25():
    st.markdown("""
    ## Lección 25: Sintaxis I - Coordinación y Subordinadas (Causales/Temp)
    
    ### 1. La Oración Compuesta y la Coordinación
    
    Antes de entrar en las subordinadas, es vital dominar las **conjunciones coordinantes** que unen oraciones del mismo nivel.
    
    #### A. Copulativas (Suman)
    *   **et**: y (la más común).
    *   **-que**: y (enclítica, se une a la segunda palabra). *Senatus Populus**que** Romanus* (El Senado **y** el Pueblo Romano).
    *   **atque / ac**: y además, y también (más fuerte).
    *   **etiam**: también, incluso.
    *   **neque / nec**: y no, ni. *Nec possum nec volo* (Ni puedo ni quiero).
    
    #### B. Disyuntivas (Eligen)
    *   **aut**: o (una cosa o la otra, excluyente). *Vincere **aut** mori* (Vencer **o** morir).
    *   **vel**: o (puedes elegir, incluyente).
    *   **-ve**: o (enclítica). *Bis ter**ve*** (Dos **o** tres veces).
    
    #### C. Adversativas (Oponen)
    *   **sed**: pero, sino. *Non est vivere **sed** valere vita* (La vida no es vivir, **sino** estar sano).
    *   **autem**: pero, en cambio (suele ir en 2ª posición).
    *   **tamen**: sin embargo.
    *   **at**: pero (objeción fuerte).
    
    #### D. Ilativas (Deducen)
    *   **ergo**: por tanto, luego. *Cogito, **ergo** sum* (Pienso, **luego** existo).
    *   **igitur**: así pues (suele ir en 2ª posición).
    *   **itaque**: así que, por consiguiente.
    
    #### E. Causales Coordinadas (Explican)
    *   **nam**: pues, porque (al principio de frase). *Nam tua res agitur* (Pues se trata de tu asunto).
    *   **enim**: pues, en efecto (en 2ª posición).
    *   **etenim**: y en efecto.

    ---

    ### 2. La Lógica de la Subordinación
    
    Las oraciones subordinadas adverbiales funcionan como un adverbio: indican **cuándo** (tiempo), **por qué** (causa), **para qué** (fin), etc.
    
    En latín, el uso del **Indicativo** o **Subjuntivo** depende del matiz:
    *   **Indicativo**: Hecho real, objetivo temporal.
    *   **Subjuntivo**: Causa subjetiva, circunstancia histórica, matiz lógico.
    
    ### 2. El "Cum" Histórico (Narrativo)
    """)



    st.markdown("""
    Es una de las construcciones más frecuentes en la narración histórica (César, Tito Livio).
    
    **Estructura**: **CUM + Subjuntivo** (Imperfecto o Pluscuamperfecto).
    
    **Traducción**:
    *   **Gerundio simple**: *Cum videret* -> "Viendo..."
    *   **Gerundio compuesto**: *Cum vidisset* -> "Habiendo visto..."
    *   **Al + Infinitivo**: "Al ver..."
    *   **Como + Subjuntivo**: "Como viera..."
    
    """)
    
    if os.path.exists("static/images/curso_gramatica/leccion25_causales_temporales.png"):
        st.image("static/images/curso_gramatica/leccion25_causales_temporales.png",
                 caption="Línea Temporal: Cum Histórico y Oraciones Causales",
                 use_container_width=True)
    else:
        render_mermaid(r"""
    graph LR
        A[CUM + Subjuntivo] --> B{Tiempo}
        B -->|Imperfecto| C["Simultaneidad en el pasado<br/>'Cum veniret' = Al venir / Viniendo"]
        B -->|Pluscuamperfecto| D["Anterioridad en el pasado<br/>'Cum venisset' = Al haber venido / Habiendo venido"]
    """)
    
    st.markdown("""
    ### 3. Otras Oraciones Temporales (con Indicativo)
    
    Indican el momento exacto (tiempo puro) y suelen llevar **Indicativo**.
    
    #### Tabla de Conjunciones Temporales:
    """)
    
    render_styled_table(
        ["Conjunción", "Significado", "Ejemplo", "Traducción"],
        [
            ["**Cum** (+ Ind)", "Cuando", "*Cum eum videbis...*", "**Cuando** lo veas..."],
            ["**Ubi**", "Cuando / Donde", "*Ubi Caesar venit...*", "**Cuando** César llegó..."],
            ["**Postquam**", "Después de que", "*Postquam hostes fugerunt...*", "**Después de que** los enemigos huyeron..."],
            ["**Dum** (+ Pres)", "Mientras", "*Dum haec geruntur...*", "**Mientras** esto sucedía..."]
        ]
    )

    st.markdown("""
    
    > **¡Ojo con DUM!** Suele llevar Presente de Indicativo aunque narre el pasado ("Presente Histórico").
    
    ### 4. Oraciones Causales
    
    Explican el motivo de la acción principal.
    
    *   **Quod, Quia, Quoniam** + **Indicativo**: Causa real / objetiva.
        *   *Gaudeo **quod vales**.* (Me alegro **porque estás bien** - es un hecho).
    
    *   **Cum, Quod** + **Subjuntivo**: Causa subjetiva / supuesta.
        *   *Laudatur **quod fuerit** fortis.* (Es alabado **porque [dicen que] fue** valiente).
        *   ***Cum** sis bonus, te amo.* (**Puesto que / Como** eres bueno, te amo).
    
    ### 5. Ejercicios de Análisis
    
    Analiza y traduce:
    
    1.  *Cum Caesar in Galliam venisset, Romani laeti erant.*
        *   *Cum ... venisset* (Cum Histórico, Plusc. Subj).
        *   → **Habiendo llegado César a la Galia**, los romanos estaban contentos.
        *   → **Al llegar César a la Galia**...
    
    2.  *Dum Romae sum, multos libros lego.*
        *   *Dum* + Presente.
        *   → **Mientras estoy en Roma**, leo muchos libros.
    
    3.  *Postquam urbs capta est, milites redierunt.*
        *   *Postquam* + Perfecto Indicativo.
        *   → **Después de que la ciudad fue tomada**, los soldados regresaron.

    4.  *Quod vales, gaudeo.*
        *   *Quod* + Indicativo (Causa real).
        *   → **Porque estás bien**, me alegro.

    5.  *Socrates accusatus est quod corrumperet juventutem.*
        *   *Quod* + Subjuntivo (Causa alegada/subjetiva).
        *   → Sócrates fue acusado **porque (supuestamente) corrompía** a la juventud.
    
    ### Vocabulario Esencial
    *   **Cum**: cuando, como, aunque (depende del contexto)
    *   **Ubi**: cuando, donde
    *   **Postquam**: después de que
    *   **Dum**: mientras
    *   **Quod / Quia**: porque
    """)

def render_lesson_26():
    st.markdown("""
    ## Lección 26: Sintaxis II - Completivas y Finales
    
    ### 1. Oraciones Completivas (Sustantivas)
    
    Las oraciones completivas **funcionan como un sustantivo**: son el **Sujeto** o el **Objeto Directo** del verbo principal.
    
    #### A. Completivas con UT / NE (Verbos de Voluntad)
    Dependen de verbos como *volo* (querer), *nolo* (no querer), *malo* (preferir), *oro* (rogar), *impero* (mandar).
    
    *   **Estructura**: Verbo de voluntad + **UT** (que) / **NE** (que no) + **Subjuntivo**.
    *   *Impero tibi **ut venias**.* (Te mando **que vengas**).
    *   *Oro te **ne eas**.* (Te ruego **que no vayas**).
    
    #### B. Verbos de Temor (*Verba Timendi*)
    ¡Cuidado! Aquí el uso es contraintuitivo:
    *   **Timeo NE...** = Temo **QUE** ocurra (algo que NO quiero).
    *   **Timeo UT...** = Temo **QUE NO** ocurra (algo que SÍ quiero).
    
    *   *Timeo **ne** pluat.* (Temo **que** llueva). [No quiero que llueva]
    *   *Timeo **ut** veniat.* (Temo **que no** venga). [Quiero que venga]
    
    ---

    ### 2. El Doble Juego de "UT" en Adverbiales
    
    La conjunción **UT** (y su negación **NE** o **UT NON**) es una de las más versátiles.
    Dos de sus usos principales con **Subjuntivo** son:
    
    1.  **Finales**: Indican el **propósito** (Para qué).
    2.  **Consecutivas**: Indican la **consecuencia** (De modo que).
    
    """)
    
    if os.path.exists("static/images/curso_gramatica/leccion26_finales_consecutivas.png"):
        st.image("static/images/curso_gramatica/leccion26_finales_consecutivas.png",
                 caption="Oraciones Finales vs Consecutivas",
                 use_container_width=True)
    
    st.markdown("""
    ### 2. Oraciones Finales (Propósito)
    
    Responden a: **¿Para qué?**
    
    *   **Afirmativa**: **UT** + Subjuntivo.
    *   **Negativa**: **NE** + Subjuntivo.
    
    **Ejemplos**:
    *   *Edo **ut vivam**.* (Como **para vivir** / para que viva).
    *   *Hoc facio **ne** puniar.* (Hago esto **para no** ser castigado).
    *   *Legatos misit **ut** pacem **peterent**.* (Envió embajadores **para pedir** la paz).
    
    > **Nota**: En español solemos traducir con "para" + Infinitivo si el sujeto es el mismo, o "para que" + Subjuntivo si cambia.
    
    ### 3. Oraciones Consecutivas (Consecuencia)
    
    Responden a: **¿Con qué consecuencia?**
    Suelen ir anunciadas en la principal por un adverbio o adjetivo de intensidad (**Tam, Ita, Sic, Tantus, Talis**).
    
    *   **Afirmativa**: **UT** + Subjuntivo.
    *   **Negativa**: **UT NON** + Subjuntivo (¡No se usa NE!).
    
    **Ejemplos**:
    *   ***Tam** stultus est **ut** nihil **intelligat**.* (Es **tan** tonto **que no entiende** nada).
    *   ***Ita** locutus est **ut** omnes **flerent**.* (Habló **de tal modo que** todos lloraban).
    *   ***Tantus** erat timor **ut** nemo **exiret**.* (**Tanto** era el miedo **que** nadie salía).
    
    ### 4. Cómo Distinguirlas
    
    #### Diferencias Clave:
    """)
    
    render_styled_table(
        ["Característica", "Finales", "Consecutivas"],
        [
            ["**Significado**", "Intención / Propósito", "Resultado / Efecto"],
            ["**Negación**", "**NE**", "**UT NON**"],
            ["**Pistas**", "Verbos de movimiento, voluntad", "*Tam, Ita, Sic, Tantus, Adeo* en la principal"]
        ]
    )

    st.markdown("""
    
    ### 5. Ejercicios de Análisis
    
    Identifica si es Final o Consecutiva y traduce:
    
    1.  *Milites pugnant **ut** urbem **defendant**.*
        *   ¿Hay pista de intensidad? No. ¿Es propósito? Sí.
        *   → **Final**: Los soldados luchan **para defender** la ciudad.
    
    2.  *Solis ardor **tam** magnus est **ut** herba **arescat**.*
        *   Pista: *Tam* (tan).
        *   → **Consecutiva**: El calor del sol es **tan** grande **que** la hierba se seca.
    
    3.  *Portas clausit **ne** hostes **intrarent**.*
        *   Negación *Ne*.
        *   → **Final**: Cerró las puertas **para que** los enemigos **no entraran**.

    4.  *Timeo **ne** hostes veniant.*
        *   Verbo de temor + *ne*.
        *   → **Completiva (Sustantiva)**: Temo **que** los enemigos vengan.

    5.  *Imperavit militibus **ut** oppugnarent.*
        *   Verbo de mando + *ut*.
        *   → **Completiva (Sustantiva)**: Mandó a los soldados **que** atacaran.
    
    ### Vocabulario Esencial
    *   **Ut**: que, para que, de modo que
    *   **Ne**: para que no
    *   **Tam**: tan
    *   **Ita / Sic**: así, de tal modo
    *   **Tantus, -a, -um**: tanto, tan grande
    *   **Talis, -e**: tal, de tal clase
    """)

def render_lesson_27():
    st.markdown("""
    ## Lección 27: Subordinadas III - Condicionales
    
    ### 1. La Estructura Condicional
    
    Una oración condicional se compone de:
    1.  **Prótasis**: La condición (Si...).
    2.  **Apódosis**: La consecuencia (...entonces...).
    
    En latín, hay tres tipos principales según el grado de realidad.
    """)

    
    st.markdown("""
    """)
    
    if os.path.exists("static/images/curso_gramatica/leccion27_condicionales.png"):
        st.image("static/images/curso_gramatica/leccion27_condicionales.png",
                 caption="Tipos de Oraciones Condicionales",
                 use_container_width=True)
    else:
        render_mermaid(r"""
    graph TD
        C{Tipo de Condición}
        C --> Real["REAL (Tipo I)<br/>Hecho objetivo"]
        C --> Posible["POSIBLE (Tipo II)<br/>Podría ocurrir"]
        C --> Irreal["IRREAL (Tipo III)<br/>No ocurrió / No ocurre"]
        
        Real --> R_Modo[INDICATIVO]
        Posible --> P_Modo["SUBJUNTIVO Presente/Perf"]
        Irreal --> I_Modo["SUBJUNTIVO Imperf/Plusc"]
    """)
    
    st.markdown("""
    ### 2. Tipo I: Realidad (Indicativo)
    
    Expresa un hecho real o lógico. Si pasa A, pasa B.
    
    *   **Modo**: **Indicativo** en ambas partes.
    *   *Si hoc **facis**, **erras**.*
        *   Si haces esto, te equivocas.
    *   *Si **venies**, **videbis**.*
        *   Si vienes (futuro), verás.
    
    ### 3. Tipo II: Posibilidad (Subjuntivo Presente/Perfecto)
    
    Expresa algo que **podría** ocurrir en el futuro, pero no es seguro. ("Si hicieras...").
    
    *   **Modo**: **Subjuntivo Presente** (o Perfecto).
    *   *Si hoc **facias**, **erres**.*
        *   Si hicieras esto (en el futuro), te equivocarías.
        *   (Traducción alternativa: "Si llegaras a hacer esto...")
    
    ### 4. Tipo III: Irrealidad (Subjuntivo Imperfecto/Pluscuamperfecto)
    
    Expresa algo que **no ocurre** (presente) o **no ocurrió** (pasado).
    
    *   **Irreal de Presente**: **Subjuntivo Imperfecto**.
        *   *Si hoc **faceres**, **errares**.*
            *   Si hicieras esto (ahora mismo, pero no lo haces), te equivocarías.
    
    *   **Irreal de Pasado**: **Subjuntivo Pluscuamperfecto**.
        *   *Si hoc **fecisses**, **erravisses**.*
            *   Si hubieras hecho esto (en el pasado), te habrías equivocado.
    
    ### 5. Tabla Resumen
    
    #### Resumen de Condicionales:
    """)
    
    render_styled_table(
        ["Tipo", "Tiempo Latino", "Traducción Prótasis (Si...)", "Traducción Apódosis"],
        [
            ["**Real**", "Indicativo", "Si haces...", "Haces / Harás"],
            ["**Posible**", "Subj. Presente", "Si hicieras...", "Harías / Te equivocarías"],
            ["**Irreal Pres.**", "Subj. Imperfecto", "Si hicieras (ahora)...", "Harías"],
            ["**Irreal Pas.**", "Subj. Pluscuamp.", "Si hubieras hecho...", "Habrías hecho"]
        ]
    )

    st.markdown("""
    
    ### 6. Ejercicios de Análisis
    
    Clasifica y traduce:
    
    1.  *Si venisses, laetus fuissem.*
        *   Tiempos: Pluscuamperfecto Subjuntivo.
        *   Tipo: **Irreal de Pasado**.
        *   → **Si hubieras venido, habría estado contento.**
    
    2.  *Si id credis, erras.*
        *   Tiempos: Presente Indicativo.
        *   Tipo: **Real**.
        *   → **Si crees eso, te equivocas.**
    
    3.  *Si dives sim, orbem peragrem.*
        *   Tiempos: Presente Subjuntivo.
        *   Tipo: **Posible**.
        *   → **Si fuera rico** (llegara a serlo), **recorrería el mundo.**

    4.  *Si tacuisses, philosophus mansisses.* (Boecio)
        *   Tiempos: Pluscuamperfecto Subjuntivo.
        *   Tipo: **Irreal de Pasado**.
        *   → **Si te hubieras callado, habrías permanecido (como un) filósofo.**

    5.  *Si vis pacem, para bellum.* (Vegecio)
        *   Tiempos: Presente Indicativo / Imperativo.
        *   Tipo: **Real**.
        *   → **Si quieres la paz, prepara la guerra.**
    
    ### Vocabulario Esencial
    *   **Si**: si
    *   **Nisi**: si no, a menos que
    *   **Sin**: pero si, si por el contrario
    """)

def render_lesson_28():
    st.markdown("""
    ## Lección 28: Subordinadas IV - Relativas
    
    ### 1. El Pronombre Relativo (Qui, Quae, Quod)
    
    Las oraciones de relativo adjetivan a un sustantivo anterior llamado **antecedente**.
    
    *   "El libro **que** lees es bueno."
        *   Antecedente: *Libro*.
        *   Relativo: *Que*.
    
    ### 2. La Regla de Oro de la Concordancia
    
    El pronombre relativo concuerda con su antecedente en **GÉNERO y NÚMERO**.
    Pero su **CASO** depende de su función **dentro de la oración subordinada**.
    """)


    
    
    if os.path.exists("static/images/curso_gramatica/leccion28_oraciones_relativas.png"):
        st.image("static/images/curso_gramatica/leccion28_oraciones_relativas.png",
                 caption="Árbol de Concordancia del Relativo",
                 use_container_width=True)
    else:
        render_mermaid(r"""
    graph LR
        Ant[Antecedente] -- "Género y Número" --> Rel["Relativo (Qui/Quae/Quod)"]
        Sub["Oración Subordinada"] -- "Función Sintáctica" --> Caso["Caso del Relativo"]
        
        Rel --> Caso
    """)
    
    st.markdown("""
    ### 3. Declinación de Qui, Quae, Quod
    
    #### Declinación del Relativo:
    """)
    
    render_styled_table(
        ["Caso", "Masc. Sg", "Fem. Sg", "Neut. Sg", "Masc. Pl", "Fem. Pl", "Neut. Pl"],
        [
            ["**Nom**", "**qui**", "**quae**", "**quod**", "**qui**", "**quae**", "**quae**"],
            ["**Ac**", "**quem**", "**quam**", "**quod**", "**quos**", "**quas**", "**quae**"],
            ["**Gen**", "**cuius**", "**cuius**", "**cuius**", "**quorum**", "**quarum**", "**quorum**"],
            ["**Dat**", "**cui**", "**cui**", "**cui**", "**quibus**", "**quibus**", "**quibus**"],
            ["**Abl**", "**quo**", "**qua**", "**quo**", "**quibus**", "**quibus**", "**quibus**"]
        ]
    )

    st.markdown("""
    
    ### 4. Ejemplos de Análisis de Caso
    
    1.  *Puer, **quem** vides, amicus meus est.*
        *   Antecedente: *Puer* (Masc, Sg).
        *   Función en sub.: Objeto Directo de *vides* (tú ves al niño).
        *   → Relativo: Masc, Sg, **Acusativo** = **QUEM**.
        *   "El niño, **al cual** ves, es mi amigo."
    
    2.  *Puella, **cui** librum dedi, laeta est.*
        *   Antecedente: *Puella* (Fem, Sg).
        *   Función en sub.: Objeto Indirecto de *dedi* (di el libro a la niña).
        *   → Relativo: Fem, Sg, **Dativo** = **CUI**.
        *   "La niña, **a la cual** di el libro, está contenta."
    
    3.  *Urbs, **in qua** habito, magna est.*
        *   Antecedente: *Urbs* (Fem, Sg).
        *   Función en sub.: CC Lugar (*in* + Abl).
        *   → Relativo: Fem, Sg, **Ablativo** = **QUA**.
        *   "La ciudad **en la que** vivo es grande."
    
    ### 5. Relativas con Subjuntivo
    
    Normalmente llevan Indicativo. Si llevan **Subjuntivo**, añaden un matiz circunstancial (Final, Consecutivo o Causal).
    
    *   **Final**: *Milites misit **qui** (= ut ii) nuntiarent.*
        *   Envió soldados **para que** anunciaran (literal: "que anunciaran").
    
    *   **Consecutiva**: *Nemo est tam stultus **qui** (= ut is) hoc credat.*
        *   Nadie es tan tonto **que** crea esto.

    ### 6. El Relativo de Unión (Nexo Relativo)
    
    En latín, a veces se usa un relativo al **principio de una oración** (después de punto) para referirse a algo dicho anteriormente.
    Se traduce como un demostrativo: "Y este...", "Este...", "El cual...".
    
    *   ***Quae** cum ita sint...*
        *   Literal: Las cuales cosas como sean así...
        *   Traducción: **Y como esto es así...** / **Puesto que esto es así...**
    
    *   ***Quod** cum audivisset...*
        *   Literal: Lo cual como hubiese oído...
        *   Traducción: **Cuando oyó esto...** / **Al oír esto...**
    
    ### Vocabulario Esencial
    *   **Qui, quae, quod**: el cual, la cual, lo cual / que / quien
    *   **Ubi** (adv. relativo): donde (= in quo)
    *   **Unde** (adv. relativo): de donde (= ex quo)
    *   **Quo** (adv. relativo): a donde (= ad quem)
    """)

def render_lesson_29():
    st.markdown("""
    ## Lección 29: Estilo Indirecto (Oratio Obliqua)
    
    ### 1. ¿Qué es la Oratio Obliqua?
    
    Es referir las palabras de otro sin citarlas textualmente.
    *   **Directo**: César dijo: "Voy a Roma".
    *   **Indirecto**: César dijo **que él iba a Roma**.
    
    En latín, esto provoca una transformación gramatical masiva en toda la oración.
    
    ### 2. Reglas de Transformación
    """)


    

    if os.path.exists("static/images/curso_gramatica/leccion29_estilo_indirecto.png"):
        st.image("static/images/curso_gramatica/leccion29_estilo_indirecto.png",
                 caption="Transformación a Estilo Indirecto",
                 use_container_width=True)
    else:
        render_mermaid(r"""
    graph TD
        Directo[ESTILO DIRECTO] --> Indirecto[ESTILO INDIRECTO]
        
        subgraph Oraciones Principales
        D_Princ[Verbo Principal] -->|AcI| I_Princ[Infinitivo + Acusativo]
        D_Imper[Imperativo] -->|Subjuntivo| I_Imper[Subjuntivo]
        end
        
        subgraph Oraciones Subordinadas
        D_Sub[Cualquier Verbo Subordinado] -->|Subjuntivo| I_Sub[Subjuntivo]
        end
    """)
    
    st.markdown("""
    ### 3. Transformación Detallada
    
    #### A. Oraciones Principales (Aseverativas)
    Pasan a la construcción de **Acusativo con Infinitivo (AcI)**.
    
    *   Directo: *"Romani fortes **sunt**."*
    *   Indirecto: *Dicit **Romanos** fortes **esse**.*
    
    #### B. Oraciones Principales (Imperativas / Desiderativas)
    Pasan a **Subjuntivo**.
    
    *   Directo: *"**Veni**, Caesar!"*
    *   Indirecto: *Orat Caesarem **ut veniat**.* (Le ruega que venga).
    
    #### C. Oraciones Subordinadas
    Todos los verbos de las oraciones subordinadas pasan a **SUBJUNTIVO**.
    
    *   Directo: *"Romani, **qui** fortes **sunt**, vincunt."*
    *   Indirecto: *Dicit Romanos, **qui** fortes **sint**, vincere.*
    
    ### 4. Ejemplo Completo de Transformación
    
    **Texto Original (Directo):**
    > *"Ariovistus respondit: Ego in Galliam non veni, sed Galli ad me venerunt. Si quid vultis, pugnate!"*
    
    **Texto Indirecto (César, De Bello Gallico):**
    > *Ariovistus respondit:*
    > 1.  **se** in Galliam non **venisse** (AcI - Inf. Perf),
    > 2.  sed **Gallos** ad **se** **venisse** (AcI - Inf. Perf).
    > 3.  **Si** quid **vellent** (Subj. Imp - Subordinada), **pugnarent** (Subj. Imp - Imperativo transformado).
    
    ### 5. La Consecutio Temporum en Estilo Indirecto
    
    Como todo pasa a Subjuntivo o Infinitivo, la referencia temporal depende del verbo introductor (*Dicit* vs *Dixit*).
    
    *   *Dicit se id facere **quod vellet**.* (Dice que hace lo que quiere).
    
    ### 6. Ejercicios de Práctica
    
    Pasa a Estilo Indirecto dependiendo de *Dicit* (Dice):
    
    1.  *"Puer currit."*
        *   → *Dicit **puerum currere**.*
    
    2.  *"Ego laetus sum."*
        *   → *Dicit **se** laetum **esse**.*
    
    3.  *"Milites, qui pugnant, vincunt."*
        *   → *Dicit **milites**, qui **pugnent**, **vincere**.*

    ### 7. Ejemplo Completo de Análisis
    
    **Texto**: *Caesar dixit se, postquam hostes vicisset, Romam venturum esse.*
    
    *   **Verbo introductor**: *Dixit* (Dijo) -> Tiempo histórico.
    *   **Oración Principal Indirecta**: *se ... Romam venturum esse*.
        *   *se*: Sujeto (César) en Acusativo.
        *   *venturum esse*: Infinitivo Futuro (Posterioridad).
        *   → "Que él vendría a Roma".
    *   **Oración Subordinada**: *postquam hostes vicisset*.
        *   *vicisset*: Pluscuamperfecto Subjuntivo.
        *   ¿Por qué Pluscuamperfecto?
            *   1. Subjuntivo por Estilo Indirecto.
            *   2. Pluscuamperfecto por **Anterioridad** respecto a un tiempo histórico (*Dixit*).
        *   → "Después de que hubiera vencido a los enemigos".
    
    **Traducción final**: César dijo que él, después de haber vencido a los enemigos, vendría a Roma.
    
    ### Vocabulario Esencial
    *   **Aio / Inquam**: decir (defectivos, usados en directo)
    *   **Nego**: decir que no
    *   **Respondeo**: responder
    *   **Nuntio**: anunciar
    *   **Polliceor**: prometer (+ AcI Futuro)
    """)

def render_lesson_30():
    st.markdown("## Lección 30: Métrica y Poesía")
    
    if os.path.exists("static/images/curso_gramatica/leccion30_metrica.png"):
        st.image("static/images/curso_gramatica/leccion30_metrica.png",
                 caption="Esquema del Hexámetro Dactílico",
                 use_container_width=True)
                 
    st.info("🚧 Contenido en desarrollo. Próximamente: Hexametro dactílico, escansión y figuras retóricas.")

def render_lesson_31():
    st.markdown("## Lección 31: César y la Prosa Militar")
    st.image("static/images/curso_gramatica/leccion31_cesar.png",
             caption="Julio César y la Guerra de las Galias",
             use_container_width=True)
    st.info("🚧 Contenido en desarrollo. Próximamente: Análisis de 'De Bello Gallico', estilo directo y preciso.")

def render_lesson_32():
    st.markdown("## Lección 32: Cicerón y la Retórica")
    st.image("static/images/curso_gramatica/leccion32_ciceron.png",
             caption="Cicerón: El Maestro de la Oratoria",
             use_container_width=True)
    st.info("🚧 Contenido en desarrollo. Próximamente: Análisis de discursos (Catilinarias), periodos oratorios.")

def render_lesson_33():
    st.markdown("## Lección 33: Salustio y la Historiografía")
    st.image("static/images/curso_gramatica/leccion33_salustio.png",
             caption="Salustio: La Conjuración de Catilina",
             use_container_width=True)
    st.info("🚧 Contenido en desarrollo. Próximamente: 'Conjuración de Catilina', arcaísmos y brevedad.")

def render_lesson_34():
    st.markdown("## Lección 34: Catulo y la Lírica")
    st.image("static/images/curso_gramatica/leccion34_catulo.png",
             caption="Catulo: Pasión y Lírica",
             use_container_width=True)
    st.info("🚧 Contenido en desarrollo. Próximamente: Poesía neotérica, endecasílabos falecios, Odio et Amo.")

def render_lesson_35():
    st.markdown("## Lección 35: Virgilio y la Épica")
    st.image("static/images/curso_gramatica/leccion35_virgilio.png",
             caption="Virgilio y la Eneida",
             use_container_width=True)
    st.info("🚧 Contenido en desarrollo. Próximamente: 'La Eneida', hexámetro épico, destino de Roma.")

def render_lesson_36():
    st.markdown("## Lección 36: Horacio y las Odas")
    st.image("static/images/curso_gramatica/leccion36_horacio.png",
             caption="Horacio: Carpe Diem",
             use_container_width=True)
    st.info("🚧 Contenido en desarrollo. Próximamente: 'Carpe Diem', aurea mediocritas, lírica reflexiva.")

def render_lesson_37():
    st.markdown("## Lección 37: Ovidio y la Narrativa Poética")
    st.image("static/images/curso_gramatica/leccion37_ovidio.png",
             caption="Ovidio: El Poeta del Cambio",
             use_container_width=True)
    st.info("🚧 Contenido en desarrollo. Próximamente: 'Metamorfosis', dístico elegíaco, mitología.")

def render_lesson_38():
    st.markdown("## Lección 38: Latín Medieval")
    st.info("🚧 Contenido en desarrollo. Próximamente: Cambios sintácticos, vocabulario cristiano, 'Carmina Burana'.")

def render_lesson_39():
    st.markdown("## Lección 39: Latín Eclesiástico")
    st.info("🚧 Contenido en desarrollo. Próximamente: La Vulgata, liturgia, pronunciación eclesiástica.")

def render_lesson_40():
    st.markdown("## Lección 40: Latín Renacentista y Neolatín")
    st.info("🚧 Contenido en desarrollo. Próximamente: Erasmo, Newton, Spinoza, el latín como lengua científica.")

if __name__ == "__main__":
    main()
