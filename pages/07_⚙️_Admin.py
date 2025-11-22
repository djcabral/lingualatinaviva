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

from database.connection import get_session
from database.models import Word, Text, TextWordLink

st.set_page_config(page_title="Admin", page_icon="⚙️", layout="wide")

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
        if st.button("Ingresar", type="primary", use_container_width=True):
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

# Sidebar Navigation
section = st.sidebar.radio(
    "Sección",
    ["Vocabulario", "Textos", "Estadísticas"],
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
    
    vocab_tabs = st.tabs(["➕ Sustantivos", "➕ Verbos", "➕ Otros", "📥 Importar", "📤 Exportar", "📋 Lista Completa", "❓ Ayuda"])
    
    # --- Tab: Nouns ---
    with vocab_tabs[0]:
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
                            irregular_forms=irregular_json, category="noun"
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

    # --- Tab: Others ---
    with vocab_tabs[2]:
        st.markdown("### Añadir Otra Palabra")
        with st.form("add_other"):
            col1, col2 = st.columns(2)
            with col1:
                latin = st.text_input("Palabra (Latín) *")
                translation = st.text_input("Traducción *")
                level = st.number_input("Nivel", min_value=1, max_value=10, value=1, key="other_level")
            
            with col2:
                pos_options = {
                    "Adjetivo": "adjective", "Adverbio": "adverb", 
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
    with vocab_tabs[3]:
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
                        use_container_width=True
                    )
                    
                    # Count selected
                    to_import_count = len(edited_df[edited_df['Importar'] == True])
                    
                    st.info(f"Se importarán **{to_import_count}** palabras.")
                    
                    # Import button
                    if st.button("💾 Importar Selección", type="primary", use_container_width=True, disabled=to_import_count==0):
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
    with vocab_tabs[4]:
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
        
        if st.button("📥 Generar Archivo", use_container_width=True, type="primary"):
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
                        use_container_width=True
                    )
                    
                    st.success(f"✅ {len(words)} palabras listas para descargar")

    # --- Tab: List ---
    with vocab_tabs[5]:
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
                    use_container_width=True
                )
            else:
                st.info("No hay palabras.")
    
    # --- Tab: Help ---
    with vocab_tabs[6]:
        st.markdown("### ❓ Ayuda y Tutoriales")
        
        help_sections = st.tabs(["📖 Manual de Entrada", "📥 Importar CSV/Excel", "📦 Descargar Plantillas"])
        
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
        
        # CSV/Excel Import Tutorial
        with help_sections[1]:
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
        with help_sections[2]:
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
                    use_container_width=True
                )
                
                excel_bytes = VocabularyExporter.to_excel(noun_template)
                st.download_button(
                    label="⬇️ Excel",
                    data=excel_bytes,
                    file_name="plantilla_sustantivos.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
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
                    use_container_width=True
                )
                
                excel_bytes = VocabularyExporter.to_excel(verb_template)
                st.download_button(
                    label="⬇️ Excel",
                    data=excel_bytes,
                    file_name="plantilla_verbos.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
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
                    use_container_width=True
                )
                
                excel_bytes = VocabularyExporter.to_excel(other_template)
                st.download_button(
                    label="⬇️ Excel",
                    data=excel_bytes,
                    file_name="plantilla_otras.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            
            st.markdown("---")
            st.success("✅ Descarga la plantilla que necesites, complétala, y súbela en la pestaña '📥 Importar'")


# --- SECTION: TEXTS ---
elif section == "Textos":
    st.markdown("## 📜 Gestión de Textos")
    
    text_tabs = st.tabs(["➕ Añadir Texto", "📚 Ver Textos", "🛠️ Herramientas"])
    
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
        
        if st.button("💾 Guardar Texto", use_container_width=True, type="primary"):
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
                    st.caption(f"Autor: {t.author.name if t.author else 'Desconocido'}")

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
