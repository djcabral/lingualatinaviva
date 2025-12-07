#!/usr/bin/env python3
"""
HERRAMIENTA CLI DE CATALOGACIÓN - Lingua Latina Viva

Ejecuta el sistema de análisis integral y catalogación desde línea de comandos.
Permite procesar textos, generar reportes y gestionar vocabulario.

Uso:
    python catalog_tool.py process --input textos.json --source "Cicerón"
    python catalog_tool.py analyze --text "Salve, munde!"
    python catalog_tool.py vocabulary --stats
    python catalog_tool.py validate --text "Rosa"
"""

import argparse
import json
import sys
import logging
from pathlib import Path
from typing import Optional
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Imports locales
try:
    from utils.comprehensive_analyzer import ComprehensiveLatinAnalyzer, create_analysis_summary
    from utils.vocabulary_manager import VocabularyManager, InMemoryVocabularyRepository
    from utils.batch_processor import BatchTextProcessor, TextSource, BatchProcessingReport
except ImportError as e:
    logger.error(f"Error importando módulos: {e}")
    print("ERROR: Asegúrate de que estás ejecutando desde el directorio del proyecto")
    sys.exit(1)


# ============================================================================
# UTILIDADES
# ============================================================================

def create_analyzer() -> ComprehensiveLatinAnalyzer:
    """Crea instancia del analizador"""
    logger.info("Inicializando analizador integral...")
    analyzer = ComprehensiveLatinAnalyzer()
    logger.info("✅ Analizador listo")
    return analyzer


def create_vocabulary_manager() -> VocabularyManager:
    """Crea instancia del gestor de vocabulario"""
    repo = InMemoryVocabularyRepository()
    return VocabularyManager(repo)


def format_result(data: dict, json_output: bool = False) -> str:
    """Formatea resultado para output"""
    if json_output:
        return json.dumps(data, indent=2, ensure_ascii=False, default=str)
    else:
        # Formato legible
        return json.dumps(data, indent=2, ensure_ascii=False, default=str)


# ============================================================================
# COMANDOS
# ============================================================================

def cmd_analyze(args):
    """Analiza un texto individual"""
    if not args.text:
        print("ERROR: Debes proporcionar --text")
        sys.exit(1)
    
    analyzer = create_analyzer()
    
    logger.info(f"Analizando: {args.text}")
    
    result = analyzer.analyze_text(
        text=args.text,
        translation=args.translation,
        source=args.source,
        difficulty_level=args.difficulty
    )
    
    # Si es lista, tomar el primero
    if isinstance(result, list):
        result = result[0]
    
    # Crear resumen
    summary = create_analysis_summary(result)
    summary['full_analysis'] = {
        'word_analyses': [
            {
                'word': wa.word,
                'lemma': wa.morphology.lemma,
                'pos': wa.morphology.pos.value,
                'case': wa.morphology.case,
                'number': wa.morphology.number,
                'syntax': wa.syntax.function.value,
                'confidence': wa.overall_confidence,
            }
            for wa in result.word_analyses
        ],
        'issues': result.issues,
    }
    
    print(format_result(summary, args.json))


def cmd_process_batch(args):
    """Procesa un lote de textos"""
    if not args.input:
        print("ERROR: Debes proporcionar --input")
        sys.exit(1)
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: Archivo no encontrado: {args.input}")
        sys.exit(1)
    
    # Crear analizador
    analyzer = create_analyzer()
    vocab_manager = create_vocabulary_manager()
    processor = BatchTextProcessor(analyzer, vocab_manager)
    
    # Procesar
    logger.info(f"Procesando lote desde {args.input}")
    
    source = TextSource(
        name=args.source or "Desconocida",
        author=args.author,
        period=args.period,
        genre=args.genre,
    )
    
    # Detectar formato
    format = args.format
    if format == "auto":
        if args.input.endswith('.jsonl'):
            format = 'jsonl'
        elif args.input.endswith('.json'):
            format = 'json'
        elif args.input.endswith('.csv'):
            format = 'csv'
        else:
            format = 'json'
    
    # Procesar
    def progress_cb(current, total):
        print(f"\rProcesando... {current}/{total}", end='', flush=True)
    
    report = processor.process_from_file(
        input_path,
        source,
        format=format,
        progress_callback=progress_cb if not args.json else None
    )
    
    print()  # Nueva línea después del progreso
    
    # Output
    output_data = report.to_dict()
    output_data['recommendations'] = report.recommendations
    
    print(format_result(output_data, args.json))
    
    # Guardar reporte si se solicita
    if args.output:
        report.save_to_json(args.output)
        print(f"✅ Reporte guardado en {args.output}")


