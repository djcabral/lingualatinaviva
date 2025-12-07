"""
EJEMPLO DE INTEGRACIÓN - Validación, Auditoría y Asistentes

Este archivo muestra cómo integrar el sistema completo de validación,
auditoría y asistentes en el panel de administración.

NOTA: Este es un ejemplo. La integración final en pages/99_⚙️_Administracion.py
seguirá este patrón.
"""

import streamlit as st
import sys
import os

# Setup paths
root_path = os.path.dirname(os.path.dirname(__file__))
if root_path not in sys.path:
    sys.path.append(root_path)

from utils.admin_data_assistants import (
    AssistantMode, DataType, create_assistant,
    VocabularyAssistant, SentenceAssistant, TextAssistant,
)
from utils.admin_validation_audit import (
    ComprehensiveValidator, ValidationLevel
)
from utils.admin_validation_audit_ui import (
    render_validation_level_selector,
    render_vocabulary_validation,
    render_sentence_validation,
    render_text_validation,
    render_audit_log_table,
    render_audit_log_details,
    render_audit_report_export,
    render_save_confirmation,
    render_save_success_message,
    init_validator,
)
from database.connection import get_session
from database import Word, SentenceAnalysis, Text


# ============================================================================
# EJEMPLO 1: ASISTENTE DE VOCABULARIO CON VALIDACIÓN
# ============================================================================

def example_vocabulary_assistant_with_validation():
    """
    Ejemplo completo: Usuario carga vocabulario con validación y auditoría
    """
    
    st.header("🧙 Asistente de Vocabulario")
    st.write("Carga palabras con validación automática de duplicados y completitud")
    
    # 1. Selector de nivel de validación
    validation_level = render_validation_level_selector()
    
    # 2. Inicializar validador
    validator = init_validator(validation_level)
    
    # 3. Crear asistente
    if 'vocab_assistant' not in st.session_state:
        st.session_state.vocab_assistant = VocabularyAssistant(
            mode=AssistantMode.MANUAL
        )
    
    assistant = st.session_state.vocab_assistant
    
    # 4. Renderizar paso actual
    st.subheader(f"Paso {assistant.current_step + 1} de {len(assistant.steps)}")
    step = assistant.get_current_step()
    
    # Recolectar datos del paso
    step_data = {}
    for field in step.fields:
        # Renderizar campo (simplificado)
        if field['type'] == 'text':
            step_data[field['name']] = st.text_input(
                field['name'],
                help=field.get('help', ''),
                key=f"vocab_{field['name']}"
            )
        elif field['type'] == 'number':
            step_data[field['name']] = st.number_input(
                field['name'],
                min_value=field.get('min', 0),
                max_value=field.get('max', 10),
                value=field.get('value', 1),
                key=f"vocab_{field['name']}"
            )
        elif field['type'] == 'select':
            step_data[field['name']] = st.selectbox(
                field['name'],
                field.get('options', []),
                key=f"vocab_{field['name']}"
            )
    
    # 5. Guardar datos del paso
    if st.button("Guardar paso", key="save_vocab_step"):
        assistant.save_step_data(step_data)
        st.success("Datos del paso guardados")
    
    # 6. Botones de navegación
    col1, col2, col3 = st.columns(3)
    with col1:
        if assistant.has_previous_step():
            if st.button("⬅️ Anterior", key="vocab_prev"):
                assistant.previous_step()
                st.rerun()
    
    with col2:
        if assistant.has_next_step():
            if st.button("Siguiente ➡️", key="vocab_next"):
                assistant.next_step()
                st.rerun()
        else:
            # Último paso - validar y guardar
            if st.button("🎉 Finalizar", key="vocab_finish"):
                # Compilar datos completos
                vocab_data = {
                    'latin_word': st.session_state.get('vocab_latin_word', ''),
                    'translation': st.session_state.get('vocab_translation', ''),
                    'part_of_speech': st.session_state.get('vocab_part_of_speech', ''),
                    'level': st.session_state.get('vocab_level', 1),
                    'genitive': st.session_state.get('vocab_genitive', ''),
                    'gender': st.session_state.get('vocab_gender', ''),
                    'declension': st.session_state.get('vocab_declension', ''),
                    'principal_parts': st.session_state.get('vocab_principal_parts', ''),
                    'conjugation': st.session_state.get('vocab_conjugation', ''),
                    'source': st.session_state.get('vocab_source', 'manual'),
                    'notes': st.session_state.get('vocab_notes', ''),
                }
                
                # Validar
                validation_result = render_vocabulary_validation(
                    vocab_data,
                    validator,
                    show_duplicates=True
                )
                
                # Confirmación
                if validation_result['is_valid']:
                    if render_save_confirmation(validation_result, vocab_data, 'vocabulary'):
                        # Guardar en BD (aquí va la lógica real)
                        with get_session() as session:
                            new_word = Word(
                                latin=vocab_data['latin_word'],
                                translation=vocab_data['translation'],
                                part_of_speech=vocab_data['part_of_speech'],
                                level=vocab_data['level'],
                            )
                            session.add(new_word)
                            session.commit()
                            session.refresh(new_word)
                            
                            render_save_success_message('vocabulary', new_word.id)
    
    with col3:
        if st.button("❌ Cancelar", key="vocab_cancel"):
            st.warning("Asistente cancelado")
            if 'vocab_assistant' in st.session_state:
                del st.session_state.vocab_assistant


# ============================================================================
# EJEMPLO 2: ASISTENTE DE ORACIONES CON VALIDACIÓN
# ============================================================================

