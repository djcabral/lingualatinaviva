"""
Motor de Verificación de Desafíos Gamificados

Este módulo contiene la lógica para verificar las respuestas de los usuarios
en los diferentes tipos de desafíos del mapa de aprendizaje.

DOCUMENTACIÓN COMPLETA PARA CONTINUIDAD:
=========================================

Este motor reutiliza la lógica existente de:
- LatinMorphology.decline_noun() -> Para desafíos de declinación
- LatinMorphology.conjugate_verb() -> Para desafíos de conjugación

Tipos de desafíos soportados:
1. declension: Declinar sustantivos (rosa, puella, etc.)
2. conjugation: Conjugar verbos (amo, moneo, etc.)
3. multiple_choice: Preguntas de opción múltiple
4. translation: Traducción español → latín
5. syntax: Identificar elementos sintácticos

IMPORTANTE PARA CONTINUIDAD:
----------------------------
Si necesitas agregar un nuevo tipo de desafío:
1. Agrega un elif en ChallengeEngine.verify_challenge()
2. Crea el método _verify_TIPO()
3. Retorna (score, errors, feedback) según el formato establecido
4. Actualiza la documentación del __init__()
"""

# Setup para testing standalone
import sys
from pathlib import Path
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Dict, List, Tuple, Optional
import json
from database import Word, Challenge
from database.connection import get_session
from utils.latin_logic import LatinMorphology
from sqlmodel import select


