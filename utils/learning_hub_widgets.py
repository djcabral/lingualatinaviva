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
import time

# ============================================================================
# GAMIFICATION ENGINE (New)
# ============================================================================

def _init_game_session(session_key: str, total_items: int):
    """Initializes the game session state if not present."""
    if f"{session_key}_state" not in st.session_state:
        st.session_state[f"{session_key}_state"] = "INTRO" # INTRO, PLAYING, FEEDBACK, VICTORY
        st.session_state[f"{session_key}_score"] = 0
        st.session_state[f"{session_key}_progress"] = 0
        st.session_state[f"{session_key}_streak"] = 0
        st.session_state[f"{session_key}_total"] = total_items
        st.session_state[f"{session_key}_answers"] = {} # Store user answers

def render_mission_intro(title: str, objective: str, xp_reward: int, on_start):
    """Renders the pre-exercise mission card."""
    st.markdown(
        f"""
        <div style='background: linear-gradient(135deg, #ffffff, #f0fdf4); 
                    padding: 30px; border-radius: 15px; border: 2px solid #bbf7d0; 
                    text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px;'>
            <div style='font-size: 3rem; margin-bottom: 10px;'>📜</div>
            <h2 style='color: #166534; margin: 0;'>Nueva Misión: {title}</h2>
            <p style='font-size: 1.2rem; color: #374151; margin: 15px 0;'>{objective}</p>
            <div style='background: #dcfce7; color: #15803d; display: inline-block; 
                        padding: 5px 15px; border-radius: 20px; font-weight: bold; margin-bottom: 20px;'>
                🏆 Recompensa: {xp_reward} XP
            </div>
            <br>
        </div>
        """,
        unsafe_allow_html=True
    )
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 ¡Comenzar Misión!", type="primary", use_container_width=True, key=f"start_{title}"):
            on_start()
            st.rerun()

def render_mission_hud(current: int, total: int, streak: int):
    """Renders the persistent progress bar and stats."""
    progress = current / total if total > 0 else 0
    st.progress(progress)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.caption(f"Progreso: {current}/{total}")
    with col2:
        if streak > 1:
            st.markdown(f"🔥 **Racha: {streak}**")

