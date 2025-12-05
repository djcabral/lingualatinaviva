#!/usr/bin/env python3
"""
Script de Población - Etapa 2: Requisitos de Lecciones
Crea los requisitos por defecto para las lecciones 1-10.
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.connection import get_session
from database import LessonRequirement
from sqlmodel import select

def seed_lesson_requirements():
    print("🌱 Poblando requisitos de lecciones 1-10...")
    
    # Definición de requisitos por lección
    # Progresión gradual: las primeras lecciones son más fáciles
    requirements_config = [
        # Lecciones Básicas (1-5): Enfoque en vocabulario
        {"lesson": 1, "vocab": 0.7, "translations": 3, "analyses": 0, "readings": 0},
        {"lesson": 2, "vocab": 0.75, "translations": 4, "analyses": 0, "readings": 0},
        {"lesson": 3, "vocab": 0.75, "translations": 4, "analyses": 0, "readings": 0},
        {"lesson": 4, "vocab": 0.8, "translations": 5, "analyses": 0, "readings": 0},
        {"lesson": 5, "vocab": 0.8, "translations": 5, "analyses": 0, "readings": 0},
        
        # Lecciones Intermedias (6-10): Añadir análisis sintáctico
        {"lesson": 6, "vocab": 0.8, "translations": 5, "analyses": 2, "readings": 0},
        {"lesson": 7, "vocab": 0.8, "translations": 5, "analyses": 2, "readings": 0},
        {"lesson": 8, "vocab": 0.8, "translations": 6, "analyses": 3, "readings": 0},
        {"lesson": 9, "vocab": 0.8, "translations": 6, "analyses": 3, "readings": 0},
        {"lesson": 10, "vocab": 0.85, "translations": 7, "analyses": 3, "readings": 0},
    ]
    
    with get_session() as session:
        added = 0
        updated = 0
        
        for config in requirements_config:
            # Check if requirement already exists
            existing = session.exec(
                select(LessonRequirement).where(
                    LessonRequirement.lesson_number == config["lesson"]
                )
            ).first()
            
            if existing:
                # Update existing
                existing.required_vocab_mastery = config["vocab"]
                existing.required_translations = config["translations"]
                existing.required_analyses = config["analyses"]
                existing.required_readings = config["readings"]
                session.add(existing)
                updated += 1
            else:
                # Create new
                req = LessonRequirement(
                    lesson_number=config["lesson"],
                    required_vocab_mastery=config["vocab"],
                    required_translations=config["translations"],
                    required_analyses=config["analyses"],
                    required_readings=config["readings"],
                    is_hard_requirement=True
                )
                session.add(req)
                added += 1
        
        session.commit()
        
        print(f"✅ Requisitos creados: {added}")
        print(f"✅ Requisitos actualizados: {updated}")
        
        # Show summary
        print("\n📊 Resumen de Requisitos:")
        print("Lección | Vocab | Traducciones | Análisis")
        print("--------|-------|--------------|----------")
        for config in requirements_config:
            print(f"   L{config['lesson']:02d}  | {int(config['vocab']*100):3d}%  |      {config['translations']:2d}      |    {config['analyses']:2d}")

if __name__ == "__main__":
    seed_lesson_requirements()