class ChallengeEngine:
    """
    Motor que verifica respuestas de desafíos.
    
    **Ret retorno estándar**: Todas las funciones _verify_*() deben retornar:
        Tuple[float, List[str], Dict]
        - score (float): 0.0-100.0 (porcentaje de aciertos)
        - errors (List[str]): Lista de mensajes de error específicos
        - feedback (Dict): Información adicional para mostrar al usuario
    
    **Ejemplo de uso**:
    ```python
    engine = ChallengeEngine()
    
    challenge = session.query(Challenge).filter(Challenge.id == 1).first()
    user_answers = {
        'nom_sg': 'rosa',
        'acc_sg': 'rosam',
        # ...
    }
    
    score, errors, feedback = engine.verify_challenge(challenge, user_answers)
    
    if score >= 60:
        print(f"✅ Aprobado! Score: {score}%")
        stars = engine.calculate_stars(score, attempts=1)
        print(f"Estrellas: {stars}")
    else:
        print(f"❌ Reprobado. Score: {score}%")
        print(f"Errores: {', '.join(errors)}")
    ```
    """
    
    def __init__(self):
        """Inicializa el motor de verificación"""
        pass
    
    def verify_challenge(
        self, 
        challenge: Challenge, 
        user_answers: Dict[str, str],
        config_override: Optional[Dict] = None
    ) -> Tuple[float, List[str], Dict]:
        """
        Verifica respuestas según el tipo de desafío.
        
        Args:
            challenge: Objeto Challenge de la BD
            user_answers: Respuestas del usuario
            config_override: (Opcional) Configuración específica para usar en lugar de la del desafío.
                             Útil para desafíos multi-etapa.
        
        Returns:
            (score, errors, feedback)
            
        Raises:
            ValueError: Si challenge_type no es reconocido
        """
        # Parsear configuración JSON
        if config_override:
            config = config_override
        else:
            try:
                config = json.loads(challenge.config_json)
            except json.JSONDecodeError:
                return (0.0, ["Error: Configuración de desafío inválida"], {})
        
        # Despachar según tipo
        if challenge.challenge_type == 'declension':
            return self._verify_declension(config, user_answers)
        
        elif challenge.challenge_type == 'conjugation':
            return self._verify_conjugation(config, user_answers)
        
        elif challenge.challenge_type == 'multiple_choice':
            return self._verify_multiple_choice(config, user_answers)
        
        elif challenge.challenge_type == 'translation':
            return self._verify_translation(config, user_answers)
        
        elif challenge.challenge_type == 'syntax':
            return self._verify_syntax(config, user_answers)
            
        elif challenge.challenge_type == 'sentence_order':
            return self._verify_sentence_order(config, user_answers)
            
        elif challenge.challenge_type == 'match_pairs':
            return self._verify_match_pairs(config, user_answers)
        
        else:
            raise ValueError(f"Tipo de desafío desconocido: {challenge.challenge_type}")

    def _verify_sentence_order(
        self,
        config: Dict,
        user_answers: Dict[str, List[str]]
    ) -> Tuple[float, List[str], Dict]:
        """
        Verifica el orden de palabras en una oración.
        
        Configuración esperada:
            {
                "target_sentence": "Puella rosam amat",
                ...
            }
            
        Respuestas del usuario:
            {
                "ordered_words": ["Puella", "rosam", "amat"]
            }
        """
        target = config.get('target_sentence', '')
        # Normalizar espacios y puntuación básica para comparación
        target_words = [w.strip() for w in target.split()]
        
        user_order = user_answers.get('ordered_words', [])
        
        if not user_order:
            return (0.0, ["No has seleccionado ninguna palabra"], {})
            
        # Comparación palabra por palabra
        errors = []
        correct_count = 0
        
        # Verificar longitud
        if len(user_order) != len(target_words):
            errors.append(f"Longitud incorrecta. Esperaba {len(target_words)} palabras, recibí {len(user_order)}.")
        
        # Verificar orden
        for i, (u, t) in enumerate(zip(user_order, target_words)):
            if self._normalize_latin(u) == self._normalize_latin(t):
                correct_count += 1
            else:
                if i < len(target_words):
                    errors.append(f"Posición {i+1}: Esperaba '{target_words[i]}', recibí '{u}'")
        
        # Score estricto: debe ser perfecto para 100%, o parcial basado en posición
        score = (correct_count / len(target_words) * 100) if target_words else 0
        
        # Penalizar si la longitud es incorrecta aunque las primeras coincidan
        if len(user_order) != len(target_words):
            score = score * 0.8
            
        return (score, errors, {'target': target})

    def _verify_match_pairs(
        self,
        config: Dict,
        user_answers: Dict[str, Dict[str, str]]
    ) -> Tuple[float, List[str], Dict]:
        """
        Verifica pares coincidentes.
        
        Configuración esperada:
            {
                "pairs": [
                    {"left": "rosa", "right": "la rosa"},
                    ...
                ]
            }
            
        Respuestas del usuario:
            {
                "matches": {
                    "rosa": "la rosa",
                    "puella": "la niña"
                }
            }
        """
        pairs = config.get('pairs', [])
        expected_matches = {p['left']: p['right'] for p in pairs}
        
        user_matches = user_answers.get('matches', {})
        
        if not user_matches:
            return (0.0, ["No has realizado ninguna coincidencia"], {})
            
        correct = 0
        errors = []
        
        for left, right in user_matches.items():
            if left in expected_matches:
                if expected_matches[left] == right:
                    correct += 1
                else:
                    errors.append(f"Incorrecto: {left} no es {right}")
            else:
                errors.append(f"Término desconocido: {left}")
                
        total_pairs = len(pairs)
        score = (correct / total_pairs * 100) if total_pairs > 0 else 0
        
        return (score, errors, {'total_pairs': total_pairs, 'correct': correct})
    
    def _verify_declension(
        self, 
        config: Dict, 
        user_answers: Dict[str, str]
    ) -> Tuple[float, List[str], Dict]:
        """
        Verifica declinación de sustantivos.
        
        Configuración esperada (config):
            {
                "word": "rosa",  # Palabra a declinar
                "cases": ["nominative", "accusative"],  # o "all" para todos
                "numbers": ["singular", "plural"]  # singular/plural a verificar
            }
        
        Respuestas del usuario (user_answers):
            {
                "nom_sg": "rosa",
                "acc_sg": "rosam",
                "nom_pl": "rosae",
                "acc_pl": "rosas",
                ...
            }
        
        Args:
            config: Configuración del desafío
            user_answers: Respuestas proporcionadas por el usuario
        
        Returns:
            (score, errors, feedback)
            
        Ejemplo:
            >>> config = {"word": "rosa", "cases": ["nominative", "accusative"], "numbers": ["singular", "plural"]}
            >>> user_answers = {"nom_sg": "rosa", "acc_sg": "rosam", "nom_pl": "rosae", "acc_pl": "rosas"}
            >>> score, errors, feedback = engine._verify_declension(config, user_answers)
            >>> score
            100.0
        """
        word_latin = config.get('word')
        cases_to_check = config.get('cases', 'all')
        numbers_to_check = config.get('numbers', ['singular', 'plural'])
        
        # Buscar la palabra en la BD
        with get_session() as session:
            word = session.exec(
                select(Word).where(Word.latin == word_latin)
            ).first()
        
        if not word:
            return (0.0, [f"Palabra '{word_latin}' no encontrada en BD"], {})
        
        # Generar formas correctas usando LatinMorphology
        correct_forms = LatinMorphology.decline_noun(
            word.latin,
            word.declension,
            word.gender,
            word.genitive,
            word.irregular_forms,
            word.parisyllabic,
            word.is_plurale_tantum,
            word.is_singulare_tantum
        )
        
        if not correct_forms:
            return (0.0, ["Error generando formas correctas"], {})
        
        # Mapeo de nombres de casos (config usa inglés, pero la BD puede usar español)
        case_map = {
            'nominative': 'nom',
            'genitive': 'gen',
            'dative': 'dat',
            'accusative': 'acc',
            'ablative': 'abl',
            'vocative': 'voc'
        }
        
        number_map = {
            'singular': 'sg',
            'plural': 'pl'
        }
        
        # Determinar qué casos verificar
        if cases_to_check == 'all':
            cases_list = list(case_map.keys())
        else:
            cases_list = cases_to_check
        
        # Verificar cada forma
        errors = []
        total = 0
        correct = 0
        
        for case in cases_list:
            case_abbr = case_map.get(case, case)
            
            for number in numbers_to_check:
                number_abbr = number_map.get(number, number)
                key = f"{case_abbr}_{number_abbr}"  # Ej: "nom_sg"
                
                total += 1
                
                # Obtener respuesta del usuario y forma correcta
                user_answer = user_answers.get(key, '').strip().lower()
                correct_answer = correct_forms.get(key, '').lower()
                
                # Normalizar (quitar macrones para comparación flexible)
                user_normalized = self._normalize_latin(user_answer)
                correct_normalized = self._normalize_latin(correct_answer)
                
                if user_normalized == correct_normalized:
                    correct += 1
                else:
                    errors.append(
                        f"{case.title()} {number}: esperaba '{correct_answer}', "
                        f"recibido '{user_answer}'"
                    )
        
        # Calcular score
        score = (correct / total * 100) if total > 0 else 0
        
        # Preparar feedback
        feedback = {
            'correct': correct,
            'total': total,
            'correct_forms': correct_forms,
            'word': word_latin
        }
        
        return (score, errors, feedback)
    
    def _verify_conjugation(
        self, 
        config: Dict, 
        user_answers: Dict[str, str]
    ) -> Tuple[float, List[str], Dict]:
        """
        Verifica conjugación de verbos.
        
        Configuración esperada (config):
            {
                "verb": "amo",  # Verbo a conjugar
                "tense": "present",  # present, imperfect, perfect, future, pluperfect
                "mood": "indicative",  # indicative, subjunctive, imperative
                "voice": "active"  # active, passive
            }
        
        Respuestas del usuario (user_answers):
            {
                "pres_1sg": "amo",
                "pres_2sg": "amas",
                "pres_3sg": "amat",
                ...
            }
        
        Args:
            config: Configuración del desafío
            user_answers: Respuestas del usuario
        
        Returns:
            (score, errors, feedback)
        """
        verb_latin = config.get('verb')
        tense = config.get('tense', 'present')
        mood = config.get('mood', 'indicative')
        voice = config.get('voice', 'active')
        
        # Buscar el verbo en la BD
        with get_session() as session:
            verb = session.exec(
                select(Word).where(
                    Word.latin == verb_latin,
                    Word.part_of_speech == 'verb'
                )
            ).first()
        
        if not verb:
            return (0.0, [f"Verbo '{verb_latin}' no encontrado en BD"], {})
        
        # Generar formas correctas
        correct_forms = LatinMorphology.conjugate_verb(
            verb.latin,
            verb.conjugation,
            verb.principal_parts,
            verb.irregular_forms
        )
        
        if not correct_forms:
            return (0.0, ["Error generando formas correctas"], {})
        
        # Mapeo de tiempos
        tense_prefix = {
            'present': 'pres',
            'imperfect': 'imp',
            'perfect': 'perf',
            'future': 'fut',
            'pluperfect': 'plup'
        }.get(tense, 'pres')
        
        # Personas y números a verificar
        persons = ['1sg', '2sg', '3sg', '1pl', '2pl', '3pl']
        
        # Verificar cada forma
        errors = []
        total = 0
        correct = 0
        
        for person in persons:
            key = f"{tense_prefix}_{person}"
            
            if key not in correct_forms:
                continue  # Saltar formas no generadas
            
            total += 1
            
            user_answer = user_answers.get(key, '').strip().lower()
            correct_answer = correct_forms[key].lower()
            
            # Normalizar
            user_normalized = self._normalize_latin(user_answer)
            correct_normalized = self._normalize_latin(correct_answer)
            
            if user_normalized == correct_normalized:
                correct += 1
            else:
                person_label = {
                    '1sg': '1ª sg', '2sg': '2ª sg', '3sg': '3ª sg',
                    '1pl': '1ª pl', '2pl': '2ª pl', '3pl': '3ª pl'
                }[person]
                
                errors.append(
                    f"{person_label}: esperaba '{correct_answer}', "
                    f"recibido '{user_answer}'"
                )
        
        # Calcular score
        score = (correct / total * 100) if total > 0 else 0
        
        # Preparar feedback
        feedback = {
            'correct': correct,
            'total': total,
            'correct_forms': correct_forms,
            'verb': verb_latin,
            'tense': tense
        }
        
        return (score, errors, feedback)
    
    def _verify_multiple_choice(
        self, 
        config: Dict, 
        user_answers: Dict[str, int]
    ) -> Tuple[float, List[str], Dict]:
        """
        Verifica preguntas de opción múltiple.
        
        Configuración esperada (config):
            {
                "questions": [
                    {
                        "text": "¿Qué caso es 'rosam'?",
                        "options": ["Nominativo", "Acusativo", "Genitivo"],
                        "correct": 1  # Índice de la respuesta correcta (0-indexed)
                    },
                    ...
                ]
            }
        
        Respuestas del usuario (user_answers):
            {
                "q0": 1,  # Usuario eligió opción en índice 1
                "q1": 0,
                ...
            }
        
        Args:
            config: Configuración del desafío
            user_answers: Índices de opciones elegidas por el usuario
        
        Returns:
            (score, errors, feedback)
        """
        questions = config.get('questions', [])
        
        if not questions:
            return (0.0, ["No hay preguntas en este desafío"], {})
        
        errors = []
        correct = 0
        
        for i, question in enumerate(questions):
            question_key = f"q{i}"
            user_choice = user_answers.get(question_key)
            correct_choice = question['correct']
            
            if user_choice == correct_choice:
                correct += 1
            else:
                errors.append(
                    f"Pregunta {i+1}: incorrecto. "
                    f"Respuesta correcta: {question['options'][correct_choice]}"
                )
        
        # Calcular score
        score = (correct / len(questions) * 100) if questions else 0
        
        # Feedback
        feedback = {
            'correct': correct,
            'total': len(questions),
            'questions': questions
        }
        
        return (score, errors, feedback)
    
    def _verify_translation(
        self, 
        config: Dict, 
        user_answers: Dict[str, str]
    ) -> Tuple[float, List[str], Dict]:
        """
        Verifica traducciones español → latín.
        
        NOTA IMPORTANTE:
        ---------------
        Esta es una verificación BÁSICA usando coincidencia de palabras.
        En el futuro, cuando el modelo de traducción esté entrenado,
        se puede mejorar usando el modelo para scoring más inteligente.
        
        Configuración esperada (config):
            {
                "translations": [
                    {
                        "spanish": "la rosa",
                        "latin": "rosa"
                    },
                    ...
                ]
            }
        
        O:
            {
                "spanish": "la rosa",  # Alternativa simple
                "latin": "rosa"
            }
        
        Respuestas del usuario (user_answers):
            {
                "translation": "rosa"  # Para formato simple
            }
            O
            {
                "t0": "rosa",  # Para múltiples traducciones
                "t1": "puellae",
                ...
            }
        
        Args:
            config: Configuración del desafío
            user_answers: Traducciones proporcionadas por el usuario
        
        Returns:
            (score, errors, feedback)
        """
        # Soportar dos formatos:
        # 1. Simple: {"spanish": "...", "latin": "..."}
        # 2. Múltiple: {"translations": [{...}, {...}]}
        
        if 'translations' in config:
            translations = config['translations']
        else:
            translations = [{'spanish': config.get('spanish'), 'latin': config.get('latin')}]
        
        errors = []
        total_score = 0
        total_translations = len(translations)
        
        for i, trans in enumerate(translations):
            expected = trans['latin'].lower().strip()
            
            # Obtener respuesta del usuario
            if total_translations == 1:
                user_input = user_answers.get('translation', '').lower().strip()
            else:
                user_input = user_answers.get(f't{i}', '').lower().strip()
            
            # Normalizar
            expected_norm = self._normalize_latin(expected)
            user_norm = self._normalize_latin(user_input)
            
            # Verificación exacta
            if user_norm == expected_norm:
                total_score += 100
            else:
                # Verificación flexible (palabras clave)
                expected_words = set(expected_norm.split())
                user_words = set(user_norm.split())
                
                if expected_words and user_words:
                    overlap = len(expected_words & user_words) / len(expected_words)
                    score_for_this = overlap * 100
                    total_score += score_for_this
                    
                    if score_for_this < 100:
                        errors.append(
                            f"Traducción {i+1}: esperaba '{expected}', recibido '{user_input}' "
                            f"(similitud: {score_for_this:.0f}%)"
                        )
                else:
                    errors.append(
                        f"Traducción {i+1}: esperaba '{expected}', recibido '{user_input}'"
                    )
        
        # Score promedio
        score = total_score / total_translations if total_translations > 0 else 0
        
        # Feedback
        feedback = {
            'translations': translations,
            'total': total_translations
        }
        
        return (score, errors, feedback)
    
    def _verify_syntax(
        self, 
        config: Dict, 
        user_answers: Dict[str, str]
    ) -> Tuple[float, List[str], Dict]:
        """
        Verifica identificación de elementos sintácticos.
        
        Configuración esperada (config):
            {
                "sentences": [
                    {
                        "sentence": "Puella amat",
                        "subject": "Puella",  # Respuesta esperada
                        # Otros elementos opcionales: "verb", "object", etc.
                    },
                    ...
                ]
            }
        
        Respuestas del usuario (user_answers):
            {
                "subject_0": "Puella",  # Para oración 0
                "verb_0": "amat",
                ...
            }
        
        Args:
            config: Configuración del desafío
            user_answers: Elementos identificados por el usuario
        
        Returns:
            (score, errors, feedback)
        """
        sentences = config.get('sentences', [])
        
        if not sentences:
            return (0.0, ["No hay oraciones en este desafío"], {})
        
        errors = []
        total = 0
        correct = 0
        
        for i, sentence in enumerate(sentences):
            # Elementos a verificar (subject, verb, object, etc.)
            for element in ['subject', 'verb', 'object', 'predicate']:
                if element in sentence:
                    total += 1
                    
                    user_answer = user_answers.get(f"{element}_{i}", '').strip().lower()
                    correct_answer = sentence[element].lower()
                    
                    # Normalizar
                    user_norm = self._normalize_latin(user_answer)
                    correct_norm = self._normalize_latin(correct_answer)
                    
                    if user_norm == correct_norm:
                        correct += 1
                    else:
                        errors.append(
                            f"Oración {i+1} - {element.title()}: "
                            f"esperaba '{correct_answer}', recibido '{user_answer}'"
                        )
        
        # Score
        score = (correct / total * 100) if total > 0 else 0
        
        # Feedback
        feedback = {
            'correct': correct,
            'total': total,
            'sentences': sentences
        }
        
        return (score, errors, feedback)
    
    def calculate_stars(self, score: float, attempts: int = 1) -> int:
        """
        Calcula las estrellas (0-3) basado en el score y el número de intentos.
        
        Criterios:
        - 3 estrellas: 100% correcto en el primer intento
        - 2 estrellas: 80-99% correcto
        - 1 estrella: 60-79% correcto (aprobado mínimo)
        - 0 estrellas: <60% (reprobado, debe reintentar)
        
        Args:
            score: Porcentaje de aciertos (0.0-100.0)
            attempts: Número de intentos (no usado actualmente, para expansión futura)
        
        Returns:
            int: Número de estrellas (0-3)
        
        Ejemplos:
            >>> engine.calculate_stars(100, attempts=1)
            3
            >>> engine.calculate_stars(85, attempts=1)
            2
            >>> engine.calculate_stars(65, attempts=1)
            1
            >>> engine.calculate_stars(50, attempts=1)
            0
        """
        if score >= 100:
            return 3  # Perfecto
        elif score >= 80:
            return 2  # Bien
        elif score >= 60:
            return 1  # Aprobado
        else:
            return 0  # Reprobado (debe reintentar)
    
    def _normalize_latin(self, text: str) -> str:
        """
        Normaliza texto latino para comparación flexible.
        
        Elimina:
        - Macrones (ā → a, ē → e, etc.)
        - Espacios extras
        - Puntuación
        
        Args:
            text: Texto a normalizar
        
        Returns:
            str: Texto normalizado
        
        Ejemplos:
            >>> engine._normalize_latin("  rosā  ")
            "rosa"
            >>> engine._normalize_latin("amāre")
            "amare"
        """
        # Mapeo de caracteres con macrones a sin macrones
        macron_map = {
            'ā': 'a', 'ē': 'e', 'ī': 'i', 'ō': 'o', 'ū': 'u',
            'Ā': 'A', 'Ē': 'E', 'Ī': 'I', 'Ō': 'O', 'Ū': 'U'
        }
        
        # Reemplazar macrones
        for macro, normal in macron_map.items():
            text = text.replace(macro, normal)
        
        # Limpiar espacios y puntuación
        text = text.strip()
        
        return text


