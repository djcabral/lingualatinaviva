"""
COMPONENTES DE VALIDACIÓN Y AUDITORÍA PARA UI - Panel Admin

Integración de validación, detección de duplicados y auditoría
en la interfaz de los asistentes de carga de datos.

Filosofía: Proporcionar feedback inmediato y claro sobre la calidad de los datos.
"""

import streamlit as st
from typing import Dict, Any, Optional, Tuple
import json
from datetime import datetime

from utils.admin_data_assistants import (
    VocabularyWizardData, SentenceWizardData, TextWizardData
)
from utils.admin_validation_audit import (
    ComprehensiveValidator, ValidationLevel,
    format_validation_result_for_ui, format_audit_log_for_ui
)


# ============================================================================
# COMPONENTES DE VALIDACIÓN
# ============================================================================

def render_validation_level_selector() -> ValidationLevel:
    """Renderiza selector de nivel de validación"""
    st.subheader("🔍 Nivel de Validación")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        strict = st.radio(
            "Elige el nivel de validación:",
            options=[
                ("🔴 ESTRICTO", "strict"),
                ("🟡 MODERADO", "moderate"),
                ("🟢 FLEXIBLE", "lenient")
            ],
            format_func=lambda x: x[0],
            key="validation_level"
        )
    
    if strict == "strict":
        level = ValidationLevel.STRICT
        help_text = "**ESTRICTO**: Rechaza cualquier duplicado, requiere completitud total"
    elif strict == "moderate":
        level = ValidationLevel.MODERATE
        help_text = "**MODERADO**: Advierte sobre duplicados, requiere campos obligatorios"
    else:
        level = ValidationLevel.LENIENT
        help_text = "**FLEXIBLE**: Solo advierte, permite más flexibilidad"
    
    st.info(help_text)
    
    return level


def render_vocabulary_validation(
    data: Dict[str, Any],
    validator: ComprehensiveValidator,
    show_duplicates: bool = True
) -> Dict[str, Any]:
    """
    Renderiza validación de vocabulario con feedback visual
    
    Returns:
        Dict con 'is_valid', 'result', 'audit_log'
    """
    
    st.divider()
    st.subheader("✅ Validación de Datos")
    
    # Ejecutar validación
    validation_result, audit_log = validator.validate_vocabulary_complete(data)
    formatted_result = format_validation_result_for_ui(validation_result)
    
    # Mostrar estado general
    if formatted_result['valid']:
        st.success(f"{formatted_result['status']}")
    else:
        st.error(f"{formatted_result['status']}")
    
    # Mostrar completitud
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Completitud", formatted_result['completeness_percent'])
    
    with col2:
        # Barra de progreso de completitud
        st.progress(validation_result.completeness_score)
    
    # Mostrar errores
    if formatted_result['errors']:
        st.error("**❌ Errores:**")
        for error in formatted_result['errors']:
            st.write(f"• {error}")
    
    # Mostrar advertencias
    if formatted_result['warnings']:
        st.warning("**⚠️ Advertencias:**")
        for warning in formatted_result['warnings']:
            st.write(f"• {warning}")
    
    # Mostrar sugerencias
    if formatted_result['suggestions']:
        st.info("**💡 Sugerencias:**")
        for suggestion in formatted_result['suggestions']:
            st.write(f"• {suggestion}")
    
    # Mostrar duplicados
    if show_duplicates and formatted_result['has_duplicates']:
        st.warning("**⚠️ DUPLICADOS DETECTADOS:**")
        for dup in formatted_result['duplicates']:
            with st.expander(f"Entrada similar: {dup.get('latin', 'N/A')} (ID: {dup.get('id')})"):
                st.json(dup, expanded=False)
    
    st.divider()
    
    return {
        'is_valid': formatted_result['valid'],
        'result': validation_result,
        'audit_log': audit_log,
        'formatted': formatted_result
    }


