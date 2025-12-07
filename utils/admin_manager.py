"""
Admin Manager - Gestión de CRUD para administración de contenido latinao
Integración con catalogación integral y BD SQLite
"""

import sqlite3
import json
from typing import List, Dict, Any, Optional
from dataclasses import asdict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class AdminVocabularyManager:
    """Gestor CRUD para vocabulario en administración"""
    
    def __init__(self, db_path: str = "lingua_latina.db"):
        self.db_path = db_path
    
    def get_connection(self):
        """Obtener conexión a BD"""
        return sqlite3.connect(self.db_path)
    
    def add_vocabulary(self, latin: str, translation: str, pos: str, 
                       level: int = 1, gender: str = "", genitive: str = "") -> bool:
        """Agregar palabra al vocabulario"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO word (latin, translation, part_of_speech, level, gender, genitive)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (latin, translation, pos, level, gender, genitive))
            
            conn.commit()
            conn.close()
            logger.info(f"✅ Palabra agregada: {latin}")
            return True
        except Exception as e:
            logger.error(f"❌ Error al agregar palabra: {e}")
            return False
    
    def update_vocabulary(self, word_id: int, latin: str, translation: str, 
                         pos: str, level: int = 1, gender: str = "", genitive: str = "") -> bool:
        """Actualizar palabra existente"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE word 
                SET latin = ?, translation = ?, part_of_speech = ?, level = ?, gender = ?, genitive = ?
                WHERE id = ?
            """, (latin, translation, pos, level, gender, genitive, word_id))
            
            conn.commit()
            conn.close()
            logger.info(f"✅ Palabra actualizada: {latin}")
            return True
        except Exception as e:
            logger.error(f"❌ Error al actualizar palabra: {e}")
            return False
    
    def delete_vocabulary(self, word_id: int) -> bool:
        """Eliminar palabra"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM word WHERE id = ?", (word_id,))
            
            conn.commit()
            conn.close()
            logger.info(f"✅ Palabra eliminada: ID {word_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Error al eliminar palabra: {e}")
            return False
    
    def get_all_vocabulary(self) -> List[Dict[str, Any]]:
        """Obtener todo el vocabulario"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, latin, translation, part_of_speech, level, gender, genitive
                FROM word
                ORDER BY latin
            """)
            
            rows = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'id': row[0],
                    'latin': row[1],
                    'translation': row[2],
                    'part_of_speech': row[3],
                    'level': row[4],
                    'gender': row[5],
                    'genitive': row[6]
                }
                for row in rows
            ]
        except Exception as e:
            logger.error(f"❌ Error al obtener vocabulario: {e}")
            return []
    
    def search_vocabulary(self, query: str) -> List[Dict[str, Any]]:
        """Buscar palabras"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, latin, translation, part_of_speech, level, gender, genitive
                FROM word
                WHERE latin LIKE ? OR translation LIKE ?
                ORDER BY latin
            """, (f"%{query}%", f"%{query}%"))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'id': row[0],
                    'latin': row[1],
                    'translation': row[2],
                    'part_of_speech': row[3],
                    'level': row[4],
                    'gender': row[5],
                    'genitive': row[6]
                }
                for row in rows
            ]
        except Exception as e:
            logger.error(f"❌ Error en búsqueda: {e}")
            return []


class AdminSentenceManager:
    """Gestor CRUD para sentencias"""
    
    def __init__(self, db_path: str = "lingua_latina.db"):
        self.db_path = db_path
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def add_sentence(self, text: str, translation: str, level: int = 1, 
                    source: str = "", grammatical_notes: str = "") -> bool:
        """Agregar sentencia"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO text (content, translation, level, source, notes)
                VALUES (?, ?, ?, ?, ?)
            """, (text, translation, level, source, grammatical_notes))
            
            conn.commit()
            conn.close()
            logger.info(f"✅ Sentencia agregada: {text[:50]}")
            return True
        except Exception as e:
            logger.error(f"❌ Error al agregar sentencia: {e}")
            return False
    
    def update_sentence(self, sentence_id: int, text: str, translation: str, 
                       level: int = 1, source: str = "", grammatical_notes: str = "") -> bool:
        """Actualizar sentencia"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE text 
                SET content = ?, translation = ?, level = ?, source = ?, notes = ?
                WHERE id = ?
            """, (text, translation, level, source, grammatical_notes, sentence_id))
            
            conn.commit()
            conn.close()
            logger.info(f"✅ Sentencia actualizada: ID {sentence_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Error al actualizar sentencia: {e}")
            return False
    
    def delete_sentence(self, sentence_id: int) -> bool:
        """Eliminar sentencia"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM text WHERE id = ?", (sentence_id,))
            
            conn.commit()
            conn.close()
            logger.info(f"✅ Sentencia eliminada: ID {sentence_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Error al eliminar sentencia: {e}")
            return False
    
    def get_all_sentences(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Obtener sentencias"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, content, translation, level, source, notes
                FROM text
                LIMIT ?
            """, (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'id': row[0],
                    'content': row[1],
                    'translation': row[2],
                    'level': row[3],
                    'source': row[4],
                    'notes': row[5]
                }
                for row in rows
            ]
        except Exception as e:
            logger.error(f"❌ Error al obtener sentencias: {e}")
            return []