def cmd_vocabulary_stats(args):
    """Muestra estadísticas del vocabulario"""
    vocab = create_vocabulary_manager()
    
    # Por ahora sin datos, pero estructura lista
    stats = {
        'message': 'Gestor de vocabulario listo',
        'features': [
            'Almacenamiento y recuperación de lemas',
            'Enriquecimiento de definiciones',
            'Gestión de formas inflexionadas',
            'Análisis de frecuencia',
            'Validación de coherencia',
        ],
        'repository_type': 'in_memory',
    }
    
    print(format_result(stats, args.json))


def cmd_validate_text(args):
    """Valida un texto"""
    if not args.text:
        print("ERROR: Debes proporcionar --text")
        sys.exit(1)
    
    analyzer = create_analyzer()
    
    logger.info(f"Validando: {args.text}")
    
    result = analyzer.analyze_text(args.text, validate=True)
    
    if isinstance(result, list):
        result = result[0]
    
    validation = {
        'text': args.text,
        'valid': result.validation_status == 'validated',
        'status': result.validation_status,
        'issues': result.issues,
        'quality_score': result.quality_score,
    }
    
    print(format_result(validation, args.json))
    
    if result.validation_status == 'error':
        sys.exit(1)


def cmd_quality_report(args):
    """Genera reporte de calidad de análisis"""
    if not args.text:
        print("ERROR: Debes proporcionar --text")
        sys.exit(1)
    
    analyzer = create_analyzer()
    
    logger.info(f"Analizando calidad de: {args.text}")
    
    result = analyzer.analyze_text(args.text, validate=True)
    
    if isinstance(result, list):
        result = result[0]
    
    report = {
        'text': args.text,
        'overall_quality': result.quality_score,
        'words_analyzed': len(result.word_analyses),
        'word_confidence_scores': [
            {
                'word': wa.word,
                'confidence': wa.overall_confidence,
                'morphology_confidence': wa.morphology.confidence,
                'syntax_confidence': wa.syntax.confidence,
            }
            for wa in result.word_analyses
        ],
        'issues': result.issues,
        'status': result.validation_status,
    }
    
    print(format_result(report, args.json))


def cmd_morphology(args):
    """Analiza morfología de una palabra"""
    if not args.word:
        print("ERROR: Debes proporcionar --word")
        sys.exit(1)
    
    analyzer = create_analyzer()
    
    if not analyzer.morph_analyzer:
        print("ERROR: Analizador morfológico no disponible")
        sys.exit(1)
    
    logger.info(f"Analizando morfología de: {args.word}")
    
    result = analyzer._analyze_morphology(args.word)
    
    morphology_data = {
        'word': args.word,
        'lemma': result.lemma,
        'pos': result.pos.value,
        'case': result.case,
        'number': result.number,
        'gender': result.gender,
        'tense': result.tense,
        'mood': result.mood,
        'voice': result.voice,
        'declension': result.declension,
        'conjugation': result.conjugation,
        'confidence': result.confidence,
        'alternatives': result.alternatives,
    }
    
    print(format_result(morphology_data, args.json))


def cmd_syntax(args):
    """Analiza sintaxis de una oración"""
    if not args.text:
        print("ERROR: Debes proporcionar --text")
        sys.exit(1)
    
    analyzer = create_analyzer()
    
    if not analyzer.syntax_analyzer:
        print("ERROR: Analizador sintáctico no disponible")
        sys.exit(1)
    
    logger.info(f"Analizando sintaxis de: {args.text}")
    
    try:
        doc = analyzer.syntax_analyzer.nlp(args.text)
        
        syntax_data = {
            'text': args.text,
            'tokens': [
                {
                    'text': token.text,
                    'pos': token.pos_,
                    'dep': token.dep_,
                    'head': token.head.text if token.head else None,
                }
                for token in doc
            ],
        }
        
        print(format_result(syntax_data, args.json))
    
    except Exception as e:
        print(f"ERROR en análisis sintáctico: {e}")
        sys.exit(1)