def render_juicy_feedback(is_correct: bool, explanation: str, correct_answer: str = None, on_continue=None, key: str = None):
    """Renders the immediate feedback with style."""
    
    if is_correct:
        bg_color = "#dcfce7" # Green-100
        border_color = "#22c55e"
        text_color = "#15803d"
        title = random.choice(["¡Optime!", "¡Bene factum!", "¡Recte!", "¡Excellens!"])
        icon = "🌟"
    else:
        bg_color = "#fee2e2" # Red-100
        border_color = "#ef4444" 
        text_color = "#b91c1c"
        title = "Errare humanum est..."
        icon = "⚠️"
        
    st.markdown(
        f"""
        <div style='background: {bg_color}; padding: 20px; border-radius: 12px; 
                    border: 2px solid {border_color}; margin: 20px 0; animation: fadeIn 0.5s;'>
            <div style='font-size: 1.5rem; font-weight: bold; color: {text_color}; display: flex; align-items: center; gap: 10px;'>
                <span>{icon}</span> {title}
            </div>
            <div style='color: {text_color}; margin-top: 10px;'>
                {explanation.replace('**', '<b>').replace('</b><b>', '</b>')}
            </div>
            {f"<div style='margin-top:10px; font-weight:bold;'>Respuesta correcta: {correct_answer}</div>" if not is_correct and correct_answer else ""}
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    if on_continue:
        # Use provided key or fallback to timestamp (less safe but OK if unique key provided usually)
        btn_key = f"cont_{key}" if key else f"cont_{int(time.time())}"
        if st.button("continuar ➡️", type="primary", key=btn_key):
            on_continue()
            st.rerun()

def render_mission_victory(score: int, total: int, xp_earned: int, on_finish):
    """Renders the summary screen."""
    percentage = (score / total) * 100 if total > 0 else 0
    
    stars = "⭐"
    if percentage > 50: stars += "⭐"
    if percentage > 90: stars += "⭐"
    
    msg = "¡Misión Cumplida!" if percentage >= 60 else "Misión Finalizada"
    
    st.markdown(
        f"""
        <div style='text-align: center; padding: 40px; background: #fff; border-radius: 20px; border: 1px solid #e5e7eb;'>
            <div style='font-size: 4rem; margin-bottom: 10px;'>{stars}</div>
            <h1 style='color: #1e3a8a; margin: 0;'>{msg}</h1>
            <p style='font-size: 1.5rem; color: #4b5563;'>Obtuviste {score}/{total} aciertos</p>
            <div style='margin: 30px 0;'>
                <span style='background: #fef08a; padding: 10px 20px; border-radius: 30px; font-weight: bold; color: #854d0e; font-size: 1.2rem;'>
                    +{xp_earned} XP Ganados
                </span>
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    if st.button("🔙 Volver al Tablero", type="primary", use_container_width=True):
        on_finish()
        st.rerun()



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
            
            # Obtener oraciones ya completadas por el usuario
            from database import ExerciseAttempt
            attempts = session.exec(
                select(ExerciseAttempt)
                .where(
                    ExerciseAttempt.user_id == user_id,
                    ExerciseAttempt.lesson_number == lesson_number,
                    ExerciseAttempt.exercise_type == "translation",
                    ExerciseAttempt.is_correct == True
                )
            ).all()
            
            # Extraer IDs de oraciones completadas (parseando exercise_config JSON)
            import json
            completed_ids = set()
            for attempt in attempts:
                try:
                    config = json.loads(attempt.exercise_config)
                    if "sentence_id" in config:
                        completed_ids.add(config["sentence_id"])
                except:
                    pass
            
            # Mostrar resumen
            completed_count = len([s for s in sentences if s.id in completed_ids])
            st.markdown(f"**{len(sentences)} oraciones** para practicar ({completed_count} completadas)")
            
            # Función de formateo para el selector
            def format_sentence_option(i):
                s = sentences[i]
                prefix = "✅ " if s.id in completed_ids else ""
                return f"{prefix}Oración {i+1} (Nivel {s.complexity_level})"

            # Selector de oración
            sentence_idx = st.selectbox(
                "Selecciona una oración:",
                range(len(sentences)),
                format_func=format_sentence_option,
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
                    tracker_record_attempt(
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
                    tracker_record_attempt(
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
                    tracker_record_attempt(
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
    
    # 1. Initialize Session
    key_prefix = f"vocab_match_l{lesson_number}_ex{exercise_index}_{key_suffix}"
    
    if f"{key_prefix}_state" not in st.session_state:
        _init_game_session(key_prefix, len(exercises))
        # Initial Shuffle Setup
        # Initial Shuffle Setup
        spanish_order = list(range(len(exercises)))
        random.shuffle(spanish_order)
        st.session_state[f"{key_prefix}_shuffled_indices"] = spanish_order
        st.session_state[f"{key_prefix}_current_idx"] = 0

    state = st.session_state[f"{key_prefix}_state"]
    current_idx = st.session_state[f"{key_prefix}_current_idx"]
    shuffled_indices = st.session_state[f"{key_prefix}_shuffled_indices"]
    
    # 2. Render State Machine
    if state == "INTRO":
        def start_mission():
            st.session_state[f"{key_prefix}_state"] = "PLAYING"
            
        render_mission_intro(
            title="Conexión de Vocabulario", 
            objective=f"Empareja correctamente {len(exercises)} pares de palabras.",
            xp_reward=10, 
            on_start=start_mission
        )

    elif state == "PLAYING":
        render_mission_hud(
            current=current_idx, 
            total=len(exercises), 
            streak=st.session_state[f"{key_prefix}_streak"]
        )
        
        # Get current question based on shuffled index
        # We iterate through the exercises one by one in the shuffled order? 
        # Or do we show ALL matches at once? 
        # The previous implementation showed ALL matches at once.
        # Gamified approach usually implies "One by one" flow for better "Juicy" feedback loop.
        # Let's switch to One-by-One flow.
        
        ex_real_idx = shuffled_indices[current_idx]
        ex = exercises[ex_real_idx]
        
        st.markdown(f"### ¿Qué significa **{ex['latin']}**?")
        
        # Generate options (Correct + 3 random distractors)
        # We need options to be consistent during the question, so store them?
        # For simplicity, let's regenerate or store. Storing is safer.
        if f"{key_prefix}_opts_{current_idx}" not in st.session_state:
            options = [ex['spanish']]
            # Add distractors
            potential_distractors = [e['spanish'] for i, e in enumerate(exercises) if i != ex_real_idx]
            if len(potential_distractors) < 3:
                # Not enough distinct items, just take what we have
                options.extend(potential_distractors)
            else:
                options.extend(random.sample(potential_distractors, 3))
            random.shuffle(options)
            st.session_state[f"{key_prefix}_opts_{current_idx}"] = options
            
        options = st.session_state[f"{key_prefix}_opts_{current_idx}"]
        
        # UI for Options
        col1, col2 = st.columns(2)
        for i, opt in enumerate(options):
            # Split into 2 columns
            with (col1 if i % 2 == 0 else col2):
                if st.button(opt, key=f"{key_prefix}_opt_{current_idx}_{i}", use_container_width=True):
                    # Check Answer
                    is_correct = (opt == ex['spanish'])
                    
                    # Update State
                    st.session_state[f"{key_prefix}_last_correct"] = is_correct
                    st.session_state[f"{key_prefix}_last_explanation"] = f"**{ex['latin']}** significa **{ex['spanish']}**"
                    st.session_state[f"{key_prefix}_last_answer"] = ex['spanish'] # Correct answer
                    
                    if is_correct:
                        st.session_state[f"{key_prefix}_score"] += 1
                        st.session_state[f"{key_prefix}_streak"] += 1
                        # Record success attempt in DB background
                        with get_session() as session:
                             record_exercise_attempt(
                                session,
                                user_id, lesson_number, "vocab_match", True, opt, ex['spanish']
                            )
                    else:
                        st.session_state[f"{key_prefix}_streak"] = 0
                        # Record fail attempt
                        with get_session() as session:
                            record_exercise_attempt(
                                session,
                                user_id, lesson_number, "vocab_match", False, opt, ex['spanish']
                            )
                        
                    st.session_state[f"{key_prefix}_state"] = "FEEDBACK"
                    st.rerun()

    elif state == "FEEDBACK":
        render_mission_hud(
            current=current_idx + 1, # Show as completed step
            total=len(exercises), 
            streak=st.session_state[f"{key_prefix}_streak"]
        )
        
        def next_question():
            # Advance index
            new_idx = current_idx + 1
            if new_idx >= len(exercises):
                st.session_state[f"{key_prefix}_state"] = "VICTORY"
            else:
                st.session_state[f"{key_prefix}_current_idx"] = new_idx
                st.session_state[f"{key_prefix}_state"] = "PLAYING"
                
        render_juicy_feedback(
            is_correct=st.session_state[f"{key_prefix}_last_correct"],
            explanation=st.session_state[f"{key_prefix}_last_explanation"],
            correct_answer=st.session_state[f"{key_prefix}_last_answer"],
            on_continue=next_question,
            key=f"{key_prefix}_{current_idx}"
        )

    elif state == "VICTORY":
        def restart():
            # Clear state to restart
            keys_to_del = [k for k in st.session_state.keys() if k.startswith(key_prefix)]
            for k in keys_to_del:
                del st.session_state[k]
                
        render_mission_victory(
            score=st.session_state[f"{key_prefix}_score"],
            total=len(exercises),
            xp_earned=10, # Reward logic
            on_finish=restart
        )


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
"""
Learning Hub Widgets - NEW EXERCISE TYPES
Widgets adicionales para ejercicios de traducción, morfología y reconocimiento de patrones.
"""

import streamlit as st
from typing import List, Dict
from difflib import SequenceMatcher


def render_translation_latin_spanish_exercise(
    exercise: Dict,
    lesson_number: int,
    exercise_index: int = 0,
    user_id: int = 1,
    key_suffix: str = ""
):
    """
    Renderiza ejercicio de traducción Latín → Español con hints.
    
    Args:
        exercise: Dict con 'latin', 'expected_spanish', 'hints'
        lesson_number: Número de lección
        exercise_index: Índice del ejercicio
        user_id: ID del usuario
        key_suffix: Sufijo para claves únicas
    """
    st.markdown("#### 📖 Traducción: Latín → Español")
    
    key_prefix = f"trans_ls_l{lesson_number}_ex{exercise_index}_{key_suffix}"
    
    # Mostrar texto latino
    st.markdown(
        f"""
        <div style='background: linear-gradient(135deg, rgba(139,69,19,0.1), rgba(210,180,140,0.1));
                    padding: 25px; border-radius: 10px; text-align: center; 
                    border-left: 5px solid #8b4513; margin-bottom: 20px;'>
            <div style='font-size: 1.8em; font-weight: bold; font-style: italic; color: #8b4513;'>
                {exercise['latin']}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Hints expandibles
    if 'hints' in exercise and exercise['hints']:
        with st.expander("💡 Ver pistas morfológicas"):
            for word, hint in exercise['hints'].items():
                st.markdown(f"- **{word}**: {hint}")
    
    # Área de traducción
    user_translation = st.text_area(
        "Tu traducción al español:",
        height=80,
        key=f"{key_prefix}_input",
        placeholder="Escribe tu traducción aquí..."
    )
    
    # Botón de verificación
    if st.button("✅ Verificar", key=f"{key_prefix}_check"):
        if user_translation.strip():
            # Calcular similitud
            expected = exercise['expected_spanish'].lower().strip()
            user_input = user_translation.lower().strip()
            similarity = SequenceMatcher(None, expected, user_input).ratio()
            
            if similarity >= 0.9:
                st.success(f"✅ ¡Excelente! Tu traducción es correcta.")
                st.balloons()
            elif similarity >= 0.7:
                st.warning(f"~📊 Muy cerca. Compara con la respuesta correcta.")
                with st.expander("Ver respuesta correcta"):
                    st.info(f"**Respuesta**: {exercise['expected_spanish']}")
            else:
                st.error(f"❌ Revisa tu traducción. Compara con la respuesta correcta.")
                with st.expander("Ver respuesta correcta"):
                    st.info(f"**Respuesta**: {exercise['expected_spanish']}")
                    if 'explanation' in exercise:
                        st.caption(f"💡 {exercise['explanation']}")
        else:
            st.warning("Escribe una traducción antes de verificar.")


def render_translation_spanish_latin_exercise(
    exercise: Dict,
    lesson_number: int,
    exercise_index: int = 0,
    user_id: int = 1,
    key_suffix: str = ""
):
    """
    Renderiza ejercicio de traducción inversa Español → Latín con banco de palabras.
    
    Args:
        exercise: Dict con 'spanish', 'expected_latin', 'word_bank', 'morphology_hints'
        lesson_number: Número de lección
        exercise_index: Índice del ejercicio
        user_id: ID del usuario
        key_suffix: Sufijo para claves únicas
    """
    st.markdown("#### 🔄 Traducción Inversa: Español → Latín")
    
    key_prefix = f"trans_sl_l{lesson_number}_ex{exercise_index}_{key_suffix}"
    
    # Mostrar texto español
    st.markdown(
        f"""
        <div style='background: #e8f5e9; padding: 20px; border-radius: 10px; 
                    border-left: 5px solid #4caf50; margin-bottom: 15px;'>
            <div style='font-size: 1.5em; font-weight: bold; color: #2e7d32;'>
                {exercise['spanish']}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Banco de palabras
    if 'word_bank' in exercise and exercise['word_bank']:
        st.markdown("**Banco de palabras:**")
        st.code(" | ".join(exercise['word_bank']))
    
    # Hints morfológicos
    if exercise.get('morphology_hints', False):
        with st.expander("🔍 Ayuda Morfológica"):
            st.info("""
            **Recuerda:**
            - Sujeto: nominativo
            - Objeto directo: acusativo
            - Verbo: concuerda con el sujeto en persona y número
            - Adjetivos: concuerdan en género, número y caso
            """)
    
    # Área de traducción
    user_latin = st.text_input(
        "Tu traducción al latín:",
        key=f"{key_prefix}_input",
        placeholder="Escribe la oración en latín..."
    )
    
    # Botón de verificación
    if st.button("✅ Verificar", key=f"{key_prefix}_check"):
        if user_latin.strip():
            expected = exercise['expected_latin'].lower().strip()
            user_input = user_latin.lower().strip()
            
            if user_input == expected:
                st.success("✅ ¡Perfecto! Traducción correcta.")
                st.balloons()
            else:
                # Calcular similitud
                similarity = SequenceMatcher(None, expected, user_input).ratio()
                if similarity >= 0.8:
                    st.warning(f"~📊 Muy cerca. Revisa el orden o las formas.")
                    st.info(f"**Respuesta esperada**: {exercise['expected_latin']}")
                else:
                    st.error(f"❌ Revisa tu traducción.")
                    st.info(f"**Respuesta correcta**: {exercise['expected_latin']}")
                    if 'explanation' in exercise:
                        st.caption(f"💡 {exercise['explanation']}")
        else:
            st.warning("Escribe una traducción antes de verificar.")


def render_morphology_analysis_exercise(
    exercise: Dict,
    lesson_number: int,
    exercise_index: int = 0,
    user_id: int = 1,
    key_suffix: str = ""
):
    """
    Renderiza ejercicio de análisis morfológico.
    
    Args:
        exercise: Dict con 'form', 'expected' (case, number, gender, syntactic_function), 'hint'
        lesson_number: Número de lección
        exercise_index: Índice del ejercicio
        user_id: ID del usuario
        key_suffix: Sufijo para claves únicas
    """
    st.markdown("#### 🔬 Análisis Morfológico")
    
    key_prefix = f"morph_l{lesson_number}_ex{exercise_index}_{key_suffix}"
    
    # Mostrar forma
    st.markdown(
        f"""
        <div style='background: #fff3e0; padding: 20px; border-radius: 10px; 
                    text-align: center; border: 3px dashed #ff9800;'>
            <div style='font-size: 2em; font-weight: bold; color: #e65100;'>
                {exercise['form']}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("###")
    
    # Hint si existe
    if 'hint' in exercise:
        st.caption(f"💡 {exercise['hint']}")
    
    # Formulario de análisis
    expected = exercise['expected']
    
    col1, col2 = st.columns(2)
    
    with col1:
        case_options = ["nominativo", "genitivo", "dativo", "acusativo", "ablativo", "vocativo"]
        selected_case = st.selectbox(
            "Caso:",
            options=case_options,
            key=f"{key_prefix}_case"
        )
        
        number_options = ["singular", "plural"]
        selected_number = st.selectbox(
            "Número:",
            options=number_options,
            key=f"{key_prefix}_number"
        )
    
    with col2:
        gender_options = ["masculino", "femenino", "neutro"]
        selected_gender = st.selectbox(
            "Género:",
            options=gender_options,
            key=f"{key_prefix}_gender"
        )
        
        function_options = [
            "sujeto", "objeto_directo", "objeto_indirecto",
            "complemento_del_nombre", "complemento_circunstancial",
            "atributo", "predicado"
        ]
        selected_function = st.selectbox(
            "Función sintáctica:",
            options=function_options,
            key=f"{key_prefix}_function"
        )
    
    # Verificar
    if st.button("✅ Verificar Análisis", key=f"{key_prefix}_check"):
        is_correct = (
            selected_case == expected.get('case') and
            selected_number == expected.get('number') and
            selected_gender == expected.get('gender') and
            selected_function == expected.get('syntactic_function')
        )
        
        if is_correct:
            st.success("✅ ¡Análisis correcto en todos los aspectos!")
            st.balloons()
        else:
            st.error("❌ Revisa tu análisis. Compara con la respuesta:")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("**Tu análisis:**")
                st.write(f"Caso: {selected_case}")
                st.write(f"Número: {selected_number}")
                st.write(f"Género: {selected_gender}")
                st.write(f"Función: {selected_function}")
            
            with col_b:
                st.markdown("**Análisis correcto:**")
                st.write(f"Caso: {expected.get('case')}")
                st.write(f"Número: {expected.get('number')}")
                st.write(f"Género: {expected.get('gender')}")
                st.write(f"Función: {expected.get('syntactic_function')}")


def render_sentence_builder_exercise(
    exercise: Dict,
    lesson_number: int,
    exercise_index: int = 0,
    user_id: int = 1,
    key_suffix: str = ""
):
    """
    Renderiza ejercicio de construcción de oraciones.
    
    Args:
        exercise: Dict con 'words', 'expected_order', 'translation', 'explanation'
        lesson_number: Número de lección
        exercise_index: Índice del ejercicio
        user_id: ID del usuario
        key_suffix: Sufijo para claves únicas
    """
    st.markdown("#### 🏗️ Construcción de Oraciones")
    
    key_prefix = f"builder_l{lesson_number}_ex{exercise_index}_{key_suffix}"
    
    st.info("📝 Ordena las palabras para formar una oración correcta")
    
    # Inicializar orden si no existe
    if f"{key_prefix}_order" not in st.session_state:
        import random
        words = exercise['words'].copy()
        random.shuffle(words)
        st.session_state[f"{key_prefix}_order"] = words
    
    current_order = st.session_state[f"{key_prefix}_order"]
    
    # Mostrar palabras desordenadas
    st.markdown("**Palabras disponibles:**")
    cols = st.columns(len(current_order))
    for i, col in enumerate(cols):
        with col:
            st.markdown(
                f"""
                <div style='background: #e3f2fd; padding: 10px; border-radius: 5px; 
                            text-align: center; border: 2px solid #2196f3;'>
                    <b>{current_order[i]}</b>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    st.markdown("###")
    
    # Selector de orden
    st.markdown("**Ordena las palabras:**")
    selected_order = []
    for i in range(len(current_order)):
        remaining = [w for w in current_order if w not in selected_order]
        if remaining:
            word = st.selectbox(
                f"Posición {i+1}:",
                options=remaining,
                key=f"{key_prefix}_pos_{i}"
            )
            selected_order.append(word)
    
    # Mostrar oración formada
    if len(selected_order) == len(current_order):
        st.markdown("**Tu oración:**")
        st.markdown(
            f"""
            <div style='background: #f5f5f5; padding: 15px; border-radius: 8px; 
                        text-align: center; font-size: 1.3em; font-weight: bold;'>
                {' '.join(selected_order)}
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown("###")
    
    # Botones
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Verificar", key=f"{key_prefix}_check"):
            if selected_order == exercise['expected_order']:
                st.success("✅ ¡Correcto! Oración bien formada.")
                st.info(f"**Traducción**: {exercise['translation']}")
                if 'explanation' in exercise:
                    st.caption(f"💡 {exercise['explanation']}")
                st.balloons()
            else:
                st.error("❌ Orden incorrecto. Intenta de nuevo.")
                st.info(f"**Pista**: La traducción es '{exercise['translation']}'")
    
    with col2:
        if st.button("🔀 Mezclar de nuevo", key=f"{key_prefix}_shuffle"):
            import random
            words = exercise['words'].copy()
            random.shuffle(words)
            st.session_state[f"{key_prefix}_order"] = words
            st.rerun()


def render_transformation_exercise(
    exercise: Dict,
    lesson_number: int,
    exercise_index: int = 0,
    user_id: int = 1,
    key_suffix: str = ""
):
    """
    Renderiza ejercicio de transformación de oraciones.
    
    Args:
        exercise: Dict con 'sentence', 'transformation', 'expected', 'explanation'
        lesson_number: Número de lección
        exercise_index: Índice del ejercicio
        user_id: ID del usuario
        key_suffix: Sufijo para claves únicas
    """
    st.markdown("#### 🔄 Transformación de Oraciones")
    
    key_prefix = f"transf_l{lesson_number}_ex{exercise_index}_{key_suffix}"
    
    # Mostrar oración original
    st.markdown("**Oración original:**")
    st.markdown(
        f"""
        <div style='background: #e8f5e9; padding: 15px; border-radius: 8px; 
                    border-left: 5px solid #4caf50;'>
            <span style='font-size: 1.3em; font-weight: bold;'>{exercise['sentence']}</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Instrucción de transformación
    transformation_instructions = {
        "plural_subject": "Cambia el sujeto a plural y ajusta el verbo",
        "passive_voice": "Convierte la oración a voz pasiva",
        "singular_to_plural": "Cambia todos los elementos a plural",
        "change_tense": "Cambia el tiempo verbal según se indica"
    }
    
    transformation = exercise.get('transformation', '')
    instruction = exercise.get('instructions', transformation_instructions.get(transformation, "Transforma la oración"))
    
    st.info(f"📝 **Tarea**: {instruction}")
    
    # Área de respuesta
    user_answer = st.text_input(
        "Oración transformada:",
        key=f"{key_prefix}_input",
        placeholder="Escribe la oración transformada..."
    )
    
    # Verificar
    if st.button("✅ Verificar", key=f"{key_prefix}_check"):
        if user_answer.strip():
            expected = exercise['expected'].lower().strip()
            user_input = user_answer.lower().strip()
            
            if user_input == expected:
                st.success("✅ ¡Transformación correcta!")
                if 'explanation' in exercise:
                    st.info(f"💡 {exercise['explanation']}")
                st.balloons()
            else:
                similarity = SequenceMatcher(None, expected, user_input).ratio()
                if similarity >= 0.8:
                    st.warning("~📊 Muy cerca. Compara con la respuesta correcta:")
                else:
                    st.error("❌ Revisa tu respuesta:")
                
                st.info(f"**Respuesta correcta**: {exercise['expected']}")
                if 'explanation' in exercise:
                    st.caption(f"💡 {exercise['explanation']}")
        else:
            st.warning("Escribe una respuesta antes de verificar.")


def render_pattern_recognition_exercise(
    exercise: Dict,
    lesson_number: int,
    exercise_index: int = 0,
    user_id: int = 1,
    key_suffix: str = ""
):
    """
    Renderiza ejercicio de reconocimiento de patrones sintácticos.
    
    Args:
        exercise: Dict con 'text', 'pattern', 'expected_identification', 'hint', 'explanation'
        lesson_number: Número de lección
        exercise_index: Índice del ejercicio
        user_id: ID del usuario
        key_suffix: Sufijo para claves únicas
    """
    st.markdown("#### 🎯 Reconocimiento de Patrones")
    
    key_prefix = f"pattern_l{lesson_number}_ex{exercise_index}_{key_suffix}"
    
    # Descripción del patrón
    pattern_descriptions = {
        "acusativo_objeto_directo": "Acusativo como Objeto Directo",
        "ablativo_absoluto": "Ablativo Absoluto",
        "aci": "Acusativo con Infinitivo (AcI)",
        "genitivo_posesivo": "Genitivo Posesivo",
        "dativo_interes": "Dativo de Interés"
    }
    
    pattern = exercise.get('pattern', '')
    pattern_name = pattern_descriptions.get(pattern, pattern.replace('_', ' ').title())
    
    st.info(f"🔍 **Identifica**: {pattern_name}")
    
    # Mostrar texto
    st.markdown("**Texto en latín:**")
    st.markdown(
        f"""
        <div style='background: linear-gradient(135deg, #fff3e0, #ffe0b2); 
                    padding: 20px; border-radius: 10px; 
                    border: 2px solid #ff9800; margin: 15px 0;'>
            <div style='font-size: 1.4em; font-style: italic; color: #e65100; text-align: center;'>
                {exercise['text']}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Hint
    if 'hint' in exercise:
        with st.expander("💡 Ver pista"):
            st.caption(exercise['hint'])
    
    # Área de respuesta
    user_answer = st.text_input(
        f"Escribe las palabras que forman el patrón '{pattern_name}':",
        key=f"{key_prefix}_input",
        placeholder="Ejemplo: rosam, aquam"
    )
    
    # Verificar
    if st.button("✅ Verificar", key=f"{key_prefix}_check"):
        if user_answer.strip():
            expected = exercise['expected_identification'].lower().strip()
            user_input = user_answer.lower().strip()
            
            # Normalizar (quitar espacios extra, etc.)
            expected_words = set(w.strip() for w in expected.split(','))
            user_words = set(w.strip() for w in user_input.split(','))
            
            if expected_words == user_words:
                st.success(f"✅ ¡Correcto! '{exercise['expected_identification']}' es un {pattern_name}")
                if 'explanation' in exercise:
                    st.info(f"💡 {exercise['explanation']}")
                st.balloons()
            elif expected in user_input or user_input in expected:
                st.success(f"✅ ¡Correcto! Identificaste el patrón correctamente.")
                if 'explanation' in exercise:
                    st.info(f"💡 {exercise['explanation']}")
            else:
                st.error("❌ Revisa tu respuesta.")
                st.info(f"**Respuesta correcta**: {exercise['expected_identification']}")
                if 'explanation' in exercise:
                    st.caption(f"💡 {exercise['explanation']}")
        else:
            st.warning("Escribe una respuesta antes de verificar.")


# --- Consolidated Practice Renderer ---

def render_practice_content(lesson_number: int):
    """
    Renderiza el contenido de práctica unificado para una lección.
    Maneja la lógica de selección entre ejercicios estáticos curados.
    """
    st.markdown(f"### ⚔️ Práctica de Lección {lesson_number}")
    
    # 1. Taller de Traducción (Siempre disponible si hay datos)
    with st.expander("📝 Taller de Traducción (Guiado)", expanded=False):
        render_translation_workshop(lesson_number)
    
    st.divider()

    # 2. Selector Unificado de Ejercicios
    from utils.static_exercise_loader import get_all_exercise_types, load_static_exercises as load_static_db_exercises
    
    # Intentar cargar de ambas fuentes
    static_ex_v1 = get_all_exercise_types(lesson_number)
    static_ex_v2 = load_static_db_exercises(lesson_number)
    
    # Consolidar opciones disponibles
    available_options = {}
    
    # Mapeo de tipos a nombres amigables
    type_labels = {
        "vocabulary_match": "🔗 Emparejar Vocabulario",
        "multiple_choice": "📋 Opción Múltiple (General)",
        "sentence_completion": "✍️ Completar Oraciones",
        "translation_latin_spanish": "📖 Traducción Latín → Español",
        "translation_spanish_latin": "🔄 Traducción Español → Latín",
        "morphology_analysis": "🔬 Análisis Morfológico",
        "sentence_builder": "🏗️ Construcción de Oraciones",
        "transformation": "🔀 Transformaciones",
        "pattern_recognition": "🎯 Reconocimiento de Patrones"
    }
    
    # Detectar estáticos V1
    if static_ex_v1:
        if static_ex_v1.get("multiple_choice"):
            available_options["static_mc"] = ("Estático", static_ex_v1["multiple_choice"])
        if static_ex_v1.get("sentence_completion"):
             available_options["static_fill"] = ("Estático", static_ex_v1["sentence_completion"])
        if static_ex_v1.get("vocabulary_match"):
             available_options["static_vocab"] = ("Estático", static_ex_v1["vocabulary_match"])

    # Detectar estáticos V2 (Lista de ejercicios)
    if static_ex_v2 and 'exercises' in static_ex_v2:
        for ex in static_ex_v2['exercises']:
            ex_type = ex.get('type')
            # Agrupar por tipo para el selector
            key = f"db_{ex_type}"
            if key not in available_options:
                available_options[key] = ("DB", [])
            available_options[key][1].append(ex)

    if not available_options:
        st.info("No hay ejercicios estáticos disponibles para esta lección aún.")
        return

    # --- UI DEL SELECTOR ---
    
    st.info("Selecciona el tipo de actividad que deseas practicar hoy:")

    # Crear lista para selectbox
    options_keys = list(available_options.keys())
    
    selected_key = st.selectbox(
        "Actividad:",
        options=options_keys,
        format_func=lambda k: type_labels.get(k.replace("static_", "").replace("db_", ""), k)
    )
    
    st.markdown("---")
    
    # --- RENDERIZADO SEGÚN SELECCIÓN ---
    
    source_type, data = available_options[selected_key]
    
    if source_type == "Estático":
        # Renderizado V1
        if "mc" in selected_key:
            render_multiple_choice_exercise(data, lesson_number, key_suffix="consolidated_v1")
        elif "fill" in selected_key:
            render_sentence_completion_exercise(data, lesson_number, key_suffix="consolidated_v1")
        elif "vocab" in selected_key:
             for vm_idx, vm_ex in enumerate(data):
                if "pairs" in vm_ex:
                    render_vocabulary_match_exercise(vm_ex["pairs"], lesson_number, exercise_index=vm_idx, key_suffix="consolidated_v1")
                    
    elif source_type == "DB":
        # Renderizado V2
        exercises = data
        st.caption(f"{len(exercises)} ejercicio(s) disponible(s)")
        
        # Selector de ejercicio individual si hay más de uno
        if len(exercises) > 1:
            ex_idx = st.selectbox(
                "Selecciona ejercicio específico:",
                range(len(exercises)),
                format_func=lambda i: f"Ejercicio {i+1}",
                key=f"ex_selector_{selected_key}_l{lesson_number}"
            )
        else:
            ex_idx = 0
            
        exercise = exercises[ex_idx]
        real_type = selected_key.replace("db_", "")
        
        # Dispatcher - Usando las funciones ya definidas en este módulo
        if real_type == "vocabulary_match":
            pairs = exercise.get('pairs', [])
            render_vocabulary_match_exercise(pairs, lesson_number, exercise_index=ex_idx, key_suffix="consolidated_v2")
        elif real_type == "multiple_choice":
             questions = [{
                "question": exercise.get('question'),
                "options": exercise.get('options', []),
                "correct_answer": exercise['options'][exercise.get('correct', 0)] if 'correct' in exercise and 'options' in exercise else "",
                "explanation": exercise.get('explanation', '')
            }]
             render_multiple_choice_exercise(questions, lesson_number, key_suffix="consolidated_v2")
        elif real_type == "sentence_completion":
             questions = [{
                "question": exercise.get('sentence', ''),
                "options": exercise.get('options', []),
                "correct_answer": exercise['options'][exercise.get('correct', 0)] if 'correct' in exercise else "",
                "explanation": exercise.get('explanation', ''),
                "translation": exercise.get('translation', '')
            }]
             render_sentence_completion_exercise(questions, lesson_number, key_suffix="consolidated_v2")
        elif real_type == "translation_latin_spanish":
            render_translation_latin_spanish_exercise(exercise, lesson_number, ex_idx, key_suffix="consolidated_v2")
        elif real_type == "translation_spanish_latin":
            render_translation_spanish_latin_exercise(exercise, lesson_number, ex_idx, key_suffix="consolidated_v2")
        elif real_type == "morphology_analysis":
            render_morphology_analysis_exercise(exercise, lesson_number, ex_idx, key_suffix="consolidated_v2")
        elif real_type == "sentence_builder":
            render_sentence_builder_exercise(exercise, lesson_number, ex_idx, key_suffix="consolidated_v2")
        elif real_type == "transformation":
            render_transformation_exercise(exercise, lesson_number, ex_idx, key_suffix="consolidated_v2")
        elif real_type == "pattern_recognition":
            render_pattern_recognition_exercise(exercise, lesson_number, ex_idx, key_suffix="consolidated_v2")

# ============================================================================
# FINAL CHALLENGE WIDGET
# ============================================================================

def render_final_challenge(lesson_number: int, on_complete=None):
    """
    Renders the Final Challenge (Prueba Final) for the lesson.
    Reuses the game engine but with stricter rules (Exam Mode).
    """
    
    # 1. Initialize Exam Session
    key_prefix = f"final_challenge_l{lesson_number}"
    
    # Only if not initialized
    if f"{key_prefix}_state" not in st.session_state:
        # Generate exercises on the fly (Vocabulary + Grammar mix if possible)
        # For MVP: We use vocabulary matching but with 20 questions (or max available)
        
        # We need to fetch exercises
        from utils.exercise_generator import ExerciseGenerator
        with get_session() as session:
            generator = ExerciseGenerator(session)
            # Fetch a larger set for the exam
            exercises = generator.generate_vocabulary_match(lesson_number, count=20)
            
        st.session_state[f"{key_prefix}_exam_exercises"] = exercises
        _init_game_session(key_prefix, len(exercises))
        # Shuffle for exam
        import random
        spanish_order = list(range(len(exercises)))
        random.shuffle(spanish_order)
        st.session_state[f"{key_prefix}_shuffled_indices"] = spanish_order
        st.session_state[f"{key_prefix}_current_idx"] = 0

    # Retrieve State
    state = st.session_state[f"{key_prefix}_state"]
    exercises = st.session_state.get(f"{key_prefix}_exam_exercises", [])
    
    # Validation: Check if exercises are valid (have options) - Fix for cached old state
    if exercises and ('options' not in exercises[0]):
        del st.session_state[f"{key_prefix}_state"]
        del st.session_state[f"{key_prefix}_exam_exercises"]
        st.rerun()
    
    if not exercises:
        st.warning("No hay suficientes ejercicios para generar la prueba final.")
        if st.button("Reintentar Generación"):
            del st.session_state[f"{key_prefix}_state"]
            st.rerun()
        return

    # 2. Render State Machine
    if state == "INTRO":
        def start_exam():
            st.session_state[f"{key_prefix}_state"] = "PLAYING"
            
        st.markdown(f"### ⚔️ Prueba Final: Lección {lesson_number}")
        st.markdown("""
        Bienvenido a la prueba final. 
        
        *   **Reglas**: Debes completar todos los ejercicios.
        *   **Aprobación**: Necesitas un **80% de aciertos** para pasar.
        *   **Recompensa**: 50 XP y Desbloqueo del siguiente nivel.
        """)
        
        if st.button("🔥 COMENZAR PRUEBA", type="primary", key=f"{key_prefix}_start"):
            start_exam()
            st.rerun()

    elif state == "PLAYING":
        # Reuse existing logic logic, but maybe suppress hints?
        # For now, we reuse render_vocabulary_match_exercise logic but mostly manually to control flow
        
        current_idx = st.session_state[f"{key_prefix}_current_idx"]
        shuffled_indices = st.session_state[f"{key_prefix}_shuffled_indices"]
        
        # Safety check
        if current_idx >= len(exercises):
             st.session_state[f"{key_prefix}_state"] = "VICTORY"
             st.rerun()
             return

        real_idx = shuffled_indices[current_idx]
        ex = exercises[real_idx]
        
        # Show Progress for Exam
        progress = (current_idx / len(exercises))
        st.progress(progress, text=f"Pregunta {current_idx + 1} de {len(exercises)}")
        
        # Question Card
        st.markdown(
            f"""
            <div style="text-align: center; padding: 40px; background-color: #f8fafc; border-radius: 10px; border: 2px solid #e2e8f0; margin-bottom: 20px;">
                <div style="font-size: 1.2em; color: #64748b; margin-bottom: 10px;">Traduce al Latín:</div>
                <div style="font-size: 2.5em; font-weight: bold; color: #1e293b; font-family: 'Cinzel', serif;">{ex['spanish']}</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Options
        opts = ex['options']
        cols = st.columns(2)
        
        # Callback for answer
        def check_answer(selected_opt):
             is_correct = (selected_opt == ex['latin'])
             
             # Exam Logic: We record internally
             if is_correct:
                 st.session_state[f"{key_prefix}_score"] += 1
             
             # Save last result for feedback (even in exam, feedback is good learning)
             st.session_state[f"{key_prefix}_last_correct"] = is_correct
             st.session_state[f"{key_prefix}_last_answer"] = ex['latin']
             st.session_state[f"{key_prefix}_last_explanation"] = f"'{ex['latin']}' significa '{ex['spanish']}'"
             
             # Move to feedback state
             st.session_state[f"{key_prefix}_state"] = "FEEDBACK"
        
        for idx, opt in enumerate(opts):
             with cols[idx % 2]:
                 st.button(
                     opt, 
                     key=f"{key_prefix}_opt_{current_idx}_{idx}", 
                     use_container_width=True,
                     on_click=check_answer,
                     args=(opt,)
                 )

    elif state == "FEEDBACK":
        # In Exam Mode, maybe we just show brief feedback or NO feedback?
        # User requested "Exam Mode". Let's show brief feedback but continue automatically?
        # Or standard Juicy Feedback is fine.
        
        def next_question():
             # Advance index
             st.session_state[f"{key_prefix}_current_idx"] += 1
             if st.session_state[f"{key_prefix}_current_idx"] >= len(exercises):
                 st.session_state[f"{key_prefix}_state"] = "VICTORY"
             else:
                 st.session_state[f"{key_prefix}_state"] = "PLAYING"
        
        # Show feedback
        render_juicy_feedback(
            is_correct=st.session_state[f"{key_prefix}_last_correct"],
            explanation=st.session_state[f"{key_prefix}_last_explanation"],
            correct_answer=st.session_state[f"{key_prefix}_last_answer"],
            on_continue=next_question,
            key=f"{key_prefix}_feed_{st.session_state[f'{key_prefix}_current_idx']}"
        )

    elif state == "VICTORY":
        # Calculate Final Grade
        score = st.session_state[f"{key_prefix}_score"]
        total = len(exercises)
        percentage = score / total
        
        has_passed = percentage >= 0.8
        
        st.markdown(f"### 🏁 Resultado de la Prueba")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Puntaje", f"{score}/{total}")
        col2.metric("Porcentaje", f"{int(percentage*100)}%")
        col3.metric("Estado", "APROBADO" if has_passed else "REPROBADO")
        
        if has_passed:
            st.success("🎉 ¡Felicidades! Has superado la prueba final.")
            st.balloons()
            
            if st.button("🏆 Reclamar Recompensa y Finalizar", type="primary", key=f"{key_prefix}_claim"):
                 # Trigger Completion Callback
                 if on_complete:
                     on_complete()
                 # Clean state
                 del st.session_state[f"{key_prefix}_state"]
                 st.rerun()
        else:
            st.error("❌ No has alcanzado el 80% necesario.")
            st.markdown("Debes repasar la lección y volver a intentarlo.")
            if st.button("🔄 Intentar de Nuevo", key=f"{key_prefix}_retry"):
                 # Reset key to force re-init
                 del st.session_state[f"{key_prefix}_state"]
                 st.rerun()
