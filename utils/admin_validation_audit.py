"""
MÓDULO DE VALIDACIÓN Y AUDITORÍA - Panel Admin

Sistema integral de:
1. Validación de Duplicados - Detección de datos ya existentes
2. Validación de Completitud - Asegurar información completa
3. Auditoría - Registro de todas las cargas (quién, qué, cuándo)

Filosofía: Garantizar integridad de datos y trazabilidad completa.
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
import json
import logging
import hashlib
from enum import Enum
from sqlmodel import select
from database.connection import get_session
from database import Word, Text, SentenceAnalysis

logger = logging.getLogger(__name__)


# ============================================================================
# ENUMERACIONES
# ============================================================================

class AuditAction(Enum):
    """Tipos de acciones auditadas"""
    VOCABULARY_ADD = "vocabulary_add"
    VOCABULARY_UPDATE = "vocabulary_update"
    VOCABULARY_DELETE = "vocabulary_delete"
    SENTENCE_ADD = "sentence_add"
    SENTENCE_UPDATE = "sentence_update"
    SENTENCE_DELETE = "sentence_delete"
    TEXT_ADD = "text_add"
    TEXT_UPDATE = "text_update"
    TEXT_DELETE = "text_delete"
    VALIDATION_ERROR = "validation_error"
    DUPLICATE_DETECTED = "duplicate_detected"


class ValidationLevel(Enum):
    """Niveles de validación"""
    STRICT = "strict"      # Rechaza cualquier duplicado, requiere completitud total
    MODERATE = "moderate"  # Advierte sobre duplicados, requiere campos obligatorios
    LENIENT = "lenient"    # Solo advierte, permite más flexibilidad


# ============================================================================
# DATACLASSES PARA AUDITORÍA
# ============================================================================

@dataclass
class AuditLog:
    """Registro de auditoría para cada operación"""
    timestamp: datetime = field(default_factory=datetime.now)
    action: AuditAction = AuditAction.VOCABULARY_ADD
    user_id: Optional[str] = None  # Usuario que realizó la acción
    data_type: str = ""  # vocabulary, sentence, text
    data_id: Optional[int] = None
    original_value: Optional[Dict[str, Any]] = None
    new_value: Optional[Dict[str, Any]] = None
    validation_status: str = "success"  # success, warning, error
    error_message: Optional[str] = None
    ip_address: Optional[str] = None
    duplicates_found: List[Dict[str, Any]] = field(default_factory=list)
    completeness_score: float = 1.0  # 0-1: qué tan completo está el registro
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario para almacenamiento"""
        return {
            'timestamp': self.timestamp.isoformat(),
            'action': self.action.value,
            'user_id': self.user_id,
            'data_type': self.data_type,
            'data_id': self.data_id,
            'original_value': self.original_value,
            'new_value': self.new_value,
            'validation_status': self.validation_status,
            'error_message': self.error_message,
            'ip_address': self.ip_address,
            'duplicates_found': self.duplicates_found,
            'completeness_score': self.completeness_score,
        }
    
    def to_json(self) -> str:
        """Convierte a JSON"""
        return json.dumps(self.to_dict(), default=str, ensure_ascii=False)


@dataclass
class ValidationResult:
    """Resultado de una validación"""
    is_valid: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    duplicates: List[Dict[str, Any]] = field(default_factory=list)
    completeness_score: float = 1.0
    missing_fields: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)


# ============================================================================
# VALIDADOR DE DUPLICADOS
# ============================================================================

