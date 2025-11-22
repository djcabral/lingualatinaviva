"""
Analizador de textos latinos usando Stanza (Stanford NLP)

Stanza es uno de los mejores modelos para latín en 2025:
- Modelos entrenados en PROIEL, Perseus, IT-TB, UDante
- Muy precisa lematización y POS tagging
- Análisis de dependencias y NER
- Sin problemas de GPU
"""

import json
import sys
import os
from typing import List, Dict, Optional, Tuple

# Force CPU mode to avoid GPU issues
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

# Check if Stanza is available
STANZA_AVAILABLE = False
try:
    import stanza
    STANZA_AVAILABLE = True
except ImportError:
    pass


class StanzaAnalyzer:
    """Analizador de textos latinos usando Stanza"""
    
    def __init__(self):
        """Inicializa el analizador Stanza si está disponible"""
        self.nlp = None
        if STANZA_AVAILABLE:
            try:
                # Intentar cargar modelo de latín
                self.nlp = stanza.Pipeline('la', processors='tokenize,mwt,pos,lemma', use_gpu=False)
            except Exception as e:
                print(f"⚠️ Modelo de latín no descargado. Error: {e}")
                print("   Ejecuta: stanza.download('la')")
                self.nlp = None
    
    @staticmethod
    def is_available() -> bool:
        """Verifica si Stanza está disponible"""
        return STANZA_AVAILABLE
    
    @staticmethod
    def install_instructions() -> str:
        """Retorna instrucciones para instalar Stanza"""
        return """
Para usar análisis Stanza, instala las dependencias:

    pip install stanza

Luego descarga el modelo de latín:

    python -c "import stanza; stanza.download('la')"

Esto solo es necesario para ADMINISTRADORES que añaden textos nuevos.
Los usuarios finales NO necesitan Stanza instalado.
        """
    
    def analyze_text(self, text: str) -> List[Dict]:
        """
        Analiza un texto latino con Stanza
        
        Args:
            text: Texto latino a analizar
            
        Returns:
            Lista de diccionarios con análisis de cada palabra
        """
        if not self.nlp:
            raise RuntimeError("Stanza no está disponible. " + self.install_instructions())
        
        try:
            # Procesar texto con Stanza
            doc = self.nlp(text)
            
            results = []
            position = 0
            
            for sentence in doc.sentences:
                for word in sentence.words:
                    # Verificar si es puntuación
                    is_punct = word.upos == 'PUNCT'
                    
                    # Extraer información morfológica
                    analysis = {
                        "position": position,
                        "form": word.text,
                        "lemma": word.lemma if word.lemma else word.text,
                        "pos": self._normalize_pos(word.upos),
                        "morphology": self._extract_morphology(word),
                        "is_punctuation": is_punct
                    }
                    
                    results.append(analysis)
                    position += 1
            
            return results
            
        except Exception as e:
            print(f"❌ Error al analizar texto con Stanza: {e}")
            raise
    
    def _normalize_pos(self, upos: Optional[str]) -> str:
        """Normaliza etiquetas POS de Stanza a nuestro sistema"""
        if not upos:
            return "unknown"
        
        pos_map = {
            "NOUN": "noun",
            "VERB": "verb",
            "ADJ": "adjective",
            "ADV": "adverb",
            "PRON": "pronoun",
            "DET": "determiner",
            "ADP": "preposition",
            "CCONJ": "conjunction",
            "SCONJ": "conjunction",
            "INTJ": "interjection",
            "NUM": "numeral",
            "PROPN": "proper_noun",
            "PUNCT": "punctuation"
        }
        
        return pos_map.get(upos, upos.lower())
    
    def _extract_morphology(self, word) -> Dict:
        """Extrae información morfológica de una palabra Stanza"""
        morph = {}
        
        # Stanza ya tiene feats parseado como dict
        if word.feats:
            # Parse feats format: "Case=Nom|Number=Sing|Gender=Fem"
            for feat_pair in word.feats.split('|'):
                if '=' in feat_pair:
                    key, value = feat_pair.split('=', 1)
                    morph[key.lower()] = value.lower()
        
        return morph
    
    def format_morphology_spanish(self, morphology: Dict, pos: str) -> str:
        """Formatea morfología en español para mostrar al usuario"""
        parts = []
        
        # Caso
        if 'case' in morphology:
            case_map = {
                'nom': 'nominativo',
                'gen': 'genitivo',
                'dat': 'dativo',
                'acc': 'acusativo',
                'abl': 'ablativo',
                'voc': 'vocativo',
                'loc': 'locativo'
            }
            parts.append(case_map.get(morphology['case'], morphology['case']))
        
        # Número
        if 'number' in morphology:
            number_map = {'sing': 'singular', 'plur': 'plural'}
            parts.append(number_map.get(morphology['number'], morphology['number']))
        
        # Género
        if 'gender' in morphology:
            gender_map = {'masc': 'masculino', 'fem': 'femenino', 'neut': 'neutro'}
            parts.append(gender_map.get(morphology['gender'], morphology['gender']))
        
        # Tiempo
        if 'tense' in morphology:
            tense_map = {
                'pres': 'presente',
                'past': 'pasado',
                'impf': 'imperfecto',
                'fut': 'futuro',
                'perf': 'perfecto',
                'plup': 'pluscuamperfecto',
                'futp': 'futuro perfecto'
            }
            parts.append(tense_map.get(morphology['tense'], morphology['tense']))
        
        # Modo
        if 'mood' in morphology:
            mood_map = {
                'ind': 'indicativo',
                'sub': 'subjuntivo',
                'imp': 'imperativo',
                'inf': 'infinitivo',
                'part': 'participio'
            }
            parts.append(mood_map.get(morphology['mood'], morphology['mood']))
        
        # Voz
        if 'voice' in morphology:
            voice_map = {'act': 'activa', 'pass': 'pasiva'}
            parts.append(voice_map.get(morphology['voice'], morphology['voice']))
        
        # Persona
        if 'person' in morphology:
            parts.append(f"{morphology['person']}ª persona")
        
        return ' '.join(parts) if parts else 'invariable'


