import streamlit as st
import sys
import os
import json
import re
import unicodedata
from sqlmodel import select
import pandas as pd

root_path = os.path.dirname(os.path.dirname(__file__))
if root_path not in sys.path:
    sys.path.append(root_path)

from database.connection import get_session, init_db
from database import Word, Text, ReviewLog, UserProfile, TextWordLink, Lesson
from database import SentenceAnalysis, TokenAnnotation, SentenceStructure
from database import LessonRequirement, UserLessonProgress
from utils.csv_handler import import_vocabulary_from_csv, export_vocabulary_to_excel

from utils.i18n import get_text
from utils.ui_helpers import load_css
from utils.text_utils import normalize_latin
from utils.content_importer import ContentImporter as NLPContentImporter

st.set_page_config(page_title="Admin", page_icon="⚙️", layout="wide")

load_css()
from utils.ui_helpers import render_sidebar_config
render_sidebar_config()

st.markdown(
    """
    <h1 style='text-align: center; font-family: "Cinzel", serif;'>
        ⚙️ Admin - Panel de Administración
    </h1>
    """,
    unsafe_allow_html=True
)

# Admin Authentication
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

if not st.session_state.is_admin:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🔒 Acceso Restringido")
        password = st.text_input("Contraseña de Administrador", type="password")
        if st.button("Ingresar", type="primary", width='stretch'):
            if password == "admin123":  # Simple hardcoded password
                st.session_state.is_admin = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta")
    st.stop()

# Logout button
with st.sidebar:
    if st.button("🔒 Cerrar Sesión"):
        st.session_state.is_admin = False
        st.rerun()

# Importar módulo de catalogación (si está disponible)
try:
    from utils.admin_catalog_module import get_catalog_module
    catalog_module = get_catalog_module()
except ImportError:
    catalog_module = None

# Sidebar Navigation - Agregar Catalogación si está disponible
sections = ["Vocabulario", "Textos", "Lecciones", "Ejercicios", "Sintaxis", "Usuario", "Estadísticas", "Requisitos de Lección"]
if catalog_module and catalog_module.is_available:
    sections.append("Catalogación")
sections.append("Configuración")

section = st.sidebar.radio(
    "Sección",
    sections,
    index=0
)

st.sidebar.markdown("---")
st.sidebar.info("Usa este panel para gestionar el contenido de la aplicación.")

def normalize_latin(text):
    """Remove macrons and diacritics for matching"""
    normalized = unicodedata.normalize('NFD', text)
    return ''.join(char for char in normalized if unicodedata.category(char) != 'Mn')

