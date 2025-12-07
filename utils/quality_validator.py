"""
UTILIDADES DE VALIDACIÓN Y CONTROL DE CALIDAD - Lingua Latina Viva

Sistema robusto para validar análisis y garantizar calidad de datos.
Incluye:
- Validaciones morfológicas
- Validaciones sintácticas
- Validaciones semánticas
- Detección de inconsistencias
- Reportes de calidad

Puede usarse independientemente del módulo principal.
"""

from typing import List, Dict, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import logging

from .comprehensive_analyzer import (
    ComprehensiveWordAnalysis,
    ComprehensiveSentenceAnalysis,
    MorphologicalData,
    WordClass,
    SyntacticFunction
)
from .vocabulary_manager import LatinWord

logger = logging.getLogger(__name__)


# ============================================================================
# TIPOS Y ENUMERACIONES
# ============================================================================

class ValidationLevel(Enum):
    """Niveles de validación"""
    BASIC = "basic"          # Validaciones básicas
    STANDARD = "standard"    # Validaciones estándar
    STRICT = "strict"        # Validaciones exhaustivas
    EXPERT = "expert"        # Validaciones de experto


class IssueType(Enum):
    """Tipos de problemas detectados"""
    MORPHOLOGY_MISSING = "morphology_missing"
    MORPHOLOGY_INVALID = "morphology_invalid"
    SYNTAX_UNCLEAR = "syntax_unclear"
    CASE_AGREEMENT = "case_agreement"
    GENDER_AGREEMENT = "gender_agreement"
    NUMBER_AGREEMENT = "number_agreement"
    SEMANTIC_MISSING = "semantic_missing"
    CONFIDENCE_LOW = "confidence_low"
    UNKNOWN = "unknown"


@dataclass
class ValidationIssue:
    """Un problema detectado durante validación"""
    type: IssueType
    severity: str  # "critical", "warning", "info"
    message: str
    element: str  # palabra, oración, etc.
    suggestion: Optional[str] = None
    confidence: float = 0.8


@dataclass
class ValidationReport:
    """Reporte completo de validación"""
    element: str
    is_valid: bool
    issues: List[ValidationIssue] = field(default_factory=list)
    
    # Scores
    morphology_score: float = 1.0
    syntax_score: float = 1.0
    semantic_score: float = 1.0
    overall_score: float = 1.0
    
    # Sugerencias
    recommendations: List[str] = field(default_factory=list)
    requires_manual_review: bool = False


# ============================================================================
# VALIDADOR MORFOLÓGICO
# ============================================================================

