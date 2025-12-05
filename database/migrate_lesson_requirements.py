"""
Script de migración para Stage 2: Arquitectura Lección-Céntrica

Este script:
1. Crea/actualiza las tablas LessonRequirement y UserLessonProgress
2. Seed requirements para lecciones 1-10 (Básico)
"""

import sys
import json
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.connection import create_db_and_tables, get_session
from database import LessonRequirement, UserLessonProgress
from sqlmodel import select
from datetime import datetime


def create_lesson_requirements():
    """Define los requisitos para lecciones 1-10"""
    
    requirements = [
        # LECCIÓN 1: Primeros Pasos
        {
            "lesson_number": 1,
            "requirement_type": "vocabulary_mastery",
            "required_vocab_mastery": 0.7,
            "criteria_json": json.dumps({"min_words": 10, "min_accuracy": 0.7}),
            "description": "Dominar 10 palabras básicas con 70% de precisión",
            "is_required": True,
            "weight": 1.0
        },
        {
            "lesson_number": 1,
            "requirement_type": "challenge_completion",
            "criteria_json": json.dumps({"challenge_ids": [1], "min_stars": 1}),
            "description": "Completar Desafío #1: Rosa (Nominativo y Acusativo)",
            "is_required": True,
            "weight": 1.0
        },
        
        # LECCIÓN 2: El Sujeto (Nominativo)
        {
            "lesson_number": 2,
            "requirement_type": "vocabulary_mastery",
            "required_vocab_mastery": 0.75,
            "criteria_json": json.dumps({"min_words": 15, "min_accuracy": 0.75}),
            "description": "Dominar 15 palabras con 75% de precisión",
            "is_required": True,
            "weight": 1.0
        },
        {
            "lesson_number": 2,
            "requirement_type": "challenge_completion",
            "criteria_json": json.dumps({"challenge_ids": [1, 2], "min_stars": 1}),
            "description": "Completar Desafíos #1-2",
            "is_required": True,
            "weight": 1.0
        },
        
        # LECCIÓN 3: Primera Declinación
        {
            "lesson_number": 3,
            "requirement_type": "vocabulary_mastery",
            "required_vocab_mastery": 0.8,
            "criteria_json": json.dumps({"min_words": 20, "min_accuracy": 0.8}),
            "description": "Dominar 20 palabras de 1ª declinación con 80% de precisión",
            "is_required": True,
            "weight": 1.5
        },
        {
            "lesson_number": 3,
            "requirement_type": "challenge_completion",
            "criteria_json": json.dumps({"challenge_ids": [3, 4, 5], "min_stars": 2}),
            "description": "Completar Desafíos #3-5 (Rosa completa + Puella) con al menos 2 estrellas",
            "is_required": True,
            "weight": 1.5
        },
        {
            "lesson_number": 3,
            "requirement_type": "analysis_practice",
            "required_analyses": 3,
            "criteria_json": json.dumps({"min_analyses": 3, "min_accuracy": 0.7}),
            "description": "Analizar correctamente 3 oraciones",
            "is_required": False,  # Opcional - para badge
            "weight": 0.5
        },
        
        # LECCIÓN 4: Segunda Declinación
        {
            "lesson_number": 4,
            "requirement_type": "vocabulary_mastery",
            "required_vocab_mastery": 0.8,
            "criteria_json": json.dumps({"min_words": 25, "min_accuracy": 0.8}),
            "description": "Dominar 25 palabras (1ª + 2ª) con 80% de precisión",
            "is_required": True,
            "weight": 1.5
        },
        {
            "lesson_number": 4,
            "requirement_type": "challenge_completion",
            "criteria_json": json.dumps({"challenge_ids": [6, 7, 8], "min_stars": 2}),
            "description": "Completar Desafíos #6-8",
            "is_required": True,
            "weight": 1.5
        },
        
        # LECCIÓN 5: El Neutro
        {
            "lesson_number": 5,
            "requirement_type": "vocabulary_mastery",
            "required_vocab_mastery": 0.75,
            "criteria_json": json.dumps({"min_words": 10, "min_accuracy": 0.75}),
            "description": "Dominar 10 sustantivos neutros con 75% de precisión",
            "is_required": True,
            "weight": 1.0
        },
        {
            "lesson_number": 5,
            "requirement_type": "challenge_completion",
            "criteria_json": json.dumps({"challenge_ids": [9], "min_stars": 2}),
            "description": "Completar desafío temático de neutro",
            "is_required": True,
            "weight": 1.0
        },
        
        # LECCIÓN 6: Consolidación y Adjetivos
        {
            "lesson_number": 6,
            "requirement_type": "vocabulary_mastery",
            "required_vocab_mastery": 0.85,
            "criteria_json": json.dumps({"min_words": 30, "min_accuracy": 0.85}),
            "description": "Dominar 30 palabras totales con 85% de precisión",
            "is_required": True,
            "weight": 2.0
        },
        {
            "lesson_number": 6,
            "requirement_type": "challenge_completion",
            "criteria_json": json.dumps({"challenge_ids": [10], "min_stars": 2}),
            "description": "Completar quiz de consolidación",
            "is_required": True,
            "weight": 1.5
        },
        
        # LECCIÓN 7: Tercera Declinación y Dativo
        {
            "lesson_number": 7,
            "requirement_type": "vocabulary_mastery",
            "required_vocab_mastery": 0.75,
            "criteria_json": json.dumps({"min_words": 20, "min_accuracy": 0.75}),
            "description": "Dominar 20 palabras de 3ª declinación con 75% de precisión",
            "is_required": True,
            "weight": 1.5
        },
        {
            "lesson_number": 7,
            "requirement_type": "challenge_completion",
            "criteria_json": json.dumps({"challenge_ids": [11, 12, 13], "min_stars": 2}),
            "description": "Completar Desafíos #11-13",
            "is_required": True,
            "weight": 1.5
        },
        
        # LECCIÓN 8: Cuarta Declinación y Pasado
        {
            "lesson_number": 8,
            "requirement_type": "vocabulary_mastery",
            "required_vocab_mastery": 0.8,
            "criteria_json": json.dumps({"min_words": 15, "min_accuracy": 0.8}),
            "description": "Dominar 15 palabras + verbos en pasado con 80% de precisión",
            "is_required": True,
            "weight": 1.5
        },
        {
            "lesson_number": 8,
            "requirement_type": "challenge_completion",
            "criteria_json": json.dumps({"challenge_ids": [11, 12, 13], "min_stars": 2}),
            "description": "Completar Desafíos #12-14 (SUM + AMO + MONEO)",
            "is_required": True,
            "weight": 1.5
        },
        
        # LECCIÓN 9: Quinta Declinación y Futuro
        {
            "lesson_number": 9,
            "requirement_type": "vocabulary_mastery",
            "required_vocab_mastery": 0.75,
            "criteria_json": json.dumps({"min_words": 10, "min_accuracy": 0.75}),
            "description": "Dominar 10 palabras de 5ª + verbos futuro con 75% de precisión",
            "is_required": True,
            "weight": 1.0
        },
        {
            "lesson_number": 9,
            "requirement_type": "challenge_completion",
            "criteria_json": json.dumps({"challenge_ids": [15], "min_stars": 2}),
            "description": "Completar Desafío #15",
            "is_required": True,
            "weight": 1.0
        },
        
        # LECCIÓN 10: Adjetivos de 2ª Clase
        {
            "lesson_number": 10,
            "requirement_type": "vocabulary_mastery",
            "required_vocab_mastery": 0.8,
            "criteria_json": json.dumps({"min_words": 15, "min_accuracy": 0.8}),
            "description": "Dominar 15 adjetivos con 80% de precisión",
            "is_required": True,
            "weight": 1.5
        },
        {
            "lesson_number": 10,
            "requirement_type": "challenge_completion",
            "criteria_json": json.dumps({"challenge_ids": [16, 17], "min_stars": 2}),
            "description": "Completar Desafíos #16-17",
            "is_required": True,
            "weight": 1.5
        },
    ]
    
    return requirements


