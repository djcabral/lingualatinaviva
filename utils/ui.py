import streamlit as st

def render_sidebar_footer():
    """
    Renders the footer in the sidebar with the 'Buy Me a Coffee' button.
    """
    st.sidebar.markdown("---")
    
    # Fetch contact email from DB
    from database.connection import get_session
    from database import SystemSetting
    from sqlmodel import select
    
    contact_email = "lengualatinaviva@gmail.com" # Default fallback
    try:
        with get_session() as session:
            setting = session.get(SystemSetting, "contact_email")
            if setting:
                contact_email = setting.value
    except Exception:
        pass # Fail silently to default if DB error
    
    # Global font size control moved to top of sidebar (utils/ui_helpers.py)
    
    st.sidebar.markdown(
        f"""
        <div style="text-align: center;">
            <p style="font-size: 0.9em; color: #666;">
                ¿Te gusta Lingua Latina Viva?
            </p>
            <a href="https://www.buymeacoffee.com/djcabralc" target="_blank">
                <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 40px !important;width: 145px !important;" >
            </a>
            <p style="font-size: 0.8em; color: #888; margin-top: 10px;">
                Ayuda a mantener el servidor activo.
            </p>
            <p style="font-size: 0.8em; color: #888; margin-top: 5px;">
                📧 <a href="mailto:{contact_email}" style="color: #888; text-decoration: none;">{contact_email}</a>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Dev Reminder
    with st.sidebar.expander("🛠️ Estado del Proyecto", expanded=True):
        st.caption("Recordatorio para el Desarrollador")
        st.info("🎨 **Imágenes IA**: La cuota se renueva cada 4 horas. ¡Recuerda solicitar nuevas ilustraciones!")
