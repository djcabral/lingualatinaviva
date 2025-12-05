import streamlit as st
from sqlmodel import select
from database.connection import get_session
from database import Word
from utils.collatinus_analyzer import analyzer
from utils.ui_helpers import load_css, render_styled_table
from utils.text_utils import normalize_latin

def render_content():
    """Renderiza la herramienta de consulta de Collatinus"""
    
    load_css()
    
    st.markdown(
        """
        <h2 style='text-align: center; font-family: "Cinzel", serif;'>
            📖 Consulta Collatinus
        </h2>
        <p style='text-align: center; color: #666;'>
            Diccionario morfológico independiente
        </p>
        """,
        unsafe_allow_html=True
    )
    
    # Verificar disponibilidad
    if not analyzer.is_ready():
        st.error("⚠️ El motor Collatinus no está disponible.")
        return

    # Interfaz de búsqueda
    col1, col2 = st.columns([3, 1])
    
    with col1:
        word_input = st.text_input(
            "Palabra latina",
            placeholder="Ej: amabam, regibus, bonas...",
            label_visibility="collapsed"
        )
    
    with col2:
        search_btn = st.button("🔍 Analizar", type="primary", width="stretch")
    
    if search_btn and word_input:
        st.session_state.collatinus_search = word_input
    
    # Usar estado para persistencia
    if 'collatinus_search' in st.session_state and st.session_state.collatinus_search:
        current_word = st.session_state.collatinus_search
        
        with st.spinner("Consultando Collatinus..."):
            results = analyzer.analyze_word(current_word.strip().lower())
            
            if results:
                st.success(f"Se encontraron {len(results)} análisis posibles para '**{current_word}**'")
                
                # Buscar traducciones en DB para todos los lemas encontrados
                lemmas = set(res['lemma'] for res in results)
                translations = {}
                
                with get_session() as session:
                    for lemma in lemmas:
                        # 1. Intentar coincidencia exacta con collatinus_lemma
                        db_word = session.exec(select(Word).where(Word.collatinus_lemma == lemma)).first()
                        
                        # 2. Si no, intentar coincidencia exacta con latin
                        if not db_word:
                            db_word = session.exec(select(Word).where(Word.latin == lemma)).first()
                            
                        # 3. Si no, intentar normalizando (ignorando macrones)
                        if not db_word:
                            # Esto es ineficiente si hay muchas palabras, pero aceptable para búsquedas puntuales
                            # Idealmente tendríamos una columna normalized_latin indexada
                            all_words = session.exec(select(Word)).all()
                            for w in all_words:
                                if normalize_latin(w.latin) == normalize_latin(lemma):
                                    db_word = w
                                    break
                        
                        if db_word:
                            translations[lemma] = db_word.definition_es or db_word.translation
                
                for i, res in enumerate(results, 1):
                    lemma = res['lemma']
                    translation = translations.get(lemma, "Traducción no disponible en DB local")
                    
                    with st.expander(f"Resultado {i}: **{lemma}** ({translation})", expanded=True):
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            st.markdown(f"**Lema:** {lemma}")
                            st.markdown(f"**Morfología:** {res['morph']}")
                            if translation != "Traducción no disponible en DB local":
                                st.markdown(f"**Significado:** {translation}")
                        
                        with col_b:
                            # Botón para ver paradigma (usar índice único)
                            if st.button(f"📊 Ver Paradigma Completo", key=f"btn_para_{i}_{lemma}"):
                                st.session_state.show_paradigm_for = f"{i}_{lemma}"
                        
                        # Mostrar paradigma solo si está seleccionado ESTE resultado específico
                        if st.session_state.get('show_paradigm_for') == f"{i}_{lemma}":
                            st.markdown("---")
                            st.markdown(f"#### Paradigma de *{lemma}*")
                            
                            with st.spinner("Generando tabla..."):
                                paradigm = analyzer.generate_paradigm(lemma)
                                
                                if 'error' in paradigm:
                                    st.error(f"Error: {paradigm['error']}")
                                else:
                                    # Mostrar paradigma organizado
                                    render_paradigm_tables(paradigm)
                                    
                                    if st.button("Cerrar Paradigma", key=f"close_{i}_{lemma}"):
                                        st.session_state.show_paradigm_for = None
                                        st.rerun()

            else:
                st.warning(f"No se encontraron resultados para '{current_word}' en Collatinus.")
                st.info("Intenta con otra forma o verifica la ortografía.")

