import streamlit as st
import json
import pandas as pd
from sqlalchemy.orm import selectinload
from sqlmodel import select
from database.connection import get_session
from database import SentenceAnalysis, SyntaxCategory, TokenAnnotation, SentenceStructure
from utils.ui_helpers import load_css
from utils.auth_helpers import is_admin_authenticated, render_admin_login_compact


def count_role_changes(current_roles, new_role_map):
    """
    Count number of changed role assignments.
    
    Args:
        current_roles: Current syntax_roles dict {role: [token_ids]}
        new_role_map: New mapping dict {token_id: role}
        
    Returns:
        int: Number of tokens with changed roles
    """
    # Build reverse map of current roles
    current_map = {}
    if current_roles:
        for role, ids in current_roles.items():
            for tid in ids:
                current_map[tid] = role
    
    changes = 0
    for tid, new_role in new_role_map.items():
        old_role = current_map.get(tid, "")
        if old_role != new_role:
            changes += 1
    
    return changes


def save_to_edit_history(sentence_id, syntax_roles):
    """
    Save current state to edit history for undo functionality.
    
    Args:
        sentence_id: ID of the sentence
        syntax_roles: Current syntax_roles JSON string
    """
    if 'syntax_edit_history' not in st.session_state:
        st.session_state.syntax_edit_history = []
    
    # Limit history to last 10 changes
    if len(st.session_state.syntax_edit_history) >= 10:
        st.session_state.syntax_edit_history.pop(0)
    
    st.session_state.syntax_edit_history.append({
        'sentence_id': sentence_id,
        'syntax_roles': syntax_roles,
        'timestamp': pd.Timestamp.now()
    })


def undo_last_change():
    """
    Restore previous syntax_roles from history.
    
    Returns:
        bool: True if undo successful, False if no history
    """
    if 'syntax_edit_history' not in st.session_state or len(st.session_state.syntax_edit_history) == 0:
        return False
    
    last_state = st.session_state.syntax_edit_history.pop()
    
    try:
        with get_session() as session:
            db_sent = session.get(SentenceAnalysis, last_state['sentence_id'])
            if db_sent:
                db_sent.syntax_roles = last_state['syntax_roles']
                session.add(db_sent)
                session.commit()
                return True
    except Exception as e:
        st.error(f"Error al deshacer: {e}")
        return False


