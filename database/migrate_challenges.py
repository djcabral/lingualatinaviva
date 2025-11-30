"""
Script de migración para crear el sistema de desafíos gamificados.

Este script:
1. Crea las tablas Challenge y UserChallengeProgress
2. Puebla con los primeros 20 desafíos siguiendo el curriculum educativo estándar
3. Inicializa el progreso del usuario (solo nivel 1 desbloqueado)
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.connection import create_db_and_tables, get_session
from database import Challenge, UserChallengeProgress, UserProfile
import json

def create_initial_challenges():
    """Crea los primeros 20 desafíos según el plan pedagógico"""
    
    challenges_data = [
        # ===== FASE 1: PRIMERA DECLINACIÓN (Niveles 1-10) =====
        
        {
            'order': 1,
            'title': 'Rosa: Nominativo y Acusativo',
            'description': 'Aprende los casos nominativo y acusativo de "rosa" (singular y plural). El nominativo es el sujeto. El acusativo es el complemento directo.',
            'challenge_type': 'declension',
            'config_json': json.dumps({
                'word': 'rosa',
                'cases': ['nominative', 'accusative'],
                'numbers': ['singular', 'plural']
            }),
            'xp_reward': 10,
            'requires_challenge_ids': None,  # Primer desafío, sin prerequisitos
            'grammar_topic': '1st_declension_basic',
            'difficulty_level': 1
        },
        
        {
            'order': 2,
            'title': 'Rosa: Genitivo y Dativo',
            'description': 'Aprende los casos genitivo y dativo de "rosa". El genitivo expresa posesión. El dativo es el complemento indirecto.',
            'challenge_type': 'declension',
            'config_json': json.dumps({
                'word': 'rosa',
                'cases': ['genitive', 'dative'],
                'numbers': ['singular', 'plural']
            }),
            'xp_reward': 15,
            'requires_challenge_ids': '1',
            'grammar_topic': '1st_declension_cases',
            'difficulty_level': 1
        },
        
        {
            'order': 3,
            'title': 'Rosa: Ablativo',
            'description': 'Aprende el caso ablativo de "rosa". El ablativo expresa circunstancias (con, de, desde, en, por).',
            'challenge_type': 'declension',
            'config_json': json.dumps({
                'word': 'rosa',
                'cases': ['ablative'],
                'numbers': ['singular', 'plural']
            }),
            'xp_reward': 15,
            'requires_challenge_ids': '2',
            'grammar_topic': '1st_declension_ablative',
            'difficulty_level': 2
        },
        
        {
            'order': 4,
            'title': 'Rosa: Declinación Completa',
            'description': 'Declina "rosa" en todos sus casos (nominativo, genitivo, dativo, acusativo, ablativo).',
            'challenge_type': 'declension',
            'config_json': json.dumps({
                'word': 'rosa',
                'cases': ['nominative', 'genitive', 'dative', 'accusative', 'ablative'],
                'numbers': ['singular', 'plural']
            }),
            'xp_reward': 25,
            'requires_challenge_ids': '3',
            'grammar_topic': '1st_declension_complete',
            'difficulty_level': 2
        },
        
        {
            'order': 5,
            'title': 'Puella: Declinación Completa',
            'description': 'Declina "puella" (niña) en todos los casos. Sigue el mismo patrón que "rosa".',
            'challenge_type': 'declension',
            'config_json': json.dumps({
                'word': 'puella',
                'cases': ['nominative', 'genitive', 'dative', 'accusative', 'ablative'],
                'numbers': ['singular', 'plural']
            }),
            'xp_reward': 25,
            'requires_challenge_ids': '4',
            'grammar_topic': '1st_declension_complete',
            'difficulty_level': 2
        },
        
        {
            'order': 6,
            'title': 'Quiz: Casos de la 1ª Declinación',
            'description': 'Identifica correctamente los casos de sustantivos de la primera declinación.',
            'challenge_type': 'multiple_choice',
            'config_json': json.dumps({
                'questions': [
                    {
                        'text': '¿Qué caso es "rosam"?',
                        'options': ['Nominativo', 'Acusativo', 'Genitivo', 'Dativo'],
                        'correct': 1  # Acusativo
                    },
                    {
                        'text': '¿Qué caso es "rosae" (singular)?',
                        'options': ['Nominativo', 'Genitivo', 'Dativo', 'Todas las anteriores'],
                        'correct': 3  # Genitivo, Dativo y Nominativo plural (pero singular es Gen/Dat)
                    },
                    {
                        'text': '¿Qué función tiene el acusativo?',
                        'options': ['Sujeto', 'Complemento directo', 'Posesión', 'Complemento indirecto'],
                        'correct': 1  # Complemento directo
                    }
                ]
            }),
            'xp_reward': 15,
            'requires_challenge_ids': '5',
            'grammar_topic': '1st_declension_quiz',
            'difficulty_level': 2
        },
        
        {
            'order': 7,
            'title': 'Aqua: Declinación Completa',
            'description': 'Declina "aqua" (agua) en todos los casos.',
            'challenge_type': 'declension',
            'config_json': json.dumps({
                'word': 'aqua',
                'cases': ['nominative', 'genitive', 'dative', 'accusative', 'ablative'],
                'numbers': ['singular', 'plural']
            }),
            'xp_reward': 25,
            'requires_challenge_ids': '6',
            'grammar_topic': '1st_declension_complete',
            'difficulty_level': 2
        },
        
        {
            'order': 8,
            'title': 'Concordancia Básica',
            'description': 'Aprende a combinar sustantivos con adjetivos de la 1ª clase.',
            'challenge_type': 'multiple_choice',
            'config_json': json.dumps({
                'questions': [
                    {
                        'text': 'Forma correcta de "rosa bonita" (nominativo singular):',
                        'options': ['rosa pulchra', 'rosam pulchram', 'rosae pulchrae', 'rosa pulcher'],
                        'correct': 0
                    },
                    {
                        'text': 'Forma correcta de "de la rosa bonita" (genitivo singular):',
                        'options': ['rosa pulchra', 'rosae pulchrae', 'rosam pulchram', 'rosas pulchras'],
                        'correct': 1
                    }
                ]
            }),
            'xp_reward': 20,
            'requires_challenge_ids': '7',
            'grammar_topic': 'concordance_basic',
            'difficulty_level': 3
        },
        
        {
            'order': 9,
            'title': 'Traducción Simple',
            'description': 'Traduce del español al latín oraciones simples.',
            'challenge_type': 'translation',
            'config_json': json.dumps({
                'translations': [
                    {'spanish': 'la rosa', 'latin': 'rosa'},
                    {'spanish': 'de la niña', 'latin': 'puellae'},
                    {'spanish': 'para el agua', 'latin': 'aquae'}  # dativo
                ]
            }),
            'xp_reward': 30,
            'requires_challenge_ids': '8',
            'grammar_topic': 'translation_basic',
            'difficulty_level': 3
        },
        
        {
            'order': 10,
            'title': 'Boss: 1ª Declinación',
            'description': '¡Desafío final de la 1ª declinación! Demuestra que dominas todos los casos.',
            'challenge_type': 'declension',
            'config_json': json.dumps({
                'word': 'silva',  # bosque
                'cases': ['nominative', 'genitive', 'dative', 'accusative', 'ablative'],
                'numbers': ['singular', 'plural']
            }),
            'xp_reward': 50,
            'requires_challenge_ids': '9',
            'grammar_topic': '1st_declension_boss',
            'difficulty_level': 3
        },
        
        # ===== FASE 2: PRESENTE DE INDICATIVO (Niveles 11-20) =====
        
        {
            'order': 11,
            'title': 'Verbo SUM (ser/estar)',
            'description': 'Conjuga el verbo irregular "sum" en presente de indicativo.',
            'challenge_type': 'conjugation',
            'config_json': json.dumps({
                'verb': 'sum',
                'tense': 'present',
                'mood': 'indicative',
                'voice': 'active'
            }),
            'xp_reward': 30,
            'requires_challenge_ids': '10',
            'grammar_topic': 'sum_present',
            'difficulty_level': 3
        },
        
        {
            'order': 12,
            'title': 'AMO: 1ª Conjugación',
            'description': 'Conjuga "amo" (amar) en presente de indicativo - 1ª conjugación.',
            'challenge_type': 'conjugation',
            'config_json': json.dumps({
                'verb': 'amo',
                'tense': 'present',
                'mood': 'indicative',
                'voice': 'active'
            }),
            'xp_reward': 35,
            'requires_challenge_ids': '11',
            'grammar_topic': '1st_conjugation_present',
            'difficulty_level': 4
        },
        
        {
            'order': 13,
            'title': 'MONEO: 2ª Conjugación',
            'description': 'Conjuga "moneo" (avisar) en presente de indicativo - 2ª conjugación.',
            'challenge_type': 'conjugation',
            'config_json': json.dumps({
                'verb': 'moneo',
                'tense': 'present',
                'mood': 'indicative',
                'voice': 'active'
            }),
            'xp_reward': 35,
            'requires_challenge_ids': '12',
            'grammar_topic': '2nd_conjugation_present',
            'difficulty_level': 4
        },
        
        {
            'order': 14,
            'title': 'Quiz: Presente de Indicativo',
            'description': 'Identifica formas verbales del presente de indicativo.',
            'challenge_type': 'multiple_choice',
            'config_json': json.dumps({
                'questions': [
                    {
                        'text': '¿Qué persona/número es "amant"?',
                        'options': ['1ª sg', '3ª sg', '3ª pl', '2ª pl'],
                        'correct': 2  # 3ª plural
                    },
                    {
                        'text': 'Forma correcta de "tú amas":',
                        'options': ['amo', 'amas', 'amat', 'amant'],
                        'correct': 1
                    },
                    {
                        'text': '¿Qué verbo es "sunt"?',
                        'options': ['amo', 'sum', 'moneo', 'lego'],
                        'correct': 1  # sum, 3ª pl
                    }
                ]
            }),
            'xp_reward': 20,
            'requires_challenge_ids': '13',
            'grammar_topic': 'present_indicative_quiz',
            'difficulty_level': 4
        },
        
        {
            'order': 15,
            'title': 'LEGO: 3ª Conjugación',
            'description': 'Conjuga "lego" (leer) en presente de indicativo - 3ª conjugación.',
            'challenge_type': 'conjugation',
            'config_json': json.dumps({
                'verb': 'lego',
                'tense': 'present',
                'mood': 'indicative',
                'voice': 'active'
            }),
            'xp_reward': 40,
            'requires_challenge_ids': '14',
            'grammar_topic': '3rd_conjugation_present',
            'difficulty_level': 5
        },
        
        {
            'order': 16,
            'title': 'AUDIO: 4ª Conjugación',
            'description': 'Conjuga "audio" (oír) en presente de indicativo - 4ª conjugación.',
            'challenge_type': 'conjugation',
            'config_json': json.dumps({
                'verb': 'audio',
                'tense': 'present',
                'mood': 'indicative',
                'voice': 'active'
            }),
            'xp_reward': 40,
            'requires_challenge_ids': '15',
            'grammar_topic': '4th_conjugation_present',
            'difficulty_level': 5
        },
        
        {
            'order': 17,
            'title': 'Oraciones: Sujeto + Verbo',
            'description': 'Traduce oraciones simples con sujeto y verbo.',
            'challenge_type': 'translation',
            'config_json': json.dumps({
                'translations': [
                    {'spanish': 'yo amo', 'latin': 'amo'},
                    {'spanish': 'tú eres', 'latin': 'es'},
                    {'spanish': 'ellos leen', 'latin': 'legunt'}
                ]
            }),
            'xp_reward': 30,
            'requires_challenge_ids': '16',
            'grammar_topic': 'translation_sv',
            'difficulty_level': 4
        },
        
        {
            'order': 18,
            'title': 'Análisis: Identificar Sujeto',
            'description': 'Identifica el sujeto en oraciones latinas.',
            'challenge_type': 'syntax',
            'config_json': json.dumps({
                'sentences': [
                    {'sentence': 'Puella amat', 'subject': 'Puella'},
                    {'sentence': 'Rosa est pulchra', 'subject': 'Rosa'},
                ]
            }),
            'xp_reward': 35,
            'requires_challenge_ids': '17',
            'grammar_topic': 'syntax_subject',
            'difficulty_level': 5
        },
        
        {
            'order': 19,
            'title': 'Traducción: S + V + OD',
            'description': 'Traduce oraciones con sujeto, verbo y objeto directo (acusativo).',
            'challenge_type': 'translation',
            'config_json': json.dumps({
                'translations': [
                    {'spanish': 'la niña ama a la rosa', 'latin': 'puella rosam amat'},
                    {'spanish': 'el muchacho lee el libro', 'latin': 'puer librum legit'}  # Nota: Necesitarás agregar "puer" y "librum"
                ]
            }),
            'xp_reward': 45,
            'requires_challenge_ids': '18',
            'grammar_topic': 'translation_svo',
            'difficulty_level': 5
        },
        
        {
            'order': 20,
            'title': 'Boss: Presente de Indicativo',
            'description': '¡Desafío final del presente! Conjuga cualquiera de las 4 conjugaciones.',
            'challenge_type': 'conjugation',
            'config_json': json.dumps({
                'verb': 'laboro',  # trabajar (1ª conjugación)
                'tense': 'present',
                'mood': 'indicative',
                'voice': 'active'
            }),
            'xp_reward': 75,
            'requires_challenge_ids': '19',
            'grammar_topic': 'present_indicative_boss',
            'difficulty_level': 5
        },
    ]
    
    return challenges_data


def migrate():
    """Ejecuta la migración completa"""
    print("=" * 60)
    print("MIGRACIÓN: Sistema de Desafíos Gamificados")
    print("=" * 60)
    
    # 1. Crear tablas
    print("\n📦 Creando tablas...")
    create_db_and_tables()
    print("✅ Tablas creadas")
    
    # 2. Obtener sesión
    session = get_session()
    
    # 3. Crear desafíos
    print("\n🎯 Creando desafíos...")
    challenges_data = create_initial_challenges()
    
    # Verificar si ya existen desafíos
    existing_count = session.exec(select(Challenge)).first()
    
    if existing_count:
        print(f"⚠️ Los desafíos ya existen. Saltando creación.")
        print(f"   (Si quieres recrearlos, borra la tabla challenge primero)")
    else:
        for data in challenges_data:
            challenge = Challenge(**data)
            session.add(challenge)
        
        session.commit()
        print(f"✅ Creados {len(challenges_data)} desafíos")
    
    # 4. Inicializar progreso del usuario
    print("\n👤 Inicializando progreso del usuario...")
    
    # Desbloquear solo el primer desafío
    first_challenge = session.exec(select(Challenge).where(Challenge.order == 1)).first()
    
    if first_challenge:
        progress = UserChallengeProgress(
            user_id=1,
            challenge_id=first_challenge.id,
            status='unlocked',
            unlocked_at=datetime.now()
        )
        session.add(progress)
        session.commit()
        print(f"✅ Desbloqueado desafío 1: {first_challenge.title}")
    
    # Bloquear el resto
    all_challenges = session.exec(select(Challenge).where(Challenge.order > 1)).all()
    for challenge in all_challenges:
        progress = UserChallengeProgress(
            user_id=1,
            challenge_id=challenge.id,
            status='locked'
        )
        session.add(progress)
    session.commit()
    print(f"✅ Bloqueados {len(all_challenges)} desafíos restantes")
    
    # 5. Actualizar UserProfile si existe (OPCIONAL - puede fallar si la tabla necesita migración)
    print("\n📊 Actualizando perfil de usuario...")
    try:
        user = session.exec(select(UserProfile)).first()
        if user:
            user.current_challenge_id = first_challenge.id
            session.commit()
            print("✅ Perfil actualizado")
        else:
            print("⚠️ No se encontró perfil de usuario (se puede crear después)")
    except Exception as e:
        print(f"⚠️ No se pudo actualizar perfil (tabla necesita migración): {str(e)[:100]}")
        print("   → Esto es normal si es la primera vez que ejecutas este script")
    
    print("\n" + "=" * 60)
    print("✅ MIGRACIÓN COMPLETADA")
    print("=" * 60)
    print(f"\n🎮 Primeros {len(challenges_data)} desafíos listos para jugar!")
    print(f"🔓 Desafío 1 desbloqueado: {first_challenge.title}")
    print("\n💡 Próximo paso: Abre la página 08_🗺️_Mapa.py para ver el mapa")


if __name__ == "__main__":
    from datetime import datetime
    from sqlmodel import select
    migrate()
