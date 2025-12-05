import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from utils.collatinus_analyzer import analyzer
from utils.ui_helpers import load_css, render_styled_table

def render_content():
    """Renderiza el generador de paradigmas usando PyCollatinus"""
    
    load_css()
    
    st.markdown(
        """
        <h1 style='text-align: center; font-family: "Cinzel", serif;'>
            📊 Generador de Paradigmas
        </h1>
        <p style='text-align: center; color: #666;'>
            Genera tablas completas de conjugación y declinación
        </p>
        """,
        unsafe_allow_html=True
    )
    
    # Verificar que PyCollatinus esté disponible
    if not analyzer.is_ready():
        st.error("⚠️ PyCollatinus no está disponible. Por favor, contacta al administrador.")
        st.info("Para instalar: `pip install pycollatinus`")
        return
    
    # Input para la palabra
    col1, col2 = st.columns([3, 1])
    
    with col1:
        word_input = st.text_input(
            "Ingresa un lema latino (ej. rosa, amo, dominus, puella):",
            placeholder="rosa",
            help="Escribe el lema (forma base) de la palabra que quieres conjugar o declinar"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        generate_btn = st.button("🔍 Generar Paradigma", type="primary", width="stretch")
    
    # Ejemplos rápidos
    st.markdown("**Ejemplos rápidos:**")
    col_ex1, col_ex2, col_ex3, col_ex4, col_ex5 = st.columns(5)
    
    with col_ex1:
        if st.button("rosa 🌹", width="stretch"):
            st.session_state.paradigm_word = "rosa"
            st.rerun()
    with col_ex2:
        if st.button("amo ❤️", width="stretch"):
            st.session_state.paradigm_word = "amo"
            st.rerun()
    with col_ex3:
        if st.button("dominus 👑", width="stretch"):
            st.session_state.paradigm_word = "dominus"
            st.rerun()
    with col_ex4:
        if st.button("sum 🌟", width="stretch"):
            st.session_state.paradigm_word = "sum"
            st.rerun()
    with col_ex5:
        if st.button("do 🎁", width="stretch"):
            st.session_state.paradigm_word = "do"
            st.rerun()
    
    # Usar palabra de session_state si existe
    if 'paradigm_word' in st.session_state and st.session_state.paradigm_word:
        word_input = st.session_state.paradigm_word
        generate_btn = True
        # Limpiar después de usar
        st.session_state.paradigm_word = None
    
    # Generar paradigma y guardarlo en session_state
    if generate_btn and word_input:
        with st.spinner(f"Generando paradigma para '{word_input}'..."):
            paradigm = analyzer.generate_paradigm(word_input.strip().lower())
        
        # Guardar en session_state
        st.session_state.current_paradigm = paradigm
        st.session_state.current_word = word_input.strip().lower()
    
    # Mostrar paradigma si existe en session_state
    if 'current_paradigm' in st.session_state and st.session_state.current_paradigm:
        paradigm = st.session_state.current_paradigm
        
        if 'error' in paradigm:
            st.error(f"❌ {paradigm['error']}")
            st.info("💡 Asegúrate de ingresar el **lema** (forma base) de la palabra, no una forma declinada/conjugada.")
        else:
            # Mostrar información del paradigma
            st.success(f"✅ Paradigma generado: **{paradigm['lemma']}**")
            
            col_info1, col_info2, col_info3 = st.columns(3)
            with col_info1:
                st.metric("Total de formas", paradigm['total_forms'])
            with col_info2:
                st.info(f"**Modelo:** {paradigm['model'].split('[')[1].split(']')[0]}")
            with col_info3:
                if st.button("🔄 Nueva palabra", width="stretch"):
                    # Limpiar session_state
                    st.session_state.current_paradigm = None
                    st.session_state.current_word = None
                    st.rerun()
            
            st.markdown("---")
            
            # Determinar si es sustantivo o verbo basado en el número de formas
            is_noun = paradigm['total_forms'] <= 20  # Sustantivos/adjetivos tienen ~12 formas
            
            if is_noun:
                render_noun_paradigm(paradigm)
            else:
                render_verb_paradigm(paradigm)



def render_noun_paradigm(paradigm):
    """Renderiza el paradigma de un sustantivo/adjetivo en formato tabla"""
    
    st.markdown("### 📋 Tabla de Declinación")
    
    # Organizar formas por caso y número
    cases = ["Nominativo", "Vocativo", "Acusativo", "Genitivo", "Dativo", "Ablativo"]
    numbers = ["Singular", "Plural"]
    
    # Mapeo de morfología a caso/número
    case_map = {
        "nominativo": "Nominativo",
        "vocativo": "Vocativo", 
        "acusativo": "Acusativo",
        "genitivo": "Genitivo",
        "dativo": "Dativo",
        "ablativo": "Ablativo"
    }
    
    number_map = {
        "singular": "Singular",
        "plural": "Plural"
    }
    
    # Crear diccionario de formas organizadas
    table_data = {case: {"Singular": "", "Plural": ""} for case in cases}
    
    for form_data in paradigm['forms']:
        morph = form_data['morph'].lower()
        form = form_data['form']
        
        # Identificar caso y número
        found_case = None
        found_number = None
        
        for case_key, case_val in case_map.items():
            if case_key in morph:
                found_case = case_val
                break
        
        for num_key, num_val in number_map.items():
            if num_key in morph:
                found_number = num_val
                break
        
        if found_case and found_number:
            # Si ya hay una forma, agregar con / (sincretismo)
            if table_data[found_case][found_number]:
                if form not in table_data[found_case][found_number]:
                    table_data[found_case][found_number] += f" / {form}"
            else:
                table_data[found_case][found_number] = form
    
    
    # Preparar datos para render_styled_table
    headers = ["Caso", "Singular", "Plural"]
    rows = []
    
    for case in cases:
        rows.append([
            f"**{case}**",
            table_data[case]['Singular'] or '—',
            table_data[case]['Plural'] or '—'
        ])
    
    render_styled_table(headers, rows)
    
    # Mostrar todas las formas en detalle (expandible)
    with st.expander("📖 Ver todas las formas con morfología detallada"):
        for i, form_data in enumerate(paradigm['forms'], 1):
            st.markdown(f"**{i}. {form_data['form']}** → {form_data['morph']}")


def render_participle_table(forms_in_category, title):
    """Renderiza un participio como tabla de declinación por género"""
    
    st.markdown(f"##### {title}")
    
    # Organizar formas por caso, número y género
    cases = ["Nominativo", "Vocativo", "Acusativo", "Genitivo", "Dativo", "Ablativo"]
    
    case_map = {
        "nominativo": "Nominativo",
        "vocativo": "Vocativo",
        "acusativo": "Acusativo",
        "genitivo": "Genitivo",
        "dativo": "Dativo",
        "ablativo": "Ablativo"
    }
    
    number_map = {
        "singular": "Singular",
        "plural": "Plural"
    }
    
    gender_map = {
        "masculino": "Masc.",
        "femenino": "Fem.",
        "neutro": "Neut."
    }
    
    # Detectar qué géneros están presentes
    genders_present = set()
    for data in forms_in_category.values():
        morph_lower = data['morph'].lower()
        for gender_key in gender_map.keys():
            if gender_key in morph_lower:
                genders_present.add(gender_key)
    
    # Si solo hay un género (participio presente solo masculino/femenino), simplificar
    if len(genders_present) == 1:
        # Tabla simple: Caso | Singular | Plural
        table_data = {case: {"Singular": "", "Plural": ""} for case in cases}
        
        for data in forms_in_category.values():
            morph = data['morph'].lower()
            form = data['form']
            
            found_case = None
            found_number = None
            
            for case_key, case_val in case_map.items():
                if case_key in morph:
                    found_case = case_val
                    break
            
            for num_key, num_val in number_map.items():
                if num_key in morph:
                    found_number = num_val
                    break
            
            if found_case and found_number:
                if table_data[found_case][found_number]:
                    if form not in table_data[found_case][found_number]:
                        table_data[found_case][found_number] += f" / {form}"
                else:
                    table_data[found_case][found_number] = form
        
        headers = ["Caso", "Singular", "Plural"]
        rows = []
        for case in cases:
            if table_data[case]['Singular'] or table_data[case]['Plural']:
                rows.append([
                    f"**{case}**",
                    table_data[case]['Singular'] or '—',
                    table_data[case]['Plural'] or '—'
                ])
        
        render_styled_table(headers, rows)
    
    else:
        # Tabla compleja: Caso | Masc. Sg | Fem. Sg | Neut. Sg | Masc. Pl | Fem. Pl | Neut. Pl
        table_data = {}
        for case in cases:
            table_data[case] = {
                "Masc_Sing": "", "Fem_Sing": "", "Neut_Sing": "",
                "Masc_Plur": "", "Fem_Plur": "", "Neut_Plur": ""
            }
        
        for data in forms_in_category.values():
            morph = data['morph'].lower()
            form = data['form']
            
            found_case = None
            found_number = None
            found_gender = None
            
            for case_key, case_val in case_map.items():
                if case_key in morph:
                    found_case = case_val
                    break
            
            for num_key, num_val in number_map.items():
                if num_key in morph:
                    found_number = "Sing" if num_val == "Singular" else "Plur"
                    break
            
            for gender_key in gender_map.keys():
                if gender_key in morph:
                    found_gender = gender_key.capitalize()[:4]  # Masc, Feme, Neut
                    if found_gender == "Feme":
                        found_gender = "Fem"
                    break
            
            if found_case and found_number and found_gender:
                key = f"{found_gender}_{found_number}"
                if key in table_data[found_case]:
                    if table_data[found_case][key]:
                        if form not in table_data[found_case][key]:
                            table_data[found_case][key] += f" / {form}"
                    else:
                        table_data[found_case][key] = form
        
        # Construir encabezados basados en géneros presentes
        headers = ["Caso"]
        col_order = []
        
        for number in ["Sing", "Plur"]:
            for gender in ["Masc", "Fem", "Neut"]:
                gender_key_lower = gender.lower()
                if gender_key_lower == "masc":
                    gender_key_lower = "masculino"
                elif gender_key_lower == "fem":
                    gender_key_lower = "femenino"
                elif gender_key_lower == "neut":
                    gender_key_lower = "neutro"
                
                if gender_key_lower in genders_present:
                    col_key = f"{gender}_{number}"
                    col_order.append(col_key)
                    number_label = "Sg" if number == "Sing" else "Pl"
                    headers.append(f"{gender}. {number_label}")
        
        rows = []
        for case in cases:
            # Solo incluir fila si tiene al menos una forma
            if any(table_data[case][col] for col in col_order):
                row = [f"**{case}**"]
                for col in col_order:
                    row.append(table_data[case][col] or '—')
                rows.append(row)
        
        render_styled_table(headers, rows)


def render_verb_paradigm(paradigm):
    """Renderiza el paradigma de un verbo organizado en tablas por tiempo"""
    
    st.markdown("### 🔄 Tabla de Conjugación")
    
    # Organizar formas por tiempo/modo/voz
    organized = {}
    
    for form_data in paradigm['forms']:
        morph = form_data['morph']
        form = form_data['form']
        
        # Extraer categorías principales de la morfología
        tiempo = ""
        modo = "Indicativo"
        voz = "Activa"
        persona = ""
        numero = ""
        
        # Buscar tiempo (orden importante: más específico primero)
        if "Futuro Perfecto" in morph:
            tiempo = "Futuro Perfecto"
        elif "Futuro" in morph:
            tiempo = "Futuro Imperfecto"
        elif "Pluscuamperfecto" in morph:
            tiempo = "Pluscuamperfecto"
        elif "Perfecto" in morph:
            tiempo = "Perfecto"
        elif "Imperfecto" in morph:
            tiempo = "Imperfecto"
        elif "Presente" in morph:
            tiempo = "Presente"
        
        # Buscar modo
        if "Subjuntivo" in morph:
            modo = "Subjuntivo"
        elif "Imperativo" in morph:
            modo = "Imperativo"
        elif "Infinitivo" in morph:
            modo = "Infinitivo"
        elif "Participio" in morph:
            modo = "Participio"
        elif "Gerundio" in morph:
            modo = "Gerundio"
        elif "Supino" in morph:
            modo = "Supino"
        
        # Buscar voz
        if "Pasiva" in morph or "Pasivo" in morph:
            voz = "Pasiva"
        
        # Extraer persona y número
        if "1ª" in morph:
            persona = "1"
        elif "2ª" in morph:
            persona = "2"
        elif "3ª" in morph:
            persona = "3"
        
        if "Singular" in morph:
            numero = "Sing"
        elif "Plural" in morph:
            numero = "Plur"
        
        # Crear clave de categoría (reemplazar espacios en tiempo para evitar problemas con split)
        tiempo_key = tiempo.replace(" ", "_")
        
        if modo in ["Infinitivo", "Gerundio", "Supino"]:
            category = f"{modo}_{voz}"
            subcategory = morph  # Usar morfología completa como subcategoría
        elif modo == "Participio":
            category = f"Participio_{tiempo_key}_{voz}"
            subcategory = morph
        else:
            category = f"{modo}_{tiempo_key}_{voz}"
            subcategory = f"{persona}_{numero}"
        
        if category not in organized:
            organized[category] = {}
        
        organized[category][subcategory] = {
            'form': form,
            'morph': morph,
            'persona': persona,
            'numero': numero
        }
    
    # Filtros
    st.markdown("#### 🎛️ Filtros")
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        modo_filter = st.multiselect(
            "Modo",
            ["Indicativo", "Subjuntivo", "Imperativo", "Infinitivo", "Participio", "Gerundio", "Supino"],
            default=["Indicativo", "Subjuntivo"],
            help="Selecciona los modos que quieres ver"
        )
    
    with col_f2:
        voz_filter = st.multiselect(
            "Voz",
            ["Activa", "Pasiva"],
            default=["Activa"],
            help="Selecciona las voces que quieres ver"
        )
    
    with col_f3:
        tiempo_filter = st.multiselect(
            "Tiempo",
            ["Presente", "Imperfecto", "Futuro Imperfecto", "Futuro Perfecto", "Perfecto", "Pluscuamperfecto"],
            default=["Presente", "Perfecto"],
            help="Selecciona los tiempos que quieres ver"
        )
    
    # Aplicar filtros
    filtered_categories = []
    
    # Normalizar filtros de tiempo para coincidir con el formato de las claves (espacios -> guiones bajos)
    tiempo_filter_normalized = [t.replace(" ", "_") for t in tiempo_filter]
    
    for category in organized.keys():
        parts = category.split('_')
        modo_match = any(m in category for m in modo_filter)
        voz_match = any(v in category for v in voz_filter)
        
        # Para modos que tienen tiempo
        if parts[0] in ["Indicativo", "Subjuntivo"]:
            # Extraer el tiempo de la categoría (todo entre el modo y la voz)
            # Estructura: Modo_Tiempo_..._Voz
            if len(parts) >= 3:
                category_tiempo = "_".join(parts[1:-1])
                # Usar coincidencia exacta para evitar que "Perfecto" coincida con "Futuro_Perfecto"
                tiempo_match = category_tiempo in tiempo_filter_normalized
            else:
                tiempo_match = False
                
            if modo_match and voz_match and tiempo_match:
                filtered_categories.append(category)
        else:
            # Para modos sin tiempo (Imperativo, Infinitivo, etc.)
            if modo_match and voz_match:
                filtered_categories.append(category)
    
    if not filtered_categories:
        st.warning("No hay formas que coincidan con los filtros seleccionados.")
        return
    
    # Ordenar categorías de forma lógica
    priority_order = [
        "Indicativo_Presente_Activa",
        "Indicativo_Imperfecto_Activa",
        "Indicativo_Futuro_Imperfecto_Activa",
        "Indicativo_Futuro_Perfecto_Activa",
        "Indicativo_Perfecto_Activa",
        "Indicativo_Pluscuamperfecto_Activa",
        "Indicativo_Presente_Pasiva",
        "Indicativo_Imperfecto_Pasiva",
        "Indicativo_Futuro_Imperfecto_Pasiva",
        "Indicativo_Futuro_Perfecto_Pasiva",
        "Indicativo_Perfecto_Pasiva",
        "Indicativo_Pluscuamperfecto_Pasiva",
        "Subjuntivo_Presente_Activa",
        "Subjuntivo_Imperfecto_Activa",
        "Subjuntivo_Perfecto_Activa",
        "Subjuntivo_Pluscuamperfecto_Activa",
        "Subjuntivo_Presente_Pasiva",
        "Subjuntivo_Imperfecto_Pasiva",
        "Imperativo_Presente_Activa",
        "Imperativo_Presente_Pasiva",
    ]
    
    sorted_categories = []
    for priority in priority_order:
        if priority in filtered_categories:
            sorted_categories.append(priority)
    
    # Agregar el resto
    for cat in filtered_categories:
        if cat not in sorted_categories:
            sorted_categories.append(cat)
    
    
    # Renderizar cada categoría
    for category in sorted_categories:
        forms_in_category = organized[category]
        
        # Título de la sección
        display_name = category.replace('_', ' ')
        st.markdown(f"#### {display_name}")
        
        # Si son formas personales (tienen persona y número), usar tabla
        if any('_' in k and k.split('_')[0] in ['1', '2', '3'] for k in forms_in_category.keys()):
            # Crear tabla de conjugación usando render_styled_table
            headers = ["Persona", "Singular", "Plural"]
            rows = []
            
            for persona in ['1', '2', '3']:
                row = [f"**{persona}ª**"]
                
                # Singular
                key_sing = f"{persona}_Sing"
                if key_sing in forms_in_category:
                    row.append(forms_in_category[key_sing]['form'])
                else:
                    row.append('—')
                
                # Plural
                key_plur = f"{persona}_Plur"
                if key_plur in forms_in_category:
                    row.append(forms_in_category[key_plur]['form'])
                else:
                    row.append('—')
                
                rows.append(row)
            
            render_styled_table(headers, rows)
        else:
            # Formas no personales
            # Si es participio, mostrar como tabla de declinación
            if "Participio" in category:
                render_participle_table(forms_in_category, display_name)
            else:
                # Infinitivos, gerundios, supinos: mostrar como lista
                for subcategory, data in forms_in_category.items():
                    st.markdown(f"**{data['form']}** — {data['morph']}")
        
        st.markdown("---")
    
    # Mostrar todas las formas en detalle (expandible)
    with st.expander(f"📖 Ver todas las {paradigm['total_forms']} formas"):
        for i, form_data in enumerate(paradigm['forms'], 1):
            st.markdown(f"**{i}. {form_data['form']}** → {form_data['morph']}")