class DuplicateValidator:
    """Detecta duplicados en la base de datos"""
    
    @staticmethod
    def check_vocabulary_duplicate(
        latin_word: str,
        level: int = None,
        strict: bool = True
    ) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Detecta duplicados de vocabulario
        
        Args:
            latin_word: Palabra en latín
            level: Nivel (opcional para búsqueda más específica)
            strict: Si True, busca coincidencias exactas. Si False, busca similares
        
        Returns:
            (es_duplicado, lista_de_duplicados)
        """
        duplicates = []
        
        try:
            with get_session() as session:
                # Búsqueda exacta
                statement = select(Word).where(
                    Word.latin == latin_word.strip()
                )
                exact_matches = session.exec(statement).all()
                
                if exact_matches:
                    for match in exact_matches:
                        duplicates.append({
                            'id': match.id,
                            'type': 'exact_match',
                            'latin': match.latin,
                            'translation': match.translation,
                            'level': match.level,
                            'pos': match.part_of_speech,
                        })
                
                # Búsqueda de similares (si no es strict)
                if not strict and not duplicates:
                    # Buscar variaciones de la palabra base
                    from difflib import SequenceMatcher
                    
                    all_words = session.exec(select(Word)).all()
                    similar_threshold = 0.85
                    
                    for word in all_words:
                        similarity = SequenceMatcher(
                            None,
                            latin_word.lower(),
                            word.latin.lower()
                        ).ratio()
                        
                        if similarity > similar_threshold:
                            duplicates.append({
                                'id': word.id,
                                'type': 'similar',
                                'similarity': round(similarity, 2),
                                'latin': word.latin,
                                'translation': word.translation,
                                'level': word.level,
                                'pos': word.part_of_speech,
                            })
        
        except Exception as e:
            logger.error(f"Error checking vocabulary duplicates: {e}")
            return False, []
        
        return len(duplicates) > 0, duplicates
    
    @staticmethod
    def check_sentence_duplicate(
        latin_text: str,
        translation: str = None
    ) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Detecta duplicados de oraciones
        
        Args:
            latin_text: Texto de la oración en latín
            translation: Traducción (opcional)
        
        Returns:
            (es_duplicado, lista_de_duplicados)
        """
        duplicates = []
        
        try:
            with get_session() as session:
                # Normalizar texto para comparación
                normalized = latin_text.strip().lower()
                
                # Búsqueda exacta
                statement = select(SentenceAnalysis).where(
                    SentenceAnalysis.latin_text == latin_text.strip()
                )
                exact_matches = session.exec(statement).all()
                
                if exact_matches:
                    for match in exact_matches:
                        duplicates.append({
                            'id': match.id,
                            'type': 'exact_match',
                            'latin_text': match.latin_text,
                            'spanish_translation': match.spanish_translation,
                            'difficulty': match.complexity_level,
                        })
        
        except Exception as e:
            logger.error(f"Error checking sentence duplicates: {e}")
            return False, []
        
        return len(duplicates) > 0, duplicates
    
    @staticmethod
    def check_text_duplicate(title: str, author: str = None) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Detecta duplicados de textos
        
        Args:
            title: Título del texto
            author: Autor (opcional)
        
        Returns:
            (es_duplicado, lista_de_duplicados)
        """
        duplicates = []
        
        try:
            with get_session() as session:
                # Búsqueda por título
                statement = select(Text).where(
                    Text.title == title.strip()
                )
                exact_matches = session.exec(statement).all()
                
                if exact_matches:
                    for match in exact_matches:
                        duplicates.append({
                            'id': match.id,
                            'type': 'title_duplicate',
                            'title': match.title,
                            'author': match.author,
                            'difficulty': match.difficulty,
                            'created_at': match.created_at.isoformat() if match.created_at else None,
                        })
        
        except Exception as e:
            logger.error(f"Error checking text duplicates: {e}")
            return False, []
        
        return len(duplicates) > 0, duplicates


# ============================================================================
# VALIDADOR DE COMPLETITUD
# ============================================================================

class CompletenessValidator:
    """Valida que los datos estén completos y sean de calidad"""
    
    # Esquemas de completitud para cada tipo
    VOCABULARY_REQUIRED_FIELDS = [
        'latin_word',
        'translation',
        'part_of_speech',
    ]
    
    VOCABULARY_IMPORTANT_FIELDS = [
        'genitive',  # Para sustantivos
        'principal_parts',  # Para verbos
        'level',
    ]
    
    SENTENCE_REQUIRED_FIELDS = [
        'latin_text',
        'translation',
        'level',
    ]
    
    SENTENCE_IMPORTANT_FIELDS = [
        'grammar_focus',
    ]
    
    TEXT_REQUIRED_FIELDS = [
        'title',
        'author',
        'content',
        'difficulty',
    ]
    
    TEXT_IMPORTANT_FIELDS = [
        'source_type',
    ]
    
    @staticmethod
    def validate_vocabulary(data: Dict[str, Any]) -> ValidationResult:
        """Valida completitud de datos de vocabulario"""
        result = ValidationResult()
        
        # Verificar campos obligatorios
        for field in CompletenessValidator.VOCABULARY_REQUIRED_FIELDS:
            if field not in data or not data[field]:
                result.is_valid = False
                result.errors.append(f"Campo obligatorio faltante: {field}")
                result.missing_fields.append(field)
        
        # Verificar campos importantes
        important_present = 0
        for field in CompletenessValidator.VOCABULARY_IMPORTANT_FIELDS:
            if field in data and data[field]:
                important_present += 1
        
        # Validaciones específicas según POS
        pos = data.get('part_of_speech', '')
        
        if pos == 'noun':
            if not data.get('genitive'):
                result.warnings.append(
                    "Para sustantivos se recomienda incluir el genitivo"
                )
                result.suggestions.append("Ej: puella → puellae")
            if not data.get('gender'):
                result.warnings.append("El género del sustantivo no está especificado")
        
        elif pos == 'verb':
            if not data.get('principal_parts'):
                result.errors.append("Para verbos las partes principales son obligatorias")
                result.is_valid = False
            if not data.get('conjugation'):
                result.warnings.append("Se recomienda especificar la conjugación")
        
        # Calcular puntuación de completitud
        total_fields = len(CompletenessValidator.VOCABULARY_REQUIRED_FIELDS) + \
                      len(CompletenessValidator.VOCABULARY_IMPORTANT_FIELDS)
        present_fields = len(CompletenessValidator.VOCABULARY_REQUIRED_FIELDS)
        present_fields += important_present
        result.completeness_score = min(1.0, present_fields / total_fields)
        
        return result
    
    @staticmethod
    def validate_sentence(data: Dict[str, Any]) -> ValidationResult:
        """Valida completitud de datos de oración"""
        result = ValidationResult()
        
        # Verificar campos obligatorios
        for field in CompletenessValidator.SENTENCE_REQUIRED_FIELDS:
            if field not in data or not data[field]:
                result.is_valid = False
                result.errors.append(f"Campo obligatorio faltante: {field}")
                result.missing_fields.append(field)
        
        # Validaciones de contenido
        latin_text = data.get('latin_text', '').strip()
        if latin_text:
            # Verificar que tiene longitud razonable
            if len(latin_text) < 5:
                result.errors.append("La oración es demasiado corta")
                result.is_valid = False
            
            # Verificar terminación apropiada
            if not latin_text.endswith(('.', '!', '?')):
                result.warnings.append(
                    "La oración no termina con puntuación. Se recomienda agregarla."
                )
        
        translation = data.get('translation', '').strip()
        if translation and len(translation) < 3:
            result.errors.append("La traducción es demasiado corta")
            result.is_valid = False
        
        # Calcular completitud
        total_fields = len(CompletenessValidator.SENTENCE_REQUIRED_FIELDS)
        present_fields = sum(
            1 for field in CompletenessValidator.SENTENCE_REQUIRED_FIELDS
            if field in data and data[field]
        )
        result.completeness_score = min(1.0, present_fields / total_fields)
        
        return result
    
    @staticmethod
    def validate_text(data: Dict[str, Any]) -> ValidationResult:
        """Valida completitud de datos de texto"""
        result = ValidationResult()
        
        # Verificar campos obligatorios
        for field in CompletenessValidator.TEXT_REQUIRED_FIELDS:
            if field not in data or not data[field]:
                result.is_valid = False
                result.errors.append(f"Campo obligatorio faltante: {field}")
                result.missing_fields.append(field)
        
        # Validaciones de contenido
        content = data.get('content', '').strip()
        if content:
            word_count = len(content.split())
            
            if word_count < 10:
                result.errors.append(
                    f"El texto es demasiado corto ({word_count} palabras). "
                    "Mínimo 10 palabras recomendadas."
                )
                result.is_valid = False
            
            # Sugerencias según longitud
            if word_count < 50:
                result.warnings.append(
                    f"Texto muy corto ({word_count} palabras). "
                    "Se recomienda mínimo 50 para un análisis completo."
                )
            elif word_count > 10000:
                result.warnings.append(
                    f"Texto muy largo ({word_count} palabras). "
                    "Considere dividirlo en secciones."
                )
        
        # Calcular completitud
        total_fields = len(CompletenessValidator.TEXT_REQUIRED_FIELDS)
        present_fields = sum(
            1 for field in CompletenessValidator.TEXT_REQUIRED_FIELDS
            if field in data and data[field]
        )
        result.completeness_score = min(1.0, present_fields / total_fields)
        
        return result


# ============================================================================
# GESTOR DE AUDITORÍA
# ============================================================================

class AuditManager:
    """Gestor central de auditoría"""
    
    def __init__(self, user_id: Optional[str] = None, ip_address: Optional[str] = None):
        self.user_id = user_id or "anonymous"
        self.ip_address = ip_address
        self.logs: List[AuditLog] = []
        self._load_logs()
    
    def _load_logs(self) -> None:
        """Carga logs existentes del archivo (si existe)"""
        # Los logs se almacenarán en memoria durante la sesión
        # Y se pueden persistir en BD o archivo si es necesario
        pass
    
    def create_vocabulary_audit(
        self,
        action: AuditAction,
        data: Dict[str, Any],
        validation_result: ValidationResult,
        data_id: Optional[int] = None,
        duplicates_found: List[Dict] = None
    ) -> AuditLog:
        """Crea un log de auditoría para vocabulario"""
        
        log = AuditLog(
            action=action,
            user_id=self.user_id,
            data_type='vocabulary',
            data_id=data_id,
            new_value=data,
            validation_status='success' if validation_result.is_valid else 'error',
            error_message='; '.join(validation_result.errors) if validation_result.errors else None,
            ip_address=self.ip_address,
            duplicates_found=duplicates_found or [],
            completeness_score=validation_result.completeness_score,
        )
        
        self.logs.append(log)
        logger.info(f"Audit log created: {log.action.value} by {self.user_id}")
        
        return log
    
    def create_sentence_audit(
        self,
        action: AuditAction,
        data: Dict[str, Any],
        validation_result: ValidationResult,
        data_id: Optional[int] = None,
        duplicates_found: List[Dict] = None
    ) -> AuditLog:
        """Crea un log de auditoría para oraciones"""
        
        log = AuditLog(
            action=action,
            user_id=self.user_id,
            data_type='sentence',
            data_id=data_id,
            new_value=data,
            validation_status='success' if validation_result.is_valid else 'error',
            error_message='; '.join(validation_result.errors) if validation_result.errors else None,
            ip_address=self.ip_address,
            duplicates_found=duplicates_found or [],
            completeness_score=validation_result.completeness_score,
        )
        
        self.logs.append(log)
        logger.info(f"Audit log created: {log.action.value} by {self.user_id}")
        
        return log
    
    def create_text_audit(
        self,
        action: AuditAction,
        data: Dict[str, Any],
        validation_result: ValidationResult,
        data_id: Optional[int] = None,
        duplicates_found: List[Dict] = None
    ) -> AuditLog:
        """Crea un log de auditoría para textos"""
        
        log = AuditLog(
            action=action,
            user_id=self.user_id,
            data_type='text',
            data_id=data_id,
            new_value=data,
            validation_status='success' if validation_result.is_valid else 'error',
            error_message='; '.join(validation_result.errors) if validation_result.errors else None,
            ip_address=self.ip_address,
            duplicates_found=duplicates_found or [],
            completeness_score=validation_result.completeness_score,
        )
        
        self.logs.append(log)
        logger.info(f"Audit log created: {log.action.value} by {self.user_id}")
        
        return log
    
    def get_logs(self, data_type: Optional[str] = None) -> List[AuditLog]:
        """Obtiene logs filtrados por tipo de dato"""
        if data_type:
            return [log for log in self.logs if log.data_type == data_type]
        return self.logs
    
    def export_audit_report(self, format: str = 'json') -> str:
        """Exporta logs en formato especificado"""
        if format == 'json':
            return json.dumps(
                [log.to_dict() for log in self.logs],
                default=str,
                ensure_ascii=False,
                indent=2
            )
        elif format == 'csv':
            # CSV format
            import csv
            import io
            
            output = io.StringIO()
            if not self.logs:
                return ""
            
            fieldnames = list(self.logs[0].to_dict().keys())
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            
            for log in self.logs:
                row = log.to_dict()
                # Convertir valores complejos a strings
                for key in row:
                    if isinstance(row[key], (dict, list)):
                        row[key] = json.dumps(row[key], ensure_ascii=False)
                writer.writerow(row)
            
            return output.getvalue()
        else:
            raise ValueError(f"Formato no soportado: {format}")


# ============================================================================
# VALIDADOR INTEGRADO (COMBINA DUPLICADOS + COMPLETITUD + AUDITORÍA)
# ============================================================================

class ComprehensiveValidator:
    """Validador integral que combina todos los controles"""
    
    def __init__(
        self,
        level: ValidationLevel = ValidationLevel.MODERATE,
        user_id: Optional[str] = None
    ):
        self.level = level
        self.duplicate_validator = DuplicateValidator()
        self.completeness_validator = CompletenessValidator()
        self.audit_manager = AuditManager(user_id=user_id)
    
    def validate_vocabulary_complete(
        self,
        data: Dict[str, Any],
        check_duplicates: bool = True
    ) -> Tuple[ValidationResult, Optional[AuditLog]]:
        """
        Validación completa para vocabulario
        
        Returns:
            (ValidationResult, AuditLog)
        """
        result = self.completeness_validator.validate_vocabulary(data)
        duplicates = []
        
        if check_duplicates:
            is_dup, duplicates = self.duplicate_validator.check_vocabulary_duplicate(
                data.get('latin_word', ''),
                strict=(self.level == ValidationLevel.STRICT)
            )
            
            if is_dup and self.level == ValidationLevel.STRICT:
                result.is_valid = False
                result.errors.insert(0, "⚠️ DUPLICADO DETECTADO: Esta palabra ya existe en la BD")
            elif is_dup:
                result.warnings.insert(0, "⚠️ Posible duplicado: Verifique la lista abajo")
            
            result.duplicates = duplicates
        
        # Crear log de auditoría
        audit_log = self.audit_manager.create_vocabulary_audit(
            action=AuditAction.VOCABULARY_ADD,
            data=data,
            validation_result=result,
            duplicates_found=duplicates
        )
        
        return result, audit_log
    
    def validate_sentence_complete(
        self,
        data: Dict[str, Any],
        check_duplicates: bool = True
    ) -> Tuple[ValidationResult, Optional[AuditLog]]:
        """
        Validación completa para oraciones
        
        Returns:
            (ValidationResult, AuditLog)
        """
        result = self.completeness_validator.validate_sentence(data)
        duplicates = []
        
        if check_duplicates:
            is_dup, duplicates = self.duplicate_validator.check_sentence_duplicate(
                data.get('latin_text', '')
            )
            
            if is_dup and self.level == ValidationLevel.STRICT:
                result.is_valid = False
                result.errors.insert(0, "⚠️ DUPLICADO DETECTADO: Esta oración ya existe")
            elif is_dup:
                result.warnings.insert(0, "⚠️ Posible duplicado: Verifique abajo")
            
            result.duplicates = duplicates
        
        # Crear log de auditoría
        audit_log = self.audit_manager.create_sentence_audit(
            action=AuditAction.SENTENCE_ADD,
            data=data,
            validation_result=result,
            duplicates_found=duplicates
        )
        
        return result, audit_log
    
    def validate_text_complete(
        self,
        data: Dict[str, Any],
        check_duplicates: bool = True
    ) -> Tuple[ValidationResult, Optional[AuditLog]]:
        """
        Validación completa para textos
        
        Returns:
            (ValidationResult, AuditLog)
        """
        result = self.completeness_validator.validate_text(data)
        duplicates = []
        
        if check_duplicates:
            is_dup, duplicates = self.duplicate_validator.check_text_duplicate(
                data.get('title', '')
            )
            
            if is_dup and self.level == ValidationLevel.STRICT:
                result.is_valid = False
                result.errors.insert(0, "⚠️ DUPLICADO DETECTADO: Este texto ya existe")
            elif is_dup:
                result.warnings.insert(0, "⚠️ Posible duplicado: Verifique abajo")
            
            result.duplicates = duplicates
        
        # Crear log de auditoría
        audit_log = self.audit_manager.create_text_audit(
            action=AuditAction.TEXT_ADD,
            data=data,
            validation_result=result,
            duplicates_found=duplicates
        )
        
        return result, audit_log
    
    def get_audit_logs(self) -> List[AuditLog]:
        """Obtiene todos los logs de auditoría"""
        return self.audit_manager.logs
    
    def export_audit_report(self, format: str = 'json') -> str:
        """Exporta reporte de auditoría"""
        return self.audit_manager.export_audit_report(format)


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def format_validation_result_for_ui(result: ValidationResult) -> Dict[str, Any]:
    """
    Formatea el resultado de validación para mostrar en UI
    
    Returns:
        Dict con claves: 'valid', 'status', 'errors', 'warnings', 'duplicates', 'score'
    """
    return {
        'valid': result.is_valid,
        'status': '✅ VÁLIDO' if result.is_valid else '❌ INVÁLIDO',
        'errors': result.errors,
        'warnings': result.warnings,
        'duplicates': result.duplicates,
        'completeness_score': result.completeness_score,
        'completeness_percent': f"{result.completeness_score * 100:.0f}%",
        'missing_fields': result.missing_fields,
        'suggestions': result.suggestions,
        'has_warnings': len(result.warnings) > 0,
        'has_errors': len(result.errors) > 0,
        'has_duplicates': len(result.duplicates) > 0,
    }


def format_audit_log_for_ui(log: AuditLog) -> Dict[str, Any]:
    """Formatea log de auditoría para mostrar en UI"""
    return {
        'timestamp': log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        'action': log.action.value,
        'user': log.user_id,
        'data_type': log.data_type,
        'status': log.validation_status.upper(),
        'status_icon': '✅' if log.validation_status == 'success' else '❌',
        'completeness': f"{log.completeness_score * 100:.0f}%",
        'error_message': log.error_message,
        'has_duplicates': len(log.duplicates_found) > 0,
    }


__all__ = [
    'AuditAction',
    'ValidationLevel',
    'AuditLog',
    'ValidationResult',
    'DuplicateValidator',
    'CompletenessValidator',
    'AuditManager',
    'ComprehensiveValidator',
    'format_validation_result_for_ui',
    'format_audit_log_for_ui',
]
