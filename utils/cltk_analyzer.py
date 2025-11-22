"""
Analizador de textos latinos usando CLTK (Classical Language Toolkit)

Este módulo usa CLTK como dependencia opcional para analizar textos.
El análisis se guarda en TextWordLink para uso posterior sin necesidad de CLTK.
"""

import json
import sys
import os
from typing import List, Dict, Optional, Tuple

# Check if CLTK is available
CLTK_AVAILABLE = False
try:
    from cltk import NLP
    from cltk.languages.utils import get_lang
    CLTK_AVAILABLE = True
except ImportError:
    pass


class CLTKAnalyzer:
    """Analizador de textos latinos usando CLTK"""
    
    def __init__(self):
        """Inicializa el analizador CLTK si está disponible"""
        self.nlp = None
        if CLTK_AVAILABLE:
            try:
                self.nlp = NLP(language="lat", suppress_banner=True)
            except Exception as e:
                print(f"⚠️  Error al inicializar CLTK: {e}")
                self.nlp = None
    
    @staticmethod
    def is_available() -> bool:
        """Verifica si CLTK está disponible"""
        return CLTK_AVAILABLE
    
    @staticmethod
    def install_instructions() -> str:
        """Retorna instrucciones para instalar CLTK"""
        return """
Para usar análisis CLTK, instala las dependencias:

    pip install cltk

La primera vez que uses CLTK, descargará modelos (~250MB).
Esto solo es necesario para ADMINISTRADORES que añaden textos nuevos.
Los usuarios finales NO necesitan CLTK instalado.
        """
    
    def analyze_text(self, text: str) -> List[Dict]:
        """
        Analiza un texto latino con CLTK
        
        Args:
            text: Texto latino a analizar
            
        Returns:
            Lista de diccionarios con análisis de cada palabra:
            [
                {
                    "form": "forma original",
                    "lemma": "lema",
                    "pos": "parte del discurso",
                    "morphology": {...},
                    "is_punctuation": bool
                },
                ...
            ]
        """
        if not self.nlp:
            raise RuntimeError("CLTK no está disponible. " + self.install_instructions())
        
        try:
            # Procesar texto con CLTK
            doc = self.nlp.analyze(text=text)
            
            results = []
            position = 0
            
            for word in doc.words:
                # Extraer información morfológica
                analysis = {
                    "position": position,
                    "form": word.string,
                    "lemma": word.lemma if hasattr(word, 'lemma') else word.string,
                    "pos": self._normalize_pos(word.upos if hasattr(word, 'upos') else None),
                    "morphology": self._extract_morphology(word),
                    "is_punctuation": self._is_punctuation(word.string)
                }
                
                results.append(analysis)
                position += 1
            
            return results
            
        except Exception as e:
            print(f"❌ Error al analizar texto con CLTK: {e}")
            raise
    
    def _normalize_pos(self, upos: Optional[str]) -> str:
        """Normaliza etiquetas POS de CLTK a nuestro sistema"""
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
            "PROPN": "proper_noun"
        }
        
        return pos_map.get(upos, upos.lower())
    
    def _extract_morphology(self, word) -> Dict:
        """Extrae información morfológica de una palabra CLTK"""
        morph = {}
        
        # Extraer características morfológicas si existen
        if hasattr(word, 'feats') and word.feats:
            # CLTK usa formato "Case=Nom|Number=Sing|Gender=Fem"
            for feat in word.feats.split('|'):
                if '=' in feat:
                    key, value = feat.split('=', 1)
                    morph[key.lower()] = value.lower()
        
        # Normalizar nombres de características
        morph_normalized = {}
        
        key_map = {
            'case': 'case',
            'number': 'number',
            'gender': 'gender',
            'tense': 'tense',
            'mood': 'mood',
            'voice': 'voice',
            'person': 'person',
            'degree': 'degree'
        }
        
        for old_key, new_key in key_map.items():
            if old_key in morph:
                morph_normalized[new_key] = morph[old_key]
        
        return morph_normalized
    
    def _is_punctuation(self, text: str) -> bool:
        """Verifica si el texto es puntuación"""
        return text.strip() in '.,;:!?-—()[]{}""\'\'«»'
    
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
    Analiza un texto con CLTK y guarda el análisis en TextWordLink
    
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
    
    # Verificar si CLTK está disponible
    if not CLTKAnalyzer.is_available():
        raise RuntimeError(
            "CLTK no está disponible.\n" + 
            CLTKAnalyzer.install_instructions()
        )
    
    # Limpiar análisis anteriores
    existing_links = session.exec(
        select(TextWordLink).where(TextWordLink.text_id == text_id)
    ).all()
    
    for link in existing_links:
        session.delete(link)
    session.commit()
    
    # Analizar con CLTK
    analyzer = CLTKAnalyzer()
    analyses = analyzer.analyze_text(text_content)
    
    print(f"📊 Texto analizado: {len(analyses)} tokens encontrados")
    
    saved_count = 0
    
    for analysis in analyses:
        # Intentar encontrar palabra en vocabulario
        normalized_form = LatinMorphology.normalize_latin(analysis['lemma'])
        
        word = session.exec(
            select(Word).where(
                (Word.latin == analysis['lemma']) |
                (Word.latin == normalized_form)
            )
        ).first()
        
        # Crear TextWordLink
        link = TextWordLink(
            text_id=text_id,
            word_id=word.id if word else None,
            position_in_sentence=analysis['position'],
            form=analysis['form'],
            morphology_json=json.dumps(analysis['morphology']),
            syntax_role=None  # Puede ser extendido después
        )
        
        # Guardar lemma y POS adicionales si no está en vocabulario
        if not word:
            # Temporalmente guardar en notes
            link.notes = json.dumps({
                "lemma": analysis['lemma'],
                "pos": analysis['pos'],
                "cltk_analysis": True
            })
        
        session.add(link)
        saved_count += 1
    
    session.commit()
    
    print(f"✅ {saved_count} análisis guardados en base de datos")
    
    return len(analyses), saved_count