def organize_paradigm_data(paradigm_data):
    """
    Organiza los datos planos del paradigma en estructuras tabulares
    según el tipo de palabra (sustantivo/adjetivo o verbo).
    """
    forms = paradigm_data.get('forms', [])
    if not forms:
        return None, "unknown"
        
    # Detectar tipo basado en morfología
    is_verb = any("Persona" in f['morph'] or "Infinitivo" in f['morph'] for f in forms)
    
    if is_verb:
        # Estructura para verbos: Tiempo -> Voz -> Modo -> [Personas]
        tables = {}
        
        for form in forms:
            morph = form['morph']
            text = form['form']
            
            # Extraer información
            mood = "Indicativo" # Default
            if "Subjuntivo" in morph: mood = "Subjuntivo"
            elif "Imperativo" in morph: mood = "Imperativo"
            elif "Infinitivo" in morph: mood = "Infinitivo"
            elif "Participio" in morph: mood = "Participio"
            elif "Gerundio" in morph: mood = "Gerundio"
            elif "Supino" in morph: mood = "Supino"
            
            tense = "Presente" # Default
            if "Imperfecto" in morph: tense = "Imperfecto"
            elif "Futuro Perfecto" in morph: tense = "Futuro Perfecto"
            elif "Futuro" in morph: tense = "Futuro Imperfecto"
            elif "Pluscuamperfecto" in morph: tense = "Pluscuamperfecto"
            elif "Perfecto" in morph: tense = "Perfecto"
            
            voice = "Activa"
            if "Pasiva" in morph: voice = "Pasiva"
            
            # Clave para agrupar
            if mood in ["Infinitivo", "Gerundio", "Supino"]:
                key = f"{mood}"
            elif mood == "Participio":
                key = f"{mood} {tense}" # Participio Presente, etc.
            else:
                key = f"{mood} {tense} {voice}"
            
            if key not in tables:
                tables[key] = []
            
            tables[key].append(f"{text} ({morph})")
            
        return tables, "verb"
        
    else:
        # Estructura para sustantivos/adjetivos: Caso -> [Singular, Plural]
        # Simplificado: Lista de formas con su caso/número
        # Mejor: Intentar reconstruir tabla de declinación
        
        declension_table = {
            "Nominativo": {"Singular": "", "Plural": ""},
            "Vocativo": {"Singular": "", "Plural": ""},
            "Acusativo": {"Singular": "", "Plural": ""},
            "Genitivo": {"Singular": "", "Plural": ""},
            "Dativo": {"Singular": "", "Plural": ""},
            "Ablativo": {"Singular": "", "Plural": ""},
            "Locativo": {"Singular": "", "Plural": ""}
        }
        
        has_locative = False
        
        for form in forms:
            morph = form['morph']
            text = form['form']
            
            case = None
            for c in ["Nominativo", "Vocativo", "Acusativo", "Genitivo", "Dativo", "Ablativo", "Locativo"]:
                if c in morph:
                    case = c
                    break
            
            number = "Singular" if "Singular" in morph else "Plural" if "Plural" in morph else None
            
            if case and number:
                if case == "Locativo":
                    has_locative = True
                
                current = declension_table[case][number]
                if current:
                    declension_table[case][number] = current + ", " + text
                else:
                    declension_table[case][number] = text
                    
        if not has_locative:
            del declension_table["Locativo"]
            
        return declension_table, "noun"