# ============================================================================
# EJEMPLO DE USO (para testing)
# ============================================================================

if __name__ == "__main__":
    """
    Ejemplo de uso del ChallengeEngine.
    Ejecuta este archivo directamente para ver una demo.
    """
    print("=== DEMO: ChallengeEngine ===\n")
    
    # Crear motor
    engine = ChallengeEngine()
    
    # Ejemplo 1: Verificar declinación
    print("1. Verificando declinación de 'rosa'")
    declension_config = {
        'word': 'rosa',
        'cases': ['nominative', 'accusative'],
        'numbers': ['singular', 'plural']
    }
    declension_answers = {
        'nom_sg': 'rosa',
        'acc_sg': 'rosam',
        'nom_pl': 'rosae',
        'acc_pl': 'rosas'
    }
    
    score, errors, feedback = engine._verify_declension(declension_config, declension_answers)
    print(f"   Score: {score}%")
    print(f"   Errores: {len(errors)}")
    print(f"   Estrellas: {engine.calculate_stars(score)}")
    print()
    
    # Ejemplo 2: Verificar opción múltiple
    print("2. Verificando quiz de opción múltiple")
    quiz_config = {
        'questions': [
            {
                'text': '¿Qué caso es "rosam"?',
                'options': ['Nominativo', 'Acusativo', 'Genitivo'],
                'correct': 1
            }
        ]
    }
    quiz_answers = {'q0': 1}  # Usuario eligió acusativo (correcto)
    
    score, errors, feedback = engine._verify_multiple_choice(quiz_config, quiz_answers)
    print(f"   Score: {score}%")
    print(f"   Errores: {len(errors)}")
    print(f"   Estrellas: {engine.calculate_stars(score)}")
    print()
    
    print("✅ Demo completada")