class MorphologyValidator:
    """Valida datos morfológicos"""
    
    # Paradigmas latinos conocidos
    VALID_CASES = {
        'nominativo', 'vocativo', 'acusativo',
        'genitivo', 'dativo', 'ablativo', 'locativo'
    }
    
    VALID_NUMBERS = {'singular', 'plural'}
    VALID_GENDERS = {'masculino', 'femenino', 'neutro'}
    VALID_PERSONS = {'1ª', '2ª', '3ª'}
    VALID_TENSES = {
        'presente', 'imperfecto', 'futuro',
        'perfecto', 'pluscuamperfecto', 'futuro perfecto'
    }
    VALID_MOODS = {'indicativo', 'subjuntivo', 'imperativo', 'infinitivo'}
    VALID_VOICES = {'activo', 'pasivo'}
    VALID_DEGREES = {'positivo', 'comparativo', 'superlativo'}
    
    NOUN_DECLENSIONS = {'1ª', '2ª', '3ª', '4ª', '5ª'}
    VERB_CONJUGATIONS = {'1ª', '2ª', '3ª', '4ª'}
    
    def validate_morphology(
        self,
        morphology: MorphologicalData
    ) -> ValidationReport:
        """Valida un análisis morfológico"""
        report = ValidationReport(
            element=morphology.lemma,
            is_valid=True
        )
        
        issues = []
        
        # Validar lemma
        if not morphology.lemma or not morphology.lemma.strip():
            issues.append(ValidationIssue(
                type=IssueType.MORPHOLOGY_MISSING,
                severity="critical",
                message="Lema vacío",
                element=morphology.lemma or "[vacío]"
            ))
            report.is_valid = False
        
        # Validar POS
        if morphology.pos == WordClass.UNKNOWN:
            issues.append(ValidationIssue(
                type=IssueType.MORPHOLOGY_MISSING,
                severity="warning",
                message="Categoría gramatical desconocida",
                element=morphology.lemma,
                suggestion="Requiere revisión manual"
            ))
            report.morphology_score -= 0.3
        
        # Validaciones específicas por POS
        if morphology.pos == WordClass.NOUN:
            issues.extend(self._validate_noun(morphology))
        elif morphology.pos == WordClass.VERB:
            issues.extend(self._validate_verb(morphology))
        elif morphology.pos == WordClass.ADJECTIVE:
            issues.extend(self._validate_adjective(morphology))
        
        # Validar confianza
        if morphology.confidence < 0.5:
            issues.append(ValidationIssue(
                type=IssueType.CONFIDENCE_LOW,
                severity="warning",
                message=f"Confianza muy baja: {morphology.confidence:.2f}",
                element=morphology.lemma
            ))
            report.morphology_score -= 0.2
        
        report.issues.extend(issues)
        report.is_valid = len([i for i in issues if i.severity == "critical"]) == 0
        
        return report
    
    def _validate_noun(self, morphology: MorphologicalData) -> List[ValidationIssue]:
        """Valida sustantivo"""
        issues = []
        
        # Verificar género
        if not morphology.gender:
            issues.append(ValidationIssue(
                type=IssueType.MORPHOLOGY_MISSING,
                severity="warning",
                message="Género faltante para sustantivo",
                element=morphology.lemma,
                suggestion=f"Especificar género (m/f/n)"
            ))
        elif morphology.gender not in self.VALID_GENDERS:
            issues.append(ValidationIssue(
                type=IssueType.MORPHOLOGY_INVALID,
                severity="warning",
                message=f"Género inválido: {morphology.gender}",
                element=morphology.lemma
            ))
        
        # Verificar declinación
        if not morphology.declension:
            issues.append(ValidationIssue(
                type=IssueType.MORPHOLOGY_MISSING,
                severity="info",
                message="Declinación no especificada",
                element=morphology.lemma
            ))
        elif morphology.declension not in self.NOUN_DECLENSIONS:
            issues.append(ValidationIssue(
                type=IssueType.MORPHOLOGY_INVALID,
                severity="warning",
                message=f"Declinación inválida: {morphology.declension}",
                element=morphology.lemma
            ))
        
        # Verificar caso (debería estar presente para nombres)
        if not morphology.case:
            issues.append(ValidationIssue(
                type=IssueType.MORPHOLOGY_MISSING,
                severity="info",
                message="Caso no especificado",
                element=morphology.lemma
            ))
        elif morphology.case not in self.VALID_CASES:
            issues.append(ValidationIssue(
                type=IssueType.MORPHOLOGY_INVALID,
                severity="warning",
                message=f"Caso inválido: {morphology.case}",
                element=morphology.lemma
            ))
        
        return issues
    
    def _validate_verb(self, morphology: MorphologicalData) -> List[ValidationIssue]:
        """Valida verbo"""
        issues = []
        
        # Verificar conjugación
        if not morphology.conjugation:
            issues.append(ValidationIssue(
                type=IssueType.MORPHOLOGY_MISSING,
                severity="info",
                message="Conjugación no especificada",
                element=morphology.lemma
            ))
        elif morphology.conjugation not in self.VERB_CONJUGATIONS:
            issues.append(ValidationIssue(
                type=IssueType.MORPHOLOGY_INVALID,
                severity="warning",
                message=f"Conjugación inválida: {morphology.conjugation}",
                element=morphology.lemma
            ))
        
        # Verificar persona
        if morphology.person:
            if morphology.person not in self.VALID_PERSONS:
                issues.append(ValidationIssue(
                    type=IssueType.MORPHOLOGY_INVALID,
                    severity="warning",
                    message=f"Persona inválida: {morphology.person}",
                    element=morphology.lemma
                ))
        
        # Verificar tiempo
        if morphology.tense:
            if morphology.tense not in self.VALID_TENSES:
                issues.append(ValidationIssue(
                    type=IssueType.MORPHOLOGY_INVALID,
                    severity="warning",
                    message=f"Tiempo inválido: {morphology.tense}",
                    element=morphology.lemma
                ))
        
        return issues
    
    def _validate_adjective(self, morphology: MorphologicalData) -> List[ValidationIssue]:
        """Valida adjetivo"""
        issues = []
        
        # Debe tener género, caso, número como mínimo
        required = ['gender', 'case', 'number']
        for attr in required:
            if not getattr(morphology, attr):
                issues.append(ValidationIssue(
                    type=IssueType.MORPHOLOGY_MISSING,
                    severity="warning",
                    message=f"{attr.capitalize()} faltante para adjetivo",
                    element=morphology.lemma
                ))
        
        return issues