# --- SECTION: VOCABULARY ---
if section == "Vocabulario":
    st.markdown("## 📚 Gestión de Vocabulario")
    
    # Check if we're editing a word from dictionary
    editing_word_id = st.session_state.get('word_to_edit', None)
    
    if editing_word_id:
        # Load the word to edit and convert to dict
        with get_session() as session:
            word_obj = session.get(Word, editing_word_id)
            if word_obj:
                # Convert to dict to avoid DetachedInstanceError
                word_to_edit = {
                    'id': word_obj.id,
                    'latin': word_obj.latin,
                    'translation': word_obj.translation,
                    'part_of_speech': word_obj.part_of_speech,
                    'level': word_obj.level,
                    'genitive': word_obj.genitive,
                    'gender': word_obj.gender,
                    'declension': word_obj.declension,
                    'parisyllabic': word_obj.parisyllabic,
                    'is_plurale_tantum': word_obj.is_plurale_tantum,
                    'is_singulare_tantum': word_obj.is_singulare_tantum,
                    'irregular_forms': word_obj.irregular_forms,
                    'principal_parts': word_obj.principal_parts,
                    'conjugation': word_obj.conjugation,
                    'is_invariable': word_obj.is_invariable
                }
            else:
                word_to_edit = None
            
        if word_to_edit:
            st.info(f"✏️ **Editando palabra:** {word_to_edit['latin']}")
            
            # Create tab list with Edit tab first
            tab_list = ["✏️ Editar", "➕ Sustantivos", "➕ Verbos", "➕ Adjetivos", "➕ Otros", "📥 Importar", "📤 Exportar", "📋 Lista Completa", "❓ Ayuda"]
            vocab_tabs = st.tabs(tab_list)
            
            # Edit tab
            with vocab_tabs[0]:
                st.markdown(f"### Editar: {word_to_edit['latin']}")
                
                # Determine word type and show appropriate form
                pos = word_to_edit['part_of_speech']
                
                if pos == "noun":
                    with st.form("edit_noun"):
                        col1, col2 = st.columns(2)
                        with col1:
                            latin = st.text_input("Nominativo Singular *", value=word_to_edit['latin'])
                            translation = st.text_input("Traducción *", value=word_to_edit['translation'] or "")
                            level = st.number_input("Nivel", min_value=1, max_value=10, value=word_to_edit['level'] or 1)
                        
                        with col2:
                            genitive = st.text_input("Genitivo Singular *", value=word_to_edit['genitive'] or "")
                            gender = st.selectbox("Género *", ["m", "f", "n"], index=["m", "f", "n"].index(word_to_edit['gender']) if word_to_edit['gender'] else 0)
                            declension = st.selectbox("Declinación *", ["1", "2", "3", "4", "5"], index=int(word_to_edit['declension'])-1 if word_to_edit['declension'] else 0)
                        
                        col3, col4 = st.columns(2)
                        with col3:
                            parisyllabic = st.checkbox("Parisílabo", value=word_to_edit['parisyllabic'] or False)
                        with col4:
                            is_plurale_tantum = st.checkbox("Pluralia tantum", value=word_to_edit['is_plurale_tantum'] or False)
                            is_singulare_tantum = st.checkbox("Singularia tantum", value=word_to_edit['is_singulare_tantum'] or False, disabled=is_plurale_tantum)
                        
                        irregular_forms = st.text_area("Formas Irregulares (JSON)", value=word_to_edit['irregular_forms'] or "")
                        
                        col_submit, col_cancel = st.columns(2)
                        with col_submit:
                            submitted = st.form_submit_button("💾 Guardar Cambios", type="primary")
                        with col_cancel:
                            cancelled = st.form_submit_button("❌ Cancelar")
                        
                        if cancelled:
                            del st.session_state.word_to_edit
                            st.rerun()
                        
                        if submitted:
                            if latin and translation and genitive and gender and declension:
                                with get_session() as session:
                                    db_word = session.get(Word, editing_word_id)
                                    db_word.latin = latin
                                    db_word.translation = translation
                                    db_word.level = level
                                    db_word.genitive = genitive
                                    db_word.gender = gender
                                    db_word.declension = declension
                                    db_word.parisyllabic = parisyllabic if declension == "3" else None
                                    db_word.is_plurale_tantum = is_plurale_tantum
                                    db_word.is_singulare_tantum = is_singulare_tantum
                                    db_word.irregular_forms = irregular_forms if irregular_forms else None
                                    session.add(db_word)
                                    session.commit()
                                    st.success(f"✅ Palabra '{latin}' actualizada")
                                    del st.session_state.word_to_edit
                                    st.balloons()
                                    st.rerun()
                            else:
                                st.error("Faltan campos obligatorios")
                
                elif pos == "verb":
                    with st.form("edit_verb"):
                        col1, col2 = st.columns(2)
                        with col1:
                            latin = st.text_input("Presente 1ª Persona *", value=word_to_edit['latin'])
                            translation = st.text_input("Traducción *", value=word_to_edit['translation'] or "")
                            level = st.number_input("Nivel", min_value=1, max_value=10, value=word_to_edit['level'] or 1)
                        
                        with col2:
                            principal_parts = st.text_input("Partes Principales *", value=word_to_edit['principal_parts'] or "")
                            conjugation = st.selectbox("Conjugación *", ["1", "2", "3", "4", "irregular"], 
                                                      index=["1", "2", "3", "4", "irregular"].index(word_to_edit['conjugation']) if word_to_edit['conjugation'] else 0)
                            irregular_forms = st.text_area("Formas Irregulares", value=word_to_edit['irregular_forms'] or "")
                        
                        col_submit, col_cancel = st.columns(2)
                        with col_submit:
                            submitted = st.form_submit_button("💾 Guardar Cambios", type="primary")
                        with col_cancel:
                            cancelled = st.form_submit_button("❌ Cancelar")
                        
                        if cancelled:
                            del st.session_state.word_to_edit
                            st.rerun()
                        
                        if submitted:
                            if latin and translation and principal_parts and conjugation:
                                with get_session() as session:
                                    db_word = session.get(Word, editing_word_id)
                                    db_word.latin = latin
                                    db_word.translation = translation
                                    db_word.level = level
                                    db_word.principal_parts = principal_parts
                                    db_word.conjugation = conjugation
                                    db_word.irregular_forms = irregular_forms if irregular_forms else None
                                    session.add(db_word)
                                    session.commit()
                                    st.success(f"✅ Verbo '{latin}' actualizado")
                                    del st.session_state.word_to_edit
                                    st.balloons()
                                    st.rerun()
                            else:
                                st.error("Faltan campos obligatorios")
                
                else:
                    # Other word types
                    with st.form("edit_other"):
                        col1, col2 = st.columns(2)
                        with col1:
                            latin = st.text_input("Palabra *", value=word_to_edit['latin'])
                            translation = st.text_input("Traducción *", value=word_to_edit['translation'] or "")
                            level = st.number_input("Nivel", min_value=1, max_value=10, value=word_to_edit['level'] or 1)
                        
                        with col2:
                            pos_options = {"Adverbio": "adverb", "Preposición": "preposition", "Conjunción": "conjunction", "Pronombre": "pronoun", "Adjetivo": "adjective"}
                            pos_display = [k for k, v in pos_options.items() if v == pos][0] if pos in pos_options.values() else "Adverbio"
                            pos_new = pos_options[st.selectbox("Tipo *", list(pos_options.keys()), index=list(pos_options.keys()).index(pos_display))]
                            is_invariable = st.checkbox("Es invariable", value=word_to_edit['is_invariable'] or False)
                        
                        col_submit, col_cancel = st.columns(2)
                        with col_submit:
                            submitted = st.form_submit_button("💾 Guardar Cambios", type="primary")
                        with col_cancel:
                            cancelled = st.form_submit_button("❌ Cancelar")
                        
                        if cancelled:
                            del st.session_state.word_to_edit
                            st.rerun()
                        
                        if submitted:
                            if latin and translation:
                                with get_session() as session:
                                    db_word = session.get(Word, editing_word_id)
                                    db_word.latin = latin
                                    db_word.translation = translation
                                    db_word.level = level
                                    db_word.part_of_speech = pos_new
                                    db_word.is_invariable = is_invariable
                                    session.add(db_word)
                                    session.commit()
                                    st.success(f"✅ Palabra '{latin}' actualizada")
                                    del st.session_state.word_to_edit
                                    st.balloons()
                                    st.rerun()
                            else:
                                st.error("Faltan campos obligatorios")
            
            # Adjust indices for other tabs (they're now shifted by 1)
            noun_tab_idx = 1
            verb_tab_idx = 2
            adj_tab_idx = 3
            other_tab_idx = 4
            import_tab_idx = 5
            export_tab_idx = 6
            list_tab_idx = 7
            help_tab_idx = 8
        else:
            st.warning("Palabra no encontrada")
            if st.button("Volver a añadir palabras"):
                del st.session_state.word_to_edit
                st.rerun()
            vocab_tabs = st.tabs(["➕ Sustantivos", "➕ Verbos", "➕ Adjetivos", "➕ Otros", "📥 Importar", "📤 Exportar", "📋 Lista Completa", "❓ Ayuda"])
            noun_tab_idx = 0
            verb_tab_idx = 1
            adj_tab_idx = 2
            other_tab_idx = 3
            import_tab_idx = 4
            export_tab_idx = 5
            list_tab_idx = 6
            help_tab_idx = 7
    else:
        # Normal mode - no editing
        vocab_tabs = st.tabs(["➕ Sustantivos", "➕ Verbos", "➕ Adjetivos", "➕ Otros", "📥 Importar", "📤 Exportar", "📋 Lista Completa", "❓ Ayuda"])
        noun_tab_idx = 0
        verb_tab_idx = 1
        adj_tab_idx = 2
        other_tab_idx = 3
        import_tab_idx = 4
        export_tab_idx = 5
        list_tab_idx = 6
        help_tab_idx = 7
    
    # --- Tab: Nouns ---
    with vocab_tabs[noun_tab_idx]:
        st.markdown("### Añadir Sustantivo")
        with st.form("add_noun"):
            col1, col2 = st.columns(2)
            with col1:
                latin = st.text_input("Nominativo Singular *")
                translation = st.text_input("Traducción *")
                level = st.number_input("Nivel", min_value=1, max_value=10, value=1, key="noun_level")
            
            with col2:
                genitive = st.text_input("Genitivo Singular *")
                gender = st.selectbox("Género *", ["m", "f", "n"])
                declension = st.selectbox("Declinación *", ["1", "2", "3", "4", "5"])
                
            # Add parisyllabic and pluralia/singularia tantum options
            col3, col4 = st.columns(2)
            with col3:
                parisyllabic = st.checkbox("Parisílabo (solo 3ª decl.)", help="Marca si es parisílabo (para 3ª declinación)")
            with col4:
                pass
            
            col5, col6 = st.columns(2)
            with col5:
                is_plurale_tantum = st.checkbox(
                    "🔢 Pluralia tantum (solo plural)", 
                    help="Palabras como castra, arma, divitiae que solo existen en plural"
                )
            with col6:
                is_singulare_tantum = st.checkbox(
                    "1️⃣ Singularia tantum (solo singular)", 
                    help="Sustantivos que solo existen en singular",
                    disabled=is_plurale_tantum
                )
            
            if is_plurale_tantum and is_singulare_tantum:
                st.error("❌ Una palabra no puede ser pluralia tantum Y singularia tantum a la vez")
                
            irregular_forms = st.text_area("Formas Irregulares (JSON)", help='Ejemplo: {"dat_pl": "filiābus"}', key="noun_irr")

            
            submitted = st.form_submit_button("✅ Guardar Sustantivo", type="primary")
            
            if submitted:
                if latin and translation and genitive and gender and declension:
                    irregular_json = None
                    if irregular_forms:
                        try:
                            json.loads(irregular_forms)
                            irregular_json = irregular_forms
                        except json.JSONDecodeError:
                            st.error("❌ JSON inválido")
                            st.stop()
                    
                    with get_session() as session:
                        word = Word(
                            latin=latin, translation=translation, part_of_speech="noun", level=level,
                            genitive=genitive, gender=gender, declension=declension,
                            irregular_forms=irregular_json, category="noun",
                            parisyllabic=parisyllabic if declension == "3" else None,
                            is_plurale_tantum=is_plurale_tantum,
                            is_singulare_tantum=is_singulare_tantum
                        )
                        session.add(word)
                        session.commit()
                        st.success(f"Sustantivo '{latin}' añadido.")
                else:
                    st.error("Faltan campos obligatorios.")

    # --- Tab: Verbs ---
    with vocab_tabs[1]:
        st.markdown("### Añadir Verbo")
        with st.form("add_verb"):
            col1, col2 = st.columns(2)
            with col1:
                latin = st.text_input("Presente 1ª Persona (o Infinitivo) *")
                translation = st.text_input("Traducción *")
                level = st.number_input("Nivel", min_value=1, max_value=10, value=1, key="verb_level")
            
            with col2:
                principal_parts = st.text_input("Partes Principales *", help="Ej: amo, amare, amavi, amatum")
                conjugation = st.selectbox("Conjugación *", ["1", "2", "3", "4", "irregular"])
                irregular_forms = st.text_area("Formas Irregulares (JSON)", help='Ejemplo: {"pres_3sg": "est"}', key="verb_irr")
            
            submitted = st.form_submit_button("✅ Guardar Verbo", type="primary")
            
            if submitted:
                if latin and translation and principal_parts and conjugation:
                    irregular_json = None
                    if irregular_forms:
                        try:
                            json.loads(irregular_forms)
                            irregular_json = irregular_forms
                        except json.JSONDecodeError:
                            st.error("❌ JSON inválido")
                            st.stop()
                            
                    with get_session() as session:
                        word = Word(
                            latin=latin, translation=translation, part_of_speech="verb", level=level,
                            principal_parts=principal_parts, conjugation=conjugation,
                            irregular_forms=irregular_json, category="verb"
                        )
                        session.add(word)
                        session.commit()
                        st.success(f"Verbo '{latin}' añadido.")
                else:
                    st.error("Faltan campos obligatorios.")

    # --- Tab: Adjectives ---
    with vocab_tabs[2]:
        st.markdown("### Añadir Adjetivo")
        with st.form("add_adjective"):
            col1, col2 = st.columns(2)
            with col1:
                latin = st.text_input("Nominativo Singular (Masc) *", help="Ej: bonus, miser, acer, fortis, audax")
                translation = st.text_input("Traducción *")
                level = st.number_input("Nivel", min_value=1, max_value=10, value=1, key="adj_level")
            
            with col2:
                adj_class = st.selectbox(
                    "Clase de Adjetivo *",
                    [
                        "1ª Clase (2-1-2) - us/a/um (bonus)",
                        "1ª Clase (2-1-2) - er/a/um (miser)",
                        "2ª Clase (3ª Decl) - 3 terminaciones (acer)",
                        "2ª Clase (3ª Decl) - 2 terminaciones (fortis)",
                        "2ª Clase (3ª Decl) - 1 terminación (audax)"
                    ]
                )
            
            # Dynamic fields based on class
            st.markdown("#### Formas Adicionales")
            col3, col4 = st.columns(2)
            
            irregular_json = {}
            genitive_val = None
            declension_val = "1/2"
            category_val = "adj_1"
            fem_form = None
            neut_form = None
            
            if "1ª Clase" in adj_class:
                declension_val = "1/2"
                category_val = "adj_1"
                st.info("ℹ️ Se generarán automáticamente las formas femeninas (-a) y neutras (-um).")
                with col3:
                    fem_override = st.text_input("Femenino (opcional)", help="Solo si es irregular")
                with col4:
                    neut_override = st.text_input("Neutro (opcional)", help="Solo si es irregular")
                
                if fem_override: irregular_json["nom_sg_f"] = fem_override
                if neut_override: irregular_json["nom_sg_n"] = neut_override
                
            elif "3 terminaciones" in adj_class:
                declension_val = "3"
                category_val = "adj_3_3term"
                with col3:
                    fem_form = st.text_input("Femenino *", help="Ej: acris")
                with col4:
                    neut_form = st.text_input("Neutro *", help="Ej: acre")
                
                if fem_form: irregular_json["nom_sg_f"] = fem_form
                if neut_form: irregular_json["nom_sg_n"] = neut_form
                
            elif "2 terminaciones" in adj_class:
                declension_val = "3"
                category_val = "adj_3_2term"
                with col3:
                    neut_form = st.text_input("Neutro *", help="Ej: forte")
                
                if neut_form: irregular_json["nom_sg_n"] = neut_form
                # Fem is same as Masc
                
            elif "1 terminación" in adj_class:
                declension_val = "3"
                category_val = "adj_3_1term"
                with col3:
                    genitive_val = st.text_input("Genitivo *", help="Ej: audacis")
            
            st.markdown("---")
            submitted = st.form_submit_button("✅ Guardar Adjetivo", type="primary")
            
            if submitted:
                valid = True
                if not latin or not translation:
                    st.error("Faltan campos obligatorios (Latín, Traducción).")
                    valid = False
                
                if "3 terminaciones" in adj_class and (not fem_form or not neut_form):
                    st.error("Para adjetivos de 3 terminaciones, debes indicar las formas Femenina y Neutra.")
                    valid = False
                
                if "2 terminaciones" in adj_class and not neut_form:
                    st.error("Para adjetivos de 2 terminaciones, debes indicar la forma Neutra.")
                    valid = False
                    
                if "1 terminación" in adj_class and not genitive_val:
                    st.error("Para adjetivos de 1 terminación, debes indicar el Genitivo.")
                    valid = False
                
                if valid:
                    with get_session() as session:
                        # Prepare JSON string if not empty
                        irr_str = json.dumps(irregular_json) if irregular_json else None
                        
                        word = Word(
                            latin=latin, 
                            translation=translation, 
                            part_of_speech="adjective", 
                            level=level,
                            declension=declension_val,
                            category=category_val,
                            genitive=genitive_val,
                            irregular_forms=irr_str
                        )
                        session.add(word)
                        session.commit()
                        st.success(f"Adjetivo '{latin}' añadido exitosamente.")

    # --- Tab: Others ---
    with vocab_tabs[3]:
        st.markdown("### Añadir Otra Palabra")
        with st.form("add_other"):
            col1, col2 = st.columns(2)
            with col1:
                latin = st.text_input("Palabra (Latín) *")
                translation = st.text_input("Traducción *")
                level = st.number_input("Nivel", min_value=1, max_value=10, value=1, key="other_level")
            
            with col2:
                pos_options = {
                    "Adverbio": "adverb", 
                    "Preposición": "preposition", "Conjunción": "conjunction", 
                    "Pronombre": "pronoun"
                }
                pos_display = st.selectbox("Tipo *", list(pos_options.keys()))
                pos = pos_options[pos_display]
                
                is_invariable = st.checkbox("Es invariable", value=(pos in ["adverb", "preposition", "conjunction"]))
            
            submitted = st.form_submit_button("✅ Guardar Palabra", type="primary")
            
            if submitted:
                if latin and translation:
                    with get_session() as session:
                        word = Word(
                            latin=latin, translation=translation, part_of_speech=pos, level=level,
                            is_invariable=is_invariable, category=pos
                        )
                        session.add(word)
                        session.commit()
                        st.success(f"Palabra '{latin}' añadida.")
                else:
                    st.error("Faltan campos obligatorios.")
    
    # --- Tab: Import ---
    with vocab_tabs[4]:
        st.markdown("### 📥 Importar Vocabulario desde CSV/Excel")
        
        # Import CSV handler
        from utils.csv_handler import VocabularyImporter, TemplateGenerator
        
        st.info("📝 Importa múltiples palabras a la vez usando archivos CSV o Excel.")
        
        # Word type selector
        import_type = st.selectbox(
            "Tipo de palabras a importar",
            ["Sustantivos", "Verbos", "Otras Palabras"],
            key="import_type_selector"
        )
        
        type_map = {
            "Sustantivos": "noun",
            "Verbos": "verb",
            "Otras Palabras": "other"
        }
        word_type = type_map[import_type]
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Selecciona archivo CSV o Excel",
            type=['csv', 'xlsx', 'xls'],
            help="El archivo debe contener las columnas requeridas según el tipo de palabra"
        )
        
        if uploaded_file is not None:
            try:
                # Parse file
                file_bytes = uploaded_file.read()
                df = VocabularyImporter.parse_file(file_bytes, uploaded_file.name)
                
                st.success(f"✅ Archivo leído: {len(df)} filas encontradas")
                
                # Validate
                is_valid, errors = VocabularyImporter.validate_dataframe(df, word_type)
                
                if not is_valid:
                    st.error("❌ Errores de validación:")
                    for error in errors:
                        st.error(f"  • {error}")
                else:
                    st.success("✅ Validación de estructura exitosa")
                    
                    # --- PRE-IMPORT ANALYSIS ---
                    st.markdown("### 🔍 Análisis Previo")
                    
                    with get_session() as session:
                        # Fetch existing words for comparison
                        existing_words = session.exec(select(Word.latin)).all()
                        existing_set = {normalize_latin(w.lower()) for w in existing_words}
                    
                    # Analyze duplicates
                    df['normalized_latin'] = df['latin'].apply(lambda x: normalize_latin(str(x).lower()))
                    df['status'] = df['normalized_latin'].apply(
                        lambda x: 'Duplicado' if x in existing_set else 'Nuevo'
                    )
                    
                    new_count = len(df[df['status'] == 'Nuevo'])
                    dup_count = len(df[df['status'] == 'Duplicado'])
                    
                    col1, col2 = st.columns(2)
                    col1.metric("Palabras Nuevas", new_count)
                    col2.metric("Duplicados", dup_count)
                    
                    # --- FILTERING UI ---
                    st.markdown("#### Filtrar y Seleccionar")
                    
                    filter_option = st.radio(
                        "Mostrar:",
                        ["Todo", "Solo Nuevas", "Solo Duplicados"],
                        horizontal=True
                    )
                    
                    # Apply filter
                    if filter_option == "Solo Nuevas":
                        filtered_df = df[df['status'] == 'Nuevo'].copy()
                    elif filter_option == "Solo Duplicados":
                        filtered_df = df[df['status'] == 'Duplicado'].copy()
                    else:
                        filtered_df = df.copy()
                    
                    # Add 'Importar' checkbox column
                    if 'Importar' not in filtered_df.columns:
                        filtered_df.insert(0, 'Importar', True)
                        # Default uncheck duplicates if showing all
                        if filter_option == "Todo":
                            filtered_df.loc[filtered_df['status'] == 'Duplicado', 'Importar'] = False
                    
                    # Show interactive editor
                    edited_df = st.data_editor(
                        filtered_df,
                        column_config={
                            "Importar": st.column_config.CheckboxColumn(
                                "Importar",
                                help="Selecciona para importar",
                                default=True,
                            ),
                            "status": st.column_config.TextColumn(
                                "Estado",
                                help="Nuevo o Duplicado",
                                width="medium",
                            ),
                        },
                        disabled=["latin", "translation", "status"],
                        hide_index=True,
                        width='stretch'
                    )
                    
                    # Count selected
                    to_import_count = len(edited_df[edited_df['Importar'] == True])
                    
                    st.info(f"Se importarán **{to_import_count}** palabras.")
                    
                    # Import button
                    if st.button("💾 Importar Selección", type="primary", width='stretch', disabled=to_import_count==0):
                        try:
                            # Filter only selected rows
                            final_df = edited_df[edited_df['Importar'] == True].drop(columns=['Importar', 'status', 'normalized_latin'])
                            
                            if len(final_df) > 0:
                                words = VocabularyImporter.dataframe_to_words(final_df, word_type)
                                
                                with get_session() as session:
                                    for word in words:
                                        session.add(word)
                                    session.commit()
                                
                                st.success(f"🎉 {len(words)} palabras importadas exitosamente!")
                                st.balloons()
                            else:
                                st.warning("No hay palabras seleccionadas para importar.")
                                
                        except Exception as e:
                            st.error(f"Error al importar: {str(e)}")
            
            except Exception as e:
                st.error(f"Error al procesar archivo: {str(e)}")
    
    # --- Tab: Export ---
    with vocab_tabs[5]:
        st.markdown("### 📤 Exportar Vocabulario")
        
        from utils.csv_handler import VocabularyExporter
        
        st.info("💾 Descarga el vocabulario actual en formato CSV o Excel para backup o edición externa.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            export_type = st.selectbox(
                "Tipo de palabras",
                ["Todas", "Sustantivos", "Verbos", "Adjetivos", "Adverbios", "Otros"],
                key="export_type"
            )
        
        with col2:
            export_format = st.selectbox(
                "Formato",
                ["CSV", "Excel"],
                key="export_format"
            )
        
        # Level filter
        min_level = st.slider("Nivel mínimo", 1, 10, 1, key="export_min_level")
        max_level = st.slider("Nivel máximo", 1, 10, 10, key="export_max_level")
        
        if st.button("📥 Generar Archivo", width='stretch', type="primary"):
            with get_session() as session:
                query = select(Word)
                
                # Apply filters
                if export_type == "Sustantivos":
                    query = query.where(Word.part_of_speech == "noun")
                    file_type = "noun"
                elif export_type == "Verbos":
                    query = query.where(Word.part_of_speech == "verb")
                    file_type = "verb"
                elif export_type == "Adjetivos":
                    query = query.where(Word.part_of_speech == "adjective")
                    file_type = "other"
                elif export_type == "Adverbios":
                    query = query.where(Word.part_of_speech == "adverb")
                    file_type = "other"
                elif export_type == "Otros":
                    query = query.where(Word.part_of_speech.not_in(["noun", "verb"]))
                    file_type = "other"
                else:
                    file_type = "all"
                
                query = query.where(Word.level >= min_level, Word.level <= max_level)
                words = session.exec(query).all()
                
                if len(words) == 0:
                    st.warning("No hay palabras que coincidan con los filtros seleccionados.")
                else:
                    # Convert to DataFrame
                    if file_type == "all":
                        # Mixed export
                        data = []
                        for w in words:
                            row = {
                                'latin': w.latin,
                                'translation': w.translation,
                                'part_of_speech': w.part_of_speech,
                                'level': w.level
                            }
                            data.append(row)
                        df = pd.DataFrame(data)
                    else:
                        df = VocabularyExporter.words_to_dataframe(words, "noun" if file_type == "noun" else "verb" if file_type == "verb" else "other")
                    
                    # Generate file
                    if export_format == "CSV":
                        file_bytes = VocabularyExporter.to_csv(df)
                        mime_type = "text/csv"
                        file_ext = "csv"
                    else:
                        file_bytes = VocabularyExporter.to_excel(df)
                        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        file_ext = "xlsx"
                    
                    filename = f"vocabulario_{export_type.lower()}_{min_level}-{max_level}.{file_ext}"
                    
                    st.download_button(
                        label=f"⬇️ Descargar {filename}",
                        data=file_bytes,
                        file_name=filename,
                        mime=mime_type,
                        width='stretch'
                    )
                    
                    st.success(f"✅ {len(words)} palabras listas para descargar")

    # --- Tab: List ---
    with vocab_tabs[6]:
        st.markdown("### Lista de Vocabulario")
        with get_session() as session:
            words = session.exec(select(Word)).all()
            if words:
                # Filter
                filter_text = st.text_input("🔍 Buscar palabra", "")
                filtered_words = [w for w in words if filter_text.lower() in w.latin.lower() or filter_text.lower() in w.translation.lower()] if filter_text else words
                
                data = []
                for w in filtered_words:
                    data.append({
                        "ID": w.id,
                        "Latín": w.latin,
                        "Traducción": w.translation,
                        "Tipo": w.part_of_speech,
                        "Nivel": w.level
                    })
                st.dataframe(
                    data, 
                    column_config={
                        "id": None,
                        "author_id": None,
                        "irregular_forms": st.column_config.TextColumn("Irregular", help="Formas irregulares JSON"),
                    },
                    width='stretch'
                )
            else:
                st.info("No hay palabras.")
    
    # --- Tab: Help ---
    with vocab_tabs[7]:
        st.markdown("### ❓ Ayuda y Tutoriales")
        
        help_sections = st.tabs(["📖 Manual de Entrada", "📝 Formato JSON", "📥 Importar CSV/Excel", "📦 Descargar Plantillas"])
        
        # Manual Entry Tutorial
        with help_sections[0]:
            st.markdown("#### Cómo añadir palabras manualmente")
            
            with st.expander("🔸 Sustantivos", expanded=True):
                st.markdown("""
                Los sustantivos requieren:
                - **Nominativo Singular**: La forma del diccionario (ej: `puella`)
                - **Genitivo Singular**: Para determinar la declinación (ej: `puellae`)
                - **Género**: `m` (masculino), `f` (femenino), o `n` (neutro)
                - **Declinación**: `1`, `2`, `3`, `4`, o `5`
                - **Traducción**: Significado en español
                - **Nivel**: 1-10 (dificultad sugerida)
                
                **Formas Irregulares** (opcional): JSON con formas especiales
                ```json
                {"dat_pl": "filiābus", "abl_pl": "filiābus"}
                ```
                """)
            
            with st.expander("🔸 Verbos"):
                st.markdown("""
                Los verbos requieren:
                - **1ª Persona Presente**: Forma del diccionario (ej: `amo`)
                - **Partes Principales**: Todas las formas principales separadas por comas
                  - Ejemplo: `amo, amāre, amāvī, amātum`
                - **Conjugación**: `1`, `2`, `3`, `4`, o `irregular`
                - **Traducción**: Significado (ej: "amar")
                - **Nivel**: 1-10
                
                **Formas Irregulares** (opcional): Para verbos como `sum`
                ```json
                {"pres_1sg": "sum", "pres_2sg": "es"}
                ```
                """)
            
            with st.expander("🔸 Otras Palabras"):
                st.markdown("""
                Adjetivos, adverbios, preposiciones, conjunciones:
                - **Palabra**: La forma en latín
                - **Tipo**: Selecciona del menú desplegable
                - **Traducción**: Significado en español
                - **Es invariable**: Marca si la palabra no cambia (adverbios, preposiciones, etc.)
                """)
        
        # JSON Format Tutorial
        with help_sections[1]:
            st.markdown("#### 📝 Guía de Formato JSON para Irregularidades")
            
            st.info("El campo 'Formas Irregulares' permite especificar formas que no siguen las reglas estándar de declinación o conjugación.")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### 🔸 Sustantivos")
                st.markdown("Usa las siguientes claves para definir casos específicos:")
                st.markdown("""
                | Clave | Significado |
                |---|---|
                | `nom_sg` / `nom_pl` | Nominativo |
                | `gen_sg` / `gen_pl` | Genitivo |
                | `dat_sg` / `dat_pl` | Dativo |
                | `acc_sg` / `acc_pl` | Acusativo |
                | `abl_sg` / `abl_pl` | Ablativo |
                | `voc_sg` / `voc_pl` | Vocativo |
                """)
                
                st.markdown("**Ejemplo (Dea - Dat/Abl Plural irregular):**")
                st.code('{"dat_pl": "deābus", "abl_pl": "deābus"}', language="json")
            
            with col2:
                st.markdown("##### 🔹 Verbos")
                st.markdown("Claves para tiempos y personas (pres/imp/fut/perf/pqp/futp):")
                st.markdown("""
                | Clave | Significado |
                |---|---|
                | `pres_1sg` | Presente 1ª Sing |
                | `imp_3pl` | Imperfecto 3ª Pl |
                | `perf_1sg` | Perfecto 1ª Sing |
                | `inf_pres` | Infinitivo Presente |
                | `imp_2sg` | Imperativo 2ª Sing |
                """)
                
                st.markdown("**Ejemplo (Sum - Presente irregular):**")
                st.code("""
{
  "pres_1sg": "sum",
  "pres_2sg": "es",
  "pres_3sg": "est",
  "pres_1pl": "sumus",
  "pres_2pl": "estis",
  "pres_3pl": "sunt"
}
""", language="json")

        # CSV/Excel Import Tutorial
        with help_sections[2]:
            st.markdown("#### Cómo importar vocabulario desde archivos")
            
            st.info("📋 La importación masiva te permite cargar cientos de palabras en segundos.")
            
            st.markdown("""
            **Pasos:**
            1. Descarga una plantilla desde la pestaña "Descargar Plantillas"
            2. Completa el archivo con tus palabras (puedes usar Excel, Google Sheets, o cualquier editor CSV)
            3. Guarda como `.csv` o `.xlsx`
            4. Ve a la pestaña "📥 Importar"
            5. Selecciona el tipo de palabra
            6. Sube el archivo
            7. Revisa la vista previa y valida que no haya errores
            8. Haz clic en "Importar al Sistema"
            
            **Columnas Requeridas por Tipo:**
            
            **Sustantivos:**
            - `latin`, `translation`, `genitive`, `gender`, `declension`
            
            **Verbos:**
            - `latin`, `translation`, `principal_parts`, `conjugation`
            
            **Otras Palabras:**
            - `latin`, `translation`, `part_of_speech`
            
            **Columnas Opcionales:**
            - `level` (por defecto: 1)
            - `irregular_forms` (JSON string, por defecto: vacío)
            """)
            
            st.warning("⚠️ **Importante**: Las columnas deben tener exactamente los nombres indicados (en inglés, minúsculas).")
        
        # Template Downloads
        with help_sections[3]:
            st.markdown("#### Plantillas para Importación")
            
            from utils.csv_handler import TemplateGenerator, VocabularyExporter
            
            st.info("💡 Estas plantillas incluyen ejemplos. Puedes eliminar las filas de ejemplo y agregar tus propias palabras.")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("##### 📗 Sustantivos")
                noun_template = TemplateGenerator.generate_noun_template()
                
                csv_bytes = VocabularyExporter.to_csv(noun_template)
                st.download_button(
                    label="⬇️ CSV",
                    data=csv_bytes,
                    file_name="plantilla_sustantivos.csv",
                    mime="text/csv",
                    width='stretch'
                )
                
                excel_bytes = VocabularyExporter.to_excel(noun_template)
                st.download_button(
                    label="⬇️ Excel",
                    data=excel_bytes,
                    file_name="plantilla_sustantivos.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    width='stretch'
                )
            
            with col2:
                st.markdown("##### 📘 Verbos")
                verb_template = TemplateGenerator.generate_verb_template()
                
                csv_bytes = VocabularyExporter.to_csv(verb_template)
                st.download_button(
                    label="⬇️ CSV",
                    data=csv_bytes,
                    file_name="plantilla_verbos.csv",
                    mime="text/csv",
                    width='stretch'
                )
                
                excel_bytes = VocabularyExporter.to_excel(verb_template)
                st.download_button(
                    label="⬇️ Excel",
                    data=excel_bytes,
                    file_name="plantilla_verbos.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    width='stretch'
                )
            
            with col3:
                st.markdown("##### 📙 Otras Palabras")
                other_template = TemplateGenerator.generate_other_template()
                
                csv_bytes = VocabularyExporter.to_csv(other_template)
                st.download_button(
                    label="⬇️ CSV",
                    data=csv_bytes,
                    file_name="plantilla_otras.csv",
                    mime="text/csv",
                    width='stretch'
                )
                
                excel_bytes = VocabularyExporter.to_excel(other_template)
                st.download_button(
                    label="⬇️ Excel",
                    data=excel_bytes,
                    file_name="plantilla_otras.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    width='stretch'
                )
            
            st.markdown("---")
            st.success("✅ Descarga la plantilla que necesites, complétala, y súbela en la pestaña '📥 Importar'")


