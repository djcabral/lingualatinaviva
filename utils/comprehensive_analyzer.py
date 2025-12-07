"""
MÓDULO CENTRAL DE ANÁLISIS INTEGRAL - Lingua Latina Viva

Proporciona análisis completo, confiable y exhaustivo de textos latinos:
- Análisis morfológico (usando PyCollatinus)
- Análisis sintáctico (usando LatinCy)
- Enriquecimiento semántico
- Validación cruzada de resultados
- Almacenamiento en BD optimizado

Este módulo es independiente de Streamlit y puede usarse en sistemas CLI o API.
"""

from typing import List, Dict, Optional, Tuple, Any, Union
from dataclasses import dataclass, field, asdict
from enum import Enum
import json
import logging
from datetime import datetime
import hashlib

# Importar analizadores existentes
from .collatinus_analyzer import LatinMorphAnalyzer
from .syntax_analyzer import LatinSyntaxAnalyzer
from .latin_logic import LatinLogicEngine

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# ENUMERACIONES Y TIPOS
# ============================================================================

class ConfidenceLevel(Enum):
    """Niveles de confianza en el análisis"""
    VERY_LOW = 0.0      # < 20%
    LOW = 0.2           # 20-40%
    MEDIUM = 0.5        # 40-60%
    HIGH = 0.8          # 60-80%
    VERY_HIGH = 0.95    # 80-100%


class WordClass(Enum):
    """Clases de palabras (categorías POS)"""
    NOUN = "sustantivo"
    VERB = "verbo"
    ADJECTIVE = "adjetivo"
    ADVERB = "adverbio"
    PRONOUN = "pronombre"
    PREPOSITION = "preposición"
    CONJUNCTION = "conjunción"
    INTERJECTION = "interjección"
    NUMERAL = "numeral"
    ARTICLE = "artículo"
    PARTICLE = "partícula"
    UNKNOWN = "desconocido"


class SyntacticFunction(Enum):
    """Funciones sintácticas posibles"""
    SUBJECT = "sujeto"
    PREDICATE = "predicado"
    DIRECT_OBJECT = "objeto directo"
    INDIRECT_OBJECT = "objeto indirecto"
    PREPOSITIONAL_OBJECT = "objeto preposicional"
    ADVERBIAL = "adverbial"
    ATTRIBUTE = "atributo"
    PREDICATE_NOMINATIVE = "nominativo predicativo"
    APPOSITION = "aposición"
    MODIFIER = "modificador"
    VOCATIVE = "vocativo"
    GENITIVE_POSSESSIVE = "genitivo posesivo"
    ABLATIVE_MEANS = "ablativo de medio"
    ABLATIVE_MANNER = "ablativo de modo"
    ABLATIVE_AGENT = "ablativo de agente"
    ABLATIVE_TIME = "ablativo de tiempo"
    LOCATIVE = "locativo"
    UNKNOWN = "desconocida"


# ============================================================================
# DATACLASSES PARA ALMACENAMIENTO ESTRUCTURADO
# ============================================================================

@dataclass
class MorphologicalData:
    """Información morfológica de una palabra"""
    lemma: str
    pos: WordClass
    
    # Información de paradigma
    declension: Optional[str] = None  # 1ª, 2ª, 3ª, 4ª, 5ª
    conjugation: Optional[str] = None  # 1ª, 2ª, 3ª, 4ª
    
    # Categorías gramaticales
    number: Optional[str] = None  # singular, plural
    case: Optional[str] = None    # nominativo, acusativo, genitivo, etc.
    gender: Optional[str] = None  # masculino, femenino, neutro
    
    # Para verbos
    person: Optional[str] = None  # 1ª, 2ª, 3ª
    tense: Optional[str] = None   # presente, pretérito, futuro, etc.
    mood: Optional[str] = None    # indicativo, subjuntivo, imperativo, etc.
    voice: Optional[str] = None   # activo, pasivo
    
    # Para adjetivos
    degree: Optional[str] = None  # positivo, comparativo, superlativo
    
    # Confianza del análisis
    confidence: float = 0.8
    source: str = "collatinus"  # collatinus, latincy, manual
    
    # Información adicional
    alternatives: List[Dict[str, Any]] = field(default_factory=list)
    notes: Optional[str] = None


