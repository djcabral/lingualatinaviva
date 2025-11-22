import streamlit as st

def render_sidebar_footer():
    """
    Renders the footer in the sidebar with the 'Buy Me a Coffee' button.
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        <div style="text-align: center;">
            <p style="font-size: 0.9em; color: #666;">
                ¿Te gusta Lingua Latina Viva?
            </p>
            <a href="https://www.buymeacoffee.com/tu_usuario" target="_blank">
                <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 40px !important;width: 145px !important;" >
            </a>
            <p style="font-size: 0.8em; color: #888; margin-top: 10px;">
                Ayuda a mantener el servidor activo.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