# --- SECTION: TEXTS ---
elif section == "Textos":
    st.markdown("## 📜 Gestión de Textos")
    
    text_tabs = st.tabs(["➕ Añadir Texto", "📚 Ver Textos", "📥 Importar", "📤 Exportar", "🛠️ Herramientas"])
    
    with text_tabs[0]:
        st.markdown("### Nuevo Texto")
        col1, col2 = st.columns([3, 1])
        
        with col1:
            title = st.text_input("Título")
            author = st.text_input("Autor")
            content = st.text_area("Contenido (Latín)", height=300)
        
        with col2:
            level = st.number_input("Nivel", 1, 10, 1)
            book = st.number_input("Libro (opcional)", 0, 100, 0, help="Número de libro (ej: 1)")
            chapter = st.number_input("Capítulo (opcional)", 0, 100, 0, help="Número de capítulo (ej: 5)")
            st.info("El sistema analizará el texto y vinculará el vocabulario automáticamente.")
        
        if st.button("💾 Guardar Texto", width='stretch', type="primary"):
            if title and content:
                with get_session() as session:
                    new_text = Text(
                        title=title, 
                        author=author, 
                        content=content, 
                        difficulty=level,
                        book_number=book if book > 0 else None,
                        chapter_number=chapter if chapter > 0 else None
                    )
                    session.add(new_text)
                    session.commit()
                    session.refresh(new_text)
                    
                    # Tokenize and Link
                    words_in_text = re.findall(r'[a-zA-ZāēīōūĀĒĪŌŪ]+', content.lower())
                    word_freq = {}
                    for w in words_in_text:
                        nw = normalize_latin(w)
                        word_freq[nw] = word_freq.get(nw, 0) + 1
                    
                    all_words = session.exec(select(Word)).all()
                    linked_count = 0
                    
                    for text_word, freq in word_freq.items():
                        for db_word in all_words:
                            if normalize_latin(db_word.latin.lower()) == text_word:
                                link = TextWordLink(text_id=new_text.id, word_id=db_word.id, frequency=freq)
                                session.add(link)
                                session.add(link)
                                linked_count += 1
                                break
                    session.commit()
                    st.success(f"Texto guardado. {linked_count} palabras vinculadas.")
            else:
                st.error("Título y contenido requeridos.")

    with text_tabs[1]:
        st.markdown("### Textos Existentes")
        with get_session() as session:
            texts = session.exec(select(Text)).all()
            for t in texts:
                with st.expander(f"{t.title} (Nivel {t.difficulty})"):
                    st.write(t.content[:200] + "...")
                    st.caption(f"Autor: {t.author if t.author else 'Desconocido'}")

    # --- Import Tab ---
    with text_tabs[2]:
        st.markdown("### 📥 Importar Textos")
        
        import_mode = st.radio("Método de Importación", ["Desde Archivo (CSV/Excel)", "Desde Texto con NLP (Inteligente)"], horizontal=True)
        
        if import_mode == "Desde Archivo (CSV/Excel)":
            st.info("Sube archivos CSV o Excel con tus textos. Columnas requeridas: title, content, difficulty.")
            
            from utils.content_import_export import ContentImporter, ContentTemplateGenerator
            
            # Download Template
            st.markdown("#### 1. Descargar Plantilla")
            col_t1, col_t2 = st.columns(2)
            template_df = ContentTemplateGenerator.generate_text_template()
            
            with col_t1:
                st.download_button(
                    "⬇️ Plantilla CSV",
                    data=template_df.to_csv(index=False).encode('utf-8'),
                    file_name="plantilla_textos.csv",
                    mime="text/csv",
                    width="stretch"
                )
            with col_t2:
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    template_df.to_excel(writer, index=False)
                st.download_button(
                    "⬇️ Plantilla Excel",
                    data=output.getvalue(),
                    file_name="plantilla_textos.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    width="stretch"
                )
                
            st.markdown("#### 2. Subir Archivo")
            uploaded_file = st.file_uploader("Seleccionar archivo", type=['csv', 'xlsx', 'xls'], key="text_uploader")
            
            if uploaded_file:
                try:
                    df = ContentImporter.parse_file(uploaded_file.getvalue(), uploaded_file.name)
                    is_valid, errors = ContentImporter.validate_dataframe(df, 'text')
                    
                    if is_valid:
                        st.success(f"✅ Archivo válido. {len(df)} textos encontrados.")
                        st.dataframe(df.head())
                        
                        if st.button("🚀 Importar Textos", type="primary"):
                            with get_session() as session:
                                texts = ContentImporter.dataframe_to_texts(df)
                                for t in texts:
                                    session.add(t)
                                session.commit()
                                st.success(f"✅ Se importaron {len(texts)} textos exitosamente.")
                                st.balloons()
                    else:
                        st.error("❌ El archivo tiene errores:")
                        for err in errors:
                            st.write(f"- {err}")
                            
                except Exception as e:
                    st.error(f"Error al procesar el archivo: {e}")
                    
        else:
            # NLP Smart Import
            st.info("🤖 **Importación Inteligente**: Pega cualquier texto en latín. El sistema analizará morfológicamente cada palabra, detectará lemas y generará todo el vocabulario necesario automáticamente.")
            
            with st.form("nlp_import_form"):
                col1, col2 = st.columns(2)
                with col1:
                    title = st.text_input("Título del Texto", placeholder="Ej: De Bello Gallico I.1")
                    author_name = st.text_input("Autor", placeholder="Ej: Caesar")
                with col2:
                    level = st.slider("Nivel de Dificultad", 1, 10, 1, key="nlp_level")
                
                content = st.text_area("Contenido (Latín)", height=300, placeholder="Gallia est omnis divisa in partes tres...")
                
                submitted = st.form_submit_button("🚀 Analizar e Importar", type="primary")
                
                if submitted and content and title:
                    with st.spinner("🧠 Analizando texto con Spacy NLP + Base de Datos..."):
                        try:
                            # Already imported at top as NLPContentImporter
                            importer = NLPContentImporter()
                            text_id = importer.import_text(title, content, level, author_name)
                            
                            st.success(f"✅ Texto '{title}' importado correctamente (ID: {text_id}).")
                            st.balloons()
                            
                            with get_session() as session:
                                link_count = len(session.exec(select(TextWordLink).where(TextWordLink.text_id == text_id)).all())
                                st.info(f"📊 Se han analizado y vinculado {link_count} palabras.")
                                
                        except Exception as e:
                            st.error(f"Error durante la importación: {e}")


    # --- Export Tab ---
    with text_tabs[3]:
        st.markdown("### 📤 Exportar Textos")
        from utils.content_import_export import ContentExporter
        
        if st.button("🔄 Generar Exportación"):
            with get_session() as session:
                texts = session.exec(select(Text)).all()
                if texts:
                    df = ContentExporter.texts_to_dataframe(texts)
                    
                    st.download_button(
                        "⬇️ Descargar CSV",
                        data=ContentExporter.to_csv(df),
                        file_name="textos_export.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("No hay textos para exportar.")

    with text_tabs[2]:
        st.markdown("### 🛠️ Herramientas de Análisis")
        
        st.info("Ejecuta el análisis morfológico profundo (Stanza) para todos los textos. Útil después de añadir textos o corregir vocabulario.")
        
        if st.button("🔄 Re-analizar Todos los Textos", type="primary"):
            try:
                from utils.stanza_analyzer import StanzaAnalyzer, analyze_and_save_text
                
                if not StanzaAnalyzer.is_available():
                    st.error("❌ Stanza no está disponible. Revisa la instalación.")
                else:
                    with get_session() as session:
                        texts = session.exec(select(Text)).all()
                        
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        total_analyzed = 0
                        total_saved = 0
                        errors = []
                        
                        for i, text in enumerate(texts):
                            status_text.text(f"Analizando: {text.title}...")
                            
                            try:
                                analyzed, saved = analyze_and_save_text(
                                    text.id,
                                    text.content,
                                    session
                                )
                                total_analyzed += analyzed
                                total_saved += saved
                            except Exception as e:
                                errors.append(f"{text.title}: {str(e)}")
                            
                            progress_bar.progress((i + 1) / len(texts))
                        
                        status_text.text("¡Análisis completado!")
                        st.success(f"✅ Procesados {len(texts)} textos. {total_analyzed} palabras analizadas.")
                        
                        if errors:
                            st.warning(f"⚠️ Hubo {len(errors)} errores:")
                            for err in errors:
                                st.write(f"- {err}")
                                
            except ImportError:
                st.error("❌ No se pudo importar el módulo de análisis. Verifica que stanza esté instalado.")
            except Exception as e:
                st.error(f"❌ Error inesperado: {str(e)}")

# --- SECTION: SYNTAX ---

elif section == "Lecciones":
    st.markdown("## 📚 Gestión de Lecciones")
    
    lesson_tabs = st.tabs(["➕ Añadir Lección", "📖 Ver Lecciones"])
    
    with lesson_tabs[0]:
        st.markdown("### Nueva Lección")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            lesson_number = st.number_input("Número de Lección", min_value=1, max_value=100, value=41, 
                                           help="Lecciones 1-13: Básico, 14-30: Avanzado, 31+: Experto")
            lesson_title = st.text_input("Título de la Lección", placeholder="Ej: Primeros Pasos")
            
            content_markdown = st.text_area("Contenido (Markdown)", height=400, 
                                           placeholder="## Lección X: Título\n\nContenido en formato Markdown...")
            
            image_path = st.text_input("Ruta de Imagen (opcional)", 
                                       placeholder="static/images/curso_gramatica/leccion41.png")
        
        with col2:
            # Auto-detect level based on lesson number
            if lesson_number <= 13:
                default_level = "basico"
            elif lesson_number <= 30:
                default_level = "avanzado"
            else:
                default_level = "experto"
            
            level = st.selectbox("Nivel", ["basico", "avanzado", "experto"], 
                                index=["basico", "avanzado", "experto"].index(default_level))
            
            order_in_level = st.number_input("Orden dentro del nivel", min_value=0, value=0,
                                             help="Para ordenamiento personalizado")
            
            is_published = st.checkbox("Publicada", value=True, 
                                       help="Si está desmarcada, la lección no será visible")
            
            st.info("💡 **Tip:** Usa Markdown para formato.\nEjemplos:\n- `## Título`\n- `**negrita**`\n- `*cursiva*`")
        
        if st.button("💾 Guardar Lección", type="primary", width="stretch"):
            if not lesson_title or not content_markdown:
                st.error("⚠️ Título y contenido son obligatorios")
            else:
                try:
                    with get_session() as session:
                        # Check if lesson number already exists
                        existing = session.exec(
                            select(Lesson).where(Lesson.lesson_number == lesson_number)
                        ).first()
                        
                        if existing:
                            st.error(f"❌ Ya existe una lección con el número {lesson_number}")
                        else:
                            new_lesson = Lesson(
                                lesson_number=lesson_number,
                                title=lesson_title,
                                level=level,
                                content_markdown=content_markdown,
                                image_path=image_path if image_path else None,
                                is_published=is_published,
                                order_in_level=order_in_level
                            )
                            session.add(new_lesson)
                            session.commit()
                            st.success(f"✅ Lección {lesson_number}: {lesson_title} guardada correctamente")
                            st.balloons()
                except Exception as e:
                    st.error(f"❌ Error al guardar: {str(e)}")
    
    with lesson_tabs[1]:
        st.markdown("### Lecciones Existentes")
        
        with get_session() as session:
            lessons = session.exec(
                select(Lesson).order_by(Lesson.lesson_number)
            ).all()
            
            if not lessons:
                st.info("📭 No hay lecciones en la base de datos aún. Crea la primera usando la pestaña anterior.")
            else:
                st.markdown(f"**Total de lecciones:** {len(lessons)}")
                
                # Create DataFrame for display
                lesson_data = []
                for lesson in lessons:
                    lesson_data.append({
                        "Nº": lesson.lesson_number,
                        "Título": lesson.title,
                        "Nivel": lesson.level.upper(),
                        "Publicada": "✅" if lesson.is_published else "❌",
                        "Creada": lesson.created_at.strftime("%Y-%m-%d") if lesson.created_at else "N/A"
                    })
                
                df = pd.DataFrame(lesson_data)
                st.dataframe(df, width="stretch", hide_index=True)
                
                st.markdown("---")
                st.markdown("### Editar / Eliminar Lección")
                
                selected_lesson_num = st.selectbox(
                    "Seleccionar lección",
                    [l.lesson_number for l in lessons],
                    format_func=lambda x: f"Lección {x}: {next(l.title for l in lessons if l.lesson_number == x)}"
                )
                
                selected_lesson = next((l for l in lessons if l.lesson_number == selected_lesson_num), None)
                
                if selected_lesson:
                    edit_col, delete_col = st.columns([3, 1])
                    
                    with edit_col:
                        with st.expander("✏️ Editar Lección", expanded=False):
                            edit_title = st.text_input("Título", value=selected_lesson.title, key="edit_title")
                            edit_level = st.selectbox("Nivel", ["basico", "avanzado", "experto"], 
                                                     index=["basico", "avanzado", "experto"].index(selected_lesson.level),
                                                     key="edit_level")
                            edit_content = st.text_area("Contenido", value=selected_lesson.content_markdown, 
                                                       height=300, key="edit_content")
                            edit_image = st.text_input("Ruta de Imagen", value=selected_lesson.image_path or "", 
                                                      key="edit_image")
                            edit_published = st.checkbox("Publicada", value=selected_lesson.is_published, 
                                                        key="edit_published")
                            
                            if st.button("💾 Guardar Cambios", type="primary", key="save_edit"):
                                try:
                                    with get_session() as session:
                                        lesson_to_update = session.get(Lesson, selected_lesson.id)
                                        lesson_to_update.title = edit_title
                                        lesson_to_update.level = edit_level
                                        lesson_to_update.content_markdown = edit_content
                                        lesson_to_update.image_path = edit_image if edit_image else None
                                        lesson_to_update.is_published = edit_published
                                        from datetime import datetime
                                        lesson_to_update.updated_at = datetime.utcnow()
                                        session.commit()
                                        st.success("✅ Lección actualizada correctamente")
                                        st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Error al actualizar: {str(e)}")
                    
                    with delete_col:
                        with st.expander("🗑️ Eliminar", expanded=False):
                            st.warning(f"⚠️ **Peligro:** Eliminar Lección {selected_lesson.lesson_number}")
                            confirm_delete = st.text_input(
                                "Escribe el número de lección para confirmar",
                                key="confirm_delete"
                            )
                            
                            if st.button("🗑️ ELIMINAR", type="secondary", key="delete_btn"):
                                if confirm_delete == str(selected_lesson.lesson_number):
                                    try:
                                        with get_session() as session:
                                            lesson_to_delete = session.get(Lesson, selected_lesson.id)
                                            session.delete(lesson_to_delete)
                                            session.commit()
                                            st.success("✅ Lección eliminada")
                                            st.rerun()
                                    except Exception as e:
                                        st.error(f"❌ Error: {str(e)}")
                                else:
                                    st.error("❌ Número incorrecto. No se eliminó la lección.")


# --- SECTION: EXERCISES ---
elif section == "Ejercicios":
    st.markdown("## 🏋️ Gestión de Ejercicios Estáticos")
    
    st.info("Sube archivos JSON para definir los ejercicios estáticos de cada lección.")
    
    st.markdown("### 📤 Cargar Archivo JSON")
    uploaded_file = st.file_uploader("Seleccionar archivo JSON", type=['json'], key="exercise_uploader")
    
    if uploaded_file:
        try:
            content = json.load(uploaded_file)
            
            # Validation
            required_keys = ["lesson", "topic", "exercises"]
            missing = [k for k in required_keys if k not in content]
            
            if missing:
                st.error(f"❌ JSON inválido. Faltan claves: {', '.join(missing)}")
            else:
                st.success(f"✅ JSON válido. Lección: {content['lesson']} - Título: {content['topic']}")
                st.write(f"Contiene {len(content['exercises'])} ejercicios.")
                
                if st.button("💾 Guardar en Sistema", type="primary"):
                    # Save to data/static_exercises/
                    target_dir = os.path.join(root_path, "data", "static_exercises")
                    os.makedirs(target_dir, exist_ok=True)
                    
                    filename = f"exercises_l{content['lesson']}.json"
                    target_path = os.path.join(target_dir, filename)
                    
                    with open(target_path, "w", encoding="utf-8") as f:
                        json.dump(content, f, indent=4, ensure_ascii=False)
                    
                    st.success(f"✅ Archivo guardado como: {filename}")
                    st.balloons()
        except json.JSONDecodeError:
            st.error("❌ El archivo no es un JSON válido")
                    
    st.markdown("---")
    st.markdown("### 📂 Archivos Existentes")
    
    exercises_dir = os.path.join(root_path, "data", "static_exercises")
    if os.path.exists(exercises_dir):
        files = sorted([f for f in os.listdir(exercises_dir) if f.endswith(".json")])
        if files:
            for f in files:
                st.text(f"📄 {f}")
        else:
            st.info("No hay archivos de ejercicios.")

elif section == "Sintaxis":
    st.markdown("## 📐 Gestión de Sintaxis")
    
    syntax_tabs = st.tabs(["➕ Nueva Oración", "📚 Ver Oraciones", "📥 Importar", "📤 Exportar", "❓ Ayuda"])
    
    # ... (New Sentence logic remains same) ...
    # ... (View Sentences logic remains same) ...

    # --- Import Tab (Syntax) ---
    with syntax_tabs[2]:
        st.markdown("### 📥 Importar Oraciones")
        st.info("Importa oraciones masivamente para análisis posterior. Columnas: latin_text, spanish_translation, complexity.")
        
        from utils.content_import_export import ContentImporter, ContentTemplateGenerator
        
        # Download Template
        st.markdown("#### 1. Descargar Plantilla")
        col_t1, col_t2 = st.columns(2)
        template_df = ContentTemplateGenerator.generate_syntax_template()
        
        with col_t1:
            st.download_button(
                "⬇️ Plantilla CSV",
                data=template_df.to_csv(index=False).encode('utf-8'),
                file_name="plantilla_sintaxis.csv",
                mime="text/csv",
                width="stretch",
                key="syntax_csv_dl"
            )
        with col_t2:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                template_df.to_excel(writer, index=False)
            st.download_button(
                "⬇️ Plantilla Excel",
                data=output.getvalue(),
                file_name="plantilla_sintaxis.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                width="stretch",
                key="syntax_excel_dl"
            )
            
        st.markdown("#### 2. Subir Archivo")
        uploaded_file = st.file_uploader("Seleccionar archivo", type=['csv', 'xlsx', 'xls'], key="syntax_uploader")
        
        if uploaded_file:
            try:
                df = ContentImporter.parse_file(uploaded_file.getvalue(), uploaded_file.name)
                is_valid, errors = ContentImporter.validate_dataframe(df, 'syntax')
                
                if is_valid:
                    st.success(f"✅ Archivo válido. {len(df)} oraciones encontradas.")
                    st.dataframe(df.head())
                    
                    if st.button("🚀 Importar Oraciones", type="primary"):
                        with get_session() as session:
                            sentences = ContentImporter.dataframe_to_sentences(df)
                            for s in sentences:
                                session.add(s)
                            session.commit()
                            st.success(f"✅ Se importaron {len(sentences)} oraciones. Aparecerán en la 'Zona de Espera' análisis.")
                else:
                    st.error("❌ El archivo tiene errores:")
                    for e in errors:
                        st.write(f"- {e}")
            except Exception as e:
                st.error(f"Error al procesar: {e}")

    # --- Export Tab (Syntax) ---
    with syntax_tabs[3]:
        st.markdown("### 📤 Exportar Oraciones")
        from utils.content_import_export import ContentExporter
        
        if st.button("🔄 Generar Exportación", key="export_syntax_btn"):
            with get_session() as session:
                sentences = session.exec(select(SentenceAnalysis)).all()
                if sentences:
                    df = ContentExporter.sentences_to_dataframe(sentences)
                    
                    st.download_button(
                        "⬇️ Descargar CSV",
                        data=ContentExporter.to_csv(df),
                        file_name="sintaxis_export.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("No hay oraciones para exportar.")
        st.markdown("### Añadir Nueva Oración")
        
        # Session state for analysis workflow
        if 'syntax_analysis_result' not in st.session_state:
            st.session_state.syntax_analysis_result = None
        if 'syntax_form_data' not in st.session_state:
            st.session_state.syntax_form_data = {}
            
        with st.form("analyze_sentence_form"):
            col1, col2 = st.columns([3, 1])
            with col1:
                latin_text = st.text_input("Oración en Latín *", help="Ej: Puella rosam videt.")
                spanish_translation = st.text_input("Traducción *", help="Ej: La niña ve la rosa.")
            with col2:
                complexity = st.number_input("Nivel de Complejidad", 1, 10, 1)
                source = st.text_input("Fuente (opcional)", help="Ej: familia_romana_cap1")
            
            analyze_btn = st.form_submit_button("🔍 Analizar con Stanza", type="primary")
            
            if analyze_btn and latin_text and spanish_translation:
                try:
                    from utils.stanza_analyzer import StanzaAnalyzer
                    
                    if not StanzaAnalyzer.is_available():
                        st.error("❌ Stanza no está disponible. Revisa la instalación.")
                    else:
                        analyzer = StanzaAnalyzer()
                        # Analyze text
                        analysis = analyzer.analyze_text(latin_text)
                        
                        # Store in session state
                        st.session_state.syntax_analysis_result = analysis
                        st.session_state.syntax_form_data = {
                            "latin_text": latin_text,
                            "spanish_translation": spanish_translation,
                            "complexity": complexity,
                            "source": source
                        }
                        st.success("✅ Análisis completado. Revisa y edita los detalles abajo.")
                        
                except Exception as e:
                    st.error(f"Error al analizar: {e}")

        # --- EDITOR UI ---
        if st.session_state.syntax_analysis_result:
            st.markdown("---")
            st.markdown("#### 📝 Editor de Anotaciones")
            
            analysis = st.session_state.syntax_analysis_result
            form_data = st.session_state.syntax_form_data
            
            # Prepare data for editor
            editor_data = []
            for token in analysis:
                editor_data.append({
                    "ID": token['position'] + 1,
                    "Palabra": token['form'],
                    "Lema": token['lemma'],
                    "POS": token['pos'].upper(),
                    "Dep": token['deprel'],
                    "Head": token['head'],
                    "Rol Pedagógico": "", # User to fill
                    "Función Caso": "", # User to fill
                    "Explicación": "" # User to fill
                })
            
            df_editor = pd.DataFrame(editor_data)
            
            edited_df = st.data_editor(
                df_editor,
                column_config={
                    "ID": st.column_config.NumberColumn("ID", disabled=True, width="small"),
                    "Palabra": st.column_config.TextColumn("Palabra", disabled=True),
                    "Lema": st.column_config.TextColumn("Lema", disabled=True),
                    "POS": st.column_config.TextColumn("POS", disabled=True),
                    "Dep": st.column_config.TextColumn("Dep", disabled=True, width="small"),
                    "Head": st.column_config.NumberColumn("Head", disabled=True, width="small"),
                    "Rol Pedagógico": st.column_config.SelectboxColumn(
                        "Rol Pedagógico",
                        options=[
                            "Sujeto", "Predicado", "Objeto Directo", "Objeto Indirecto", 
                            "Complemento Circunstancial", "Atributo", "Aposición", 
                            "Modificador", "Determinante", "Conjunción", "Puntuación"
                        ],
                        required=False,
                        width="medium"
                    ),
                    "Función Caso": st.column_config.TextColumn(
                        "Función (Opcional)",
                        help="Ej: Ablativo Instrumental",
                        width="medium"
                    ),
                    "Explicación": st.column_config.TextColumn(
                        "Explicación (Opcional)",
                        width="large"
                    )
                },
                hide_index=True,
                num_rows="fixed",
                width="stretch",
                key="syntax_editor_table"
            )
            
            st.markdown("#### Estructura General")
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                sentence_type = st.selectbox("Tipo de Oración", ["simple", "compound", "complex"], index=0)
            with col_s2:
                constructions = st.multiselect(
                    "Construcciones Especiales", 
                    ["ablative_absolute", "accusative_infinitive", "dative_possession", "passive_voice"]
                )
            
            notes = st.text_area("Notas Generales / Estructura", help="Ej: Oración simple transitiva con orden SOV.")
            
            if st.button("💾 Guardar Oración en Base de Datos", type="primary"):
                try:
                    with get_session() as session:
                        # 1. Create SentenceAnalysis
                        # Construct dependency_json
                        dep_json = []
                        for index, row in edited_df.iterrows():
                            # Reconstruct morphology string from analysis result (it's complex to reconstruct exactly, 
                            # but we can try to use what we have or just store what Stanza gave us initially)
                            # Better: use the original analysis for technical fields and edited_df for annotations
                            
                            orig_token = analysis[index]
                            
                            # Reconstruct morph string like "Case=Nom|Gender=Fem"
                            morph_dict = orig_token['morphology']
                            morph_str = "|".join([f"{k.title()}={v.title()}" for k, v in morph_dict.items()])
                            
                            dep_json.append({
                                "id": row['ID'],
                                "text": row['Palabra'],
                                "lemma": row['Lema'],
                                "pos": row['POS'],
                                "dep": row['Dep'],
                                "head": row['Head'],
                                "morph": morph_str
                            })
                            
                        # Construct syntax_roles
                        # {"subject": [1], "direct_object": [2]}
                        roles_map = {}
                        role_translation_rev = {
                            "Sujeto": "subject", "Predicado": "predicate", 
                            "Objeto Directo": "direct_object", "Objeto Indirecto": "indirect_object",
                            "Complemento Circunstancial": "complement", "Atributo": "attribute",
                            "Aposición": "apposition", "Modificador": "modifier",
                            "Determinante": "determiner", "Conjunción": "conjunction"
                        }
                        
                        for index, row in edited_df.iterrows():
                            role_es = row['Rol Pedagógico']
                            if role_es and role_es in role_translation_rev:
                                role_key = role_translation_rev[role_es]
                                if role_key not in roles_map:
                                    roles_map[role_key] = []
                                roles_map[role_key].append(int(row['ID']))
                        
                        new_sentence = SentenceAnalysis(
                            latin_text=form_data['latin_text'],
                            spanish_translation=form_data['spanish_translation'],
                            complexity_level=form_data['complexity'],
                            sentence_type=sentence_type,
                            source=form_data['source'],
                            dependency_json=json.dumps(dep_json),
                            syntax_roles=json.dumps(roles_map),
                            constructions=json.dumps(constructions) if constructions else None
                        )
                        session.add(new_sentence)
                        session.commit()
                        session.refresh(new_sentence)
                        
                        # 2. Create TokenAnnotations
                        for index, row in edited_df.iterrows():
                            if row['Rol Pedagógico'] or row['Función Caso'] or row['Explicación']:
                                ann = TokenAnnotation(
                                    sentence_id=new_sentence.id,
                                    token_index=index, # 0-based index
                                    token_text=row['Palabra'],
                                    pedagogical_role=row['Rol Pedagógico'] or "Sin rol",
                                    case_function=row['Función Caso'],
                                    explanation=row['Explicación']
                                )
                                session.add(ann)
                        
                        # 3. Create SentenceStructure
                        if notes:
                            struct = SentenceStructure(
                                sentence_id=new_sentence.id,
                                clause_type="Principal", # Default
                                notes=notes
                            )
                            session.add(struct)
                        
                        session.commit()
                        st.success("✅ Oración guardada exitosamente!")
                        # Clear state
                        st.session_state.syntax_analysis_result = None
                        st.session_state.syntax_form_data = {}
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"Error al guardar: {e}")

    # --- Tab: View Sentences ---
    with syntax_tabs[1]:
        st.markdown("### Oraciones Existentes")
        with get_session() as session:
            sentences = session.exec(select(SentenceAnalysis)).all()
            if sentences:
                for s in sentences:
                    with st.expander(f"{s.latin_text} (Nivel {s.complexity_level})"):
                        st.write(f"**Traducción:** {s.spanish_translation}")
                        st.caption(f"Fuente: {s.source}")
                        if st.button("🗑️ Eliminar", key=f"del_sent_{s.id}"):
                            session.delete(s)
                            session.commit()
                            st.rerun()
            else:
                st.info("No hay oraciones registradas.")

    # --- Tab: Help ---
    with syntax_tabs[2]:
        st.markdown("### ❓ Ayuda Sintaxis")
        st.write("Instrucciones para añadir oraciones...")

# --- SECTION: USUARIO ---
elif section == "Usuario":
    st.markdown("## 👤 Gestión de Usuario")
    
    user_tabs = st.tabs(["📊 Progreso Actual", "🔄 Resetear Progreso", "⚙️ Configuración"])
    
    # --- Tab: Current Progress ---
    with user_tabs[0]:
        st.markdown("### Estado del Progreso")
        
        with get_session() as session:
            # Get all progress-related data
            user = session.exec(select(UserProfile)).first()
            
            if user:
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Nivel", user.level)
                col2.metric("XP Total", user.xp)
                col3.metric("Estrellas", user.total_stars)
                col4.metric("Racha", user.streak)
                
                st.markdown("---")
                
                col5, col6, col7 = st.columns(3)
                col5.metric("Desafíos Completados", user.challenges_completed)
                col6.metric("Desafíos Perfectos", user.perfect_challenges)
                col7.metric("Último Login", user.last_login.strftime("%Y-%m-%d %H:%M"))
                
                # Progress tables
                from database import LessonProgress, UserVocabularyProgress, ExerciseAttempt
                
                st.markdown("---")
                st.markdown("#### Detalles de Progreso por Sistema")
                
                prog_tabs = st.tabs(["📚 Lecciones", "📖 Vocabulario", "✏️ Ejercicios"])
                
                with prog_tabs[0]:
                    lessons = session.exec(select(LessonProgress)).all()
                    if lessons:
                        data = [{
                            "Lección": l.lesson_number,
                            "Completado": "✅" if l.status == 'completed' else "🚧",
                            "Progreso %": 0 # Placeholder as progress_percentage is not in the model
                        } for l in lessons]
                        st.dataframe(data, width='stretch')
                    else:
                        st.info("No hay progreso de lecciones registrado")
                
                with prog_tabs[1]:
                    vocab_count = len(session.exec(select(UserVocabularyProgress)).all())
                    st.metric("Palabras en Progreso", vocab_count)
                    
                with prog_tabs[2]:
                    attempts = session.exec(select(ExerciseAttempt)).all()
                    if attempts:
                        total = len(attempts)
                        correct = len([a for a in attempts if a.is_correct])
                        st.metric("Total Intentos", total)
                        st.metric("Correctos", f"{correct} ({int(correct/total*100)}%)")
                    else:
                        st.info("No hay intentos de ejercicios registrados")
            else:
                st.warning("⚠️ No hay perfil de usuario creado")
                if st.button("Crear Perfil por Defecto"):
                    from database.seed import seed_user
                    seed_user()
                    st.success("✅ Perfil creado")
                    st.rerun()
    
    # --- Tab: Reset Progress ---
    with user_tabs[1]:
        st.markdown("### 🔄 Resetear Progreso")
        st.warning("⚠️ **ADVERTENCIA**: Estas acciones son irreversibles")
        
        reset_options = st.tabs(["🎮 Gamificación", "📚 Aprendizaje", "🗑️ Reset Total"])
        
        # Reset Gamification
        with reset_options[0]:
            st.markdown("#### Resetear Sistema de Gamificación")
            st.info("Resetea niveles, XP, estrellas y desafíos. **No afecta** el progreso de lecciones ni vocabulario.")
            
            with st.form("reset_gamification_form"):
                st.markdown("**Se reseteará:**")
                st.markdown("- ✨ Nivel → 1")
                st.markdown("- 🏆 XP → 0")
                st.markdown("- ⭐ Estrellas → 0")
                st.markdown("- 🎯 Desafíos completados → 0")
                st.markdown("- 🔥 Racha → 0")
                
                confirm = st.checkbox("Confirmo que quiero resetear la gamificación")
                
                if st.form_submit_button("🔄 Resetear Gamificación", type="primary", disabled=not confirm):
                    try:
                        with get_session() as session:
                            user = session.exec(select(UserProfile)).first()
                            if user:
                                user.level = 1
                                user.xp = 0
                                user.total_stars = 0
                                user.challenges_completed = 0
                                user.perfect_challenges = 0
                                user.streak = 0
                                user.current_challenge_id = None
                                user.badges_json = None
                                session.add(user)
                                session.commit()
                                st.success("✅ Gamificación reseteada exitosamente")
                                st.balloons()
                                st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
        
        # Reset Learning Progress
        with reset_options[1]:
            st.markdown("#### Resetear Progreso de Aprendizaje")
            st.info("Resetea lecciones, vocabulario y ejercicios. **No afecta** XP ni estrellas.")
            
            with st.form("reset_learning_form"):
                st.markdown("**Se reseteará:**")
                st.markdown("- 📚 Progreso de lecciones")
                st.markdown("- 📖 Progreso de vocabulario (SRS)")
                st.markdown("- ✏️ Intentos de ejercicios")
                st.markdown("- 📖 Progreso de lecturas")
                
                confirm = st.checkbox("Confirmo que quiero resetear el progreso de aprendizaje")
                
                if st.form_submit_button("🔄 Resetear Aprendizaje", type="primary"):
                    if confirm:
                        try:
                            with get_session() as session:
                                from database import (
                                    LessonProgress, UserVocabularyProgress, 
                                    ExerciseAttempt, ReadingProgress, ReviewLog,
                                    UserProgressSummary
                                )
                                
                                # Delete all progress records
                                for model in [LessonProgress, UserVocabularyProgress, 
                                            ExerciseAttempt, ReadingProgress, ReviewLog]:
                                    records = session.exec(select(model)).all()
                                    for record in records:
                                        session.delete(record)
                                
                                # Reset summary
                                summary = session.exec(select(UserProgressSummary)).first()
                                if summary:
                                    summary.current_lesson = 1
                                    summary.lessons_completed = "[]"
                                    summary.lessons_in_progress = "[]"
                                    summary.vocab_mastery_avg = 0.0
                                    summary.exercises_accuracy_avg = 0.0
                                    summary.comprehension_avg = 0.0
                                    session.add(summary)
                                
                                session.commit()
                                st.success("✅ Progreso de aprendizaje reseteado")
                                
                                # Clear session state to force reload, but preserve auth
                                preserved_keys = {'is_admin': st.session_state.get('is_admin', False)}
                                for key in list(st.session_state.keys()):
                                    del st.session_state[key]
                                for key, value in preserved_keys.items():
                                    st.session_state[key] = value
                                
                                st.balloons()
                                st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
                    else:
                        st.error("❌ Debes confirmar la acción para proceder.")
        
        # Total Reset
        with reset_options[2]:
            st.markdown("#### 🗑️ Reset Total")
            st.error("⚠️ **PELIGRO**: Esto eliminará **TODO** el progreso del usuario")
            
            with st.form("reset_total_form"):
                st.markdown("**Se reseteará COMPLETAMENTE:**")
                st.markdown("- 🎮 Sistema de gamificación")
                st.markdown("- 📚 Progreso de lecciones")
                st.markdown("- 📖 Vocabulario y SRS")
                st.markdown("- ✏️ Ejercicios")
                st.markdown("- 📖 Lecturas")
                st.markdown("- 🎯 Desafíos")
                
                st.markdown("---")
                confirm1 = st.checkbox("Entiendo que esta acción es irreversible")
                confirm2 = st.checkbox("Confirmo que quiero eliminar TODO el progreso")
                confirmation_text = st.text_input("Escribe 'RESETEAR TODO' para confirmar")
                
                can_submit = confirm1 and confirm2 and confirmation_text == "RESETEAR TODO"
                
                if st.form_submit_button("🗑️ RESETEAR TODO", type="primary"):
                    if confirm1 and confirm2 and confirmation_text == "RESETEAR TODO":
                        try:
                            with get_session() as session:
                                from database import (
                                    UserProfile, LessonProgress, UserVocabularyProgress,
                                    ExerciseAttempt, ReadingProgress, ReviewLog,
                                    UserChallengeProgress, UserProgressSummary
                                )
                                
                                # Reset user profile
                                user = session.exec(select(UserProfile)).first()
                                if user:
                                    user.level = 1
                                    user.xp = 0
                                    user.total_stars = 0
                                    user.challenges_completed = 0
                                    user.perfect_challenges = 0
                                    user.streak = 0
                                    user.current_challenge_id = None
                                    user.badges_json = None
                                    session.add(user)
                                
                                # Delete all progress records
                                for model in [LessonProgress, UserVocabularyProgress,
                                            ExerciseAttempt, ReadingProgress, ReviewLog,
                                            UserChallengeProgress]:
                                    records = session.exec(select(model)).all()
                                    for record in records:
                                        session.delete(record)
                                
                                # Reset summary
                                summary = session.exec(select(UserProgressSummary)).first()
                                if summary:
                                    summary.current_lesson = 1
                                    summary.lessons_completed = "[]"
                                    summary.lessons_in_progress = "[]"
                                    summary.vocab_mastery_avg = 0.0
                                    summary.exercises_accuracy_avg = 0.0
                                    summary.comprehension_avg = 0.0
                                    summary.challenges_passed = "[]"
                                    summary.challenges_failed_attempts = 0
                                    summary.weak_areas = "[]"
                                    summary.total_xp = 0
                                    summary.level = 1
                                    summary.badges = "[]"
                                    session.add(summary)
                                
                                session.commit()
                                st.success("✅ TODO el progreso ha sido reseteado")
                                
                                # Clear session state to force reload, but preserve auth
                                preserved_keys = {'is_admin': st.session_state.get('is_admin', False)}
                                for key in list(st.session_state.keys()):
                                    del st.session_state[key]
                                for key, value in preserved_keys.items():
                                    st.session_state[key] = value
                                
                                st.snow()
                                st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
                    else:
                        st.error("❌ Debes marcar ambas casillas y escribir 'RESETEAR TODO' correctamente para confirmar.")
    
    # --- Tab: Configuration ---
    with user_tabs[2]:
        st.markdown("### ⚙️ Configuración de Usuario")
        
        with get_session() as session:
            user = session.exec(select(UserProfile)).first()
            
            if user:
                with st.form("user_config_form"):
                    username = st.text_input("Nombre de Usuario", value=user.username)
                    level = st.number_input("Nivel", min_value=1, max_value=100, value=user.level)
                    xp = st.number_input("XP", min_value=0, value=user.xp)
                    
                    if st.form_submit_button("💾 Guardar Configuración"):
                        user.username = username
                        user.level = level
                        user.xp = xp
                        session.add(user)
                        session.commit()
                        st.success("✅ Configuración actualizada")
                        st.rerun()
            else:
                st.info("Crea un perfil de usuario primero en la pestaña 'Progreso Actual'")

# --- SECTION: STATS ---
elif section == "Estadísticas":
    st.markdown("## 📋 Estadísticas del Corpus")
    
    with get_session() as session:
        all_words = session.exec(select(Word)).all()
        texts = session.exec(select(Text)).all()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Palabras", len(all_words))
        col2.metric("Total Textos", len(texts))
        
        # Breakdown
        pos_counts = {}
        for w in all_words:
            pos_counts[w.part_of_speech] = pos_counts.get(w.part_of_speech, 0) + 1
        
        st.markdown("### Distribución por Tipo")
        st.bar_chart(pos_counts)


# --- SECTION: REQUISITOS DE LECCIÓN ---
if section == "Requisitos de Lección":
    st.markdown("## 📋 Gestión de Requisitos de Lección")
    
    st.info("""
    **Filosofía de Diseño:** 100% de requisitos obligatorios (strict mode)  
    _"Mejor frustración al principio que al final cuando se vuelve más difícil"_
    """)
    
    # Selector de lección
    lesson_number = st.selectbox(
        "Seleccionar Lección",
        options=list(range(1, 41)),
        format_func=lambda x: f"Lección {x}"
    )
    
    with get_session() as session:
        # Obtener requisitos existentes para esta lección
        requirements = session.exec(
            select(LessonRequirement)
            .where(LessonRequirement.lesson_number == lesson_number)
            .order_by(LessonRequirement.id)
        ).all()
        
        st.markdown(f"### Requisitos para Lección {lesson_number}")
        
        if requirements:
            # Mostrar requisitos existentes
            for req in requirements:
                with st.expander(
                    f"{'✅ ' if req.is_required else '⭐ '}{req.description or req.requirement_type}",
                    expanded=False
                ):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Tipo:** `{req.requirement_type}`")
                        st.markdown(f"**Obligatorio:** {'Sí' if req.is_required else 'No (Opcional)'}")
                        st.markdown(f"**Peso:** {req.weight}")
                    
                    with col2:
                        if req.criteria_json:
                            st.markdown("**Criterios JSON:**")
                            try:
                                criteria = json.loads(req.criteria_json)
                                st.json(criteria)
                            except:
                                st.code(req.criteria_json)
                        
                        # Legacy fields
                        if req.required_vocab_mastery > 0:
                            st.markdown(f"**Dominio vocab:** {req.required_vocab_mastery:.0%}")
                        if req.required_translations > 0:
                            st.markdown(f"**Traducciones:** {req.required_translations}")
                        if req.required_analyses > 0:
                            st.markdown(f"**Análisis:** {req.required_analyses}")
                        if req.required_readings > 0:
                            st.markdown(f"**Lecturas:** {req.required_readings}")
                    
                    # Botones de acción
                    col_edit, col_delete = st.columns(2)
                    with col_edit:
                        if st.button("✏️ Editar", key=f"edit_{req.id}"):
                            st.session_state[f'editing_req_{req.id}'] = True
                            st.rerun()
                    
                    with col_delete:
                        if st.button("🗑️ Eliminar", key=f"delete_{req.id}", type="secondary"):
                            session.delete(req)
                            session.commit()
                            st.success(f"Requisito eliminado")
                            st.rerun()
                    
                    # Form de edición (si está en modo edición)
                    if st.session_state.get(f'editing_req_{req.id}', False):
                        st.markdown("---")
                        st.markdown("#### Editar Requisito")
                        
                        with st.form(f"edit_form_{req.id}"):
                            new_description = st.text_input("Descripción", value=req.description or "")
                            new_type = st.selectbox(
                                "Tipo de Requisito",
                                options=["vocabulary_mastery", "challenge_completion", "analysis_practice", "reading_completion", "exercise_completion"],
                                index=["vocabulary_mastery", "challenge_completion", "analysis_practice", "reading_completion", "exercise_completion"].index(req.requirement_type) if req.requirement_type in ["vocabulary_mastery", "challenge_completion", "analysis_practice", "reading_completion", "exercise_completion"] else 0
                            )
                            new_is_required = st.checkbox("Obligatorio", value=req.is_required)
                            new_weight = st.number_input("Peso", min_value=0.1, max_value=5.0, value=req.weight, step=0.1)
                            new_criteria = st.text_area("Criterios JSON", value=req.criteria_json or "{}")
                            
                            col_save, col_cancel = st.columns(2)
                            with col_save:
                                if st.form_submit_button("💾 Guardar Cambios", type="primary"):
                                    req.description = new_description
                                    req.requirement_type = new_type
                                    req.is_required = new_is_required
                                    req.is_hard_requirement = new_is_required  # Mantener sincronizado
                                    req.weight = new_weight
                                    req.criteria_json = new_criteria
                                    
                                    session.add(req)
                                    session.commit()
                                    
                                    st.session_state[f'editing_req_{req.id}'] = False
                                    st.success("Requisito actualizado")
                                    st.rerun()
                            
                            with col_cancel:
                                if st.form_submit_button("❌ Cancelar"):
                                    st.session_state[f'editing_req_{req.id}'] = False
                                    st.rerun()
            
            # Resumen
            st.markdown("---")
            st.markdown("### 📊 Resumen")
            required_count = sum(1 for r in requirements if r.is_required)
            optional_count = len(requirements) - required_count
            total_weight = sum(r.weight for r in requirements if r.is_required)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Requisitos Obligatorios", required_count)
            col2.metric("Requisitos Opcionales", optional_count)
            col3.metric("Peso Total", f"{total_weight:.1f}")
        
        else:
            st.warning(f"No hay requisitos definidos para la Lección {lesson_number}")
        
        # Formulario para agregar nuevo requisito
        st.markdown("---")
        st.markdown("### ➕ Agregar Nuevo Requisito")
        
        with st.form("add_requirement"):
            new_req_description = st.text_input("Descripción", placeholder="Ej: Dominar 20 palabras con 80% de precisión")
            
            new_req_type = st.selectbox(
                "Tipo de Requisito",
                options=["vocabulary_mastery", "challenge_completion", "analysis_practice", "reading_completion", "exercise_completion"],
                format_func=lambda x: {
                    "vocabulary_mastery": "📚 Dominio de Vocabulario",
                    "challenge_completion": "🎯 Completar Desafíos",
                    "analysis_practice": "🔍 Práctica de Análisis",
                    "reading_completion": "📖 Completar Lecturas",
                    "exercise_completion": "✍️ Completar Ejercicios"
                }.get(x, x)
            )
            
            new_req_is_required = st.checkbox("Obligatorio (required para pasar la lección)", value=True)
            new_req_weight = st.number_input("Peso", min_value=0.1, max_value=5.0, value=1.0, step=0.1, help="Importancia relativa de este requisito")
            
            # Criterios JSON
            st.markdown("**Criterios (JSON):**")
            
            # Templates según tipo
            if new_req_type == "vocabulary_mastery":
                template = json.dumps({"min_words": 20, "min_accuracy": 0.8}, indent=2)
            elif new_req_type == "challenge_completion":
                template = json.dumps({"challenge_ids": [1, 2, 3], "min_stars": 2}, indent=2)
            elif new_req_type == "analysis_practice":
                template = json.dumps({"min_analyses": 5, "min_accuracy": 0.7}, indent=2)
            else:
                template = json.dumps({}, indent=2)
            
            new_req_criteria = st.text_area("Criterios JSON", value=template, height=150)
            
            if st.form_submit_button("➕ Agregar Requisito", type="primary"):
                # Validar JSON
                try:
                    json.loads(new_req_criteria)
                except:
                    st.error("El JSON de criterios no es válido")
                    st.stop()
                
                # Crear requisito
                new_requirement = LessonRequirement(
                    lesson_number=lesson_number,
                    requirement_type=new_req_type,
                    description=new_req_description,
                    is_required=new_req_is_required,
                    is_hard_requirement=new_req_is_required,
                    weight=new_req_weight,
                    criteria_json=new_req_criteria,
                    required_vocab_mastery=0.0,  # Legacy defaults
                    required_translations=0,
                    required_analyses=0,
                    required_readings=0
                )
                
                session.add(new_requirement)
                session.commit()
                
                st.success(f"✅ Requisito agregado a Lección {lesson_number}")
                st.rerun()

# --- SECTION: CATALOGACIÓN (Módulo independiente) ---
elif section == "Catalogación":
    if catalog_module and catalog_module.render(section):
        pass  # El módulo se renderiza a sí mismo
    else:
        st.warning("⚠️ Módulo de Catalogación no disponible")
        st.info("""
        Para usar este módulo:
        1. Instala las dependencias del catalogador
        2. Ejecuta: `python catalog_tool.py`
        3. Vuelve a cargar esta página
        """)

# --- SECTION: CONFIGURACIÓN ---
elif section == "Configuración":
        # Configuración Global
        st.markdown("---")
        st.markdown("### ⚙️ Configuración Global")
        
        st.info("""
        **Umbral de Desbloqueo Actual:** 100% de requisitos obligatorios  
        Este umbral está hardcoded según tu preferencia. Para hacerlo configurable, se puede agregar a SystemSetting.
        """)
        
        if st.button("🔄 Aplicar cambios a todos los usuarios"):
            st.warning("Esta función recalculará el progreso de todos los usuarios basándose en los nuevos requisitos.")
            st.info("Funcionalidad pendiente de implementación - Stage 3")
