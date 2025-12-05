"""
Learning Hub Widgets
Widgets interactivos para mostrar vocabulario y ejercicios de traducción dentro de las lecciones.
"""

import streamlit as st
from typing import List, Dict, Optional
from sqlmodel import Session, select
import random

from database import (
    get_session, Word, LessonVocabulary, SentenceAnalysis,
    UserVocabularyProgress
)
from utils.progress_tracker import record_vocabulary_practice, record_exercise_attempt as tracker_record_attempt
from utils.ui_components import render_progress_bar
from utils.progress_service import record_exercise_attempt


def render_vocabulary_widget(lesson_number: int, user_id: int = 1):
    """
    Widget interactivo de vocabulario esencial de la lección.
    
    Args:
        lesson_number: Número de lección
        user_id: ID del usuario (default: 1)
    """
    st.markdown("---")
    st.markdown("## 📚 Vocabulario Esencial")
    
    with st.expander("🎴 Practica el Vocabulario de esta Lección", expanded=False):
        with get_session() as session:
            # Obtener vocabulario de la lección
            statement = (
                select(Word, LessonVocabulary)
                .join(LessonVocabulary, Word.id == LessonVocabulary.word_id)
                .where(LessonVocabulary.lesson_number == lesson_number)
                .order_by(LessonVocabulary.presentation_order)
            )
            
            results = session.exec(statement).all()
            
            if not results:
                st.info(f"📝 El vocabulario para la Lección {lesson_number} se agregará próximamente.")
                return
            
            words = [(word, vocab) for word, vocab in results]
            
            # Calcular progreso general
            statement_progress = (
                select(UserVocabularyProgress)
                .where(
                    UserVocabularyProgress.user_id == user_id,
                    UserVocabularyProgress.word_id.in_([w[0].id for w in words])
                )
            )
            progress_records = session.exec(statement_progress).all()
            progress_dict = {p.word_id: p for p in progress_records}
            
            # Calcular mastery promedio
            total_words = len(words)
            mastered_count = sum(1 for w in words if progress_dict.get(w[0].id) and progress_dict[w[0].id].mastery_level >= 0.8)
            
            # Mostrar resumen
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Palabras", total_words)
            with col2:
                st.metric("Dominadas", mastered_count)
            with col3:
                mastery_pct = (mastered_count / total_words) * 100 if total_words > 0 else 0
                st.metric("Dominio", f"{mastery_pct:.0f}%")
            
            render_progress_bar(mastered_count, total_words, "Progreso de Vocabulario")
            
            st.markdown("---")
            
            # Modo de práctica
            practice_mode = st.radio(
                "Modo de práctica:",
                ["📖 Ver Lista", "🎯 Flashcards"],
                horizontal=True,
                key=f"vocab_mode_l{lesson_number}"
            )
            
            if practice_mode == "📖 Ver Lista":
                _render_vocabulary_list(words, progress_dict, lesson_number)
            else:
                _render_flashcards(words, progress_dict, lesson_number, user_id, session)


def _render_vocabulary_list(words: List, progress_dict: Dict, lesson_number: int):
    """Renderiza la lista completa de vocabulario."""
    st.markdown("### 📋 Lista de Vocabulario")
    
    for word, vocab_link in words:
        # Obtener progreso
        progress = progress_dict.get(word.id)
        mastery = progress.mastery_level if progress else 0.0
        
        # Color según dominio
        if mastery >= 0.8:
            badge = "✅"
            color = "#28a745"
        elif mastery >= 0.5:
            badge = "🟡"
            color = "#ffc107"
        elif mastery > 0:
            badge = "🔴"
            color = "#dc3545"
        else:
            badge = "⚪"
            color = "#999"
        
        # Crear entrada expandible
        with st.expander(f"{badge} **{word.latin}** - {word.translation}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Latín:** {word.latin}")
                st.markdown(f"**Español:** {word.translation}")
                
                if word.part_of_speech == "noun":
                    if word.genitive:
                        st.markdown(f"**Genitivo:** {word.genitive}")
                    if word.gender:
                        st.markdown(f"**Género:** {word.gender}")
                    if word.declension:
                        st.markdown(f"**Declinación:** {word.declension}")
                elif word.part_of_speech == "verb":
                    if word.principal_parts:
                        st.markdown(f"**Partes principales:** {word.principal_parts}")
                    if word.conjugation:
                        st.markdown(f"**Conjugación:** {word.conjugation}")
                elif word.part_of_speech == "adjective":
                    if word.declension:
                        st.markdown(f"**Declinación:** {word.declension}")
                
                if vocab_link.example_sentence:
                    st.markdown(f"**Ejemplo:** _{vocab_link.example_sentence}_")
                
                if word.cultural_context:
                    st.info(f"🏛️ **Contexto Cultural:** {word.cultural_context}")
            
            with col2:
                if progress:
                    st.metric("Dominio", f"{mastery*100:.0f}%")
                    st.caption(f"Visto {progress.times_seen} veces")
                    st.caption(f"✅ {progress.times_correct} | ❌ {progress.times_incorrect}")
                else:
                    st.info("No practicado aún")


