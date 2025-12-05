#!/usr/bin/env python3
"""
Auditor de Contenido
Este script verifica la cobertura de contenido en la base de datos para cada lección.
Genera un reporte detallado de qué recursos existen y cuáles faltan.
"""

import sys
from pathlib import Path
from sqlmodel import Session, select, func
from typing import Dict, List, Any

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database import get_session, Word, Lesson, LessonVocabulary, SentenceAnalysis
from utils.exercise_generator import ExerciseGenerator

def audit_lesson(session: Session, lesson_number: int) -> Dict[str, Any]:
    """Audita el contenido disponible para una lección específica."""
    
    audit_data = {
        "lesson_number": lesson_number,
        "has_lesson_entry": False,
        "lesson_title": None,
        "vocabulary_count": 0,
        "vocabulary_nouns": 0,
        "vocabulary_verbs": 0,
        "vocabulary_adjectives": 0,
        "sentence_count": 0,
        "reading_texts": 0,
        "exercise_capabilities": {
            "vocabulary_match": False,
            "declension_choice": False,
            "conjugation_choice": False,
            "sentence_completion": False
        }
    }
    
    # Verificar entrada en tabla Lesson
    lesson_entry = session.exec(
        select(Lesson).where(Lesson.lesson_number == lesson_number)
    ).first()
    
    if lesson_entry:
        audit_data["has_lesson_entry"] = True
        audit_data["lesson_title"] = lesson_entry.title
    
    # Contar vocabulario total
    vocab_count = session.exec(
        select(func.count(LessonVocabulary.id))
        .where(LessonVocabulary.lesson_number == lesson_number)
    ).first()
    audit_data["vocabulary_count"] = vocab_count or 0
    
    # Contar por tipo de palabra
    if vocab_count and vocab_count > 0:
        # Sustantivos
        noun_count = session.exec(
            select(func.count(Word.id))
            .join(LessonVocabulary, Word.id == LessonVocabulary.word_id)
            .where(LessonVocabulary.lesson_number == lesson_number)
            .where(Word.part_of_speech == 'noun')
        ).first()
        audit_data["vocabulary_nouns"] = noun_count or 0
        
        # Verbos
        verb_count = session.exec(
            select(func.count(Word.id))
            .join(LessonVocabulary, Word.id == LessonVocabulary.word_id)
            .where(LessonVocabulary.lesson_number == lesson_number)
            .where(Word.part_of_speech == 'verb')
        ).first()
        audit_data["vocabulary_verbs"] = verb_count or 0
        
        # Adjetivos
        adj_count = session.exec(
            select(func.count(Word.id))
            .join(LessonVocabulary, Word.id == LessonVocabulary.word_id)
            .where(LessonVocabulary.lesson_number == lesson_number)
            .where(Word.part_of_speech == 'adjective')
        ).first()
        audit_data["vocabulary_adjectives"] = adj_count or 0
    
    # Contar frases analizadas
    sentence_count = session.exec(
        select(func.count(SentenceAnalysis.id))
        .where(SentenceAnalysis.lesson_number == lesson_number)
    ).first()
    audit_data["sentence_count"] = sentence_count or 0
    
    # Contar textos de lectura (modelo no existe aún)
    audit_data["reading_texts"] = 0
    
    # Verificar capacidades del generador de ejercicios
    generator = ExerciseGenerator(session)
    
    # Vocabulary match (requiere al menos 5 palabras)
    if audit_data["vocabulary_count"] >= 5:
        audit_data["exercise_capabilities"]["vocabulary_match"] = True
    
    # Declension choice (requiere sustantivos)
    if audit_data["vocabulary_nouns"] >= 3:
        audit_data["exercise_capabilities"]["declension_choice"] = True
    
    # Conjugation choice (requiere verbos)
    if audit_data["vocabulary_verbs"] >= 3:
        audit_data["exercise_capabilities"]["conjugation_choice"] = True
    
    # Sentence completion (requiere frases)
    if audit_data["sentence_count"] >= 3:
        audit_data["exercise_capabilities"]["sentence_completion"] = True
    
    return audit_data

