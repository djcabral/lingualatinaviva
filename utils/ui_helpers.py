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

def render_sidebar_config():
    """
    Renderiza la configuración global en el sidebar (parte superior).
    Debe ser llamada al inicio de cada página.
    """
    st.sidebar.markdown("### ⚙️ Configuración")
    
    # Get current font size from session state or DB
    from database.connection import get_session
    from database import UserProfile
    from sqlmodel import select
    import json
    
    current_size = 1.0
    
    # Try to get from session state first (faster)
    if 'global_font_size' in st.session_state:
        current_size = st.session_state.global_font_size
    else:
        # Fallback to DB
        try:
            with get_session() as session:
                user = session.exec(select(UserProfile)).first()
                if user and user.preferences_json:
                    prefs = json.loads(user.preferences_json)
                    current_size = prefs.get('global_font_size', 1.0)
                    st.session_state.global_font_size = current_size
        except:
            pass
    
    new_font_size = st.sidebar.slider(
        "Tamaño de letra",
        min_value=0.8,
        max_value=1.5,
        value=float(current_size),
        step=0.1,
        help="Ajusta el tamaño de toda la letra en la aplicación",
        key="global_font_size_slider_top"
    )
    
    # Save if changed
    if new_font_size != current_size:
        st.session_state.global_font_size = new_font_size
        try:
            with get_session() as save_session:
                user = save_session.exec(select(UserProfile)).first()
                if user:
                    prefs = {}
                    if user.preferences_json:
                        try:
                            prefs = json.loads(user.preferences_json)
                        except:
                            pass
                    prefs['global_font_size'] = new_font_size
                    user.preferences_json = json.dumps(prefs)
                    save_session.add(user)
                    save_session.commit()
        except:
            pass
        st.rerun()
    
    # Apply global font size CSS
    st.markdown(f"""
    <style>
        /* Global font size control */
        html, body, [class*="css"] {{
            font-size: {new_font_size}rem !important;
        }}
        
        /* Preserve original vocabulary card sizes - do NOT scale with global font */
        .vocab-latin {{
            font-size: 3.5em !important;
        }}
        .vocab-translation {{
            font-size: 1.8em !important;
        }}
        .vocab-pos {{
            font-size: 1.1em !important;
        }}
        
        /* Ensure headers scale proportionally but less aggressively */
        h1 {{ font-size: {max(1.8, new_font_size * 1.8)}rem !important; }}
        h2 {{ font-size: {max(1.5, new_font_size * 1.5)}rem !important; }}
        h3 {{ font-size: {max(1.3, new_font_size * 1.3)}rem !important; }}
        h4 {{ font-size: {max(1.2, new_font_size * 1.2)}rem !important; }}
        h5 {{ font-size: {max(1.1, new_font_size * 1.1)}rem !important; }}
        h6 {{ font-size: {max(1.0, new_font_size * 1.0)}rem !important; }}
        
        /* Sidebar specific adjustments to prevent overflow */
        [data-testid="stSidebar"] h1 {{ font-size: {max(1.5, new_font_size * 1.5)}rem !important; }}
        [data-testid="stSidebar"] h2 {{ font-size: {max(1.3, new_font_size * 1.3)}rem !important; }}
        [data-testid="stSidebar"] h3 {{ font-size: {max(1.2, new_font_size * 1.2)}rem !important; }}
        
        /* Streamlit specific elements */
        .stMarkdown, .stText, p, div:not(.vocab-latin):not(.vocab-translation):not(.vocab-pos), span {{
            font-size: inherit !important;
        }}
        
        /* Fix for specific components that might break */
        .stButton button {{
            font-size: {new_font_size}rem !important;
        }}
    </style>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("---")