def _render_flashcards(words: List, progress_dict: Dict, lesson_number: int, user_id: int, session: Session):
    """Renderiza modo flashcards interactivo."""
    st.markdown("### 🎴 Práctica con Flashcards")
    
    # Inicializar session state
    if f'flashcard_idx_l{lesson_number}' not in st.session_state:
        st.session_state[f'flashcard_idx_l{lesson_number}'] = 0
        st.session_state[f'flashcard_show_l{lesson_number}'] = False
        st.session_state[f'flashcard_mode_l{lesson_number}'] = "latin_to_spanish"
    
    idx_key = f'flashcard_idx_l{lesson_number}'
    show_key = f'flashcard_show_l{lesson_number}'
    mode_key = f'flashcard_mode_l{lesson_number}'
    
    # Selector de modo
    mode = st.radio(
        "Dirección:",
        ["Latín → Español", "Español → Latín"],
        horizontal=True,
        key=f"flashcard_direction_l{lesson_number}"
    )
    st.session_state[mode_key] = "latin_to_spanish" if mode == "Latín → Español" else "spanish_to_latin"
    
    if len(words) == 0:
        st.warning("No hay palabras para practicar.")
        return
    
    # Obtener palabra actual
    current_idx = st.session_state[idx_key] % len(words)
    word, vocab_link = words[current_idx]
    
    # Mostrar progreso
    st.progress((current_idx + 1) / len(words))
    st.caption(f"Palabra {current_idx + 1} de {len(words)}")
    
    # Mostrar flashcard
    st.markdown("###")
    
    # Traducir part_of_speech al español
    pos_translations = {
        "noun": "sustantivo",
        "verb": "verbo",
        "adjective": "adjetivo",
        "pronoun": "pronombre",
        "adverb": "adverbio",
        "preposition": "preposición",
        "conjunction": "conjunción",
        "interjection": "interjección"
    }
    
    if st.session_state[mode_key] == "latin_to_spanish":
        question = word.latin
        answer = word.translation
        hint = pos_translations.get(word.part_of_speech, word.part_of_speech)
    else:
        question = word.translation
        answer = word.latin
        hint = pos_translations.get(word.part_of_speech, word.part_of_speech)
    
    # Tarjeta frontal
    st.markdown(
        f"""
        <div style='background: linear-gradient(135deg, rgba(139,69,19,0.1), rgba(210,180,140,0.1));
                    padding: 40px; border-radius: 15px; text-align: center; 
                    border: 3px solid #8b4513; min-height: 200px;
                    display: flex; align-items: center; justify-content: center;'>
            <div>
                <div style='font-size: 2.5em; font-weight: bold; color: #8b4513; margin-bottom: 10px;'>
                    {question}
                </div>
                <div style='font-size: 1.2em; color: #666; font-style: italic;'>
                    ({hint})
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("###")
    
    # Botón para mostrar respuesta
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if not st.session_state[show_key]:
            if st.button("👁️ Mostrar Respuesta", key=f"show_l{lesson_number}_{current_idx}", width="stretch"):
                st.session_state[show_key] = True
                st.rerun()
        else:
            # Mostrar respuesta
            st.markdown(
                f"""
                <div style='background: #d4edda; padding: 20px; border-radius: 10px; 
                            text-align: center; border: 2px solid #28a745;'>
                    <div style='font-size: 2em; font-weight: bold; color: #155724;'>
                        {answer}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            st.markdown("###")
            st.markdown("#### ¿La sabías?")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                if st.button("✅ Sí", key=f"correct_l{lesson_number}_{current_idx}", width="stretch"):
                    record_vocabulary_practice(session, user_id, word.id, was_correct=True)
                    st.session_state[show_key] = False
                    st.session_state[idx_key] += 1
                    st.success("¡Bien hecho!")
                    st.rerun()
            
            with col_b:
                if st.button("❌ No", key=f"incorrect_l{lesson_number}_{current_idx}", width="stretch"):
                    record_vocabulary_practice(session, user_id, word.id, was_correct=False)
                    st.session_state[show_key] = False
                    st.session_state[idx_key] += 1
                    st.info("¡Sigue practicando!")
                    st.rerun()
    
    # Navegación
    st.markdown("---")
    col_nav1, col_nav2, col_nav3 = st.columns(3)
    
    with col_nav1:
        if st.button("⏮️ Anterior", disabled=(current_idx == 0), key=f"prev_l{lesson_number}"):
            st.session_state[idx_key] = max(0, current_idx - 1)
            st.session_state[show_key] = False
            st.rerun()
    
    with col_nav2:
        if st.button("🔀 Aleatorio", key=f"random_l{lesson_number}"):
            st.session_state[idx_key] = random.randint(0, len(words) - 1)
            st.session_state[show_key] = False
            st.rerun()
    
    with col_nav3:
        if st.button("⏭️ Siguiente", disabled=(current_idx >= len(words) - 1), key=f"next_l{lesson_number}"):
            st.session_state[idx_key] = min(len(words) - 1, current_idx + 1)
            st.session_state[show_key] = False
            st.rerun()


def render_translation_workshop(lesson_number: int, user_id: int = 1):
    """
    Widget de taller de traducción con oraciones de la lección.
    
    Args:
        lesson_number: Número de lección
        user_id: ID del usuario (default: 1)
    """
    st.markdown("---")
    st.markdown("## 📝 Taller de Traducción")
    
    with st.expander("✍️ Practica Traduciendo", expanded=False):
        with get_session() as session:
            # Obtener oraciones de traducción de la lección
            statement = (
                select(SentenceAnalysis)
                .where(
                    SentenceAnalysis.lesson_number == lesson_number,
                    SentenceAnalysis.usage_type == "translation_exercise"
                )
                .order_by(SentenceAnalysis.complexity_level)
            )
            
            sentences = session.exec(statement).all()
            
            if not sentences:
                st.info(f"📝 Los ejercicios de traducción para la Lección {lesson_number} se agregarán próximamente.")
                return
            
            # Mostrar resumen
            st.markdown(f"**{len(sentences)} oraciones** para practicar")
            
            # Selector de oración
            sentence_idx = st.selectbox(
                "Selecciona una oración:",
                range(len(sentences)),
                format_func=lambda i: f"Oración {i+1} (Nivel {sentences[i].complexity_level})",
                key=f"translation_selector_l{lesson_number}"
            )
            
            sentence = sentences[sentence_idx]
            
            st.markdown("---")
            
            # Mostrar oración latina
            st.markdown(
                f"""
                <div style='background: linear-gradient(135deg, rgba(139,69,19,0.1), rgba(210,180,140,0.1));
                            padding: 30px; border-radius: 10px; text-align: center; 
                            border-left: 5px solid #8b4513;'>
                    <div style='font-size: 1.8em; font-weight: bold; font-style: italic; color: #8b4513;'>
                        {sentence.latin_text}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            st.markdown("###")
            
            # Área de traducción del usuario
            user_translation = st.text_area(
                "Tu traducción al español:",
                height=100,
                key=f"translation_input_l{lesson_number}_{sentence_idx}",
                placeholder="Escribe tu traducción aquí..."
            )
            
            # Botón de Guía de Traducción
            st.markdown("###")
            from utils.hint_system import detect_sentence_type, get_translation_guide_path, generate_structure_hints
            
            sentence_type = detect_sentence_type(sentence.latin_text)
            
            if st.button("📚 Ver Guía de Traducción Paso a Paso", key=f"guide_l{lesson_number}_{sentence_idx}", width="stretch"):
                st.markdown(f"### 🎓 Guía: Oraciones {sentence_type.capitalize()}s")
                
                # Mostrar pasos estratégicos
                st.markdown("**Sigue estos pasos:**")
                for hint in generate_structure_hints(sentence_type):
                    st.markdown(hint)
                
                # Mostrar infografía
                guide_path = get_translation_guide_path(sentence_type)
                if guide_path:
                    st.image(guide_path, 
                            caption=f"Estrategia de traducción para oraciones {sentence_type}s",
                            width=650)
            
            st.markdown("###")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📖 Ver Traducción Correcta", key=f"show_translation_l{lesson_number}_{sentence_idx}"):
                    st.markdown(
                        f"""
                        <div style='background: #d4edda; padding: 20px; border-radius: 10px; 
                                    border: 2px solid #28a745; margin-top: 10px;'>
                            <div style='font-weight: bold; color: #155724; margin-bottom: 10px;'>
                                ✅ Traducción:
                            </div>
                            <div style='font-size: 1.2em; color: #155724;'>
                                {sentence.spanish_translation}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            with col2:
                if st.button("💡 Pista", key=f"hint_translation_l{lesson_number}_{sentence_idx}"):
                    # Generar pista simple (primeras palabras)
                    words = sentence.spanish_translation.split()
                    hint_words = words[:min(3, len(words))]
                    st.info(f"**Pista:** Empieza con '{' '.join(hint_words)}...'")
            
            # Botón de autoevaluación
            st.markdown("###")
            st.markdown("#### ¿Cómo te fue con esta traducción?")
            
            col_eval1, col_eval2, col_eval3 = st.columns(3)
            
            with col_eval1:
                if st.button("🎯 Perfecta", key=f"eval_perfect_l{lesson_number}_{sentence_idx}"):
                    # Registrar como correcto
                    record_exercise_attempt(
                        session, user_id, lesson_number,
                        "translation", 
                        {"sentence_id": sentence.id},
                        user_translation,
                        sentence.spanish_translation,
                        True, 0, False
                    )
                    st.success("¡Excelente trabajo!")
            
            with col_eval2:
                if st.button("~📊 Aproximada", key=f"eval_close_l{lesson_number}_{sentence_idx}"):
                    # Registrar como parcialmente correcto (marcar como correcto)
                    record_exercise_attempt(
                        session, user_id, lesson_number,
                        "translation",
                        {"sentence_id": sentence.id},
                        user_translation,
                        sentence.spanish_translation,
                        True, 0, False
                    )
                    st.info("¡Bien! Sigue mejorando.")
            
            with col_eval3:
                if st.button("❌ Incorrecta", key=f"eval_wrong_l{lesson_number}_{sentence_idx}"):
                    # Registrar como incorrecto
                    record_exercise_attempt(
                        session, user_id, lesson_number,
                        "translation",
                        {"sentence_id": sentence.id},
                        user_translation,
                        sentence.spanish_translation,
                        False, 0, False
                    )
                    st.warning("Sigue practicando. Compara con la respuesta correcta.")


def render_lesson_progress_summary(lesson_number: int, user_id: int = 1):
    """
    Muestra un resumen visual del progreso en la lección.
    
    Args:
        lesson_number: Número de lección
        user_id: ID del usuario (default: 1)
    """
    with get_session() as session:
        # Obtener métricas de vocabulario
        statement_vocab = (
            select(Word, LessonVocabulary)
            .join(LessonVocabulary, Word.id == LessonVocabulary.word_id)
            .where(LessonVocabulary.lesson_number == lesson_number)
        )
        vocab_words = session.exec(statement_vocab).all()
        total_vocab = len(vocab_words)
        
        # Obtener progreso de vocabulario
        statement_progress = (
            select(UserVocabularyProgress)
            .where(
                UserVocabularyProgress.user_id == user_id,
                UserVocabularyProgress.word_id.in_([w[0].id for w in vocab_words])
            )
        )
        progress_records = session.exec(statement_progress).all()
        vocab_mastered = sum(1 for p in progress_records if p.mastery_level >= 0.8)
        
        # Obtener oraciones
        statement_sentences = (
            select(SentenceAnalysis)
            .where(
                SentenceAnalysis.lesson_number == lesson_number,
                SentenceAnalysis.usage_type == "translation_exercise"
            )
        )
        total_sentences = len(session.exec(statement_sentences).all())
        
        # Mostrar resumen
        st.markdown(
            f"""
            <div style='background: linear-gradient(135deg, rgba(139,69,19,0.05), rgba(210,180,140,0.05));
                        padding: 20px; border-radius: 10px; border: 2px solid rgba(139,69,19,0.2);
                        margin: 20px 0;'>
                <h4 style='color: #8b4513; margin-top: 0;'>📊 Progreso de Lección {lesson_number}</h4>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if total_vocab > 0:
                vocab_pct = (vocab_mastered / total_vocab)
                render_progress_bar(vocab_mastered, total_vocab, "📚 Vocabulario Dominado")
            else:
                st.info("📚 Vocabulario: Próximamente")
        
        with col2:
            if total_sentences > 0:
                st.info(f"📝 {total_sentences} oraciones de práctica disponibles.")
            else:
                st.info("📝 Traducción: Próximamente")


def render_sentence_analysis_widget(lesson_number: int):
    """
    Widget para análisis sintáctico interactivo.
    
    Args:
        lesson_number: Número de lección
    """
    import json
    import re
    
    st.markdown("---")
    st.markdown("## 🔍 Análisis Sintáctico")
    
    with st.expander("🕵️ Analiza la Estructura", expanded=False):
        with get_session() as session:
            statement = (
                select(SentenceAnalysis)
                .where(
                    SentenceAnalysis.lesson_number == lesson_number,
                    SentenceAnalysis.usage_type == "analysis"
                )
            )
            sentences = session.exec(statement).all()
            
            if not sentences:
                st.info("Próximamente ejercicios de análisis para esta lección.")
                return
                
            # Selector
            s_idx = st.selectbox(
                "Selecciona una oración para analizar:",
                range(len(sentences)),
                format_func=lambda i: f"Oración {i+1}: {sentences[i].latin_text[:40]}...",
                key=f"analysis_sel_l{lesson_number}"
            )
            
            sentence = sentences[s_idx]
            roles_map = json.loads(sentence.syntax_roles) if sentence.syntax_roles else {}
            
            # Display Sentence
            st.markdown(
                f"""
                <div style='font-size: 1.5em; font-weight: bold; text-align: center; 
                            padding: 20px; background: linear-gradient(to right, #f8f9fa, #e9ecef); 
                            border-radius: 10px; border-left: 5px solid #17a2b8; 
                            margin-bottom: 20px; color: #2c3e50; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                    {sentence.latin_text}
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Interaction
            col1, col2 = st.columns([1, 2])
            
            with col1:
                role_options = {
                    "subject": "Sujeto (Nominativo)",
                    "verb": "Verbo / Predicado",
                    "direct_object": "Objeto Directo (Acusativo)",
                    "indirect_object": "Objeto Indirecto (Dativo)",
                    "attribute": "Atributo / Predicativo",
                    "subject_accusative": "Sujeto (Acusativo)",
                    "attribute_accusative": "Atributo (Acusativo)",
                    "ablative_absolute": "Ablativo Absoluto",
                    "agent": "Agente (Ablativo)",
                    "conjunction": "Conjunción / Nexo",
                    "coordinator": "Coordinante",
                    "negative": "Negación",
                    "adverb": "Adverbio",
                    "prepositional_phrase": "Frase Preposicional",
                    "infinitive": "Infinitivo"
                }
                # Filter options based on what's actually in the sentence
                available_roles = {k: v for k, v in role_options.items() if k in roles_map}
                
                if not available_roles:
                    st.warning("Esta oración no tiene roles etiquetados aún.")
                    return

                target_role = st.radio(
                    "¿Qué quieres identificar?",
                    list(available_roles.keys()),
                    format_func=lambda x: available_roles[x],
                    key=f"role_radio_l{lesson_number}_{s_idx}"
                )
            
            with col2:
                # Tokenize for selection
                tokens = sentence.latin_text.split()
                
                st.markdown(f"Selecciona las palabras que funcionan como **{available_roles[target_role]}**:")
                
                selected_indices = st.multiselect(
                    "Palabras:",
                    options=range(len(tokens)),
                    format_func=lambda i: tokens[i],
                    key=f"word_sel_l{lesson_number}_{s_idx}",
                    label_visibility="collapsed"
                )
                
                st.markdown("###")
                
                if st.button("Verificar Análisis", key=f"check_analysis_l{lesson_number}_{s_idx}", width="stretch"):
                    correct_indices = roles_map.get(target_role, [])
                    
                    # Compare sets
                    if set(selected_indices) == set(correct_indices):
                        st.success(f"¡Correcto! '{' '.join([tokens[i] for i in correct_indices])}' es el {available_roles[target_role]}.")
                        st.balloons()
                    elif not selected_indices:
                        st.warning("Debes seleccionar al menos una palabra.")
                    else:
                        st.error("Incorrecto. Revisa tu selección e intenta de nuevo.")
                        
            # Show translation
            st.markdown("---")
            with st.expander("👁️ Ver Traducción al Español"):
                st.info(f"**Traducción:** {sentence.spanish_translation}")


# ============================================================================
# EJERCICIOS INTERACTIVOS (Reemplazan st.write de JSON crudo)
# ============================================================================

def render_vocabulary_match_exercise(exercises: list, lesson_number: int, user_id: int = 1, exercise_index: int = 0, key_suffix: str = ""):
    """
    Renderiza ejercicio de emparejamiento de vocabulario con UI interactiva.
    
    Args:
        exercises: Lista de diccionarios con 'latin' y 'spanish'
        lesson_number: Número de lección
        user_id: ID del usuario
        exercise_index: Índice del ejercicio (para diferenciar múltiples ejercicios en la misma lección)
        key_suffix: Sufijo adicional para diferenciar ejercicios estáticos de dinámicos (ej: "static", "dyn")
    """
    if not exercises:
        st.info("No hay suficiente vocabulario para generar ejercicios de emparejamiento.")
        return
    
    st.markdown("#### 🔗 Empareja Latín con Español")
    
    # Inicializar estado - incluir exercise_index y key_suffix para evitar duplicados
    key_prefix = f"vocab_match_l{lesson_number}_ex{exercise_index}_{key_suffix}" if key_suffix else f"vocab_match_l{lesson_number}_ex{exercise_index}"
    if f"{key_prefix}_shuffled" not in st.session_state:
        import random
        spanish_order = list(range(len(exercises)))
        random.shuffle(spanish_order)
        st.session_state[f"{key_prefix}_shuffled"] = spanish_order
        st.session_state[f"{key_prefix}_answers"] = {}
        st.session_state[f"{key_prefix}_submitted"] = False
    
    shuffled = st.session_state[f"{key_prefix}_shuffled"]
    answers = st.session_state[f"{key_prefix}_answers"]
    submitted = st.session_state[f"{key_prefix}_submitted"]
    
    # Crear opciones españolas mezcladas
    spanish_options = [exercises[i]["spanish"] for i in shuffled]
    
    # Mostrar pares
    for i, ex in enumerate(exercises):
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Mostrar palabra latina
            if submitted:
                correct_answer = ex["spanish"]
                user_answer = answers.get(i, "")
                if user_answer == correct_answer:
                    st.markdown(f"✅ **{ex['latin']}**")
                else:
                    st.markdown(f"❌ **{ex['latin']}**")
            else:
                st.markdown(f"**{ex['latin']}**")
        
        with col2:
            if submitted:
                correct_answer = ex["spanish"]
                user_answer = answers.get(i, "")
                if user_answer == correct_answer:
                    st.success(f"{user_answer}")
                else:
                    st.error(f"Tu respuesta: {user_answer}")
                    st.caption(f"Correcta: {correct_answer}")
            else:
                selected = st.selectbox(
                    f"Selecciona traducción para '{ex['latin']}'",
                    options=["-- Selecciona --"] + spanish_options,
                    key=f"{key_prefix}_select_{i}",
                    label_visibility="collapsed"
                )
                if selected != "-- Selecciona --":
                    answers[i] = selected
    
    st.markdown("---")
    
    # Botones de acción
    col1, col2 = st.columns(2)
    
    with col1:
        if not submitted:
            if st.button("✅ Verificar Respuestas", key=f"{key_prefix}_submit", width="stretch"):
                st.session_state[f"{key_prefix}_answers"] = answers
                st.session_state[f"{key_prefix}_submitted"] = True
                st.rerun()
    
    with col2:
        if st.button("🔄 Nuevo Ejercicio", key=f"{key_prefix}_reset", width="stretch"):
            # Limpiar estado
            for key in list(st.session_state.keys()):
                if key.startswith(key_prefix):
                    del st.session_state[key]
            st.rerun()
    
    # Mostrar puntuación si está enviado
    if submitted:
        correct_count = sum(1 for i, ex in enumerate(exercises) if answers.get(i) == ex["spanish"])
        total = len(exercises)
        pct = (correct_count / total) * 100 if total > 0 else 0
        
        st.markdown("---")
        if pct >= 80:
            st.success(f"🎉 ¡Excelente! {correct_count}/{total} correctas ({pct:.0f}%)")
        elif pct >= 50:
            st.warning(f"👍 ¡Bien! {correct_count}/{total} correctas ({pct:.0f}%)")
        else:
            st.error(f"📚 Sigue practicando. {correct_count}/{total} correctas ({pct:.0f}%)")


def render_multiple_choice_exercise(questions: list, lesson_number: int, user_id: int = 1, key_suffix: str = ""):
    """
    Renderiza ejercicio de opción múltiple con UI interactiva.
    
    Args:
        questions: Lista de preguntas con 'question', 'options', 'correct_answer', 'explanation'
        lesson_number: Número de lección
        user_id: ID del usuario
        key_suffix: Sufijo para claves únicas (ej. "static", "dyn")
    """
    if not questions:
        st.info("No hay suficientes datos para generar ejercicios de opción múltiple.")
        return
    
    st.markdown("#### 📋 Opción Múltiple")
    
    key_prefix = f"mc_l{lesson_number}_{key_suffix}" if key_suffix else f"mc_l{lesson_number}"
    
    for q_idx, q in enumerate(questions):
        st.markdown(f"**Pregunta {q_idx + 1}:** {q['question']}")
        
        answer_key = f"{key_prefix}_q{q_idx}"
        checked_key = f"{key_prefix}_checked_{q_idx}"
        
        # Radio buttons para opciones
        selected = st.radio(
            f"Opciones para pregunta {q_idx + 1}",
            options=q["options"],
            key=answer_key,
            label_visibility="collapsed"
        )
        
        # Botón de verificar
        if st.button(f"Verificar", key=f"{key_prefix}_check_{q_idx}"):
            st.session_state[checked_key] = True
        
        # Mostrar resultado si verificado
        if st.session_state.get(checked_key, False):
            is_correct = selected == q["correct_answer"]
            
            # Record attempt (only once per verification)
            attempt_recorded_key = f"{key_prefix}_recorded_{q_idx}"
            if not st.session_state.get(attempt_recorded_key, False):
                with get_session() as session:
                    record_exercise_attempt(
                        session=session,
                        user_id=user_id,
                        lesson_number=lesson_number,
                        exercise_type="mc",
                        is_correct=is_correct,
                        user_answer=selected,
                        correct_answer=q["correct_answer"]
                    )
                st.session_state[attempt_recorded_key] = True
            
            if is_correct:
                st.success(f"✅ ¡Correcto! {q.get('explanation', '')}")
            else:
                st.error(f"❌ Incorrecto. La respuesta correcta es: **{q['correct_answer']}**")
                if q.get('explanation'):
                    st.caption(q['explanation'])
        
        st.markdown("---")


def render_sentence_completion_exercise(questions: list, lesson_number: int, user_id: int = 1, key_suffix: str = ""):
    """
    Renderiza ejercicio de completar oraciones con UI interactiva.
    
    Args:
        questions: Lista con 'question', 'options', 'correct_answer', 'explanation'
        lesson_number: Número de lección
        user_id: ID del usuario
        key_suffix: Sufijo para claves únicas
    """
    if not questions:
        st.info("No hay suficientes oraciones para generar ejercicios de completar.")
        return
    
    st.markdown("#### ✏️ Completa la Oración")
    
    key_prefix = f"fill_l{lesson_number}_{key_suffix}" if key_suffix else f"fill_l{lesson_number}"
    
    for q_idx, q in enumerate(questions):
        # Mostrar oración con hueco
        st.markdown(
            f"""
            <div style='background: #f8f9fa; padding: 15px; border-radius: 8px; 
                        border-left: 4px solid #8b4513; margin-bottom: 10px;'>
                <span style='font-size: 1.1em;'>{q['question'].replace('<br>', '')}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        answer_key = f"{key_prefix}_q{q_idx}"
        checked_key = f"{key_prefix}_checked_{q_idx}"
        
        # Opciones como botones en columnas
        selected = st.radio(
            f"Selecciona la palabra correcta:",
            options=q["options"],
            key=answer_key,
            horizontal=True
        )
        
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button(f"Verificar", key=f"{key_prefix}_check_{q_idx}"):
                st.session_state[checked_key] = True
        
        # Mostrar resultado
        if st.session_state.get(checked_key, False):
            if selected == q["correct_answer"]:
                st.success(f"✅ ¡Correcto! La palabra es **{q['correct_answer']}**")
            else:
                st.error(f"❌ Incorrecto. La respuesta correcta es: **{q['correct_answer']}**")
            
            if q.get('explanation'):
                st.caption(f"💡 {q['explanation']}")
        
        st.markdown("---")