def render_sentence_validation(
    data: Dict[str, Any],
    validator: ComprehensiveValidator,
    show_duplicates: bool = True
) -> Dict[str, Any]:
    """
    Renderiza validación de oración con feedback visual
    """
    
    st.divider()
    st.subheader("✅ Validación de Oración")
    
    # Ejecutar validación
    validation_result, audit_log = validator.validate_sentence_complete(data)
    formatted_result = format_validation_result_for_ui(validation_result)
    
    # Mostrar estado general
    if formatted_result['valid']:
        st.success(f"{formatted_result['status']}")
    else:
        st.error(f"{formatted_result['status']}")
    
    # Mostrar completitud
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Completitud", formatted_result['completeness_percent'])
    
    with col2:
        st.progress(validation_result.completeness_score)
    
    # Mostrar errores
    if formatted_result['errors']:
        st.error("**❌ Errores:**")
        for error in formatted_result['errors']:
            st.write(f"• {error}")
    
    # Mostrar advertencias
    if formatted_result['warnings']:
        st.warning("**⚠️ Advertencias:**")
        for warning in formatted_result['warnings']:
            st.write(f"• {warning}")
    
    # Mostrar sugerencias
    if formatted_result['suggestions']:
        st.info("**💡 Sugerencias:**")
        for suggestion in formatted_result['suggestions']:
            st.write(f"• {suggestion}")
    
    # Mostrar duplicados
    if show_duplicates and formatted_result['has_duplicates']:
        st.warning("**⚠️ DUPLICADOS DETECTADOS:**")
        for dup in formatted_result['duplicates']:
            with st.expander(f"Oración similar (ID: {dup.get('id')})"):
                st.json(dup, expanded=False)
    
    st.divider()
    
    return {
        'is_valid': formatted_result['valid'],
        'result': validation_result,
        'audit_log': audit_log,
        'formatted': formatted_result
    }


def render_text_validation(
    data: Dict[str, Any],
    validator: ComprehensiveValidator,
    show_duplicates: bool = True
) -> Dict[str, Any]:
    """
    Renderiza validación de texto con feedback visual
    """
    
    st.divider()
    st.subheader("✅ Validación de Texto")
    
    # Ejecutar validación
    validation_result, audit_log = validator.validate_text_complete(data)
    formatted_result = format_validation_result_for_ui(validation_result)
    
    # Mostrar estado general
    if formatted_result['valid']:
        st.success(f"{formatted_result['status']}")
    else:
        st.error(f"{formatted_result['status']}")
    
    # Mostrar completitud
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Completitud", formatted_result['completeness_percent'])
    
    with col2:
        st.progress(validation_result.completeness_score)
    
    # Mostrar errores
    if formatted_result['errors']:
        st.error("**❌ Errores:**")
        for error in formatted_result['errors']:
            st.write(f"• {error}")
    
    # Mostrar advertencias
    if formatted_result['warnings']:
        st.warning("**⚠️ Advertencias:**")
        for warning in formatted_result['warnings']:
            st.write(f"• {warning}")
    
    # Mostrar sugerencias
    if formatted_result['suggestions']:
        st.info("**💡 Sugerencias:**")
        for suggestion in formatted_result['suggestions']:
            st.write(f"• {suggestion}")
    
    # Mostrar duplicados
    if show_duplicates and formatted_result['has_duplicates']:
        st.warning("**⚠️ DUPLICADOS DETECTADOS:**")
        for dup in formatted_result['duplicates']:
            with st.expander(f"Texto similar: {dup.get('title', 'N/A')} (ID: {dup.get('id')})"):
                st.json(dup, expanded=False)
    
    st.divider()
    
    return {
        'is_valid': formatted_result['valid'],
        'result': validation_result,
        'audit_log': audit_log,
        'formatted': formatted_result
    }


# ============================================================================
# COMPONENTES DE AUDITORÍA
# ============================================================================

def render_audit_log_table(validator: ComprehensiveValidator) -> None:
    """Renderiza tabla de logs de auditoría"""
    
    st.subheader("📋 Registro de Auditoría")
    
    logs = validator.get_audit_logs()
    
    if not logs:
        st.info("No hay registros de auditoría aún")
        return
    
    # Convertir logs para mostrar
    log_data = []
    for log in logs:
        formatted = format_audit_log_for_ui(log)
        log_data.append(formatted)
    
    # Mostrar como tabla
    st.dataframe(
        log_data,
        use_container_width=True,
        hide_index=True,
        column_config={
            'timestamp': st.column_config.TextColumn("Momento"),
            'action': st.column_config.TextColumn("Acción"),
            'user': st.column_config.TextColumn("Usuario"),
            'data_type': st.column_config.TextColumn("Tipo"),
            'status': st.column_config.TextColumn("Estado"),
            'completeness': st.column_config.TextColumn("Completitud"),
        }
    )


def render_audit_log_details(validator: ComprehensiveValidator) -> None:
    """Renderiza detalles detallados de logs de auditoría"""
    
    st.subheader("🔍 Detalles de Auditoría")
    
    logs = validator.get_audit_logs()
    
    if not logs:
        st.info("No hay registros de auditoría")
        return
    
    # Selector de log
    log_descriptions = [
        f"{log.action.value} - {log.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        for log in logs
    ]
    
    selected_idx = st.selectbox(
        "Selecciona un registro para ver detalles:",
        range(len(logs)),
        format_func=lambda i: log_descriptions[i]
    )
    
    log = logs[selected_idx]
    
    # Mostrar detalles
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Acción", log.action.value)
    col2.metric("Usuario", log.user_id)
    col3.metric("Tipo", log.data_type)
    col4.metric("Estado", log.validation_status.upper())
    
    # Mostrar datos
    if log.new_value:
        with st.expander("📝 Datos Cargados"):
            st.json(log.new_value, expanded=False)
    
    # Mostrar errores
    if log.error_message:
        st.error(f"**Errores:** {log.error_message}")
    
    # Mostrar duplicados detectados
    if log.duplicates_found:
        with st.expander("⚠️ Duplicados Detectados"):
            st.json(log.duplicates_found, expanded=False)
    
    # Mostrar completitud
    st.metric(
        "Puntuación de Completitud",
        f"{log.completeness_score * 100:.0f}%"
    )


