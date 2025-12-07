"""
INTERFAZ STREAMLIT PARA ASISTENTES DE CARGA DE DATOS

Componentes UI para guiar al usuario paso a paso a través de los asistentes
de carga de Vocabulario, Oraciones y Textos.

Filosofía:
- Paso a paso, no abrumador
- Validación en cada etapa
- Sugerencias del motor NLP
- Feedback claro y directo
"""

import streamlit as st
from typing import Dict, Any, Optional, Tuple
import json

from utils.admin_data_assistants import (
    AssistantMode, DataType, create_assistant,
    VocabularyAssistant, SentenceAssistant, TextAssistant,
    VocabularyWizardData, SentenceWizardData, TextWizardData
)


# ============================================================================
# COMPONENTES COMPARTIDOS
# ============================================================================

def render_progress_bar(current_step: int, total_steps: int) -> None:
    """Renderiza una barra de progreso del asistente"""
    progress = current_step / total_steps
    st.progress(progress)
    col1, col2, col3 = st.columns(3)
    col1.write(f"Paso {current_step + 1}")
    col2.write(f"de {total_steps}")
    col3.write(f"{int(progress * 100)}%")


def render_step_navigation(assistant) -> Tuple[bool, bool]:
    """Renderiza botones de navegación entre pasos"""
    col1, col2, col3, col4 = st.columns(4)
    
    prev_clicked = False
    next_clicked = False
    skip_clicked = False
    
    with col1:
        if assistant.has_previous_step():
            prev_clicked = st.button("⬅️ Anterior", key="prev_step")
    
    with col2:
        if st.button("💾 Guardar Progreso", key="save_progress"):
            st.success("✅ Progreso guardado")
    
    with col3:
        if assistant.has_next_step():
            skip_clicked = st.button("Omitir ⏭️", key="skip_step")
    
    with col4:
        if assistant.has_next_step():
            next_clicked = st.button("Siguiente ➡️", key="next_step", type="primary")
        else:
            st.button("🎉 Finalizar", key="finish", type="primary", disabled=True)
    
    return prev_clicked, next_clicked


def render_field(field: Dict[str, Any], key_prefix: str = "") -> Any:
    """Renderiza un campo individual"""
    field_name = field['name']
    field_type = field.get('type', 'text')
    required = field.get('required', False)
    
    label = f"{field_name.replace('_', ' ').title()}{'*' if required else ''}"
    key = f"{key_prefix}_{field_name}"
    
    try:
        if field_type == 'text':
            return st.text_input(
                label,
                help=field.get('help', ''),
                placeholder=field.get('placeholder', ''),
                key=key
            )
        
        elif field_type == 'textarea':
            return st.text_area(
                label,
                help=field.get('help', ''),
                placeholder=field.get('placeholder', ''),
                height=field.get('height', 100),
                key=key
            )
        
        elif field_type == 'number':
            return st.number_input(
                label,
                min_value=field.get('min', 0),
                max_value=field.get('max', 100),
                value=field.get('value', 0),
                help=field.get('help', ''),
                key=key
            )
        
        elif field_type == 'select':
            options = field.get('options', [])
            return st.selectbox(
                label,
                options,
                help=field.get('help', ''),
                key=key
            )
        
        elif field_type == 'multiselect':
            options = field.get('options', [])
            return st.multiselect(
                label,
                options,
                help=field.get('help', ''),
                key=key
            )
        
        elif field_type == 'checkbox':
            return st.checkbox(
                label,
                help=field.get('help', ''),
                key=key
            )
    
    except Exception as e:
        st.error(f"Error renderizando campo {field_name}: {str(e)}")
        return None


# ============================================================================
# ASISTENTE DE VOCABULARIO - UI
# ============================================================================