def migrate():
    """Ejecuta la migración completa"""
    print("=" * 60)
    print("MIGRACIÓN: Stage 2 - Arquitectura Lección-Céntrica")
    print("=" * 60)
    
    # 1. Crear tablas
    print("\n📦 Creando/actualizando tablas...")
    create_db_and_tables()
    print("✅ Tablas actualizadas")
    
    # 2. Seed requirements
    with get_session() as session:
        print("\n🎯 Seeding lesson requirements...")
        
        # Check if requirements already exist
        existing = session.exec(select(LessonRequirement)).first()
        
        if existing:
            print("⚠️ Los requisitos ya existen. Saltando seed.")
            print("   (Si quieres recrearlos, elimina la tabla lesson_requirement primero)")
        else:
            requirements_data = create_lesson_requirements()
            
            for req_data in requirements_data:
                requirement = LessonRequirement(**req_data)
                session.add(requirement)
            
            session.commit()
            print(f"✅ Creados {len(requirements_data)} requisitos para lecciones 1-10")
            
            # Mostrar resumen
            print("\n📊 Resumen de requisitos:")
            for lesson_num in range(1, 11):
                count = session.exec(
                    select(LessonRequirement)
                    .where(LessonRequirement.lesson_number == lesson_num)
                ).all()
                required_count = sum(1 for r in count if r.is_required)
                optional_count = len(count) - required_count
                print(f"   Lección {lesson_num}: {required_count} requeridos, {optional_count} opcionales")
    
    print("\n" + "=" * 60)
    print("✅ MIGRACIÓN COMPLETADA")
    print("=" * 60)
    print("\n💡 Próximo paso: Los usuarios ahora tendrán progreso detallado por lección")
    print("   El sistema rastreará:")
    print("   - Vocabulario dominado")
    print("   - Desafíos completados")
    print("   - Análisis de oraciones")
    print("\n🎯 Umbral de completitud: 70% de requisitos requeridos")


if __name__ == "__main__":
    migrate()