@dataclass
class SemanticData:
    """Información semántica de una palabra"""
    definitions: List[str] = field(default_factory=list)
    context_translations: List[str] = field(default_factory=list)
    semantic_fields: List[str] = field(default_factory=list)  # familia semántica
    etymology: Optional[str] = None
    cognates: List[str] = field(default_factory=list)
    
    frequency_score: Optional[float] = None  # 0-1, qué tan común es
    difficulty_level: Optional[int] = None   # 1-10, cuán difícil es


@dataclass
class SyntacticAnalysis:
    """Análisis sintáctico de una palabra en contexto"""
    function: SyntacticFunction
    head_word_index: Optional[int] = None  # índice de la palabra de la que depende
    dependency_relation: Optional[str] = None  # suj, obj, iobj, etc.
    governing_case: Optional[str] = None  # el caso que exige
    
    confidence: float = 0.8
    notes: Optional[str] = None


@dataclass
class ComprehensiveWordAnalysis:
    """Análisis integral de una palabra"""
    word: str
    position_in_sentence: int  # índice 0-based
    
    morphology: MorphologicalData
    semantics: SemanticData
    syntax: SyntacticAnalysis
    
    overall_confidence: float  # promedio de confianzas
    validation_status: str = "pending"  # pending, validated, needs_review, error
    last_updated: datetime = field(default_factory=datetime.now)
    
    # Información para BD
    db_id: Optional[int] = None