def render_vocabulary_assistant(mode: AssistantMode = AssistantMode.MANUAL) -> Optional[VocabularyWizardData]:
    """
    Renderiza el asistente completo de vocabulario
    
    Returns:
        VocabularyWizardData si se completa, None si se cancela
    """
    
    # Inicializar asistente en session state
    if 'vocab_assistant' not in st.session_state:
        st.session_state.vocab_assistant = create_assistant(DataType.VOCABULARY, mode)
    
    assistant: VocabularyAssistant = st.session_state.vocab_assistant
    
    # Encabezado
    st.markdown("## 📚 Asistente de Carga de Vocabulario")
    st.markdown(f"**Modo:** {mode.value.upper()}")
    
    # Barra de progreso
    render_progress_bar(assistant.current_step, len(assistant.steps))
    
    # Paso actual
    step = assistant.get_current_step()
    if not step:
        st.error("Error: No hay pasos disponibles")
        return None
    
    # Contenido del paso
    with st.container(border=True):
        st.markdown(f"### {step.title}")
        st.write(step.description)
        
        if step.help_text:
            with st.expander("ℹ️ Información"):
                st.write(step.help_text)
                if step.examples:
                    st.write("**Ejemplos:**")
                    for example in step.examples:
                        st.write(f"- {example}")
        
        # Renderizar campos del paso
        st.markdown("---")
        
        # Mostrar solo campos visibles (según POS si ya se seleccionó)
        pos = assistant.wizard_data.part_of_speech if assistant.current_step > 0 else None
        
        if pos and hasattr(assistant, 'get_visible_fields'):
            visible_fields = assistant.get_visible_fields(pos)
        else:
            visible_fields = step.fields
        
        # Recolectar datos del paso
        step_data = {}
        for field in visible_fields:
            value = render_field(field, f"vocab_step{step.step_number}")
            if value is not None:
                step_data[field['name']] = value
        
        # Guardar datos en el asistente y en wizard_data
        assistant.save_step_data(step_data)
        
        # Actualizar wizard_data con los datos recolectados
        for key, value in step_data.items():
            if hasattr(assistant.wizard_data, key):
                setattr(assistant.wizard_data, key, value)
    
    # Validación
    is_valid, errors = assistant.validate_step(step_data)
    
    if errors:
        st.error("⚠️ Hay errores en este paso:")
        for error in errors:
            st.write(f"  • {error}")
    
    # Navegación
    st.markdown("---")
    prev_clicked, next_clicked = render_step_navigation(assistant)
    
    if prev_clicked:
        assistant.previous_step()
        st.rerun()
    
    if next_clicked:
        if is_valid:
            if assistant.next_step():
                st.rerun()
            else:
                # Último paso completado
                st.success("✅ ¡Asistente completado!")
                return assistant.wizard_data
        else:
            st.error("❌ Por favor corrige los errores antes de continuar")
    
    return None


# ============================================================================
# ASISTENTE DE ORACIONES - UI
# ============================================================================

def render_sentence_assistant(mode: AssistantMode = AssistantMode.MANUAL) -> Optional[SentenceWizardData]:
    """Renderiza el asistente de oraciones"""
    
    if 'sentence_assistant' not in st.session_state:
        st.session_state.sentence_assistant = create_assistant(DataType.SENTENCES, mode)
    
    assistant: SentenceAssistant = st.session_state.sentence_assistant
    
    st.markdown("## 📝 Asistente de Carga de Oraciones")
    st.markdown(f"**Modo:** {mode.value.upper()}")
    
    render_progress_bar(assistant.current_step, len(assistant.steps))
    
    step = assistant.get_current_step()
    if not step:
        st.error("Error: No hay pasos disponibles")
        return None
    
    with st.container(border=True):
        st.markdown(f"### {step.title}")
        st.write(step.description)
        
        if step.help_text:
            with st.expander("ℹ️ Información"):
                st.write(step.help_text)
        
        st.markdown("---")
        
        # Recolectar datos
        step_data = {}
        for field in step.fields:
            value = render_field(field, f"sentence_step{step.step_number}")
            if value is not None:
                step_data[field['name']] = value
        
        assistant.save_step_data(step_data)
        
        for key, value in step_data.items():
            if hasattr(assistant.wizard_data, key):
                setattr(assistant.wizard_data, key, value)
    
    is_valid, errors = assistant.validate_step(step_data)
    
    if errors:
        st.error("⚠️ Hay errores en este paso:")
        for error in errors:
            st.write(f"  • {error}")
    
    st.markdown("---")
    prev_clicked, next_clicked = render_step_navigation(assistant)
    
    if prev_clicked:
        assistant.previous_step()
        st.rerun()
    
    if next_clicked:
        if is_valid:
            if assistant.next_step():
                st.rerun()
            else:
                st.success("✅ ¡Asistente completado!")
                return assistant.wizard_data
        else:
            st.error("❌ Por favor corrige los errores antes de continuar")
    
    return None


