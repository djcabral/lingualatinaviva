import streamlit as st
import sys
import os
import random
import unicodedata

root_path = os.path.dirname(os.path.dirname(__file__))
if root_path not in sys.path:
    sys.path.append(root_path)

from database.connection import get_session
from database.models import Word
from sqlmodel import select
from utils.latin_logic import LatinMorphology
from utils.gamification import process_xp_gain

def normalize_latin(text):
    """Remove macrons and diacritics from Latin text for comparison"""
    # Normalize to NFD (decomposed form) then remove combining characters
    normalized = unicodedata.normalize('NFD', text)
    # Remove combining diacritical marks (macrons, etc.)
    return ''.join(char for char in normalized if unicodedata.category(char) != 'Mn')

st.set_page_config(page_title="Declinatio", page_icon="📜", layout="wide")

# Load CSS
def load_css():
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.markdown(
    """
    <h1 style='text-align: center; font-family: "Cinzel", serif;'>
        📜 Declinatio - Declinaciones
    </h1>
    """,
    unsafe_allow_html=True
)

morphology = LatinMorphology()

# Get user level for progressive learning
with get_session() as session:
    from database.models import UserProfile
    user = session.exec(select(UserProfile)).first()
    user_level = user.level if user else 1

st.markdown(f"### 📚 Nivel {user_level} - Sustantivos")

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
        nouns = session.exec(
            select(Word).where(
                Word.part_of_speech.in_(available_pos),
                Word.declension.in_(available_declensions)
            )
        ).all()
        
        if not nouns:
            st.warning("No hay sustantivos disponibles para tu nivel. Usa el panel de Admin para añadirlos.")
            st.stop()
        
        if 'current_noun' not in st.session_state:
            st.session_state.current_noun = random.choice(nouns)
        
        noun = st.session_state.current_noun
        
        
        st.markdown(f"### Declina: **{noun.latin}** ({noun.translation})")
        st.info(f"📋 Declinación: {noun.declension}ª • Género: {noun.gender} • Genitivo: {noun.genitive}")
        
        # Create declension table
        cases = ["nominativus", "vocativus", "accusativus", "genitivus", "dativus", "ablativus"]
        case_labels = ["Nominativus", "Vocativus", "Accusativus", "Genitivus", "Dativus", "Ablativus"]
        
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
                st.warning("Este sustantivo no tiene declinación o género definido.")
                st.stop()
            
            genitive = noun.genitive if noun.genitive else noun.latin
            forms = morphology.decline_noun(noun.latin, noun.declension, noun.gender, genitive, noun.irregular_forms, noun.parisyllabic)
            
            if not forms:
                st.warning("No se pudo generar la declinación para este sustantivo.")
                st.stop()

        
        
        # Check if this is a demonstrative pronoun (has gender forms)
        is_demonstrative = any(key.endswith('_m') or key.endswith('_f') or key.endswith('_n') for key in forms.keys())
        
        # Initialize show_answers state
        if 'show_declension_answers' not in st.session_state:
            st.session_state.show_declension_answers = False
        if 'user_declension_answers' not in st.session_state:
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
                        ans_m = st.session_state.user_declension_answers.get(f"input_sg_{case}_m", "")
                        corr_m = normalize_latin(ans_m.strip()).lower() == normalize_latin(form_m).lower()
                        with c1:
                            if form_m == "—": st.info("—")
                            elif corr_m: st.success(form_m)
                            else: st.error(f"{ans_m} → {form_m}")
                        
                        # FEMININE
                        ans_f = st.session_state.user_declension_answers.get(f"input_sg_{case}_f", "")
                        corr_f = normalize_latin(ans_f.strip()).lower() == normalize_latin(form_f).lower()
                        with c2:
                            if form_f == "—": st.info("—")
                            elif corr_f: st.success(form_f)
                            else: st.error(f"{ans_f} → {form_f}")
                            
                        # NEUTER
                        ans_n = st.session_state.user_declension_answers.get(f"input_sg_{case}_n", "")
                        corr_n = normalize_latin(ans_n.strip()).lower() == normalize_latin(form_n).lower()
                        with c3:
                            if form_n == "—": st.info("—")
                            elif corr_n: st.success(form_n)
                            else: st.error(f"{ans_n} → {form_n}")
                    else:
                        with c1: 
                            if form_m == "—": st.text_input("M", value="—", key=f"input_sg_{case}_m", disabled=True, label_visibility="collapsed")
                            else: st.text_input("M", key=f"input_sg_{case}_m", placeholder="Masc", label_visibility="collapsed")
                        with c2: 
                            if form_f == "—": st.text_input("F", value="—", key=f"input_sg_{case}_f", disabled=True, label_visibility="collapsed")
                            else: st.text_input("F", key=f"input_sg_{case}_f", placeholder="Fem", label_visibility="collapsed")
                        with c3: 
                            if form_n == "—": st.text_input("N", value="—", key=f"input_sg_{case}_n", disabled=True, label_visibility="collapsed")
                            else: st.text_input("N", key=f"input_sg_{case}_n", placeholder="Neut", label_visibility="collapsed")
                
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
                        ans_m = st.session_state.user_declension_answers.get(f"input_pl_{case}_m", "")
                        corr_m = normalize_latin(ans_m.strip()).lower() == normalize_latin(form_m).lower()
                        with c1:
                            if form_m == "—": st.info("—")
                            elif corr_m: st.success(form_m)
                            else: st.error(f"{ans_m} → {form_m}")
                        
                        # FEMININE
                        ans_f = st.session_state.user_declension_answers.get(f"input_pl_{case}_f", "")
                        corr_f = normalize_latin(ans_f.strip()).lower() == normalize_latin(form_f).lower()
                        with c2:
                            if form_f == "—": st.info("—")
                            elif corr_f: st.success(form_f)
                            else: st.error(f"{ans_f} → {form_f}")
                            
                        # NEUTER
                        ans_n = st.session_state.user_declension_answers.get(f"input_pl_{case}_n", "")
                        corr_n = normalize_latin(ans_n.strip()).lower() == normalize_latin(form_n).lower()
                        with c3:
                            if form_n == "—": st.info("—")
                            elif corr_n: st.success(form_n)
                            else: st.error(f"{ans_n} → {form_n}")
                    else:
                        with c1: 
                            if form_m == "—": st.text_input("M", value="—", key=f"input_pl_{case}_m", disabled=True, label_visibility="collapsed")
                            else: st.text_input("M", key=f"input_pl_{case}_m", placeholder="Masc", label_visibility="collapsed")
                        with c2: 
                            if form_f == "—": st.text_input("F", value="—", key=f"input_pl_{case}_f", disabled=True, label_visibility="collapsed")
                            else: st.text_input("F", key=f"input_pl_{case}_f", placeholder="Fem", label_visibility="collapsed")
                        with c3: 
                            if form_n == "—": st.text_input("N", value="—", key=f"input_pl_{case}_n", disabled=True, label_visibility="collapsed")
                            else: st.text_input("N", key=f"input_pl_{case}_n", placeholder="Neut", label_visibility="collapsed")
                
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
                        user_answer = st.session_state.user_declension_answers.get(f"input_sg_{case}", "")
                        # Normalize both for comparison (remove macrons)
                        is_correct = normalize_latin(user_answer.strip()).lower() == normalize_latin(correct_form).lower()
                        
                        # Display with color coding
                        if correct_form == "—":
                            st.info("—")
                        elif is_correct:
                            st.success(f"✅ {label}: **{correct_form}**")
                        else:
                            st.error(f"❌ {label}: Tu respuesta: '{user_answer}' → Correcto: **{correct_form}**")
                    else:
                        # Empty input for practice
                        if correct_form == "—":
                            st.text_input(label, value="—", key=f"input_sg_{case}", disabled=True, label_visibility="collapsed")
                        else:
                            st.text_input(label, value="", key=f"input_sg_{case}", placeholder=f"{label} singular", label_visibility="collapsed")
            
            with col2:
                st.markdown("#### Pluralis")
                for case, label in zip(cases, case_labels):
                    key = f"{case[:3]}_pl"
                    correct_form = forms.get(key, "—")
                    
                    if st.session_state.show_declension_answers:
                        # Show user's answer and correct answer
                        user_answer = st.session_state.user_declension_answers.get(f"input_pl_{case}", "")
                        # Normalize both for comparison (remove macrons)
                        is_correct = normalize_latin(user_answer.strip()).lower() == normalize_latin(correct_form).lower()
                        
                        # Display with color coding
                        if correct_form == "—":
                            st.info("—")
                        elif is_correct:
                            st.success(f"✅ {label}: **{correct_form}**")
                        else:
                            st.error(f"❌ {label}: Tu respuesta: '{user_answer}' → Correcto: **{correct_form}**")
                    else:
                        # Empty input for practice
                        if correct_form == "—":
                            st.text_input(label, value="—", key=f"input_pl_{case}", disabled=True, label_visibility="collapsed")
                        else:
                            st.text_input(label, value="", key=f"input_pl_{case}", placeholder=f"{label} plural", label_visibility="collapsed")
        
        # Show XP feedback if available
        if 'xp_feedback' in st.session_state and st.session_state.show_declension_answers:
            st.success(st.session_state.xp_feedback)
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("✅ Verificar", use_container_width=True):
                # Save user answers
                st.session_state.user_declension_answers = {}
                
                if is_demonstrative:
                    # Save all 3 genders x 2 numbers x 6 cases = 36 inputs
                    for case in cases:
                        for num in ["sg", "pl"]:
                            for g in ["m", "f", "n"]:
                                key = f"input_{num}_{case}_{g}"
                                if key in st.session_state:
                                    st.session_state.user_declension_answers[key] = st.session_state[key]
                else:
                    # Save regular inputs
                    for case in cases:
                        sg_key = f"input_sg_{case}"
                        pl_key = f"input_pl_{case}"
                        if sg_key in st.session_state:
                            st.session_state.user_declension_answers[sg_key] = st.session_state[sg_key]
                        if pl_key in st.session_state:
                            st.session_state.user_declension_answers[pl_key] = st.session_state[pl_key]
                
                # Calculate score and award XP
                correct_count = 0
                total_count = 0
                
                for case in cases:
                    if is_demonstrative:
                        # Check 3 genders
                        for num in ["sg", "pl"]:
                            for g in ["m", "f", "n"]:
                                key = f"input_{num}_{case}_{g}"
                                user_ans = st.session_state.user_declension_answers.get(key, "")
                                corr_form = forms.get(f"{case[:3]}_{num}_{g}", "")
                                
                                if user_ans.strip():
                                    total_count += 1
                                    if normalize_latin(user_ans.strip()).lower() == normalize_latin(corr_form).lower():
                                        correct_count += 1
                    else:
                        # Regular check
                        # Singular
                        sg_key = f"input_sg_{case}"
                        user_answer_sg = st.session_state.user_declension_answers.get(sg_key, "")
                        correct_form_sg = forms.get(f"{case[:3]}_sg", "")
                        if user_answer_sg.strip():  # Solo contar si el usuario respondió
                            total_count += 1
                            if normalize_latin(user_answer_sg.strip()).lower() == normalize_latin(correct_form_sg).lower():
                                correct_count += 1
                        
                        # Plural
                        pl_key = f"input_pl_{case}"
                        user_answer_pl = st.session_state.user_declension_answers.get(pl_key, "")
                        correct_form_pl = forms.get(f"{case[:3]}_pl", "")
                        if user_answer_pl.strip():  # Solo contar si el usuario respondió
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
                            st.session_state.xp_feedback = f"🎉 +{xp_gained} XP ({correct_count}/{total_count} correctas)"
                
                st.session_state.show_declension_answers = True
                st.rerun()
        
        with col2:
            if st.button("🔄 Limpiar", use_container_width=True):
                st.session_state.show_declension_answers = False
                st.session_state.user_declension_answers = {}
                st.rerun()
        
        with col3:
            if st.button("🎲 Nueva Palabra", use_container_width=True):
                st.session_state.current_noun = random.choice(nouns)
                st.session_state.show_declension_answers = False
                st.session_state.user_declension_answers = {}
                st.rerun()

