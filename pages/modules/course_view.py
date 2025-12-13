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
from utils.exercise_generator import ExerciseGenerator
from utils.reading_service import ReadingService
from utils.progression_engine import (
    get_lesson_status, 
    update_theory_completion, 
    increment_exercises_count,
    mark_reading_completed,
    get_next_step_recommendation
)
from pages.modules.gamified_lesson import render_standard_gamified_lesson





def _render_lesson_progression_bar(lesson_number: int, lesson_status: dict):
    """
    Renders a visual 5-step progression bar for the lesson.
    
    Steps: 1. Theory -> 2. Vocabulary -> 3. Exercises -> 4. Reading -> 5. Challenge
    """
    steps = [
        ("📖 Teoría", lesson_status.get('theory_completed', False)),
        ("🧠 Vocab", lesson_status.get('vocab', {}).get('completed', False)),
        (f"⚔️ Ejercicios ({lesson_status.get('exercises', {}).get('count', 0)}/3)", 
         lesson_status.get('exercises', {}).get('completed', False)),
        ("📖 Lectura", lesson_status.get('reading', {}).get('completed', False)),
        ("🏆 Desafío", lesson_status.get('challenge', {}).get('completed', False)),
    ]
    
    overall_progress = lesson_status.get('overall_progress', 0)
    progress_pct = int(overall_progress * 100)
    
    # Determine step colors
    step_html = ""
    for i, (label, completed) in enumerate(steps):
        if completed:
            color = "#28a745"  # Green
            icon = "✓"
        elif i == 0 or steps[i-1][1]:  # Current step
            color = "#fd7e14"  # Orange (in progress)
            icon = "●"
        else:
            color = "#adb5bd"  # Gray (locked)
            icon = "○"
        
        step_html += f'''
<div style="text-align: center; flex: 1;">
    <div style="font-size: 1.5em; color: {color};">{icon}</div>
    <div style="font-size: 0.75em; color: {color};">{label}</div>
</div>'''
        if i < len(steps) - 1:
            step_html += f'<div style="flex: 0.3; border-top: 2px solid {color if completed else "#adb5bd"}; margin-top: 12px;"></div>'
    
    st.markdown(
        f'''
        <div style="background: linear-gradient(135deg, rgba(139,69,19,0.05), rgba(210,180,140,0.1));
                    padding: 15px; border-radius: 10px; margin-bottom: 15px;
                    border: 1px solid rgba(139,69,19,0.2);">
            <div style="display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 10px;">
                {step_html}
            </div>
            <div style="width: 100%; background-color: #e0e0e0; border-radius: 8px; height: 8px; overflow: hidden;">
                <div style="width: {progress_pct}%; background: linear-gradient(90deg, #8B4513, #A0522D); height: 100%; transition: width 0.5s ease;"></div>
            </div>
            <div style="text-align: center; font-size: 0.8em; color: #666; margin-top: 5px;">
                Lección {lesson_number}: {progress_pct}% completado
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )


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
        
        # Integración de Ejercicios Dinámicos
        from utils.exercise_generator import ExerciseGenerator
        from utils.learning_hub_widgets import (
            render_vocabulary_match_exercise,
            render_multiple_choice_exercise,
            render_sentence_completion_exercise
        )
        
        with get_session() as session:
            generator = ExerciseGenerator(session)
            
            # Selector de tipo de ejercicio
            ex_type = st.selectbox(
                "Tipo de Ejercicio:",
                ["Emparejar Vocabulario", "Opción Múltiple (Morfología)", "Completar Oraciones"],
                key=f"ex_type_practice_l{lesson_number}"
            )
            
            if st.button("Generar Nuevos Ejercicios", key=f"gen_ex_practice_l{lesson_number}"):
                if ex_type == "Emparejar Vocabulario":
                    exercises = generator.generate_vocabulary_match(lesson_number)
                    st.session_state[f"practice_exercises_l{lesson_number}"] = ("vocab", exercises)
                elif ex_type == "Opción Múltiple (Morfología)":
                    exercises = generator.generate_declension_choice(lesson_number)
                    st.session_state[f"practice_exercises_l{lesson_number}"] = ("mc", exercises)
                elif ex_type == "Completar Oraciones":
                    exercises = generator.generate_sentence_completion(lesson_number)
                    st.session_state[f"practice_exercises_l{lesson_number}"] = ("fill", exercises)
            
            # Renderizar ejercicios almacenados
            if f"practice_exercises_l{lesson_number}" in st.session_state:
                ex_type_stored, exercises = st.session_state[f"practice_exercises_l{lesson_number}"]
                if ex_type_stored == "vocab":
                    render_vocabulary_match_exercise(exercises, lesson_number, key_suffix="dyn")
                elif ex_type_stored == "mc":
                    render_multiple_choice_exercise(exercises, lesson_number)
                elif ex_type_stored == "fill":
                    render_sentence_completion_exercise(exercises, lesson_number)
            
    else:
        st.info("🔒 Completa el vocabulario para desbloquear los ejercicios")
    
    st.markdown("")
    
    # Lectura
    st.markdown("### 📖 Lectura Graduada")
    if reading_unlocked:
        from utils.reading_service import ReadingService
        with get_session() as session:
            reader = ReadingService(session)
            text = reader.get_reading_for_lesson(lesson_number)
            
            if text:
                st.markdown(f"#### {text.title}")
                enriched_html = reader.enrich_reading_with_tooltips(text.id)
                st.markdown(enriched_html, unsafe_allow_html=True)
                
                if st.button("Marcar como Leída", key=f"read_l{lesson_number}"):
                    reader.mark_reading_as_completed(1, text.id)
                    st.success("¡Lectura completada!")
            else:
                st.info("No hay lectura asignada para esta lección aún.")
                
    else:
        st.info("🔒 Completa los ejercicios para desbloquear la lectura")
    
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
    
    # Get user level for progression
    from database.connection import get_session
    from database import UserProfile
    from sqlmodel import select
    
    # Get current level from DB or session
    user_level = 1
    user_id = st.session_state.get('user_id', 1)
    
    try:
        with get_session() as session:
            user = session.exec(select(UserProfile).where(UserProfile.id == user_id)).first()
            if user:
                user_level = user.level
    except Exception:
        pass
        
    st.session_state.user_level = user_level # Cache in session
    
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
        "l10": "10. Adjetivos de 2a Clase",
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
        "l26": "26. Subordinadas Sustantivas",
        "l27": "27. Sub. Adverbiales II (Cond/Fin/Cons)",
        "l28": "28. Subordinadas Adjetivas (Relativas)",
        "l29": "29. Estilo Indirecto (Oratio Obliqua)",
        "l30": "30. Verbos Irregulares y Síntesis",
    }
    
    # EXPERTO (L31-40) - Temporalmente oculto hasta completar contenido
    # experto = {
    #     "l31": "31. César y Prosa Militar",
    #     "l32": "32. Cicerón y Retórica",
    #     "l33": "33. Salustio y Historiografía",
    #     "l34": "34. Catulo y Lírica",
    #     "l35": "35. Virgilio y Épica",
    #     "l36": "36. Horacio y Odas",
    #     "l37": "37. Ovidio y Metamorfosis",
    #     "l38": "38. Latín Medieval",
    #     "l39": "39. Latín Eclesiástico",
    #     "l40": "40. Latín Renacentista"
    # }
    
    # Session state for current lesson
    if 'current_lesson' not in st.session_state:
        st.session_state.current_lesson = "intro"
    
    # Determine which level the current lesson belongs to
    current_level = None
    if st.session_state.current_lesson in basico:
        current_level = "basico"
    elif st.session_state.current_lesson in avanzado:
        current_level = "avanzado"
    # experto temporarily hidden
    # elif st.session_state.current_lesson in experto:
    #     current_level = "experto"
    
    # Render level sections with expanders
    with st.sidebar:
        # BÁSICO
        basic_label = "📗 BÁSICO (Intro + Lec. 1-13)" + (" " if current_level == "basico" else "")
        with st.expander(basic_label, expanded=(current_level == "basico")):
            for lesson_id, lesson_name in basico.items():
                # Determine if lesson is unlocked
                is_unlocked = True
                if lesson_id == "intro":
                    is_unlocked = True
                elif lesson_id.startswith("l") and lesson_id[1:].isdigit():
                    num = int(lesson_id[1:])
                    is_unlocked = num <= user_level
                
                # Render button
                display_name = lesson_name
                if not is_unlocked:
                    display_name = f"🔒 {lesson_name}"
                
                # Check if it's the current active lesson
                is_active = (st.session_state.current_lesson == lesson_id)
                type_style = "primary" if is_active else "secondary"
                
                # CLICK HANDLER
                if st.button(
                    display_name,
                    key=f"btn_{lesson_id}",
                    width="stretch",
                    type=type_style,
                    disabled=False # Always enabled to allow feedback
                ):
                    if is_unlocked:
                        st.session_state.current_lesson = lesson_id
                        st.rerun()
                    else:
                        # Show explicit feedback for locked lesson
                        prev_lesson = int(lesson_id[1:]) - 1 if lesson_id.startswith("l") else 0
                        st.toast(f"🔒 **Lección Bloqueada**", icon="🚫")
                        st.error(f"Para desbloquear esta lección, debes completar el **Desafío Final** de la **Lección {prev_lesson}**.")
        
        # AVANZADO
        adv_label = "📘 AVANZADO (Lec. 14-30)" + (" " if current_level == "avanzado" else "")
        with st.expander(adv_label, expanded=(current_level == "avanzado")):
            for lesson_id, lesson_name in avanzado.items():
                # Determine if unlocked
                is_unlocked = False
                if lesson_id.startswith("l") and lesson_id[1:].isdigit():
                    num = int(lesson_id[1:])
                    is_unlocked = num <= user_level
                
                display_name = f"🔒 {lesson_name}" if not is_unlocked else lesson_name
                
                is_active = (st.session_state.current_lesson == lesson_id)
                
                if st.button(
                    display_name,
                    key=f"btn_{lesson_id}",
                    width="stretch",
                    type="primary" if is_active else "secondary",
                    disabled=False
                ):
                    if is_unlocked:
                        st.session_state.current_lesson = lesson_id
                        st.rerun()
                    else:
                        prev_lesson = int(lesson_id[1:]) - 1
                        st.toast(f"🔒 **Lección Bloqueada**", icon="🚫")
                        st.error(f"Para desbloquear esta lección, debes completar el **Desafío Final** de la **Lección {prev_lesson}**.")
        
        # # EXPERTO (Temporalmente oculto)
        # exp_label = "📕 EXPERTO (Lec. 31-40)" + (" " if current_level == "experto" else "")
        # with st.expander(exp_label, expanded=(current_level == "experto")):
        #     for lesson_id, lesson_name in experto.items():
        #         if st.button(
        #             lesson_name,
        #             key=f"btn_{lesson_id}",
        #             width="stretch",
        #             type="primary" if st.session_state.current_lesson == lesson_id else "secondary"
        #         ):
        #             st.session_state.current_lesson = lesson_id
        #             st.rerun()
    
    # Render Content
    render_lesson_content(st.session_state.current_lesson)
    
    # Footer handled by parent page



def render_practice_content(lesson_number, mode="practice", sections=None):
    """
    Renders practice exercises or challenge content.
    
    Args:
        lesson_number: Lesson number
        mode: "practice" or "challenge"
        sections: Optional list of specific sections to render
    """
    user_id = st.session_state.get('user_id', 1)
    
    # Check unlocks - Re-check using helper
    try:
        with get_session() as session:
             # Just checking conditions for UI feedback
             exercises_unlocked = check_unlock_conditions(session, user_id, f"exercises_l{lesson_number}")
             challenge_unlocked = check_unlock_conditions(session, user_id, f"challenge_l{lesson_number}")
    except Exception:
        exercises_unlocked = True
        challenge_unlocked = True
        

    if mode == "practice":
        st.markdown(f"### ⚔️ Práctica: Lección {lesson_number}")
        st.info("Completa 3 sesiones de ejercicios para desbloquear la lectura.")
        
        # 1. Try Loading Static Exercises
        from utils.static_exercise_loader import load_static_exercises
        from utils.learning_hub_widgets import (
            render_vocabulary_match_exercise,
            render_multiple_choice_exercise,
            render_sentence_completion_exercise,
            render_translation_latin_spanish_exercise,
            render_translation_spanish_latin_exercise,
            render_morphology_analysis_exercise,
            render_sentence_builder_exercise,
            render_transformation_exercise,
            render_pattern_recognition_exercise
        )
        
        exercises_data = load_static_exercises(lesson_number)
        
        # Check if we have valid static exercises
        has_static = False
        if exercises_data and 'exercises' in exercises_data and len(exercises_data['exercises']) > 0:
            has_static = True
            
        # Toggle for Dynamic if Static exists
        use_dynamic = False
        if has_static:
            tab_static, tab_dynamic = st.tabs(["📝 Ejercicios Estáticos", "🎲 Generador Dinámico"])
            with tab_dynamic:
                use_dynamic = True
                st.markdown("### 🎲 Generador Aleatorio")
            with tab_static:
                 st.info(f"📚 **{len(exercises_data['exercises'])} ejercicios** disponibles para esta lección")
                 
                 # Organize by type
                 exercises_by_type = {}
                 for ex in exercises_data['exercises']:
                     ex_type = ex.get('type')
                     if ex_type not in exercises_by_type:
                         exercises_by_type[ex_type] = []
                     exercises_by_type[ex_type].append(ex)
                 
                 # Spanish labels
                 exercise_types_spanish = {
                    "vocabulary_match": "🔗 Emparejar Vocabulario",
                    "multiple_choice": "📋 Opción Múltiple",
                    "sentence_completion": "✍️ Completar Oraciones",
                    "translation_latin_spanish": "📖 Traducción Latín → Español",
                    "translation_spanish_latin": "🔄 Traducción Español → Latín",
                    "morphology_analysis": "🔬 Análisis Morfológico",
                    "sentence_builder": "🏗️ Construcción de Oraciones",
                    "transformation": "🔀 Transformaciones",
                    "pattern_recognition": "🎯 Reconocimiento de Patrones"
                 }
                 
                 available_types = [t for t in exercise_types_spanish.keys() if t in exercises_by_type]
                 
                 selected_type = st.selectbox(
                    "Selecciona el tipo de ejercicio:",
                    options=available_types,
                    format_func=lambda x: exercise_types_spanish.get(x, x),
                    key=f"static_type_l{lesson_number}"
                 )
                 
                 st.markdown("---")
                 
                 if selected_type in exercises_by_type:
                     exercises = exercises_by_type[selected_type]
                     st.caption(f"{len(exercises)} ejercicio(s) disponible(s)")
                     
                     # Exercise Selector
                     if len(exercises) > 1:
                         ex_idx = st.selectbox(
                             "Selecciona ejercicio:",
                             range(len(exercises)),
                             format_func=lambda i: f"Ejercicio {i+1}",
                             key=f"ex_sel_{selected_type}_l{lesson_number}"
                         )
                     else:
                         ex_idx = 0
                     
                     exercise = exercises[ex_idx]
                     st.markdown("---")
                     
                     # Render based on type
                     if selected_type == "vocabulary_match":
                         pairs = exercise.get('pairs', [])
                         render_vocabulary_match_exercise(pairs, lesson_number, exercise_index=ex_idx, key_suffix="static")
                     elif selected_type == "multiple_choice":
                         questions = [{
                            "question": exercise.get('question'),
                            "options": exercise.get('options', []),
                            "correct_answer": exercise['options'][exercise.get('correct', 0)] if 'correct' in exercise else "",
                            "explanation": exercise.get('explanation', '')
                         }]
                         render_multiple_choice_exercise(questions, lesson_number, key_suffix=f"static_{ex_idx}")
                     elif selected_type == "sentence_completion":
                         questions = [{
                            "question": exercise.get('sentence', ''),
                            "options": exercise.get('options', []),
                            "correct_answer": exercise['options'][exercise.get('correct', 0)] if 'correct' in exercise else "",
                            "explanation": exercise.get('explanation', ''),
                            "translation": exercise.get('translation', '')
                         }]
                         render_sentence_completion_exercise(questions, lesson_number, key_suffix=f"static_{ex_idx}")
                     elif selected_type == "translation_latin_spanish":
                         render_translation_latin_spanish_exercise(exercise, lesson_number, ex_idx, key_suffix="static")
                     elif selected_type == "translation_spanish_latin":
                         render_translation_spanish_latin_exercise(exercise, lesson_number, ex_idx, key_suffix="static")
                     elif selected_type == "morphology_analysis":
                         render_morphology_analysis_exercise(exercise, lesson_number, ex_idx, key_suffix="static")
                     elif selected_type == "sentence_builder":
                         render_sentence_builder_exercise(exercise, lesson_number, ex_idx, key_suffix="static")
                     elif selected_type == "transformation":
                         render_transformation_exercise(exercise, lesson_number, ex_idx, key_suffix="static")
                     elif selected_type == "pattern_recognition":
                         render_pattern_recognition_exercise(exercise, lesson_number, ex_idx, key_suffix="static")

        else:
            use_dynamic = True
            
        if use_dynamic:
            # Integración de Ejercicios Dinámicos
            from utils.exercise_generator import ExerciseGenerator
            
            with get_session() as session:
                generator = ExerciseGenerator(session)
                
                # Selector de tipo de ejercicio
                ex_type = st.selectbox(
                    "Tipo de Ejercicio (Dinámico):",
                    ["Emparejar Vocabulario", "Opción Múltiple (Morfología)", "Completar Oraciones"],
                    key=f"ex_type_practice_l{lesson_number}"
                )
                
                if st.button("Generar Nuevos Ejercicios", key=f"gen_ex_practice_l{lesson_number}"):
                    if ex_type == "Emparejar Vocabulario":
                        exercises = generator.generate_vocabulary_match(lesson_number)
                        st.session_state[f"practice_exercises_l{lesson_number}"] = ("vocab", exercises)
                    elif ex_type == "Opción Múltiple (Morfología)":
                        exercises = generator.generate_declension_choice(lesson_number)
                        st.session_state[f"practice_exercises_l{lesson_number}"] = ("mc", exercises)
                    elif ex_type == "Completar Oraciones":
                        exercises = generator.generate_sentence_completion(lesson_number)
                        st.session_state[f"practice_exercises_l{lesson_number}"] = ("fill", exercises)
                    
                    # Increment exercise count on generation (simplified for now, ideally on completion)
                    try:
                        increment_exercises_count(session, user_id, lesson_number)
                    except:
                        pass
                
                # Renderizar ejercicios almacenados
                if f"practice_exercises_l{lesson_number}" in st.session_state:
                    st.divider()
                    ex_type_stored, exercises = st.session_state[f"practice_exercises_l{lesson_number}"]
                    if ex_type_stored == "vocab":
                        render_vocabulary_match_exercise(exercises, lesson_number, key_suffix="dyn")
                    elif ex_type_stored == "mc":
                        render_multiple_choice_exercise(exercises, lesson_number)
                    elif ex_type_stored == "fill":
                        render_sentence_completion_exercise(exercises, lesson_number)
    
    elif mode == "challenge" or (sections and "challenge" in sections):
        from pages.modules import challenges_view
        
        # We need to ensure the session state is set up for the challenge view
        # Find the challenge ID for this lesson.
        # This is a bit tricky if we don't have a direct mapping.
        # Fallback: Use the button flow to redirect to the dedicated page if inline isn't ready.
        
        st.success("¡Desafío Desbloqueado!")
        
        if st.button("🚀 INICIAR DESAFÍO", key=f"btn_start_chal_l{lesson_number}"):
            # We need to find the specific challenge ID.
            # Using a simplified query: Challenge order usually matches lesson number or similar.
            with get_session() as session:
                from database import Challenge
                from sqlmodel import select
                # Finding challenge where order matches lesson (Simplified assumption for now)
                challenge = session.exec(select(Challenge).where(Challenge.order == lesson_number)).first()
                if challenge:
                    st.session_state['current_challenge_id'] = challenge.id
                    st.switch_page("pages/06_🎮_Ludus.py") # Or explicit Challenge page
                else:
                    st.error("No se encontró un desafío vinculado a esta lección.")


def render_lesson_with_tabs(lesson_number, theory_content_func):
    """
    Helper function to wrap lesson content with Tabs layout.
    Integrates with progression_engine to track 5-step progress.
    
    Args:
        lesson_number: The lesson number
        theory_content_func: A callable that renders the theory content
    """
    user_id = st.session_state.get('user_id', 1)
    
    # Get lesson status for progression display
    try:
        with get_session() as session:
            lesson_status = get_lesson_status(session, user_id, lesson_number)
    except Exception:
        lesson_status = None
    
    # Show progression bar at top
    if lesson_status:
        _render_lesson_progression_bar(lesson_number, lesson_status)
    
    # Create Tabs
    current_tab_idx = 0
    # Logic to auto-select tab could go here based on progress
    
    tab_labels = ["📖 Teoría", "🧠 Vocabulario", "⚔️ Práctica", "📜 Lectura", "🏆 Desafío"]
    tab_theory, tab_vocab, tab_practice, tab_reading, tab_challenge = st.tabs(tab_labels)
    
    # --- TAB 1: THEORY ---
    with tab_theory:
        theory_content_func()
        
        # Mark theory as completed when viewed
        if not lesson_status or not lesson_status.get('theory_completed'):
            try:
                with get_session() as session:
                    update_theory_completion(session, user_id, lesson_number)
                    # st.toast(f"✅ Teoría de Lección {lesson_number} marcada como completada!") # Less noise
            except Exception:
                pass
        
    # --- TAB 2: VOCABULARY ---
    with tab_vocab:
        from utils.learning_hub_widgets import render_vocabulary_widget
        render_vocabulary_widget(lesson_number)
    
    # --- TAB 3: PRACTICE ---
    with tab_practice:
        # Pass context that this is just practice, not the challenge
        render_practice_content(lesson_number, mode="practice")
    
    # --- TAB 4: READING ---
    with tab_reading:
        with get_session() as session:
            reader = ReadingService(session)
            text = reader.get_reading_for_lesson(lesson_number)
            
            if text:
                st.markdown(f"### {text.title}")
                enriched_html = reader.enrich_reading_with_tooltips(text.id)
                st.markdown(enriched_html, unsafe_allow_html=True)
                
                # Check status
                is_reading_completed = lesson_status.get('reading', {}).get('completed', False) if lesson_status else False
                
                if not is_reading_completed:
                    if st.button("✅ Marcar como Leída", key=f"read_l{lesson_number}"):
                        reader.mark_reading_as_completed(user_id, text.id)
                        # Also update progression engine
                        try:
                            mark_reading_completed(session, user_id, lesson_number)
                            st.balloons()
                            st.success("¡Lectura completada!")
                            time.sleep(1)
                            st.rerun()
                        except Exception:
                            pass
                else:
                    st.success("✅ Lectura completada")
            else:
                st.info("No hay lectura asignada para esta lección aún.")
                
    # --- TAB 5: CHALLENGE ---
    with tab_challenge:
        # Check if unlocked
        is_challenge_unlocked = lesson_status.get('challenge', {}).get('unlocked', False) if lesson_status else False
        
        if is_challenge_unlocked:
             # Render proper challenge UI
             # For now, we reuse render_practice_content with mode='challenge' or similar, 
             # OR explicitly call the challenge widget if it exists separate from practice.
             # Based on current code, 'render_practice_content' handles everything.
             # We should probably modify 'render_practice_content' to ONLY show challenge when correct mode.
             
             # Let's try to assume render_practice_content handles the unified view unless we split it.
             # Since the user wants explicit distinction, we should ensure the Content only shows 
             # the Final Challenge here.
             
             st.markdown("### 🏆 Desafío Final del Capítulo")
             st.markdown("Demuestra tu dominio de la lección para avanzar.")
             
             # Trigger the challenge view from here
             # This might require some refactoring of render_practice_content to allow targeting just the challenge.
             # For now, let's call the generic placeholder or check if there's a specific function.
             # Looking at previous code, 'challenges_view.render_content()' seems to be the main challenge runner.
             
             # We need to set the context for the challenge runner
             if st.button("🚀 Iniciar Desafío Final", key=f"start_final_{lesson_number}"):
                 # Logic to find the challenge ID for this lesson
                 with get_session() as session:
                     # Find challenge for this lesson
                     # Assumption: Challenge is linked to lesson via ID or separate map
                     # For V2, we might not have direct link in simple table yet, usually it's by order.
                     # Let's use a workaround: The Practice tab usually lists challenges.
                     pass
                 st.info("El sistema de desafío dedicado está en construcción. Por favor usa la pestaña Práctica por ahora.")
                 
             # TEMPORARY: Call the standard practice content but ask it to focus on challenge?
             # No, better to verify what render_practice_content does.
             # It likely renders the list of exercises AND the challenge at the bottom.
             # We will just note that for this iteration we enable the tab.
             
             render_practice_content(lesson_number, sections=["challenge"])
             
        else:
             st.warning("🔒 **Desafío Bloqueado**")
             st.markdown("""
             Para desbloquear el Desafío Final, debes completar:
             1. 📖 **Teoría** (Leer la lección)
             2. 🧠 **Vocabulario** (50% maestría)
             3. ⚔️ **Práctica** (3 sesiones de ejercicios)
             4. 📜 **Lectura** (Completar lectura)
             """)
             
             # Show progress
             if lesson_status:
                 st.progress(lesson_status.get('overall_progress', 0) / 100)

    st.divider()
    from utils.learning_hub_widgets import render_lesson_progress_summary
    render_lesson_progress_summary(lesson_number)



def render_database_lesson(lesson):
    """Render a lesson loaded from the database"""
    
    # Check unlocks
    try:
        with get_session() as session:
            vocab_unlocked = check_unlock_conditions(session, 1, f"vocab_l{lesson.lesson_number}")
            exercises_unlocked = check_unlock_conditions(session, 1, f"exercises_l{lesson.lesson_number}")
            reading_unlocked = check_unlock_conditions(session, 1, f"reading_l{lesson.lesson_number}")
    except Exception:
        vocab_unlocked = True
        exercises_unlocked = False
        reading_unlocked = False

    # Get lesson status for progression display
    try:
        with get_session() as session:
            lesson_status = get_lesson_status(session, 1, lesson.lesson_number) # user_id=1 default
    except Exception:
        lesson_status = {}

    # Show progression bar at top
    if lesson_status:
        _render_lesson_progression_bar(lesson.lesson_number, lesson_status)

    # Create Tabs
    tab_theory, tab_vocab, tab_practice, tab_reading = st.tabs(["📖 Teoría", "🧠 Vocabulario", "⚔️ Práctica", "📜 Lectura"])
    
    # --- TAB 1: THEORY ---
    with tab_theory:
        # Display image if available
        if lesson.image_path and os.path.exists(lesson.image_path):
            st.image(lesson.image_path, width="stretch")
        
        # Render markdown content
        st.markdown(lesson.content_markdown)
        
        # Mark as in progress
        try:
            with get_session() as session:
                update_lesson_progress(session, user_id=1, lesson_number=lesson.lesson_number, status="in_progress")
        except:
            pass

    # --- TAB 2: VOCABULARY ---
    with tab_vocab:
        if vocab_unlocked:
            from utils.learning_hub_widgets import render_vocabulary_widget
            render_vocabulary_widget(lesson.lesson_number)
        else:
            st.info("🔒 Completa la teoría para desbloquear el vocabulario.")

    # --- TAB 3: PRACTICE ---
    with tab_practice:
        # Usar la función consolidada
        render_practice_content(lesson.lesson_number)


    # --- TAB 4: READING ---
    with tab_reading:
        if reading_unlocked:
            with get_session() as session:
                reader = ReadingService(session)
                text = reader.get_reading_for_lesson(lesson.lesson_number)
                
                if text:
                    st.markdown(f"### {text.title}")
                    enriched_html = reader.enrich_reading_with_tooltips(text.id)
                    st.markdown(enriched_html, unsafe_allow_html=True)
                    
                    if st.button("Marcar como Leída", key=f"read_db_l{lesson.lesson_number}"):
                        reader.mark_reading_as_completed(1, text.id)
                        st.success("¡Lectura completada!")
                else:
                    st.info("No hay lectura asignada para esta lección aún.")
        else:
            st.info("🔒 Completa los ejercicios para desbloquear la lectura.")


def render_lesson_content(lesson_id):
    """Render lesson content - checks database first, then falls back to hardcoded functions"""
    
    # Try to load from database first
    # UPDATE: Disabled to favor explicit render_lesson_X functions that provide full context (theory, practice, reading callbacks)
    # if lesson_id.startswith("l") and lesson_id[1:].isdigit():
    #     lesson_number = int(lesson_id[1:])
    #     
    #     try:
    #         from database import Lesson
    #         from sqlmodel import select
    #         
    #         with get_session() as session:
    #             db_lesson = session.exec(
    #                 select(Lesson).where(
    #                     Lesson.lesson_number == lesson_number,
    #                     Lesson.is_published == True
    #                 )
    #             ).first()
    #             
    #             if db_lesson:
    #                 # UPDATED: Use new gamified renderer
    #                 render_standard_gamified_lesson(db_lesson)
    #                 # render_database_lesson(db_lesson) # Legacy
    #                 return
    #     except Exception as e:
    #         # If database fails, continue to hardcoded fallback
    #         pass
    
    from utils.progress_service import record_lesson_view
    
    # Registrar visualización de la lección (solo para lecciones numeradas)
    if lesson_id.startswith("l") and lesson_id[1:].isdigit():
        with get_session() as session:
            # Asumimos user_id=1 por ahora
            record_lesson_view(session, 1, int(lesson_id[1:]))

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
    st.image("static/images/intro_course_summary.png", caption="Los Cuatro Pilares del Aprendizaje: Leccion, Memorizacion, Practica y Analisis", width="stretch")

    st.markdown("""
    ## Aprende Latin: Un Enfoque Progresivo
    
    Bienvenido al curso de gramatica latina. Este curso esta disenado para guiarte paso a paso 
    desde los conceptos mas basicos hasta las estructuras complejas, siguiendo el enfoque pedagogico 
    del profesor **Fernando Nieto Mesa**.
    
    ### \u00bfPor que estudiar Latin?
    
    *   **Origen**: Es la madre del espanol y de las lenguas romances (frances, italiano, portugues, etc.).
    *   **Cultura**: Nos conecta con el origen de nuestra civilizacion, leyes y costumbres.
    *   **Etimologia**: Mas del 60% del vocabulario espanol proviene del latin.
    
    ### Estructura del Curso
    
    El curso consta de **40 lecciones progresivas** organizadas en tres niveles:
    
    ---
    
    ## 📗 NIVEL BASICO (Lecciones 1-13)
    **Objetivo**: Fundamentos de morfologia nominal y verbal
    
    """)
    
    render_styled_table(
        ["Leccion", "Titulo", "Contenido Principal", "Objetivo"],
        [
            ["**1**", "Primeros Pasos", "Alfabeto, pronunciacion, primeras palabras", "Familiarizarse con el latin"],
            ["**2**", "El Sujeto", "Nominativo, verbo SUM (presente)", "Estructura de oracion basica"],
            ["**3**", "Primera Declinacion", "Sustantivos femeninos -a, -ae", "Declinar sustantivos 1a"],
            ["**4**", "Segunda Declinacion", "Masculinos -us, neutros -um", "Declinar sustantivos 2a"],
            ["**5**", "El Neutro", "Reglas especiales neutros", "Dominar genero neutro"],
            ["**6**", "Consolidacion", "Adjetivos 1a clase", "Concordancia adj-sustantivo"],
            ["**7**", "Tercera Declinacion", "Temas consonanticos, Dativo", "Declinar sustantivos 3a"],
            ["**8**", "Cuarta Declinacion", "Temas en -u, Preterito Perfecto", "Declinar 4a y tiempo pasado"],
            ["**9**", "Quinta Declinacion", "Temas en -e, Futuro", "Completar 5 declinaciones"],
            ["**10**", "Adjetivos 2a Clase", "Adjetivos 3a declinacion", "Adjetivos de tres tipos"],
            ["**11**", "Comparacion", "Comparativo, superlativo, numerales", "Grados del adjetivo"],
            ["**12**", "Pronombres", "Personales, demostrativos, relativos", "Sistema pronominal completo"],
            ["**13**", "Voz Pasiva y Ablativo", "Pasiva, complementos de lugar", "Voz pasiva e introduccion ablativo"]
        ]
    )
    
    st.markdown("""
    
    ---
    
    ## 📘 NIVEL AVANZADO (Lecciones 14-30)
    **Objetivo**: Sistema verbal completo y sintaxis compleja
    
    """)
    
    render_styled_table(
        ["Leccion", "Titulo", "Contenido Principal", "Objetivo"],
        [
            ["**14**", "Pluscuamperf. y Fut. Perf.", "Tiempos compuestos de indicativo", "Completar indicativo"],
            ["**15**", "Voz Pasiva - Infectum", "Pasiva presente, imperfecto, futuro", "Dominar pasiva infectum"],
            ["**16**", "Voz Pasiva - Perfectum", "Pasiva perfecta con sum + participio", "Dominar pasiva perfectum"],
            ["**17**", "Verbos Deponentes", "Forma pasiva, significado activo", "Identificar deponentes"],
            ["**18**", "Subjuntivo I", "Presente y perfecto subjuntivo", "Formar subjuntivo"],
            ["**19**", "Subjuntivo II", "Imperfecto y plusc. subj., consecutio", "Concordancia de tiempos"],
            ["**20**", "Infinitivos y AcI", "Infinitivos, acusativo con infinitivo", "Oraciones infinitivas"],
            ["**21**", "Participios", "Presente, perfecto, futuro", "Sistema de participios"],
            ["**22**", "Ablativo Absoluto", "Construccion absoluta", "Usar ablativo absoluto"],
            ["**23**", "Gerundio y Gerundivo", "Formas verbales -nd-", "Distinguir gerundio/gerundivo"],
            ["**24**", "Perifrasticas", "Activa (-urus sum) y pasiva (-ndus sum)", "Intencion y obligacion"],
            ["**25**", "Sintaxis I", "Coordinacion, causales, temporales", "Oraciones coordinadas y subordinadas basicas"],
            ["**26**", "Sintaxis II", "Completivas, finales, consecutivas", "Subordinadas con ut/ne"],
            ["**27**", "Condicionales", "Real, posible, irreal", "Tipos de condicion"],
            ["**28**", "Relativas", "Oraciones de relativo, qui quae quod", "Subordinadas adjetivas"],
            ["**29**", "Estilo Indirecto", "Oratio obliqua", "Discurso indirecto Latino"],
            ["**30**", "Metrica y Poesia", "Hexametro, distica elegiaco", "Leer poesia latina"]
        ]
    )
    
    st.markdown("""
    
    ---
    
    ## 📕 NIVEL EXPERTO (Lecciones 31-40)
    **Objetivo**: Autores, estilistica y evolucion del latin
    
    """)
    
    render_styled_table(
        ["Leccion", "Titulo", "Contenido Principal", "Objetivo"],
        [
            ["**31**", "Cesar y Prosa Militar", "De Bello Gallico, estilo militar", "Leer prosa narrativa"],
            ["**32**", "Ciceron y Retorica", "Catilinarias, estilo oratorio", "Leer discursos"],
            ["**33**", "Salustio e Historiografia", "Conjuracion de Catilina", "Leer historia"],
            ["**34**", "Catulo y Lirica", "Carmina, poesia amorosa", "Leer lirica"],
            ["**35**", "Virgilio y Epica", "Eneida, hexametro epico", "Leer epica"],
            ["**36**", "Horacio y Odas", "Odas, metros variados", "Leer poesia lirica"],
            ["**37**", "Ovidio y Metamorfosis", "Transformaciones, hexametro", "Leer poesia narrativa"],
            ["**38**", "Latin Medieval", "Textos medievales", "Reconocer caracteristicas medievales"],
            ["**39**", "Latin Eclesiastico", "Vulgata, liturgia", "Leer textos religiosos"],
            ["**40**", "Latin Renacentista", "Humanismo, neolatin", "Latin moderno y cientifico"]
        ]
    )
    
    st.markdown("""
    
    ---
    
    ### Como usar este curso
    
    1.  **Sigue el orden**: Las lecciones estan cuidadosamente secuenciadas
    2.  **Practica activamente**: Usa las secciones de Memorizacion y Practica
    3.  **Analiza textos**: Usa la herramienta de Analisis para consolidar
    4.  **Estudia con los infogramas**: Recursos visuales para memorizar estructuras clave
    
    \u00a1Comencemos! Selecciona la **Leccion 1** en el menu lateral.
    """)

def render_lesson_1():
    def theory_content():
        st.image("static/images/curso_gramatica/leccion1_mapa_imperio.png", 
                 caption="El Imperio Romano en su máxima extensión, con el Lacio (Latium) y Roma destacados",
                 width="stretch")
        
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
                 width="stretch")
        
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

    def practice_content():
        render_practice_content(1, mode="practice")

    def reading_content():
        from utils.reading_service import ReadingService
        with get_session() as session:
            reader = ReadingService(session)
            text = reader.get_reading_for_lesson(1)
            
            if text:
                st.markdown(f"#### 📖 {text.title}")
                
                # Parse text into words
                words = text.content.split()
                
                # Create two columns: main text (wider) and analysis sidebar
                col_text, col_analysis = st.columns([3, 1])
                
                with col_text:
                    st.markdown("""
                    <style>
                    .reading-word {
                        display: inline-block;
                        padding: 2px 4px;
                        margin: 2px;
                        border-radius: 4px;
                        cursor: pointer;
                        font-size: 1.3em;
                        font-family: 'Georgia', serif;
                        transition: background-color 0.2s;
                    }
                    .reading-word:hover {
                        background-color: #fff3cd;
                    }
                    </style>
                    """, unsafe_allow_html=True)
                    
                    # Render words as clickable buttons in a flow
                    # Use button grid for clickable words
                    num_cols = 8
                    
                    # Use global index for unique keys
                    global_idx = 0
                    rows = [words[i:i+num_cols] for i in range(0, len(words), num_cols)]
                    
                    for row_words in rows:
                        cols = st.columns(len(row_words))
                        for i, word in enumerate(row_words):
                            with cols[i]:
                                clean_word = word.strip('.,;:!?')
                                if st.button(word, key=f"rw_{global_idx}", use_container_width=True):
                                    st.session_state['selected_reading_word'] = clean_word
                                global_idx += 1
                
                with col_analysis:
                    st.markdown("##### 🔍 Análisis")
                    
                    selected_word = st.session_state.get('selected_reading_word', None)
                    
                    if selected_word:
                        # Lookup word in database
                        from database import Word, TextWordLink
                        from sqlmodel import select
                        
                        # First try exact match
                        word_obj = session.exec(
                            select(Word).where(Word.latin == selected_word)
                        ).first()
                        
                        # If not found, try lemmatization with Collatinus
                        if not word_obj:
                            try:
                                from utils.collatinus_analyzer import analyzer
                                if analyzer.is_ready():
                                    analyses = analyzer.analyze_word(selected_word)
                                    if analyses:
                                        lemma = analyses[0].get('lemma', '')
                                        if lemma:
                                            word_obj = session.exec(
                                                select(Word).where(Word.latin == lemma)
                                            ).first()
                                            if word_obj:
                                                st.markdown(f"**{selected_word}** → *{lemma}*")
                                                st.markdown(f"*Morfología:* {analyses[0].get('morph', '')}")
                            except Exception as e:
                                pass  # Fallback silently
                        
                        if word_obj:
                            if selected_word == word_obj.latin:
                                st.markdown(f"**{selected_word}**")
                            st.markdown(f"*Lema:* {word_obj.latin}")
                            st.markdown(f"*Traducción:* {word_obj.translation}")
                            st.markdown(f"*Tipo:* {word_obj.part_of_speech}")
                            if word_obj.definition_es:
                                st.caption(word_obj.definition_es)
                        else:
                            st.info(f"'{selected_word}' no encontrado.")
                    else:
                        st.caption("Haz clic en una palabra para ver su análisis.")
                
                # Comprehension section
                st.markdown("---")
                st.markdown("##### 💡 Comprensión")
                with st.expander("Preguntas de comprensión", expanded=True):
                    questions = [
                        ("¿Dónde está Roma?", "Roma está en Italia."),
                        ("¿Qué idioma hablan los romanos?", "Hablan latín."),
                        ("¿Cómo es Roma?", "Roma es una ciudad grande."),
                    ]
                    
                    for i, (question, answer) in enumerate(questions):
                        st.markdown(f"**{i+1}. {question}**")
                        answer_key = f"comp_q_{i}_revealed"
                        
                        if st.session_state.get(answer_key, False):
                            st.success(f"✓ {answer}")
                        else:
                            if st.button("Ver respuesta", key=f"reveal_q_{i}"):
                                st.session_state[answer_key] = True
                                st.rerun()
            else:
                st.info("Lectura no disponible para esta lección.")

    # Fetch Lesson Object and extract data within session
    from database import Lesson
    from sqlmodel import select
    with get_session() as session:
        lesson = session.exec(select(Lesson).where(Lesson.lesson_number == 1)).first()
        if lesson:
            # Extract all needed attributes while session is active
            lesson_data = {
                'id': lesson.id,
                'lesson_number': lesson.lesson_number,
                'title': lesson.title,
                'content_markdown': lesson.content_markdown,
            }
        else:
            lesson_data = None
        
    if lesson_data:
        render_standard_gamified_lesson(lesson_data, theory_content, practice_content, reading_content)
    else:
        st.error("Error crítico: Lección 1 no encontrada en la base de datos.")


def render_lesson_2():
    def theory_content():
        st.image("static/images/curso_gramatica/leccion2_foro_romano.png",
                 caption="El Foro Romano, centro de la vida pública en la antigua Roma",
                 width="stretch")
        
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
                 width="stretch")
                 
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
        
    def practice_content():
        render_practice_content(2, mode="practice")

    def reading_content():
        from utils.reading_service import ReadingService
        with get_session() as session:
            reader = ReadingService(session)
            text = reader.get_reading_for_lesson(2)
            
            if text:
                st.markdown(f"#### {text.title}")
                enriched_html = reader.enrich_reading_with_tooltips(text.id)
                st.markdown(f"<div>{enriched_html}</div>", unsafe_allow_html=True)
            else:
                st.info("Lectura no disponible para esta lección.")

    # Fetch Lesson Object
    from database import Lesson
    from sqlmodel import select
    with get_session() as session:
        lesson_obj = session.exec(select(Lesson).where(Lesson.lesson_number == 2)).first()
        lesson = None
        if lesson_obj:
            lesson = {
                'id': lesson_obj.id,
                'lesson_number': lesson_obj.lesson_number,
                'title': lesson_obj.title,
                'content_markdown': lesson_obj.content_markdown,
            }
        
    if lesson:
        render_standard_gamified_lesson(lesson, theory_content, practice_content, reading_content)
    else:
        st.error("Error crítico: Lección 2 no encontrada en la base de datos.")

def render_lesson_3():
    def theory_content():
        st.markdown("""
        ## Lección 3: Primera Declinación y Verbos Fundamentales
        
        ### 1. Primera Declinación (Temas en -a): Sustantivos Femeninos
        
        La Primera Declinación agrupa sustantivos mayoritariamente **femeninos** que terminan en **-a** en Nominativo Singular.
        
        **Enunciado**: Los sustantivos se enuncian con el Nominativo y el Genitivo Singular:
        *   *Rosa, rosae* (la rosa, de la rosa) -> indica que es 1a Declinación
        """)
        
        st.image("static/images/curso_gramatica/leccion3_primera_declinacion.png",
                 caption="Primera Declinación completa con ejemplos situacionales de uso de cada caso",
                 width="stretch")

        st.image("static/images/curso_gramatica/leccion3_casos_accion.png",
                 caption="Casos en Acción: Nominativo (Sujeto), Acusativo (Objeto) y Dativo (Receptor)",
                 width="stretch")

        st.markdown("""
        
        > **Nota sobre el Ablativo Sg**: La terminación **-ā** es larga (aunque se escribe igual que el Nominativo).
        
        **Otros ejemplos de 1a Declinación:**
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
                ["1a Sg", "**sum**", "yo soy", "yo estoy"],
                ["2a Sg", "**es**", "tú eres", "tú estás"],
                ["3a Sg", "**est**", "él/ella es", "él/ella está"],
                ["1a Pl", "**sumus**", "nosotros somos", "nosotros estamos"],
                ["2a Pl", "**estis**", "vosotros sois", "vosotros estáis"],
                ["3a Pl", "**sunt**", "ellos/ellas son", "ellos/ellas están"]
            ]
        )

        st.markdown("""
        
        **Ejemplos de uso:**
        *   *Sum Romanus.* (Soy romano)
        *   *Puella est pulchra.* (La niña es hermosa)
        *   *Rosae sunt pulchrae.* (Las rosas son hermosas)
        *   *Ubi es?* (¿Dónde estás?)
        
        ### 3. Primera Conjugación (verbos en -ARE): AMARE (Amar)
        
        Los verbos cuyo infinitivo termina en **-are** pertenecen a la 1a Conjugación.
        Son los más regulares y numerosos.
        
        **Presente de Indicativo - Voz Activa:**
        """)
        
        render_styled_table(
            ["Persona", "Raíz", "Desinencia", "Forma completa", "Español"],
            [
                ["1a Sg", "am-", "**-o**", "am-**o**", "yo amo"],
                ["2a Sg", "am-", "**-as**", "am-**as**", "tú amas"],
                ["3a Sg", "am-", "**-at**", "am-**at**", "él/ella ama"],
                ["1a Pl", "am-", "**-amus**", "am-**amus**", "nosotros amamos"],
                ["2a Pl", "am-", "**-atis**", "am-**atis**", "vosotros amáis"],
                ["3a Pl", "am-", "**-ant**", "am-**ant**", "ellos/ellas aman"]
            ]
        )

        st.markdown("""
        
        **Otros verbos de 1a Conjugación:**
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
        """)
        
    def practice_content():
        render_practice_content(3, mode="practice")

    def reading_content():
        from utils.reading_service import ReadingService
        with get_session() as session:
            reader = ReadingService(session)
            text = reader.get_reading_for_lesson(3)
            
            if text:
                st.markdown(f"#### {text.title}")
                enriched_html = reader.enrich_reading_with_tooltips(text.id)
                st.markdown(enriched_html, unsafe_allow_html=True)
            else:
                st.info("Lectura no disponible para esta lección.")

    # Fetch Lesson Object
    from database import Lesson
    from sqlmodel import select
    with get_session() as session:
        lesson_obj = session.exec(select(Lesson).where(Lesson.lesson_number == 3)).first()
        lesson = None
        if lesson_obj:
            lesson = {
                'id': lesson_obj.id,
                'lesson_number': lesson_obj.lesson_number,
                'title': lesson_obj.title,
                'content_markdown': lesson_obj.content_markdown,
            }
        
    if lesson:
        render_standard_gamified_lesson(lesson, theory_content, practice_content, reading_content)
    else:
        st.error("Error crítico: Lección 3 no encontrada en la base de datos.")

def render_lesson_4():
    def theory_content():
        st.image("static/images/curso_gramatica/leccion4_vida_cotidiana.png",
                 caption="La vida cotidiana en una domus romana",
                 width="stretch")

        st.image("static/images/curso_gramatica/leccion4_escuela_romana.png",
                 caption="Escuela Romana (Ludus Litterarius): El Magister y los Discipuli",
                 width="stretch")
        
        st.markdown("""
        ## Lección 4: Segunda Declinación (Masculinos) y el Acusativo
        
        ### 1. Segunda Declinación: Sustantivos Masculinos en -US
        
        La Segunda Declinación agrupa sustantivos mayoritariamente **masculinos** que terminan en **-us** en Nominativo.
        El Genitivo Singular termina en **-i**.
        
        **Enunciado estándar**: *Dominus, domini* (el señor, del señor)
        
        **Paradigma completo: Dominus, -i (El señor)**
        """)

        st.markdown("### 🧠 Mnemotecnia: Segunda Declinación")
        st.image("static/images/curso_gramatica/leccion4_segunda_declinacion_completa.png",
                 caption="Resumen Visual de la Segunda Declinación (Masculinos y Neutros)",
                 width="stretch")
        
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
        Algunos masculinos de 2a Declinación terminan en **-er** en Nominativo:
        *   *Puer, pueri* (niño) - Mantiene la **e**
        *   *Ager, agri* (campo) - Pierde la **e** en los demás casos
        
        **Otros ejemplos de 2a Declinación Masculina:**
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
        
        **Formación**: Se añade el sufijo temporal **-ba-** (1a/2a conj.) a la raíz del presente.
        
        **Verbo SUM (Irregular):**
        """)
        
        render_styled_table(
            ["Persona", "Forma", "Traducción"],
            [
                ["1a Sg", "**eram**", "yo era / estaba"],
                ["2a Sg", "**eras**", "tú eras / estabas"],
                ["3a Sg", "**erat**", "él/ella era / estaba"],
                ["1a Pl", "**eramus**", "nosotros éramos / estábamos"],
                ["2a Pl", "**eratis**", "vosotros erais / estabais"],
                ["3a Pl", "**erant**", "ellos eran / estaban"]
            ]
        )

        st.markdown("""
        
        **Primera Conjugación (AMARE):**
        """)
        
        render_styled_table(
            ["Persona", "Raíz + Sufijo", "Forma", "Traducción"],
            [
                ["1a Sg", "ama + ba + m", "**amabam**", "yo amaba"],
                ["2a Sg", "ama + ba + s", "**amabas**", "tú amabas"],
                ["3a Sg", "ama + ba + t", "**amabat**", "él/ella amaba"],
                ["1a Pl", "ama + ba + mus", "**amabamus**", "nosotros amábamos"],
                ["2a Pl", "ama + ba + tis", "**amabatis**", "vosotros amabais"],
                ["3a Pl", "ama + ba + nt", "**amabant**", "ellos/ellas amaban"]
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
        
    def practice_content():
        render_practice_content(4, mode="practice")

    def reading_content():
        from utils.reading_service import ReadingService
        with get_session() as session:
            reader = ReadingService(session)
            text = reader.get_reading_for_lesson(4)
            
            if text:
                st.markdown(f"#### {text.title}")
                enriched_html = reader.enrich_reading_with_tooltips(text.id)
                st.markdown(enriched_html, unsafe_allow_html=True)
            else:
                st.info("Lectura no disponible para esta lección.")

    # Fetch Lesson Object
    from database import Lesson
    from sqlmodel import select
    with get_session() as session:
        lesson_obj = session.exec(select(Lesson).where(Lesson.lesson_number == 4)).first()
        lesson = None
        if lesson_obj:
            lesson = {
                'id': lesson_obj.id,
                'lesson_number': lesson_obj.lesson_number,
                'title': lesson_obj.title,
                'content_markdown': lesson_obj.content_markdown,
            }
        
    if lesson:
        render_standard_gamified_lesson(lesson, theory_content, practice_content, reading_content)
    else:
        st.error("Error crítico: Lección 4 no encontrada en la base de datos.")

def render_lesson_5():
    def theory_content():
        st.markdown("""
        ## Lección 5: El Neutro y Segunda Conjugación
        """)
        
        st.image("static/images/curso_gramatica/leccion5_neutro_diagram.png",
                 caption="Diagrama del Género Neutro y sus reglas fundamentales",
                 width="stretch")

        st.image("static/images/curso_gramatica/leccion5_animales_neutros.png",
                 caption="Animales en el campo: muchos nombres de rebaño son Neutros (Ovis, Pecus)",
                 width="stretch")
                 
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
        
        > **Observación**: Los casos Genitivo, Dativo y Ablativo son idénticos a los masculinos de 2a Declinación.
        > La única diferencia está en Nom/Voc/Ac.
        
        **Otros ejemplos de Neutros en -UM:**
        *   *Bellum, -i*: guerra
        *   *Donum, -i*: regalo, don
        *   *Verbum, -i*: palabra
        *   *Caelum, -i*: cielo
        *   *Oppidum, -i*: ciudad, plaza fuerte
        *   *Auxilium, -i*: ayuda, auxilio
        *   *Forum, -i*: foro, plaza pública
        
        **¡Nota sobre concordancia!**
        En latín, cuando el sujeto es neutro plural (*templa*, *bella*), el verbo va en **plural**, igual que con los masculinos y femeninos.
        
        *   *Templa **sunt** pulchra.* ✓ (Correcto) - Los templos son hermosos.
        *   *Templa est pulchra.* ❌ (Incorrecto en latín) - El verbo debe concordar en número.
        
        ### 2. Segunda Conjugación: Verbos en -ĒRE
        
        Los verbos cuyo infinitivo termina en **-ēre** (con **e larga**) pertenecen a la 2a Conjugación.
        
        **Modelo: Monere (Aconsejar, Advertir)**
        
        **Presente de Indicativo:**
        """)
        
        render_styled_table(
            ["Persona", "Raíz", "Desinencia", "Forma", "Español"],
            [
                ["1a Sg", "mone-", "**-o**", "**moneo**", "yo aconsejo"],
                ["2a Sg", "mone-", "**-s**", "**mones**", "tú aconsejas"],
                ["3a Sg", "mone-", "**-t**", "**monet**", "él/ella aconseja"],
                ["1a Pl", "mone-", "**-mus**", "**monemus**", "nosotros aconsejamos"],
                ["2a Pl", "mone-", "**-tis**", "**monetis**", "vosotros aconsejáis"],
                ["3a Pl", "mone-", "**-nt**", "**monent**", "ellos/ellas aconsejan"]
            ]
        )

        st.markdown("""
        
        **Pretérito Imperfecto:**
        Sufijo temporal: **-eba-** (no -ba- como en la 1a)
        """)
        
        render_styled_table(
            ["Persona", "Forma", "Traducción"],
            [
                ["1a Sg", "**monebam**", "yo aconsejaba"],
                ["2a Sg", "**monebas**", "tú aconsejabas"],
                ["3a Sg", "**monebat**", "él/ella aconsejaba"],
                ["1a Pl", "**monebamus**", "nosotros aconsejábamos"],
                ["2a Pl", "**monebatis**", "vosotros aconsejabais"],
                ["3a Pl", "**monebant**", "ellos/ellas aconsejaban"]
            ]
        )

        st.markdown("""
        
        **Otros verbos de 2a Conjugación:**
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
                ["*Bellum timebamus.*", "Bellum (Ac, OD) + timebamus (verbo 1a Pl)", "Temíamos la guerra."]
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
    
    def practice_content():
        render_practice_content(5, mode="practice")

    def reading_content():
        from utils.reading_service import ReadingService
        with get_session() as session:
            reader = ReadingService(session)
            text = reader.get_reading_for_lesson(5)
            
            if text:
                st.markdown(f"#### {text.title}")
                enriched_html = reader.enrich_reading_with_tooltips(text.id)
                st.markdown(enriched_html, unsafe_allow_html=True)
            else:
                st.info("Lectura no disponible para esta lección.")

    # Fetch Lesson Object
    from database import Lesson
    from sqlmodel import select
    with get_session() as session:
        lesson_obj = session.exec(select(Lesson).where(Lesson.lesson_number == 5)).first()
        lesson = None
        if lesson_obj:
            lesson = {
                'id': lesson_obj.id,
                'lesson_number': lesson_obj.lesson_number,
                'title': lesson_obj.title,
                'content_markdown': lesson_obj.content_markdown,
            }
        
    if lesson:
        render_standard_gamified_lesson(lesson, theory_content, practice_content, reading_content)
    else:
        st.error("Error crítico: Lección 5 no encontrada en la base de datos.")

def render_lesson_6():
    def theory_content():
        st.image("static/images/curso_gramatica/leccion6_arquitectura.png",
                 caption="Arquitectura romana icónica: Coliseo, Panteón, acueductos y columnas",
                 width="stretch")
        
        st.markdown("""
        ## Lección 6: Consolidación, 3a/4a Conjugación y Adjetivos
        """)
        
        st.image("static/images/curso_gramatica/conjugaciones_overview.png",
                 caption="Resumen visual de las 4 conjugaciones latinas",
                 width="stretch")
                 
        st.markdown("""
        
        ### Revisión: Lo que hemos aprendido hasta ahora
        
        **Declinaciones:**
        *   1a Declinación: Femeninos en **-a** (*rosa, puella*)
        *   2a Declinación: Masculinos en **-us/-er** (*dominus, puer*) y Neutros en **-um** (*templum*)
        
        **Casos dominados:**
        *   **Nominativo**: Sujeto
        *   **Acusativo**: Objeto Directo
        
        **Verbos:**
        *   *Sum* (irregular): Presente e Imperfecto
        *   1a Conjugación (*amare*): Presente e Imperfecto
        *   2a Conjugación (*monere*): Presente e Imperfecto
        
        ### 1. Tercera Conjugación: Verbos en -ERE (e breve)
        
        Los verbos cuyo infinitivo termina en **-ere** (con **e breve**, no larga) pertenecen a la 3a Conjugación.
        Son más irregulares que la 1a y 2a.
        
        **Modelo: Legere (Leer)**
        
        **Presente de Indicativo:**
        """)
    
        render_styled_table(
            ["Persona", "Forma", "Español"],
            [
                ["1a Sg", "**lego**", "yo leo"],
                ["2a Sg", "**legis**", "tú lees"],
                ["3a Sg", "**legit**", "él/ella lee"],
                ["1a Pl", "**legimus**", "nosotros leemos"],
                ["2a Pl", "**legitis**", "vosotros leéis"],
                ["3a Pl", "**legunt**", "ellos/ellas leen"]
            ]
        )
    
        st.markdown("""
        
        **Pretérito Imperfecto:**
        Sufijo: **-eba-** (igual que la 2a)
        *   *legebam, legebas, legebat, legebamus, legebatis, legebant*
        
        **Otros verbos de 3a Conjugación:**
        *   *Dico, dicere*: decir
        *   *Duco, ducere*: conducir, guiar
        *   *Scribo, scribere*: escribir
        *   *Mitto, mittere*: enviar
        *   *Vivo, vivere*: vivir
        
        ### 2. Cuarta Conjugación: Verbos en -IRE
        
        Los verbos cuyo infinitivo termina en **-ire** pertenecen a la 4a Conjugación.
        
        **Modelo: Audire (Oír, Escuchar)**
        
        **Presente de Indicativo:**
        """)
    
        render_styled_table(
            ["Persona", "Forma", "Español"],
            [
                ["1a Sg", "**audio**", "yo oigo"],
                ["2a Sg", "**audis**", "tú oyes"],
                ["3a Sg", "**audit**", "él/ella oye"],
                ["1a Pl", "**audimus**", "nosotros oímos"],
                ["2a Pl", "**auditis**", "vosotros oís"],
                ["3a Pl", "**audiunt**", "ellos/ellas oyen"]
            ]
        )
    
        st.markdown("""
        
        **Pretérito Imperfecto:**
        Sufijo: **-ieba-**
        *   *audiebam, audiebas, audiebat, audiebamus, audiebatis, audiebant*
        
        **Otros verbos de 4a Conjugación:**
        *   *Venio, venire*: venir
        *   *Dormio, dormire*: dormir
        *   *Sentio, sentire*: sentir
        """)
        
        st.markdown("### 🧠 Mnemotecnia: Primera Declinación")
        
        st.image("static/images/curso_gramatica/leccion3_rosa_diagram.png",
                 caption="Diagrama Clásico de ROSA (Estructura)",
                 width="stretch")
    
        st.image("static/images/curso_gramatica/leccion3_rosa_paradigma_mnemotecnia.png",
                 caption="Mnemotecnia: Paradigma y Trucos de Memoria",
                 width="stretch")
    
        st.image("static/images/curso_gramatica/leccion3_verbo_sum_mnemotecnia.png",
                 caption="Conjugación del Verbo SUM y Regla Mnemotécnica",
                 width="stretch")
    
        if os.path.exists("static/images/curso_gramatica/leccion6_sum_possum_tree.png"):
            st.image("static/images/curso_gramatica/leccion6_sum_possum_tree.png",
                     caption="El Árbol de SUM y POSSUM: Raíces y Ramas",
                     width="stretch")
        
        st.markdown("""
        ### 3. Adjetivos de Primera Clase (Sistema 2-1-2)
        
        Los adjetivos de 1a Clase se declinan como los sustantivos de **1a y 2a Declinación**.
        
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
        
        **Otros adjetivos de 1a Clase:**
        *   *Magnus, -a, -um*: grande
        *   *Parvus, -a, -um*: pequeño
        *   *Pulcher, pulchra, pulchrum*: hermoso
        *   *Liber, libera, liberum*: libre
        *   *Malus, -a, -um*: malo
        
        ### 4. El Caso Vocativo: La Invocación
        
        El **Vocativo** se usa para **invocar, llamar o dirigirse** a alguien.
        
        **Reglas:**
        *   En 1a Declinación: **igual al Nominativo**
        *   En 2a Declinación (-us): termina en **-e**
        *   En 2a Declinación (-um): **igual al Nominativo**
        
        **Ejemplos:**
        *   *Domine!* (¡Señor!)
        *   *Puella!* (¡Niña!)
        *   *Fili!* (¡Hijo!) - Excepción: *filius* hace *fili*, no *filie*
        *   *Mi amice!* (¡Amigo mío!)
        """)
        
    def practice_content():
        render_practice_content(6, mode="practice")

    def reading_content():
        from utils.reading_service import ReadingService
        with get_session() as session:
            reader = ReadingService(session)
            text = reader.get_reading_for_lesson(6)
            
            if text:
                st.markdown(f"#### {text.title}")
                enriched_html = reader.enrich_reading_with_tooltips(text.id)
                st.markdown(enriched_html, unsafe_allow_html=True)
            else:
                st.info("Lectura no disponible para esta lección.")

    # Fetch Lesson Object
    from database import Lesson
    from sqlmodel import select
    with get_session() as session:
        lesson_obj = session.exec(select(Lesson).where(Lesson.lesson_number == 6)).first()
        lesson = None
        if lesson_obj:
            lesson = {
                'id': lesson_obj.id,
                'lesson_number': lesson_obj.lesson_number,
                'title': lesson_obj.title,
                'content_markdown': lesson_obj.content_markdown,
            }
        
    if lesson:
        render_standard_gamified_lesson(lesson, theory_content, practice_content, reading_content)
    else:
        st.error("Error crítico: Lección 6 no encontrada en la base de datos.")

def render_lesson_7():
    def theory_content():
        st.markdown("""
        ## Lección 7: Tercera Declinación y el Dativo
        """)
        
        st.image("static/images/curso_gramatica/leccion7_third_declension.png",
                 caption="Esquema de la Tercera Declinación: Imparísílabos y Parisísílabos",
                 width="stretch")

        st.image("static/images/curso_gramatica/leccion7_soldado_romano.png",
                 caption="El Soldado Romano: Muchas partes del cuerpo y equipo son de la 3a Declinación",
                 width="stretch")
                 
        st.markdown("""
        
        ### 1. Tercera Declinación: La Más Compleja
        
        La 3a Declinación es la más amplia y compleja. Agrupa sustantivos de **los tres géneros**.
        
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
        
        **Neutros de 3a Declinación:**
        Siguen la **regla de oro del neutro** (Nom/Voc/Ac iguales, plural en -a).
        
        *   *Corpus, corporis* (n): cuerpo
        *   *Opus, operis* (n): obra
        *   *Nomen, nominis* (n): nombre
        
        ### 3. Excepciones de la Tercera Declinación (Refuerzo)
        """)
    
        if os.path.exists("static/images/curso_gramatica/leccion7_rarezas_3a.png"):
            st.image("static/images/curso_gramatica/leccion7_rarezas_3a.png",
                     caption="Museo de Rarezas: Vis, Bos, Sus, Iuppiter",
                     width="stretch")
    
        if os.path.exists("static/images/curso_gramatica/leccion7_torre_i.png"):
            st.image("static/images/curso_gramatica/leccion7_torre_i.png",
                     caption="La Torre de la -i: Turris, Puppis, Securis, Mare, Animal",
                     width="stretch")
    
        st.markdown("""
        ### 4. El Caso Dativo: Objeto Indirecto
        
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
        *   1a Declinación: Sg **-ae**, Pl **-is**
        *   2a Declinación: Sg **-o**, Pl **-is**
        *   3a Declinación: Sg **-i**, Pl **-ibus**
        """)
        
    def practice_content():
        render_practice_content(7, mode="practice")

    def reading_content():
        from utils.reading_service import ReadingService
        with get_session() as session:
            reader = ReadingService(session)
            text = reader.get_reading_for_lesson(7)
            
            if text:
                st.markdown(f"#### {text.title}")
                enriched_html = reader.enrich_reading_with_tooltips(text.id)
                st.markdown(enriched_html, unsafe_allow_html=True)
            else:
                st.info("Lectura no disponible para esta lección.")

    # Fetch Lesson Object
    from database import Lesson
    from sqlmodel import select
    with get_session() as session:
        lesson_obj = session.exec(select(Lesson).where(Lesson.lesson_number == 7)).first()
        lesson = None
        if lesson_obj:
            lesson = {
                'id': lesson_obj.id,
                'lesson_number': lesson_obj.lesson_number,
                'title': lesson_obj.title,
                'content_markdown': lesson_obj.content_markdown,
            }
        
    if lesson:
        render_standard_gamified_lesson(lesson, theory_content, practice_content, reading_content)
    else:
        st.error("Error crítico: Lección 7 no encontrada en la base de datos.")

def render_lesson_8():
    def theory_content():
        st.markdown("""
        ## Lección 8: Cuarta Declinación, Pretérito Perfecto y Genitivo
        """)
        
        st.image("static/images/curso_gramatica/leccion8_perfect_tense.png",
                 caption="El Pretérito Perfecto: Formación y Uso",
                 width="stretch")
                 
        st.markdown("""
        
        ### 1. Cuarta Declinación: Temas en -U
        
        Sustantivos mayoritariamente **masculinos** (aunque hay algunos femeninos y neutros).
        Terminan en **-us** en Nominativo y **-us** en Genitivo (no confundir con la 2a).
        
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
        
        # Infografía de la 4ª Declinación
        if os.path.exists("static/images/curso_gramatica/leccion8_cuarta_declinacion.png"):
            st.image("static/images/curso_gramatica/leccion8_cuarta_declinacion.png",
                     caption="Cuarta Declinación: Paradigma y Características",
                     width="stretch")
    
        st.markdown("""
        
        **Otros ejemplos de 4a Declinación:**
        *   *Exercitus, -us* (m): ejército
        *   *Fructus, -us* (m): fruto
        *   *Senatus, -us* (m): senado
        *   *Portus, -us* (m): puerto
        *   *Domus, -us* (f): casa (irregular, mezcla 2a y 4a)
        
        **Neutros de 4a Declinación** (muy raros):
        *   *Cornu, -us* (n): cuerno
        *   *Genu, -us* (n): rodilla
        
        
        ### 2. Pretérito Perfecto (Perfectum): El Pasado Acabado
        
        El **Pretérito Perfecto** expresa una acción **completada en el pasado**.
        Equivale a "amé", "he amado" en español.
        
        **Formación**: Se construye sobre el **tema de perfecto** (3a forma del enunciado del verbo).
        
        **Enunciado completo de un verbo**: Siempre se dan 4 formas:
        1.  Presente 1a Sg: *amo*
        2.  Infinitivo: *amare*
        3.  **Perfecto 1a Sg**: *amavi*
        4.  Supino: *amatum*
        
        **Terminaciones del Perfecto** (IGUALES para todas las conjugaciones):
        
        """
        )
    
        render_styled_table(
            ["Persona", "Desinencia", "Ejemplo (AMARE)", "Traducción"],
            [
                ["1a Sg", "**-i**", "amav-**i**", "yo amé / he amado"],
                ["2a Sg", "**-isti**", "amav-**isti**", "tú amaste"],
                ["3a Sg", "**-it**", "amav-**it**", "él/ella amó"],
                ["1a Pl", "**-imus**", "amav-**imus**", "nosotros amamos"],
                ["2a Pl", "**-istis**", "amav-**istis**", "vosotros amasteis"],
                ["3a Pl", "**-erunt/-ere**", "amav-**erunt**", "ellos/ellas amaron"]
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
        *   1a Declinación: Sg **-ae**, Pl **-arum**
        *   2a Declinación: Sg **-i**, Pl **-orum**
        *   3a Declinación: Sg **-is**, Pl **-um/-ium**
        *   4a Declinación: Sg **-us**, Pl **-uum**
    
        ### 4. El Genitivo Partitivo (El Todo y la Parte)
        
        Un uso muy común del genitivo es expresar **el todo del cual se toma una parte**.
        
        *   *Pars militum* (Una parte **de los soldados**)
        *   *Nihil boni* (Nada **de bueno**)
        *   *Plus pecuniae* (Más **de dinero** -> Más dinero)
        
        """)
        
        if os.path.exists("static/images/curso_gramatica/genitivo_partitivo.png"):
            st.image("static/images/curso_gramatica/genitivo_partitivo.png",
                     caption="Genitivo Partitivo: La Parte del Todo (Pars militum, Nihil boni, Plus pecuniae)",
                     width="stretch")
    

        
    def practice_content():
        render_practice_content(8, mode="practice")

    def reading_content():
        from utils.reading_service import ReadingService
        with get_session() as session:
            reader = ReadingService(session)
            text = reader.get_reading_for_lesson(8)
            
            if text:
                st.markdown(f"#### {text.title}")
                enriched_html = reader.enrich_reading_with_tooltips(text.id)
                st.markdown(enriched_html, unsafe_allow_html=True)
            else:
                st.info("Lectura no disponible para esta lección.")

    # Fetch Lesson Object
    from database import Lesson
    from sqlmodel import select
    with get_session() as session:
        lesson_obj = session.exec(select(Lesson).where(Lesson.lesson_number == 8)).first()
        lesson = None
        if lesson_obj:
            lesson = {
                'id': lesson_obj.id,
                'lesson_number': lesson_obj.lesson_number,
                'title': lesson_obj.title,
                'content_markdown': lesson_obj.content_markdown,
            }
        
    if lesson:
        render_standard_gamified_lesson(lesson, theory_content, practice_content, reading_content)
    else:
        st.error("Error crítico: Lección 8 no encontrada en la base de datos.")

def render_lesson_9():
    def theory_content():
        st.markdown("""
        ## Lección 9: Quinta Declinación y Futuro
        """)
        
        st.image("static/images/curso_gramatica/leccion9_fifth_declension.png",
                 caption="La Quinta Declinación: Temas en -E",
                 width="stretch")

        st.image("static/images/curso_gramatica/leccion9_calendario_fiestas.png",
                 caption="Calendario Romano y Fiestas (Las fechas usaban la 5a Declinación: Dies, Idus, Kalendae)",
                 width="stretch")
                 
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
        
        **Palabra más importante de 5a Declinación:**
        *   **Res, rei** (f): cosa, asunto, hecho
            - *Res publica* = La cosa pública = La república
        
        **Otras palabras de 5a Declinación:**
        *   *Spes, spei* (f): esperanza
        *   *Fides, fidei* (f): fe, confianza
        *   *Species, speciei* (f): aspecto, especie
        
        ### 2. Futuro Imperfecto: El Tiempo Venidero
        
        El **Futuro Imperfecto** expresa una acción que **ocurrirá en el futuro**.
        
        **¡Atención!** La formación es **diferente** en 1a/2a conj. y 3a/4a conj.
        
        #### A. Primera y Segunda Conjugación: Sufijo -BO-
        
        **Modelo: AMARE**
        
        """
        )
    
        render_styled_table(
            ["Persona", "Forma", "Traducción"],
            [
                ["1a Sg", "ama-**bo**", "yo amaré"],
                ["2a Sg", "ama-**bis**", "tú amarás"],
                ["3a Sg", "ama-**bit**", "él/ella amará"],
                ["1a Pl", "ama-**bimus**", "nosotros amaremos"],
                ["2a Pl", "ama-**bitis**", "vosotros amaréis"],
                ["3a Pl", "ama-**bunt**", "ellos/ellas amarán"]
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
                ["1a Sg", "leg-**am**", "yo leeré"],
                ["2a Sg", "leg-**es**", "tú leerás"],
                ["3a Sg", "leg-**et**", "él/ella leerá"],
                ["1a Pl", "leg-**emus**", "nosotros leeremos"],
                ["2a Pl", "leg-**etis**", "vosotros leeréis"],
                ["3a Pl", "leg-**ent**", "ellos/ellas leerán"]
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
            ["Tiempo", "Significado", "1a/2a Conj", "3a/4a Conj"],
            [
                ["**Presente**", "amo", "-o, -as, -at", "-o, -is, -it"],
                ["**Imperfecto**", "amaba", "-**ba**m, -**ba**s", "-**eba**m, -**eba**s"],
                ["**Perfecto**", "amé", "-**vi**, -v**isti**", "Varía según verbo"],
                ["**Futuro**", "amaré", "-**bo**, -**bis**", "-**am**, -**es**"]
            ]
        )
    
        st.markdown("""
        """)
    
        st.markdown("### 🧠 Mnemotecnia: Las 5 Declinaciones")
        st.image("static/images/curso_gramatica/leccion9_5declinaciones_completas.png",
                 caption="Resumen Visual de las 5 Declinaciones Latinas",
                 width="stretch")
        
        # Cultural content: Roman Seasons
        st.markdown("### 🏛️ Cultura Romana: Las Cuatro Estaciones")
        st.info("La palabra **dies** (día) nos conecta con el calendario romano. Veamos cómo los romanos nombraban las estaciones:")
        if os.path.exists("static/images/curso_gramatica/cultura_estaciones.png"):
            st.image("static/images/curso_gramatica/cultura_estaciones.png",
                     caption="Las Cuatro Estaciones en Roma: Ver, Aestas, Autumnus, Hiems",
                     width="stretch")
        

        
    def practice_content():
        render_practice_content(9, mode="practice")

    def reading_content():
        from utils.reading_service import ReadingService
        with get_session() as session:
            reader = ReadingService(session)
            text = reader.get_reading_for_lesson(9)
            
            if text:
                st.markdown(f"#### {text.title}")
                enriched_html = reader.enrich_reading_with_tooltips(text.id)
                st.markdown(enriched_html, unsafe_allow_html=True)
            else:
                st.info("Lectura no disponible para esta lección.")

    # Fetch Lesson Object
    from database import Lesson
    from sqlmodel import select
    with get_session() as session:
        lesson_obj = session.exec(select(Lesson).where(Lesson.lesson_number == 9)).first()
        lesson = None
        if lesson_obj:
            lesson = {
                'id': lesson_obj.id,
                'lesson_number': lesson_obj.lesson_number,
                'title': lesson_obj.title,
                'content_markdown': lesson_obj.content_markdown,
            }
        
    if lesson:
        render_standard_gamified_lesson(lesson, theory_content, practice_content, reading_content)
    else:
        st.error("Error crítico: Lección 9 no encontrada en la base de datos.")

def render_lesson_10():
    def theory_content():
        st.markdown("""
        ## Lección 10: Adjetivos de Segunda Clase y Sintaxis
        """)
        
        if os.path.exists("static/images/curso_gramatica/leccion10_adjetivos_2clase.png"):
            st.image("static/images/curso_gramatica/leccion10_adjetivos_2clase.png",
                     caption="Clasificación de Adjetivos de 3a Declinación (2a Clase)",
                     width="stretch")
                     
        st.markdown("""
        
        ### Revisión: Las Cinco Declinaciones y los Casos
        
        Ya hemos cubierto **todas las declinaciones del latín**:
        *   1a: Femeninos en -a (*rosa, puella*)
        *   2a: Masculinos en -us/er (*dominus, puer*) y Neutros en -um (*templum*)
        *   3a: Los tres géneros (*rex, urbs, corpus*)
        *   4a: Masculinos/Femeninos en -us (*manus, senatus*)
        *   5a: Femeninos en -es (*res, dies*)
        
        Y **todos los seis casos**: Nominativo, Vocativo, Acusativo, Genitivo, Dativo, Ablativo.
        
        ### 1. Adjetivos de Segunda Clase (3a Declinación)
        
        Los adjetivos de 2a Clase se declinan como sustantivos de **3a Declinación** (temas en -i).
        
        **Tres tipos según el número de terminaciones:**
        
        #### A. Tres Terminaciones (M / F / N)
        
        **Modelo: Acer, acris, acre (Agudo, penetrante)**
        *   Masc: *acer* (como *puer* pero con casos de 3a)
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
        

        
    def practice_content():
        render_practice_content(10, mode="practice")

    def reading_content():
        from utils.reading_service import ReadingService
        with get_session() as session:
            reader = ReadingService(session)
            text = reader.get_reading_for_lesson(10)
            
            if text:
                st.markdown(f"#### {text.title}")
                enriched_html = reader.enrich_reading_with_tooltips(text.id)
                st.markdown(enriched_html, unsafe_allow_html=True)
            else:
                st.info("Lectura no disponible para esta lección.")

    # Fetch Lesson Object
    from database import Lesson
    from sqlmodel import select
    with get_session() as session:
        lesson_obj = session.exec(select(Lesson).where(Lesson.lesson_number == 10)).first()
        lesson = None
        if lesson_obj:
            lesson = {
                'id': lesson_obj.id,
                'lesson_number': lesson_obj.lesson_number,
                'title': lesson_obj.title,
                'content_markdown': lesson_obj.content_markdown,
            }
        
    if lesson:
        render_standard_gamified_lesson(lesson, theory_content, practice_content, reading_content)
    else:
        st.error("Error crítico: Lección 10 no encontrada en la base de datos.")

def render_lesson_11():
    def theory_content():
        st.markdown("""
        ## Lección 11: Comparativos, Superlativos y Numerales
        """)
        
        if os.path.exists("static/images/curso_gramatica/leccion11_comparative_degrees.png"):
            st.image("static/images/curso_gramatica/leccion11_comparative_degrees.png",
                     caption="Grados del Adjetivo: Positivo, Comparativo, Superlativo",
                     width="stretch")
        
        st.markdown("""
        
        ### 1. Grados del Adjetivo
        
        En latín, como en español, los adjetivos tienen tres grados:
        
        #### A. Positivo (Normal)
        *   *Altus* (Alto)
        *   *Fortis* (Fuerte)
        
        #### B. Comparativo (Más que...)
        
        **Formación**: Raíz + **-ior** (m/f) / **-ius** (n)
        
        **Modelo: Altior, altius (Más alto)**
        Se declina como 3a Declinación.
        
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
        Se declina como adjetivo de 1a Clase (2-1-2).
        
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

        
        # Infografía Cultural: Numerales Romanos en la Vida Cotidiana
        if os.path.exists("static/images/curso_gramatica/leccion11_numerales_monumentos.png"):
            st.image("static/images/curso_gramatica/leccion11_numerales_monumentos.png",
                     caption="Numerales Romanos en Monumentos y la Vida Cotidiana",
                     width="stretch")
        
    def practice_content():
        render_practice_content(11, mode="practice")

    def reading_content():
        from utils.reading_service import ReadingService
        with get_session() as session:
            reader = ReadingService(session)
            text = reader.get_reading_for_lesson(11)
            
            if text:
                st.markdown(f"#### {text.title}")
                enriched_html = reader.enrich_reading_with_tooltips(text.id)
                st.markdown(enriched_html, unsafe_allow_html=True)
            else:
                st.info("Lectura no disponible para esta lección.")

    # Fetch Lesson Object
    from database import Lesson
    from sqlmodel import select
    with get_session() as session:
        lesson_obj = session.exec(select(Lesson).where(Lesson.lesson_number == 11)).first()
        lesson = None
        if lesson_obj:
            lesson = {
                'id': lesson_obj.id,
                'lesson_number': lesson_obj.lesson_number,
                'title': lesson_obj.title,
                'content_markdown': lesson_obj.content_markdown,
            }
        
    if lesson:
        render_standard_gamified_lesson(lesson, theory_content, practice_content, reading_content)
    else:
        st.error("Error crítico: Lección 11 no encontrada en la base de datos.")

def render_lesson_12():
    def theory_content():
        st.markdown("""
        ## Lección 12: Los Pronombres
        """)
        
        if os.path.exists("static/images/curso_gramatica/leccion12_pronouns_demonstratives.png"):
            st.image("static/images/curso_gramatica/leccion12_pronouns_demonstratives.png",
                     caption="Pronombres Demostrativos: Hic, Ille, Is",
                     width="stretch")
                     
        st.markdown("""
        
        ### 1. Pronombres Personales
        
        Los pronombres personales se usan para referirse a personas sin nombrarlas.
        
        **Primera y Segunda Persona:**
        
        """
        )
    
        render_styled_table(
            ["Caso", "1a Sg (Yo)", "2a Sg (Tú)", "1a Pl (Nosotros)", "2a Pl (Vosotros)"],
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
        Solo existe para 3a persona (no hay formas de 1a y 2a, se usan *me, te*).
        
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
        
        Indican posesión. Se declinan como adjetivos de 1a Clase.
        
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
        
        """
        )
        
        if os.path.exists("static/images/curso_gramatica/leccion12_pronombres_heatmap.png"):
            st.image("static/images/curso_gramatica/leccion12_pronombres_heatmap.png",
                     caption="Mapa de Calor de Pronombres: Distancias Relativas (Hic, Iste, Ille)",
                     width="stretch")
                     
        st.markdown("""
        
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
        Es el demostrativo **neutro** y también se usa como pronombre personal de 3a persona.
        
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

        
        # Infografía Cultural: Estructura de la Familia Romana
        if os.path.exists("static/images/curso_gramatica/leccion12_familia_romana.png"):
            st.image("static/images/curso_gramatica/leccion12_familia_romana.png",
                     caption="La Familia Romana: Estructura Social y Jerarquía",
                     width="stretch")
    
    def practice_content():
        render_practice_content(12, mode="practice")

    def reading_content():
        from utils.reading_service import ReadingService
        with get_session() as session:
            reader = ReadingService(session)
            text = reader.get_reading_for_lesson(12)
            
            if text:
                st.markdown(f"#### {text.title}")
                enriched_html = reader.enrich_reading_with_tooltips(text.id)
                st.markdown(enriched_html, unsafe_allow_html=True)
            else:
                st.info("Lectura no disponible para esta lección.")

    # Fetch Lesson Object
    from database import Lesson
    from sqlmodel import select
    with get_session() as session:
        lesson_obj = session.exec(select(Lesson).where(Lesson.lesson_number == 12)).first()
        lesson = None
        if lesson_obj:
            lesson = {
                'id': lesson_obj.id,
                'lesson_number': lesson_obj.lesson_number,
                'title': lesson_obj.title,
                'content_markdown': lesson_obj.content_markdown,
            }
        
    if lesson:
        render_standard_gamified_lesson(lesson, theory_content, practice_content, reading_content)
    else:
        st.error("Error crítico: Lección 12 no encontrada en la base de datos.")

def render_lesson_13():
    def theory_content():
        st.markdown("""
        ## Lección 13: Voz Pasiva y el Ablativo
        """)
        
        st.image("static/images/curso_gramatica/passive_voice_diagram.png",
                 caption="La Voz Pasiva: Estructura y Formación",
                 width="stretch")
                 
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
                ["1a Sg", "-o/-m", "**-r**"],
                ["2a Sg", "-s", "**-ris**"],
                ["3a Sg", "-t", "**-tur**"],
                ["1a Pl", "-mus", "**-mur**"],
                ["2a Pl", "-tis", "**-mini**"],
                ["3a Pl", "-nt", "**-ntur**"]
            ]
        )
    
        st.markdown("""
        
        #### Presente Pasivo - Ejemplo: AMARE
        
        """
        )
    
        render_styled_table(
            ["Persona", "Activa", "Pasiva", "Traducción"],
            [
                ["1a Sg", "amo", "amo**r**", "yo soy amado"],
                ["2a Sg", "amas", "ama**ris** / ama**re**", "tú eres amado"],
                ["3a Sg", "amat", "ama**tur**", "él/ella es amado/a"],
                ["1a Pl", "amamus", "ama**mur**", "nosotros somos amados"],
                ["2a Sg", "amatis", "ama**mini**", "vosotros sois amados"],
                ["3a Pl", "amant", "ama**ntur**", "ellos/ellas son amados/as"]
            ]
        )
    
        st.markdown("""
        
        #### Imperfecto Pasivo
        *   *Amabar, amabaris, amabatur...* (Yo era amado, tú eras amado...)
        
        #### Futuro Pasívo (1a/2a Conj)
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
                 width="stretch")
        
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
        
        st.markdown("### 🧠 Mnemotecnia: Preposiciones")
        st.image("static/images/curso_gramatica/leccion13_preposiciones_completas.png",
                 caption="Guía Visual de Preposiciones (Acusativo vs Ablativo)",
                 width="stretch")
    
        st.image("static/images/curso_gramatica/leccion13_preposiciones_casos.png",
                 caption="Preposiciones de Lugar con sus Casos Gramaticales",
                 width="stretch")
        
        st.image("static/images/curso_gramatica/leccion13_decision_preposiciones.png",
                 caption="Diagrama de Decisión: ¿Qué Preposición Usar?",
                 width="stretch")
        
        st.markdown("""
        
        ### 3.5 EL LOCATIVO: Caso Especial para Ciudades
        
        El **Locativo** es un caso arcaico que sobrevive SOLO para:
        *   Nombres de **ciudades** y **pueblos**
        *   Nombres de **islas pequeñas**
        *   Las palabras **domus** (casa) y **rus** (campo)
        
        """)
        
        st.image("static/images/curso_gramatica/leccion13_locativo.png",
                 caption="El Locativo: Nombres de Ciudades e Islas Pequeñas",
                 width="stretch")
        
        st.markdown("""
        
        **Terminaciones del Locativo:**
        
        """)
        
        render_styled_table(
            ["Declinación", "Singular", "Plural", "Ejemplos"],
            [
                ["**1a Decl**", "-ae", "-is", "*Romae* (en Roma), *Athenis* (en Atenas)"],
                ["**2a Decl**", "-i", "-is", "*Corinthi* (en Corinto), *Delphi* (en Delfos)"],
                ["**3a Decl**", "-i / -e", "-ibus", "*Carthagine* (en Cartago)"]
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
        
        """)
        
        if os.path.exists("static/images/curso_gramatica/leccion13_geografia_militar.png"):
            st.image("static/images/curso_gramatica/leccion13_geografia_militar.png",
                     caption="Geografía Militar: Términos Estratégicos y Movimiento",
                     width="stretch")
        
        st.markdown("""
        ---
        
        ## COMPLEMENTOS CIRCUNSTANCIALES DE TIEMPO
        """)
        
        st.image("static/images/curso_gramatica/leccion13_complementos_tiempo.png",
                 caption="Esquema de los Complementos de Tiempo en Latín",
                 width="stretch")
        
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
                 width="stretch")
        
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
        
        """
        )
    
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
        
    def practice_content():
        render_practice_content(13, mode="practice")

    def reading_content():
        from utils.reading_service import ReadingService
        with get_session() as session:
            reader = ReadingService(session)
            text = reader.get_reading_for_lesson(13)
            
            if text:
                st.markdown(f"#### {text.title}")
                enriched_html = reader.enrich_reading_with_tooltips(text.id)
                st.markdown(enriched_html, unsafe_allow_html=True)
            else:
                st.info("Lectura no disponible para esta lección.")

    # Fetch Lesson Object
    from database import Lesson
    from sqlmodel import select
    with get_session() as session:
        lesson_obj = session.exec(select(Lesson).where(Lesson.lesson_number == 13)).first()
        lesson = None
        if lesson_obj:
            lesson = {
                'id': lesson_obj.id,
                'lesson_number': lesson_obj.lesson_number,
                'title': lesson_obj.title,
                'content_markdown': lesson_obj.content_markdown,
            }
        
    if lesson:
        render_standard_gamified_lesson(lesson, theory_content, practice_content, reading_content)
    else:
        st.error("Error crítico: Lección 13 no encontrada en la base de datos.")

def render_lesson_14():
    def theory_content():
        st.markdown("""
        ## Lección 14: Pluscuamperfecto y Futuro Perfecto
        """)
        
        if os.path.exists("static/images/curso_gramatica/leccion14_time_line.png"):
            st.image("static/images/curso_gramatica/leccion14_time_line.png",
                     caption="Línea de Tiempo: Relación entre los Tiempos de Perfectum",
                     width="stretch")
                     
        st.markdown("""
        
        ### 1. Pretérito Pluscuamperfecto: El Pasado del Pasado
        
        El **Pluscuamperfecto** indica una acción pasada que ocurrió **antes** de otra acción pasada.
        Equivale al español "había amado".
        
        **Formación**: Tema de Perfecto + **-eram, -eras, -erat...**
        
        > **Truco**: ¡Es el Tema de Perfecto + el Imperfecto de *SUM*!
        
        #### Paradigma: AMARE
        (Tema de Perfecto: *amav-*)
        
        """
        )
    
        render_styled_table(
            ["Persona", "Forma", "Traducción"],
            [
                ["1a Sg", "amav-**eram**", "yo había amado"],
                ["2a Sg", "amav-**eras**", "tú habías amado"],
                ["3a Sg", "amav-**erat**", "él/ella había amado"],
                ["1a Pl", "amav-**eramus**", "nosotros habíamos amado"],
                ["2a Pl", "amav-**eratis**", "vosotros habíais amado"],
                ["3a Pl", "amav-**erant**", "ellos/ellas habían amado"]
            ]
        )
    
        st.markdown("""
        
        #### Otros ejemplos con verbos irregulares:
        
        """
        )
    
        render_styled_table(
            ["Verbo", "Perfecto (3a Sg)", "Pluscuamperfecto (3a Sg)", "Traducción"],
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
        > excepto en la 3a persona plural: -erint (no -erunt)
        
        #### Paradigma: AMARE
        
        """
        )
    
        render_styled_table(
            ["Persona", "Forma", "Traducción"],
            [
                ["1a Sg", "amav-**ero**", "yo habré amado"],
                ["2a Sg", "amav-**eris**", "tú habrás amado"],
                ["3a Sg", "amav-**erit**", "él/ella habrá amado"],
                ["1a Pl", "amav-**erimus**", "nosotros habremos amado"],
                ["2a Pl", "amav-**eritis**", "vosotros habréis amado"],
                ["3a Pl", "amav-**erint**", "ellos/ellas habrán amado"]
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
        
        Conjuga en los tres tiempos los siguientes verbos (3a persona singular):
        
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
        
        # Infografía Cultural: El Calendario Romano
        if os.path.exists("static/images/curso_gramatica/leccion14_calendario_romano.png"):
            st.image("static/images/curso_gramatica/leccion14_calendario_romano.png",
                     caption="El Calendario Romano: Nombres de los Meses y Días",
                     width="stretch")
        
        # Infografía Cultural: Fiestas Religiosas Romanas
        st.markdown("### 🏛️ Cultura Romana: Las Grandes Fiestas Religiosas")
        st.info("El calendario romano estaba marcado por numerosas **fiestas religiosas** (*feriae*) en honor a los dioses.")
        if os.path.exists("static/images/curso_gramatica/cultura_fiestas_religiosas.png"):
            st.image("static/images/curso_gramatica/cultura_fiestas_religiosas.png",
                     caption="Las Principales Fiestas Religiosas Romanas: Saturnalia, Lupercalia, Floralia...",
                     width="stretch")
    
    def practice_content():
        render_practice_content(14, mode="practice")

    def reading_content():
        from utils.reading_service import ReadingService
        with get_session() as session:
            reader = ReadingService(session)
            text = reader.get_reading_for_lesson(14)
            
            if text:
                st.markdown(f"#### {text.title}")
                enriched_html = reader.enrich_reading_with_tooltips(text.id)
                st.markdown(enriched_html, unsafe_allow_html=True)
            else:
                st.info("Lectura no disponible para esta lección.")

    # Fetch Lesson Object
    from database import Lesson
    from sqlmodel import select
    with get_session() as session:
        lesson_obj = session.exec(select(Lesson).where(Lesson.lesson_number == 14)).first()
        lesson = None
        if lesson_obj:
            lesson = {
                'id': lesson_obj.id,
                'lesson_number': lesson_obj.lesson_number,
                'title': lesson_obj.title,
                'content_markdown': lesson_obj.content_markdown,
            }
        
    if lesson:
        render_standard_gamified_lesson(lesson, theory_content, practice_content, reading_content)
    else:
        st.error("Error crítico: Lección 14 no encontrada en la base de datos.")

def render_lesson_15():
    def theory_content():
        st.markdown("""
        ## Lección 15: Voz Pasiva - Sistema de Infectum
        """)
                 
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
            ["1a Sg", "-o / -m", "**-r** / **-or**"],
            ["2a Sg", "-s", "**-ris** / **-re**"],
            ["3a Sg", "-t", "**-tur**"],
            ["1a Pl", "-mus", "**-mur**"],
            ["2a Pl", "-tis", "**-mini**"],
            ["3a Pl", "-nt", "**-ntur**"]
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
            ["1a Sg", "amo", "am**or**", "yo soy amado/a"],
            ["2a Sg", "amas", "ama**ris** / ama**re**", "tú eres amado/a"],
            ["3a Sg", "amat", "ama**tur**", "él/ella es amado/a"],
            ["1a Pl", "amamus", "ama**mur**", "nosotros somos amados/as"],
            ["2a Sg", "amatis", "ama**mini**", "vosotros sois amados/as"],
            ["3a Pl", "amant", "ama**ntur**", "ellos/ellas son amados/as"]
        ]
    )

    st.markdown("""
    
    #### Segunda Conjugación: MONERE
    
    """
    )

    render_styled_table(
        ["Persona", "Pasiva", "Traducción"],
        [
            ["1a Sg", "mone**or**", "yo soy aconsejado/a"],
            ["2a Sg", "mone**ris**", "tú eres aconsejado/a"],
            ["3a Sg", "mone**tur**", "él/ella es aconsejado/a"],
            ["1a Pl", "mone**mur**", "nosotros somos aconsejados/as"],
            ["2a Sg", "mone**mini**", "vosotros sois aconsejados/as"],
            ["3a Pl", "mone**ntur**", "ellos/ellas son aconsejados/as"]
        ]
    )

    st.markdown("""
    
    #### Tercera Conjugación: LEGERE
    
    """
    )

    render_styled_table(
        ["Persona", "Pasiva", "Traducción"],
        [
            ["1a Sg", "leg**or**", "yo soy leído/a"],
            ["2a Sg", "lege**ris**", "tú eres leído/a"],
            ["3a Sg", "legi**tur**", "él/ella es leído/a"],
            ["1a Pl", "legi**mur**", "nosotros somos leídos/as"],
            ["2a Sg", "legi**mini**", "vosotros sois leídos/as"],
            ["3a Pl", "leg**untur**", "ellos/ellas son leídos/as"]
        ]
    )

    st.markdown("""
    
    #### Cuarta Conjugación: AUDIRE
    
    """
    )

    render_styled_table(
        ["Persona", "Pasiva", "Traducción"],
        [
            ["1a Sg", "audi**or**", "yo soy oído/a"],
            ["2a Sg", "audi**ris**", "tú eres oído/a"],
            ["3a Sg", "audi**tur**", "él/ella es oído/a"],
            ["1a Pl", "audi**mur**", "nosotros somos oídos/as"],
            ["2a Sg", "audi**mini**", "vosotros sois oídos/as"],
            ["3a Pl", "audi**untur**", "ellos/ellas son oídos/as"]
        ]
    )

    st.markdown("""
    
    ### 4. Imperfecto Pasivo
    
    **Formación**: Raíz + **vocal temática + -ba- + desinencias pasivas**
    
    #### Las Cuatro Conjugaciones:
    
    """
    )

    render_styled_table(
        ["Conjugación", "1a Sg", "2a Sg", "3a Sg", "Ejemplo"],
        [
            ["**1a**", "ama**bar**", "ama**baris**", "ama**batur**", "yo era amado"],
            ["**2a**", "mone**bar**", "mone**baris**", "mone**batur**", "yo era aconsejado"],
            ["**3a**", "lege**bar**", "lege**baris**", "lege**batur**", "yo era leído"],
            ["**4a**", "audie**bar**", "audie**baris**", "audie**batur**", "yo era oído"]
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
        ["Conjugación", "1a Sg", "2a Sg", "3a Sg"],
        [
            ["**1a**", "ama**bor**", "ama**beris**", "ama**bitur**"],
            ["**2a**", "mone**bor**", "mone**beris**", "mone**bitur**"]
        ]
    )

    st.markdown("""
    
    #### Tercera y Cuarta Conjugación: Vocal -E-/-I- 
    
    """
    )

    render_styled_table(
        ["Conjugación", "1a Sg", "2a Sg", "3a Sg"],
        [
            ["**3a**", "leg**ar**", "leg**eris**", "leg**etur**"],
            ["**4a**", "audi**ar**", "audi**eris**", "audi**etur**"]
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
    
    def practice_content():
        render_practice_content(15, mode="practice")

    def reading_content():
        from utils.reading_service import ReadingService
        with get_session() as session:
            reader = ReadingService(session)
            text = reader.get_reading_for_lesson(15)
            
            if text:
                st.markdown(f"#### {text.title}")
                enriched_html = reader.enrich_reading_with_tooltips(text.id)
                st.markdown(enriched_html, unsafe_allow_html=True)
            else:
                st.info("Lectura no disponible para esta lección.")

    # Fetch Lesson Object
    from database import Lesson
    from sqlmodel import select
    with get_session() as session:
        lesson_obj = session.exec(select(Lesson).where(Lesson.lesson_number == 15)).first()
        lesson = None
        if lesson_obj:
            lesson = {
                'id': lesson_obj.id,
                'lesson_number': lesson_obj.lesson_number,
                'title': lesson_obj.title,
                'content_markdown': lesson_obj.content_markdown,
            }
        
    if lesson:
        render_standard_gamified_lesson(lesson, theory_content, practice_content, reading_content)
    else:
        st.error("Error crítico: Lección 15 no encontrada en la base de datos.")

def render_lesson_16():
    def theory_content():
        st.markdown("""
        ## Lección 16: Voz Pasiva - Sistema de Perfectum
        """)
    
    if os.path.exists("static/images/curso_gramatica/leccion16_passive_perfect_system.png"):
        st.image("static/images/curso_gramatica/leccion16_passive_perfect_system.png",
                 caption="Formación del Sistema de Perfectum Pasivo",
                 width="stretch")
                 
    st.markdown("""
    
    ### El Participio Perfecto Pasivo
    
    La voz pasiva del Sistema de Perfectum se forma de manera **completamente diferente** 
    al Sistema de Infectum. No usa desinencias especiales, sino una **construcción perifrástica** 
    con el Participio Perfecto Pasivo.
    
    ### 1. El Participio Perfecto Pasivo (PPP)
    
    El **Participio Perfecto Pasivo** es un **adjetivo verbal** que se declina como 
    los adjetivos de 1a clase (*bonus, -a, -um*).
    
    **Formación**: Se forma sobre el **tema de supino** (4a forma del enunciado del verbo).
    
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
            ["1a Sg", "amat**us sum**", "yo fui amado / he sido amado"],
            ["2a Sg", "amat**us es**", "tú fuiste amado"],
            ["3a Sg", "amat**us est**", "él fue amado"],
            ["1a Pl", "amat**i sumus**", "nosotros fuimos amados"],
            ["2a Sg", "amat**i estis**", "vosotros fuisteis amados"],
            ["3a Pl", "amat**i sunt**", "ellos fueron amados"]
        ]
    )

    st.markdown("""
    
    #### Femenino y Neutro:
    *   Femenino Sg: *amata sum, amata es, amata est*
    *   Neutro Sg: *amatum est* (solo 3a persona, cosas)
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
            ["1a Sg", "amat**us eram**", "yo había sido amado"],
            ["2a Sg", "amat**us eras**", "tú habías sido amado"],
            ["3a Sg", "amat**us erat**", "él había sido amado"],
            ["1a Pl", "amat**i eramus**", "nosotros habíamos sido amados"],
            ["2a Sg", "amat**i eratis**", "vosotros habíais sido amados"],
            ["3a Pl", "amat**i erant**", "ellos habían sido amados"]
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
            ["1a Sg", "amat**us ero**", "yo habré sido amado"],
            ["2a Sg", "amat**us eris**", "tú habrás sido amado"],
            ["3a Sg", "amat**us erit**", "él habrá sido amado"],
            ["1a Pl", "amat**i erimus**", "nosotros habremos sido amados"],
            ["2a Sg", "amat**i eritis**", "vosotros habréis sido amados"],
            ["3a Pl", "amat**i erunt**", "ellos habrán sido amados"]
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
    """
    )
    
    # Infografía Cultural: Organización de las Legiones Romanas
    if os.path.exists("static/images/curso_gramatica/leccion16_legion_estructura.png"):
        st.image("static/images/curso_gramatica/leccion16_legion_estructura.png",
                 caption="La Legión Romana: Organización Militar del Imperio",
                 width="stretch")
    
    st.markdown("""
    *   **Video, videre, vidi, visum**: ver
    """)
    
    def practice_content():
        render_practice_content(16, mode="practice")

    def reading_content():
        from utils.reading_service import ReadingService
        with get_session() as session:
            reader = ReadingService(session)
            text = reader.get_reading_for_lesson(16)
            
            if text:
                st.markdown(f"#### {text.title}")
                enriched_html = reader.enrich_reading_with_tooltips(text.id)
                st.markdown(enriched_html, unsafe_allow_html=True)
            else:
                st.info("Lectura no disponible para esta lección.")

    # Fetch Lesson Object
    from database import Lesson
    from sqlmodel import select
    with get_session() as session:
        lesson_obj = session.exec(select(Lesson).where(Lesson.lesson_number == 16)).first()
        lesson = None
        if lesson_obj:
            lesson = {
                'id': lesson_obj.id,
                'lesson_number': lesson_obj.lesson_number,
                'title': lesson_obj.title,
                'content_markdown': lesson_obj.content_markdown,
            }
        
    if lesson:
        render_standard_gamified_lesson(lesson, theory_content, practice_content, reading_content)
    else:
        st.error("Error crítico: Lección 16 no encontrada en la base de datos.")

def render_lesson_17():
    st.markdown("""
    ## Lección 17: Verbos Deponentes y Semideponentes
    """)
    
    if os.path.exists("static/images/curso_gramatica/leccion17_deponent_verbs.png"):
        st.image("static/images/curso_gramatica/leccion17_deponent_verbs.png",
                 caption="Verbos Deponentes: Forma Pasiva, Significado Activo",
                 width="stretch")
                 
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
    - 1a forma: Presente Indicativo (1a persona singular)
    - 2a forma: Infinitivo Presente
    - 3a forma: Perfecto (PPP + sum)
    
    **Presente Indicativo**:
    
    """
    )

    render_styled_table(
        ["Persona", "Forma", "Traducción"],
        [
            ["1a Sg", "hort**or**", "yo exhorto"],
            ["2a Sg", "hort**āris** / hort**āre**", "tú exhortas"],
            ["3a Sg", "hort**ātur**", "él/ella exhorta"],
            ["1a Pl", "hort**āmur**", "nosotros exhortamos"],
            ["2a Sg", "hort**āmini**", "vosotros exhortáis"],
            ["3a Pl", "hort**antur**", "ellos/ellas exhortan"]
        ]
    )

    st.markdown("""
    
    #### Segunda Conjugación: VEREOR, VERERI, VERITUS SUM (temer, respetar)
    
    """
    )

    render_styled_table(
        ["Persona", "Presente", "Imperfecto", "Futuro"],
        [
            ["1a Sg", "vere**or**", "verē**bar**", "verē**bor**"],
            ["2a Sg", "verē**ris**", "verē**bāris**", "verē**beris**"],
            ["3a Sg", "verē**tur**", "verē**bātur**", "verē**bitur**"]
        ]
    )

    st.markdown("""
    
    #### Tercera Conjugación: SEQUOR, SEQUI, SECUTUS SUM (seguir)
    
    """
    )

    render_styled_table(
        ["Persona", "Presente", "Imperfecto", "Futuro"],
        [
            ["1a Sg", "sequ**or**", "sequē**bar**", "sequ**ar**"],
            ["2a Sg", "seque**ris**", "sequē**bāris**", "sequē**ris**"],
            ["3a Sg", "sequi**tur**", "sequē**bātur**", "sequē**tur**"]
        ]
    )

    st.markdown("""
    
    #### Cuarta Conjugación: LARGIOR, LARGIRI, LARGITUS SUM (regalar, conceder)
    
    """
    )

    render_styled_table(
        ["Persona", "Presente", "Imperfecto", "Futuro"],
        [
            ["1a Sg", "largi**or**", "largiē**bar**", "largi**ar**"],
            ["2a Sg", "largī**ris**", "largiē**bāris**", "largiē**ris**"],
            ["3a Sg", "largī**tur**", "largiē**bātur**", "largiē**tur**"]
        ]
    )

    st.markdown("""
    
    ### 3. Formación de Tiempos en Deponentes
    
    #### Sistema de Infectum (igual que pasiva regular):
    - **Presente**: Terminaciones pasivas
    - **Imperfecto**: -bar (pasivo)
    - **Futuro**: -bor (1a/2a conj) o -ar (3a/4a conj)
    
    #### Sistema de Perfectum (PPP + sum, como pasiva):
    - **Perfecto**: PPP + sum -> *secutus sum* (he seguido)
    - **Pluscuamperfecto**: PPP + eram -> *secutus eram* (había seguido)
    - **Futuro Perfecto**: PPP + ero -> *secutus ero* (habré seguido)
    
    ### 4. Deponentes Frecuentes e Importantes
    
    #### 1a Conjugación (-or, -ari, -atus sum):
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
    
    #### 2a Conjugación (-eor, -eri, -itus sum):
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
    
    #### 3a Conjugación (-or, -i, -us sum):
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
    
    #### 4a Conjugación (-ior, -iri, -itus sum):
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
       -> Los soldados **siguen** al jefe.
    
    2. *Cives de pace **loquebantur**.*
       -> Los ciudadanos **hablaban** sobre la paz.
    
    3. *Multi in bello **passi sunt**.*
       -> Muchos **sufrieron** en la guerra.
    
    4. *Philosophus sapienter **loquitur**.*
       -> El filósofo **habla** sabiamente.
    
    5. *Populus libertate **utitur**.*
       -> El pueblo **usa** la libertad.
    
    ### Vocabulario Esencial de Deponentes
    *   **sequor, sequi, secutus sum**: seguir
    *   **loquor, loqui, locutus sum**: hablar
    *   **patior, pati, passus sum**: sufrir
    *   **nascor, nasci, natus sum**: nacer
    *   **proficiscor, proficisci, profectus sum**: partir
    *   **utor, uti, usus sum**: usar (+ ablativo)
    *   **audeo, audere, ausus sum**: atreverse
    *   **gaudeo, gaudere, gavisus sum**: alegrarse
    """
    )
    
    # Infografía Cultural: Cursus Honorum - Magistraturas Romanas
    if os.path.exists("static/images/curso_gramatica/leccion17_cursus_honorum.png"):
        st.image("static/images/curso_gramatica/leccion17_cursus_honorum.png",
                 caption="El Cursus Honorum: La Carrera Política en la República Romana",
                 width="stretch")
    
    def practice_content():
        render_practice_content(17, mode="practice")

    def reading_content():
        from utils.reading_service import ReadingService
        with get_session() as session:
            reader = ReadingService(session)
            text = reader.get_reading_for_lesson(17)
            
            if text:
                st.markdown(f"#### {text.title}")
                enriched_html = reader.enrich_reading_with_tooltips(text.id)
                st.markdown(enriched_html, unsafe_allow_html=True)
            else:
                st.info("Lectura no disponible para esta lección.")

    # Fetch Lesson Object
    from database import Lesson
    from sqlmodel import select
    with get_session() as session:
        lesson_obj = session.exec(select(Lesson).where(Lesson.lesson_number == 17)).first()
        lesson = None
        if lesson_obj:
            lesson = {
                'id': lesson_obj.id,
                'lesson_number': lesson_obj.lesson_number,
                'title': lesson_obj.title,
                'content_markdown': lesson_obj.content_markdown,
            }
        
    if lesson:
        render_standard_gamified_lesson(lesson, theory_content, practice_content, reading_content)
    else:
        st.error("Error crítico: Lección 17 no encontrada en la base de datos.")

def render_lesson_18():
    def theory_content():
        st.image("static/images/lesson_18_subjunctive.png", caption="El Orador: Expresando deseos y posibilidades con el Subjuntivo", width="stretch")

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

    st.image("static/images/lesson_18_vowels.png", caption="Cambios Vocálicos en el Subjuntivo", width="stretch")

    st.markdown("""
    ### 1. Formación del Subjuntivo Presente

    **Regla general**: Cambiar la vocal temática
    
    #### 1a Conjugación: A -> E
    - Indicativo: am**a**-o, am**a**-s
    - Subjuntivo: am**e**-m, am**e**-s
    
    """
    )

    render_styled_table(
        ["Persona", "Indicativo", "Subjuntivo", "Traducción"],
        [
            ["1a Sg", "am**o**", "am**em**", "(que) yo ame"],
            ["2a Sg", "am**as**", "am**es**", "(que) tú ames"],
            ["3a Sg", "am**at**", "am**et**", "(que) él/ella ame"],
            ["1a Pl", "am**amus**", "am**emus**", "(que) nosotros amemos"],
            ["2a Sg", "am**atis**", "am**etis**", "(que) vosotros améis"],
            ["3a Pl", "am**ant**", "am**ent**", "(que) ellos/ellas amen"]
        ]
    )

    st.markdown("""
    
    #### 2a Conjugación: E -> EA
    - Indicativo: mon**e**-o, mon**e**-s
    - Subjuntivo: mon**ea**-m, mon**ea**-s
    
    """
    )

    render_styled_table(
        ["Persona", "Indicativo", "Subjuntivo"],
        [
            ["1a Sg", "mone**o**", "mone**am**"],
            ["2a Sg", "mone**s**", "mone**as**"],
            ["3a Sg", "mone**t**", "mone**at**"]
        ]
    )

    st.markdown("""
    
    #### 3a Conjugación: Consonante/E -> A
    - Indicativo: leg-**o**, leg-i**s**
    - Subjuntivo: leg-**a**-m, leg-**a**-s
    
    """
    )

    render_styled_table(
        ["Persona", "Indicativo", "Subjuntivo"],
        [
            ["1a Sg", "leg**o**", "leg**am**"],
            ["2a Sg", "leg**is**", "leg**as**"],
            ["3a Sg", "leg**it**", "leg**at**"]
        ]
    )

    st.markdown("""
    
    #### 4a Conjugación: I -> IA
    - Indicativo: aud**i**-o, aud**i**-s
    - Subjuntivo: aud**ia**-m, aud**ia**-s
    
    """
    )

    render_styled_table(
        ["Persona", "Indicativo", "Subjuntivo"],
        [
            ["1a Sg", "audi**o**", "audi**am**"],
            ["2a Sg", "audi**s**", "audi**as**"],
            ["3a Sg", "audi**t**", "audi**at**"]
        ]
    )

    st.markdown("### 🧠 Mnemotecnia: Vocales del Subjuntivo")
    st.image("static/images/curso_gramatica/leccion18_subjuntivo_vocales_regla.png",
             caption="Regla de Cambio Vocálico en el Subjuntivo",
             width="stretch")

    st.markdown("""
    
    ### 2. Sub juntivo de SUM
    
    **SUM** (ser/estar) tiene subjuntivo irregular:
    
    """
    )

    render_styled_table(
        ["Persona", "Indicativo", "Subjuntivo Presente"],
        [
            ["1a Sg", "sum", "**sim**"],
            ["2a Sg", "es", "**sis**"],
            ["3a Sg", "est", "**sit**"],
            ["1a Pl", "sumus", "**simus**"],
            ["2a Sg", "estis", "**sitis**"],
            ["3a Pl", "sunt", "**sint**"]
        ]
    )

    st.markdown("""
    
    ### 3. Formación del Subjuntivo Imperfecto
    
    **Regla universal**: Infinitivo presente + terminaciones personales activas (-m, -s, -t, -mus, -tis, -nt)
    
    #### Las Cuatro Conjugaciones:
    
    """
    )

    render_styled_table(
        ["Conjugación", "Infinitivo", "1a Sg", "2a Sg", "3a Sg"],
        [
            ["**1a**", "am**āre**", "amāre**m**", "amāre**s**", "amāre**t**"],
            ["**2a**", "mon**ēre**", "monēre**m**", "monēre**s**", "monēre**t**"],
            ["**3a**", "leg**ĕre**", "legĕre**m**", "legĕre**s**", "legĕre**t**"],
            ["**4a**", "aud**īre**", "audīre**m**", "audīre**s**", "audīre**t**"]
        ]
    )

    st.markdown("""
    
    **Paradigma completo de AMARE**:
    
    """
    )

    render_styled_table(
        ["Persona", "Subjuntivo Imperfecto", "Traducción"],
        [
            ["1a Sg", "amāre**m**", "(si) yo amara/amase"],
            ["2a Sg", "amāre**s**", "(si) tú amaras"],
            ["3a Sg", "amāre**t**", "(si) él amara"],
            ["1a Pl", "amārē**mus**", "(si) nosotros amáramos"],
            ["2a Sg", "amārē**tis**", "(si) vosotros amarais"],
            ["3a Pl", "amāre**nt**", "(si) ellos amaran"]
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
            ["1a Sg", "**essem**", "(si) yo fuera/fuese"],
            ["2a Sg", "**esses**", "(si) tú fueras"],
            ["3a Sg", "**esset**", "(si) él fuera"],
            ["1a Pl", "**essemus**", "(si) nosotros fuéramos"],
            ["2a Sg", "**essetis**", "(si) vosotros fuerais"],
            ["3a Pl", "**essent**", "(si) ellos fueran"]
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
    """)

    if os.path.exists("static/images/curso_gramatica/leccion18_subjuntivo_augur.png"):
        st.image("static/images/curso_gramatica/leccion18_subjuntivo_augur.png",
                 caption="El Augur: Interpretando la voluntad de los dioses (Subjuntivo Optativo)",
                 width="stretch")

    st.markdown("""
    #### B. Subjuntivo Yusivo / Exhortativo
    Expresa una **orden o exhortación** en 1a o 3a persona.
    
    *   ***Gaudeamus igitur!*** (¡Alegrémonos, pues!)
    *   ***Veniat!*** (¡Que venga!)
    *   ***Ne timeas!*** (¡No temas!)
    
    **Negación**: *ne*
    
    #### C. Subjuntivo Dubitativo (Deliberativo)
    Expresa **duda** en forma interrogativa.
    
    *   ***Quid faciam?*** (¿Qué debo hacer? / ¿Qué haga?)
    *   ***Quo eam?*** (¿A dónde voy? / ¿A dónde vaya?)
    
    """)

    st.image("static/images/lesson_18_potential.png", caption="El Subjuntivo Potencial: Imaginando posibilidades", width="stretch")

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
        ["Verbo", "Presente (3a Sg)", "Imperfecto (3a Sg)"],
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
       -> ¡Ojalá vivieras!
    
    2. *Gaudeamus omnes!*
       -> ¡Alegrémonos todos!
    
    3. *Veniat Caesar.*
       -> Que venga César.
    
    4. *Quid agam?*
       -> ¿Qué debo hacer?
    
    5. *Ne timeas.*
       -> No temas.
    
    ### Vocabulario Esencial
    *   **utinam**: ojalá
    *   **ne**: no (en subjuntivo)
    *   **quid**: qué
    *   **quo**: a dónde
    *   **cur**: por qué
    *   **ut**: que (afirmativo)
    """)
    
    def practice_content():
        render_practice_content(18, mode="practice")

    def reading_content():
        from utils.reading_service import ReadingService
        with get_session() as session:
            reader = ReadingService(session)
            text = reader.get_reading_for_lesson(18)
            
            if text:
                st.markdown(f"#### {text.title}")
                enriched_html = reader.enrich_reading_with_tooltips(text.id)
                st.markdown(enriched_html, unsafe_allow_html=True)
            else:
                st.info("Lectura no disponible para esta lección.")

    # Fetch Lesson Object
    from database import Lesson
    from sqlmodel import select
    with get_session() as session:
        lesson_obj = session.exec(select(Lesson).where(Lesson.lesson_number == 18)).first()
        lesson = None
        if lesson_obj:
            lesson = {
                'id': lesson_obj.id,
                'lesson_number': lesson_obj.lesson_number,
                'title': lesson_obj.title,
                'content_markdown': lesson_obj.content_markdown,
            }
        
    if lesson:
        render_standard_gamified_lesson(lesson, theory_content, practice_content, reading_content)
    else:
        st.error("Error crítico: Lección 18 no encontrada en la base de datos.")

def render_lesson_19():
    def theory_content():
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
            ["1a Sg", "amav**erim**", "(que) yo haya amado"],
            ["2a Sg", "amav**eris**", "(que) tú hayas amado"],
            ["3a Sg", "amav**erit**", "(que) él haya amado"],
            ["1a Pl", "amav**erimus**", "(que) nosotros hayamos amado"],
            ["2a Pl", "amav**eritis**", "(que) vosotros hayáis amado"],
            ["3a Pl", "amav**erint**", "(que) ellos hayan amado"]
        ]
    )

    st.markdown("""
    
    > **Nota**: Es casi idéntico al Futuro Perfecto Indicativo, excepto en 1a Sg: 
    > - Fut. Perfecto: amav**ero**
    > - Subj. Perfecto: amav**erim**
    
    #### Otras Conjugaciones (3a persona singular):
    
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
            ["1a Sg", "amavisse**m**", "(si) yo hubiera/hubiese amado"],
            ["2a Sg", "amavisse**s**", "(si) tú hubieras amado"],
            ["3a Sg", "amavisse**t**", "(si) él hubiera amado"],
            ["1a Pl", "amavisē**mus**", "(si) nosotros hubiéramos amado"],
            ["2a Sg", "amavisē**tis**", "(si) vosotros hubierais amado"],
            ["3a Pl", "amavisse**nt**", "(si) ellos hubieran amado"]
        ]
    )

    st.markdown("""
    
    #### Otras Conjugaciones (3a Sg):
    
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
        ["Tiempo", "Formación", "Ejemplo (1a Sg)", "Traducción"],
        [
            ["**Presente**", "Vocal temática cambiada", "am**em**", "(que) yo ame"],
            ["**Imperfecto**", "Infinitivo presente + -m", "amāre**m**", "(si) yo amara"],
            ["**Perfecto**", "Tema perfecto + -erim", "amav**erim**", "(que) yo haya amado"],
            ["**Pluscuamperfecto**", "Inf. perfecto + -m", "amavisse**m**", "(si) yo hubiera amado"]
        ]
    )

    st.markdown("""
    
    """)

    st.image("static/images/lesson_19_timeline.png", caption="Línea Temporal: La relación entre tiempos verbales", width="stretch")

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
    *   *Rogo **ut venias**.* (Te pido que vengas) - Simultaneidad -> Pres. Subj.
    *   *Rogo **ut veneris**.* (Te pido que hayas venido) - Anterioridad -> Perf. Subj.
    
    **Principal Histórica**:
    *   *Rogavi **ut venīres**.* (Te pedí que vinieras) - Simultaneidad -> Imp. Subj.
    *   *Rogavi **ut venisses**.* (Te pedí que hubieras venido) - Anterioridad -> Plusc. Subj.
    
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

    st.image("static/images/lesson_19_structure.png", caption="Estructura de la Consecutio Temporum", width="stretch")

    st.markdown("""
    """)

    if os.path.exists("static/images/curso_gramatica/leccion19_consecutio_temporum_diagram.png"):
        st.image("static/images/curso_gramatica/leccion19_consecutio_temporum_diagram.png",
                 caption="Tabla Maestra de Consecutio Temporum",
                 width="stretch")
    elif os.path.exists("static/images/curso_gramatica/leccion19_consecutio_temporum.png"):
        st.image("static/images/curso_gramatica/leccion19_consecutio_temporum.png",
                 caption="Esquema de la Consecutio Temporum",
                 width="stretch")

    st.markdown("""
    ### 8. Ejercicios de Aplicación
    
    Completa con el tiempo correcto del subjuntivo:
    
    1. *Rogo ut ______ (venire).*
       -> **venias** (Principal presente -> Pres. Subj.)
    
    2. *Rogavi ut ______ (venire).*
       -> **venīres** (Principal perfecto -> Imp. Subj.)
    
    3. *Timeo ne hoc ______ (facere) iam.*
       -> **fecerit** (Anterioridad + Principal pres. -> Perf. Subj.)
    
    4. *Si hoc ______ (facere), felix ______ (esse).*
       -> **faceres**, **esses** (Condicional irreal presente)
    
    5. *Tam sapienter loquitur ut omnes eum ______ (audire).*
       -> **audiant** (Consecutiva + Principal pres. -> Pres. Subj.)
    
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
    *   **quamvis**: aunque (+ subjuntivo)
    """)
    
    # Infografía Cultural: El Senado Romano
    if os.path.exists("static/images/curso_gramatica/leccion19_senado_discurso.png"):
        st.image("static/images/curso_gramatica/leccion19_senado_discurso.png",
                 caption="El Senado Romano: Oratoria y Debate Político",
                 width="stretch")
    
    def practice_content():
        render_practice_content(19, mode="practice")

    def reading_content():
        from utils.reading_service import ReadingService
        with get_session() as session:
            reader = ReadingService(session)
            text = reader.get_reading_for_lesson(19)
            
            if text:
                st.markdown(f"#### {text.title}")
                enriched_html = reader.enrich_reading_with_tooltips(text.id)
                st.markdown(enriched_html, unsafe_allow_html=True)
            else:
                st.info("Lectura no disponible para esta lección.")

    # Fetch Lesson Object
    from database import Lesson
    from sqlmodel import select
    with get_session() as session:
        lesson_obj = session.exec(select(Lesson).where(Lesson.lesson_number == 19)).first()
        lesson = None
        if lesson_obj:
            lesson = {
                'id': lesson_obj.id,
                'lesson_number': lesson_obj.lesson_number,
                'title': lesson_obj.title,
                'content_markdown': lesson_obj.content_markdown,
            }
        
    if lesson:
        render_standard_gamified_lesson(lesson, theory_content, practice_content, reading_content)
    else:
        st.error("Error crítico: Lección 19 no encontrada en la base de datos.")

def render_lesson_20():
    def theory_content():
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
                 width="stretch")

    st.markdown("""
    El latín tiene infinitivos para **tres tiempos** (Presente, Perfecto, Futuro) y **dos voces** (Activa, Pasiva).
    
    #### A. Infinitivo Presente (Simultaneidad)
    """)
    
    render_styled_table(
        ["Conjugación", "Activa", "Pasiva", "Traducción (Act/Pas)"],
        [
            ["**1a (amare)**", "amā**re**", "amā**ri**", "amar / ser amado"],
            ["**2a (monere)**", "monē**re**", "monē**ri**", "aconsejar / ser aconsejado"],
            ["**3a (legere)**", "leg**ĕre**", "leg**i**", "leer / ser leído"],
            ["**4a (audire)**", "audī**re**", "audī**ri**", "oír / ser oído"],
            ["**Mixta (capere)**", "cap**ĕre**", "cap**i**", "tomar / ser tomado"]
        ]
    )

    st.markdown("""
    
    > **¡Ojo a la 3a conjugación pasiva!** Termina en **-i** (no -eri). *Legi*, *duci*, *mitti*.
    
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
        *   -> **Tales dijo que el agua era el principio de todas las cosas.**
    
    2.  *Sentio vos laetos esse.*
        *   -> Siento que vosotros estáis contentos.
    
    3.  *Credimus Romam aeternam fore (= futuram esse).*
        *   -> Creemos que Roma será eterna.
    
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
    
    # Infografía Cultural: Filosofía Romana
    if os.path.exists("static/images/curso_gramatica/leccion20_filosofia_romana.png"):
        st.image("static/images/curso_gramatica/leccion20_filosofia_romana.png",
                 caption="Escuelas Filosóficas Romanas: Estoicismo, Epicureísmo y Eclecticismo",
                 width="stretch")
    
    # Infografía Cultural: Teatro Romano
    st.markdown("### 🎭 Cultura Romana: El Teatro")
    st.info("Los géneros teatrales romanos se expresaban con infinitivos y oraciones de AcI en las obras.")
    if os.path.exists("static/images/curso_gramatica/cultura_teatro_romano.png"):
        st.image("static/images/curso_gramatica/cultura_teatro_romano.png",
                 caption="El Teatro Romano: Tragoedia, Comoedia, géneros y dramaturgos",
                 width="stretch")

    def practice_content():
        # render_practice_content handles static exercises automatically
        render_practice_content(20, mode="practice")

    def reading_content():
        from utils.reading_service import ReadingService
        with get_session() as session:
            reader = ReadingService(session)
            text = reader.get_reading_for_lesson(20)
            
            if text:
                st.markdown(f"#### {text.title}")
                enriched_html = reader.enrich_reading_with_tooltips(text.id)
                st.markdown(enriched_html, unsafe_allow_html=True)
            else:
                st.info("Lectura no disponible para esta lección.")

    # Fetch Lesson Object
    from database import Lesson
    from sqlmodel import select
    with get_session() as session:
        lesson_obj = session.exec(select(Lesson).where(Lesson.lesson_number == 20)).first()
        lesson = None
        if lesson_obj:
            lesson = {
                'id': lesson_obj.id,
                'lesson_number': lesson_obj.lesson_number,
                'title': lesson_obj.title,
                'content_markdown': lesson_obj.content_markdown,
            }
        
    if lesson:
        render_standard_gamified_lesson(lesson, theory_content, practice_content, reading_content)
    else:
        st.error("Error crítico: Lección 20 no encontrada en la base de datos.")


def render_lesson_21():
    def theory_content():
        st.markdown("""
        ## Leccion 21: Los Participios
        
        ### 1. ¿Que es un Participio?
        
        El participio es un **adjetivo verbal**: una forma hibrida que combina caracteristicas de verbo y adjetivo.
        *   Como **adjetivo**: concuerda en Genero, Numero y Caso con un sustantivo.
        *   Como **verbo**: tiene Tiempo y Voz, y puede regir complementos (OD, circunstanciales, etc.).
        
        > En espanol tenemos "amado" (pasivo) y "amante" (activo), pero el latin tiene un sistema mucho mas completo.
        
        ### 2. El Sistema de Participios Latino
        
        El latin tiene **TRES participios** que cubren todas las combinaciones de tiempo y voz:
        
        """)
        
        render_styled_table(
            ["Participio", "Tiempo", "Voz", "Formacion", "Ejemplo (AMARE)"],
            [
                ["**Presente**", "Presente", "Activa", "Tema + **-ns, -ntis**", "*ama-**ns**, ama-**ntis***"],
                ["**Perfecto**", "Pasado", "Pasiva", "Tema Supino + **-us, -a, -um**", "*ama-**tus, -a, -um***"],
                ["**Futuro**", "Futuro", "Activa", "Tema Supino + **-urus, -a, -um**", "*ama-**turus, -a, -um***"]
            ]
        )
        
        st.markdown("""
        
        ### 3. Participio Presente Activo (-ns, -ntis)
        
        Indica una accion **simultanea** con la accion principal.
        Se declina como adjetivo de 3a declinacion (una terminacion).
        
        **Formacion**:
        *   1a/2a Conjugacion: Tema + **-ns** -> *amans, monens*
        *   3a Conjugacion: Tema + **-ens** -> *legens*
        *   4a Conjugacion: Tema + **-iens** -> *audiens*
        
        **Declinacion** (Modelo: *amans, amantis* - que ama / amante):
        
        """)
        
        render_styled_table(
            ["Caso", "Masc/Fem Sg", "Neutro Sg", "Masc/Fem Pl", "N Pl"],
            [
                ["**Nom**", "ama**ns**", "ama**ns**", "ama**ntes**", "ama**ntia**"],
                ["**Ac**", "ama**ntem**", "ama**ns**", "ama**ntes**", "ama**ntia**"],
                ["**Gen**", "ama**ntis**", "ama**ntis**", "ama**ntium**", "ama**ntium**"],
                ["**Dat**", "ama**nti**", "ama**nti**", "ama**ntibus**", "ama**ntibus**"],
                ["**Abl**", "ama**nte/-i**", "ama**nte/-i**", "ama**ntibus**", "ama**ntibus**"]
            ]
        )
        
        st.markdown("""
        
        **Ejemplos**:
        *   *Puer **currens** cadit.* (El nino, **corriendo**, cae / El nino **que corre** cae).
        *   *Milites **pugnantes** vicerunt.* (Los soldados **que luchaban** vencieron).
        *   *Video puellam **canentem**.* (Veo a la nina **que canta**).
        
        ### 4. Participio Perfecto Pasivo (-tus, -a, -um)
        
        Indica una accion **anterior** a la accion principal, con sentido **pasivo**.
        Se declina como adjetivo de 1a Clase (2-1-2: *bonus, -a, -um*).
        
        **Formacion**: Se forma del **tema de supino** (4a forma del enunciado):
        *   *Amare, amavi, **amatum*** -> *ama**tus**, -a, -um* (amado/a)
        *   *Legere, legi, **lectum*** -> *lec**tus**, -a, -um* (leido/a)
        *   *Capere, cepi, **captum*** -> *cap**tus**, -a, -um* (capturado/a)
        
        **Ejemplos**:
        *   *Urbs, ab hostibus **capta**, incensa est.*
            *   La ciudad, **capturada** por los enemigos, fue incendiada.
            *   (Primero fue capturada, luego incendiada)
        *   *Poeta, a rege **laudatus**, felix erat.*
            *   El poeta, **alabado** por el rey, era feliz.
        *   *Liber **lectus** bonus est.*
            *   El libro **leido** es bueno.
        
        ### 5. Participio Futuro Activo (-urus, -a, -um)
        
        Indica **intencion** o **accion futura** respecto a la principal.
        Se declina como adjetivo de 1a Clase.
        
        **Formacion**: Tema de supino + **-urus, -a, -um**:
        *   *Amare* -> *ama**turus**, -a, -um* (que va a amar / a punto de amar)
        *   *Legere* -> *lec**turus**, -a, -um* (que va a leer)
        *   *Mori* -> *mori**turus**, -a, -um* (que va a morir)
        
        **Ejemplos**:
        *   ***Ave, Caesar, morituri te salutant.***
            *   Salve, Cesar, **los que van a morir** te saludan.
            *   (Frase famosa de los gladiadores)
        *   *Nuntii **venturi** sunt.*
            *   Los mensajeros **estan a punto de llegar**.
        
        ### 6. Traduccion de Participios al Espanol
        
        Los participios latinos se pueden traducir de varias formas:
        
        1.  **Como participio** (cuando existe): "amado", "corriendo"
        2.  **Como oracion de relativo**: "que ama", "que fue amado"
        3.  **Como oracion adverbial**:
            *   Temporal: "cuando ama", "despues de ser amado"
            *   Causal: "porque ama", "como fue amado"
            *   Concesiva: "aunque ama"
        
        **Ejemplo de multiples traducciones**:
        *Consul, **urbem videns**, laetus erat.*
        
        *   El consul, **viendo la ciudad**, estaba contento. (Gerundio)
        *   El consul, **que veia la ciudad**, estaba contento. (Relativo)
        *   El consul, **cuando vio la ciudad**, estaba contento. (Temporal)
        *   El consul, **porque veia la ciudad**, estaba contento. (Causal)
        
        ### Vocabulario Esencial
        *   **Curro, currere**: correr
        *   **Pugno, pugnare**: luchar
        *   **Cano, canere**: cantar
        *   **Incendo, incendere**: incendiar, quemar
        *   **Laudo, laudare**: alabar
        *   **Saluto, salutare**: saludar
        
        """)
        
        if os.path.exists("static/images/curso_gramatica/leccion21_participios.png"):
            st.image("static/images/curso_gramatica/leccion21_participios.png",
                     caption="Sistema de Participios Latinos: Presente, Perfecto y Futuro",
                     width="stretch")
    
    
    def practice_content():
        render_practice_content(21, mode="practice")

    def reading_content():
        from utils.reading_service import ReadingService
        with get_session() as session:
            reader = ReadingService(session)
            text = reader.get_reading_for_lesson(21)
            
            if text:
                st.markdown(f"#### {text.title}")
                enriched_html = reader.enrich_reading_with_tooltips(text.id)
                st.markdown(enriched_html, unsafe_allow_html=True)
            else:
                st.info("Lectura no disponible para esta lección.")

    # Fetch Lesson Object
    from database import Lesson
    from sqlmodel import select
    with get_session() as session:
        lesson_obj = session.exec(select(Lesson).where(Lesson.lesson_number == 21)).first()
        lesson = None
        if lesson_obj:
            lesson = {
                'id': lesson_obj.id,
                'lesson_number': lesson_obj.lesson_number,
                'title': lesson_obj.title,
                'content_markdown': lesson_obj.content_markdown,
            }
        
    if lesson:
        render_standard_gamified_lesson(lesson, theory_content, practice_content, reading_content)
    else:
        st.error("Error crítico: Lección 21 no encontrada en la base de datos.")


def render_lesson_22():
    def theory_content():
        st.markdown("""
        ## Leccion 22: El Ablativo Absoluto
        
        ### 1. La Construccion Reina del Latin
        
        El **Ablativo Absoluto** es una construccion sintactica fundamental y muy frecuente en latin clasico.
        Equivale a una **oracion subordinada circunstancial** (temporal, causal, concesiva, condicional).
        
        Se llama "absoluto" (*absolutus* = desatado, suelto) porque gramaticalmente esta **desligado** de la oracion principal:
        *   Su sujeto NO es el sujeto de la principal.
        *   Su sujeto NO es el objeto de la principal.
        *   Funciona como un complemento circunstancial independiente.
        
        ### 2. Estructura Basica
        
        Se compone de **DOS elementos en caso ABLATIVO**:
        
        1.  **Sujeto** (Sustantivo o Pronombre en Ablativo)
        2.  **Predicado** (Participio, Adjetivo o Sustantivo en Ablativo)
        
        **Formula**: **[Sust. Ablativo] + [Participio/Adj/Sust Ablativo]**
        
        ### 3. Tipos de Ablativo Absoluto
        
        """)

        # Infografía de Ablativo Absoluto
        if os.path.exists("static/images/curso_gramatica/leccion22_ablativo_absoluto.png"):
             st.image("static/images/curso_gramatica/leccion22_ablativo_absoluto.png",
                      caption="El Ablativo Absoluto: Estructura y Tipos",
                      width="stretch")
        
        render_styled_table(
            ["Tipo", "Estructura", "Significado", "Ejemplo"],
            [
                ["**Con Part. Presente**", "Abl + Part. Pres", "Simultaneidad", "*Sole **oriente*** (Saliendo el sol)"],
                ["**Con Part. Perfecto**", "Abl + Part. Perf", "Anterioridad", "*Urbe **capta*** (Capturada la ciudad)"],
                ["**Nominal**", "Abl + Sust/Adj", "Estado/Circunstancia", "*Me **consule*** (Siendo yo consul)"]
            ]
        )
        
        st.markdown("""
        
        ### 4. Ablativo Absoluto con Participio Presente
        
        Expresa una **accion simultanea** a la principal.
        
        **Ejemplos**:
        *   *Sole **oriente**, aves canunt.*
            *   **Saliendo el sol** / **Al salir el sol**, las aves cantan.
            *   (= Cuando sale el sol)
        
        *   *Caesare **duce**, Romani vincebant.*
            *   **Siendo Cesar el jefe** / **Bajo el mando de Cesar**, los romanos vencian.
        
        *   *Me **tacente**, tu loquebaris.*
            * **Callando yo** / **Mientras yo callaba**, tu hablabas.
        
        ### 5. Ablativo Absoluto con Participio Perfecto
        
        Expresa una **accion anterior** a la principal (la mas comun).
        
        **Ejemplos**:
        *   *Urbe **capta**, hostes redierunt.*
            *   **Capturada la ciudad** / **Despues de capturar la ciudad**, los enemigos regresaron.
            *   (Primero capturaron, luego regresaron)
        
        *   *His rebus **cognitis**, Caesar exercitum movit.*
            *   **Conocidas estas cosas** / **Cuando supo esto**, Cesar movio el ejercito.
        
        *   *Romulo **regnante**, urbs condita est.*
            *   **Reinando Romulo** / **En el reinado de Romulo**, la ciudad fue fundada.
        
        ### 6. Ablativo Absoluto Nominal (sin Participio)
        
        Cuando NO hay participio, se sobreentiende el verbo **SUM** ("ser/estar").
        
        **Estructura**: Sustantivo/Pronombre + Sustantivo/Adjetivo (ambos en Ablativo)
        
        **Ejemplos**:
        *   *Me **consule**, pax erat.*
            *   **Siendo yo consul** / **Durante mi consulado**, habia paz.
            *   (= Cum ego consul essem)
        
        *   *Cicerone **oratore**, Romani eloquentes erant.*
            *   **Siendo Ciceron orador** / **Con Ciceron como orador**, los romanos eran elocuentes.
        
        *   ***Vivo** patre, felix sum.*
            *   **Viviendo el padre** / **Estando vivo el padre**, soy feliz.
        
        ### 7. Como Traducir el Ablativo Absoluto
        
        El Ablativo Absoluto puede tener diversos matices y traducirse de varias formas:
        
        """)
        
        render_styled_table(
            ["Matiz", "Conjuncion Espanola", "Ejemplo Traduccion"],
            [
                ["**Temporal**", "Cuando, Al, Mientras", "**Cuando** el sol salia..."],
                ["**Causal**", "Como, Porque, Ya que", "**Como** la ciudad fue capturada..."],
                ["**Concesivo**", "Aunque", "**Aunque** el padre vivia..."],
                ["**Condicional**", "Si", "**Si** el consul hubiera muerto..."]
            ]
        )
        
        st.markdown("""
        
        ### 8. Diferencia con el Participio Concertado
        
        Es crucial NO confundir:
        
        **Participio Concertado**: El participio concuerda con un elemento de la oracion principal (Sujeto, OD, etc.)
        *   *Consul, **urbem videns**, laetus erat.*
        *   El consul, **viendo la ciudad**, estaba contento.
        *   (*videns* concuerda con *consul*, que es el sujeto)
        
        **Ablativo Absoluto**: El participio esta en Ablativo con su propio sujeto, separado de la principal.
        *   ***Sole oriente**, consul laetus erat.*
        *   **Al salir el sol**, el consul estaba contento.
        *   (*oriente* esta con *sole*, en Ablativo, independiente de *consul*)
        
        ### 9. Ejercicios de Analisis
        
        Identifica y traduce:
        
        1.  *Romanis **pugnan tibus**, hostes fugerunt.*
            *   Ablativo Absoluto con Participio Presente.
            *   **Luchando los romanos** / **Mientras los romanos luchaban**, los enemigos huyeron.
        
        2.  *Caesare **mortuo**, Marcus consul factus est.*
            *   Ablativo Absoluto con Participio Perfecto.
            *   **Muerto Cesar** / **Despues de morir Cesar**, Marco fue hecho consul.
        
        3.  *Te **duce**, vincere possumus.*
            *   Ablativo Absoluto Nominal (sin participio, se sobreentiende *sum*).
            *   **Siendo tu el jefe** / **Contigo como jefe**, podemos vencer.
        
        4.  *Omnibus **audientibus**, orator dixit.*
            *   Ablativo Absoluto con Participio Presente.
            *   **Escuchando todos** / **Mientras todos escuchaban**, el orador hablo.
        
        ### Vocabulario Esencial
        *   **Orior, oriri, ortus sum**: salir, levantarse (el sol)
        *   **Dux, ducis** (m): jefe, general
        *   **Taceo, tacere**: callar
        *   **Loquor, loqui**: hablar (deponente)
        *   **Cognosco, cognoscere, cognovi**: conocer, enterarse
        *   **Moveo, movere**: mover
        *   **Exercitus, -us** (m): ejercito
        *   **Eloquens, -entis**: elocuente
        
        """)
        
        if os.path.exists("static/images/curso_gramatica/leccion22_ablativo_absoluto.png"):
            st.image("static/images/curso_gramatica/leccion22_ablativo_absoluto.png",
                     caption="El Ablativo Absoluto: Estructura y Tipos",
                     width="stretch")
    
    
    def practice_content():
        render_practice_content(22, mode="practice")

    def reading_content():
        from utils.reading_service import ReadingService
        with get_session() as session:
            reader = ReadingService(session)
            text = reader.get_reading_for_lesson(22)
            
            if text:
                st.markdown(f"#### {text.title}")
                enriched_html = reader.enrich_reading_with_tooltips(text.id)
                st.markdown(enriched_html, unsafe_allow_html=True)
            else:
                st.info("Lectura no disponible para esta lección.")

    # Fetch Lesson Object
    from database import Lesson
    from sqlmodel import select
    with get_session() as session:
        lesson_obj = session.exec(select(Lesson).where(Lesson.lesson_number == 22)).first()
        lesson = None
        if lesson_obj:
            lesson = {
                'id': lesson_obj.id,
                'lesson_number': lesson_obj.lesson_number,
                'title': lesson_obj.title,
                'content_markdown': lesson_obj.content_markdown,
            }
        
    if lesson:
        render_standard_gamified_lesson(lesson, theory_content, practice_content, reading_content)
    else:
        st.error("Error crítico: Lección 22 no encontrada en la base de datos.")



def render_lesson_23():
    def theory_content():
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
                     width="stretch")
        
        st.markdown("""
        ### 2. El Gerundio (Sustantivo Verbal)
        
        El Gerundio sirve para **declinar el infinitivo**.
        El infinitivo (*amare*) se usa como Nominativo. Para los demás casos, usamos el Gerundio.
        
        **Formación**: Tema de presente + **-nd-** + terminaciones de segunda declinación neutra singular.
        
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
        
        El Gerundivo es un **adjetivo de la primera clase** (*-ndus, -nda, -ndum*).
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
            *   -> Tiempo **de leer**.
        
        2.  *Ad **pacem petendam** venerunt.*
            *   **Gerundivo**. *Petendam* concuerda con *pacem* (Acusativo Fem. Sing).
            *   -> Vinieron **para pedir la paz**.
        
        3.  *In **libro legendo**.*
            *   **Gerundivo**. *Legendo* concuerda con *libro* (Ablativo Masc. Sing).
            *   -> **Al leer el libro** (En el libro que debe ser leído).
        
        ### Vocabulario Esencial
        *   **Cupidus, -a, -um**: deseoso (+ Gen)
        *   **Peritus, -a, -um**: experto (+ Gen)
        *   **Ad**: para (+ Acusativo)
        *   **Causa / Gratia**: por causa de, para (+ Genitivo)
        """)
    
    def practice_content():
        render_practice_content(23, mode="practice")

    def reading_content():
        from utils.reading_service import ReadingService
        with get_session() as session:
            reader = ReadingService(session)
            text = reader.get_reading_for_lesson(23)
            
            if text:
                st.markdown(f"#### {text.title}")
                enriched_html = reader.enrich_reading_with_tooltips(text.id)
                st.markdown(enriched_html, unsafe_allow_html=True)
            else:
                st.info("Lectura no disponible para esta lección.")

    # Fetch Lesson Object
    from database import Lesson
    from sqlmodel import select
    with get_session() as session:
        lesson_obj = session.exec(select(Lesson).where(Lesson.lesson_number == 23)).first()
        lesson = None
        if lesson_obj:
            lesson = {
                'id': lesson_obj.id,
                'lesson_number': lesson_obj.lesson_number,
                'title': lesson_obj.title,
                'content_markdown': lesson_obj.content_markdown,
            }
        
    if lesson:
        render_standard_gamified_lesson(lesson, theory_content, practice_content, reading_content)
    else:
        st.error("Error crítico: Lección 23 no encontrada en la base de datos.")

def render_lesson_24():
    def theory_content():
        st.markdown("""
        ## Lección 24: Conjugaciones Perifrásticas
        
        ### 1. ¿Qué es una Perifrástica?
        
        Una conjugación perifrástica es un rodeo ("perífrasis") para expresar matices que los tiempos normales no tienen, como **intención** o **obligación**.
        
        Se forman con un **Participio** + el verbo **SUM**.
        
        """)
        
        if os.path.exists("static/images/curso_gramatica/leccion24_perifrastica.png"):
            st.image("static/images/curso_gramatica/leccion24_perifrastica.png",
                     caption="Conjugaciones Perifrásticas: Activa vs Pasiva",
                     width="stretch")
        
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
            *   -> **Hay que leer** este libro.
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
            *   -> **Debemos destruir** Cartago.
        
        ### 5. Ejercicios de Traducción
        
        Traduce estas oraciones con matiz de obligación o intención:
        
        1.  *Bellum **gesturi sumus**.*
            *   Perifrástica Activa (Part. Futuro).
            *   -> **Vamos a hacer** la guerra / Tenemos intención de hacer la guerra.
        
        2.  *Pacta **servanda sunt**.*
            *   Perifrástica Pasiva (Gerundivo).
            *   -> Los pactos **deben ser cumplidos** (o conservados).
        
        3.  *Hoc **tibi faciendum est**.*
            *   Perifrástica Pasiva + Dativo Agente (*tibi*).
            *   -> Esto debe ser hecho **por ti**.
            *   -> **Tú tienes que hacer** esto.

        4.  ***Scripturus sum** epistulam.*
            *   Perifrástica Activa.
            *   -> **Voy a escribir** una carta / Estoy a punto de escribir una carta.

        5.  ***Delenda est Carthago**.* (Catón el Viejo)
            *   Perifrástica Pasiva.
            *   -> Cartago **debe ser destruida**.

        6.  ***Nunc est bibendum**.* (Horacio)
            *   Perifrástica Pasiva Impersonal.
            *   -> Ahora **hay que beber** (es momento de celebrar).
        
        ### Vocabulario Esencial
        *   **Gero, gerere**: llevar a cabo, hacer (guerra)
        *   **Servo, servare**: guardar, cumplir, conservar
        *   **Colo, colere**: cultivar, honrar
        *   **Deleo, delere**: destruir
        """)
    
    def practice_content():
        render_practice_content(24, mode="practice")

    def reading_content():
        from utils.reading_service import ReadingService
        with get_session() as session:
            reader = ReadingService(session)
            text = reader.get_reading_for_lesson(24)
            
            if text:
                st.markdown(f"#### {text.title}")
                enriched_html = reader.enrich_reading_with_tooltips(text.id)
                st.markdown(enriched_html, unsafe_allow_html=True)
            else:
                st.info("Lectura no disponible para esta lección.")

    # Fetch Lesson Object
    from database import Lesson
    from sqlmodel import select
    with get_session() as session:
        lesson_obj = session.exec(select(Lesson).where(Lesson.lesson_number == 24)).first()
        lesson = None
        if lesson_obj:
            lesson = {
                'id': lesson_obj.id,
                'lesson_number': lesson_obj.lesson_number,
                'title': lesson_obj.title,
                'content_markdown': lesson_obj.content_markdown,
            }
        
    if lesson:
        render_standard_gamified_lesson(lesson, theory_content, practice_content, reading_content)
    else:
        st.error("Error crítico: Lección 24 no encontrada en la base de datos.")

def render_lesson_25():
    def theory_content():
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
        *   **autem**: pero, en cambio (suele ir en segunda posición).
        *   **tamen**: sin embargo.
        *   **at**: pero (objeción fuerte).
        
        #### D. Ilativas (Deducen)
        *   **ergo**: por tanto, luego. *Cogito, **ergo** sum* (Pienso, **luego** existo).
        *   **igitur**: así pues (suele ir en segunda posición).
        *   **itaque**: así que, por consiguiente.
        
        #### E. Causales Coordinadas (Explican)
        *   **nam**: pues, porque (al principio de frase). *Nam tua res agitur* (Pues se trata de tu asunto).
        *   **enim**: pues, en efecto (en segunda posición).
        *   **etenim**: y en efecto.
        """)
        
        # Infografía de Coordinación
        if os.path.exists("static/images/curso_gramatica/leccion25_coordinacion.png"):
            st.image("static/images/curso_gramatica/leccion25_coordinacion.png",
                     caption="Mapa Mental de las Conjunciones Coordinantes",
                     width="stretch")
        elif os.path.exists("static/images/curso_gramatica/leccion25_coordinadas.png"):
            st.image("static/images/curso_gramatica/leccion25_coordinadas.png",
                     caption="Las Conjunciones Coordinantes en Latín",
                     width="stretch")

        st.markdown("### 🧠 Mnemotecnia: Palabras Invariables Frecuentes")
        if os.path.exists("static/images/curso_gramatica/palabras_invariables_50_frecuentes.png"):
            st.image("static/images/curso_gramatica/palabras_invariables_50_frecuentes.png",
                     caption="Las 50 Palabras Invariables Más Frecuentes (Adverbios, Conjunciones, Preposiciones)",
                     width="stretch")

        st.markdown("""
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
                     width="stretch")
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
        
        > **Ojo con DUM!** Suele llevar Presente de Indicativo aunque narre el pasado ("Presente Histórico").
        
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
            *   -> **Habiendo llegado César a la Galia**, los romanos estaban contentos.
            *   -> **Al llegar César a la Galia**...
        
        2.  *Dum Romae sum, multos libros lego.*
            *   *Dum* + Presente.
            *   -> **Mientras estoy en Roma**, leo muchos libros.
        
        3.  *Postquam urbs capta est, milites redierunt.*
            *   *Postquam* + Perfecto Indicativo.
            *   -> **Después de que la ciudad fue tomada**, los soldados regresaron.

        4.  *Quod vales, gaudeo.*
            *   *Quod* + Indicativo (Causa real).
            *   -> **Porque estás bien**, me alegro.

        5.  *Socrates accusatus est quod corrumperet juventutem.*
            *   *Quod* + Subjuntivo (Causa alegada/subjetiva).
            *   -> Sócrates fue acusado **porque (supuestamente) corrompía** a la juventud.
        
        ### Vocabulario Esencial
        *   **Cum**: cuando, como, aunque (depende del contexto)
        *   **Ubi**: cuando, donde
        *   **Postquam**: después de que
        *   **Dum**: mientras
        *   **Quod / Quia**: porque
        """)
    
    
    def practice_content():
        render_practice_content(25, mode="practice")

    def reading_content():
        from utils.reading_service import ReadingService
        with get_session() as session:
            reader = ReadingService(session)
            text = reader.get_reading_for_lesson(25)
            
            if text:
                st.markdown(f"#### {text.title}")
                enriched_html = reader.enrich_reading_with_tooltips(text.id)
                st.markdown(enriched_html, unsafe_allow_html=True)
            else:
                st.info("Lectura no disponible para esta lección.")

    # Fetch Lesson Object
    from database import Lesson
    from sqlmodel import select
    with get_session() as session:
        lesson_obj = session.exec(select(Lesson).where(Lesson.lesson_number == 25)).first()
        lesson = None
        if lesson_obj:
            lesson = {
                'id': lesson_obj.id,
                'lesson_number': lesson_obj.lesson_number,
                'title': lesson_obj.title,
                'content_markdown': lesson_obj.content_markdown,
            }
        
    if lesson:
        render_standard_gamified_lesson(lesson, theory_content, practice_content, reading_content)
    else:
        st.error("Error crítico: Lección 25 no encontrada en la base de datos.")



def render_lesson_26():
    def theory_content():
        st.markdown("""
        ## Lección 26: Subordinadas Sustantivas (Completivas)
        
        ### 1. ¿Qué son las Oraciones Completivas?
        
        Las oraciones completivas **funcionan como un sustantivo**: son el **Sujeto** o el **Objeto Directo** del verbo principal.
        
        Por ejemplo:
        - "**Quiero** que vengas" → "Que vengas" es el objeto de "quiero"
        - "**Es necesario** que estudies" → "Que estudies" es el sujeto de "es necesario"
        
        En latín, estas oraciones se construyen de formas diferentes según el tipo de verbo principal.
        
        ---
        
        ### 2. Completivas con UT / NE (Verbos de Voluntad y Mandato)
        
        Dependen de verbos que expresan **voluntad, deseo, mandato, ruego**:
        - *Volo* (querer), *Nolo* (no querer), *Malo* (preferir)
        - *Oro* (rogar), *Peto* (pedir)
        - *Impero* (mandar), *Hortor* (exhortar)
        
        """
        )

        if os.path.exists("static/images/curso_gramatica/leccion26_volo_nolo_malo.png"):
            st.image("static/images/curso_gramatica/leccion26_volo_nolo_malo.png",
                     caption="Los Tres Deseos: Volo, Nolo, Malo",
                     width="stretch")

        st.markdown("""
        **Estructura**: Verbo principal + **UT** (que) / **NE** (que no) + **Subjuntivo**
        
        **Ejemplos**:
        *   *Impero tibi **ut venias**.*
            - Te mando **que vengas**.
        *   *Oro te **ne eas**.*
            - Te ruego **que no vayas**.
        *   *Volo **ut discas**.*
            - Quiero **que aprendas**.
        
        ---
        
        ### 3. Verbos de Temor (*Verba Timendi*)
        
        ⚠️ **¡Atención!** Los verbos de temor usan UT/NE de forma **contraintuitiva**:
        
        - **Timeo NE...** = Temo **QUE** ocurra (algo que NO quiero)
        - **Timeo UT...** = Temo **QUE NO** ocurra (algo que SÍ quiero)
        
        **Ejemplos**:
        *   *Timeo **ne** pluat.*
            - Temo **que** llueva. [No quiero que llueva]
        *   *Timeo **ut** veniat.*
            - Temo **que no** venga. [Quiero que venga]
        *   *Vereor **ne** hostes urbem capiant.*
            - Temo **que** los enemigos tomen la ciudad.
        
        **Verbos de temor comunes**: *Timeo, vereor, metuo* (temer)
        
        ---
        
        ### 4. Interrogativas Indirectas
        
        Las **preguntas indirectas** también son completivas. Usan:
        - Partículas interrogativas (*quis, quid, cur, quando, ubi, quo, unde*)
        - **Subjuntivo** (aunque en español usamos indicativo)
        
        **Ejemplos**:
        *   *Nescio **quid** **facias**.*
            - No sé **qué** haces. (Lit: "qué hagas")
        *   *Rogat **cur** **veneris**.*
            - Pregunta **por qué** has venido.
        *   *Ignoro **ubi** **sit**.*
            - Ignoro **dónde** está. (Lit: "dónde esté")
        
        ---
        
        ### 5. Cuadro Resumen
        
        """)
        
        render_styled_table(
            ["Tipo", "Conjunción", "Modo", "Ejemplo", "Traducción"],
            [
                ["**Voluntad**", "UT", "Subjuntivo", "*Volo ut venias*", "Quiero que vengas"],
                ["**Voluntad (Neg)**", "NE", "Subjuntivo", "*Nolo ne eas*", "No quiero que vayas"],
                ["**Temor**", "NE", "Subjuntivo", "*Timeo ne pluat*", "Temo que llueva"],
                ["**Temor (Neg)**", "UT", "Subjuntivo", "*Timeo ut veniat*", "Temo que NO venga"],
                ["**Interrog. Ind.**", "Quis/Quid/Cur/etc", "Subjuntivo", "*Nescio quid faciam*", "No sé qué hacer"]
            ]
        )
        
        st.markdown("""
        
        ---
        
        ### 6. Ejercicios de Análisis
        
        Identifica el tipo de completiva y traduce:
        
        1.  *Imperavit militibus **ut** oppugnarent.*
            - Verbo de mando + *ut* → **Completiva de Voluntad**
            - **Traducción**: Mandó a los soldados **que** atacaran.
        
        2.  *Timeo **ne** hostes veniant.*
            - Verbo de temor + *ne* → **Completiva de Temor**
            - **Traducción**: Temo **que** los enemigos vengan.
        
        3.  *Peto **ne** me relinquas.*
            - Verbo de ruego + *ne* → **Completiva de Voluntad (negativa)**
            - **Traducción**: Pido **que no** me abandones.
        
        4.  *Nescio **quo** fugerint.*
            - Verbo de ignorancia + *quo* → **Interrogativa Indirecta**
            - **Traducción**: No sé **a dónde** huyeron.
        
        5.  *Vereor **ut** id facere possit.*
            - Verbo de temor + *ut* → **Completiva de Temor (negativa)**
            - **Traducción**: Temo **que no** pueda hacerlo.
        
        ---
        
        ### Vocabulario Esencial
        
        **Verbos de Voluntad**:
        *   **Volo, velle, volui**: querer
        *   **Nolo, nolle, nolui**: no querer
        *   **Malo, malle, malui**: preferir
        *   **Cupio, cupere**: desear
        *   **Hortor, hortari**: exhortar
        
        **Verbos de Mandato**:
        *   **Impero, imperare**: mandar
        *   **Iubeo, iubere**: ordenar
        *   **Rogo, rogare**: rogar, pedir
        *   **Peto, petere**: pedir, solicitar
        
        **Verbos de Temor**:
        *   **Timeo, timere**: temer
        *   **Vereor, vereri**: temer (deponente)
        *   **Metuo, metuere**: temer
        
        **Conjunciones**:
        *   **Ut**: que (afirmativo)
        *   **Ne**: que no (negativo)
        
        """)
        
        # Imagen de Completivas si existe
        if os.path.exists("static/images/curso_gramatica/completivas_sustantivas.png"):
            st.image("static/images/curso_gramatica/completivas_sustantivas.png",
                     caption="Oraciones Subordinadas Sustantivas (Completivas)",
                     width="stretch")
        elif os.path.exists("static/images/curso_gramatica/leccion26_sustantivas.png"):
            st.image("static/images/curso_gramatica/leccion26_sustantivas.png",
                     caption="Oraciones Subordinadas Sustantivas (Completivas)",
                     width="stretch")
    
    
    def practice_content():
        render_practice_content(26, mode="practice")

    def reading_content():
        from utils.reading_service import ReadingService
        with get_session() as session:
            reader = ReadingService(session)
            text = reader.get_reading_for_lesson(26)
            
            if text:
                st.markdown(f"#### {text.title}")
                enriched_html = reader.enrich_reading_with_tooltips(text.id)
                st.markdown(enriched_html, unsafe_allow_html=True)
            else:
                st.info("Lectura no disponible para esta lección.")

    # Fetch Lesson Object
    from database import Lesson
    from sqlmodel import select
    with get_session() as session:
        lesson_obj = session.exec(select(Lesson).where(Lesson.lesson_number == 26)).first()
        lesson = None
        if lesson_obj:
            lesson = {
                'id': lesson_obj.id,
                'lesson_number': lesson_obj.lesson_number,
                'title': lesson_obj.title,
                'content_markdown': lesson_obj.content_markdown,
            }
        
    if lesson:
        render_standard_gamified_lesson(lesson, theory_content, practice_content, reading_content)
    else:
        st.error("Error crítico: Lección 26 no encontrada en la base de datos.")

def render_lesson_27():
    def theory_content():
        st.markdown("""
        ## Lección 27: Subordinadas Adverbiales II (Finales, Consecutivas y Condicionales)
        
        En esta lección completamos las subordinadas adverbiales, añadiendo tres tipos esenciales:
        **Finales** (para qué), **Consecutivas** (con qué resultado), y **Condicionales** (si...).
        
        ---
        
        ### 1. Oraciones Finales (Propósito)
        
        Responden a: **¿Para qué?** / **¿Con qué fin?**
        
        **Estructura**:
        *   **Afirmativa**: **UT** + Subjuntivo
        *   **Negativa**: **NE** + Subjuntivo
        
        **Ejemplos**:
        *   *Edo **ut vivam**.*
            *   Como **para vivir**.
        *   *Portas clausit **ne** hostes **intrarent**.*
            *   Cerró las puertas **para que** los enemigos **no entraran**.
        *   *Legatos misit **ut** pacem **peterent**.*
            *   Envió embajadores **para pedir** la paz.
        
        ---
        
        ### 2. Oraciones Consecutivas (Consecuencia)
        
        Responden a: **¿Con qué consecuencia?** / **¿Con qué resultado?**
        
        Suelen estar **anunciadas** en la principal por un adverbio de intensidad:
        **Tam, Ita, Sic, Adeo, Tantus, Talis**
        
        **Estructura**:
        *   **Afirmativa**: **UT** + Subjuntivo
        *   **Negativa**: **UT NON** + Subjuntivo (¡No *NE*!)
        
        **Ejemplos**:
        *   ***Tam** stultus est **ut** nihil **intelligat**.*
            *   Es **tan** tonto **que no entiende** nada.
        *   ***Ita** locutus est **ut** omnes **flerent**.*
            *   Habló **de tal modo que** todos lloraban.
        *   ***Tantus** erat timor **ut** nemo **exiret**.*
            *   **Tanto** era el miedo **que** nadie salía.
        
        ---
        
        ### 3. Diferencia entre Finales y Consecutivas
        
        Ambas usan **UT**, pero tienen significados muy distintos:
        
        """)
        
        render_styled_table(
            ["Característica", "Finales", "Consecutivas"],
            [
                ["**Significado**", "Intención / Propósito", "Resultado / Efecto"],
                ["**Negación**", "**NE**", "**UT NON**"],
                ["**Pistas**", "Verbos de movimiento, voluntad", "*Tam, Ita, Sic, Tantus, Adeo* en la principal"],
                ["**Ejemplo**", "*Venit ut me videat*", "*Tam fortis est ut vincat*"]
            ]
        )
        
        st.markdown("""
        
        ---
        
        ### 4. Oraciones Condicionales
        
        Expresan una **condición** (prótasis: "Si...") y su **consecuencia** (apódosis: "...entonces").
        
        Hay **tres tipos** según el grado de realidad:
        
        #### A. Tipo I: Real (Indicativo)
        
        Expresa un hecho real o lógico. *Si pasa A, pasa B.*
        
        *   **Modo**: **Indicativo** en ambas partes
        *   *Si hoc **facis**, **erras**.*
            *   Si haces esto, te equivocas.
        
        #### B. Tipo II: Posible (Subjuntivo Presente/Perfecto)
        
        Expresa algo que **podría** ocurrir en el futuro.
        
        *   **Modo**: **Subjuntivo Presente**
        *   *Si hoc **facias**, **erres**.*
            *   Si hicieras esto (en el futuro), te equivocarías.
        
        #### C. Tipo III: Irreal (Subjuntivo Imperfecto/Pluscuamperfecto)
        
        Expresa algo que **no ocurre** (presente) o **no ocurrió** (pasado).
        
        *   **Irreal de Presente**: Subjuntivo Imperfecto
            *   *Si hoc **faceres**, **errares**.*
                *   Si hicieras esto (ahora, pero no lo haces), te equivocarías.
        
        *   **Irreal de Pasado**: Subjuntivo Pluscuamperfecto
            *   *Si hoc **fecisses**, **erravisses**.*
                *   Si hubieras hecho esto, te habrías equivocado.
        
        ---
        
        ### 5. Cuadro Resumen Completo
        
        """)
        
        render_styled_table(
            ["Tipo", "Conjunción", "Modo", "Ejemplo", "Traducción"],
            [
                ["**Final**", "UT / NE", "Subjuntivo", "*Venit ut me videat*", "Viene para verme"],
                ["**Consecutiva**", "UT / UT NON", "Subjuntivo", "*Tam fortis est ut vincat*", "Es tan fuerte que vence"],
                ["**Cond. Real**", "SI", "Indicativo", "*Si facis, erras*", "Si haces, te equivocas"],
                ["**Cond. Posible**", "SI", "Subj. Pres.", "*Si facias, erres*", "Si hicieras, te equivocarías"],
                ["**Cond. Irreal Pres.**", "SI", "Subj. Imperf.", "*Si faceres, errares*", "Si hicieras (ahora), te equivocarías"],
                ["**Cond. Irreal Pas.**", "SI", "Subj. Plusc.", "*Si fecisses, erravisses*", "Si hubieras hecho, te habrías equivocado"]
            ]
        )
        
        # Infografías de Condicionales y Finales/Consecutivas
        col1, col2 = st.columns(2)
        with col1:
            if os.path.exists("static/images/curso_gramatica/leccion27_condicionales.png"):
                st.image("static/images/curso_gramatica/leccion27_condicionales.png",
                         caption="Los Tres Tipos de Oraciones Condicionales",
                         width="stretch")
        with col2:
            if os.path.exists("static/images/curso_gramatica/leccion26_finales_consecutivas.png"):
                st.image("static/images/curso_gramatica/leccion26_finales_consecutivas.png",
                         caption="Finales vs Consecutivas",
                         width="stretch")
        
        st.markdown("""
        
        ---
        
        ### 6. Ejercicios de Análisis
        
        Identifica el tipo de subordinada y traduce:
        
        1.  *Milites pugnant **ut** urbem **defendant**.*
            *   ¿Pista de intensidad? No. ¿Es propósito? Sí.
            *   → **Final**: Los soldados luchan **para defender** la ciudad.
        
        2.  *Solis ardor **tam** magnus est **ut** herba **arescat**.*
            *   Pista: *Tam* (tan).
            *   → **Consecutiva**: El calor del sol es **tan** grande **que** la hierba se seca.
        
        3.  *Si venisses, laetus fuissem.*
            *   Subjuntivo Pluscuamperfecto.
            *   → **Condicional Irreal de Pasado**: **Si hubieras venido**, habría estado contento.
        
        4.  *Portas clausit **ne** hostes **intrarent**.*
            *   Negación *NE*.
            *   → **Final**: Cerró las puertas **para que** los enemigos **no entraran**.
        
        5.  *Si dives sim, orbem peragrem.*
            *   Subjuntivo Presente.
            *   → **Condicional Posible**: **Si fuera rico**, recorrería el mundo.
        
        ---
        
        ### Vocabulario Esencial
        
        **Conjunciones Finales**:
        *   **Ut**: para que (afirmativa)
        *   **Ne**: para que no (negativa)
        
        **Adverbios de Intensidad** (anuncian Consecutivas):
        *   **Tam**: tan
        *   **Ita / Sic**: así, de tal modo
        *   **Adeo**: tanto, hasta tal punto
        *   **Tantus, -a, -um**: tanto, tan grande
        *   **Talis, -e**: tal, de tal clase
        
        **Conjunciones Condicionales**:
        *   **Si**: si
        *   **Nisi**: si no, a menos que
        *   **Sin**: pero si, si por el contrario
        """)
    
    
    def practice_content():
        render_practice_content(27, mode="practice")

    def reading_content():
        from utils.reading_service import ReadingService
        with get_session() as session:
            reader = ReadingService(session)
            text = reader.get_reading_for_lesson(27)
            
            if text:
                st.markdown(f"#### {text.title}")
                enriched_html = reader.enrich_reading_with_tooltips(text.id)
                st.markdown(enriched_html, unsafe_allow_html=True)
            else:
                st.info("Lectura no disponible para esta lección.")

    # Fetch Lesson Object
    from database import Lesson
    from sqlmodel import select
    with get_session() as session:
        lesson_obj = session.exec(select(Lesson).where(Lesson.lesson_number == 27)).first()
        lesson = None
        if lesson_obj:
            lesson = {
                'id': lesson_obj.id,
                'lesson_number': lesson_obj.lesson_number,
                'title': lesson_obj.title,
                'content_markdown': lesson_obj.content_markdown,
            }
        
    if lesson:
        render_standard_gamified_lesson(lesson, theory_content, practice_content, reading_content)
    else:
        st.error("Error crítico: Lección 27 no encontrada en la base de datos.")

def render_lesson_28():
    def theory_content():
        st.markdown("""
        ## Lección 28: Subordinadas Adjetivas (Relativas)
        
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
                     width="stretch")
        elif os.path.exists("static/images/curso_gramatica/leccion_subordinadas_adjetivas.png"):
            st.image("static/images/curso_gramatica/leccion_subordinadas_adjetivas.png",
                     caption="Oraciones Subordinadas Adjetivas (Relativas)",
                     width="stretch")
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
        
        Normalmente llevan Indicativo. Si llevan **Subjuntivo**, añaden un matiz circunstancial (Final, Consecut o Causal).
        
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
    
    
    def practice_content():
        render_practice_content(28, mode="practice")

    def reading_content():
        from utils.reading_service import ReadingService
        with get_session() as session:
            reader = ReadingService(session)
            text = reader.get_reading_for_lesson(28)
            
            if text:
                st.markdown(f"#### {text.title}")
                enriched_html = reader.enrich_reading_with_tooltips(text.id)
                st.markdown(enriched_html, unsafe_allow_html=True)
            else:
                st.info("Lectura no disponible para esta lección.")

    # Fetch Lesson Object
    from database import Lesson
    from sqlmodel import select
    with get_session() as session:
        lesson_obj = session.exec(select(Lesson).where(Lesson.lesson_number == 28)).first()
        lesson = None
        if lesson_obj:
            lesson = {
                'id': lesson_obj.id,
                'lesson_number': lesson_obj.lesson_number,
                'title': lesson_obj.title,
                'content_markdown': lesson_obj.content_markdown,
            }
        
    if lesson:
        render_standard_gamified_lesson(lesson, theory_content, practice_content, reading_content)
    else:
        st.error("Error crítico: Lección 28 no encontrada en la base de datos.")


def render_lesson_29():
    def theory_content():
        st.markdown("""
        ## Lección 29: Estilo Indirecto (Oratio Obliqua)
        
        ### 1. ¿Qué es la Oratio Obliqua?
        
        Es referir las palabras de otro **sin citarlas textualmente**.
        *   **Directo**: César dijo: "Voy a Roma".
        *   **Indirecto**: César dijo **que él iba a Roma**.
        
        En latín, esto provoca una **transformación gramatical masiva** en toda la oración.
        
        ---
        
        ### 2. Reglas de Transformación
        
        """)
        
        if os.path.exists("static/images/curso_gramatica/leccion29_estilo_indirecto.png"):
            st.image("static/images/curso_gramatica/leccion29_estilo_indirecto.png",
                     caption="Transformación a Estilo Indirecto",
                     width="stretch")
        elif os.path.exists("static/images/curso_gramatica/leccion30_estilo_indirecto.png"):
            st.image("static/images/curso_gramatica/leccion30_estilo_indirecto.png",
                     caption="Transformación a Estilo Indirecto",
                     width="stretch")
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
        
        ---
        
        ### 4. Ejemplo Completo de Transformación
        
        **Texto Original (Directo):**
        > *"Ariovistus respondit: Ego in Galliam non veni, sed Galli ad me venerunt. Si quid vultis, pugnate!"*
        
        **Texto Indirecto (César, De Bello Gallico):**
        > *Ariovistus respondit:*
        > 1.  **se** in Galliam non **venisse** (AcI - Inf. Perf),
        > 2.  sed **Gallos** ad **se** **venisse** (AcI - Inf. Perf).
        > 3.  **Si** quid **vellent** (Subj. Imp - Subordinada), **pugnarent** (Subj. Imp - Imperativo transformado).
        
        ---
        
        ### 5. La Consecutio Temporum en Estilo Indirecto
        
        Como todo pasa a Subjuntivo o Infinitivo, la referencia temporal depende del verbo introductor (*Dicit* vs *Dixit*).
        
        *   *Dicit se id facere **quod vellet**.* (Dice que hace lo que quiere).
        
        ---
        
        ### 6. Ejercicios de Práctica
        
        Pasa a Estilo Indirecto dependiendo de *Dicit* (Dice):
        
        1.  *"Puer currit."*
            *   → *Dicit **puerum currere**.*
        
        2.  *"Ego laetus sum."*
            *   → *Dicit **se** laetum **esse**.*
        
        3.  *"Milites, qui pugnant, vincunt."*
            *   → *Dicit **milites**, qui **pugnent**, **vincere**.*
        
        ---
        
        ### 7. Ejemplo Completo de Análisis
        
        **Texto**: *Caesar dixit se, postquam hostes vicisset, Romam venturum esse.*
        
        *   **Verbo introductor**: *Dixit* (Dijo) → Tiempo histórico.
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
        
        ---
        
        ### Vocabulario Esencial
        *   **Aio / Inquam**: decir (defectivos, usados en directo)
        *   **Dico, dicere**: decir
        *   **Nego**: decir que no, negar
        *   **Respondeo**: responder
        *   **Nuntio**: anunciar
        *   **Polliceor**: prometer (+ AcI Futuro)
        """)
    
    
    def practice_content():
        render_practice_content(29, mode="practice")

    def reading_content():
        from utils.reading_service import ReadingService
        with get_session() as session:
            reader = ReadingService(session)
            text = reader.get_reading_for_lesson(29)
            
            if text:
                st.markdown(f"#### {text.title}")
                enriched_html = reader.enrich_reading_with_tooltips(text.id)
                st.markdown(enriched_html, unsafe_allow_html=True)
            else:
                st.info("Lectura no disponible para esta lección.")

    # Fetch Lesson Object
    from database import Lesson
    from sqlmodel import select
    with get_session() as session:
        lesson_obj = session.exec(select(Lesson).where(Lesson.lesson_number == 29)).first()
        lesson = None
        if lesson_obj:
            lesson = {
                'id': lesson_obj.id,
                'lesson_number': lesson_obj.lesson_number,
                'title': lesson_obj.title,
                'content_markdown': lesson_obj.content_markdown,
            }
        
    if lesson:
        render_standard_gamified_lesson(lesson, theory_content, practice_content, reading_content)
    else:
        st.error("Error crítico: Lección 29 no encontrada en la base de datos.")


def render_lesson_30():
    def theory_content():
        st.markdown("""
        ## Lección 30: Verbos Irregulares y Síntesis Final
        
        ### 1. Los Tres Irregulares Clásicos
        
        Para completar tu dominio del latín, debes conocer tres verbos irregulares omnipresentes que desafían las reglas normales.
        
        #### A. Fero, ferre, tuli, latum (Llevar, soportar)
        
        Es irregular porque **pierde la vocal de unión** en Presente.
        
        *   **Presente**: *Fero, Fers, Fert, Ferimus, Fertis, Ferunt*.
        *   **Infinitivo**: *Ferre* (no *ferere*).
        *   **Compuestos**: *Au-fero* (llevarse), *In-fero* (introducir), *Con-fero* (reunir).
        
        """
        )

        if os.path.exists("static/images/curso_gramatica/leccion30_fero_v2.png"):
            st.image("static/images/curso_gramatica/leccion30_fero_v2.png",
                     caption="El Viajero FERO: Sus múltiples equipajes (compuestos)",
                     width="stretch")

        st.markdown("""
        #### B. Eo, ire, ii, itum (Ir)
        
        La raíz es **i-**. Se transforma en **e-** ante vocal (*eo, eunt*).
        
        *   **Presente**: *Eo, Is, It, Imus, Itis, Eunt*.
        *   **Futuro**: *Ibo, ibis...* (Como la 1ª/2ª conj).
        *   **Compuestos**: *Ex-eo* (salir), *Red-eo* (volver), *Transe-o* (cruzar).
        
        #### C. Fio, fieri, factus sum (Hacerse, suceder)
        
        Funciona como la **voz pasiva de *Facio*** (hacer).
        
        *   **Presente**: *Fio, Fis, Fit, Fimus, Fitis, Fiunt*.
        *   **Significado**:
            *   *Hoc **fit**.* = Esto **sucede** / Esto **es hecho**.
            *   *Consul **factus est**.* = **Se hizo** (fue nombrado) cónsul.
        
        ---

        ### 2. La Métrica Latina (Bonus)
        
        El latín clásico no se basaba en la rima, sino en la **cantidad** (duración) de las sílabas.
        
        *   **Sílaba Larga (-)**: Dura dos tiempos.
        *   **Sílaba Breve (u)**: Dura un tiempo.
        
        El verso más famoso es el **Hexametro Dactílico** (usado en la Eneida).
        
        ### 3. Síntesis y Despedida
        
        Has recorrido el camino desde `Rosa, -ae` hasta el Estilo Indirecto y los verbos anómalos. Tienes, ahora sí, las llaves de Roma.
        
        > **Per aspera ad astra**
        > (A través de las dificultades, hacia las estrellas)
        
        A partir de aquí, el aprendizaje continúa leyendo a los clásicos: César, Cicerón, Virgilio.
        
        **¡Felicidades, Grammaticus!**
        """)
        
        if os.path.exists("static/images/curso_gramatica/leccion30_sintesis.png"):
             st.image("static/images/curso_gramatica/leccion30_sintesis.png",
                      caption="Síntesis del Curso",
                      width="stretch")

    
    def practice_content():
        render_practice_content(30, mode="practice")

    def reading_content():
        from utils.reading_service import ReadingService
        with get_session() as session:
            reader = ReadingService(session)
            text = reader.get_reading_for_lesson(30)
            
            if text:
                st.markdown(f"#### {text.title}")
                enriched_html = reader.enrich_reading_with_tooltips(text.id)
                st.markdown(enriched_html, unsafe_allow_html=True)
            else:
                st.info("Lectura no disponible para esta lección.")

    # Fetch Lesson Object
    from database import Lesson
    from sqlmodel import select
    with get_session() as session:
        lesson_obj = session.exec(select(Lesson).where(Lesson.lesson_number == 30)).first()
        lesson = None
        if lesson_obj:
            lesson = {
                'id': lesson_obj.id,
                'lesson_number': lesson_obj.lesson_number,
                'title': lesson_obj.title,
                'content_markdown': lesson_obj.content_markdown,
            }
        
    if lesson:
        render_standard_gamified_lesson(lesson, theory_content, practice_content, reading_content)
    else:
        st.error("Error crítico: Lección 30 no encontrada en la base de datos.")




def render_lesson_31():
    def theory_content():
        st.markdown("""
        ## Lección 31: César y la Prosa Militar
        
        ### 1. C. Iulius Caesar (100-44 a.C.)
        
        Julio César no solo fue uno de los generales y políticos más brillantes de Roma, sino también un **maestro de la prosa latina**. Sus *Commentarii* (Comentarios) son el modelo de la latinidad pura.
        """)

        st.image("static/images/curso_gramatica/leccion31_cesar.png",
                 caption="Julio César: Conquistador y Escritor",
                 width="stretch")

        st.markdown("""
        ### 2. Estilo: *Pura et Illustris Brevitas*
        
        El estilo de César se caracteriza por:
        *   **Brevedad y Claridad**: Evita palabras raras o arcaicas.
        *   **Uso de la 3ª Persona**: Se refiere a sí mismo como "César" para dar apariencia de objetividad.
        *   **Vocabulario Militar**: Preciso y técnico (*acies, legio, castra, imperator*).
        *   **Ablativo Absoluto**: Uso frecuente para acelerar la narración.
        
        ### 3. Texto: De Bello Gallico (I.1)
        
        El inicio más famoso de la literatura latina histórica:
        
        > *Gallia est omnis divisa in partes tres, quarum unam incolunt Belgae, aliam Aquitani, tertiam qui ipsorum lingua Celtae, nostra Galli appellantur.*
        
        **Traducción**:
        "Toda la Galia está dividida en tres partes, de las cuales una la habitan los Belgas, otra los Aquitanos, la tercera los que en su propia lengua se llaman Celtas, en la nuestra Galos."
        
        ### 4. Vocabulario de Autor
        *   **Divido, -ere, -visi, -visum**: dividir
        *   **Incolo, -ere, -ui**: habitar
        *   **Appello, -are**: llamar
        *   **Lex, legis**: ley
        *   **Proelium, -ii**: batalla
        """)
    
    render_lesson_with_tabs(31, theory_content)

def render_lesson_32():
    def theory_content():
        st.markdown("""
        ## Lección 32: Cicerón y la Retórica
        
        ### 1. M. Tullius Cicero (106-43 a.C.)
        
        Cicerón es la cumbre de la oratoria romana y el creador del lenguaje filosófico latino. Su vida estuvo dedicada a la defensa de la República.
        """)
        
        st.image("static/images/curso_gramatica/leccion32_ciceron.png",
                 caption="Cicerón denunciando a Catilina en el Senado",
                 width="stretch")

        st.markdown("""
        ### 2. Estilo: El Periodo Oratorio
        
        A diferencia de la brevedad de César, Cicerón busca la **amplitud y el ritmo**:
        *   **Concinnitas**: Equilibrio y simetría en las frases.
        *   **Cláusulas Métricas**: El final de las frases tiene un ritmo poético.
        *   **Anáfora y Tricolon**: Repetición de palabras y estructuras de tres elementos.
        
        ### 3. Texto: In Catilinam (I.1)
        
        El ataque directo contra el conspirador Catilina:
        
        > *Quousque tandem abutere, Catilina, patientia nostra? Quamdiu etiam furor iste tuus nos eludet? Quem ad finem sese effrenata iactabit audacia?*
        
        **Traducción**:
        "¿Hasta cuándo, finalmente, abusarás, Catilina, de nuestra paciencia? ¿Cuánto tiempo todavía esa locura tuya se burlará de nosotros? ¿Hasta qué límite se arrojará esa audacia desenfrenada?"
        
        ### 4. Vocabulario de Autor
        *   **Abutor, -i, -usus sum** (+ Abl): abusar
        *   **Patientia, -ae**: paciencia
        *   **Furor, -oris**: locura
        *   **Eludo, -ere**: burlar, esquivar
        *   **Audacia, -ae**: audacia, osadía
        """)
    
    render_lesson_with_tabs(32, theory_content)

def render_lesson_33():
    def theory_content():
        st.markdown("""
        ## Lección 33: Salustio y la Historiografía
        
        ### 1. C. Sallustius Crispus (86-34 a.C.)
        
        Salustio creó la **monografía histórica**. Se centró en la corrupción moral de Roma que llevó al fin de la República.
        """)
        
        st.image("static/images/curso_gramatica/leccion33_salustio.png",
                 caption="Salustio: El Historiador Moralista",
                 width="stretch")

        st.markdown("""
        ### 2. Estilo: *Inconcinnitas* y Arcaísmo
        
        Salustio se opone al estilo de Cicerón:
        *   **Brevitas**: Concisión extrema, a veces oscura.
        *   **Inconcinnitas**: Evita la simetría deliberadamente para sorprender.
        *   **Arcaísmos**: Usa palabras antiguas para dar gravedad (*optumus* en vez de *optimus*).
        *   **Infinitivo Histórico**: Usa infinitivos como verbos principales para dar rapidez.
        
        ### 3. Texto: Retrato de Catilina (5.1)
        
        > *Lucius Catilina, nobili genere natus, fuit magna vi et animi et corporis, sed ingenio malo pravoque.*
        
        **Traducción**:
        "Lucio Catilina, nacido de noble linaje, fue de gran fuerza tanto de espíritu como de cuerpo, pero de carácter malo y depravado."
        
        ### 4. Vocabulario de Autor
        *   **Ingenium, -ii**: carácter, talento natural
        *   **Pravus, -a, -um**: torcido, depravado
        *   **Inedia, -ae**: falta de comida, ayuno
        *   **Algor, -oris**: frío
        *   **Vigilia, -ae**: falta de sueño, guardia
        """)
    
    render_lesson_with_tabs(33, theory_content)

def render_lesson_34():
    def theory_content():
        st.markdown("""
        ## Lección 34: Catulo y la Lírica
        
        ### 1. C. Valerius Catullus (84-54 a.C.)
        
        Líder de los *Poetae Novi* (Neotéricos). Se alejó de la épica y la política para centrarse en **el arte por el arte** y los **sentimientos personales**.
        """)
        
        st.image("static/images/curso_gramatica/leccion34_catulo.png",
                 caption="Catulo y Lesbia: El Odio y el Amor",
                 width="stretch")

        st.markdown("""
        ### 2. Estilo: Pasión y Erudición
        
        *   **Endecasílabo Falecio**: Su metro favorito (11 sílabas).
        *   **Diminutivos**: Uso afectivo (*libellus, ocellus*).
        *   **Coloquialismos**: Lenguaje de la calle mezclado con mitología griega.
        *   **Lesbia**: Pseudónimo de su amada Clodia.
        
        ### 3. Texto: Odi et Amo (Carmen 85)
        
        Dos versos que resumen la complejidad del amor:
        
        > *Odi et amo. Quare id faciam, fortasse requiris.*
        > *Nescio, sed fieri sentio et excrucior.*
        
        **Traducción**:
        "Odio y amo. Por qué hago esto, quizás preguntas.
        No lo sé, pero siento que sucede y me torturo."
        
        ### 4. Vocabulario de Autor
        *   **Odi** (defectivo): odiar
        *   **Requiro, -ere**: preguntar, buscar
        *   **Fio, fieri**: suceder, hacerse
        *   **Sentio, -ire**: sentir
        *   **Excrucior, -ari**: ser torturado (crucificado)
        """)
    
    render_lesson_with_tabs(34, theory_content)

def render_lesson_35():
    def theory_content():
        st.markdown("""
        ## Lección 35: Virgilio y la Épica
        
        ### 1. P. Vergilius Maro (70-19 a.C.)
        
        El poeta nacional de Roma. Su obra glorifica los orígenes míticos de Roma y la familia Julia (Augusto).
        """)
        
        st.image("static/images/curso_gramatica/leccion35_virgilio.png",
                 caption="Virgilio leyendo la Eneida a Augusto",
                 width="stretch")

        st.markdown("""
        ### 2. Estilo: La Perfección del Hexámetro
        
        *   **Hexámetro Dactílico**: Virgilio llevó este metro a su máxima perfección y armonía.
        *   **Pietas**: El tema central de Eneas, el deber hacia los dioses, la patria y la familia.
        *   **Pathos**: Gran sensibilidad hacia el sufrimiento humano (las "lágrimas de las cosas").
        
        ### 3. Texto: La Eneida (I.1-3)
        
        El inicio de la gran epopeya romana:
        
        > *Arma virumque cano, Troiae qui primus ab oris*
        > *Italiam, fato profugus, Laviniaque venit*
        > *litora...*
        
        **Traducción**:
        "Canto a las armas y al hombre que, el primero desde las costas de Troya,
        llegó a Italia, prófugo por el destino, y a las costas de Lavinio..."
        
        ### 4. Vocabulario de Autor
        *   **Cano, -ere, cecini**: cantar (poéticamente)
        *   **Ora, -ae**: costa, orilla
        *   **Fatum, -i**: destino, hado
        *   **Profugus, -a, -um**: prófugo, fugitivo
        *   **Litus, -oris**: playa, costa
        """)
    
    render_lesson_with_tabs(35, theory_content)

def render_lesson_36():
    def theory_content():
        st.markdown("""
        ## Lección 36: Horacio y las Odas
        
        ### 1. Q. Horatius Flaccus (65-8 a.C.)
        
        Amigo de Virgilio y protegido de Mecenas. Es el maestro de la lírica reflexiva y la sátira.
        """)
        
        st.image("static/images/curso_gramatica/leccion36_horacio.png",
                 caption="Horacio: El Poeta del Carpe Diem",
                 width="stretch")

        st.markdown("""
        ### 2. Estilo: *Curiosa Felicitas*
        
        *   **Curiosa Felicitas**: La "dicha cuidadosamente buscada". Perfección técnica que parece natural.
        *   **Aurea Mediocritas**: El ideal del "dorado término medio", la moderación.
        *   **Temas**: El paso del tiempo, el vino, la amistad, la vida sencilla.
        
        ### 3. Texto: Carpe Diem (Odas I.11)
        
        > *Carpe diem, quam minimum credula postero.*
        
        **Traducción**:
        "Aprovecha el día, confiando lo menos posible en el mañana."
        (Literalmente: "Cosecha el día...")
        
        ### 4. Vocabulario de Autor
        *   **Carpo, -ere, carpsi**: arrancar, cosechar, aprovechar
        *   **Credulus, -a, -um**: crédulo, confiado
        *   **Posterus, -a, -um**: siguiente, futuro
        *   **Aetas, -atis**: edad, tiempo, vida
        *   **Fugio, -ere**: huir
        """)
    
    render_lesson_with_tabs(36, theory_content)

def render_lesson_37():
    def theory_content():
        st.markdown("""
        ## Lección 37: Ovidio y la Mitología
        
        ### 1. P. Ovidius Naso (43 a.C. - 17 d.C.)
        
        El más joven de los elegíacos. Poeta del amor (*Amores*, *Ars Amatoria*) y de los mitos (*Metamorfosis*). Murió en el exilio.
        """)
        
        st.image("static/images/curso_gramatica/leccion37_ovidio.png",
                 caption="Ovidio: Las Metamorfosis",
                 width="stretch")

        st.markdown("""
        ### 2. Estilo: Ingenio y Fluidez
        
        *   **Facilidad Versificadora**: "Todo lo que intentaba decir se convertía en verso".
        *   **Narrativa Visual**: Sus descripciones son casi cinematográficas.
        *   **Psicología Femenina**: Gran capacidad para retratar los sentimientos de sus heroínas (Heroidas).
        
        ### 3. Texto: Dafne y Apolo (Met. I.452)
        
        > *Primus amor Phoebi Daphne Peneia, quem non*
        > *fors ignara dedit, sed saeva Cupidinis ira.*
        
        **Traducción**:
        "El primer amor de Febo (Apolo) fue Dafne, hija de Peneo, el cual no
        lo dio el azar ignorante, sino la ira cruel de Cupido."
        
        ### 4. Vocabulario de Autor
        *   **Amor, -oris**: amor
        *   **Ira, -ae**: ira
        *   **Saevus, -a, -um**: cruel, fiero
        *   **Fors, fortis**: suerte, azar
        *   **Ignarus, -a, -um**: ignorante
        """)
    
    render_lesson_with_tabs(37, theory_content)

def render_lesson_38():
    def theory_content():
        st.markdown("""
        ## Lección 38: Latín Medieval
        
        ### 1. Características Generales
        
        El latín medieval (aprox. 500-1400 d.C.) fue la lengua franca de la cultura, la iglesia y la universidad en Europa.
        
        *   **Simplificación Sintáctica**: Menos uso de oraciones subordinadas complejas; preferencia por *quod* + indicativo en lugar de AcI.
        *   **Cambios Fonéticos**: *ae/oe* > *e* (caelum > celum).
        *   **Vocabulario**: Influencia cristiana y germánica.
        
        ### 2. Texto: Dies Irae (Tomás de Celano, s. XIII)
        
        > *Dies irae, dies illa,*
        > *Solvet saeclum in favilla,*
        > *Teste David cum Sibylla.*
        
        **Traducción**:
        "Día de ira, aquel día,
        disolverá el mundo en cenizas,
        como testigos David con la Sibila."
        """)
        
        if os.path.exists("static/images/curso_gramatica/leccion38_latin_medieval.png"):
            st.image("static/images/curso_gramatica/leccion38_latin_medieval.png",
                     caption="Manuscrito Medieval",
                     width="stretch")
    
    render_lesson_with_tabs(38, theory_content)



def render_lesson_39():
    def theory_content():
        st.markdown("""
        ## Lección 39: Latín Eclesiástico
        
        ### 1. El Latín de la Iglesia
        
        Es la forma de latín usada en la liturgia católica. Se basa en el latín tardío y la Vulgata de San Jerónimo.
        
        *   **Pronunciación**: "Italianizante" (c ante e/i = ch; g ante e/i = y).
        *   **Vocabulario**: Términos teológicos griegos latinizados (*ecclesia, angelus, baptisma*).
        
        ### 2. Texto: Pater Noster
        
        > *Pater noster, qui es in caelis,*
        > *sanctificetur nomen tuum.*
        > *Adveniat regnum tuum.*
        
        **Traducción**:
        "Padre nuestro, que estás en los cielos,
        santificado sea tu nombre.
        Venga tu reino."
        """)
        
        if os.path.exists("static/images/curso_gramatica/leccion39_latin_eclesiastico.png"):
            st.image("static/images/curso_gramatica/leccion39_latin_eclesiastico.png",
                     caption="Latín Eclesiástico",
                     width="stretch")
    
    render_lesson_with_tabs(39, theory_content)

def render_lesson_40():
    def theory_content():
        st.markdown("""
        ## Lección 40: Latín Renacentista y Científico
        
        ### 1. El Retorno a los Clásicos y la Ciencia
        
        En el Renacimiento, los humanistas intentaron volver al latín de Cicerón. Más tarde, el latín se convirtió en el idioma universal de la ciencia (Newton, Linneo, Descartes).
        
        *   **Neologismos**: Creación de palabras para conceptos nuevos (*microscopium, electricitas*).
        *   **Estilo**: Preciso, lógico y descriptivo.
        
        ### 2. Texto: Descartes (Principia Philosophiae)
        
        > *Cogito, ergo sum.*
        
        **Traducción**:
        "Pienso, luego existo."
        
        ### 3. Texto: Newton (Principia Mathematica)
        
        > *Hypotheses non fingo.*
        
        **Traducción**:
        "No invento hipótesis."
        """)
        
        if os.path.exists("static/images/curso_gramatica/leccion40_latin_renacentista.png"):
            st.image("static/images/curso_gramatica/leccion40_latin_renacentista.png",
                     caption="Latín Científico",
                     width="stretch")
    
    render_lesson_with_tabs(40, theory_content)

if __name__ == "__main__":
    main()
