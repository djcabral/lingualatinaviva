"""
HERRAMIENTA DE PROCESAMIENTO BATCH - Lingua Latina Viva

Sistema para procesar textos en lotes:
- Análisis de múltiples textos de forma eficiente
- Control de calidad y validación
- Almacenamiento organizado en BD
- Generación de reportes de procesamiento

Diseñado para ejecutar como tarea independiente (CLI, scheduler, etc.)
"""

from typing import List, Dict, Optional, Any, Callable, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import logging
from datetime import datetime
import json
from pathlib import Path
import hashlib

from .comprehensive_analyzer import (
    ComprehensiveLatinAnalyzer,
    ComprehensiveSentenceAnalysis,
    prepare_for_database
)
from .vocabulary_manager import VocabularyManager

logger = logging.getLogger(__name__)


# ============================================================================
# ENUMERACIONES Y TIPOS
# ============================================================================

class ProcessingStatus(Enum):
    """Estado del procesamiento"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    REQUIRES_REVIEW = "requires_review"


@dataclass
class TextSource:
    """Información sobre la fuente de un texto"""
    name: str
    path: Optional[str] = None
    author: Optional[str] = None
    period: Optional[str] = None  # clásico, post-clásico, medieval, etc.
    genre: Optional[str] = None   # epigrama, elegía, ensayo, etc.
    notes: Optional[str] = None


@dataclass
class ProcessingResult:
    """Resultado del procesamiento de un texto"""
    text_id: str
    original_text: str
    source: TextSource
    
    # Análisis
    analysis: Optional[ComprehensiveSentenceAnalysis] = None
    
    # Estado
    status: ProcessingStatus = ProcessingStatus.PENDING
    quality_score: float = 0.0
    
    # Timestamps
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    
    # Metadatos
    processing_notes: Optional[str] = None
    issues: List[str] = field(default_factory=list)
    requires_manual_review: bool = False
    
    # Para BD
    db_id: Optional[int] = None
    
    def duration_seconds(self) -> Optional[float]:
        """Duración del procesamiento en segundos"""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None


@dataclass
class BatchProcessingReport:
    """Reporte de procesamiento en batch"""
    batch_id: str
    timestamp: datetime = field(default_factory=datetime.now)
    
    # Estadísticas
    total_texts: int = 0
    successfully_processed: int = 0
    failed: int = 0
    requires_review: int = 0
    
    # Métricas
    average_quality_score: float = 0.0
    total_processing_time: float = 0.0
    
    # Resultados
    results: List[ProcessingResult] = field(default_factory=list)
    
    # Recomendaciones
    recommendations: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario para serialización"""
        return {
            'batch_id': self.batch_id,
            'timestamp': self.timestamp.isoformat(),
            'statistics': {
                'total': self.total_texts,
                'success': self.successfully_processed,
                'failed': self.failed,
                'review': self.requires_review,
            },
            'metrics': {
                'avg_quality': self.average_quality_score,
                'total_time': self.total_processing_time,
            },
            'summary': {
                'success_rate': (
                    (self.successfully_processed / self.total_texts * 100)
                    if self.total_texts > 0 else 0
                ),
                'review_rate': (
                    (self.requires_review / self.total_texts * 100)
                    if self.total_texts > 0 else 0
                ),
            },
        }
    
    def save_to_json(self, filepath: str) -> bool:
        """Guarda reporte a archivo JSON"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, indent=2, ensure_ascii=False, default=str)
            logger.info(f"Reporte guardado en {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error guardando reporte: {e}")
            return False


# ============================================================================
# PROCESADOR BATCH
# ============================================================================

class BatchTextProcessor:
    """
    Procesador de textos en lotes.
    
    Características:
    - Procesamiento eficiente de múltiples textos
    - Control de calidad integrado
    - Callbacks para monitoreo
    - Generación de reportes detallados
    """
    
    def __init__(
        self,
        analyzer: ComprehensiveLatinAnalyzer,
        vocabulary_manager: Optional[VocabularyManager] = None,
        quality_threshold: float = 0.6
    ):
        """
        Inicializa el procesador
        
        Args:
            analyzer: Instancia del analizador integral
            vocabulary_manager: Gestor de vocabulario (opcional)
            quality_threshold: Score mínimo de calidad (0-1)
        """
        self.analyzer = analyzer
        self.vocab_manager = vocabulary_manager
        self.quality_threshold = quality_threshold
        
        self._processing_history: List[ProcessingResult] = []
    
    # ========================================================================
    # PROCESAMIENTO
    # ========================================================================
    
    def process_text(
        self,
        text: str,
        source: TextSource,
        text_id: Optional[str] = None,
        translation: Optional[str] = None,
        lesson_number: Optional[int] = None,
        difficulty_level: int = 1,
        callback: Optional[Callable[[ProcessingResult], None]] = None
    ) -> ProcessingResult:
        """
        Procesa un texto individual
        """
        if not text_id:
            text_id = self._generate_text_id(text)
        
        result = ProcessingResult(
            text_id=text_id,
            original_text=text,
            source=source
        )
        
        try:
            logger.info(f"Procesando: {text_id}")
            result.status = ProcessingStatus.IN_PROGRESS
            
            # Ejecutar análisis integral
            analysis = self.analyzer.analyze_text(
                text=text,
                translation=translation,
                source=source.name,
                lesson_number=lesson_number,
                difficulty_level=difficulty_level,
                validate=True
            )
            
            # Si es lista (múltiples oraciones), tomar la primera
            if isinstance(analysis, list):
                analysis = analysis[0]
            
            result.analysis = analysis
            result.quality_score = analysis.quality_score
            
            # Validar calidad
            if result.quality_score < self.quality_threshold:
                result.status = ProcessingStatus.REQUIRES_REVIEW
                result.requires_manual_review = True
                result.processing_notes = (
                    f"Score de calidad bajo ({result.quality_score:.2f}). "
                    f"Requiere revisión manual."
                )
            else:
                result.status = ProcessingStatus.COMPLETED
            
            result.issues = analysis.issues
            
            # Actualizar vocabulario si está disponible
            if self.vocab_manager and result.status == ProcessingStatus.COMPLETED:
                self._update_vocabulary(analysis)
        
        except Exception as e:
            logger.error(f"Error procesando {text_id}: {e}")
            result.status = ProcessingStatus.FAILED
            result.processing_notes = f"Error: {str(e)}"
            result.requires_manual_review = True
        
        finally:
            result.end_time = datetime.now()
            self._processing_history.append(result)
            
            if callback:
                callback(result)
        
        return result
    
    def process_batch(
        self,
        texts: List[Dict[str, Any]],
        source: TextSource,
        batch_id: Optional[str] = None,
        progress_callback: Optional[Callable[[int, int], None]] = None,
        result_callback: Optional[Callable[[ProcessingResult], None]] = None
    ) -> BatchProcessingReport:
        """
        Procesa un lote de textos
        
        Args:
            texts: Lista de diccionarios con 'text', 'translation' (opcional), etc.
            source: Fuente común para todos los textos
            batch_id: ID del lote (generado automáticamente si no se proporciona)
            progress_callback: Función llamada con (current, total)
            result_callback: Función llamada para cada resultado
            
        Returns:
            BatchProcessingReport con resultados detallados
        """
        if not batch_id:
            batch_id = self._generate_batch_id()
        
        report = BatchProcessingReport(batch_id=batch_id)
        report.total_texts = len(texts)
        
        logger.info(f"Iniciando procesamiento de lote {batch_id} ({len(texts)} textos)")
        
        quality_scores = []
        
        for idx, text_data in enumerate(texts):
            # Preparar parámetros
            text = text_data.get('text', '')
            text_id = text_data.get('id')
            translation = text_data.get('translation')
            lesson_number = text_data.get('lesson_number')
            difficulty_level = text_data.get('difficulty_level', 1)
            
            # Procesar
            result = self.process_text(
                text=text,
                source=source,
                text_id=text_id,
                translation=translation,
                lesson_number=lesson_number,
                difficulty_level=difficulty_level,
                callback=result_callback
            )
            
            report.results.append(result)
            
            # Actualizar estadísticas
            if result.status == ProcessingStatus.COMPLETED:
                report.successfully_processed += 1
                quality_scores.append(result.quality_score)
            elif result.status == ProcessingStatus.FAILED:
                report.failed += 1
            elif result.status == ProcessingStatus.REQUIRES_REVIEW:
                report.requires_review += 1
            
            # Callback de progreso
            if progress_callback:
                progress_callback(idx + 1, len(texts))
        
        # Calcular métricas finales
        if quality_scores:
            report.average_quality_score = sum(quality_scores) / len(quality_scores)
        
        report.total_processing_time = sum(
            (r.duration_seconds() or 0) for r in report.results
        )
        
        # Generar recomendaciones
        report.recommendations = self._generate_recommendations(report)
        
        logger.info(
            f"Lote {batch_id} completado: "
            f"{report.successfully_processed}/{report.total_texts} exitosos, "
            f"{report.requires_review} para revisión"
        )
        
        return report
    
    def process_from_file(
        self,
        filepath: str,
        source: TextSource,
        format: str = "jsonl",  # jsonl, csv, json
        **kwargs
    ) -> BatchProcessingReport:
        """
        Procesa textos desde archivo
        
        Args:
            filepath: Ruta del archivo
            source: Información de fuente
            format: Formato del archivo (jsonl, csv, json)
            **kwargs: Argumentos adicionales para process_batch
            
        Returns:
            BatchProcessingReport
        """
        texts = []
        
        try:
            if format == "jsonl":
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            texts.append(json.loads(line))
            
            elif format == "json":
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    texts = data if isinstance(data, list) else [data]
            
            elif format == "csv":
                import csv
                with open(filepath, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    texts = list(reader)
            
            else:
                raise ValueError(f"Formato no soportado: {format}")
            
            logger.info(f"Cargados {len(texts)} textos desde {filepath}")
            
            return self.process_batch(texts, source, **kwargs)
        
        except Exception as e:
            logger.error(f"Error procesando archivo {filepath}: {e}")
            raise
    
    # ========================================================================
    # ANÁLISIS Y REPORTES
    # ========================================================================
    
    def get_processing_history(self) -> List[ProcessingResult]:
        """Obtiene historial de procesamiento"""
        return self._processing_history
    
    def generate_summary_report(self) -> Dict[str, Any]:
        """Genera resumen del procesamiento"""
        if not self._processing_history:
            return {"message": "Sin procesamiento registrado"}
        
        successful = [r for r in self._processing_history if r.status == ProcessingStatus.COMPLETED]
        failed = [r for r in self._processing_history if r.status == ProcessingStatus.FAILED]
        review_needed = [r for r in self._processing_history if r.requires_manual_review]
        
        quality_scores = [r.quality_score for r in successful]
        
        return {
            'total_processed': len(self._processing_history),
            'successful': len(successful),
            'failed': len(failed),
            'review_needed': len(review_needed),
            'average_quality': sum(quality_scores) / len(quality_scores) if quality_scores else 0,
            'success_rate': (len(successful) / len(self._processing_history) * 100) if self._processing_history else 0,
        }
    
    def identify_problematic_texts(
        self,
        quality_threshold: Optional[float] = None
    ) -> List[ProcessingResult]:
        """
        Identifica textos con problemas (baja calidad, errores, etc.)
        """
        threshold = quality_threshold or self.quality_threshold
        
        problems = []
        for result in self._processing_history:
            if (result.status == ProcessingStatus.FAILED or
                result.requires_manual_review or
                result.quality_score < threshold):
                problems.append(result)
        
        return sorted(problems, key=lambda r: r.quality_score)
    
    # ========================================================================
    # UTILIDADES PRIVADAS
    # ========================================================================
    
    def _update_vocabulary(self, analysis: ComprehensiveSentenceAnalysis) -> None:
        """Actualiza el vocabulario con palabras encontradas"""
        if not self.vocab_manager:
            return
        
        for word_analysis in analysis.word_analyses:
            try:
                lemma = word_analysis.morphology.lemma
                
                # Obtener o crear palabra
                existing = self.vocab_manager.get_word(lemma)
                if not existing:
                    self.vocab_manager.add_or_update_word(
                        lemma=lemma,
                        definitions=[],
                        pos=word_analysis.morphology.pos.value if word_analysis.morphology.pos else "unknown"
                    )
                
                # Actualizar frecuencia
                self.vocab_manager.update_word_frequency(lemma, 1)
            
            except Exception as e:
                logger.warning(f"Error actualizando vocabulario para {lemma}: {e}")
    
    def _generate_recommendations(self, report: BatchProcessingReport) -> List[str]:
        """Genera recomendaciones basadas en resultados"""
        recommendations = []
        
        success_rate = (report.successfully_processed / report.total_texts * 100) if report.total_texts > 0 else 0
        
        if success_rate < 50:
            recommendations.append("⚠️ Tasa de éxito muy baja. Revisar textos de entrada y configuración del analizador.")
        
        if report.average_quality_score < 0.6:
            recommendations.append("⚠️ Calidad promedio baja. Considerar mejorar definiciones y análisis sintáctico.")
        
        if report.requires_review > report.successfully_processed:
            recommendations.append("⚠️ Muchos textos requieren revisión manual. Verificar umbral de calidad.")
        
        if report.failed > 0:
            recommendations.append(f"❌ {report.failed} textos fallaron. Revisar logs de errores.")
        
        if success_rate > 80 and report.average_quality_score > 0.8:
            recommendations.append("✅ Procesamiento de excelente calidad. Proceder con confianza.")
        
        return recommendations
    
    def _generate_text_id(self, text: str) -> str:
        """Genera ID único para un texto"""
        # Usar hash del texto + timestamp
        text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"text_{timestamp}_{text_hash}"
    
    def _generate_batch_id(self) -> str:
        """Genera ID único para un lote"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"batch_{timestamp}"


