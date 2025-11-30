"""
UI Helper Functions
Funciones compartidas para la interfaz de usuario de Streamlit.
"""
import streamlit as st
import os


def load_css():
    """
    Carga los estilos CSS personalizados de la aplicación.
    Esta función debe ser llamada en cada página Streamlit.
    """
    # Buscar el archivo CSS desde la raíz del proyecto
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "style.css")
    
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        # Fallback: buscar desde el directorio actual
        alt_css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")
        if os.path.exists(alt_css_path):
            with open(alt_css_path) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def render_page_header(title: str, icon: str = "📜"):
    """
    Renderiza un encabezado de página consistente.
    
    Args:
        title: Título de la página
        icon: Emoji o icono para mostrar junto al título
    """
    st.markdown(
        f"""
        <h1 style='text-align: center; font-family: "Cinzel", serif;'>
            {icon} {title}
        </h1>
        """,
        unsafe_allow_html=True
    )


def render_stat_box(label: str, value, help_text: str = None):
    """
    Renderiza una caja de estadística estilizada.
    
    Args:
        label: Etiqueta de la estadística
        value: Valor a mostrar (número o texto)
        help_text: Texto de ayuda opcional
    """
    help_html = f'<div class="stat-help">{help_text}</div>' if help_text else ''
    
    st.markdown(
        f"""
        <div class="stat-box">
            <div class="stat-value">{value}</div>
            <div class="stat-label">{label}</div>
            {help_html}
        </div>
        """,
        unsafe_allow_html=True
    )


def get_session_defaults():
    """
    Inicializa valores por defecto en st.session_state.
    Debe ser llamada al inicio de cada página.
    """
    if 'language' not in st.session_state:
        st.session_state.language = 'es'


def render_sidebar_footer():
    """
    Renderiza el footer del sidebar con información y enlaces.
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        <div style='text-align: center; font-size: 0.8em; color: #888;'>
            <p>📜 Lingua Latina Viva</p>
            <p style='font-size: 0.9em;'>Una aplicación para el aprendizaje del latín clásico</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Dev Reminder
    with st.sidebar.expander("🛠️ Estado del Proyecto", expanded=False):
        st.info("🎨 **Imágenes IA**: La cuota se renueva cada 4 horas. ¡Recuerda solicitar nuevas ilustraciones!")


def show_success_with_xp(message: str, xp_gained: int = 0):
    """
    Muestra un mensaje de éxito con puntos de experiencia ganados.
    
    Args:
        message: Mensaje a mostrar
        xp_gained: Cantidad de XP ganados
    """
    if xp_gained > 0:
        st.success(f"{message} 🎉 +{xp_gained} XP")
    else:
        st.success(message)


def confirm_action(action_name: str, warning_message: str = None) -> bool:
    """
    Solicita confirmación del usuario antes de realizar una acción.
    
    Args:
        action_name: Nombre de la acción a confirmar
        warning_message: Mensaje de advertencia opcional
        
    Returns:
        True si el usuario confirma, False en caso contrario
    """
    if warning_message:
        st.warning(warning_message)
    
    confirmation = st.checkbox(f"Confirmo que quiero {action_name}", key=f"confirm_{action_name}")
    return confirmation


def show_loading_spinner(message: str = "Procesando..."):
    """
    Contexto para mostrar un spinner de carga.
    
    Uso:
        with show_loading_spinner("Cargando datos..."):
            # código que toma tiempo
    """
    return st.spinner(message)


def render_styled_table(headers: list, rows: list):
    """
    Renderiza una tabla HTML estilizada con la clase .pretty-table.
    
    Args:
        headers: Lista de strings con los encabezados
        rows: Lista de listas con los datos de las filas
    """
    html = '<table class="pretty-table">'
    
    # Header
    html += '<thead><tr>'
    for header in headers:
        html += f'<th>{header}</th>'
    html += '</tr></thead>'
    
    # Body
    html += '<tbody>'
    for row in rows:
        html += '<tr>'
        for cell in row:
            # Detectar si es markdown (negrita, cursiva) y convertirlo a HTML básico si es necesario
            # Por ahora asumimos texto plano o HTML seguro
            cell_str = str(cell)
            if "**" in cell_str:
                cell_str = cell_str.replace("**", "<b>", 1).replace("**", "</b>", 1)
            if "*" in cell_str:
                cell_str = cell_str.replace("*", "<i>", 1).replace("*", "</i>", 1)
                
            html += f'<td>{cell_str}</td>'
        html += '</tr>'
    html += '</tbody>'
    
    html += '</table>'
    
    st.markdown(html, unsafe_allow_html=True)

