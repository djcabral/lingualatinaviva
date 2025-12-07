"""
MÓDULO DE GESTIÓN DE VOCABULARIO - Lingua Latina Viva

Gestión integral del vocabulario latino:
- Almacenamiento y recuperación de lemas
- Enriquecimiento de definiciones y contextos
- Gestión de formas inflexionadas
- Análisis de frecuencia y dificultad
- Validación de coherencia semántica

Independiente de Streamlit, optimizado para procesamiento en batch.
"""

from typing import List, Dict, Optional, Tuple, Any, Set
from dataclasses import dataclass, field, asdict
from enum import Enum
import logging
from datetime import datetime
import json
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


# ============================================================================
# ENUMERACIONES Y TIPOS
# ============================================================================

class DefinitionSource(Enum):
    """Fuentes posibles de definiciones"""
    LEWIS_SHORT = "lewis_short"      # Diccionario Lewis & Short (clásico)
    OXFORD = "oxford"                 # Oxford Latin Dictionary
    MANUAL = "manual"                 # Ingreso manual
    COLLATINUS = "collatinus"        # Extraído de Collatinus
    AI_GENERATED = "ai_generated"    # Generado por IA
    CONTEXT_INFERRED = "context_inferred"  # Inferido del contexto


class WordFrequency(Enum):
    """Categorías de frecuencia de palabras"""
    ULTRA_COMMON = 5      # 100-500+ ocurrencias
    VERY_COMMON = 4       # 50-100 ocurrencias
    COMMON = 3            # 10-50 ocurrencias
    UNCOMMON = 2          # 2-10 ocurrencias
    RARE = 1              # 1 ocurrencia


# ============================================================================
# DATACLASSES
# ============================================================================

@dataclass
class Definition:
    """Una definición individual de una palabra"""
    text: str
    source: DefinitionSource
    language: str = "es"  # idioma de la definición
    
    # Metadatos
    added_date: datetime = field(default_factory=datetime.now)
    examples: List[str] = field(default_factory=list)
    context_note: Optional[str] = None
    is_primary: bool = False  # definición principal/más común
    
    confidence: float = 0.8
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'text': self.text,
            'source': self.source.value,
            'language': self.language,
            'is_primary': self.is_primary,
            'confidence': self.confidence,
            'context_note': self.context_note,
            'examples': self.examples,
        }


@dataclass
class InflectedForm:
    """Una forma inflexionada de una palabra"""
    form: str
    lemma: str
    
    # Información morfológica
    pos: str  # noun, verb, adj, etc.
    case: Optional[str] = None
    number: Optional[str] = None
    gender: Optional[str] = None
    person: Optional[str] = None
    tense: Optional[str] = None
    mood: Optional[str] = None
    voice: Optional[str] = None
    
    # Metadatos
    frequency: int = 0  # número de veces encontrada
    is_common: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'form': self.form,
            'lemma': self.lemma,
            'pos': self.pos,
            'case': self.case,
            'number': self.number,
            'gender': self.gender,
            'person': self.person,
            'tense': self.tense,
            'mood': self.mood,
            'voice': self.voice,
            'frequency': self.frequency,
            'is_common': self.is_common,
        }


@dataclass
class WordRelation:
    """Relación entre palabras (sinónimos, antónimos, derivados, etc.)"""
    related_lemma: str
    relation_type: str  # 'synonym', 'antonym', 'derived', 'related_root'
    confidence: float = 0.8
    notes: Optional[str] = None


@dataclass
class SemanticField:
    """Agrupación temática de palabras"""
    field_name: str
    lemmas: List[str] = field(default_factory=list)
    description: Optional[str] = None
    examples: List[str] = field(default_factory=list)