def example_sentence_assistant_with_validation():
    """
    Ejemplo completo: Usuario carga oraciones con validación
    """
    
    st.header("🧙 Asistente de Oraciones")
    st.write("Carga oraciones analizadas con validación automática")
    
    # 1. Selector de nivel
    validation_level = render_validation_level_selector()
    
    # 2. Inicializar validador
    validator = init_validator(validation_level)
    
    # 3. Crear asistente
    if 'sentence_assistant' not in st.session_state:
        st.session_state.sentence_assistant = SentenceAssistant(
            mode=AssistantMode.MANUAL
        )
    
    assistant = st.session_state.sentence_assistant
    
    # 4. Renderizar UI similar a vocabulario
    st.subheader(f"Paso {assistant.current_step + 1} de {len(assistant.steps)}")
    
    # Formulario simplificado
    sentence_data = {
        'latin_text': st.text_area(
            "Oración en latín",
            height=100,
            key="sentence_latin"
        ),
        'translation': st.text_area(
            "Traducción al español",
            height=100,
            key="sentence_translation"
        ),
        'level': st.slider(
            "Nivel de dificultad",
            1, 10, 1,
            key="sentence_level"
        ),
    }
    
    # Validar
    if st.button("Validar Oración", key="validate_sentence"):
        validation_result = render_sentence_validation(
            sentence_data,
            validator,
            show_duplicates=True
        )
        
        # Guardar si es válido
        if validation_result['is_valid']:
            if render_save_confirmation(validation_result, sentence_data, 'sentence'):
                with get_session() as session:
                    new_sentence = SentenceAnalysis(
                        latin_text=sentence_data['latin_text'],
                        spanish_translation=sentence_data['translation'],
                        complexity_level=sentence_data['level'],
                    )
                    session.add(new_sentence)
                    session.commit()
                    session.refresh(new_sentence)
                    
                    render_save_success_message('sentence', new_sentence.id)


# ============================================================================
# EJEMPLO 3: ASISTENTE DE TEXTOS CON VALIDACIÓN
# ============================================================================

def example_text_assistant_with_validation():
    """
    Ejemplo completo: Usuario carga textos con validación
    """
    
    st.header("🧙 Asistente de Textos")
    st.write("Carga textos completos con análisis de completitud")
    
    # 1. Selector de nivel
    validation_level = render_validation_level_selector()
    
    # 2. Inicializar validador
    validator = init_validator(validation_level)
    
    # 3. Formulario de texto
    text_data = {
        'title': st.text_input(
            "Título del texto",
            key="text_title"
        ),
        'author': st.text_input(
            "Autor",
            key="text_author"
        ),
        'content': st.text_area(
            "Contenido en latín",
            height=300,
            key="text_content"
        ),
        'difficulty': st.slider(
            "Dificultad",
            1, 10, 1,
            key="text_difficulty"
        ),
    }
    
    # Validar
    if st.button("Validar Texto", key="validate_text"):
        validation_result = render_text_validation(
            text_data,
            validator,
            show_duplicates=True
        )
        
        # Guardar si es válido
        if validation_result['is_valid']:
            if render_save_confirmation(validation_result, text_data, 'text'):
                with get_session() as session:
                    new_text = Text(
                        title=text_data['title'],
                        author=text_data['author'],
                        content=text_data['content'],
                        difficulty=text_data['difficulty'],
                    )
                    session.add(new_text)
                    session.commit()
                    session.refresh(new_text)
                    
                    render_save_success_message('text', new_text.id)


# ============================================================================
# EJEMPLO 4: VISTA DE AUDITORÍA
# ============================================================================

def example_audit_view():
    """
    Ejemplo: Panel de auditoría mostrando todos los logs
    """
    
    st.header("📋 Panel de Auditoría")
    
    # Inicializar validador (para acceder a logs)
    validator = init_validator(ValidationLevel.MODERATE)
    
    # Tabs de auditoría
    tab1, tab2, tab3 = st.tabs([
        "📊 Tabla de Logs",
        "🔍 Detalles",
        "📥 Exportar"
    ])
    
    with tab1:
        st.subheader("Tabla Resumen")
        render_audit_log_table(validator)
    
    with tab2:
        st.subheader("Detalles Detallados")
        render_audit_log_details(validator)
    
    with tab3:
        st.subheader("Exportar Reporte")
        render_audit_report_export(validator)


# ============================================================================
# MENÚ PRINCIPAL
# ============================================================================

def main():
    st.set_page_config(page_title="Ejemplo - Asistentes", page_icon="🧙")
    
    st.title("🧙 Ejemplo de Integración Completa")
    st.write("""
    Este archivo demuestra cómo integrar:
    1. Asistentes de carga de datos
    2. Validación de duplicados
    3. Validación de completitud
    4. Sistema de auditoría
    
    en el panel de administración.
    """)
    
    option = st.sidebar.radio(
        "Selecciona una opción:",
        [
            "Asistente Vocabulario",
            "Asistente Oraciones",
            "Asistente Textos",
            "Panel de Auditoría",
        ]
    )
    
    if option == "Asistente Vocabulario":
        example_vocabulary_assistant_with_validation()
    elif option == "Asistente Oraciones":
        example_sentence_assistant_with_validation()
    elif option == "Asistente Textos":
        example_text_assistant_with_validation()
    elif option == "Panel de Auditoría":
        example_audit_view()


if __name__ == "__main__":
    main()
