"""
Analizador morfológico de textos latinos - Estilo Collatinus
Análisis reverso: forma inflectada → lema + información morfológica
"""

import json
import re
from typing import List, Dict, Optional
from sqlmodel import select
from database.models import InflectedForm, Word
from utils.latin_logic import LatinMorphology


class LatinTextAnalyzer:
    """Analizador de textos latinos con lematización y análisis morfológico"""
    
    @staticmethod
    def analyze_word(form: str, session) -> List[Dict]:
        """
        Analiza una forma latina y retorna posibles lemas + análisis morfológico
        
        Args:
            form: Forma latina a analizar (ej: "puellae", "amat")
            session: Sesión de base de datos SQLModel
            
        Returns:
            Lista de análisis posibles:
            [
                {
                    "lemma": "puella",
                    "translation": "niña",
                    "pos": "noun",
                    "morphology": {"case": "gen", "number": "sg"},
                    "confidence": 1.0,
                    "word_id": 123
                },
                ...
            ]
        """
        # Normalizar para búsqueda (sin macrones)
        normalized = LatinMorphology.normalize_latin(form)
        
        # Buscar en tabla de formas inflectadas
        matches = session.exec(
            select(InflectedForm)
            .where(InflectedForm.normalized_form == normalized)
        ).all()
        
        results = []
        for match in matches:
            word = match.word
            if word:
                results.append({
                    "lemma": word.latin,
                    "translation": word.translation,
                    "pos": word.part_of_speech,
                    "morphology": json.loads(match.morphology),
                    "confidence": 1.0,
                    "word_id": word.id,
                    "declension": word.declension,
                    "conjugation": word.conjugation,
                    "gender": word.gender
                })
        
        # Si no encontramos nada en la tabla, intentar análisis heurístico
        if not results:
            results = LatinTextAnalyzer._heuristic_analysis(form, normalized, session)
        
        return results
    
    @staticmethod
    def _heuristic_analysis(form: str, normalized: str, session) -> List[Dict]:
        """
        Análisis heurístico para palabras no en la base de datos
        Útil para palabras invariables o formas no generadas
        """
        results = []
        
        # Buscar palabras invariables que coincidan exactamente
        invariable_words = session.exec(
            select(Word)
            .where(Word.is_invariable == True)
        ).all()
        
        for word in invariable_words:
            word_normalized = LatinMorphology.normalize_latin(word.latin)
            if word_normalized == normalized:
                results.append({
                    "lemma": word.latin,
                    "translation": word.translation,
                    "pos": word.part_of_speech,
                    "morphology": {"invariable": True},
                    "confidence": 0.9,
                    "word_id": word.id,
                    "declension": None,
                    "conjugation": None,
                    "gender": None
                })
        
        return results
    
    @staticmethod
    def analyze_text(text: str, session) -> List[Dict]:
        """
        Analiza un texto completo palabra por palabra
        
        Args:
            text: Texto latino a analizar
            session: Sesión de base de datos
            
        Returns:
            Lista de palabras analizadas:
            [
                {
                    "form": "Puella",
                    "analyses": [análisis morfológicos],
                    "position": 0
                },
                ...
            ]
        """
        # Tokenización: separar palabras y mantener puntuación
        # Regex para capturar palabras latinas (con macrones) y puntuación
        tokens = re.findall(r'[a-zA-ZāēīōūȳĀĒĪŌŪȲ]+|[.,;:!?]', text)
        
        analyzed = []
        position = 0
        
        for token in tokens:
            # Si es puntuación, saltar
            if token in '.,;:!?':
                analyzed.append({
                    "form": token,
                    "analyses": [],
                    "position": position,
                    "is_punctuation": True
                })
            else:
                # Analizar palabra
                analyses = LatinTextAnalyzer.analyze_word(token, session)
                analyzed.append({
                    "form": token,
                    "analyses": analyses,
                    "position": position,
                    "is_punctuation": False
                })
            
            position += 1
        
        return analyzed
    
    @staticmethod
    def format_morphology(morphology: Dict, pos: str) -> str:
        """
        Formatea el análisis morfológico para mostrar al usuario
        
        Args:
            morphology: Dict con información morfológica
            pos: Parte del discurso
            
        Returns:
            String formateado, ej: "genitivo singular" o "presente indicativo 3ª sg."
        """
        if morphology.get("invariable"):
            return "invariable"
        
        parts = []
        
        if pos == "noun" or pos == "adjective" or pos == "pronoun":
            # Casos
            case_map = {
                "nom": "nominativo",
                "voc": "vocativo",
                "gen": "genitivo",
                "dat": "dativo",
                "acc": "acusativo",
                "abl": "ablativo"
            }
            if "case" in morphology:
                parts.append(case_map.get(morphology["case"], morphology["case"]))
            
            # Número
            if "number" in morphology:
                parts.append("singular" if morphology["number"] == "sg" else "plural")
            
            # Género (para adjetivos/pronombres)
            if "gender" in morphology:
                gender_map = {"m": "masculino", "f": "femenino", "n": "neutro"}
                parts.append(gender_map.get(morphology["gender"], morphology["gender"]))
        
        elif pos == "verb":
            # Tiempo
            tense_map = {
                "pres": "presente",
                "imp": "imperfecto",
                "fut": "futuro",
                "perf": "perfecto",
                "plup": "pluscuamperfecto",
                "futperf": "futuro perfecto"
            }
            if "tense" in morphology:
                parts.append(tense_map.get(morphology["tense"], morphology["tense"]))
            
            # Modo
            mood_map = {
                "ind": "indicativo",
                "subj": "subjuntivo",
                "imv": "imperativo"
            }
            if "mood" in morphology:
                parts.append(mood_map.get(morphology["mood"], morphology["mood"]))
            
            # Voz
            if "voice" in morphology:
                parts.append("activa" if morphology["voice"] == "act" else "pasiva")
            
            # Persona y número
            if "person" in morphology and "number" in morphology:
                number_str = "sg" if morphology["number"] == "sg" else "pl"
                parts.append(f"{morphology['person']}ª {number_str}")
        
        return " ".join(parts) if parts else "análisis desconocido"