def render_audit_report_export(validator: ComprehensiveValidator) -> None:
    """Renderiza exportación de reporte de auditoría"""
    
    st.subheader("📊 Exportar Reporte de Auditoría")
    
    format_option = st.radio(
        "Selecciona formato de exportación:",
        options=["json", "csv"],
        horizontal=True
    )
    
    # Generar reporte
    report = validator.export_audit_report(format=format_option)
    
    if report:
        # Botón de descarga
        filename = f"audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format_option}"
        st.download_button(
            label=f"📥 Descargar {format_option.upper()}",
            data=report,
            file_name=filename,
            mime="application/json" if format_option == "json" else "text/csv"
        )
        
        # Mostrar preview
        with st.expander("👁️ Ver Preview del Reporte"):
            if format_option == "json":
                st.json(json.loads(report))
            else:
                st.text(report)
    else:
        st.info("No hay datos para exportar")


# ============================================================================
# COMPONENTES DE CONFIRMACIÓN ANTES DE GUARDAR
# ============================================================================

def render_save_confirmation(
    validation_result: Dict[str, Any],
    data: Dict[str, Any],
    data_type: str = "vocabulary"
) -> bool:
    """
    Renderiza diálogo de confirmación antes de guardar
    
    Returns:
        True si el usuario confirma guardar
    """
    
    st.divider()
    st.subheader("💾 Confirmar Guardado")
    
    # Mostrar resumen de lo que se va a guardar
    col1, col2 = st.columns(2)
    
    with col1:
        if not validation_result['is_valid']:
            st.error(
                "**⚠️ Hay errores en los datos. ¿Deseas guardar de todas formas?**"
            )
        else:
            st.success("**✅ Datos válidos. Listo para guardar.**")
    
    with col2:
        st.metric("Completitud", validation_result['formatted']['completeness_percent'])
    
    # Mostrar datos a guardar
    with st.expander("📋 Ver datos a guardar"):
        st.json(data, expanded=False)
    
    # Botones de acción
    col_confirm, col_cancel = st.columns(2)
    
    confirmed = False
    with col_confirm:
        if validation_result['is_valid']:
            confirmed = st.button(
                "✅ Guardar Datos",
                key="confirm_save",
                type="primary"
            )
        else:
            # Checkbox para confirmar incluso con errores
            user_confirms_errors = st.checkbox(
                "He revisado los errores y deseo continuar de todas formas"
            )
            if user_confirms_errors:
                confirmed = st.button(
                    "✅ Guardar Datos (con errores)",
                    key="confirm_save_with_errors"
                )
    
    with col_cancel:
        if st.button("❌ Cancelar", key="cancel_save"):
            st.info("Guardado cancelado")
            return False
    
    return confirmed


def render_save_success_message(
    data_type: str,
    data_id: Optional[int] = None
) -> None:
    """Renderiza mensaje de éxito después de guardar"""
    
    success_messages = {
        'vocabulary': "✅ Palabra guardada exitosamente en la BD",
        'sentence': "✅ Oración guardada exitosamente en la BD",
        'text': "✅ Texto guardado exitosamente en la BD",
    }
    
    message = success_messages.get(data_type, "✅ Datos guardados exitosamente")
    
    if data_id:
        message += f" (ID: {data_id})"
    
    st.success(message)
    st.balloons()


# ============================================================================
# HELPER PARA INICIALIZAR VALIDADOR EN SESSION_STATE
# ============================================================================

def init_validator(validation_level: ValidationLevel) -> ComprehensiveValidator:
    """
    Inicializa validador en session_state si no existe
    
    Returns:
        ComprehensiveValidator instance
    """
    
    if 'comprehensive_validator' not in st.session_state:
        st.session_state.comprehensive_validator = ComprehensiveValidator(
            level=validation_level,
            user_id="admin_user"  # Se podría obtener del contexto de autenticación
        )
    
    return st.session_state.comprehensive_validator


__all__ = [
    'render_validation_level_selector',
    'render_vocabulary_validation',
    'render_sentence_validation',
    'render_text_validation',
    'render_audit_log_table',
    'render_audit_log_details',
    'render_audit_report_export',
    'render_save_confirmation',
    'render_save_success_message',
    'init_validator',
]
