import streamlit as st
from sqlmodel import Session, create_engine, select, func
from database import Word
from utils.latin_logic import LatinMorphology


def render_content():
    
    st.title("📜 Scriptorium")
    st.markdown("""
    **Bienvenido al Taller de Palabras.**
    Aquí puedes ayudar a "rescatar" palabras del reservorio completando su información morfológica.
    Una vez completadas, estas palabras estarán disponibles en los ejercicios.
    """)
    
    # Initialize database
    @st.cache_resource
    def get_engine():
        return create_engine("sqlite:///lingua_latina.db")
    
    engine = get_engine()
    
    def get_reservoir_stats():
        with Session(engine) as session:
            total = session.exec(select(func.count(Word.id))).one()
            reservoir = session.exec(select(func.count(Word.id)).where(Word.status == 'reservoir')).one()
            active = session.exec(select(func.count(Word.id)).where(Word.status == 'active')).one()
            return total, reservoir, active
    
    def get_random_reservoir_word():
        with Session(engine) as session:
            # Prioritize nouns and verbs
            word = session.exec(
                select(Word)
                .where(Word.status == 'reservoir')
                .order_by(func.random())
            ).first()
            return word
    
    # Sidebar stats
    total, reservoir, active = get_reservoir_stats()
    st.sidebar.metric("Palabras Activas", active)
    st.sidebar.metric("En Reservorio", reservoir)
    if total > 0:
        progress = active / total
        st.sidebar.progress(progress, text=f"Progreso: {progress:.1%}")
    
    # Main interface
    if "current_word_id" not in st.session_state:
        st.session_state.current_word_id = None
    
    # Load word
    if st.button("🔍 Obtener palabra del reservorio") or st.session_state.current_word_id is None:
        word = get_random_reservoir_word()
        if word:
            st.session_state.current_word_id = word.id
        else:
            st.session_state.current_word_id = None
            st.success("¡El reservorio está vacío! Todas las palabras han sido rescatadas.")
    
    if st.session_state.current_word_id:
        with Session(engine) as session:
            word = session.get(Word, st.session_state.current_word_id)
            
            if word:
                st.markdown("---")
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.subheader(word.latin)
                    st.caption(f"Tipo: {word.part_of_speech}")
                    st.info(f"**Definición:** {word.definition_es or word.translation}")
                    if word.collatinus_model:
                        st.text(f"Modelo Collatinus: {word.collatinus_model}")
                
                with col2:
                    st.subheader("📝 Completar Información")
                    
                    with st.form("edit_word_form"):
                        new_status = "active"
                        
                        if word.part_of_speech == 'noun':
                            st.markdown("### Datos de Sustantivo")
                            col_a, col_b = st.columns(2)
                            with col_a:
                                declension = st.selectbox(
                                    "Declinación", 
                                    ["1", "2", "3", "4", "5"],
                                    index=["1", "2", "3", "4", "5"].index(word.declension) if word.declension in ["1", "2", "3", "4", "5"] else 0
                                )
                                gender = st.selectbox(
                                    "Género",
                                    ["m", "f", "n", "m/f"],
                                    index=["m", "f", "n", "m/f"].index(word.gender) if word.gender in ["m", "f", "n", "m/f"] else 0
                                )
                            with col_b:
                                genitive = st.text_input("Genitivo", value=word.genitive or "")
                                
                        elif word.part_of_speech == 'verb':
                            st.markdown("### Datos de Verbo")
                            conjugation = st.selectbox(
                                "Conjugación",
                                ["1", "2", "3", "3-io", "4", "irreg"],
                                index=["1", "2", "3", "3-io", "4", "irreg"].index(word.conjugation) if word.conjugation in ["1", "2", "3", "3-io", "4", "irreg"] else 0
                            )
                            principal_parts = st.text_input(
                                "Partes Principales (separadas por coma)", 
                                value=word.principal_parts or "",
                                help="Ej: amo, amare, amavi, amatum"
                            )
                            
                        elif word.part_of_speech == 'adjective':
                            st.markdown("### Datos de Adjetivo")
                            declension = st.selectbox(
                                "Declinación",
                                ["1/2", "3"],
                                index=["1/2", "3"].index(word.declension) if word.declension in ["1/2", "3"] else 0
                            )
                        
                        else:
                            st.warning(f"Tipo de palabra '{word.part_of_speech}' no requiere edición compleja.")
                        
                        submitted = st.form_submit_button("💾 Guardar y Promover")
                        
                        if submitted:
                            # Update word
                            if word.part_of_speech == 'noun':
                                word.declension = declension
                                word.gender = gender
                                word.genitive = genitive
                            elif word.part_of_speech == 'verb':
                                word.conjugation = conjugation
                                word.principal_parts = principal_parts
                            elif word.part_of_speech == 'adjective':
                                word.declension = declension
                            
                            word.status = 'active'
                            session.add(word)
                            session.commit()
                            st.success(f"¡Palabra '{word.latin}' rescatada exitosamente!")
                            st.session_state.current_word_id = None # Reset to load new word
                            st.rerun()
    
                # Show raw data for debugging
                with st.expander("Ver datos crudos"):
                    st.json({
                        "id": word.id,
                        "latin": word.latin,
                        "status": word.status,
                        "collatinus_model": word.collatinus_model
                    })
