"""
Authentication helper functions for Lingua Latina Viva.
Provides centralized authentication checks for admin-restricted features.
"""

import streamlit as st


def is_admin_authenticated():
    """
    Check if current user is authenticated as admin.
    
    Returns:
        bool: True if user has admin privileges, False otherwise.
    """
    return st.session_state.get('is_admin', False)


def require_admin(message="Esta función requiere permisos de administrador."):
    """
    Enforce admin authentication. Stops execution if user is not admin.
    
    Args:
        message (str): Warning message to display to non-admin users.
        
    Raises:
        st.stop: Halts execution if user is not authenticated as admin.
    """
    if not is_admin_authenticated():
        st.warning(message)
        st.info("💡 **Sugerencia:** Accede al [Panel de Administración](../99_⚙️_Administracion) para obtener privilegios de admin.")
        st.stop()


def render_admin_login_compact():
    """
    Render a compact admin login interface in sidebar.
    Allows quick authentication without leaving current page.
    
    Returns:
        bool: True if login was successful, False otherwise.
    """
    if is_admin_authenticated():
        st.sidebar.success("🔓 Sesión de Admin activa")
        if st.sidebar.button("🔒 Cerrar Sesión Admin"):
            st.session_state.is_admin = False
            st.rerun()
        return True
    else:
        with st.sidebar.expander("🔐 Login Admin"):
            password = st.text_input(
                "Contraseña",
                type="password",
                key="admin_login_compact"
            )
            if st.button("Ingresar", key="admin_submit_compact"):
                if password == "admin123":  # TODO: Use secure authentication
                    st.session_state.is_admin = True
                    st.rerun()
                    return True
                else:
                    st.error("Contraseña incorrecta")
                    return False
        return False


def get_admin_badge():
    """
    Get a visual badge/indicator for admin status.
    
    Returns:
        str: HTML badge to display admin status.
    """
    if is_admin_authenticated():
        return "🔓 **Admin**"
    else:
        return "🔒 Usuario"
