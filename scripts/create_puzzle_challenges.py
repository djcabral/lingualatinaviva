"""
Script para crear desafíos de tipo Puzzle en la base de datos.

Este script inserta desafíos de ejemplo para los nuevos tipos interactivos:
- sentence_order (Rompecabezas de ordenamiento)
- match_pairs (Parejas)

Uso:
    python scripts/create_puzzle_challenges.py
"""

from database.connection import get_session
from database import Challenge
import json

def create_puzzle_challenges():
    """Crea desafíos de tipo puzzle en la BD."""
    
    session = get_session()
    
    challenges = []
    
    # ========================================
    # SENTENCE ORDER CHALLENGES (Rompecabezas)
    # ========================================
    
    # Desafío 1: Oración simple nivel 1
    challenges.append(Challenge(
        level=1,
        challenge_type="sentence_order",
        title="🧩 Ordena: La niña ama la rosa",
        description="Ordena las palabras para formar una oración correcta en latín.",
        xp_reward=15,
        config=json.dumps([
            {
                "target_sentence": "Puella rosam amat",
                "distractors": ["puer"],
                "translation": "La niña ama la rosa"
            },
            {
                "target_sentence": "Rosa pulchra est",
                "distractors": ["magnus"],
                "translation": "La rosa es hermosa"
            },
            {
                "target_sentence": "Aqua clara est",
                "distractors": [],
                "translation": "El agua es clara"
            }
        ]),
        prerequisites=[]
    ))
    
    # Desafío 2: Oración con complemento nivel 2
    challenges.append(Challenge(
        level=2,
        challenge_type="sentence_order",
        title="🧩 Ordena: Oraciones con complementos",
        description="Ordena palabras formando oraciones más complejas.",
        xp_reward=20,
        config=json.dumps([
            {
                "target_sentence": "Marcus puellam videt",
                "distractors": ["rosa", "aqua"],
                "translation": "Marco ve a la niña"
            },
            {
                "target_sentence": "Dominus servum vocat",
                "distractors": ["puella"],
                "translation": "El amo llama al esclavo"
            },
            {
                "target_sentence": "Femina aquam portat",
                "distractors": ["vir"],
                "translation": "La mujer lleva agua"
            }
        ]),
        prerequisites=[1]
    ))
    
    # Desafío 3: Oraciones con adjetivos nivel 3
    challenges.append(Challenge(
        level=3,
        challenge_type="sentence_order",
        title="🧩 Ordena: Oraciones con adjetivos",
        description="Ordena oraciones que incluyen adjetivos concordantes.",
        xp_reward=25,
        config=json.dumps([
            {
                "target_sentence": "Puella pulchra rosam amat",
                "distractors": ["magnus", "servus"],
                "translation": "La niña hermosa ama la rosa"
            },
            {
                "target_sentence": "Dominus bonus servum laudat",
                "distractors": ["mala", "aqua"],
                "translation": "El buen amo alaba al esclavo"
            },
            {
                "target_sentence": "Vir fortis pugnat",
                "distractors": ["clara", "femina"],
                "translation": "El hombre valiente lucha"
            }
        ]),
        prerequisites=[2]
    ))
    
    # ========================================
    # MATCH PAIRS CHALLENGES (Parejas)
    # ========================================
    
    # Desafío 4: Vocabulario básico nivel 1
    challenges.append(Challenge(
        level=1,
        challenge_type="match_pairs",
        title="🔗 Parejas: Vocabulario básico",
description="Une cada palabra latina con su traducción al español.",
        xp_reward=15,
        config=json.dumps([
            {
                "pairs": [
                    {"left": "rosa", "right": "la rosa"},
                    {"left": "puella", "right": "la niña"},
                    {"left": "aqua", "right": "el agua"},
                    {"left": "amat", "right": "ama"}
                ]
            },
            {
                "pairs": [
                    {"left": "puer", "right": "el niño"},
                    {"left": "dominus", "right": "el amo"},
                    {"left": "servus", "right": "el esclavo"},
                    {"left": "femina", "right": "la mujer"}
                ]
            },
            {
                "pairs": [
                    {"left": "magnus", "right": "grande"},
                    {"left": "pulcher", "right": "hermoso"},
                    {"left": "malus", "right": "malo"},
                    {"left": "bonus", "right": "bueno"}
                ]
            }
        ]),
        prerequisites=[]
    ))
    
    # Desafío 5: Casos gramaticales nivel 2
    challenges.append(Challenge(
        level=2,
        challenge_type="match_pairs",
        title="🔗 Parejas: Casos de 'rosa'",
        description="Une cada forma con su caso gramatical.",
        xp_reward=20,
        config=json.dumps([
            {
                "pairs": [
                    {"left": "rosa", "right": "Nominativo sing."},
                    {"left": "rosam", "right": "Acusativo sing."},
                    {"left": "rosae", "right": "Genitivo sing."},
                    {"left": "rosas", "right": "Acusativo pl."}
                ]
            },
            {
                "pairs": [
                    {"left": "puella", "right": "Nominativo sing."},
                    {"left": "puellam", "right": "Acusativo sing."},
                    {"left": "puellae", "right": "Genitivo sing."},
                    {"left": "puellis", "right": "Dativo pl."}
                ]
            },
            {
                "pairs": [
                    {"left": "servus", "right": "Nominativo sing."},
                    {"left": "servum", "right": "Acusativo sing."},
                    {"left": "servi", "right": "Genitivo sing."},
                    {"left": "servos", "right": "Acusativo pl."}
                ]
            }
        ]),
        prerequisites=[4]
    ))
    
    # Desafío 6: Tiempos verbales nivel 3
    challenges.append(Challenge(
        level=3,
        challenge_type="match_pairs",
        title="🔗 Parejas: Tiempos de 'amo'",
        description="Une cada forma verbal con su tiempo gramatical.",
        xp_reward=25,
        config=json.dumps([
            {
                "pairs": [
                    {"left": "amo", "right": "Presente 1ª sg."},
                    {"left": "amabam", "right": "Imperfecto 1ª sg."},
                    {"left": "amavi", "right": "Perfecto 1ª sg."},
                    {"left": "amabo", "right": "Futuro 1ª sg."}
                ]
            },
            {
                "pairs": [
                    {"left": "amas", "right": "Presente 2ª sg."},
                    {"left": "amabas", "right": "Imperfecto 2ª sg."},
                    {"left": "amavisti", "right": "Perfecto 2ª sg."},
                    {"left": "amabis", "right": "Futuro 2ª sg."}
                ]
            },
            {
                "pairs": [
                    {"left": "laudat", "right": "Presente 3ª sg."},
                    {"left": "laudabat", "right": "Imperfecto 3ª sg."},
                    {"left": "laudavit", "right": "Perfecto 3ª sg."},
                    {"left": "laudabit", "right": "Futuro 3ª sg."}
                ]
            }
        ]),
        prerequisites=[5]
    ))
    
    # ========================================
    # INSERTAR EN BASE DE DATOS
    # ========================================
    
    print("🎯 Creando desafíos de tipo Puzzle...\n")
    
    for idx, challenge in enumerate(challenges, 1):
        try:
            session.add(challenge)
            session.commit()
            session.refresh(challenge)
            print(f"✅ Desafío {idx}/{len(challenges)}: '{challenge.title}' (ID: {challenge.id})")
        except Exception as e:
            print(f"❌ Error al crear desafío {idx}: {e}")
            session.rollback()
    
    session.close()
    print(f"\n🎉 ¡{len(challenges)} desafíos creados exitosamente!")
    print("\n💡 Ahora puedes probarlos en el mapa: streamlit run app.py")

if __name__ == "__main__":
    create_puzzle_challenges()