# ============================================================================
# VALIDADOR SINTÁCTICO
# ============================================================================

class SyntaxValidator:
    """Valida análisis sintáctico"""
    
    # Reglas de concordancia
    NOMINATIVE_FUNCTIONS = {
        SyntacticFunction.SUBJECT,
        SyntacticFunction.PREDICATE_NOMINATIVE
    }
    
    ACCUSATIVE_FUNCTIONS = {
        SyntacticFunction.DIRECT_OBJECT,
        SyntacticFunction.PREPOSITIONAL_OBJECT
    }
    
    GENITIVE_FUNCTIONS = {
        SyntacticFunction.GENITIVE_POSSESSIVE,
        SyntacticFunction.MODIFIER
    }
    
    DATIVE_FUNCTIONS = {
        SyntacticFunction.INDIRECT_OBJECT
    }
    
    ABLATIVE_FUNCTIONS = {
        SyntacticFunction.ABLATIVE_MEANS,
        SyntacticFunction.ABLATIVE_MANNER,
        SyntacticFunction.ABLATIVE_TIME,
        SyntacticFunction.ADVERBIAL
    }
    
    def validate_sentence_syntax(
        self,
        analysis: ComprehensiveSentenceAnalysis
    ) -> ValidationReport:
        """Valida sintaxis de oración completa"""
        report = ValidationReport(
            element=analysis.original_text,
            is_valid=True
        )
        
        issues = []
        
        # Verificar que hay palabras analizadas
        if not analysis.word_analyses:
            issues.append(ValidationIssue(
                type=IssueType.SYNTAX_UNCLEAR,
                severity="critical",
                message="Sin análisis de palabras",
                element=analysis.original_text
            ))
            report.is_valid = False
        
        # Validar cada palabra
        for word_analysis in analysis.word_analyses:
            issues.extend(self._validate_word_syntax(word_analysis))
        
        # Validaciones a nivel de oración
        if analysis.main_verb_index is None:
            issues.append(ValidationIssue(
                type=IssueType.SYNTAX_UNCLEAR,
                severity="warning",
                message="No se encontró verbo principal",
                element=analysis.original_text
            ))
            report.syntax_score -= 0.2
        
        report.issues.extend(issues)
        report.is_valid = len([i for i in issues if i.severity == "critical"]) == 0
        
        return report
    
    def _validate_word_syntax(
        self,
        word_analysis: ComprehensiveWordAnalysis
    ) -> List[ValidationIssue]:
        """Valida sintaxis de una palabra"""
        issues = []
        
        # Verificar función sintáctica
        if word_analysis.syntax.function == SyntacticFunction.UNKNOWN:
            issues.append(ValidationIssue(
                type=IssueType.SYNTAX_UNCLEAR,
                severity="warning",
                message="Función sintáctica desconocida",
                element=word_analysis.word
            ))
        
        # Validar concordancia caso-función
        if word_analysis.morphology.case and word_analysis.syntax.function:
            if not self._is_valid_case_function_pair(
                word_analysis.morphology.case,
                word_analysis.syntax.function
            ):
                issues.append(ValidationIssue(
                    type=IssueType.CASE_AGREEMENT,
                    severity="warning",
                    message=(
                        f"Posible conflicto: {word_analysis.morphology.case} "
                        f"con función {word_analysis.syntax.function.value}"
                    ),
                    element=word_analysis.word,
                    suggestion="Revisar manualmente"
                ))
        
        return issues
    
    def _is_valid_case_function_pair(
        self,
        case: str,
        function: SyntacticFunction
    ) -> bool:
        """Verifica si la combinación caso-función es válida"""
        case_lower = case.lower()
        
        valid_combinations = {
            'nominativo': self.NOMINATIVE_FUNCTIONS,
            'acusativo': self.ACCUSATIVE_FUNCTIONS,
            'genitivo': self.GENITIVE_FUNCTIONS,
            'dativo': self.DATIVE_FUNCTIONS,
            'ablativo': self.ABLATIVE_FUNCTIONS,
        }
        
        if case_lower not in valid_combinations:
            return True  # Caso desconocido, no validar
        
        return function in valid_combinations[case_lower]