def render_paradigm_tables(paradigm_data):
    """Renderiza las tablas del paradigma usando render_styled_table"""
    
    tables, type_ = organize_paradigm_data(paradigm_data)
    
    if type_ == "noun":
        # Convertir a formato para render_styled_table
        headers = ["Caso", "Singular", "Plural"]
        rows = []
        
        for case, forms in tables.items():
            rows.append([
                f"**{case}**",
                forms["Singular"] or "-",
                forms["Plural"] or "-"
            ])
            
        render_styled_table(headers, rows)
        
    elif type_ == "verb":
        # Mostrar múltiples tablas pequeñas
        # Agrupar por Modo para visualización más limpia
        
        # Orden deseado
        modes_order = ["Indicativo", "Subjuntivo", "Imperativo", "Infinitivo", "Participio", "Gerundio", "Supino"]
        
        for mode in modes_order:
            # Filtrar tablas de este modo
            mode_tables = {k: v for k, v in tables.items() if k.startswith(mode)}
            
            if mode_tables:
                # Si es Indicativo o Subjuntivo, mostrar por tiempos
                if mode in ["Indicativo", "Subjuntivo"]:
                    st.markdown(f"##### {mode}")
                    for key, forms in mode_tables.items():
                        # key es "Modo Tiempo Voz"
                        # Extraer Tiempo y Voz para el título
                        parts = key.split()
                        title = " ".join(parts[1:]) # Tiempo Voz
                        
                        with st.expander(title, expanded=False):
                            # Organizar formas en tabla de conjugación
                            # Parsear forms que vienen como "texto (morfología)"
                            person_forms = {"1": {"Sing": "", "Plur": ""}, 
                                          "2": {"Sing": "", "Plur": ""},
                                          "3": {"Sing": "", "Plur": ""}}
                            
                            for f in forms:
                                # Extraer persona y número de la morfología
                                if "1ª" in f:
                                    person = "1"
                                elif "2ª" in f:
                                    person = "2"
                                elif "3ª" in f:
                                    person = "3"
                                else:
                                    continue
                                
                                if "Singular" in f:
                                    number = "Sing"
                                elif "Plural" in f:
                                    number = "Plur"
                                else:
                                    continue
                                
                                # Extraer la forma (antes del paréntesis)
                                form_text = f.split(" (")[0].strip() if " (" in f else f
                                person_forms[person][number] = form_text
                            
                            # Crear tabla
                            headers = ["Persona", "Singular", "Plural"]
                            rows = []
                            for p in ["1", "2", "3"]:
                                rows.append([
                                    f"**{p}ª**",
                                    person_forms[p]["Sing"] or "—",
                                    person_forms[p]["Plur"] or "—"
                                ])
                            
                            render_styled_table(headers, rows)
                elif mode == "Infinitivo":
                    # Tabla de Infinitivos
                    st.markdown(f"##### {mode}")
                    headers = ["Tiempo", "Voz", "Forma"]
                    rows = []
                    
                    # Aplanar todas las formas de infinitivo (solo hay una key "Infinitivo")
                    for key, forms in mode_tables.items():
                        for f in forms:
                            # f es "amare (Infinitivo Presente Activa)"
                            text = f.split(" (")[0]
                            morph = f.split(" (")[1].replace(")", "")
                            
                            tense = "Presente"
                            if "Perfecto" in morph: tense = "Perfecto"
                            elif "Futuro" in morph: tense = "Futuro"
                            
                            voice = "Activa"
                            if "Pasiva" in morph: voice = "Pasiva"
                            
                            rows.append([tense, voice, f"**{text}**"])
                    
                    # Ordenar filas: Presente Act, Pres Pas, Perf Act, Perf Pas, Fut Act, Fut Pas
                    def sort_inf(row):
                        t_score = {"Presente": 1, "Perfecto": 2, "Futuro": 3}.get(row[0], 9)
                        v_score = {"Activa": 1, "Pasiva": 2}.get(row[1], 9)
                        return t_score * 10 + v_score
                        
                    rows.sort(key=sort_inf)
                    render_styled_table(headers, rows)

                elif mode == "Participio":
                    # Tablas de Participios (una por tiempo)
                    st.markdown(f"##### {mode}")
                    for key, forms in mode_tables.items():
                        # key es "Participio Tiempo" (ej: Participio Presente)
                        title = key.replace("Participio ", "")
                        
                        with st.expander(f"Participio {title}", expanded=False):
                            # Organizar por Caso y Número
                            # Estructura: data[Caso][Numero] = [formas]
                            data = {
                                "Nominativo": {"Singular": [], "Plural": []},
                                "Genitivo": {"Singular": [], "Plural": []},
                                "Dativo": {"Singular": [], "Plural": []},
                                "Acusativo": {"Singular": [], "Plural": []},
                                "Ablativo": {"Singular": [], "Plural": []},
                                "Vocativo": {"Singular": [], "Plural": []}
                            }
                            
                            for f in forms:
                                text = f.split(" (")[0]
                                morph = f.split(" (")[1].replace(")", "")
                                
                                case = None
                                for c in data.keys():
                                    if c in morph:
                                        case = c
                                        break
                                
                                number = "Singular" if "Singular" in morph else "Plural" if "Plural" in morph else None
                                
                                if case and number:
                                    # Añadir género si es relevante para distinguir
                                    gender = ""
                                    if "Masculino" in morph: gender = "(m)"
                                    elif "Femenino" in morph: gender = "(f)"
                                    elif "Neutro" in morph: gender = "(n)"
                                    
                                    # Evitar duplicados exactos
                                    entry = f"{text} {gender}".strip()
                                    if entry not in data[case][number]:
                                        data[case][number].append(entry)
                            
                            # Construir tabla
                            headers = ["Caso", "Singular", "Plural"]
                            rows = []
                            for case in ["Nominativo", "Genitivo", "Dativo", "Acusativo", "Ablativo"]:
                                sing_forms = ", ".join(data[case]["Singular"]) or "—"
                                plur_forms = ", ".join(data[case]["Plural"]) or "—"
                                rows.append([f"**{case}**", sing_forms, plur_forms])
                                
                            render_styled_table(headers, rows)

                elif mode in ["Gerundio", "Supino"]:
                    # Tabla simple Caso | Forma
                    st.markdown(f"##### {mode}")
                    headers = ["Caso/Uso", "Forma"]
                    rows = []
                    
                    # Orden de casos preferido
                    case_order = ["Nominativo", "Acusativo", "Genitivo", "Dativo", "Ablativo"]
                    
                    forms_by_case = {}
                    
                    for key, forms in mode_tables.items():
                        for f in forms:
                            if " (" in f:
                                text = f.split(" (")[0]
                                morph = f.split(" (")[1].replace(")", "")
                            else:
                                text = f
                                morph = ""
                            
                            case = None
                            # Intentar detectar caso en la morfología
                            for c in case_order:
                                if c in morph:
                                    case = c
                                    break
                            
                            # Si no se detectó caso, usar la morfología completa o "Forma"
                            if not case:
                                # Para supino: típicamente son 2 formas (acusativo y ablativo)
                                # Si ya hay formas, numerar como Forma 1, Forma 2, etc.
                                existing_general = [k for k in forms_by_case.keys() if k.startswith("Forma")]
                                case = f"Forma {len(existing_general) + 1}" if existing_general else morph if morph else "Forma"
                            
                            # Evitar duplicados en el mismo caso
                            if case in forms_by_case:
                                if text not in forms_by_case[case]:
                                    forms_by_case[case] = forms_by_case[case] + ", " + text
                            else:
                                forms_by_case[case] = text
                    
                    # Primero agregar casos conocidos en orden
                    for case in case_order:
                        if case in forms_by_case:
                            rows.append([f"**{case}**", f"**{forms_by_case[case]}**"])
                    
                    # Luego agregar otras formas que no coincidieron con casos conocidos
                    for case, form in forms_by_case.items():
                        if case not in case_order:
                            rows.append([f"**{case}**", f"**{form}**"])
                            
                    if rows:
                        render_styled_table(headers, rows)
                    else:
                        st.caption("(No se generaron formas para este modo)")

                else:
                    # Fallback para cualquier otro modo
                    for key, forms in mode_tables.items():
                        st.markdown(f"**{key}**")
                        for f in forms:
                            st.text(f)
    else:
        # Fallback
        for form in paradigm_data.get('forms', []):
            st.text(f"{form['form']} - {form['morph']}")
