import streamlit as st
from database.connection import get_session, engine
from database import Word, InflectedForm
from sqlmodel import select, func
from utils.latin_logic import LatinMorphology
from utils.i18n import get_text
from utils.ui_helpers import load_css
from utils.text_utils import normalize_latin


def render_content():
    # Page config
    
    st.title("📖 Diccionario Latino-Español")
    st.markdown("*Basado en datos de Collatinus © Yves Ouvrard & Philippe Verkerk*")
    
    
    morphology = LatinMorphology()
    
    # Search interface
    st.markdown("### Buscar palabra latina")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input(
            "Introduce una palabra en latín",
            placeholder="amo, puella, dominus...",
            label_visibility="collapsed"
        )
    
    with col2:
        search_mode = st.selectbox(
            "Modo",
            ["Exacto", "Contiene"],
            label_visibility="collapsed"
        )
    
    if search_term:
        # Normalize search term
        search_normalized = normalize_latin(search_term.strip().lower())
        
        with get_session() as session:
            # Search in database
            if search_mode == "Exacto":
                results = session.exec(
                    select(Word).where(Word.latin == search_normalized)
                ).all()
            else:
                results = session.exec(
                    select(Word).where(Word.latin.contains(search_normalized)).limit(50)
                ).all()
            
            # Display results
            if results:
                st.success(f"Se encontraron {len(results)} resultado(s)")
                
                for word in results:
                    pos_translated = get_text(word.part_of_speech, st.session_state.get('language', 'es'))
                    with st.expander(f"**{word.latin}** — {pos_translated}", expanded=len(results)==1):
                        # Spanish definition (preferido)
                        if word.definition_es:
                            st.markdown(f"**📖 Definición:** {word.definition_es}")
                        elif word.translation:
                            # Fallback (puede estar en inglés en datos legacy)
                            st.markdown(f"**Traducción:** {word.translation}")
                        
                        # Admin edit button
                        if st.button("✏️ Editar en Panel Admin", key=f"edit_{word.id}", width="stretch"):
                            # Store word ID in session state for editing
                            st.session_state.word_to_edit = word.id
                            st.switch_page("pages/99_⚙️_Administracion.py")
                        st.markdown("---")
                        
                        # Morphological information
                        col_a, col_b, col_c = st.columns(3)
                        
                        with col_a:
                            if word.part_of_speech == 'noun' and word.genitive:
                                st.markdown(f"**Genitivo:** {word.genitive}")
                            if word.part_of_speech == 'verb' and word.principal_parts:
                                st.markdown(f"**💡 Partes principales:**")
                                parts = word.principal_parts.split(',')
                                for i, part in enumerate(parts[:4]):
                                    st.text(f"  {i+1}. {part.strip()}")
                        
                        with col_b:
                            if word.gender:
                                gender_map = {'m': 'masculino', 'f': 'femenino', 'n': 'neutro', 'm/f': 'masc./fem.'}
                                st.markdown(f"**Género:** {gender_map.get(word.gender, word.gender)}")
                            if word.declension:
                                st.markdown(f"**Declinación:** {word.declension}ª")
                            if word.conjugation:
                                st.markdown(f"**Conjugación:** {word.conjugation}ª")
                        
                        with col_c:
                            if word.level:
                                st.markdown(f"**Nivel:** {word.level}")
                            if word.author_id:
                                st.markdown(f"**📚 Autor clásico**")
                        
                        # Collatinus metadata
                        if word.collatinus_model:
                            st.caption(f"Modelo de flexión: {word.collatinus_model}")
                        
                        # Show some inflected forms if it's a noun or verb
                        if word.part_of_speech == 'noun' and word.declension and word.gender:
                            with st.container():
                                st.markdown("**Formas declinadas (nominativo y genitivo):**")
                                try:
                                    forms = morphology.decline_noun(
                                        word.latin, 
                                        word.declension, 
                                        word.gender, 
                                        word.genitive or '',
                                        parisyllabic=word.parisyllabic,
                                        is_plurale_tantum=word.is_plurale_tantum,
                                        is_singulare_tantum=word.is_singulare_tantum
                                    )
    
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.text(f"Nom. Sg: {forms.get('nom_sg', '-')}")
                                        st.text(f"Gen. Sg: {forms.get('gen_sg', '-')}")
                                    with col2:
                                        st.text(f"Nom. Pl: {forms.get('nom_pl', '-')}")
                                        st.text(f"Gen. Pl: {forms.get('gen_pl', '-')}")
                                except Exception as e:
                                    st.caption(f"(No se pudieron generar formas declinadas)")
            else:
                st.warning("No se encontraron resultados")
                st.info("💡 **Sugerencia:** Intenta buscar sin macrones (á → a, ē → e)")
    
    load_css()
    
    # Browse by category
    st.markdown("---")
    st.markdown("### Explorar por categoría")
    
    with get_session() as session:
        # Get counts by part of speech
        all_words = session.exec(select(Word)).all()
        pos_counts = {}
        for word in all_words:
            pos = word.part_of_speech or 'unknown'
            pos_counts[pos] = pos_counts.get(pos, 0) + 1
        
        # Display categories
        pos_spanish = {
            'noun': 'Sustantivos',
            'verb': 'Verbos',
            'adjective': 'Adjetivos',
            'adverb': 'Adverbios',
            'preposition': 'Preposiciones',
            'conjunction': 'Conjunciones',
            'pronoun': 'Pronombres',
            'interjection': 'Interjecciones'
        }
        
        # Create rows of 4
        items = list(pos_spanish.items())
        for i in range(0, len(items), 4):
            cols = st.columns(4)
            for j in range(4):
                if i + j < len(items):
                    pos, label = items[i + j]
                    count = pos_counts.get(pos, 0)
                    
                    with cols[j]:
                        st.markdown(
                            f"""
                            <div class="stat-box">
                                <div class="stat-value">{count}</div>
                                <div class="stat-label">{label}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
    
    # Footer with attribution
    st.markdown("---")
    st.caption("""
    **Atribución:** Datos léxicos de [Collatinus](https://github.com/biblissima/collatinus) 
    © Yves Ouvrard & Philippe Verkerk — Licencia GPL v3
    """)