class CatalogationImporter:
    """Importar resultados del catalogador a la BD"""
    
    def __init__(self, db_path: str = "lingua_latina.db"):
        self.db_path = db_path
        self.vocab_mgr = AdminVocabularyManager(db_path)
        self.sent_mgr = AdminSentenceManager(db_path)
    
    def import_catalog_results(self, catalog_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Importar resultados completos del catalogador
        catalog_json formato esperado:
        {
            'text': str,
            'sentences': [...],
            'vocabulary': [
                {
                    'word': str,
                    'lemma': str,
                    'pos': str,
                    'translation': str,
                    'morphology': {...},
                    'syntax': {...},
                    'semantics': {...}
                }
            ]
        }
        """
        results = {
            'imported_vocab': 0,
            'imported_sentences': 0,
            'errors': []
        }
        
        try:
            # Importar vocabulario
            if 'vocabulary' in catalog_json:
                for word_data in catalog_json['vocabulary']:
                    try:
                        success = self.vocab_mgr.add_vocabulary(
                            latin=word_data.get('lemma', word_data.get('word', '')),
                            translation=word_data.get('translation', ''),
                            pos=word_data.get('pos', 'noun'),
                            level=1
                        )
                        if success:
                            results['imported_vocab'] += 1
                    except Exception as e:
                        results['errors'].append(f"Error importando palabra: {e}")
            
            # Importar sentencias
            if 'sentences' in catalog_json:
                for sent_data in catalog_json['sentences']:
                    try:
                        success = self.sent_mgr.add_sentence(
                            text=sent_data.get('text', ''),
                            translation=sent_data.get('translation', ''),
                            level=1,
                            source=sent_data.get('source', 'catalogation')
                        )
                        if success:
                            results['imported_sentences'] += 1
                    except Exception as e:
                        results['errors'].append(f"Error importando sentencia: {e}")
            
            logger.info(f"✅ Importación completada: {results['imported_vocab']} palabras, {results['imported_sentences']} sentencias")
            
        except Exception as e:
            logger.error(f"❌ Error crítico en importación: {e}")
            results['errors'].append(str(e))
        
        return results
    
    def import_from_file(self, file_path: str) -> Dict[str, Any]:
        """Importar desde archivo JSON del catalogador"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return self.import_catalog_results(data)
        except Exception as e:
            logger.error(f"❌ Error al leer archivo: {e}")
            return {'imported_vocab': 0, 'imported_sentences': 0, 'errors': [str(e)]}


class AdminDashboard:
    """Dashboard con estadísticas de administración"""
    
    def __init__(self, db_path: str = "lingua_latina.db"):
        self.db_path = db_path
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas generales"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Contar palabras
            cursor.execute("SELECT COUNT(*) FROM word")
            total_words = cursor.fetchone()[0]
            
            # Contar sentencias
            cursor.execute("SELECT COUNT(*) FROM text")
            total_sentences = cursor.fetchone()[0]
            
            # Contar lecciones
            cursor.execute("SELECT COUNT(*) FROM lesson")
            total_lessons = cursor.fetchone()[0]
            
            # Palabras por nivel
            cursor.execute("""
                SELECT level, COUNT(*) FROM word GROUP BY level ORDER BY level
            """)
            words_by_level = {f"Nivel {row[0]}": row[1] for row in cursor.fetchall()}
            
            conn.close()
            
            return {
                'total_words': total_words,
                'total_sentences': total_sentences,
                'total_lessons': total_lessons,
                'words_by_level': words_by_level,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Error al obtener estadísticas: {e}")
            return {}
    
    def get_recent_imports(self) -> List[Dict[str, Any]]:
        """Obtener importaciones recientes (placeholder)"""
        return [
            {
                'date': datetime.now().isoformat(),
                'type': 'manual',
                'items': 0,
                'status': 'ready'
            }
        ]
