#!/usr/bin/env python3
"""
Script para importar y distribuir las 1500 palabras más frecuentes del latín
a través de las lecciones L1-L30, respetando la gradualidad pedagógica.

Estrategia:
1. Importar lista de frecuencia (DCC Core 1000 + Diederich 500)
2. Clasificar por tipo morfológico (declinación, conjugación)
3. Asignar a lecciones según tema gramatical
4. Dentro de cada grupo, priorizar por frecuencia

Ejemplo:
- L3 (1ª declinación): Tomar sustantivos 1ª decl. más frecuentes
- L4 (2ª declinación): Tomar sustantivos 2ª decl. más frecuentes
- L7 (3ª declinación): Tomar sustantivos 3ª decl. más frecuentes

Uso:
    python scripts/import_frequency_vocabulary.py --source dcc --limit 1500
"""

import argparse
import csv
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.connection import get_session
from database.models import Word


# Mapa de lecciones a tipos morfológicos requeridos
LESSON_GRAMMAR_FOCUS = {
    1: {  # Primeros pasos - vocabulario básico
        "nouns": {"declensions": ["1", "2"], "count": 15},
        "verbs": {"conjugations": ["1"], "count": 8, "tenses": ["present"]},
        "adjectives": {"types": ["1_2_class"], "count": 5},
        "invariable": {"types": ["conjunction", "preposition"], "count": 7}
    },
    2: {  # El sujeto - nominativo
        "nouns": {"declensions": ["1", "2"], "count": 15, "focus": "subjects"},
        "verbs": {"conjugations": ["1", "2"], "count": 10, "transitive": True},
        "adjectives": {"count": 5}
    },
    3: {  # 1ª Declinación completa
        "nouns": {"declensions": ["1"], "count": 25},
        "verbs": {"forms": ["sum_all_forms"], "count": 5}
    },
    4: {  # 2ª Declinación
        "nouns": {"declensions": ["2"], "count": 25, "genders": ["m", "n"]},
        "verbs": {"conjugations": ["1", "2"], "count": 5}
    },
    5: {  # El neutro
        "nouns": {"declensions": ["2", "3"], "gender": "n", "count": 20},
        "adjectives": {"count": 10, "neuter_compatible": True}
    },
    6: {  # Adjetivos 1ª clase
        "adjectives": {"types": ["1_2_class"], "count": 20},
        "nouns": {"count": 10}
    },
    7: {  # 3ª Declinación
        "nouns": {"declensions": ["3"], "count": 25, "subtypes": ["consonantal"]},
        "verbs": {"count": 5}
    },
    8: {  # 4ª Declinación + Pretérito
        "nouns": {"declensions": ["4"], "count": 15},
        "verbs": {"tenses": ["perfect"], "count": 15}
    },
    9: {  # 5ª Declinación + Futuro
        "nouns": {"declensions": ["5"], "count": 10},
        "verbs": {"tenses": ["future"], "count": 15},
        "other": {"count": 5}
    },
    10: {  # Adjetivos 2ª clase
        "adjectives": {"types": ["3rd_declension"], "count": 20},
        "nouns": {"count": 10}
    },
    11: {  # Comparación
        "adjectives": {"forms": ["comparative", "superlative"], "count": 15},
        "adverbs": {"count": 10},
        "other": {"count": 5}
    },
    12: {  # Pronombres
        "pronouns": {"types": ["personal", "demonstrative", "relative"], "count": 20},
        "other": {"count": 10}
    },
    13: {  # Voz pasiva + Ablativo
        "verbs": {"voice": "passive", "count": 15},
        "nouns": {"case_focus": "ablative", "count": 10},
        "prepositions": {"case": "ablative", "count": 5}
    },
    # 14-20: Sistema verbal completo
    14: {"verbs": {"tenses": ["pluperfect", "future_perfect"], "count": 25}, "other": {"count": 5}},
    15: {"verbs": {"voice": "passive", "tenses": ["infectum"], "count": 25}, "other": {"count": 5}},
    16: {"verbs": {"voice": "passive", "tenses": ["perfectum"], "count": 25}, "other": {"count": 5}},
    17: {"verbs": {"deponent": True, "count": 25}, "other": {"count": 5}},
    18: {"verbs": {"mood": "subjunctive", "tenses": ["present", "perfect"], "count": 25}, "other": {"count": 5}},
    19: {"verbs": {"mood": "subjunctive", "tenses": ["imperfect", "pluperfect"], "count": 20}, "conjunctions": {"subordinating": True, "count": 10}},
    20: {"verbs": {"infinitives": True, "aci": True, "count": 20}, "other": {"count": 10}},
    # 21-24: Formas nominales
    21: {"verbs": {"participles": True, "count": 20}, "other": {"count": 10}},
    22: {"verbs": {"ablative_absolute": True, "count": 15}, "nouns": {"count": 10}, "other": {"count": 5}},
    23: {"verbs": {"gerund": True, "gerundive": True, "count": 20}, "other": {"count": 10}},
    24: {"verbs": {"periphrastic": True, "count": 20}, "other": {"count": 10}},
    # 25-30: Sintaxis avanzada
    25: {"conjunctions": {"all_types": True, "count": 15}, "verbs": {"count": 10}, "other": {"count": 5}},
    26: {"verbs": {"completive": True, "count": 15}, "conjunctions": {"ut_ne": True, "count": 10}, "other": {"count": 5}},
    27: {"verbs": {"conditional": True, "count": 15}, "conjunctions": {"si_nisi": True, "count": 10}, "other": {"count": 5}},
    28: {"pronouns": {"relative": True, "count": 15}, "verbs": {"count": 10}, "other": {"count": 5}},
    29: {"verbs": {"indirect_speech": True, "count": 20}, "other": {"count": 10}},
    30: {"all": {"poetry_metrics": True, "count": 30}}
}