# ============================================================================
# VALIDADOR SEMÁNTICO
# ============================================================================

class SemanticValidator:
    """Valida información semántica"""
    
    def validate_semantic_data(
        self,
        word_analysis: ComprehensiveWordAnalysis
    ) -> ValidationReport:
        """Valida datos semánticos"""
        report = ValidationReport(
            element=word_analysis.word,
            is_valid=True
        )
        
        issues = []
        semantics = word_analysis.semantics
        
        # Validar definiciones
        if not semantics.definitions or (
            len(semantics.definitions) == 1 and
            semantics.definitions[0].startswith("[")
        ):
            issues.append(ValidationIssue(
                type=IssueType.SEMANTIC_MISSING,
                severity="info",
                message="Sin definición",
                element=word_analysis.word,
                suggestion="Añadir definición"
            ))
            report.semantic_score -= 0.5
        
        # Validar frecuencia
        if semantics.frequency_score is None:
            issues.append(ValidationIssue(
                type=IssueType.SEMANTIC_MISSING,
                severity="info",
                message="Frecuencia no calculada",
                element=word_analysis.word
            ))
        
        report.issues.extend(issues)
        return report


# ============================================================================
# VALIDADOR INTEGRAL
# ============================================================================

class ComprehensiveValidator:
    """
    Validador integral que combina todas las validaciones
    """
    
    def __init__(self, level: ValidationLevel = ValidationLevel.STANDARD):
        self.level = level
        self.morph_validator = MorphologyValidator()
        self.syntax_validator = SyntaxValidator()
        self.semantic_validator = SemanticValidator()
    
    def validate_sentence(
        self,
        analysis: ComprehensiveSentenceAnalysis
    ) -> ValidationReport:
        """
        Valida análisis completo de oración
        """
        report = ValidationReport(
            element=analysis.original_text,
            is_valid=True
        )
        
        all_issues = []
        scores = []
        
        # Validación morfológica
        for word_analysis in analysis.word_analyses:
            morph_report = self.morph_validator.validate_morphology(
                word_analysis.morphology
            )
            all_issues.extend(morph_report.issues)
            scores.append(morph_report.morphology_score)
        
        report.morphology_score = (
            sum(scores) / len(scores) if scores else 1.0
        )
        
        # Validación sintáctica
        syntax_report = self.syntax_validator.validate_sentence_syntax(analysis)
        all_issues.extend(syntax_report.issues)
        report.syntax_score = syntax_report.syntax_score
        
        # Validación semántica
        semantic_scores = []
        for word_analysis in analysis.word_analyses:
            semantic_report = self.semantic_validator.validate_semantic_data(
                word_analysis
            )
            all_issues.extend(semantic_report.issues)
            semantic_scores.append(semantic_report.semantic_score)
        
        report.semantic_score = (
            sum(semantic_scores) / len(semantic_scores) if semantic_scores else 1.0
        )
        
        # Calcular score overall
        report.overall_score = (
            (report.morphology_score + report.syntax_score + report.semantic_score) / 3
        )
        
        # Generar recomendaciones
        report.recommendations = self._generate_recommendations(all_issues, report)
        
        # Determinar si requiere revisión manual
        critical_issues = [i for i in all_issues if i.severity == "critical"]
        report.requires_manual_review = len(critical_issues) > 0 or report.overall_score < 0.6
        
        report.issues = all_issues
        report.is_valid = len(critical_issues) == 0
        
        return report
    
    def _generate_recommendations(
        self,
        issues: List[ValidationIssue],
        report: ValidationReport
    ) -> List[str]:
        """Genera recomendaciones basadas en problemas"""
        recommendations = []
        
        # Agrupar problemas por tipo
        by_type = {}
        for issue in issues:
            if issue.type not in by_type:
                by_type[issue.type] = []
            by_type[issue.type].append(issue)
        
        # Generar recomendaciones
        if IssueType.MORPHOLOGY_MISSING in by_type:
            count = len(by_type[IssueType.MORPHOLOGY_MISSING])
            recommendations.append(f"⚠️ Completar {count} análisis morfológicos")
        
        if IssueType.CASE_AGREEMENT in by_type:
            recommendations.append("⚠️ Revisar concordancia de casos")
        
        if IssueType.SEMANTIC_MISSING in by_type:
            count = len(by_type[IssueType.SEMANTIC_MISSING])
            recommendations.append(f"📝 Añadir {count} definiciones")
        
        if report.overall_score < 0.5:
            recommendations.append("🔴 Análisis de baja calidad. Requiere revisión exhaustiva.")
        elif report.overall_score < 0.7:
            recommendations.append("🟡 Calidad media. Revisar puntos problemáticos.")
        else:
            recommendations.append("✅ Análisis de buena calidad")
        
        return recommendations
    
    def validate_vocabulary(self, word: LatinWord) -> ValidationReport:
        """Valida entrada de vocabulario"""
        report = ValidationReport(element=word.lemma, is_valid=True)
        
        issues = []
        
        # Verificar definiciones
        if not word.definitions:
            issues.append(ValidationIssue(
                type=IssueType.SEMANTIC_MISSING,
                severity="critical",
                message="Sin definiciones",
                element=word.lemma,
                suggestion="Añadir al menos una definición"
            ))
        elif not any(d.is_primary for d in word.definitions):
            issues.append(ValidationIssue(
                type=IssueType.SEMANTIC_MISSING,
                severity="warning",
                message="Sin definición primaria",
                element=word.lemma,
                suggestion="Marcar una definición como primaria"
            ))
        
        # Verificar información gramatical
        if not word.pos:
            issues.append(ValidationIssue(
                type=IssueType.MORPHOLOGY_MISSING,
                severity="critical",
                message="POS no especificada",
                element=word.lemma
            ))
        
        if word.pos in ["sustantivo", "noun"]:
            if not word.gender:
                issues.append(ValidationIssue(
                    type=IssueType.MORPHOLOGY_MISSING,
                    severity="warning",
                    message="Género faltante",
                    element=word.lemma
                ))
            if not word.declension:
                issues.append(ValidationIssue(
                    type=IssueType.MORPHOLOGY_MISSING,
                    severity="warning",
                    message="Declinación faltante",
                    element=word.lemma
                ))
        
        report.issues = issues
        report.is_valid = len([i for i in issues if i.severity == "critical"]) == 0
        
        return report
