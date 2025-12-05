"""
Static Exercise Loader
Carga y sirve ejercicios estáticos desde archivos JSON para lecciones específicas.
"""
import json
import os
from typing import Dict, List, Optional

EXERCISES_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "static_exercises")


def load_static_exercises(lesson_number: int) -> Optional[Dict]:
    """
    Carga ejercicios estáticos desde JSON para una lección.
    
    Args:
        lesson_number: Número de lección (20-29)
        
    Returns:
        Diccionario con ejercicios o None si no existe archivo
    """
    filepath = os.path.join(EXERCISES_DIR, f"exercises_l{lesson_number}.json")
    
    if not os.path.exists(filepath):
        return None
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error cargando ejercicios L{lesson_number}: {e}")
        return None


def get_exercises_by_type(lesson_number: int, exercise_type: str) -> List[Dict]:
    """
    Filtra y retorna ejercicios de un tipo específico.
    
    Args:
        lesson_number: Número de lección
        exercise_type: Tipo de ejercicio ('multiple_choice', 'sentence_completion', 'vocabulary_match')
        
    Returns:
        Lista de ejercicios del tipo especificado
    """
    data = load_static_exercises(lesson_number)
    
    if not data or "exercises" not in data:
        return []
    
    return [ex for ex in data["exercises"] if ex.get("type") == exercise_type]


def get_all_exercise_types(lesson_number: int) -> Dict[str, List[Dict]]:
    """
    Obtiene todos los ejercicios agrupados por tipo.
    
    Args:
        lesson_number: Número de lección
        
    Returns:
        Diccionario con listas de ejercicios por tipo
    """
    data = load_static_exercises(lesson_number)
    
    if not data or "exercises" not in data:
        return {}
    
    result = {
        "multiple_choice": [],
        "sentence_completion": [],
        "vocabulary_match": []
    }
    
    for ex in data["exercises"]:
        ex_type = ex.get("type", "")
        if ex_type in result:
            result[ex_type].append(ex)
    
    return result