def load_dcc_core_1000(csv_path: str) -> List[Dict]:
    """Carga la lista DCC Core 1000 desde CSV"""
    words = []
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                words.append({
                    'latin': row.get('Latin', row.get('latin', '')),
                    'english': row.get('English', row.get('english', '')),
                    'pos': row.get('POS', row.get('pos', '')),
                    'frequency_rank': int(row.get('Rank', row.get('rank', len(words) + 1)))
                })
        print(f"✅ Cargadas {len(words)} palabras desde {csv_path}")
        return words
    except FileNotFoundError:
        print(f"❌ No se encontró el archivo {csv_path}")
        print("   Descarga primero la lista DCC desde:")
        print("   https://dcc.dickinson.edu/latin-vocabulary-list")
        sys.exit(1)


def classify_word_morphology(latin_word: str, pos: str) -> Dict:
    """
    Clasifica una palabra por su morfología usando Collatinus.
    Retorna diccionario con: declension, gender, conjugation, etc.
    """
    from utils.collatinus_query import get_word_info
    
    try:
        info = get_word_info(latin_word)
        if not info:
            return {"type": pos, "unclassified": True}
        
        classification = {
            "latin": latin_word,
            "pos": pos
        }
        
        # Para sustantivos: extraer declinación y género
        if pos in ["noun", "nomen"]:
            # Collatinus retorna algo como: "rosa, -ae f. (1st decl.)"
            # Aquí necesitarías parsear la respuesta de Collatinus
            # Por ahora, retorno placeholder
            classification["declension"] = info.get("declension", "unknown")
            classification["gender"] = info.get("gender", "unknown")
        
        # Para verbos: extraer conjugación
        elif pos in ["verb", "verbum"]:
            classification["conjugation"] = info.get("conjugation", "unknown")
            classification["deponent"] = info.get("deponent", False)
        
        # Para adjetivos
        elif pos in ["adjective", "adj"]:
            classification["adjective_type"] = info.get("type", "1_2_class")
        
        return classification
        
    except Exception as e:
        print(f"⚠️  Error al clasificar '{latin_word}': {e}")
        return {"type": pos, "unclassified": True}