@dataclass
class ComprehensiveSentenceAnalysis:
    """Análisis integral de una oración"""
    original_text: str
    translation: Optional[str] = None
    
    word_analyses: List[ComprehensiveWordAnalysis] = field(default_factory=list)
    
    # Análisis de nivel de oración
    sentence_type: str = ""  # declarativa, interrogativa, imperativa, etc.
    main_verb_index: Optional[int] = None
    special_constructions: List[str] = field(default_factory=list)
    
    # Información de contexto
    source: Optional[str] = None
    lesson_number: Optional[int] = None
    difficulty_level: int = 1
    
    # Validación
    overall_confidence: float = 0.8
    quality_score: float = 0.0  # calculado automáticamente
    validation_status: str = "pending"
    issues: List[str] = field(default_factory=list)
    
    # Metadata
    analysis_timestamp: datetime = field(default_factory=datetime.now)
    analyzer_version: str = "1.0"
    
    # Para BD
    db_id: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario para serialización"""
        data = asdict(self)
        # Convertir Enums a strings
        if self.word_analyses:
            for wa in self.word_analyses:
                if isinstance(wa.morphology.pos, WordClass):
                    wa.morphology.pos = wa.morphology.pos.value
                if isinstance(wa.syntax.function, SyntacticFunction):
                    wa.syntax.function = wa.syntax.function.value
        return data
    
    def to_json(self) -> str:
        """Serializa a JSON"""
        return json.dumps(self.to_dict(), default=str, indent=2)


# ============================================================================
# ANALIZADOR INTEGRAL CENTRAL
# ============================================================================

class ComprehensiveLatinAnalyzer:
    """
    Analizador integral de textos latinos.
    
    Combina múltiples fuentes de análisis:
    1. Análisis morfológico (PyCollatinus)
    2. Análisis sintáctico (LatinCy)
    3. Información semántica (BD + fuentes externas)
    4. Validación cruzada
    
    Diseñado para producir análisis de alta calidad listos para la BD.
    """
    
    def __init__(self, db_connection=None, cache_enabled: bool = True):
        """
        Inicializa el analizador
        
        Args:
            db_connection: Conexión a la base de datos (opcional)
            cache_enabled: Habilitar caché de resultados
        """
        self.db = db_connection
        self.cache_enabled = cache_enabled
        self._cache: Dict[str, Any] = {}
        
        # Inicializar analizadores componentes
        logger.info("Inicializando analizadores componentes...")
        try:
            self.morph_analyzer = LatinMorphAnalyzer()
            logger.info("✅ Analizador morfológico (PyCollatinus) listo")
        except Exception as e:
            logger.warning(f"⚠️ PyCollatinus no disponible: {e}")
            self.morph_analyzer = None
        
        try:
            self.syntax_analyzer = LatinSyntaxAnalyzer()
            logger.info("✅ Analizador sintáctico (LatinCy) listo")
        except Exception as e:
            logger.warning(f"⚠️ LatinCy no disponible: {e}")
            self.syntax_analyzer = None
        
        try:
            self.logic_engine = LatinLogicEngine()
            logger.info("✅ Motor de lógica latina listo")
        except Exception as e:
            logger.warning(f"⚠️ Motor de lógica no disponible: {e}")
            self.logic_engine = None
    
    def analyze_text(
        self,
        text: str,
        translation: Optional[str] = None,
        source: Optional[str] = None,
        lesson_number: Optional[int] = None,
        difficulty_level: int = 1,
        validate: bool = True
    ) -> Union[ComprehensiveSentenceAnalysis, List[ComprehensiveSentenceAnalysis]]:
        """
        Analiza un texto latino (oración o párrafo completo)
        
        Args:
            text: Texto latino a analizar
            translation: Traducción al español (opcional)
            source: Fuente del texto
            lesson_number: Número de lección
            difficulty_level: Nivel de dificultad 1-10
            validate: Realizar validación cruzada
            
        Returns:
            ComprehensiveSentenceAnalysis o lista si hay múltiples oraciones
        """
        # Normalizar y validar entrada
        text = text.strip()
        if not text:
            raise ValueError("El texto no puede estar vacío")
        
        # Dividir en oraciones si es necesario
        sentences = self._split_sentences(text)
        
        if len(sentences) == 1:
            result = self._analyze_single_sentence(
                sentences[0],
                translation=translation,
                source=source,
                lesson_number=lesson_number,
                difficulty_level=difficulty_level
            )
            
            if validate:
                result = self._validate_analysis(result)
            
            return result
        else:
            results = []
            for sent in sentences:
                result = self._analyze_single_sentence(
                    sent,
                    translation=None,
                    source=source,
                    lesson_number=lesson_number,
                    difficulty_level=difficulty_level
                )
                
                if validate:
                    result = self._validate_analysis(result)
                
                results.append(result)
            
            return results
    
    def _analyze_single_sentence(
        self,
        sentence: str,
        translation: Optional[str] = None,
        source: Optional[str] = None,
        lesson_number: Optional[int] = None,
        difficulty_level: int = 1
    ) -> ComprehensiveSentenceAnalysis:
        """
        Analiza una única oración de manera integral
        """
        logger.info(f"Analizando: {sentence}")
        
        # Crear estructura base
        analysis = ComprehensiveSentenceAnalysis(
            original_text=sentence,
            translation=translation,
            source=source,
            lesson_number=lesson_number,
            difficulty_level=difficulty_level
        )
        
        # Tokenizar
        tokens = self._tokenize(sentence)
        
        # Analizar cada palabra
        for idx, token in enumerate(tokens):
            word_analysis = self._analyze_word(
                token,
                sentence,
                idx,
                tokens
            )
            analysis.word_analyses.append(word_analysis)
        
        # Análisis de nivel de oración
        if self.syntax_analyzer:
            analysis = self._enrich_sentence_level(analysis)
        
        # Calcular scores de calidad
        analysis.quality_score = self._calculate_quality_score(analysis)
        
        return analysis
    
    def _analyze_word(
        self,
        word: str,
        sentence: str,
        position: int,
        tokens: List[str]
    ) -> ComprehensiveWordAnalysis:
        """
        Análisis integral de una palabra individual
        """
        # Análisis morfológico
        morphology = self._analyze_morphology(word)
        
        # Análisis semántico
        semantics = self._analyze_semantics(word, morphology)
        
        # Análisis sintáctico (en contexto)
        syntax = self._analyze_syntax(word, sentence, position, tokens, morphology)
        
        # Crear análisis integral
        word_analysis = ComprehensiveWordAnalysis(
            word=word,
            position_in_sentence=position,
            morphology=morphology,
            semantics=semantics,
            syntax=syntax,
            overall_confidence=self._calculate_word_confidence(
                morphology, semantics, syntax
            )
        )
        
        return word_analysis
    
    def _analyze_morphology(self, word: str) -> MorphologicalData:
        """
        Análisis morfológico usando PyCollatinus
        """
        morphology = MorphologicalData(
            lemma=word,
            pos=WordClass.UNKNOWN
        )
        
        if not self.morph_analyzer:
            logger.warning(f"PyCollatinus no disponible para: {word}")
            return morphology
        
        try:
            results = self.morph_analyzer.analyze_word(word)
            
            if results:
                primary = results[0]
                
                # Mapear resultado a nuestro formato
                morphology.lemma = primary.get('lemma', word)
                morphology.pos = self._map_pos_class(primary.get('pos', 'unknown'))
                morphology.confidence = primary.get('confidence', 0.8)
                
                # Información gramatical según tipo
                morphology.case = primary.get('case')
                morphology.number = primary.get('number')
                morphology.gender = primary.get('gender')
                morphology.person = primary.get('person')
                morphology.tense = primary.get('tense')
                morphology.mood = primary.get('mood')
                morphology.voice = primary.get('voice')
                morphology.degree = primary.get('degree')
                
                # Información de paradigma
                morphology.declension = primary.get('declension')
                morphology.conjugation = primary.get('conjugation')
                
                # Alternativas
                if len(results) > 1:
                    morphology.alternatives = results[1:]
        
        except Exception as e:
            logger.error(f"Error en análisis morfológico de '{word}': {e}")
            morphology.validation_status = "error"
        
        return morphology
    
    def _analyze_semantics(
        self,
        word: str,
        morphology: MorphologicalData
    ) -> SemanticData:
        """
        Análisis semántico y búsqueda de significados
        """
        semantics = SemanticData()
        
        # Intentar obtener del DB si disponible
        if self.db:
            try:
                db_word = self.db.get_word(morphology.lemma)
                if db_word:
                    semantics.definitions = db_word.get('definitions', [])
                    semantics.frequency_score = db_word.get('frequency', None)
                    semantics.etymology = db_word.get('etymology', None)
            except Exception as e:
                logger.warning(f"Error obteniendo semántica de BD: {e}")
        
        # Completar con información básica si está vacía
        if not semantics.definitions:
            semantics.definitions = [f"[Definición pendiente: {morphology.lemma}]"]
        
        return semantics
    
    def _analyze_syntax(
        self,
        word: str,
        sentence: str,
        position: int,
        tokens: List[str],
        morphology: MorphologicalData
    ) -> SyntacticAnalysis:
        """
        Análisis sintáctico en contexto
        """
        syntax = SyntacticAnalysis(
            function=SyntacticFunction.UNKNOWN
        )
        
        # Intentar usar LatinCy si disponible
        if self.syntax_analyzer:
            try:
                doc = self.syntax_analyzer.nlp(sentence)
                
                # Encontrar el token correspondiente
                for token in doc:
                    if token.text.lower() == word.lower():
                        # Mapear función sintáctica
                        syntax.function = self._map_syntactic_function(
                            token.dep_,
                            morphology.pos
                        )
                        syntax.dependency_relation = token.dep_
                        syntax.head_word_index = token.head.i if token.head else None
                        syntax.governing_case = self._infer_governing_case(
                            token, morphology
                        )
                        break
            
            except Exception as e:
                logger.warning(f"Error en análisis sintáctico: {e}")
        
        return syntax
    
    def _enrich_sentence_level(
        self,
        analysis: ComprehensiveSentenceAnalysis
    ) -> ComprehensiveSentenceAnalysis:
        """
        Enriquece el análisis con información a nivel de oración
        """
        try:
            doc = self.syntax_analyzer.nlp(analysis.original_text)
            
            # Encontrar verbo principal
            for token in doc:
                if token.pos_ == "VERB" and token.head == token:
                    analysis.main_verb_index = token.i
                    break
            
            # Detectar tipo de oración
            analysis.sentence_type = self._classify_sentence_type(doc)
            
            # Detectar construcciones especiales
            analysis.special_constructions = self._detect_special_constructions(doc)
        
        except Exception as e:
            logger.warning(f"Error enriqueciendo análisis de oración: {e}")
        
        return analysis
    
    def _validate_analysis(
        self,
        analysis: ComprehensiveSentenceAnalysis
    ) -> ComprehensiveSentenceAnalysis:
        """
        Validación cruzada de resultados
        """
        issues = []
        
        # Verificar que tenemos análisis para todas las palabras
        if len(analysis.word_analyses) == 0:
            issues.append("Sin análisis de palabras")
        
        # Verificar conflictos morfológicos-sintácticos
        for wa in analysis.word_analyses:
            if wa.morphology.pos == WordClass.UNKNOWN:
                issues.append(f"POS desconocida para '{wa.word}'")
            
            # Validar concordancia caso-función
            if wa.morphology.case and wa.syntax.function:
                if not self._is_valid_case_function_pair(
                    wa.morphology.case,
                    wa.syntax.function
                ):
                    issues.append(
                        f"Posible error caso-función en '{wa.word}': "
                        f"{wa.morphology.case} + {wa.syntax.function.value}"
                    )
        
        analysis.issues = issues
        analysis.validation_status = "validated" if not issues else "needs_review"
        
        return analysis
    
    def _calculate_quality_score(
        self,
        analysis: ComprehensiveSentenceAnalysis
    ) -> float:
        """
        Calcula un score de calidad global (0-1)
        """
        if not analysis.word_analyses:
            return 0.0
        
        # Promedio de confianzas
        avg_confidence = sum(
            wa.overall_confidence for wa in analysis.word_analyses
        ) / len(analysis.word_analyses)
        
        # Penalizar por problemas de validación
        penalty = len(analysis.issues) * 0.1
        
        score = max(0.0, min(1.0, avg_confidence - penalty))
        return score
    
    # ========================================================================
    # MÉTODOS AUXILIARES
    # ========================================================================
    
    def _split_sentences(self, text: str) -> List[str]:
        """Divide un texto en oraciones"""
        # Implementación simple - puede mejorarse
        sentences = text.replace('!', '.').replace('?', '.').split('.')
        return [s.strip() for s in sentences if s.strip()]
    
    def _tokenize(self, sentence: str) -> List[str]:
        """Tokeniza una oración"""
        # Tokenización simple - puede mejorarse con spaCy
        import re
        # Mantener puntuación adjunta a palabras cuando sea apropiado
        tokens = re.findall(r'\b\w+\b|[.,;:!?\'-]', sentence)
        return tokens
    
    def _map_pos_class(self, pos_str: str) -> WordClass:
        """Mapea string POS a enum WordClass"""
        mapping = {
            'n': WordClass.NOUN,
            'v': WordClass.VERB,
            'a': WordClass.ADJECTIVE,
            'adv': WordClass.ADVERB,
            'pron': WordClass.PRONOUN,
            'prep': WordClass.PREPOSITION,
            'conj': WordClass.CONJUNCTION,
            'interj': WordClass.INTERJECTION,
            'num': WordClass.NUMERAL,
        }
        return mapping.get(pos_str.lower(), WordClass.UNKNOWN)
    
    def _map_syntactic_function(
        self,
        dep_rel: str,
        pos: WordClass
    ) -> SyntacticFunction:
        """Mapea relación de dependencia a función sintáctica"""
        mapping = {
            'nsubj': SyntacticFunction.SUBJECT,
            'obj': SyntacticFunction.DIRECT_OBJECT,
            'iobj': SyntacticFunction.INDIRECT_OBJECT,
            'obl': SyntacticFunction.ADVERBIAL,
            'amod': SyntacticFunction.MODIFIER,
            'nmod': SyntacticFunction.MODIFIER,
            'conj': SyntacticFunction.PREDICATE,
            'case': SyntacticFunction.PREPOSITIONAL_OBJECT,
        }
        return mapping.get(dep_rel, SyntacticFunction.UNKNOWN)
    
    def _infer_governing_case(
        self,
        token,
        morphology: MorphologicalData
    ) -> Optional[str]:
        """Infiere el caso gobernante basado en el contexto"""
        # Simplificación - se puede mejorar con reglas más complejas
        if token.head.pos_ == "ADP":  # Preposición
            return self._get_case_for_preposition(token.head.text)
        elif morphology.pos == WordClass.VERB:
            return None  # Verbos no gobiernan caso directamente
        return None
    
    def _get_case_for_preposition(self, prep: str) -> Optional[str]:
        """Obtiene el caso asociado a una preposición"""
        prep_cases = {
            'in': 'ablativo',
            'ad': 'acusativo',
            'ab': 'ablativo',
            'cum': 'ablativo',
            'de': 'ablativo',
            'per': 'acusativo',
            'post': 'acusativo',
            'sine': 'ablativo',
            'super': 'acusativo',
            'sub': 'acusativo/ablativo',
        }
        return prep_cases.get(prep.lower())
    
    def _is_valid_case_function_pair(
        self,
        case: str,
        function: SyntacticFunction
    ) -> bool:
        """Valida si la combinación caso-función es lógica"""
        valid_pairs = {
            'nominativo': [SyntacticFunction.SUBJECT, SyntacticFunction.PREDICATE_NOMINATIVE],
            'acusativo': [SyntacticFunction.DIRECT_OBJECT, SyntacticFunction.PREPOSITIONAL_OBJECT],
            'genitivo': [SyntacticFunction.GENITIVE_POSSESSIVE, SyntacticFunction.MODIFIER],
            'dativo': [SyntacticFunction.INDIRECT_OBJECT],
            'ablativo': [SyntacticFunction.ABLATIVE_MEANS, SyntacticFunction.ABLATIVE_MANNER, 
                        SyntacticFunction.ABLATIVE_TIME, SyntacticFunction.ADVERBIAL],
        }
        return function in valid_pairs.get(case.lower(), [SyntacticFunction.UNKNOWN])
    
    def _calculate_word_confidence(
        self,
        morphology: MorphologicalData,
        semantics: SemanticData,
        syntax: SyntacticAnalysis
    ) -> float:
        """Calcula confianza global de análisis de palabra"""
        scores = [
            morphology.confidence,
            syntax.confidence,
            0.6 if semantics.definitions else 0.3  # Semántica menos confiable
        ]
        return sum(scores) / len(scores)
    
    def _classify_sentence_type(self, doc) -> str:
        """Clasifica tipo de oración"""
        # Muy simplificado - se puede mejorar
        text = doc.text.lower()
        if '?' in text:
            return "interrogativa"
        elif any(word.pos_ == "VERB" and word.mood == "imperativo" for word in doc):
            return "imperativa"
        else:
            return "declarativa"
    
    def _detect_special_constructions(self, doc) -> List[str]:
        """Detecta construcciones especiales (ablativo absoluto, etc.)"""
        constructions = []
        
        # Ablativo absoluto: sustantivo + participio en ablativo
        for token in doc:
            if token.pos_ == "NOUN" and token.case == "ablativo":
                # Buscar participio cercano
                for child in token.subtree:
                    if child.pos_ == "VERB" and "part" in child.morph.get("VerbForm", []):
                        constructions.append("ablativo_absoluto")
                        break
        
        return constructions


# ============================================================================
# FUNCIONES AUXILIARES GLOBALES
# ============================================================================

def create_analysis_summary(
    analysis: ComprehensiveSentenceAnalysis
) -> Dict[str, Any]:
    """
    Crea un resumen ejecutivo del análisis para visualización rápida
    """
    return {
        'text': analysis.original_text,
        'translation': analysis.translation,
        'quality': analysis.quality_score,
        'main_verb': (
            analysis.word_analyses[analysis.main_verb_index].word
            if analysis.main_verb_index is not None
            else None
        ),
        'word_count': len(analysis.word_analyses),
        'issues_count': len(analysis.issues),
        'constructions': analysis.special_constructions,
        'status': analysis.validation_status
    }


def prepare_for_database(
    analysis: ComprehensiveSentenceAnalysis
) -> Dict[str, Any]:
    """
    Prepara el análisis para almacenamiento en BD
    """
    return {
        'sentence': {
            'text': analysis.original_text,
            'translation': analysis.translation,
            'sentence_type': analysis.sentence_type,
            'quality_score': analysis.quality_score,
            'validation_status': analysis.validation_status,
            'source': analysis.source,
            'lesson_number': analysis.lesson_number,
            'difficulty_level': analysis.difficulty_level,
        },
        'words': [
            {
                'position': wa.position_in_sentence,
                'text': wa.word,
                'lemma': wa.morphology.lemma,
                'pos': wa.morphology.pos.value,
                'case': wa.morphology.case,
                'number': wa.morphology.number,
                'gender': wa.morphology.gender,
                'tense': wa.morphology.tense,
                'mood': wa.morphology.mood,
                'voice': wa.morphology.voice,
                'syntactic_function': wa.syntax.function.value,
                'confidence': wa.overall_confidence,
            }
            for wa in analysis.word_analyses
        ]
    }