# ===== TAB 2: FREE PRACTICE =====
with practice_tabs[1]:
    st.markdown("### Práctica Libre")
    st.info("🎯 Elige exactamente qué quieres practicar. **Esta práctica NO otorga XP.**")
    
    # Filters
    st.markdown("#### Filtros de selección")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_pos = st.selectbox(
            "Tipo de palabra",
            options=["noun", "adjective", "pronoun"],
            format_func=lambda x: {"noun": "Sustantivo", "adjective": "Adjetivo", "pronoun": "Pronombre"}[x],
            key="free_pos"
        )
    
    # Dynamic filters based on POS
    with col2:
        if filter_pos == "noun":
            filter_declension = st.multiselect(
                "Declinaciones",
                options=["1", "2", "3", "4", "5"],
                default=["1"],
                format_func=lambda x: f"{x}ª declinación",
                key="free_decl_noun"
            )
        elif filter_pos == "adjective":
            filter_adj_class = st.multiselect(
                "Clase de adjetivo",
                options=["1-2", "3"],
                default=["1-2"],
                format_func=lambda x: {"1-2": "1ª clase (1-2 decl.)", "3": "2ª clase (3ª decl.)"}[x],
                key="free_adj_class"
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
                    "interrogative": "Interrogativo"
                }[x],
                key="free_pron_type"
            )
    
    with col3:
        if filter_pos == "noun":
            # Determine valid genders based on selected declensions
            valid_genders = set()
            if filter_declension:
                for decl in filter_declension:
                    if decl == "1":
                        valid_genders.update(["m", "f"])  # 1ª: mayormente femenino, algunos masculinos
                    elif decl == "2":
                        valid_genders.update(["m", "f", "n"])  # 2ª: masculino y neutro (algunos femeninos)
                    elif decl == "3":
                        valid_genders.update(["m", "f", "n"])  # 3ª: todos los géneros
                    elif decl == "4":
                        valid_genders.update(["m", "f", "n"])  # 4ª: mayormente masculino, algunos femeninos y neutros
                    elif decl == "5":
                        valid_genders.update(["m", "f"])  # 5ª: mayormente femenino, algunos masculinos
            else:
                valid_genders = {"m", "f", "n"}  # Si no hay declinación seleccionada, mostrar todos
            
            available_genders = sorted(list(valid_genders), key=lambda x: ["m", "f", "n"].index(x))
            
            # Ajustar default para incluir solo géneros válidos
            default_genders = [g for g in ["m", "f", "n"] if g in available_genders]
            
            filter_gender = st.multiselect(
                "Género",
                options=available_genders,
                default=default_genders,
                format_func=lambda x: {"m": "Masculino", "f": "Femenino", "n": "Neutro"}[x],
                key="free_gender_noun"
            )
        elif filter_pos == "adjective":
            filter_degree = st.multiselect(
                "Grado",
                options=["positive", "comparative", "superlative"],
                default=["positive"],
                format_func=lambda x: {"positive": "Positivo", "comparative": "Comparativo", "superlative": "Superlativo"}[x],
                key="free_degree"
            )
        else:
            st.write("")  # Empty space for pronouns
    
    # Build query based on filters
    with get_session() as session:
        query = select(Word).where(Word.part_of_speech == filter_pos)
        
        if filter_pos == "noun":
            if not filter_declension or not filter_gender:
                st.warning("⚠️ Debes seleccionar al menos una declinación y un género.")
                st.stop()
            query = query.where(
                Word.declension.in_(filter_declension),
                Word.gender.in_(filter_gender)
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
            st.warning("❌ No hay palabras disponibles con estos filtros. Usa el panel de Admin para añadir más palabras.")
            st.stop()
        
        st.success(f"✅ {len(filtered_words)} palabra(s) disponible(s) con estos filtros")
        
        # Word selection
        if 'current_free_noun' not in st.session_state:
            st.session_state.current_free_noun = random.choice(filtered_words)
        
        # Check if current word matches filters, if not pick a new one
        current_word = st.session_state.current_free_noun
        if current_word not in filtered_words:
            st.session_state.current_free_noun = random.choice(filtered_words)
            current_word = st.session_state.current_free_noun
        
        noun = current_word
        
        st.markdown("---")
        st.markdown(f"### Declina: **{noun.latin}** ({noun.translation})")
        st.info(f"📋 Declinación: {noun.declension}ª • Género: {noun.gender} • Genitivo: {noun.genitive}")
        
        # Create declension table
        cases = ["nominativus", "vocativus", "accusativus", "genitivus", "dativus", "ablativus"]
        case_labels = ["Nominativus", "Vocativus", "Accusativus", "Genitivus", "Dativus", "Ablativus"]
        
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
            forms = morphology.decline_noun(noun.latin, noun.declension, noun.gender, genitive, noun.irregular_forms, noun.parisyllabic)
            
            if not forms:
                st.warning("No se pudo generar la declinación para esta palabra.")
                st.stop()
        
        # Initialize show_answers state for free practice
        if 'show_free_answers' not in st.session_state:
            st.session_state.show_free_answers = False
        if 'user_free_answers' not in st.session_state:
            st.session_state.user_free_answers = {}
        
        # Check if demonstrative (has gender forms)
        is_demonstrative = any(key.endswith('_m') or key.endswith('_f') or key.endswith('_n') for key in forms.keys())
        
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
                        ans_m = st.session_state.user_free_answers.get(f"free_input_sg_{case}_m", "")
                        corr_m = normalize_latin(ans_m.strip()).lower() == normalize_latin(form_m).lower()
                        with c1:
                            if form_m == "—": st.info("—")
                            elif corr_m: st.success(form_m)
                            else: st.error(f"{ans_m} → {form_m}")
                        
                        # FEMININE
                        ans_f = st.session_state.user_free_answers.get(f"free_input_sg_{case}_f", "")
                        corr_f = normalize_latin(ans_f.strip()).lower() == normalize_latin(form_f).lower()
                        with c2:
                            if form_f == "—": st.info("—")
                            elif corr_f: st.success(form_f)
                            else: st.error(f"{ans_f} → {form_f}")
                            
                        # NEUTER
                        ans_n = st.session_state.user_free_answers.get(f"free_input_sg_{case}_n", "")
                        corr_n = normalize_latin(ans_n.strip()).lower() == normalize_latin(form_n).lower()
                        with c3:
                            if form_n == "—": st.info("—")
                            elif corr_n: st.success(form_n)
                            else: st.error(f"{ans_n} → {form_n}")
                    else:
                        with c1: 
                            if form_m == "—": st.text_input("M", value="—", key=f"free_input_sg_{case}_m", disabled=True, label_visibility="collapsed")
                            else: st.text_input("M", key=f"free_input_sg_{case}_m", placeholder="Masc", label_visibility="collapsed")
                        with c2: 
                            if form_f == "—": st.text_input("F", value="—", key=f"free_input_sg_{case}_f", disabled=True, label_visibility="collapsed")
                            else: st.text_input("F", key=f"free_input_sg_{case}_f", placeholder="Fem", label_visibility="collapsed")
                        with c3: 
                            if form_n == "—": st.text_input("N", value="—", key=f"free_input_sg_{case}_n", disabled=True, label_visibility="collapsed")
                            else: st.text_input("N", key=f"free_input_sg_{case}_n", placeholder="Neut", label_visibility="collapsed")
                
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
                        ans_m = st.session_state.user_free_answers.get(f"free_input_pl_{case}_m", "")
                        corr_m = normalize_latin(ans_m.strip()).lower() == normalize_latin(form_m).lower()
                        with c1:
                            if form_m == "—": st.info("—")
                            elif corr_m: st.success(form_m)
                            else: st.error(f"{ans_m} → {form_m}")
                        
                        # FEMININE
                        ans_f = st.session_state.user_free_answers.get(f"free_input_pl_{case}_f", "")
                        corr_f = normalize_latin(ans_f.strip()).lower() == normalize_latin(form_f).lower()
                        with c2:
                            if form_f == "—": st.info("—")
                            elif corr_f: st.success(form_f)
                            else: st.error(f"{ans_f} → {form_f}")
                            
                        # NEUTER
                        ans_n = st.session_state.user_free_answers.get(f"free_input_pl_{case}_n", "")
                        corr_n = normalize_latin(ans_n.strip()).lower() == normalize_latin(form_n).lower()
                        with c3:
                            if form_n == "—": st.info("—")
                            elif corr_n: st.success(form_n)
                            else: st.error(f"{ans_n} → {form_n}")
                    else:
                        with c1: 
                            if form_m == "—": st.text_input("M", value="—", key=f"free_input_pl_{case}_m", disabled=True, label_visibility="collapsed")
                            else: st.text_input("M", key=f"free_input_pl_{case}_m", placeholder="Masc", label_visibility="collapsed")
                        with c2: 
                            if form_f == "—": st.text_input("F", value="—", key=f"free_input_pl_{case}_f", disabled=True, label_visibility="collapsed")
                            else: st.text_input("F", key=f"free_input_pl_{case}_f", placeholder="Fem", label_visibility="collapsed")
                        with c3: 
                            if form_n == "—": st.text_input("N", value="—", key=f"free_input_pl_{case}_n", disabled=True, label_visibility="collapsed")
                            else: st.text_input("N", key=f"free_input_pl_{case}_n", placeholder="Neut", label_visibility="collapsed")
                
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
                        user_answer = st.session_state.user_free_answers.get(f"free_input_sg_{case}", "")
                        is_correct = normalize_latin(user_answer.strip()).lower() == normalize_latin(correct_form).lower()
                        
                        if correct_form == "—":
                            st.info("—")
                        elif is_correct:
                            st.success(f"✅ {label}: **{correct_form}**")
                        else:
                            st.error(f"❌ {label}: Tu respuesta: '{user_answer}' → Correcto: **{correct_form}**")
                    else:
                        if correct_form == "—":
                            st.text_input(label, value="—", key=f"free_input_sg_{case}", disabled=True, label_visibility="collapsed")
                        else:
                            st.text_input(label, value="", key=f"free_input_sg_{case}", placeholder=f"{label} singular", label_visibility="collapsed")
            
            with col2:
                st.markdown("#### Pluralis")
                for case, label in zip(cases, case_labels):
                    key = f"{case[:3]}_pl"
                    correct_form = forms.get(key, "—")
                    
                    if st.session_state.show_free_answers:
                        user_answer = st.session_state.user_free_answers.get(f"free_input_pl_{case}", "")
                        is_correct = normalize_latin(user_answer.strip()).lower() == normalize_latin(correct_form).lower()
                        
                        if correct_form == "—":
                            st.info("—")
                        elif is_correct:
                            st.success(f"✅ {label}: **{correct_form}**")
                        else:
                            st.error(f"❌ {label}: Tu respuesta: '{user_answer}' → Correcto: **{correct_form}**")
                    else:
                        if correct_form == "—":
                            st.text_input(label, value="—", key=f"free_input_pl_{case}", disabled=True, label_visibility="collapsed")
                        else:
                            st.text_input(label, value="", key=f"free_input_pl_{case}", placeholder=f"{label} plural", label_visibility="collapsed")
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("✅ Verificar", use_container_width=True, key="verify_free"):
                # Save user answers
                st.session_state.user_free_answers = {}
                
                if is_demonstrative:
                    # Save all 3 genders x 2 numbers x 6 cases = 36 inputs
                    for case in cases:
                        for num in ["sg", "pl"]:
                            for g in ["m", "f", "n"]:
                                key = f"free_input_{num}_{case}_{g}"
                                if key in st.session_state:
                                    st.session_state.user_free_answers[key] = st.session_state[key]
                else:
                    # Save regular inputs
                    for case in cases:
                        sg_key = f"free_input_sg_{case}"
                        pl_key = f"free_input_pl_{case}"
                        if sg_key in st.session_state:
                            st.session_state.user_free_answers[sg_key] = st.session_state[sg_key]
                        if pl_key in st.session_state:
                            st.session_state.user_free_answers[pl_key] = st.session_state[pl_key]
                
                # Calculate score (NO XP awarded in free practice)
                correct_count = 0
                total_count = 0
                
                for case in cases:
                    if is_demonstrative:
                        # Check 3 genders
                        for num in ["sg", "pl"]:
                            for g in ["m", "f", "n"]:
                                key = f"free_input_{num}_{case}_{g}"
                                user_ans = st.session_state.user_free_answers.get(key, "")
                                corr_form = forms.get(f"{case[:3]}_{num}_{g}", "")
                                
                                if user_ans.strip():
                                    total_count += 1
                                    if normalize_latin(user_ans.strip()).lower() == normalize_latin(corr_form).lower():
                                        correct_count += 1
                    else:
                        # Regular check
                        sg_key = f"free_input_sg_{case}"
                        user_answer_sg = st.session_state.user_free_answers.get(sg_key, "")
                        correct_form_sg = forms.get(f"{case[:3]}_sg", "")
                        if user_answer_sg.strip():
                            total_count += 1
                            if normalize_latin(user_answer_sg.strip()).lower() == normalize_latin(correct_form_sg).lower():
                                correct_count += 1
                        
                        pl_key = f"free_input_pl_{case}"
                        user_answer_pl = st.session_state.user_free_answers.get(pl_key, "")
                        correct_form_pl = forms.get(f"{case[:3]}_pl", "")
                        if user_answer_pl.strip():
                            total_count += 1
                            if normalize_latin(user_answer_pl.strip()).lower() == normalize_latin(correct_form_pl).lower():
                                correct_count += 1
                
                # Just show score, NO XP
                if total_count > 0:
                    percentage = (correct_count / total_count) * 100
                    st.info(f"📊 Resultado: {correct_count}/{total_count} correctas ({percentage:.1f}%) • Sin XP")
                
                st.session_state.show_free_answers = True
                st.rerun()
        
        with col2:
            if st.button("🔄 Limpiar", use_container_width=True, key="clear_free"):
                st.session_state.show_free_answers = False
                st.session_state.user_free_answers = {}
                st.rerun()
        
        with col3:
            if st.button("🎲 Nueva Palabra", use_container_width=True, key="new_word_free"):
                st.session_state.current_free_noun = random.choice(filtered_words)
                st.session_state.show_free_answers = False
                st.session_state.user_free_answers = {}
                st.rerun()
