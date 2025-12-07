"""
Panel de Administración Mejorado - Lingua Latina Viva
Gestión integrada de vocabulario, sentencias y catalogación
Autenticación simple, SQLite local
"""

import streamlit as st
import sys
import os
import json
import pandas as pd
from datetime import datetime

# Setup paths
root_path = os.path.dirname(os.path.dirname(__file__))
if root_path not in sys.path:
    sys.path.append(root_path)

from utils.admin_manager import (
    AdminVocabularyManager, 
    AdminSentenceManager,
    CatalogationImporter,
    AdminDashboard
)
from utils.ui_helpers import load_css

# Page config
st.set_page_config(
    page_title="Admin Panel",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()

# ========================
# AUTENTICACIÓN SIMPLE
# ========================

if 'admin_authenticated' not in st.session_state:
    st.session_state.admin_authenticated = False

if not st.session_state.admin_authenticated:
    st.markdown("""
    <div style='text-align: center; padding: 80px 20px;'>
        <h1 style='font-family: "Cinzel", serif; margin-bottom: 40px;'>
            🔒 Panel Administrativo
        </h1>
        <p style='font-size: 1.2em; color: #666;'>Acceso restringido</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password = st.text_input("🔐 Contraseña", type="password", key="admin_pass")
        if st.button("✓ Entrar", use_container_width=True, type="primary"):
            # Contraseña simple (cambiar en producción)
            if password == "admin":
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error("❌ Contraseña incorrecta")
    
    st.info("""
    **Demo:** Usa contraseña `admin` para acceder.
    En producción, implementar autenticación más robusta.
    """)
    st.stop()

# ========================
# HEADER Y LOGOUT
# ========================

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.markdown("""
    <h1 style='font-family: "Cinzel", serif; margin: 0;'>
        🔧 Panel Admin
    </h1>
    """, unsafe_allow_html=True)

with col3:
    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state.admin_authenticated = False
        st.rerun()

st.divider()

# ========================
# NAVEGACIÓN LATERAL
# ========================

section = st.sidebar.radio(
    "📋 Secciones",
    [
        "📊 Dashboard",
        "📚 Vocabulario",
        "📝 Sentencias",
        "📥 Importar Catalogación",
        "⚙️ Configuración"
    ],
    index=0
)

st.sidebar.divider()
st.sidebar.info("""
**Panel de Administración**

Gestiona vocabulario, sentencias y resultados del catalogador.

- ✏️ Agregar/Editar/Eliminar
- 🔍 Buscar contenido
- 📥 Importar catálogos
- 📊 Ver estadísticas
""")

# ========================
# INICIALIZAR MANAGERS
# ========================

vocab_mgr = AdminVocabularyManager()
sent_mgr = AdminSentenceManager()
catalog_importer = CatalogationImporter()
dashboard = AdminDashboard()

# ========================
# SECCIÓN: DASHBOARD
# ========================

if section == "📊 Dashboard":
    st.markdown("## 📊 Dashboard de Administración")
    
    stats = dashboard.get_stats()
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📚 Total Palabras",
            stats.get('total_words', 0),
            delta=None
        )
    
    with col2:
        st.metric(
            "📝 Total Sentencias",
            stats.get('total_sentences', 0),
            delta=None
        )
    
    with col3:
        st.metric(
            "📖 Total Lecciones",
            stats.get('total_lessons', 0),
            delta=None
        )
    
    with col4:
        st.metric(
            "🕐 Última Actualización",
            datetime.now().strftime("%H:%M"),
            delta=None
        )
    
    st.divider()
    
    # Distribución por nivel
    if stats.get('words_by_level'):
        st.markdown("### 📊 Palabras por Nivel")
        level_data = stats['words_by_level']
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.bar_chart(level_data)
        with col2:
            st.markdown("**Resumen:**")
            for level, count in level_data.items():
                st.write(f"- {level}: {count}")

# ========================
# SECCIÓN: VOCABULARIO
# ========================

elif section == "📚 Vocabulario":
    st.markdown("## 📚 Gestión de Vocabulario")
    
    tab1, tab2, tab3 = st.tabs(["➕ Agregar", "📖 Listar", "🔍 Buscar"])
    
    # TAB 1: AGREGAR
    with tab1:
        st.markdown("### ➕ Agregar Nueva Palabra")
        
        col1, col2 = st.columns(2)
        
        with col1:
            latin = st.text_input("🔤 Palabra Latina", placeholder="rosa")
            translation = st.text_input("🔤 Traducción", placeholder="rosa")
            pos = st.selectbox(
                "📝 Parte de Oración",
                ["noun", "verb", "adjective", "adverb", "preposition", "conjunction"]
            )
        
        with col2:
            level = st.slider("📍 Nivel", 1, 5, 1)
            gender = st.selectbox("⚧ Género", ["", "m", "f", "n"])
            genitive = st.text_input("🔤 Genitivo", placeholder="rosae")
        
        if st.button("✓ Agregar Palabra", type="primary", use_container_width=True):
            if latin and translation:
                if vocab_mgr.add_vocabulary(latin, translation, pos, level, gender, genitive):
                    st.success(f"✅ Palabra '{latin}' agregada correctamente")
                else:
                    st.error("❌ Error al agregar la palabra")
            else:
                st.warning("⚠️ Completa los campos requeridos")
    
    # TAB 2: LISTAR
    with tab2:
        st.markdown("### 📖 Vocabulario Completo")
        
        all_vocab = vocab_mgr.get_all_vocabulary()
        
        if all_vocab:
            df = pd.DataFrame(all_vocab)
            
            # Configurar visualización
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    'id': st.column_config.NumberColumn("ID", width=40),
                    'latin': st.column_config.TextColumn("Palabra"),
                    'translation': st.column_config.TextColumn("Traducción"),
                    'part_of_speech': st.column_config.TextColumn("POS"),
                    'level': st.column_config.NumberColumn("Nivel"),
                    'gender': st.column_config.TextColumn("Género"),
                    'genitive': st.column_config.TextColumn("Genitivo"),
                }
            )
            
            st.info(f"📊 Total: {len(all_vocab)} palabras")
        else:
            st.info("📭 No hay palabras registradas aún")
    
    # TAB 3: BUSCAR
    with tab3:
        st.markdown("### 🔍 Buscar Palabra")
        
        search_query = st.text_input("🔍 Buscar por palabra o traducción")
        
        if search_query:
            results = vocab_mgr.search_vocabulary(search_query)
            
            if results:
                st.success(f"📍 {len(results)} resultado(s) encontrado(s)")
                
                for word in results:
                    with st.container(border=True):
                        col1, col2, col3 = st.columns([2, 1, 1])
                        
                        with col1:
                            st.markdown(f"**{word['latin']}** → *{word['translation']}*")
                            st.caption(f"POS: {word['part_of_speech']} | Nivel: {word['level']}")
                        
                        with col2:
                            if st.button("✏️ Editar", key=f"edit_{word['id']}"):
                                st.session_state.edit_word_id = word['id']
                                st.rerun()
                        
                        with col3:
                            if st.button("🗑️ Eliminar", key=f"del_{word['id']}"):
                                if vocab_mgr.delete_vocabulary(word['id']):
                                    st.success("✅ Palabra eliminada")
                                    st.rerun()
            else:
                st.info("🔍 No se encontraron resultados")

# ========================
# SECCIÓN: SENTENCIAS
# ========================

elif section == "📝 Sentencias":
    st.markdown("## 📝 Gestión de Sentencias")
    
    tab1, tab2 = st.tabs(["➕ Agregar", "📖 Listar"])
    
    # TAB 1: AGREGAR
    with tab1:
        st.markdown("### ➕ Agregar Nueva Sentencia")
        
        text = st.text_area(
            "📜 Texto Latino",
            placeholder="Rosa est pulchra.",
            height=100
        )
        
        translation = st.text_area(
            "🔤 Traducción",
            placeholder="La rosa es hermosa.",
            height=80
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            level = st.slider("📍 Nivel", 1, 5, 1)
            source = st.text_input("📚 Fuente", placeholder="Liber Exemplorum")
        
        with col2:
            grammatical_notes = st.text_area(
                "📝 Notas Gramaticales",
                placeholder="Nominativo singular, predicado nominal",
                height=80
            )
        
        if st.button("✓ Agregar Sentencia", type="primary", use_container_width=True):
            if text and translation:
                if sent_mgr.add_sentence(text, translation, level, source, grammatical_notes):
                    st.success("✅ Sentencia agregada correctamente")
                else:
                    st.error("❌ Error al agregar la sentencia")
            else:
                st.warning("⚠️ Completa los campos requeridos")
    
    # TAB 2: LISTAR
    with tab2:
        st.markdown("### 📖 Sentencias Registradas")
        
        all_sentences = sent_mgr.get_all_sentences(limit=50)
        
        if all_sentences:
            for sent in all_sentences:
                with st.container(border=True):
                    col1, col2 = st.columns([1, 0.2])
                    
                    with col1:
                        st.markdown(f"**{sent['content']}**")
                        st.markdown(f"*{sent['translation']}*")
                        
                        meta = []
                        if sent['source']:
                            meta.append(f"📚 {sent['source']}")
                        if sent['level']:
                            meta.append(f"📍 Nivel {sent['level']}")
                        if meta:
                            st.caption(" | ".join(meta))
                        
                        if sent['notes']:
                            st.info(f"📝 {sent['notes']}")
                    
                    with col2:
                        if st.button("🗑️", key=f"del_sent_{sent['id']}"):
                            if sent_mgr.delete_sentence(sent['id']):
                                st.success("✅ Eliminada")
                                st.rerun()
            
            st.info(f"📊 Total: {len(all_sentences)} sentencias")
        else:
            st.info("📭 No hay sentencias registradas")

# ========================
# SECCIÓN: IMPORTAR CATALOGACIÓN
# ========================

elif section == "📥 Importar Catalogación":
    st.markdown("## 📥 Importar Resultados del Catalogador")
    
    st.info("""
    **Cómo usar:**
    1. Ejecuta el catalogador: `python catalog_tool.py process --input texto.json`
    2. Sube el archivo JSON de resultados aquí
    3. Los resultados se importarán automáticamente a la BD
    """)
    
    # Opción 1: Upload de archivo
    st.markdown("### 1️⃣ Subir archivo JSON")
    uploaded_file = st.file_uploader(
        "📁 Selecciona archivo JSON del catalogador",
        type=["json"],
        help="Archivo generado por catalog_tool.py"
    )
    
    if uploaded_file is not None:
        try:
            catalog_data = json.load(uploaded_file)
            
            st.markdown("### 📋 Vista Previa del Contenido")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Vocabulario:**")
                if 'vocabulary' in catalog_data:
                    st.write(f"- {len(catalog_data['vocabulary'])} palabras")
                    # Mostrar primeras 5
                    for word in catalog_data['vocabulary'][:5]:
                        st.write(f"  - {word.get('word', '')} → {word.get('translation', '')}")
                else:
                    st.write("- Sin vocabulario")
            
            with col2:
                st.markdown("**Sentencias:**")
                if 'sentences' in catalog_data:
                    st.write(f"- {len(catalog_data['sentences'])} sentencias")
                else:
                    st.write("- Sin sentencias")
            
            st.divider()
            
            if st.button("✓ Importar Todo", type="primary", use_container_width=True):
                with st.spinner("📥 Importando..."):
                    results = catalog_importer.import_catalog_results(catalog_data)
                    
                    st.markdown("### ✅ Resultados de Importación")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("📚 Palabras Importadas", results['imported_vocab'])
                    
                    with col2:
                        st.metric("📝 Sentencias Importadas", results['imported_sentences'])
                    
                    with col3:
                        st.metric("⚠️ Errores", len(results['errors']))
                    
                    if results['errors']:
                        st.warning("⚠️ Se encontraron errores:")
                        for error in results['errors']:
                            st.write(f"- {error}")
                    else:
                        st.success("✅ ¡Importación exitosa!")
        
        except json.JSONDecodeError:
            st.error("❌ Archivo JSON inválido")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    st.divider()
    
    # Opción 2: Entrada manual
    st.markdown("### 2️⃣ O ingresa JSON manualmente")
    
    json_input = st.text_area(
        "📝 JSON del catalogador",
        placeholder='{"vocabulary": [...], "sentences": [...]}',
        height=200
    )
    
    if json_input and st.button("✓ Importar desde JSON", type="secondary"):
        try:
            catalog_data = json.loads(json_input)
            results = catalog_importer.import_catalog_results(catalog_data)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("📚 Palabras", results['imported_vocab'])
            with col2:
                st.metric("📝 Sentencias", results['imported_sentences'])
            
            st.success("✅ Importación completada")
        except json.JSONDecodeError:
            st.error("❌ JSON inválido")

# ========================
# SECCIÓN: CONFIGURACIÓN
# ========================

elif section == "⚙️ Configuración":
    st.markdown("## ⚙️ Configuración del Panel")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Información de Base de Datos")
        
        try:
            stats = dashboard.get_stats()
            st.write(f"**Total de Palabras:** {stats.get('total_words', 0)}")
            st.write(f"**Total de Sentencias:** {stats.get('total_sentences', 0)}")
            st.write(f"**Total de Lecciones:** {stats.get('total_lessons', 0)}")
        except:
            st.warning("No se pudo conectar a la BD")
    
    with col2:
        st.markdown("### 🔐 Seguridad")
        st.info("""
        **Recomendaciones:**
        - Cambiar contraseña regularmente
        - Usar contraseña fuerte
        - Hacer respaldos periódicos
        - Registrar cambios importantes
        """)
    
    st.divider()
    
    st.markdown("### 📝 Sobre este Panel")
    st.markdown("""
    **Panel Administrativo - Lingua Latina Viva**
    
    - ✅ Administración local (SQLite)
    - ✅ Integración con catalogador
    - ✅ CRUD completo
    - ✅ Autenticación simple
    
    **Versión:** 1.0 | **Fecha:** 2025-12-07
    """)