def generate_markdown_report(audit_results: List[Dict[str, Any]]) -> str:
    """Genera un reporte en formato Markdown."""
    
    report = "# Auditoría de Contenido del Curso\n\n"
    report += f"**Fecha**: {Path(__file__).stat().st_mtime}\n\n"
    report += "## Resumen General\n\n"
    
    # Estadísticas generales
    total_lessons = len(audit_results)
    lessons_with_vocab = sum(1 for r in audit_results if r["vocabulary_count"] > 0)
    lessons_with_sentences = sum(1 for r in audit_results if r["sentence_count"] > 0)
    lessons_with_readings = sum(1 for r in audit_results if r["reading_texts"] > 0)
    
    report += f"- **Total de lecciones auditadas**: {total_lessons}\n"
    report += f"- **Lecciones con vocabulario**: {lessons_with_vocab} ({lessons_with_vocab/total_lessons*100:.1f}%)\n"
    report += f"- **Lecciones con frases analizadas**: {lessons_with_sentences} ({lessons_with_sentences/total_lessons*100:.1f}%)\n"
    report += f"- **Lecciones con textos de lectura**: {lessons_with_readings} ({lessons_with_readings/total_lessons*100:.1f}%)\n\n"
    
    report += "## Detalle por Lección\n\n"
    report += "| L# | Título | Vocab | Sust | Verb | Adj | Frases | Textos | Ejerc. Disp. |\n"
    report += "|:---|:-------|------:|-----:|-----:|----:|-------:|-------:|:-------------|\n"
    
    for result in audit_results:
        ln = result["lesson_number"]
        title = result["lesson_title"] or "❌ Sin entrada"
        vocab = result["vocabulary_count"]
        nouns = result["vocabulary_nouns"]
        verbs = result["vocabulary_verbs"]
        adjs = result["vocabulary_adjectives"]
        sentences = result["sentence_count"]
        readings = result["reading_texts"]
        
        # Ejercicios disponibles
        ex_caps = result["exercise_capabilities"]
        ex_available = sum(ex_caps.values())
        ex_str = f"{ex_available}/4"
        
        # Emojis de estado
        vocab_emoji = "✅" if vocab >= 15 else ("⚠️" if vocab > 0 else "❌")
        sentence_emoji = "✅" if sentences >= 10 else ("⚠️" if sentences > 0 else "❌")
        
        report += f"| **{ln}** | {title[:30]} | {vocab_emoji} {vocab} | {nouns} | {verbs} | {adjs} | {sentence_emoji} {sentences} | {readings} | {ex_str} |\n"
    
    report += "\n## Leyenda\n\n"
    report += "- **Vocab**: ✅ ≥15 palabras | ⚠️ 1-14 palabras | ❌ Sin vocabulario\n"
    report += "- **Frases**: ✅ ≥10 frases | ⚠️ 1-9 frases | ❌ Sin frases\n"
    report += "- **Ejerc. Disp.**: Número de tipos de ejercicios generables (máx. 4)\n\n"
    
    report += "## Prioridades de Acción\n\n"
    
    # Lecciones vacías (sin vocabulario)
    empty_lessons = [r["lesson_number"] for r in audit_results if r["vocabulary_count"] == 0]
    if empty_lessons:
        report += f"### 🔴 CRÍTICO: Lecciones sin vocabulario ({len(empty_lessons)})\n"
        report += f"Lecciones: {', '.join(f'L{ln}' for ln in empty_lessons)}\n\n"
    
    # Lecciones con poco vocabulario
    low_vocab = [r["lesson_number"] for r in audit_results if 0 < r["vocabulary_count"] < 15]
    if low_vocab:
        report += f"### 🟡 ALTA: Lecciones con vocabulario insuficiente (<15 palabras) ({len(low_vocab)})\n"
        report += f"Lecciones: {', '.join(f'L{ln}' for ln in low_vocab)}\n\n"
    
    # Lecciones sin frases
    no_sentences = [r["lesson_number"] for r in audit_results if r["sentence_count"] == 0]
    if no_sentences:
        report += f"### 🟠 MEDIA: Lecciones sin frases analizadas ({len(no_sentences)})\n"
        report += f"Lecciones: {', '.join(f'L{ln}' for ln in no_sentences)}\n\n"
    
    return report

def main():
    """Función principal."""
    print("🔍 Iniciando auditoría de contenido...")
    
    with get_session() as session:
        audit_results = []
        
        # Auditar lecciones 1-30
        for lesson_num in range(1, 31):
            print(f"  Auditando Lección {lesson_num}...", end=" ")
            result = audit_lesson(session, lesson_num)
            audit_results.append(result)
            
            # Feedback visual
            status = "✅" if result["vocabulary_count"] >= 15 else ("⚠️" if result["vocabulary_count"] > 0 else "❌")
            print(f"{status} Vocab: {result['vocabulary_count']}, Frases: {result['sentence_count']}")
        
        # Generar reporte
        print("\n📝 Generando reporte...")
        report = generate_markdown_report(audit_results)
        
        # Guardar reporte
        output_path = Path(__file__).parent.parent.parent / "AUDITORIA_CONTENIDO.md"
        output_path.write_text(report, encoding="utf-8")
        
        print(f"\n✅ Auditoría completada. Reporte guardado en: {output_path}")
        print(f"\n📊 Resumen rápido:")
        print(f"   - Lecciones con vocabulario completo (≥15): {sum(1 for r in audit_results if r['vocabulary_count'] >= 15)}/30")
        print(f"   - Lecciones con frases completas (≥10): {sum(1 for r in audit_results if r['sentence_count'] >= 10)}/30")
        print(f"   - Lecciones completamente vacías: {sum(1 for r in audit_results if r['vocabulary_count'] == 0)}/30")

if __name__ == "__main__":
    main()