@dataclass
class LatinWord:
    """Entrada completa de vocabulario latino"""
    lemma: str
    
    # Definiciones
    definitions: List[Definition] = field(default_factory=list)
    
    # Formas inflexionadas
    inflected_forms: List[InflectedForm] = field(default_factory=list)
    
    # Información morfológica base
    pos: str  # noun, verb, adj, adverb, etc.
    declension: Optional[str] = None  # para nombres: 1ª, 2ª, 3ª, 4ª, 5ª
    conjugation: Optional[str] = None  # para verbos: 1ª, 2ª, 3ª, 4ª
    gender: Optional[str] = None  # para nombres
    
    # Relaciones semánticas
    relations: List[WordRelation] = field(default_factory=list)
    semantic_fields: List[str] = field(default_factory=list)
    
    # Información adicional
    etymology: Optional[str] = None
    cognates: List[str] = field(default_factory=list)  # palabras relacionadas en otros idiomas
    
    # Estadísticas
    frequency: int = 0  # número total de ocurrencias encontradas
    frequency_level: WordFrequency = WordFrequency.UNCOMMON
    difficulty_level: int = 5  # 1-10
    
    # Metadatos
    source: str = "manual"  # fuente de origen
    added_date: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    added_by: Optional[str] = None
    last_updated_by: Optional[str] = None
    
    # Control de calidad
    is_verified: bool = False
    verification_date: Optional[datetime] = None
    verified_by: Optional[str] = None
    notes: Optional[str] = None
    
    # Para BD
    db_id: Optional[int] = None
    
    def get_primary_definition(self) -> Optional[Definition]:
        """Obtiene la definición principal"""
        for defn in self.definitions:
            if defn.is_primary:
                return defn
        # Si no hay definición principal, retornar la primera
        return self.definitions[0] if self.definitions else None
    
    def get_common_forms(self) -> List[InflectedForm]:
        """Obtiene las formas más comunes"""
        return [f for f in self.inflected_forms if f.is_common]
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializa a diccionario"""
        return {
            'lemma': self.lemma,
            'pos': self.pos,
            'declension': self.declension,
            'conjugation': self.conjugation,
            'gender': self.gender,
            'definitions': [d.to_dict() for d in self.definitions],
            'inflected_forms': [f.to_dict() for f in self.inflected_forms],
            'frequency': self.frequency,
            'difficulty_level': self.difficulty_level,
            'etymology': self.etymology,
            'is_verified': self.is_verified,
        }


# ============================================================================
# REPOSITORIO DE VOCABULARIO
# ============================================================================

class VocabularyRepository(ABC):
    """Interfaz abstracta para repositorios de vocabulario"""
    
    @abstractmethod
    def get_word(self, lemma: str) -> Optional[LatinWord]:
        """Obtiene una palabra por lema"""
        pass
    
    @abstractmethod
    def save_word(self, word: LatinWord) -> bool:
        """Guarda o actualiza una palabra"""
        pass
    
    @abstractmethod
    def delete_word(self, lemma: str) -> bool:
        """Elimina una palabra"""
        pass
    
    @abstractmethod
    def search(self, query: str) -> List[LatinWord]:
        """Busca palabras por criterios"""
        pass
    
    @abstractmethod
    def get_all_words(self) -> List[LatinWord]:
        """Obtiene todas las palabras"""
        pass


class InMemoryVocabularyRepository(VocabularyRepository):
    """Repositorio en memoria para desarrollo/testing"""
    
    def __init__(self):
        self.words: Dict[str, LatinWord] = {}
    
    def get_word(self, lemma: str) -> Optional[LatinWord]:
        return self.words.get(lemma.lower())
    
    def save_word(self, word: LatinWord) -> bool:
        self.words[word.lemma.lower()] = word
        word.last_updated = datetime.now()
        return True
    
    def delete_word(self, lemma: str) -> bool:
        if lemma.lower() in self.words:
            del self.words[lemma.lower()]
            return True
        return False
    
    def search(self, query: str) -> List[LatinWord]:
        """Búsqueda simple por substring"""
        query = query.lower()
        results = []
        for word in self.words.values():
            if query in word.lemma.lower():
                results.append(word)
            elif word.definitions:
                for defn in word.definitions:
                    if query in defn.text.lower():
                        results.append(word)
                        break
        return results
    
    def get_all_words(self) -> List[LatinWord]:
        return list(self.words.values())


# ============================================================================
# GESTOR INTEGRAL DE VOCABULARIO
# ============================================================================

class VocabularyManager:
    """
    Gestor integral del vocabulario latino.
    
    Proporciona:
    - Almacenamiento y recuperación
    - Enriquecimiento de datos
    - Validación de coherencia
    - Estadísticas y análisis
    """
    
    def __init__(self, repository: VocabularyRepository):
        """
        Inicializa el gestor
        
        Args:
            repository: Repositorio de vocabulario (puede ser BD, memoria, etc.)
        """
        self.repo = repository
        self._cache: Dict[str, LatinWord] = {}
        self._frequency_cache: Dict[str, int] = {}
    
    # ========================================================================
    # OPERACIONES BÁSICAS
    # ========================================================================
    
    def get_word(self, lemma: str, use_cache: bool = True) -> Optional[LatinWord]:
        """
        Obtiene una palabra, con caché opcional
        """
        if use_cache and lemma in self._cache:
            return self._cache[lemma]
        
        word = self.repo.get_word(lemma)
        if word and use_cache:
            self._cache[lemma] = word
        
        return word
    
    def add_or_update_word(
        self,
        lemma: str,
        definitions: List[str],
        pos: str,
        declension: Optional[str] = None,
        conjugation: Optional[str] = None,
        gender: Optional[str] = None,
        difficulty_level: int = 5,
        source: str = "manual"
    ) -> LatinWord:
        """
        Añade o actualiza una palabra
        """
        word = self.get_word(lemma)
        
        if word is None:
            # Crear nueva palabra
            word = LatinWord(
                lemma=lemma,
                pos=pos,
                declension=declension,
                conjugation=conjugation,
                gender=gender,
                difficulty_level=difficulty_level,
                source=source
            )
        
        # Añadir definiciones
        for defn_text in definitions:
            if not any(d.text == defn_text for d in word.definitions):
                defn = Definition(
                    text=defn_text,
                    source=DefinitionSource.MANUAL,
                    is_primary=len(word.definitions) == 0
                )
                word.definitions.append(defn)
        
        word.last_updated = datetime.now()
        self.repo.save_word(word)
        
        # Actualizar caché
        self._cache[lemma] = word
        
        logger.info(f"Palabra actualizada: {lemma}")
        return word
    
    def add_definition(
        self,
        lemma: str,
        definition_text: str,
        source: DefinitionSource,
        is_primary: bool = False,
        examples: Optional[List[str]] = None,
        context_note: Optional[str] = None
    ) -> bool:
        """
        Añade una definición a una palabra existente
        """
        word = self.get_word(lemma)
        if not word:
            logger.warning(f"Palabra no encontrada: {lemma}")
            return False
        
        # Evitar duplicados
        if any(d.text == definition_text for d in word.definitions):
            logger.info(f"Definición duplicada para {lemma}: {definition_text}")
            return False
        
        defn = Definition(
            text=definition_text,
            source=source,
            is_primary=is_primary or len(word.definitions) == 0,
            examples=examples or []
        )
        
        if context_note:
            defn.context_note = context_note
        
        word.definitions.append(defn)
        word.last_updated = datetime.now()
        
        self.repo.save_word(word)
        self._cache[lemma] = word
        
        logger.info(f"Definición añadida a {lemma}")
        return True
    
    def add_inflected_form(
        self,
        lemma: str,
        form: str,
        **morphology_info
    ) -> bool:
        """
        Añade una forma inflexionada a una palabra
        """
        word = self.get_word(lemma)
        if not word:
            logger.warning(f"Palabra no encontrada: {lemma}")
            return False
        
        # Evitar duplicados
        if any(f.form == form for f in word.inflected_forms):
            logger.debug(f"Forma duplicada: {form}")
            return False
        
        inflected = InflectedForm(
            form=form,
            lemma=lemma,
            pos=word.pos,
            **morphology_info
        )
        
        word.inflected_forms.append(inflected)
        word.last_updated = datetime.now()
        
        self.repo.save_word(word)
        self._cache[lemma] = word
        
        logger.info(f"Forma inflexionada añadida: {form} → {lemma}")
        return True
    
    # ========================================================================
    # ANÁLISIS Y ESTADÍSTICAS
    # ========================================================================
    
    def update_word_frequency(self, lemma: str, count: int) -> bool:
        """
        Actualiza la frecuencia de una palabra
        """
        word = self.get_word(lemma)
        if not word:
            return False
        
        word.frequency += count
        
        # Actualizar nivel de frecuencia
        word.frequency_level = self._calculate_frequency_level(word.frequency)
        word.last_updated = datetime.now()
        
        self.repo.save_word(word)
        self._cache[lemma] = word
        
        return True
    
    def get_frequency_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de frecuencia del vocabulario
        """
        words = self.repo.get_all_words()
        
        frequencies = [w.frequency for w in words]
        total_words = len(words)
        total_occurrences = sum(frequencies)
        
        level_counts = {}
        for level in WordFrequency:
            count = sum(1 for w in words if w.frequency_level == level)
            if count > 0:
                level_counts[level.name] = count
        
        return {
            'total_unique_words': total_words,
            'total_occurrences': total_occurrences,
            'average_frequency': total_occurrences / total_words if total_words > 0 else 0,
            'by_frequency_level': level_counts,
            'verified_words': sum(1 for w in words if w.is_verified),
            'pending_verification': total_words - sum(1 for w in words if w.is_verified),
        }
    
    def get_difficulty_distribution(self) -> Dict[int, int]:
        """
        Obtiene distribución por nivel de dificultad
        """
        words = self.repo.get_all_words()
        distribution = {}
        
        for word in words:
            level = word.difficulty_level
            distribution[level] = distribution.get(level, 0) + 1
        
        return dict(sorted(distribution.items()))
    
    # ========================================================================
    # VALIDACIÓN Y CONTROL DE CALIDAD
    # ========================================================================
    
    def validate_word(self, lemma: str) -> Tuple[bool, List[str]]:
        """
        Valida una palabra y retorna (is_valid, issues_list)
        """
        word = self.get_word(lemma)
        if not word:
            return False, ["Palabra no encontrada"]
        
        issues = []
        
        # Validar definiciones
        if not word.definitions:
            issues.append("Sin definiciones")
        else:
            # Debe haber al menos una definición primaria
            if not any(d.is_primary for d in word.definitions):
                issues.append("Sin definición primaria")
        
        # Validar información morfológica
        if not word.pos:
            issues.append("Categoría gramatical faltante")
        
        if word.pos in ["noun", "sustantivo"] and not word.gender:
            issues.append("Género faltante para sustantivo")
        
        if word.pos in ["noun", "sustantivo"] and not word.declension:
            issues.append("Declinación faltante para sustantivo")
        
        if word.pos in ["verb", "verbo"] and not word.conjugation:
            issues.append("Conjugación faltante para verbo")
        
        return len(issues) == 0, issues
    
    def validate_all_words(self) -> Dict[str, List[str]]:
        """
        Valida todas las palabras y retorna problemas encontrados
        """
        words = self.repo.get_all_words()
        problems = {}
        
        for word in words:
            is_valid, issues = self.validate_word(word.lemma)
            if not is_valid:
                problems[word.lemma] = issues
        
        return problems
    
    def verify_word(
        self,
        lemma: str,
        verified_by: Optional[str] = None
    ) -> bool:
        """
        Marca una palabra como verificada
        """
        word = self.get_word(lemma)
        if not word:
            return False
        
        # Validar primero
        is_valid, issues = self.validate_word(lemma)
        if not is_valid:
            logger.warning(f"No se puede verificar palabra inválida: {lemma}")
            logger.warning(f"Problemas: {issues}")
            return False
        
        word.is_verified = True
        word.verification_date = datetime.now()
        word.verified_by = verified_by
        word.last_updated = datetime.now()
        
        self.repo.save_word(word)
        self._cache[lemma] = word
        
        logger.info(f"Palabra verificada: {lemma}")
        return True
    
    # ========================================================================
    # BÚSQUEDA Y CONSULTAS
    # ========================================================================
    
    def search_by_definition(self, query: str) -> List[LatinWord]:
        """
        Busca palabras por definición
        """
        words = self.repo.get_all_words()
        query_lower = query.lower()
        
        results = []
        for word in words:
            for defn in word.definitions:
                if query_lower in defn.text.lower():
                    results.append(word)
                    break
        
        return results
    
    def search_by_semantic_field(self, field_name: str) -> List[LatinWord]:
        """
        Busca palabras por campo semántico
        """
        words = self.repo.get_all_words()
        return [w for w in words if field_name in w.semantic_fields]
    
    def get_words_by_pos(self, pos: str) -> List[LatinWord]:
        """
        Obtiene todas las palabras de una categoría gramatical
        """
        words = self.repo.get_all_words()
        return [w for w in words if w.pos == pos]
    
    def get_most_frequent_words(self, limit: int = 100) -> List[LatinWord]:
        """
        Obtiene las palabras más frecuentes
        """
        words = self.repo.get_all_words()
        sorted_words = sorted(words, key=lambda w: w.frequency, reverse=True)
        return sorted_words[:limit]
    
    def get_unverified_words(self) -> List[LatinWord]:
        """
        Obtiene palabras que aún no han sido verificadas
        """
        words = self.repo.get_all_words()
        return [w for w in words if not w.is_verified]
    
    # ========================================================================
    # OPERACIONES BATCH
    # ========================================================================
    
    def import_from_dict_list(
        self,
        words_data: List[Dict[str, Any]],
        source: str = "import"
    ) -> Tuple[int, List[str]]:
        """
        Importa palabras desde lista de diccionarios
        
        Returns:
            (número de palabras importadas, lista de errores)
        """
        imported = 0
        errors = []
        
        for idx, word_data in enumerate(words_data):
            try:
                lemma = word_data.get('lemma')
                if not lemma:
                    errors.append(f"Fila {idx}: Lema faltante")
                    continue
                
                definitions = word_data.get('definitions', [])
                if isinstance(definitions, str):
                    definitions = [definitions]
                
                pos = word_data.get('pos', 'unknown')
                
                self.add_or_update_word(
                    lemma=lemma,
                    definitions=definitions,
                    pos=pos,
                    declension=word_data.get('declension'),
                    conjugation=word_data.get('conjugation'),
                    gender=word_data.get('gender'),
                    difficulty_level=word_data.get('difficulty_level', 5),
                    source=source
                )
                
                imported += 1
            
            except Exception as e:
                errors.append(f"Fila {idx}: {str(e)}")
        
        logger.info(f"Importadas {imported} palabras de {len(words_data)}")
        if errors:
            logger.warning(f"Errores en importación: {len(errors)}")
        
        return imported, errors
    
    def export_to_json(self, filepath: str) -> bool:
        """
        Exporta el vocabulario a archivo JSON
        """
        try:
            words = self.repo.get_all_words()
            data = [w.to_dict() for w in words]
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info(f"Vocabulario exportado a {filepath}")
            return True
        
        except Exception as e:
            logger.error(f"Error exportando vocabulario: {e}")
            return False
    
    # ========================================================================
    # UTILIDADES PRIVADAS
    # ========================================================================
    
    def _calculate_frequency_level(self, frequency: int) -> WordFrequency:
        """Calcula nivel de frecuencia basado en número de ocurrencias"""
        if frequency >= 100:
            return WordFrequency.ULTRA_COMMON
        elif frequency >= 50:
            return WordFrequency.VERY_COMMON
        elif frequency >= 10:
            return WordFrequency.COMMON
        elif frequency >= 2:
            return WordFrequency.UNCOMMON
        else:
            return WordFrequency.RARE