def assign_words_to_lessons(
    frequency_words: List[Dict],
    lesson_grammar: Dict[int, Dict]
) -> Dict[int, List[Dict]]:
    """
    Asigna palabras a lecciones según la gradualidad pedagógica.
    
    Estrategia:
    1. Clasificar todas las palabras por morfología
    2. Para cada lección, seleccionar palabras que coincidan con su gramática
    3. Priorizar por frecuencia dentro de cada grupo
    """
    # Clasificar todas las palabras
    print("\n🔍 Clasificando palabras por morfología...")
    classified_words = []
    for word in frequency_words[:1500]:  # Limitar a 1500
        morphology = classify_word_morphology(word['latin'], word['pos'])
        classified_words.append({**word, **morphology})
    
    # Agrupar por tipo morfológico
    by_morph = defaultdict(list)
    for word in classified_words:
        if word.get('declension'):
            key = f"noun_decl_{word['declension']}"
            by_morph[key].append(word)
        elif word.get('conjugation'):
            key = f"verb_conj_{word['conjugation']}"
            by_morph[key].append(word)
        elif word['pos'] in ["adjective", "adj"]:
            by_morph["adjectives"].append(word)
        elif word['pos'] in ["pronoun", "pron"]:
            by_morph["pronouns"].append(word)
        else:
            by_morph[word['pos']].append(word)
    
    # Asignar a lecciones
    assignments = defaultdict(list)
    used_words = set()
    
    for lesson_num in range(1, 31):
        grammar = lesson_grammar.get(lesson_num, {})
        lesson_words = []
        
        # Sustantivos
        if "nouns" in grammar:
            noun_spec = grammar["nouns"]
            target_count = noun_spec.get("count", 15)
            declensions = noun_spec.get("declensions", ["1", "2", "3", "4", "5"])
            
            for decl in declensions:
                key = f"noun_decl_{decl}"
                available = [w for w in by_morph[key] if w['latin'] not in used_words]
                # Ordenar por frecuencia
                available.sort(key=lambda x: x['frequency_rank'])
                # Tomar los necesarios
                take = min(target_count // len(declensions), len(available))
                for word in available[:take]:
                    lesson_words.append(word)
                    used_words.add(word['latin'])
        
        # Verbos
        if "verbs" in grammar:
            verb_spec = grammar["verbs"]
            target_count = verb_spec.get("count", 10)
            conjugations = verb_spec.get("conjugations", ["1", "2", "3", "4"])
            
            for conj in conjugations:
                key = f"verb_conj_{conj}"
                available = [w for w in by_morph[key] if w['latin'] not in used_words]
                available.sort(key=lambda x: x['frequency_rank'])
                take = min(target_count // len(conjugations), len(available))
                for word in available[:take]:
                    lesson_words.append(word)
                    used_words.add(word['latin'])
        
        # Adjetivos, pronombres, etc.
        # Similar al proceso anterior...
        
        assignments[lesson_num] = lesson_words
        print(f"  L{lesson_num:2d}: {len(lesson_words):2d} palabras asignadas")
    
    return assignments


def main():
    parser = argparse.ArgumentParser(
        description="Importar 1500 palabras más frecuentes del latín"
    )
    parser.add_argument(
        '--source',
        choices=['dcc', 'diederich'],
        default='dcc',
        help="Fuente de datos de frecuencia"
    )
    parser.add_argument(
        '--csv',
        default='data/dcc_core_1000.csv',
        help="Ruta al CSV de frecuencia"
    )
    parser.add_argument(
        '--output',
        default='data/vocabulary_by_lesson_frequency.csv',
        help="Archivo CSV de salida con asignaciones"
    )
    
    args = parser.parse_args()
    
    # Cargar palabras de frecuencia
    print(f"\n📂 Cargando lista de frecuencia desde {args.csv}...")
    frequency_words = load_dcc_core_1000(args.csv)
    
    # Asignar a lecciones
    print("\n🎯 Asignando palabras a lecciones según gradualidad...")
    assignments = assign_words_to_lessons(frequency_words, LESSON_GRAMMAR_FOCUS)
    
    # Guardar CSV
    print(f"\n💾 Guardando asignaciones en {args.output}...")
    with open(args.output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['latin', 'new_lesson', 'frequency_rank', 'pos', 'reason'])
        
        for lesson, words in sorted(assignments.items()):
            for word in words:
                writer.writerow([
                    word['latin'],
                    lesson,
                    word['frequency_rank'],
                    word['pos'],
                    f"{word['pos']} pertinente a gramática L{lesson}"
                ])
    
    print(f"✅ {sum(len(v) for v in assignments.values())} palabras asignadas")
    print(f"\n📊 Distribución final:")
    for lesson in range(1, 31):
        count = len(assignments.get(lesson, []))
        print(f"  L{lesson:2d}: {count:3d} palabras")


if __name__ == "__main__":
    main()