def analyze_and_save_text(text_id: int, text_content: str, session) -> Tuple[int, int]:
    """
    Analiza un texto con Stanza y guarda el análisis en TextWordLink
    
    Args:
        text_id: ID del texto en la base de datos
        text_content: Contenido del texto a analizar
        session: Sesión de SQLModel
        
    Returns:
        Tupla (palabras_analizadas, palabras_guardadas)
    """
    from database.models import TextWordLink, Word
    from sqlmodel import select
    from utils.latin_logic import LatinMorphology
    from sqlalchemy import text as sql_text
    
    # Verificar si Stanza está disponible
    if not StanzaAnalyzer.is_available():
        raise RuntimeError(
            "Stanza no está disponible.\n" + 
            StanzaAnalyzer.install_instructions()
        )
    
    # Limpiar análisis anteriores (usar raw SQL para evitar problemas)
    session.exec(sql_text(f"DELETE FROM textwordlink WHERE text_id = {text_id}"))
    session.commit()
    
    # Analizar con Stanza
    analyzer = StanzaAnalyzer()
    analyses = analyzer.analyze_text(text_content)
    
    print(f"📊 Texto analizado: {len(analyses)} tokens encontrados")
    
    saved_count = 0
    
    for analysis in analyses:
        # Intentar encontrar palabra en vocabulario
        normalized_lemma = LatinMorphology.normalize_latin(analysis['lemma'])
        
        word = session.exec(
            select(Word).where(
                (Word.latin == analysis['lemma']) |
                (Word.latin == normalized_lemma)
            )
        ).first()
        
        # Preparar datos para INSERT
        word_id_value = word.id if word else None
        morphology_str = json.dumps(analysis['morphology'])
        
        # Guardar notes si no está en vocabulario
        notes_str = None
        if not word:
            notes_str = json.dumps({
                "lemma": analysis['lemma'],
                "pos": analysis['pos'],
                "stanza_analysis": True
            })
        
        # Usar raw SQL INSERT con cursor directo de SQLite
        # Esto evita problemas de metadata caching de SQLAlchemy
        import sqlite3
        db_path = 'data/latin_learning.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO textwordlink 
            (text_id, word_id, sentence_number, position_in_sentence, form, morphology_json, syntax_role, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            text_id,
            word_id_value,
            1,
            analysis['position'],
            analysis['form'],
            morphology_str,
            None,
            notes_str
        ))
        
        conn.commit()
        conn.close()
        
        saved_count += 1
    
    session.commit()
    
    print(f"✅ {saved_count} análisis guardados en base de datos")
    
    return len(analyses), saved_count