def render_content():
    
    # Custom CSS for syntax highlighting
    st.markdown("""
        <style>
            .syntax-token {
                display: inline-block;
                padding: 4px 8px;
                margin: 2px;
                border-radius: 4px;
                cursor: help;
                font-family: 'Cardo', serif;
                font-size: 1.1em;
            }
            .role-subject { background-color: #FF6B6B; color: white; }
            .role-predicate { background-color: #4ECDC4; color: white; }
            .role-direct_object { background-color: #95E1D3; color: #333; }
            .role-indirect_object { background-color: #FFE66D; color: #333; }
            .role-complement { background-color: #A8E6CF; color: #333; }
            .role-attribute { background-color: #C7CEEA; color: #333; }
            .role-apposition { background-color: #FF9FF3; color: white; }
            
            .legend-item {
                display: inline-block;
                padding: 2px 6px;
                border-radius: 3px;
                margin-right: 10px;
                font-size: 0.9em;
            }
            .role-none { background-color: #E0E0E0; color: #333; border: 1px solid #CCC; } /* Default style */
        </style>
        """, unsafe_allow_html=True)
    
    load_css()
    
    st.title("📐 Syntaxis - Tesauro de Oraciones")
    st.markdown("Explora construcciones gramaticales desde lo simple a lo complejo.")
    
    # --- Sidebar Filters ---
    with st.sidebar:
        st.header("Filtros")
        
        # Level Filter
        min_level, max_level = st.slider("Nivel de Complejidad", 1, 10, (1, 10))
        
        # Source Filter
        with get_session() as session:
            sources = session.exec(select(SentenceAnalysis.source).distinct()).all()
            # Clean sources for display
            unique_sources = sorted(list(set([s.split('_')[0] for s in sources if s])))
        
        selected_source = st.multiselect("Fuente", unique_sources, default=unique_sources)
        
        # Construction Filter
        constructions = [
            "ablative_absolute", "accusative_infinitive", "dative_possession"
        ]
        selected_constructions = st.multiselect("Construcciones Especiales", constructions)
        
        
        st.markdown("---")
        # View Mode (User Request: Selectivity)
        view_mode = st.radio(
            "Modo de Visualización",
            ["📚 Corpus Verificado", "🚧 Zona de Espera"],
            help="Verificado: Solo oraciones 100% analizadas. Zona de Espera: Oraciones pendientes de revisión."
        )
        
        st.markdown("---")
        
        # Admin login interface (compact)
        render_admin_login_compact()
        
        # Editor mode - Admin only
        if is_admin_authenticated():
            st.checkbox(
                "✏️ Modo Editor", 
                key="editor_mode", 
                help="Activa herramientas para corregir etiquetas sintácticas."
            )
            if st.session_state.get("editor_mode", False):
                st.success("🔓 Modo administrador activo - puedes editar etiquetas")
        else:
            st.caption("🔒 **Modo Editor** disponible solo para administradores")
            st.caption("_Inicia sesión arriba para activar herramientas de edición_")
    
    # --- Main Content ---
    
    def get_sentences(min_l, max_l, sources_list, constr_list):
        with get_session() as session:
            query = select(SentenceAnalysis).options(
                selectinload(SentenceAnalysis.token_annotations),
                selectinload(SentenceAnalysis.structures)
            ).where(
                SentenceAnalysis.complexity_level >= min_l,
                SentenceAnalysis.complexity_level <= max_l
            )
            
            # Filter for completeness (User Request)
            # query = query.where(SentenceAnalysis.tree_diagram_svg != None) # Relaxed for manual seed
            query = query.where(SentenceAnalysis.dependency_json != "[]")
            
            results = session.exec(query).all()
            
            # Filter in python for complex logic
            filtered = []
            for s in results:
                # Source check
                src_match = False
                if not sources_list:
                    src_match = True
                else:
                    for src in sources_list:
                        if src in s.source:
                            src_match = True
                            break
                
                # Construction check
                constr_match = True
                if constr_list:
                    if not s.constructions:
                        constr_match = False
                    else:
                        s_constr = json.loads(s.constructions)
                        for c in constr_list:
                            if c not in s_constr:
                                constr_match = False
                                break
                
                if src_match and constr_match:
                    # Convert to dict to avoid DetachedInstanceError
                    sent_dict = {
                        'id': s.id,
                        'latin_text': s.latin_text,
                        'spanish_translation': s.spanish_translation,
                        'complexity_level': s.complexity_level,
                        'sentence_type': s.sentence_type,
                        'source': s.source,
                        'lesson_number': s.lesson_number,
                        'dependency_json': s.dependency_json,
                        'syntax_roles': s.syntax_roles,
                        'tree_diagram_svg': s.tree_diagram_svg,
                        'constructions': s.constructions,
                        'token_annotations': [
                            {
                                'token_index': ann.token_index,
                                'pedagogical_role': ann.pedagogical_role,
                                'case_function': ann.case_function,
                                'explanation': ann.explanation
                            }
                            for ann in s.token_annotations
                        ] if s.token_annotations else [],
                        'structures': [
                            {
                                'clause_type': struct.clause_type,
                                'notes': struct.notes
                            }
                            for struct in s.structures
                        ] if s.structures else []
                    }
                    filtered.append(sent_dict)
                    
            return filtered
    
    def is_sentence_complete(sentence):
        """Check if sentence has annotations for ALL tokens."""
        try:
            deps = json.loads(sentence['dependency_json'])
            n_tokens = len(deps)
            n_anns = len(sentence['token_annotations'])
            
            # 1. Coverage check
            if n_tokens != n_anns:
                return False
                
            # 2. Quality check (User Request: Strictness)
            # If any annotation is auto-generated, it's not ready for public view
            for ann in sentence['token_annotations']:
                if ann['explanation'] and "Generado automáticamente" in ann['explanation']:
                    return False
                    
            return True
        except:
            return False
    
    # Apply View Mode Filter
    raw_sentences = get_sentences(min_level, max_level, selected_source, selected_constructions)
    sentences = []
    
    if view_mode == "📚 Corpus Verificado":
        sentences = [s for s in raw_sentences if is_sentence_complete(s)]
    else:
        # Zona de Espera: Incomplete sentences
        sentences = [s for s in raw_sentences if not is_sentence_complete(s)]
    
    if view_mode == "📚 Corpus Verificado":
        st.success(f"Mostrando {len(sentences)} oraciones verificadas (100% analizadas)")
    else:
        st.warning(f"Mostrando {len(sentences)} oraciones en zona de espera (análisis incompleto)")
    
    # --- Visualization Helpers ---
    
    POS_TRANSLATIONS = {
        "NOUN": "Sustantivo",
        "VERB": "Verbo",
        "ADJ": "Adjetivo",
        "ADV": "Adverbio",
        "PRON": "Pronombre",
        "DET": "Determinante",
        "ADP": "Preposición",
        "CCONJ": "Conjunción Coordinante",  # Más claro que "Conj. Coord."
        "SCONJ": "Conjunción Subordinante",  # Más claro que "Conj. Subord."
        "NUM": "Número",  # Más claro que "Numeral"
        "PART": "Partícula",
        "INTJ": "Interjección",
        "PROPN": "Nombre Propio",
        "AUX": "Verbo Auxiliar",  # Más claro que "Auxiliar"
        "PUNCT": "Puntuación",
        "X": "Otro"
    }
    
    MORPH_TRANSLATIONS = {
        # Categorías gramaticales (Keys)
        "Case": "Caso",
        "Gender": "Género",
        "Number": "Número",
        "Tense": "Tiempo",
        "Mood": "Modo",
        "Person": "Persona",
        "Voice": "Voz",
        "Degree": "Grado",
        "Aspect": "Aspecto",
        "VerbForm": "Forma Verbal",
        
        # Casos (Values)
        "Nom": "Nominativo",
        "Gen": "Genitivo",
        "Dat": "Dativo",
        "Acc": "Acusativo",
        "Abl": "Ablativo",
        "Voc": "Vocativo",
        "Loc": "Locativo",
        
        # Género (Values)
        "Masc": "Masculino",
        "Fem": "Femenino",
        "Neut": "Neutro",
        
        # Número (Values)
        "Sing": "Singular",
        "Plur": "Plural",
        
        # Tiempos verbales (Values)
        "Pres": "Presente",
        "Imp": "Imperfecto",
        "Fut": "Futuro",
        "Perf": "Perfecto",
        "Pqp": "Pluscuamperfecto",
        "Futp": "Futuro Perfecto",
        
        # Modos verbales (Values)
        "Ind": "Indicativo",
        "Sub": "Subjuntivo",
        "Imp": "Imperativo",
        
        # Persona (Values)
        "1": "1ª persona",
        "2": "2ª persona",
        "3": "3ª persona",
        
        # Voz (Values)
        "Act": "Voz Activa",
        "Pass": "Voz Pasiva",
        
        # Formas verbales (Values)
        "Fin": "Forma Finita",
        "Inf": "Infinitivo",
        "Part": "Participio",
        "Ger": "Gerundio",
        "Gdv": "Gerundivo",
        "Sup": "Supino",
        
        # Grados del adjetivo (Values)
        "Pos": "Grado Positivo",
        "Cmp": "Comparativo",
        "Sup": "Superlativo"
    }
    
    SYNTAX_ROLE_TRANSLATIONS = {
        "subject": "Sujeto",
        "predicate": "Predicado",
        "direct_object": "Complemento Directo",
        "indirect_object": "Complemento Indirecto",
        "complement": "Complemento Circunstancial",
        "attribute": "Atributo",
        "apposition": "Aposición",
        "modifier": "Modificador",
        "determiner": "Determinante",
        "conjunction": "Conjunción"
    }
    
    def format_morphology(morph_str):
        if not morph_str:
            return ""
        
        parts = morph_str.split('|')
        translated_parts = []
        
        for part in parts:
            if '=' in part:
                key, value = part.split('=', 1)
                # Try exact match, then title case (e.g. 'gender' -> 'Gender')
                key_lookup = key if key in MORPH_TRANSLATIONS else key.title()
                value_lookup = value if value in MORPH_TRANSLATIONS else value.title()
                
                key_es = MORPH_TRANSLATIONS.get(key_lookup, key)
                value_es = MORPH_TRANSLATIONS.get(value_lookup, value)
                
                translated_parts.append(f"{key_es}: {value_es}")
            else:
                translated_parts.append(part)
                
        return ", ".join(translated_parts)
    
    def render_colored_sentence(sentence):
        try:
            deps = json.loads(sentence['dependency_json'])
            roles = json.loads(sentence['syntax_roles'])
        except:
            st.error("Error al procesar los datos de la oración")
            return
    
        # Create map of id -> role
        id_role_map = {}
        if roles:
            for role, ids in roles.items():
                for i in ids:
                    id_role_map[i] = role
    
        html = "<div style='line-height: 2.5;'>"
        for token in deps:
            role = id_role_map.get(token['id'], "")
            role_class = f"role-{role}" if role else "role-none" # Default class
            
            # Tooltip mejorado con información gramatical
            pos_tag = token.get('pos', '')
            pos_es = POS_TRANSLATIONS.get(pos_tag, pos_tag)
            
            morph_info = f"{pos_es}"
            if 'morph' in token and token['morph']:
                # Simple translation for tooltip to keep it short
                morph_raw = token['morph']
                # We can use the formatter but maybe replace comma with newline for tooltip
                morph_fmt = format_morphology(morph_raw).replace(", ", "&#10;")
                morph_info += f"&#10;{morph_fmt}"
            
            role_es = SYNTAX_ROLE_TRANSLATIONS.get(role, role.replace('_', ' ').title()) if role else 'Sin función específica'
            tooltip = f"{token['text']} ({token['lemma']})&#10;{morph_info}&#10;Función: {role_es}"
            
            html += f'<span class="syntax-token {role_class}" title="{tooltip}">{token["text"]}</span>'
        html += "</div>"
        
        st.markdown(html, unsafe_allow_html=True)
    
    # --- Display List ---
    
    # Pagination
    items_per_page = 10
    if 'page_number' not in st.session_state:
        st.session_state.page_number = 0
    
    total_pages = max(1, (len(sentences) + items_per_page - 1) // items_per_page)
    current_page = st.session_state.page_number
    
    col_prev, col_page, col_next = st.columns([1, 2, 1])
    with col_prev:
        if st.button("⬅️ Anterior") and current_page > 0:
            st.session_state.page_number -= 1
            st.rerun()
    with col_next:
        if st.button("Siguiente ➡️") and current_page < total_pages - 1:
            st.session_state.page_number += 1
            st.rerun()
    with col_page:
        st.write(f"Página {current_page + 1} de {total_pages}")
    
    # Glosario de abreviaturas (global, antes de las oraciones)
    with st.popover("📖 Glosario de Abreviaturas del Árbol", use_container_width=False):
        st.markdown("""
        **Funciones Sintácticas:**
        - **Sujeto** - Quién realiza la acción
        - **RAÍZ** - Verbo principal de la oración
        - **C. Directo** - Complemento Directo (¿qué?)
        - **C. Indirecto** - Complemento Indirecto (¿a quién?)
        - **C. Circunst.** - Complemento Circunstancial (cómo, cuándo, dónde...)
        - **C. Adverbial** - Complemento Adverbial
        - **C. Predicativo** - Complemento Predicativo
        
        **Modificadores:**
        - **Modificador** - Palabra que modifica a otra (generalmente adjetivos)
        - **Determinante** - Palabras que determinan al sustantivo
        - **Mod. Numérico** - Modificador numérico
        
        **Conjunciones:**
        - **Conj. Coord.** - Conjunción Coordinante (y, o, pero)
        - **Conj. Subord.** - Conjunción Subordinante (que, cuando, si)
        - **Coordinado** - Elemento coordinado con otro
        
        **Verbos y Auxiliares:**
        - **Auxiliar** - Verbo auxiliar
        - **Cópula** - Verbo copulativo (sum, esse)
        
        **Oraciones Subordinadas:**
        - **Or. Adjetiva** - Oración subordinada adjetiva
        - **Or. Relativa** - Oración de relativo (qui, quae, quod)
        - **Or. Adverbial** - Oración subordinada adverbial
        - **Or. Completiva** - Oración completiva
        
        **Otros:**
        - **Aposición** - Explicación o aclaración de un sustantivo
        - **Preposición** - Palabra que introduce complementos (ad, in, cum)
        - **Vocativo** - Llamada o invocación
        """)
    
    st.markdown("---")
    
    start_idx = current_page * items_per_page
    end_idx = start_idx + items_per_page
    page_sentences = sentences[start_idx:end_idx]
    
    for sent in page_sentences:
        # Calculate completeness for display
        try:
            total_tokens = len(json.loads(sent['dependency_json']))
            annotated_tokens = len(sent['token_annotations'])
            completeness_pct = int((annotated_tokens / total_tokens) * 100) if total_tokens > 0 else 0
        except:
            completeness_pct = 0
            
        title_prefix = "✅" if completeness_pct == 100 else f"🚧 {completeness_pct}%"
        
        with st.expander(f"{title_prefix} Nivel {sent['complexity_level']} | {sent['latin_text']}"):
            
            tabs = st.tabs(["🎨 Análisis Visual", "🌲 Árbol de Dependencias", "ℹ️ Detalles Gramaticales", "🎓 Análisis Pedagógico"])
            
            with tabs[0]:
                st.markdown("#### Estructura Sintáctica")
                render_colored_sentence(sent)
                
                st.markdown("---")
                # Legend
                st.markdown("""
                <div style="font-size:0.8em; margin-top: 10px;">
                    <strong>Leyenda:</strong><br>
                    <span class="legend-item role-subject">Sujeto</span>
                    <span class="legend-item role-predicate">Predicado</span>
                    <span class="legend-item role-direct_object">Objeto Directo</span>
                    <span class="legend-item role-indirect_object">Objeto Indirecto</span>
                    <span class="legend-item role-complement">Complemento</span>
                    <span class="legend-item role-attribute">Atributo</span>
                    <span class="legend-item role-apposition">Aposición</span>
                </div>
                """, unsafe_allow_html=True)
                
                if sent['spanish_translation']:
                    st.info(f"**Traducción:** {sent['spanish_translation']}")
    
            with tabs[1]:
                if sent['tree_diagram_svg']:
                    # Envolver en un div con scroll horizontal para árboles grandes
                    # Force white background for visibility in dark mode
                    st.markdown(f"""
                    <div style="overflow-x: auto; border: 1px solid #ddd; border-radius: 5px; padding: 10px; background-color: white;">
                        {sent['tree_diagram_svg']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("Diagrama de árbol no disponible para esta oración.")
    
            with tabs[2]:
                st.markdown("#### Desglose Morfológico")
                
                try:
                    deps = json.loads(sent['dependency_json'])
                    roles = json.loads(sent['syntax_roles'])
                    
                    # Map IDs to roles
                    id_role_map = {}
                    if roles:
                        for role, ids in roles.items():
                            for i in ids:
                                id_role_map[i] = role
                    
                    # Prepare data for dataframe
                    data = []
                    for token in deps:
                        pos_tag = token.get('pos', '')
                        pos_es = POS_TRANSLATIONS.get(pos_tag, pos_tag)
                        
                        # Translate morphology
                        morph_raw = token.get('morph', '')
                        morph_es = format_morphology(morph_raw)
                        
                        # Translate syntax role
                        syntax_role = id_role_map.get(token['id'], "")
                        role_es = SYNTAX_ROLE_TRANSLATIONS.get(syntax_role, syntax_role.replace('_', ' ').title()) if syntax_role else "—"
                        
                        data.append({
                            "Palabra": token['text'],
                            "Lema": token['lemma'],
                            "Categoría": pos_es,
                            "Morfología": morph_es,
                            "Función Sintáctica": role_es
                        })
                    
                    df = pd.DataFrame(data)
                    st.dataframe(df, width='stretch', hide_index=True)
                    
                except Exception as e:
                    st.error(f"No se pudo generar la tabla de detalles: {e}")
                
                st.markdown("---")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Fuente:** {sent['source'].replace('_', ' ').title()}")
                    st.markdown(f"**Lección:** #{sent['lesson_number']}")
                
                with col2:
                    st.markdown(f"**Tipo:** {sent['sentence_type'].title()}")
                    if sent['constructions']:
                        constrs = json.loads(sent['constructions'])
                        st.markdown(f"**Construcciones:** {', '.join(constrs) if constrs else 'Ninguna'}")
    
            with tabs[3]:
                st.markdown("#### 🎓 Explicación Pedagógica")
                
                # 1. Estructura General
                if sent['structures']:
                    for struct in sent['structures']:
                        st.info(f"**Estructura:** {struct['clause_type']} | **Notas:** {struct['notes'] or 'Sin notas'}")
                else:
                    st.write("No hay información estructural disponible.")
                
                st.markdown("#### 📝 Anotaciones Palabra por Palabra")
                
                # Combinar tokens con anotaciones
                try:
                    deps = json.loads(sent['dependency_json'])
                    
                    # Crear mapa de anotaciones por índice
                    ann_map = {}
                    if sent['token_annotations']:
                        for ann in sent['token_annotations']:
                            ann_map[ann['token_index']] = ann
                    
                    # Iterar sobre TODOS los tokens (0-indexed en la lista deps)
                    for i, token in enumerate(deps):
                        ann = ann_map.get(i)
                        
                        with st.container():
                            c1, c2 = st.columns([1, 3])
                            with c1:
                                st.markdown(f"**{token['text']}**")
                                if ann:
                                    st.caption(f"{ann['pedagogical_role']}")
                                else:
                                    # Fallback a POS si no hay rol pedagógico
                                    pos_tag = token.get('pos', '')
                                    pos_es = POS_TRANSLATIONS.get(pos_tag, pos_tag)
                                    st.caption(f"({pos_es})")
                                    
                            with c2:
                                if ann:
                                    if ann['case_function']:
                                        st.markdown(f"🏷️ **{ann['case_function']}**")
                                    if ann['explanation']:
                                        st.write(ann['explanation'])
                                else:
                                    # Mostrar info básica si no hay anotación
                                    morph_raw = token.get('morph', '')
                                    if morph_raw:
                                        st.caption(format_morphology(morph_raw))
                                    else:
                                        st.caption("Sin información morfológica adicional.")
                                        
                            st.divider()
                            
                except Exception as e:
                    st.error(f"Error al renderizar anotaciones: {e}")

            # --- EDITOR MODE ---
            if st.session_state.get("editor_mode", False):
                st.markdown("---")
                
                # Undo button
                col_undo, col_title = st.columns([1, 3])
                with col_undo:
                    if 'syntax_edit_history' in st.session_state and len(st.session_state.syntax_edit_history) > 0:
                        if st.button("↩️ Deshacer", help="Restaurar el último cambio", key=f"undo_{sent['id']}"):
                            if undo_last_change():
                                st.success("✅ Cambio deshecho")
                                st.rerun()
                            else:
                                st.error("❌ No se pudo deshacer")
                    else:
                        st.caption("_No hay cambios para deshacer_")
                
                with col_title:
                    st.markdown("### ✏️ Modo Editor de Sintaxis")
                
                try:
                    deps = json.loads(sent['dependency_json'])
                    current_roles = json.loads(sent['syntax_roles'])
                    
                    # Map token_index -> current_role
                    token_role_map = {}
                    if current_roles:
                        for role, indices in current_roles.items():
                            for idx in indices:
                                token_role_map[idx] = role
                            
                    # Form for editing
                    with st.form(key=f"edit_form_{sent['id']}"):
                        st.write("Asignar funciones sintácticas:")
                        
                        new_role_map = {}
                        
                        # Grid layout for tokens
                        cols = st.columns(3)
                        
                        available_roles = [""] + list(SYNTAX_ROLE_TRANSLATIONS.keys())
                        
                        for i, token in enumerate(deps):
                            col = cols[i % 3]
                            with col:
                                # Usar el ID del token si está disponible, sino el índice + 1 (asumiendo 1-based IDs en Spacy)
                                token_id = token.get('id', i + 1)
                                current_role = token_role_map.get(token_id, "")
                                
                                # Display readable name for role
                                role_options = available_roles
                                
                                # Find index of current role
                                try:
                                    default_idx = role_options.index(current_role)
                                except ValueError:
                                    default_idx = 0
                                
                                new_role = st.selectbox(
                                    f"{token['text']} ({token_id})",
                                    options=role_options,
                                    index=default_idx,
                                    format_func=lambda x: SYNTAX_ROLE_TRANSLATIONS.get(x, x) if x else "—",
                                    key=f"role_sel_{sent['id']}_{token_id}"
                                )
                                new_role_map[token_id] = new_role
                        
                        # Show change summary
                        st.markdown("---")
                        changes_count = count_role_changes(current_roles, new_role_map)
                        
                        if changes_count > 0:
                            st.warning(f"⚠️ **{changes_count} etiqueta(s) modificada(s)**")
                        else:
                            st.info("ℹ️ No hay cambios pendientes")
                        
                        # Submit button
                        submitted = st.form_submit_button(
                            "💾 Guardar Cambios", 
                            type="primary"
                        )
                        
                        if submitted and changes_count > 0:
                            # Save current state to history before making changes
                            save_to_edit_history(sent['id'], sent['syntax_roles'])
                            
                            # Reconstruct syntax_roles dictionary
                            updated_roles = {}
                            for tid, role in new_role_map.items():
                                if role: # Only save if a role is selected
                                    if role not in updated_roles:
                                        updated_roles[role] = []
                                    updated_roles[role].append(tid)
                            
                            # Save to DB
                            try:
                                with get_session() as session:
                                    # Reload sentence to ensure attached to session
                                    db_sent = session.get(SentenceAnalysis, sent['id'])
                                    db_sent.syntax_roles = json.dumps(updated_roles)
                                    session.add(db_sent)
                                    session.commit()
                                    st.success("✅ ¡Cambios guardados correctamente!")
                                    st.balloons()
                                    st.rerun()
                            except Exception as e:
                                st.error(f"❌ Error al guardar: {e}")
                    
                    # --- PEDAGOGICAL ANNOTATIONS EDITOR ---
                    st.markdown("---")
                    st.markdown("#### 📝 Editor de Anotaciones Pedagógicas")
                    st.caption("Edita las explicaciones y funciones de caso para cada palabra")
                    
                    # Get current annotations
                    ann_map = {}
                    if sent['token_annotations']:
                        for ann in sent['token_annotations']:
                            ann_map[ann['token_index']] = ann
                    
                    # Edit each token's annotation
                    for i, token in enumerate(deps):
                        ann = ann_map.get(i)
                        
                        with st.expander(f"📌 Token {i+1}: **{token['text']}** ({token['lemma']})"):
                            with st.form(key=f"ann_form_{sent['id']}_{i}"):
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    ped_role = st.text_input(
                                        "Rol Pedagógico",
                                        value=ann['pedagogical_role'] if ann else "",
                                        help="Ej: Sujeto, Objeto Directo, Núcleo del Predicado",
                                        key=f"ped_role_{sent['id']}_{i}"
                                    )
                                    
                                    case_func = st.text_input(
                                        "Función del Caso",
                                        value=ann['case_function'] if ann else "",
                                        help="Ej: Nominativo Sujeto, Acusativo de Objeto Directo",
                                        key=f"case_func_{sent['id']}_{i}"
                                    )
                                
                                with col2:
                                    # Show morphological info for reference
                                    st.caption(f"**POS:** {token.get('pos', 'N/A')}")
                                    st.caption(f"**Morph:** {token.get('morph', 'N/A')[:50]}...")
                                
                                explanation = st.text_area(
                                    "Explicación Pedagógica",
                                    value=ann['explanation'] if ann and ann['explanation'] else "",
                                    height=100,
                                    help="Explicación didáctica de la función gramatical",
                                    key=f"expl_{sent['id']}_{i}"
                                )
                                
                                if st.form_submit_button(f"💾 Guardar Anotación Token {i+1}"):
                                    try:
                                        with get_session() as session:
                                            # Check if annotation exists
                                            if ann:
                                                # Update existing
                                                db_ann = session.exec(
                                                    select(TokenAnnotation).where(
                                                        TokenAnnotation.sentence_id == sent['id'],
                                                        TokenAnnotation.token_index == i
                                                    )
                                                ).first()
                                                
                                                if db_ann:
                                                    db_ann.pedagogical_role = ped_role
                                                    db_ann.case_function = case_func
                                                    db_ann.explanation = explanation
                                                    session.add(db_ann)
                                            else:
                                                # Create new
                                                new_ann = TokenAnnotation(
                                                    sentence_id=sent['id'],
                                                    token_index=i,
                                                    token_text=token['text'],
                                                    pedagogical_role=ped_role,
                                                    case_function=case_func,
                                                    explanation=explanation
                                                )
                                                session.add(new_ann)
                                            
                                            session.commit()
                                            st.success(f"✅ Anotación guardada para '{token['text']}'")
                                            st.rerun()
                                            
                                    except Exception as e:
                                        st.error(f"❌ Error: {e}")
                                
                except Exception as e:
                    st.error(f"Error al cargar el editor: {e}")

