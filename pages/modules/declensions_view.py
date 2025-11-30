import os
import random
import sys
from datetime import datetime

import streamlit as st
from sqlmodel import or_, select

from database import UserProfile, Word
from database.connection import get_session
from utils.constants import CASE_LABELS, CASES, NUMBER_LABELS, NUMBERS
from utils.gamification import process_xp_gain
from utils.i18n import get_text
from utils.latin_logic import (
    LatinMorphology,
    get_declension_forms,
    get_demonstrative_genders,
    get_pronoun_forms,
)
from utils.text_utils import normalize_latin
from utils.ui_helpers import load_css


def render_content():
    st.markdown(
        """
        <h1 style='text-align: center; font-family: "Cinzel", serif;'>
            📜 Declinatio - Declinaciones
        </h1>
        """,
        unsafe_allow_html=True,
    )

    morphology = LatinMorphology()

    # Get user level for progressive learning
    with get_session() as session:
        user = session.exec(select(UserProfile)).first()
        user_level = user.level if user else 1

    st.markdown(f"### 📚 Nivel {user_level} - Sustantivos")

    # Check for Practice Context
    practice_context = st.session_state.get("practice_context")
    if practice_context and practice_context.get("active"):
        st.info(f"🎯 **Modo Práctica: {practice_context.get('description')}**")
        if st.button("❌ Salir del Modo Práctica", key="exit_context_decl"):
            st.session_state.practice_context = None
            st.rerun()
    
    st.markdown("---")

    # Create tabs for practice modes
    practice_tabs = st.tabs(["📚 Práctica Guiada", "🎯 Práctica Libre"])

    # ===== TAB 1: GUIDED PRACTICE =====
    with practice_tabs[0]:
        st.markdown("### Práctica según tu nivel")

        # Level-based word selection
        if user_level == 1:
            available_declensions = ["1", "2"]
            available_pos = ["noun"]
            st.info("🎯 Nivel 1: Solo sustantivos (1ª y 2ª declinación)")
        elif user_level == 2:
            available_declensions = ["1", "2"]
            available_pos = ["noun", "adjective"]
            st.info("🎯 Nivel 2: Sustantivos y Adjetivos (1ª y 2ª declinación)")
        elif user_level == 3:
            available_declensions = ["1", "2", "3"]
            available_pos = ["noun", "adjective"]
            st.info("🎯 Nivel 3: Se añade la 3ª declinación")
        elif user_level == 4:
            available_declensions = ["1", "2", "3"]
            available_pos = ["noun", "adjective", "pronoun"]
            st.info("🎯 Nivel 4: Se añaden los Pronombres")
        else:
            available_declensions = ["1", "2", "3", "4", "5"]
            available_pos = ["noun", "adjective", "pronoun"]
            st.info("🎯 Nivel 5+: Todas las declinaciones y tipos")

        # Get words from available declensions and POS
        with get_session() as session:
            # Apply Context Filters if active
            if practice_context and practice_context.get("active"):
                filters = practice_context.get("filters", {})
                query = select(Word)
                
                if "pos" in filters:
                    query = query.where(Word.part_of_speech.in_(filters["pos"]))
                if "declension" in filters:
                    query = query.where(Word.declension.in_(filters["declension"]))
                if "gender" in filters:
                    query = query.where(Word.gender.in_(filters["gender"]))
                # Add more filters as needed
                
                nouns = session.exec(query).all()
                
                if not nouns:
                    st.warning(f"No hay palabras disponibles para el contexto: {practice_context.get('description')}")
                    # Fallback to normal selection
                    nouns = session.exec(
                        select(Word).where(
                            Word.part_of_speech.in_(available_pos),
                            Word.declension.in_(available_declensions),
                        )
                    ).all()
            else:
                # Normal Level-based selection
                nouns = session.exec(
                    select(Word).where(
                        Word.part_of_speech.in_(available_pos),
                        Word.declension.in_(available_declensions),
                    )
                ).all()

            if not nouns:
                st.warning(
                    "No hay sustantivos disponibles para tu nivel. Usa el panel de Admin para añadirlos."
                )
                st.stop()

            if "current_noun_id" not in st.session_state:
                st.session_state.current_noun_id = random.choice(nouns).id

            # Always fetch the current noun from database to ensure it's attached to session
            noun = session.get(Word, st.session_state.current_noun_id)

            st.markdown(f"### Declina: **{noun.latin}** ({noun.translation})")
            st.info(
                f"📋 Declinación: {noun.declension}ª • Género: {noun.gender} • Genitivo: {noun.genitive}"
            )

            # Create declension table
            cases = [
                "nominativus",
                "vocativus",
                "accusativus",
                "genitivus",
                "dativus",
                "ablativus",
            ]
            case_labels = [
                "Nominativus",
                "Vocativus",
                "Accusativus",
                "Genitivus",
                "Dativus",
                "Ablativus",
            ]

            # Check if it's a pronoun
            if noun.part_of_speech == "pronoun":
                forms = morphology.decline_pronoun(noun.latin)
                if not forms:
                    st.warning("Pronombre no reconocido.")
                    st.stop()
                st.info(f"📋 Pronombre personal")
            else:
                # Regular noun declension
                if not noun.declension or not noun.gender:
                    st.warning(
                        "Este sustantivo no tiene declinación o género definido."
                    )
                    st.stop()

                genitive = noun.genitive if noun.genitive else noun.latin
                forms = morphology.decline_noun(
                    noun.latin,
                    noun.declension,
                    noun.gender,
                    genitive,
                    noun.irregular_forms,
                    noun.parisyllabic,
                    noun.is_plurale_tantum,
                    noun.is_singulare_tantum,
                )

                if not forms:
                    st.warning(
                        "No se pudo generar la declinación para este sustantivo."
                    )
                    st.stop()

            # Check if this is a demonstrative pronoun (has gender forms)
            is_demonstrative = any(
                key.endswith("_m") or key.endswith("_f") or key.endswith("_n")
                for key in forms.keys()
            )

            # Initialize show_answers state
            if "show_declension_answers" not in st.session_state:
                st.session_state.show_declension_answers = False
            if "user_declension_answers" not in st.session_state:
                st.session_state.user_declension_answers = {}

            if is_demonstrative:
                # Display with 3 genders (separate inputs)
                st.markdown("### Paradigma Completo")

                for case, label in zip(cases, case_labels):
                    st.markdown(f"#### {label}")
                    col_sg, col_pl = st.columns(2)

                    with col_sg:
                        st.caption("Singularis (Masc / Fem / Neut)")
                        c1, c2, c3 = st.columns(3)

                        # Keys
                        key_m = f"{case[:3]}_sg_m"
                        key_f = f"{case[:3]}_sg_f"
                        key_n = f"{case[:3]}_sg_n"

                        # Correct forms
                        form_m = forms.get(key_m, "—")
                        form_f = forms.get(key_f, "—")
                        form_n = forms.get(key_n, "—")

                        # Inputs
                        if st.session_state.show_declension_answers:
                            # MASCULINE
                            ans_m = st.session_state.user_declension_answers.get(
                                f"input_sg_{case}_m", ""
                            )
                            corr_m = (
                                normalize_latin(ans_m.strip()).lower()
                                == normalize_latin(form_m).lower()
                            )
                            with c1:
                                if form_m == "—":
                                    st.info("—")
                                elif corr_m:
                                    st.success(form_m)
                                else:
                                    st.error(f"{ans_m} → {form_m}")

                            # FEMININE
                            ans_f = st.session_state.user_declension_answers.get(
                                f"input_sg_{case}_f", ""
                            )
                            corr_f = (
                                normalize_latin(ans_f.strip()).lower()
                                == normalize_latin(form_f).lower()
                            )
                            with c2:
                                if form_f == "—":
                                    st.info("—")
                                elif corr_f:
                                    st.success(form_f)
                                else:
                                    st.error(f"{ans_f} → {form_f}")

                            # NEUTER
                            ans_n = st.session_state.user_declension_answers.get(
                                f"input_sg_{case}_n", ""
                            )
                            corr_n = (
                                normalize_latin(ans_n.strip()).lower()
                                == normalize_latin(form_n).lower()
                            )
                            with c3:
                                if form_n == "—":
                                    st.info("—")
                                elif corr_n:
                                    st.success(form_n)
                                else:
                                    st.error(f"{ans_n} → {form_n}")
                        else:
                            with c1:
                                if form_m == "—":
                                    st.text_input(
                                        "M",
                                        value="—",
                                        key=f"input_sg_{case}_m",
                                        disabled=True,
                                        label_visibility="collapsed",
                                    )
                                else:
                                    st.text_input(
                                        "M",
                                        key=f"input_sg_{case}_m",
                                        placeholder="Masc",
                                        label_visibility="collapsed",
                                    )
                            with c2:
                                if form_f == "—":
                                    st.text_input(
                                        "F",
                                        value="—",
                                        key=f"input_sg_{case}_f",
                                        disabled=True,
                                        label_visibility="collapsed",
                                    )
                                else:
                                    st.text_input(
                                        "F",
                                        key=f"input_sg_{case}_f",
                                        placeholder="Fem",
                                        label_visibility="collapsed",
                                    )
                            with c3:
                                if form_n == "—":
                                    st.text_input(
                                        "N",
                                        value="—",
                                        key=f"input_sg_{case}_n",
                                        disabled=True,
                                        label_visibility="collapsed",
                                    )
                                else:
                                    st.text_input(
                                        "N",
                                        key=f"input_sg_{case}_n",
                                        placeholder="Neut",
                                        label_visibility="collapsed",
                                    )

                    with col_pl:
                        st.caption("Pluralis (Masc / Fem / Neut)")
                        c1, c2, c3 = st.columns(3)

                        # Keys
                        key_m = f"{case[:3]}_pl_m"
                        key_f = f"{case[:3]}_pl_f"
                        key_n = f"{case[:3]}_pl_n"

                        # Correct forms
                        form_m = forms.get(key_m, "—")
                        form_f = forms.get(key_f, "—")
                        form_n = forms.get(key_n, "—")

                        # Inputs
                        if st.session_state.show_declension_answers:
                            # MASCULINE
                            ans_m = st.session_state.user_declension_answers.get(
                                f"input_pl_{case}_m", ""
                            )
                            corr_m = (
                                normalize_latin(ans_m.strip()).lower()
                                == normalize_latin(form_m).lower()
                            )
                            with c1:
                                if form_m == "—":
                                    st.info("—")
                                elif corr_m:
                                    st.success(form_m)
                                else:
                                    st.error(f"{ans_m} → {form_m}")

                            # FEMININE
                            ans_f = st.session_state.user_declension_answers.get(
                                f"input_pl_{case}_f", ""
                            )
                            corr_f = (
                                normalize_latin(ans_f.strip()).lower()
                                == normalize_latin(form_f).lower()
                            )
                            with c2:
                                if form_f == "—":
                                    st.info("—")
                                elif corr_f:
                                    st.success(form_f)
                                else:
                                    st.error(f"{ans_f} → {form_f}")

                            # NEUTER
                            ans_n = st.session_state.user_declension_answers.get(
                                f"input_pl_{case}_n", ""
                            )
                            corr_n = (
                                normalize_latin(ans_n.strip()).lower()
                                == normalize_latin(form_n).lower()
                            )
                            with c3:
                                if form_n == "—":
                                    st.info("—")
                                elif corr_n:
                                    st.success(form_n)
                                else:
                                    st.error(f"{ans_n} → {form_n}")
                        else:
                            with c1:
                                if form_m == "—":
                                    st.text_input(
                                        "M",
                                        value="—",
                                        key=f"input_pl_{case}_m",
                                        disabled=True,
                                        label_visibility="collapsed",
                                    )
                                else:
                                    st.text_input(
                                        "M",
                                        key=f"input_pl_{case}_m",
                                        placeholder="Masc",
                                        label_visibility="collapsed",
                                    )
                            with c2:
                                if form_f == "—":
                                    st.text_input(
                                        "F",
                                        value="—",
                                        key=f"input_pl_{case}_f",
                                        disabled=True,
                                        label_visibility="collapsed",
                                    )
                                else:
                                    st.text_input(
                                        "F",
                                        key=f"input_pl_{case}_f",
                                        placeholder="Fem",
                                        label_visibility="collapsed",
                                    )
                            with c3:
                                if form_n == "—":
                                    st.text_input(
                                        "N",
                                        value="—",
                                        key=f"input_pl_{case}_n",
                                        disabled=True,
                                        label_visibility="collapsed",
                                    )
                                else:
                                    st.text_input(
                                        "N",
                                        key=f"input_pl_{case}_n",
                                        placeholder="Neut",
                                        label_visibility="collapsed",
                                    )

                    st.markdown("---")
            else:
                # Regular display (nouns and personal pronouns)
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("#### Singularis")
                    for case, label in zip(cases, case_labels):
                        key = f"{case[:3]}_sg"
                        correct_form = forms.get(key, "—")

                        if st.session_state.show_declension_answers:
                            # Show user's answer and correct answer
                            user_answer = st.session_state.user_declension_answers.get(
                                f"input_sg_{case}", ""
                            )
                            # Normalize both for comparison (remove macrons)
                            is_correct = (
                                normalize_latin(user_answer.strip()).lower()
                                == normalize_latin(correct_form).lower()
                            )

                            # Display with color coding
                            if correct_form == "—":
                                st.info("—")
                            elif is_correct:
                                st.success(f"✅ {label}: **{correct_form}**")
                            else:
                                st.error(
                                    f"❌ {label}: Tu respuesta: '{user_answer}' → Correcto: **{correct_form}**"
                                )
                        else:
                            # Empty input for practice
                            if correct_form == "—":
                                st.text_input(
                                    label,
                                    value="—",
                                    key=f"input_sg_{case}",
                                    disabled=True,
                                    label_visibility="collapsed",
                                )
                            else:
                                st.text_input(
                                    label,
                                    value="",
                                    key=f"input_sg_{case}",
                                    placeholder=f"{label} singular",
                                    label_visibility="collapsed",
                                )

                with col2:
                    st.markdown("#### Pluralis")
                    for case, label in zip(cases, case_labels):
                        key = f"{case[:3]}_pl"
                        correct_form = forms.get(key, "—")

                        if st.session_state.show_declension_answers:
                            # Show user's answer and correct answer
                            user_answer = st.session_state.user_declension_answers.get(
                                f"input_pl_{case}", ""
                            )
                            # Normalize both for comparison (remove macrons)
                            is_correct = (
                                normalize_latin(user_answer.strip()).lower()
                                == normalize_latin(correct_form).lower()
                            )

                            # Display with color coding
                            if correct_form == "—":
                                st.info("—")
                            elif is_correct:
                                st.success(f"✅ {label}: **{correct_form}**")
                            else:
                                st.error(
                                    f"❌ {label}: Tu respuesta: '{user_answer}' → Correcto: **{correct_form}**"
                                )
                        else:
                            # Empty input for practice
                            if correct_form == "—":
                                st.text_input(
                                    label,
                                    value="—",
                                    key=f"input_pl_{case}",
                                    disabled=True,
                                    label_visibility="collapsed",
                                )
                            else:
                                st.text_input(
                                    label,
                                    value="",
                                    key=f"input_pl_{case}",
                                    placeholder=f"{label} plural",
                                    label_visibility="collapsed",
                                )

            # Show XP feedback if available
            if (
                "xp_feedback" in st.session_state
                and st.session_state.show_declension_answers
            ):
                st.success(st.session_state.xp_feedback)

            st.markdown("---")

            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                if st.button("✅ Verificar", width="stretch", key="decl_verify_guided"):
                    # Save user answers
                    st.session_state.user_declension_answers = {}

                    if is_demonstrative:
                        # Save all 3 genders x 2 numbers x 6 cases = 36 inputs
                        for case in cases:
                            for num in ["sg", "pl"]:
                                for g in ["m", "f", "n"]:
                                    key = f"input_{num}_{case}_{g}"
                                    if key in st.session_state:
                                        st.session_state.user_declension_answers[
                                            key
                                        ] = st.session_state[key]
                    else:
                        # Save regular inputs
                        for case in cases:
                            sg_key = f"input_sg_{case}"
                            pl_key = f"input_pl_{case}"
                            if sg_key in st.session_state:
                                st.session_state.user_declension_answers[sg_key] = (
                                    st.session_state[sg_key]
                                )
                            if pl_key in st.session_state:
                                st.session_state.user_declension_answers[pl_key] = (
                                    st.session_state[pl_key]
                                )

                    # Calculate score and award XP
                    correct_count = 0
                    total_count = 0

                    for case in cases:
                        if is_demonstrative:
                            # Check 3 genders
                            for num in ["sg", "pl"]:
                                for g in ["m", "f", "n"]:
                                    key = f"input_{num}_{case}_{g}"
                                    user_ans = (
                                        st.session_state.user_declension_answers.get(
                                            key, ""
                                        )
                                    )
                                    corr_form = forms.get(f"{case[:3]}_{num}_{g}", "")

                                    if user_ans.strip():
                                        total_count += 1
                                        if (
                                            normalize_latin(user_ans.strip()).lower()
                                            == normalize_latin(corr_form).lower()
                                        ):
                                            correct_count += 1
                        else:
                            # Regular check
                            # Singular
                            sg_key = f"input_sg_{case}"
                            user_answer_sg = (
                                st.session_state.user_declension_answers.get(sg_key, "")
                            )
                            correct_form_sg = forms.get(f"{case[:3]}_sg", "")
                            if (
                                user_answer_sg.strip()
                            ):  # Solo contar si el usuario respondió
                                total_count += 1
                                if (
                                    normalize_latin(user_answer_sg.strip()).lower()
                                    == normalize_latin(correct_form_sg).lower()
                                ):
                                    correct_count += 1

                            # Plural
                            pl_key = f"input_pl_{case}"
                            user_answer_pl = (
                                st.session_state.user_declension_answers.get(pl_key, "")
                            )
                            correct_form_pl = forms.get(f"{case[:3]}_pl", "")
                            if (
                                user_answer_pl.strip()
                            ):  # Solo contar si el usuario respondió
                                total_count += 1
                                if (
                                    normalize_latin(user_answer_pl.strip()).lower()
                                    == normalize_latin(correct_form_pl).lower()
                                ):
                                    correct_count += 1

                    # Award XP: 5 points per correct answer
                    xp_gained = correct_count * 5

                    if xp_gained > 0:
                        with get_session() as session:
                            user = session.exec(select(UserProfile)).first()
                            if user:
                                new_level, leveled_up = process_xp_gain(
                                    session, user, xp_gained
                                )
                                if leveled_up:
                                    st.balloons()
                                    st.success(
                                        f"🎉 ¡FELICIDADES! Has alcanzado el Nivel {new_level}!"
                                    )
                                st.session_state.xp_feedback = f"🎉 +{xp_gained} XP ({correct_count}/{total_count} correctas)"

                    st.session_state.show_declension_answers = True
                    st.rerun()

            with col2:
                if st.button("🔄 Limpiar", width="stretch", key="decl_clear_guided"):
                    st.session_state.show_declension_answers = False
                    st.session_state.user_declension_answers = {}
                    st.rerun()

            with col3:
                if st.button(
                    "🎲 Nueva Palabra", width="stretch", key="decl_new_word_guided"
                ):
                    st.session_state.current_noun_id = random.choice(nouns).id
                    st.session_state.show_declension_answers = False
                    st.session_state.user_declension_answers = {}
                    st.rerun()

    # ===== TAB 2: FREE PRACTICE =====
    with practice_tabs[1]:
        st.markdown("### Práctica Libre")
        st.info(
            "🎯 Elige exactamente qué quieres practicar. **Esta práctica NO otorga XP.**"
        )

        # Filters
        st.markdown("#### Filtros de selección")

        col1, col2, col3 = st.columns(3)

        with col1:
            filter_pos = st.selectbox(
                "Tipo de palabra",
                options=["noun", "adjective", "pronoun"],
                format_func=lambda x: {
                    "noun": "Sustantivo",
                    "adjective": "Adjetivo",
                    "pronoun": "Pronombre",
                }[x],
                key="free_pos",
            )

        # Dynamic filters based on POS
        with col2:
            if filter_pos == "noun":
                filter_declension = st.multiselect(
                    "Declinaciones",
                    options=["1", "2", "3", "4", "5"],
                    default=["1"],
                    format_func=lambda x: f"{x}ª declinación",
                    key="free_decl_noun",
                )
            elif filter_pos == "adjective":
                filter_adj_class = st.multiselect(
                    "Clase de adjetivo",
                    options=["1-2", "3"],
                    default=["1-2"],
                    format_func=lambda x: {
                        "1-2": "1ª clase (1-2 decl.)",
                        "3": "2ª clase (3ª decl.)",
                    }[x],
                    key="free_adj_class",
                )
            else:  # pronoun
                filter_pronoun_type = st.multiselect(
                    "Tipo de pronombre",
                    options=["personal", "demonstrative", "relative", "interrogative"],
                    default=["personal"],
                    format_func=lambda x: {
                        "personal": "Personal",
                        "demonstrative": "Demostrativo",
                        "relative": "Relativo",
                        "interrogative": "Interrogativo",
                    }[x],
                    key="free_pron_type",
                )

        with col3:
            if filter_pos == "noun":
                # Determine valid genders based on selected declensions
                valid_genders = set()
                if filter_declension:
                    for decl in filter_declension:
                        if decl == "1":
                            valid_genders.update(
                                ["m", "f"]
                            )  # 1ª: mayormente femenino, algunos masculinos
                        elif decl == "2":
                            valid_genders.update(
                                ["m", "f", "n"]
                            )  # 2ª: masculino y neutro (algunos femeninos)
                        elif decl == "3":
                            valid_genders.update(
                                ["m", "f", "n"]
                            )  # 3ª: todos los géneros
                        elif decl == "4":
                            valid_genders.update(
                                ["m", "f", "n"]
                            )  # 4ª: mayormente masculino, algunos femeninos y neutros
                        elif decl == "5":
                            valid_genders.update(
                                ["m", "f"]
                            )  # 5ª: mayormente femenino, algunos masculinos
                else:
                    valid_genders = {
                        "m",
                        "f",
                        "n",
                    }  # Si no hay declinación seleccionada, mostrar todos

                available_genders = sorted(
                    list(valid_genders), key=lambda x: ["m", "f", "n"].index(x)
                )

                # Ajustar default para incluir solo géneros válidos
                default_genders = [g for g in ["m", "f", "n"] if g in available_genders]

                filter_gender = st.multiselect(
                    "Género",
                    options=available_genders,
                    default=default_genders,
                    format_func=lambda x: {
                        "m": "Masculino",
                        "f": "Femenino",
                        "n": "Neutro",
                    }[x],
                    key="free_gender_noun",
                )
            elif filter_pos == "adjective":
                filter_degree = st.multiselect(
                    "Grado",
                    options=["positive", "comparative", "superlative"],
                    default=["positive"],
                    format_func=lambda x: {
                        "positive": "Positivo",
                        "comparative": "Comparativo",
                        "superlative": "Superlativo",
                    }[x],
                    key="free_degree",
                )
            else:
                st.write("")  # Empty space for pronouns

        # Build query based on filters
        with get_session() as session:
            query = select(Word).where(Word.part_of_speech == filter_pos)

            if filter_pos == "noun":
                if not filter_declension or not filter_gender:
                    st.warning(
                        "⚠️ Debes seleccionar al menos una declinación y un género."
                    )
                    st.stop()
                query = query.where(
                    Word.declension.in_(filter_declension),
                    Word.gender.in_(filter_gender),
                )

            elif filter_pos == "adjective":
                if not filter_adj_class or not filter_degree:
                    st.warning("⚠️ Debes seleccionar al menos una clase y un grado.")
                    st.stop()

                # Map class to declensions
                declensions = []
                if "1-2" in filter_adj_class:
                    declensions.extend(["1", "2"])
                if "3" in filter_adj_class:
                    declensions.append("3")

                if declensions:
                    query = query.where(Word.declension.in_(declensions))

                # Filter by degree if available (might need additional field in DB)
                # For now, we'll just filter by declension

            elif filter_pos == "pronoun":
                if not filter_pronoun_type:
                    st.warning("⚠️ Debes seleccionar al menos un tipo de pronombre.")
                    st.stop()

                # Map pronoun types to actual words (esto podría requerir un campo adicional en la DB)
                # Por ahora filtramos solo por part_of_speech == pronoun
                pass

            filtered_words = session.exec(query).all()

            if not filtered_words:
                st.warning(
                    "❌ No hay palabras disponibles con estos filtros. Usa el panel de Admin para añadir más palabras."
                )
                st.stop()

            st.success(
                f"✅ {len(filtered_words)} palabra(s) disponible(s) con estos filtros"
            )

            # Word selection
            if "current_free_noun_id" not in st.session_state:
                st.session_state.current_free_noun_id = random.choice(filtered_words).id

            # Always fetch the current noun from database to ensure it's attached to session
            noun = session.get(Word, st.session_state.current_free_noun_id)

            st.markdown("---")
            st.markdown(f"### Declina: **{noun.latin}** ({noun.translation})")
            st.info(
                f"📋 Declinación: {noun.declension}ª • Género: {noun.gender} • Genitivo: {noun.genitive}"
            )

            # Create declension table
            cases = [
                "nominativus",
                "vocativus",
                "accusativus",
                "genitivus",
                "dativus",
                "ablativus",
            ]
            case_labels = [
                "Nominativus",
                "Vocativus",
                "Accusativus",
                "Genitivus",
                "Dativus",
                "Ablativus",
            ]

            # Check if it's a pronoun
            if noun.part_of_speech == "pronoun":
                forms = morphology.decline_pronoun(noun.latin)
                if not forms:
                    st.warning("Pronombre no reconocido.")
                    st.stop()
            else:
                # Regular noun/adjective declension
                if not noun.declension or not noun.gender:
                    st.warning("Esta palabra no tiene declinación o género definido.")
                    st.stop()

                genitive = noun.genitive if noun.genitive else noun.latin
                forms = morphology.decline_noun(
                    noun.latin,
                    noun.declension,
                    noun.gender,
                    genitive,
                    noun.irregular_forms,
                    noun.parisyllabic,
                    noun.is_plurale_tantum,
                    noun.is_singulare_tantum,
                )

                if not forms:
                    st.warning("No se pudo generar la declinación para esta palabra.")
                    st.stop()

            # Initialize show_answers state for free practice
            if "show_free_answers" not in st.session_state:
                st.session_state.show_free_answers = False
            if "user_free_answers" not in st.session_state:
                st.session_state.user_free_answers = {}

            # Check if demonstrative (has gender forms)
            is_demonstrative = any(
                key.endswith("_m") or key.endswith("_f") or key.endswith("_n")
                for key in forms.keys()
            )

            if is_demonstrative:
                # Display with 3 genders (separate inputs)
                st.markdown("### Paradigma Completo")

                for case, label in zip(cases, case_labels):
                    st.markdown(f"#### {label}")
                    col_sg, col_pl = st.columns(2)

                    with col_sg:
                        st.caption("Singularis (Masc / Fem / Neut)")
                        c1, c2, c3 = st.columns(3)

                        # Keys
                        key_m = f"{case[:3]}_sg_m"
                        key_f = f"{case[:3]}_sg_f"
                        key_n = f"{case[:3]}_sg_n"

                        # Correct forms
                        form_m = forms.get(key_m, "—")
                        form_f = forms.get(key_f, "—")
                        form_n = forms.get(key_n, "—")

                        # Inputs
                        if st.session_state.show_free_answers:
                            # MASCULINE
                            ans_m = st.session_state.user_free_answers.get(
                                f"free_input_sg_{case}_m", ""
                            )
                            corr_m = (
                                normalize_latin(ans_m.strip()).lower()
                                == normalize_latin(form_m).lower()
                            )
                            with c1:
                                if form_m == "—":
                                    st.info("—")
                                elif corr_m:
                                    st.success(form_m)
                                else:
                                    st.error(f"{ans_m} → {form_m}")

                            # FEMININE
                            ans_f = st.session_state.user_free_answers.get(
                                f"free_input_sg_{case}_f", ""
                            )
                            corr_f = (
                                normalize_latin(ans_f.strip()).lower()
                                == normalize_latin(form_f).lower()
                            )
                            with c2:
                                if form_f == "—":
                                    st.info("—")
                                elif corr_f:
                                    st.success(form_f)
                                else:
                                    st.error(f"{ans_f} → {form_f}")

                            # NEUTER
                            ans_n = st.session_state.user_free_answers.get(
                                f"free_input_sg_{case}_n", ""
                            )
                            corr_n = (
                                normalize_latin(ans_n.strip()).lower()
                                == normalize_latin(form_n).lower()
                            )
                            with c3:
                                if form_n == "—":
                                    st.info("—")
                                elif corr_n:
                                    st.success(form_n)
                                else:
                                    st.error(f"{ans_n} → {form_n}")
                        else:
                            with c1:
                                if form_m == "—":
                                    st.text_input(
                                        "M",
                                        value="—",
                                        key=f"free_input_sg_{case}_m",
                                        disabled=True,
                                        label_visibility="collapsed",
                                    )
                                else:
                                    st.text_input(
                                        "M",
                                        key=f"free_input_sg_{case}_m",
                                        placeholder="Masc",
                                        label_visibility="collapsed",
                                    )
                            with c2:
                                if form_f == "—":
                                    st.text_input(
                                        "F",
                                        value="—",
                                        key=f"free_input_sg_{case}_f",
                                        disabled=True,
                                        label_visibility="collapsed",
                                    )
                                else:
                                    st.text_input(
                                        "F",
                                        key=f"free_input_sg_{case}_f",
                                        placeholder="Fem",
                                        label_visibility="collapsed",
                                    )
                            with c3:
                                if form_n == "—":
                                    st.text_input(
                                        "N",
                                        value="—",
                                        key=f"free_input_sg_{case}_n",
                                        disabled=True,
                                        label_visibility="collapsed",
                                    )
                                else:
                                    st.text_input(
                                        "N",
                                        key=f"free_input_sg_{case}_n",
                                        placeholder="Neut",
                                        label_visibility="collapsed",
                                    )

                    with col_pl:
                        st.caption("Pluralis (Masc / Fem / Neut)")
                        c1, c2, c3 = st.columns(3)

                        # Keys
                        key_m = f"{case[:3]}_pl_m"
                        key_f = f"{case[:3]}_pl_f"
                        key_n = f"{case[:3]}_pl_n"

                        # Correct forms
                        form_m = forms.get(key_m, "—")
                        form_f = forms.get(key_f, "—")
                        form_n = forms.get(key_n, "—")

                        # Inputs
                        if st.session_state.show_free_answers:
                            # MASCULINE
                            ans_m = st.session_state.user_free_answers.get(
                                f"free_input_pl_{case}_m", ""
                            )
                            corr_m = (
                                normalize_latin(ans_m.strip()).lower()
                                == normalize_latin(form_m).lower()
                            )
                            with c1:
                                if form_m == "—":
                                    st.info("—")
                                elif corr_m:
                                    st.success(form_m)
                                else:
                                    st.error(f"{ans_m} → {form_m}")

                            # FEMININE
                            ans_f = st.session_state.user_free_answers.get(
                                f"free_input_pl_{case}_f", ""
                            )
                            corr_f = (
                                normalize_latin(ans_f.strip()).lower()
                                == normalize_latin(form_f).lower()
                            )
                            with c2:
                                if form_f == "—":
                                    st.info("—")
                                elif corr_f:
                                    st.success(form_f)
                                else:
                                    st.error(f"{ans_f} → {form_f}")

                            # NEUTER
                            ans_n = st.session_state.user_free_answers.get(
                                f"free_input_pl_{case}_n", ""
                            )
                            corr_n = (
                                normalize_latin(ans_n.strip()).lower()
                                == normalize_latin(form_n).lower()
                            )
                            with c3:
                                if form_n == "—":
                                    st.info("—")
                                elif corr_n:
                                    st.success(form_n)
                                else:
                                    st.error(f"{ans_n} → {form_n}")
                        else:
                            with c1:
                                if form_m == "—":
                                    st.text_input(
                                        "M",
                                        value="—",
                                        key=f"free_input_pl_{case}_m",
                                        disabled=True,
                                        label_visibility="collapsed",
                                    )
                                else:
                                    st.text_input(
                                        "M",
                                        key=f"free_input_pl_{case}_m",
                                        placeholder="Masc",
                                        label_visibility="collapsed",
                                    )
                            with c2:
                                if form_f == "—":
                                    st.text_input(
                                        "F",
                                        value="—",
                                        key=f"free_input_pl_{case}_f",
                                        disabled=True,
                                        label_visibility="collapsed",
                                    )
                                else:
                                    st.text_input(
                                        "F",
                                        key=f"free_input_pl_{case}_f",
                                        placeholder="Fem",
                                        label_visibility="collapsed",
                                    )
                            with c3:
                                if form_n == "—":
                                    st.text_input(
                                        "N",
                                        value="—",
                                        key=f"free_input_pl_{case}_n",
                                        disabled=True,
                                        label_visibility="collapsed",
                                    )
                                else:
                                    st.text_input(
                                        "N",
                                        key=f"free_input_pl_{case}_n",
                                        placeholder="Neut",
                                        label_visibility="collapsed",
                                    )

                    st.markdown("---")
            else:
                # Regular display (nouns, personal pronouns, regular adjectives)
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("#### Singularis")
                    for case, label in zip(cases, case_labels):
                        key = f"{case[:3]}_sg"
                        correct_form = forms.get(key, "—")

                        if st.session_state.show_free_answers:
                            user_answer = st.session_state.user_free_answers.get(
                                f"free_input_sg_{case}", ""
                            )
                            is_correct = (
                                normalize_latin(user_answer.strip()).lower()
                                == normalize_latin(correct_form).lower()
                            )

                            if correct_form == "—":
                                st.info("—")
                            elif is_correct:
                                st.success(f"✅ {label}: **{correct_form}**")
                            else:
                                st.error(
                                    f"❌ {label}: Tu respuesta: '{user_answer}' → Correcto: **{correct_form}**"
                                )
                        else:
                            if correct_form == "—":
                                st.text_input(
                                    label,
                                    value="—",
                                    key=f"free_input_sg_{case}",
                                    disabled=True,
                                    label_visibility="collapsed",
                                )
                            else:
                                st.text_input(
                                    label,
                                    value="",
                                    key=f"free_input_sg_{case}",
                                    placeholder=f"{label} singular",
                                    label_visibility="collapsed",
                                )

                with col2:
                    st.markdown("#### Pluralis")
                    for case, label in zip(cases, case_labels):
                        key = f"{case[:3]}_pl"
                        correct_form = forms.get(key, "—")

                        if st.session_state.show_free_answers:
                            user_answer = st.session_state.user_free_answers.get(
                                f"free_input_pl_{case}", ""
                            )
                            is_correct = (
                                normalize_latin(user_answer.strip()).lower()
                                == normalize_latin(correct_form).lower()
                            )

                            if correct_form == "—":
                                st.info("—")
                            elif is_correct:
                                st.success(f"✅ {label}: **{correct_form}**")
                            else:
                                st.error(
                                    f"❌ {label}: Tu respuesta: '{user_answer}' → Correcto: **{correct_form}**"
                                )
                        else:
                            if correct_form == "—":
                                st.text_input(
                                    label,
                                    value="—",
                                    key=f"free_input_pl_{case}",
                                    disabled=True,
                                    label_visibility="collapsed",
                                )
                            else:
                                st.text_input(
                                    label,
                                    value="",
                                    key=f"free_input_pl_{case}",
                                    placeholder=f"{label} plural",
                                    label_visibility="collapsed",
                                )

            st.markdown("---")

            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                if st.button("✅ Verificar", width="stretch", key="decl_verify_free"):
                    # Save user answers
                    st.session_state.user_free_answers = {}

                    if is_demonstrative:
                        # Save all 3 genders x 2 numbers x 6 cases = 36 inputs
                        for case in cases:
                            for num in ["sg", "pl"]:
                                for g in ["m", "f", "n"]:
                                    key = f"free_input_{num}_{case}_{g}"
                                    if key in st.session_state:
                                        st.session_state.user_free_answers[key] = (
                                            st.session_state[key]
                                        )
                    else:
                        # Save regular inputs
                        for case in cases:
                            sg_key = f"free_input_sg_{case}"
                            pl_key = f"free_input_pl_{case}"
                            if sg_key in st.session_state:
                                st.session_state.user_free_answers[sg_key] = (
                                    st.session_state[sg_key]
                                )
                            if pl_key in st.session_state:
                                st.session_state.user_free_answers[pl_key] = (
                                    st.session_state[pl_key]
                                )

                    # Calculate score (NO XP awarded in free practice)
                    correct_count = 0
                    total_count = 0

                    for case in cases:
                        if is_demonstrative:
                            # Check 3 genders
                            for num in ["sg", "pl"]:
                                for g in ["m", "f", "n"]:
                                    key = f"free_input_{num}_{case}_{g}"
                                    user_ans = st.session_state.user_free_answers.get(
                                        key, ""
                                    )
                                    corr_form = forms.get(f"{case[:3]}_{num}_{g}", "")

                                    if user_ans.strip():
                                        total_count += 1
                                        if (
                                            normalize_latin(user_ans.strip()).lower()
                                            == normalize_latin(corr_form).lower()
                                        ):
                                            correct_count += 1
                        else:
                            # Regular check
                            sg_key = f"free_input_sg_{case}"
                            user_answer_sg = st.session_state.user_free_answers.get(
                                sg_key, ""
                            )
                            correct_form_sg = forms.get(f"{case[:3]}_sg", "")
                            if user_answer_sg.strip():
                                total_count += 1
                                if (
                                    normalize_latin(user_answer_sg.strip()).lower()
                                    == normalize_latin(correct_form_sg).lower()
                                ):
                                    correct_count += 1

                            pl_key = f"free_input_pl_{case}"
                            user_answer_pl = st.session_state.user_free_answers.get(
                                pl_key, ""
                            )
                            correct_form_pl = forms.get(f"{case[:3]}_pl", "")
                            if user_answer_pl.strip():
                                total_count += 1
                                if (
                                    normalize_latin(user_answer_pl.strip()).lower()
                                    == normalize_latin(correct_form_pl).lower()
                                ):
                                    correct_count += 1

                    # Just show score, NO XP
                    if total_count > 0:
                        percentage = (correct_count / total_count) * 100
                        st.info(
                            f"📊 Resultado: {correct_count}/{total_count} correctas ({percentage:.1f}%) • Sin XP"
                        )

                    st.session_state.show_free_answers = True
                    st.rerun()

            with col2:
                if st.button("🔄 Limpiar", width="stretch", key="decl_clear_free"):
                    st.session_state.show_free_answers = False
                    st.session_state.user_free_answers = {}
                    st.rerun()

            with col3:
                if st.button(
                    "🎲 Nueva Palabra", width="stretch", key="decl_new_word_free"
                ):
                    st.session_state.current_free_noun_id = random.choice(
                        filtered_words
                    ).id
                    st.session_state.show_free_answers = False
                    st.session_state.user_free_answers = {}
                    st.rerun()