# ============================================================================
# CONFIGURACIÓN DE ARGUMENTOS
# ============================================================================

def setup_parser() -> argparse.ArgumentParser:
    """Configura parser de argumentos"""
    parser = argparse.ArgumentParser(
        description='Herramienta de Catalogación - Lingua Latina Viva',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Ejemplos:
  %(prog)s analyze --text "Salve, munde!"
  %(prog)s process --input textos.json --source "Cicerón"
  %(prog)s vocabulary --stats
  %(prog)s morphology --word "rosa"
  %(prog)s syntax --text "Rosa est pulchra"
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Comando a ejecutar')
    
    # Comando: analyze
    p_analyze = subparsers.add_parser('analyze', help='Analiza un texto individual')
    p_analyze.add_argument('--text', required=False, help='Texto latino a analizar')
    p_analyze.add_argument('--translation', help='Traducción al español')
    p_analyze.add_argument('--source', help='Fuente del texto')
    p_analyze.add_argument('--difficulty', type=int, default=1, help='Nivel de dificultad 1-10')
    p_analyze.add_argument('--json', action='store_true', help='Output en JSON')
    p_analyze.set_defaults(func=cmd_analyze)
    
    # Comando: process
    p_process = subparsers.add_parser('process', help='Procesa lote de textos')
    p_process.add_argument('--input', required=False, help='Archivo de entrada')
    p_process.add_argument('--format', default='auto', choices=['auto', 'json', 'jsonl', 'csv'],
                          help='Formato del archivo')
    p_process.add_argument('--source', help='Fuente de los textos')
    p_process.add_argument('--author', help='Autor')
    p_process.add_argument('--period', help='Período (clásico, post-clásico, etc.)')
    p_process.add_argument('--genre', help='Género')
    p_process.add_argument('--output', help='Archivo de salida para reporte')
    p_process.add_argument('--json', action='store_true', help='Output en JSON')
    p_process.set_defaults(func=cmd_process_batch)
    
    # Comando: vocabulary
    p_vocab = subparsers.add_parser('vocabulary', help='Gestión de vocabulario')
    p_vocab.add_argument('--stats', action='store_true', help='Mostrar estadísticas')
    p_vocab.add_argument('--json', action='store_true', help='Output en JSON')
    p_vocab.set_defaults(func=cmd_vocabulary_stats)
    
    # Comando: validate
    p_validate = subparsers.add_parser('validate', help='Valida un texto')
    p_validate.add_argument('--text', required=False, help='Texto a validar')
    p_validate.add_argument('--json', action='store_true', help='Output en JSON')
    p_validate.set_defaults(func=cmd_validate_text)
    
    # Comando: quality
    p_quality = subparsers.add_parser('quality', help='Reporte de calidad')
    p_quality.add_argument('--text', required=False, help='Texto a analizar')
    p_quality.add_argument('--json', action='store_true', help='Output en JSON')
    p_quality.set_defaults(func=cmd_quality_report)
    
    # Comando: morphology
    p_morph = subparsers.add_parser('morphology', help='Análisis morfológico')
    p_morph.add_argument('--word', required=False, help='Palabra a analizar')
    p_morph.add_argument('--json', action='store_true', help='Output en JSON')
    p_morph.set_defaults(func=cmd_morphology)
    
    # Comando: syntax
    p_syntax = subparsers.add_parser('syntax', help='Análisis sintáctico')
    p_syntax.add_argument('--text', required=False, help='Oración a analizar')
    p_syntax.add_argument('--json', action='store_true', help='Output en JSON')
    p_syntax.set_defaults(func=cmd_syntax)
    
    return parser


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Función principal"""
    parser = setup_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\n\n❌ Operación cancelada por el usuario")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Error fatal: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