# ============================================================================
# HERRAMIENTAS DE INTEGRACIÓN CON BD
# ============================================================================

class DatabaseSyncManager:
    """
    Sincroniza resultados de procesamiento con la base de datos
    """
    
    def __init__(self, db_connection):
        """
        Args:
            db_connection: Conexión a la base de datos
        """
        self.db = db_connection
    
    def save_analysis_to_db(
        self,
        result: ProcessingResult
    ) -> bool:
        """
        Guarda un análisis en la BD
        """
        if not result.analysis:
            logger.warning(f"Sin análisis para guardar: {result.text_id}")
            return False
        
        try:
            db_data = prepare_for_database(result.analysis)
            
            # Guardar oración
            sentence_id = self._save_sentence(db_data['sentence'])
            
            # Guardar palabras
            for word_data in db_data['words']:
                word_data['sentence_id'] = sentence_id
                self._save_word(word_data)
            
            result.db_id = sentence_id
            logger.info(f"Análisis guardado en BD: {result.text_id} (ID: {sentence_id})")
            return True
        
        except Exception as e:
            logger.error(f"Error guardando en BD: {e}")
            return False
    
    def save_batch_to_db(self, report: BatchProcessingReport) -> int:
        """
        Guarda todos los resultados de un lote en la BD
        
        Returns:
            Número de análisis guardados exitosamente
        """
        saved_count = 0
        
        for result in report.results:
            if result.status == ProcessingStatus.COMPLETED:
                if self.save_analysis_to_db(result):
                    saved_count += 1
        
        logger.info(f"Guardados {saved_count}/{len(report.results)} análisis en BD")
        return saved_count
    
    # Métodos placeholder - implementar según modelo de BD
    def _save_sentence(self, sentence_data: Dict[str, Any]) -> int:
        """Guarda una oración en BD, retorna ID"""
        # TODO: Implementar según modelo de BD
        pass
    
    def _save_word(self, word_data: Dict[str, Any]) -> int:
        """Guarda análisis de palabra en BD, retorna ID"""
        # TODO: Implementar según modelo de BD
        pass
