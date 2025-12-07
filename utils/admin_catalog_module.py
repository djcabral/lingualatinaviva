"""
Módulo de Administración de Catalogación - Independiente
Gestiona importación de resultados del catalogador integral
Puede funcionar de forma autónoma o integrada en el admin principal
"""

import streamlit as st
import json
import sqlite3
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import pandas as pd

logger = logging.getLogger(__name__)


class CatalogAdminModule:
    """Módulo admin para catalogación - independiente y modular"""
    
    def __init__(self, db_path: str = "lingua_latina.db"):
        self.db_path = db_path
        self.is_available = self._check_availability()
    
    def _check_availability(self) -> bool:
        """Detecta si el módulo de catalogación está disponible"""
        try:
            # Verifica que exista la BD
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='word'")
            exists = cursor.fetchone() is not None
            conn.close()
            return exists
        except Exception as e:
            logger.warning(f"Catalogación no disponible: {e}")
            return False
    
    def render_dashboard(self):
        """Renderiza dashboard de catalogación"""
        st.markdown("### 📊 Dashboard de Catalogación")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Estadísticas
            cursor.execute("SELECT COUNT(*) FROM word")
            total_words = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM text")
            total_texts = cursor.fetchone()[0]
            
            cursor.execute("SELECT level, COUNT(*) FROM word GROUP BY level ORDER BY level")
            level_dist = dict(cursor.fetchall())
            
            conn.close()
            
            # Mostrar métricas
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📚 Palabras", total_words)
            
            with col2:
                st.metric("📝 Textos", total_texts)
            
            with col3:
                st.metric("🕐 Última Actualización", datetime.now().strftime("%H:%M"))
            
            # Gráfico de distribución
            if level_dist:
                st.markdown("**Distribución por Nivel:**")
                level_data = {f"Nivel {k}": v for k, v in sorted(level_dist.items())}
                st.bar_chart(level_data)
        
        except Exception as e:
            st.error(f"Error al cargar estadísticas: {e}")
    
    def render_import_section(self):
        """Renderiza sección de importación de catalogación"""
        st.markdown("### 📥 Importar Resultados del Catalogador")
        
        st.info("""
        **Cómo usar:**
        1. Ejecuta: `python catalog_tool.py process --input texto.json`
        2. Sube el archivo JSON resultante aquí
        3. Los datos se importan automáticamente a la BD
        """)
        
        tab1, tab2 = st.tabs(["📁 Subir Archivo", "📝 Entrada Manual"])
        
        with tab1:
            st.markdown("**Sube un archivo JSON del catalogador:**")
            uploaded_file = st.file_uploader(
                "Selecciona archivo JSON",
                type=["json"],
                key="catalog_upload"
            )
            
            if uploaded_file is not None:
                try:
                    catalog_data = json.load(uploaded_file)
                    self._show_preview_and_import(catalog_data)
                except json.JSONDecodeError:
                    st.error("❌ Archivo JSON inválido")
        
        with tab2:
            st.markdown("**O ingresa JSON manualmente:**")
            json_input = st.text_area(
                "JSON",
                placeholder='{"vocabulary": [...], "sentences": [...]}',
                height=200,
                key="catalog_json"
            )
            
            if json_input and st.button("Importar JSON", type="primary"):
                try:
                    catalog_data = json.loads(json_input)
                    self._show_preview_and_import(catalog_data)
                except json.JSONDecodeError:
                    st.error("❌ JSON inválido")
    
    def _show_preview_and_import(self, catalog_data: Dict[str, Any]):
        """Muestra preview e importa datos"""
        vocab_count = len(catalog_data.get('vocabulary', []))
        sent_count = len(catalog_data.get('sentences', []))
        
        st.markdown("**📋 Vista Previa:**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Palabras a importar:** {vocab_count}")
            if vocab_count > 0:
                for word in catalog_data['vocabulary'][:3]:
                    st.caption(f"• {word.get('word', '')} → {word.get('translation', '')}")
                if vocab_count > 3:
                    st.caption(f"• ... y {vocab_count - 3} más")
        
        with col2:
            st.write(f"**Sentencias a importar:** {sent_count}")
            if sent_count > 0:
                for sent in catalog_data['sentences'][:2]:
                    st.caption(f"• {sent.get('text', '')[:50]}...")
                if sent_count > 2:
                    st.caption(f"• ... y {sent_count - 2} más")
        
        st.divider()
        
        if st.button("✓ Importar Todo", type="primary", use_container_width=True):
            with st.spinner("📥 Importando..."):
                results = self._import_to_db(catalog_data)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("✅ Palabras", results['vocab_imported'])
                with col2:
                    st.metric("✅ Sentencias", results['sent_imported'])
                with col3:
                    st.metric("⚠️ Errores", len(results['errors']))
                
                if results['errors']:
                    with st.expander("Ver errores"):
                        for error in results['errors']:
                            st.write(f"• {error}")
                else:
                    st.success("✅ Importación exitosa")
    
    def _import_to_db(self, catalog_data: Dict[str, Any]) -> Dict[str, Any]:
        """Importa datos a BD"""
        results = {
            'vocab_imported': 0,
            'sent_imported': 0,
            'errors': []
        }
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Importar vocabulario
            for word_data in catalog_data.get('vocabulary', []):
                try:
                    cursor.execute("""
                        INSERT OR IGNORE INTO word (latin, translation, part_of_speech, level)
                        VALUES (?, ?, ?, ?)
                    """, (
                        word_data.get('lemma', word_data.get('word', '')),
                        word_data.get('translation', ''),
                        word_data.get('pos', 'noun'),
                        1
                    ))
                    results['vocab_imported'] += cursor.rowcount
                except Exception as e:
                    results['errors'].append(f"Palabra: {e}")
            
            # Importar sentencias
            for sent_data in catalog_data.get('sentences', []):
                try:
                    cursor.execute("""
                        INSERT OR IGNORE INTO text (content, translation, level)
                        VALUES (?, ?, ?)
                    """, (
                        sent_data.get('text', ''),
                        sent_data.get('translation', ''),
                        1
                    ))
                    results['sent_imported'] += cursor.rowcount
                except Exception as e:
                    results['errors'].append(f"Sentencia: {e}")
            
            conn.commit()
            conn.close()
        
        except Exception as e:
            results['errors'].append(f"Error crítico: {e}")
        
        return results
    
    def render(self, section: str) -> bool:
        """
        Renderiza el módulo si está disponible
        Retorna True si se renderizó, False si no está disponible
        """
        if not self.is_available:
            return False
        
        if section == "Catalogación":
            st.markdown("## 📥 Catalogación Integral")
            
            tab1, tab2 = st.tabs(["📊 Dashboard", "📥 Importar"])
            
            with tab1:
                self.render_dashboard()
            
            with tab2:
                self.render_import_section()
            
            return True
        
        return False


def get_catalog_module() -> Optional[CatalogAdminModule]:
    """Factory para obtener el módulo si está disponible"""
    module = CatalogAdminModule()
    return module if module.is_available else None
