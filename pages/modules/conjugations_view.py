import streamlit as st
import sys
import os
import random
import unicodedata



from database.connection import get_session
from database import Word, UserProfile
from sqlmodel import select
from utils.i18n import get_text
from utils.latin_logic import LatinMorphology, get_conjugation_forms
from utils.gamification import process_xp_gain
from utils.ui_helpers import load_css
from utils.text_utils import normalize_latin
from utils.constants import TENSES_INDICATIVE, TENSE_LABELS_INDICATIVE, MOODS, MOOD_LABELS


def render_content():
    
    # Load CSS

    
    st.markdown(
        """
        <h1 style='text-align: center; font-family: "Cinzel", serif;'>
            ⚔️ Conjugatio - Conjugaciones
        </h1>
        """,
        unsafe_allow_html=True
    )
    
    morphology = LatinMorphology()
    
    # Get user level for progressive learning
    with get_session() as session:
        user = session.exec(select(UserProfile)).first()
        user_level = user.level if user else 1
    
    st.markdown(f"### 📚 Nivel {user_level} - Verbos")
    
    # Tense translation map
    TENSE_MAP = {
        "Praesens": "Presente",
        "Imperfectum": "Imperfecto",
        "Futurum": "Futuro",
        "Perfectum": "Perfecto",
        "Plusquamperfectum": "Pluscuamperfecto",
        "FuturumPerfectum": "Futuro Perfecto"
    }
    
    st.markdown("---")
    
    # Create tabs for practice modes
    practice_tabs = st.tabs(["📚 Práctica Guiada", "🎯 Práctica Libre"])
    
    # ===== TAB 1: GUIDED PRACTICE =====
    with practice_tabs[0]:
        st.markdown("### Práctica según tu nivel")
        
        # Progressive tense introduction based on level
        if user_level <= 2:
            available_tenses = ["Praesens"]
            st.info("🎯 Nivel básico: Solo presente de indicativo (activo)")
        elif user_level <= 3:
            available_tenses = ["Praesens", "Imperfectum", "Futurum"]
            st.info("🎯 Nivel intermedio: Presente, imperfecto y futuro")
        elif user_level <= 5:
            available_tenses = ["Praesens", "Imperfectum", "Futurum", "Perfectum"]
            st.info("🎯 Nivel intermedio-avanzado: + Perfecto")
        else:
            available_tenses = ["Praesens", "Imperfectum", "Futurum", "Perfectum", "Plusquamperfectum", "FuturumPerfectum"]
            st.info("🎯 Nivel avanzado: Todos los tiempos verbales")
        
        # Select tense and voice
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            # Use format_func to display Spanish names
            tense_selection = st.selectbox(
                "⏱️ Tiempo verbal", 
                available_tenses, 
                format_func=lambda x: TENSE_MAP.get(x, x),
                key="tense_select"
            )
        
        with col2:
            voice_selection = st.selectbox(
                "🎭 Voz",
                ["Activa", "Pasiva"],
                key="voice_select"
            )
        
        with col3:
            # Mode selector for advanced levels
            if user_level >= 4:
                mode_selection = st.selectbox(
                    "📖 Modo",
                    ["Indicativo", "Subjuntivo", "Imperativo"],
                    key="mode_select"
                )
            else:
                mode_selection = "Indicativo"  # Default for lower levels
    
        # Get verbs and store verb ID instead of object
        with get_session() as session:
            verbs = session.exec(select(Word).where(Word.part_of_speech == "verb")).all()
            
            if not verbs:
                st.warning("No hay verbos en la base de datos. Usa el panel de Admin para añadirlos.")
                st.stop()
            
            # Initialize with a random verb ID
            if 'current_verb_id' not in st.session_state:
                st.session_state.current_verb_id = random.choice(verbs).id
            
            # Reload the verb from the database using the stored ID
            verb = session.exec(select(Word).where(Word.id == st.session_state.current_verb_id)).first()
            
            if not verb:
                # If verb not found, reset to a new random verb
                st.session_state.current_verb_id = random.choice(verbs).id
                verb = session.exec(select(Word).where(Word.id == st.session_state.current_verb_id)).first()
            
            st.markdown(f"### Conjuga: **{verb.latin}** ({verb.translation})")
            
            if verb.principal_parts:
                st.info(f"📋 Partes principales: **{verb.principal_parts}** • Conjugación: {verb.conjugation}ª")
            else:
                st.warning("Este verbo no tiene partes principales definidas.")
            
            # Get full conjugation table
            if not verb.principal_parts or not verb.conjugation:
                st.error("Este verbo no tiene información completa para conjugarse.")
                st.stop()
            
            forms = morphology.conjugate_verb(verb.latin, verb.conjugation, verb.principal_parts, verb.irregular_forms)
            
            if not forms:
                st.error("No se pudo generar la conjugación para este verbo.")
                st.stop()
            
            # Map tense, voice, and mood to form keys
            tense_lower = tense_selection.lower()
            voice_es = voice_selection  # "Activa" or "Pasiva"
            mode_es = mode_selection  # "Indicativo", "Subjuntivo", or "Imperativo"
            
            # Imperative has special handling (only 2nd person, no tense selection)
            if mode_es == "Imperativo":
                prefix = "imv"
                if voice_es == "Pasiva":
                    prefix = "imv_pass"
                tense_display = f"Imperativo ({voice_es})"
                # Imperative only has 2nd person singular and plural
                persons = ["2ª persona"]
            else:
                if tense_lower == "praesens":
                    prefix = "pres"
                    tense_es = "Presente"
                elif tense_lower == "imperfectum":
                    prefix = "imp"
                    tense_es = "Imperfecto"
                elif tense_lower == "futurum":
                    prefix = "fut"
                    tense_es = "Futuro"
                elif tense_lower == "perfectum":
                    prefix = "perf"
                    tense_es = "Perfecto"
                elif tense_lower == "plusquamperfectum":
                    prefix = "plup"
                    tense_es = "Pluscuamperfecto"
                elif tense_lower == "futurumperfectum":
                    prefix = "futperf"
                    tense_es = "Futuro Perfecto"
                else:
                    prefix = "pres"
                    tense_es = "Presente"
                
                # Add "_subj" suffix for subjunctive mood
                if mode_es == "Subjuntivo":
                    # Filter invalid subjunctive tenses
                    if prefix == "fut" or prefix == "futperf":
                         st.warning("⚠️ El subjuntivo no tiene tiempo futuro.")
                         st.stop()
                    
                    prefix = prefix + "_subj"
                
                # Add "_pass" suffix for passive voice
                if voice_es == "Pasiva":
                    prefix = prefix + "_pass"
                
                tense_display = f"{tense_es} de {mode_es} ({voice_es})"
                persons = ["1ª persona", "2ª persona", "3ª persona"]
            
            st.markdown(f"**{tense_display}**")
            
            # Initialize show_answers state
            if 'show_conjugation_answers' not in st.session_state:
                st.session_state.show_conjugation_answers = False
            if 'user_conjugation_answers' not in st.session_state:
                st.session_state.user_conjugation_answers = {}
            
            # Create conjugation table
            col1, col2 = st.columns(2)
            
            if mode_es == "Imperativo":
                # Imperative only has 2nd person
                with col1:
                    st.markdown("#### Singularis")
                    key = f"{prefix}_2sg"
                    correct_form = forms.get(key, "—")
                    
                    if st.session_state.show_conjugation_answers:
                        user_answer = st.session_state.user_conjugation_answers.get(f"input_sg_2", "")
                        is_correct = normalize_latin(user_answer.strip()).lower() == normalize_latin(correct_form).lower()
                        
                        if is_correct:
                            st.success(f"✅ 2ª persona: **{correct_form}**")
                        else:
                            st.error(f"❌ 2ª persona: '{user_answer}' → **{correct_form}**")
                    else:
                        st.text_input("2ª persona", value="", key=f"input_sg_2", placeholder="2ª persona singular", label_visibility="collapsed")
                
                with col2:
                    st.markdown("#### Pluralis")
                    key = f"{prefix}_2pl"
                    correct_form = forms.get(key, "—")
                    
                    if st.session_state.show_conjugation_answers:
                        user_answer = st.session_state.user_conjugation_answers.get(f"input_pl_2", "")
                        is_correct = normalize_latin(user_answer.strip()).lower() == normalize_latin(correct_form).lower()
                        
                        if is_correct:
                            st.success(f"✅ 2ª persona: **{correct_form}**")
                        else:
                            st.error(f"❌ 2ª persona: '{user_answer}' → **{correct_form}**")
                    else:
                        st.text_input("2ª persona", value="", key=f"input_pl_2", placeholder="2ª persona plural", label_visibility="collapsed")
            else:
                # Regular conjugation (all 3 persons)
                with col1:
                    st.markdown("#### Singularis")
                    for i, person in enumerate(persons, 1):
                        key = f"{prefix}_{i}sg"
                        correct_form = forms.get(key, "—")
                        
                        if st.session_state.show_conjugation_answers:
                            # Show user's answer and correct answer
                            user_answer = st.session_state.user_conjugation_answers.get(f"input_sg_{i}", "")
                            is_correct = normalize_latin(user_answer.strip()).lower() == normalize_latin(correct_form).lower()
                            
                            if is_correct:
                                st.success(f"✅ {person}: **{correct_form}**")
                            else:
                                st.error(f"❌ {person}: '{user_answer}' → **{correct_form}**")
                        else:
                            # Empty input for practice
                            st.text_input(person, value="", key=f"input_sg_{i}", placeholder=f"{person} singular", label_visibility="collapsed")
                
                with col2:
                    st.markdown("#### Pluralis")
                    for i, person in enumerate(persons, 1):
                        key = f"{prefix}_{i}pl"
                        correct_form = forms.get(key, "—")
                        
                        if st.session_state.show_conjugation_answers:
                            # Show user's answer and correct answer
                            user_answer = st.session_state.user_conjugation_answers.get(f"input_pl_{i}", "")
                            is_correct = normalize_latin(user_answer.strip()).lower() == normalize_latin(correct_form).lower()
                            
                            if is_correct:
                                st.success(f"✅ {person}: **{correct_form}**")
                            else:
                                st.error(f"❌ {person}: '{user_answer}' → **{correct_form}**")
                        else:
                            # Empty input for practice
                            st.text_input(person, value="", key=f"input_pl_{i}", placeholder=f"{person} plural", label_visibility="collapsed")
            
            # Show XP feedback if available
            if 'xp_feedback_conjugation' in st.session_state and st.session_state.show_conjugation_answers:
                st.success(st.session_state.xp_feedback_conjugation)
            
            st.markdown("---")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if st.button("✅ Verificar", width='stretch', key="conj_verify_guided"):
                    # Save user answers
                    st.session_state.user_conjugation_answers = {}
                    for i in range(1, 4):
                        sg_key = f"input_sg_{i}"
                        pl_key = f"input_pl_{i}"
                        if sg_key in st.session_state:
                            st.session_state.user_conjugation_answers[sg_key] = st.session_state[sg_key]
                        if pl_key in st.session_state:
                            st.session_state.user_conjugation_answers[pl_key] = st.session_state[pl_key]
                    
                    # Calculate score and award XP
                    correct_count = 0
                    total_count = 0
                    
                    for i in range(1, 4):
                        # Singular
                        sg_key = f"input_sg_{i}"
                        user_answer_sg = st.session_state.user_conjugation_answers.get(sg_key, "")
                        correct_form_sg = forms.get(f"{prefix}_{i}sg", "")
                        if user_answer_sg.strip():
                            total_count += 1
                            if normalize_latin(user_answer_sg.strip()).lower() == normalize_latin(correct_form_sg).lower():
                                correct_count += 1
                        
                        # Plural
                        pl_key = f"input_pl_{i}"
                        user_answer_pl = st.session_state.user_conjugation_answers.get(pl_key, "")
                        correct_form_pl = forms.get(f"{prefix}_{i}pl", "")
                        if user_answer_pl.strip():
                            total_count += 1
                            if normalize_latin(user_answer_pl.strip()).lower() == normalize_latin(correct_form_pl).lower():
                                correct_count += 1
                    
                    # Award XP: 5 points per correct answer
                    xp_gained = correct_count * 5
                    
                    if xp_gained > 0:
                        with get_session() as session:
                            user = session.exec(select(UserProfile)).first()
                            if user:
                                new_level, leveled_up = process_xp_gain(session, user, xp_gained)
                                if leveled_up:
                                    st.balloons()
                                    st.success(f"🎉 ¡FELICIDADES! Has alcanzado el Nivel {new_level}!")
                                st.session_state.xp_feedback_conjugation = f"🎉 +{xp_gained} XP ({correct_count}/{total_count} correctas)"
                    
                    st.session_state.show_conjugation_answers = True
                    st.rerun()
            
            with col2:
                if st.button("🔄 Limpiar", width='stretch', key="conj_clear_guided"):
                    st.session_state.show_conjugation_answers = False
                    st.session_state.user_conjugation_answers = {}
                    st.rerun()
            
            with col3:
                if st.button("🎲 Nuevo Verbo", width='stretch', key="conj_new_verb_guided"):
                    # Select new verb ID instead of storing object
                    with get_session() as new_session:
                        all_verbs = new_session.exec(select(Word).where(Word.part_of_speech == "verb")).all()
                        st.session_state.current_verb_id = random.choice(all_verbs).id
                    st.session_state.show_conjugation_answers = False
                    st.session_state.user_conjugation_answers = {}
                    st.rerun()
    
    # ===== TAB 2: FREE PRACTICE =====
    with practice_tabs[1]:
        st.markdown("### Práctica Libre")
        st.info("🎯 Elige exactamente qué quieres practicar. **Esta práctica NO otorga XP.**")
        
        st.markdown("#### Filtros de selección")
        
        col1, col2 = st.columns(2)
        
        with col1:
            filter_conjugation = st.multiselect(
                "Conjugación",
                options=["1", "2", "3", "4"],
                default=["1"],
                format_func=lambda x: f"{x}ª conjugación",
                key="free_conjugation"
            )
            
            filter_mood = st.multiselect(
                "Modo",
                options=["Indicativo", "Subjuntivo", "Imperativo"],
                default=["Indicativo"],
                key="free_mood"
            )
            
        with col2:
            filter_voice = st.multiselect(
                "Voz",
                options=["Activa", "Pasiva"],
                default=["Activa"],
                key="free_voice"
            )
            
            filter_tense = st.multiselect(
                "Tiempo",
                options=["Praesens", "Imperfectum", "Futurum", "Perfectum", "Plusquamperfectum", "FuturumPerfectum"],
                default=["Praesens"],
                format_func=lambda x: TENSE_MAP.get(x, x),
                key="free_tense"
            )
        
        if not filter_conjugation or not filter_mood or not filter_voice or not filter_tense:
            st.warning("⚠️ Debes seleccionar al menos una opción en cada filtro.")
            st.stop()
            
        # Get filtered verbs
        with get_session() as session:
            filtered_verbs = session.exec(
                select(Word).where(
                    Word.part_of_speech == "verb",
                    Word.conjugation.in_(filter_conjugation)
                )
            ).all()
            
            if not filtered_verbs:
                st.warning("❌ No hay verbos disponibles con estos filtros.")
                st.stop()
                
            st.success(f"✅ {len(filtered_verbs)} verbos disponibles con estos filtros")
            
            # Get filtered verb IDs
            filtered_verb_ids = [v.id for v in filtered_verbs]
            
            # Select random verb ID
            if 'current_free_verb_id' not in st.session_state:
                st.session_state.current_free_verb_id = random.choice(filtered_verb_ids)
                
            # Check if current verb ID is still in filtered list (if conjugation changed)
            if st.session_state.current_free_verb_id not in filtered_verb_ids:
                 st.session_state.current_free_verb_id = random.choice(filtered_verb_ids)
                 
            # Reload verb from database
            verb = session.exec(select(Word).where(Word.id == st.session_state.current_free_verb_id)).first()
            
            # Select random parameters from filters for the current exercise
            if 'free_exercise_params' not in st.session_state:
                st.session_state.free_exercise_params = {
                    "mood": random.choice(filter_mood),
                    "voice": random.choice(filter_voice),
                    "tense": random.choice(filter_tense)
                }
            
            # Ensure selected params are still valid with current filters
            params = st.session_state.free_exercise_params
            if params["mood"] not in filter_mood:
                params["mood"] = random.choice(filter_mood)
            if params["voice"] not in filter_voice:
                params["voice"] = random.choice(filter_voice)
            if params["tense"] not in filter_tense:
                params["tense"] = random.choice(filter_tense)
                
            # Validate combinations (e.g. Subjunctive Future)
            # If invalid, try to pick another tense, or warn
            if params["mood"] == "Subjuntivo" and params["tense"] in ["Futurum", "FuturumPerfectum"]:
                 # Try to find a valid tense in the filter
                 valid_subj_tenses = [t for t in filter_tense if t not in ["Futurum", "FuturumPerfectum"]]
                 if valid_subj_tenses:
                     params["tense"] = random.choice(valid_subj_tenses)
                 else:
                     st.warning("⚠️ La combinación de Subjuntivo con los tiempos seleccionados (Futuro) no es válida. Por favor selecciona otros tiempos.")
                     st.stop()
            
            if params["mood"] == "Imperativo":
                 # Imperative doesn't really use tense in the same way, usually just Present
                 # But let's just ignore tense selection for Imperative or force Present
                 pass
    
            st.markdown("---")
            st.markdown(f"### Conjuga: **{verb.latin}** ({verb.translation})")
            st.info(f"📋 Conjugación: {verb.conjugation}ª • {params['mood']} • {params['voice']} • {TENSE_MAP.get(params['tense'], params['tense'])}")
            
            # Generate forms
            forms = morphology.conjugate_verb(verb.latin, verb.conjugation, verb.principal_parts, verb.irregular_forms)
            
            if not forms:
                st.error("No se pudo generar la conjugación.")
                st.stop()
                
            # Determine prefix based on params
            tense_lower = params["tense"].lower()
            voice_es = params["voice"]
            mode_es = params["mood"]
            
            if mode_es == "Imperativo":
                prefix = "imv"
                if voice_es == "Pasiva":
                    prefix = "imv_pass"
                persons = ["2ª persona"]
            else:
                if tense_lower == "praesens": prefix = "pres"
                elif tense_lower == "imperfectum": prefix = "imp"
                elif tense_lower == "futurum": prefix = "fut"
                elif tense_lower == "perfectum": prefix = "perf"
                elif tense_lower == "plusquamperfectum": prefix = "plup"
                elif tense_lower == "futurumperfectum": prefix = "futperf"
                else: prefix = "pres"
                
                if mode_es == "Subjuntivo":
                    prefix = prefix + "_subj"
                
                if voice_es == "Pasiva":
                    prefix = prefix + "_pass"
                    
                persons = ["1ª persona", "2ª persona", "3ª persona"]
                
            # Initialize show_answers state
            if 'show_free_conjugation_answers' not in st.session_state:
                st.session_state.show_free_conjugation_answers = False
            if 'user_free_conjugation_answers' not in st.session_state:
                st.session_state.user_free_conjugation_answers = {}
                
            # Display inputs
            col1, col2 = st.columns(2)
            
            if mode_es == "Imperativo":
                 with col1:
                    st.markdown("#### Singularis")
                    key = f"{prefix}_2sg"
                    correct_form = forms.get(key, "—")
                    if st.session_state.show_free_conjugation_answers:
                        user_answer = st.session_state.user_free_conjugation_answers.get("free_input_sg_2", "")
                        is_correct = normalize_latin(user_answer.strip()).lower() == normalize_latin(correct_form).lower()
                        if is_correct: st.success(f"✅ 2ª persona: **{correct_form}**")
                        else: st.error(f"❌ 2ª persona: '{user_answer}' → **{correct_form}**")
                    else:
                        st.text_input("2ª persona", value="", key="free_input_sg_2", placeholder="2ª persona singular", label_visibility="collapsed")
                 with col2:
                    st.markdown("#### Pluralis")
                    key = f"{prefix}_2pl"
                    correct_form = forms.get(key, "—")
                    if st.session_state.show_free_conjugation_answers:
                        user_answer = st.session_state.user_free_conjugation_answers.get("free_input_pl_2", "")
                        is_correct = normalize_latin(user_answer.strip()).lower() == normalize_latin(correct_form).lower()
                        if is_correct: st.success(f"✅ 2ª persona: **{correct_form}**")
                        else: st.error(f"❌ 2ª persona: '{user_answer}' → **{correct_form}**")
                    else:
                        st.text_input("2ª persona", value="", key="free_input_pl_2", placeholder="2ª persona plural", label_visibility="collapsed")
            else:
                with col1:
                    st.markdown("#### Singularis")
                    for i, person in enumerate(persons, 1):
                        key = f"{prefix}_{i}sg"
                        correct_form = forms.get(key, "—")
                        if st.session_state.show_free_conjugation_answers:
                            user_answer = st.session_state.user_free_conjugation_answers.get(f"free_input_sg_{i}", "")
                            is_correct = normalize_latin(user_answer.strip()).lower() == normalize_latin(correct_form).lower()
                            if is_correct: st.success(f"✅ {person}: **{correct_form}**")
                            else: st.error(f"❌ {person}: '{user_answer}' → **{correct_form}**")
                        else:
                            st.text_input(person, value="", key=f"free_input_sg_{i}", placeholder=f"{person} singular", label_visibility="collapsed")
                with col2:
                    st.markdown("#### Pluralis")
                    for i, person in enumerate(persons, 1):
                        key = f"{prefix}_{i}pl"
                        correct_form = forms.get(key, "—")
                        if st.session_state.show_free_conjugation_answers:
                            user_answer = st.session_state.user_free_conjugation_answers.get(f"free_input_pl_{i}", "")
                            is_correct = normalize_latin(user_answer.strip()).lower() == normalize_latin(correct_form).lower()
                            if is_correct: st.success(f"✅ {person}: **{correct_form}**")
                            else: st.error(f"❌ {person}: '{user_answer}' → **{correct_form}**")
                        else:
                            st.text_input(person, value="", key=f"free_input_pl_{i}", placeholder=f"{person} plural", label_visibility="collapsed")
    
            st.markdown("---")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if st.button("✅ Verificar", width='stretch', key="conj_verify_free"):
                    st.session_state.user_free_conjugation_answers = {}
                    # Save answers
                    if mode_es == "Imperativo":
                        if "free_input_sg_2" in st.session_state: st.session_state.user_free_conjugation_answers["free_input_sg_2"] = st.session_state["free_input_sg_2"]
                        if "free_input_pl_2" in st.session_state: st.session_state.user_free_conjugation_answers["free_input_pl_2"] = st.session_state["free_input_pl_2"]
                    else:
                        for i in range(1, 4):
                            if f"free_input_sg_{i}" in st.session_state: st.session_state.user_free_conjugation_answers[f"free_input_sg_{i}"] = st.session_state[f"free_input_sg_{i}"]
                            if f"free_input_pl_{i}" in st.session_state: st.session_state.user_free_conjugation_answers[f"free_input_pl_{i}"] = st.session_state[f"free_input_pl_{i}"]
                    
                    # Calculate score (No XP)
                    correct_count = 0
                    total_count = 0
                    
                    if mode_es == "Imperativo":
                        # Check imperative
                        key_sg = f"{prefix}_2sg"
                        ans_sg = st.session_state.user_free_conjugation_answers.get("free_input_sg_2", "")
                        if ans_sg.strip():
                            total_count += 1
                            if normalize_latin(ans_sg.strip()).lower() == normalize_latin(forms.get(key_sg, "")).lower(): correct_count += 1
                            
                        key_pl = f"{prefix}_2pl"
                        ans_pl = st.session_state.user_free_conjugation_answers.get("free_input_pl_2", "")
                        if ans_pl.strip():
                            total_count += 1
                            if normalize_latin(ans_pl.strip()).lower() == normalize_latin(forms.get(key_pl, "")).lower(): correct_count += 1
                    else:
                        # Check regular
                        for i in range(1, 4):
                            key_sg = f"{prefix}_{i}sg"
                            ans_sg = st.session_state.user_free_conjugation_answers.get(f"free_input_sg_{i}", "")
                            if ans_sg.strip():
                                total_count += 1
                                if normalize_latin(ans_sg.strip()).lower() == normalize_latin(forms.get(key_sg, "")).lower(): correct_count += 1
                                
                            key_pl = f"{prefix}_{i}pl"
                            ans_pl = st.session_state.user_free_conjugation_answers.get(f"free_input_pl_{i}", "")
                            if ans_pl.strip():
                                total_count += 1
                                if normalize_latin(ans_pl.strip()).lower() == normalize_latin(forms.get(key_pl, "")).lower(): correct_count += 1
                    
                    if total_count > 0:
                        percentage = (correct_count / total_count) * 100
                        st.info(f"📊 Resultado: {correct_count}/{total_count} correctas ({percentage:.1f}%) • Sin XP")
                    
                    st.session_state.show_free_conjugation_answers = True
                    st.rerun()
            
            with col2:
                if st.button("🔄 Limpiar", width='stretch', key="conj_clear_free"):
                    st.session_state.show_free_conjugation_answers = False
                    st.session_state.user_free_conjugation_answers = {}
                    st.rerun()
            
            with col3:
                if st.button("🎲 Nuevo Verbo", width='stretch', key="conj_new_verb_free"):
                    # Select new verb ID from filtered list
                    with get_session() as new_session:
                        new_filtered_verbs = new_session.exec(
                            select(Word).where(
                                Word.part_of_speech == "verb",
                                Word.conjugation.in_(filter_conjugation)
                            )
                        ).all()
                        st.session_state.current_free_verb_id = random.choice(new_filtered_verbs).id
                    # Also randomize params again
                    st.session_state.free_exercise_params = {
                        "mood": random.choice(filter_mood),
                        "voice": random.choice(filter_voice),
                        "tense": random.choice(filter_tense)
                    }
                    st.session_state.show_free_conjugation_answers = False
                    st.session_state.user_free_conjugation_answers = {}
                    st.rerun()
    