# ============================================================================
# ASISTENTE DE TEXTOS - UI
# ============================================================================

def render_text_assistant(mode: AssistantMode = AssistantMode.MANUAL) -> Optional[TextWizardData]:
    """Renderiza el asistente de textos"""
    
    if 'text_assistant' not in st.session_state:
        st.session_state.text_assistant = create_assistant(DataType.TEXTS, mode)
    
    assistant: TextAssistant = st.session_state.text_assistant
    
    st.markdown("## 📖 Asistente de Carga de Textos")
    st.markdown(f"**Modo:** {mode.value.upper()}")
    
    render_progress_bar(assistant.current_step, len(assistant.steps))
    
    step = assistant.get_current_step()
    if not step:
        st.error("Error: No hay pasos disponibles")
        return None
    
    with st.container(border=True):
        st.markdown(f"### {step.title}")
        st.write(step.description)
        
        if step.help_text:
            with st.expander("ℹ️ Información"):
                st.write(step.help_text)
        
        st.markdown("---")
        
        # Recolectar datos
        step_data = {}
        for field in step.fields:
            value = render_field(field, f"text_step{step.step_number}")
            if value is not None:
                step_data[field['name']] = value
        
        assistant.save_step_data(step_data)
        
        for key, value in step_data.items():
            if hasattr(assistant.wizard_data, key):
                setattr(assistant.wizard_data, key, value)
    
    is_valid, errors = assistant.validate_step(step_data)
    
    if errors:
        st.error("⚠️ Hay errores en este paso:")
        for error in errors:
            st.write(f"  • {error}")
    
    st.markdown("---")
    prev_clicked, next_clicked = render_step_navigation(assistant)
    
    if prev_clicked:
        assistant.previous_step()
        st.rerun()
    
    if next_clicked:
        if is_valid:
            if assistant.next_step():
                st.rerun()
            else:
                st.success("✅ ¡Asistente completado!")
                return assistant.wizard_data
        else:
            st.error("❌ Por favor corrige los errores antes de continuar")
    
    return None


# ============================================================================
# SELECTOR DE MODO
# ============================================================================

def render_assistant_mode_selector() -> Tuple[DataType, AssistantMode]:
    """Renderiza un selector para elegir tipo de datos y modo de asistencia"""
    
    st.markdown("### Selecciona qué deseas cargar")
    
    col1, col2 = st.columns(2)
    
    with col1:
        data_type = st.radio(
            "Tipo de datos:",
            [DataType.VOCABULARY, DataType.SENTENCES, DataType.TEXTS],
            format_func=lambda x: {
                DataType.VOCABULARY: "📚 Vocabulario",
                DataType.SENTENCES: "📝 Oraciones",
                DataType.TEXTS: "📖 Textos"
            }[x]
        )
    
    with col2:
        mode = st.radio(
            "Modo de carga:",
            [AssistantMode.MANUAL, AssistantMode.SEMI_AUTO, AssistantMode.FULL_AUTO],
            format_func=lambda x: {
                AssistantMode.MANUAL: "✍️ Manual completo",
                AssistantMode.SEMI_AUTO: "🤝 Semi-automático",
                AssistantMode.FULL_AUTO: "🤖 Automático completo"
            }[x]
        )
    
    return data_type, mode


__all__ = [
    'render_vocabulary_assistant',
    'render_sentence_assistant',
    'render_text_assistant',
    'render_assistant_mode_selector',
]
