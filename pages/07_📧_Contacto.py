import streamlit as st
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.connection import get_session
from database import Feedback
from utils.ui_helpers import load_css
from utils.ui import render_sidebar_footer

def main():
    st.set_page_config(
        page_title="Contacto - Lingua Latina Viva",
        page_icon="📧",
        layout="centered"
    )
    
    load_css()
    from utils.ui_helpers import render_sidebar_config
    render_sidebar_config()
    
    st.markdown(
        """
        <h1 style='text-align: center; font-family: "Cinzel", serif;'>
            📧 Contacto & Feedback
        </h1>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("""
    ¡Nos encantaría saber de ti! Ya sea que hayas encontrado un error, tengas una sugerencia para mejorar la aplicación, 
    o simplemente quieras compartir tu experiencia aprendiendo latín, tus comentarios son invaluables para nosotros.
    """)
    
    st.info("📧 También puedes escribirnos directamente a: **lengualatinaviva@gmail.com**")
    
    st.markdown("---")
    
    with st.form("feedback_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Nombre", placeholder="Tu nombre")
        
        with col2:
            email = st.text_input("Correo Electrónico", placeholder="tucorreo@ejemplo.com")
            
        feedback_type = st.selectbox(
            "Tipo de Mensaje",
            options=["general", "bug", "feature_request", "content_issue"],
            format_func=lambda x: {
                "general": "📝 Comentario General",
                "bug": "🐛 Reportar un Error",
                "feature_request": "💡 Sugerencia de Funcionalidad",
                "content_issue": "📖 Error en Contenido (Latín)"
            }.get(x, x)
        )
        
        message = st.text_area("Mensaje", height=150, placeholder="Escribe tu mensaje aquí...")
        
        submitted = st.form_submit_button("Enviar Mensaje", type="primary", width="stretch")
        
        if submitted:
            if not name or not email or not message:
                st.error("Por favor, completa todos los campos obligatorios.")
            else:
                try:
                    with get_session() as session:
                        feedback = Feedback(
                            name=name,
                            email=email,
                            message=message,
                            feedback_type=feedback_type,
                            created_at=datetime.utcnow()
                        )
                        session.add(feedback)
                        session.commit()
                        
                    st.success("¡Gracias por tu mensaje! Lo hemos recibido correctamente.")
                    st.balloons()
                except Exception as e:
                    st.error(f"Hubo un error al enviar tu mensaje: {str(e)}")

    render_sidebar_footer()

if __name__ == "__main__":
    main()
