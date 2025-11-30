"""
Constants
Constantes compartidas en toda la aplicación.
"""

# ===== CASOS GRAMATICALES =====

CASES = ["nominativus", "vocativus", "accusativus", "genitivus", "dativus", "ablativus"]

CASE_LABELS = {
    "nominativus": "Nominativus",
    "vocativus": "Vocativus",
    "accusativus": "Accusativus",
    "genitivus": "Genitivus",
    "dativus": "Dativus",
    "ablativus": "Ablativus"
}

CASE_LABELS_LIST = ["Nominativus", "Vocativus", "Accusativus", "Genitivus", "Dativus", "Ablativus"]

# Abreviaciones de casos (para keys en diccionarios)
CASE_ABBREV = {
    "nominativus": "nom",
    "vocativus": "voc",
    "accusativus": "acc",
    "genitivus": "gen",
    "dativus": "dat",
    "ablativus": "abl"
}

# ===== NÚMEROS GRAMATICALES =====

NUMBERS = ["singular", "plural"]

NUMBER_LABELS = {
    "singular": "Singularis",
    "plural": "Pluralis"
}

NUMBER_ABBREV = {
    "singular": "sg",
    "plural": "pl"
}

# ===== GÉNEROS GRAMATICALES =====

GENDERS = ["m", "f", "n"]

GENDER_LABELS = {
    "m": "Masculino",
    "f": "Femenino",
    "n": "Neutro"
}

GENDER_LABELS_FULL = {
    "m": "Masculino",
    "f": "Femenino",
    "n": "Neutro",
    "masculine": "Masculino",
    "feminine": "Femenino",
    "neuter": "Neutro"
}

# ===== DECLINACIONES =====

DECLENSIONS = ["1", "2", "3", "4", "5"]

DECLENSION_LABELS = {
    "1": "1ª declinación",
    "2": "2ª declinación",
    "3": "3ª declinación",
    "4": "4ª declinación",
    "5": "5ª declinación"
}

# ===== CONJUGACIONES =====

CONJUGATIONS = ["1", "2", "3", "4", "irregular"]

CONJUGATION_LABELS = {
    "1": "1ª conjugación",
    "2": "2ª conjugación",
    "3": "3ª conjugación",
    "4": "4ª conjugación",
    "irregular": "Irregular"
}

# ===== PARTES DEL DISCURSO =====

PARTS_OF_SPEECH = [
    "noun", "verb", "adjective", "adverb", 
    "preposition", "conjunction", "pronoun", "interjection"
]

POS_TRANSLATIONS = {
    "noun": "Sustantivo",
    "verb": "Verbo",
    "adjective": "Adjetivo",
    "adverb": "Adverbio",
    "preposition": "Preposición",
    "conjunction": "Conjunción",
    "pronoun": "Pronombre",
    "interjection": "Interjección"
}

POS_TRANSLATIONS_REVERSE = {v: k for k, v in POS_TRANSLATIONS.items()}

# ===== VOCES VERBALES =====

VOICES = ["active", "passive"]

VOICE_LABELS = {
    "active": "Activa",
    "passive": "Pasiva"
}

# ===== MODOS VERBALES =====

MOODS = ["indicative", "subjunctive", "imperative"]

MOOD_LABELS = {
    "indicative": "Indicativo",
    "subjunctive": "Subjuntivo",
    "imperative": "Imperativo"
}

# ===== TIEMPOS VERBALES =====

TENSES_INDICATIVE = [
    "present", "imperfect", "future",
    "perfect", "pluperfect", "future_perfect"
]

TENSE_LABELS_INDICATIVE = {
    "present": "Presente",
    "imperfect": "Imperfecto",
    "future": "Futuro",
    "perfect": "Perfecto",
    "pluperfect": "Pluscuamperfecto",
    "future_perfect": "Futuro Perfecto"
}

TENSES_SUBJUNCTIVE = [
    "present", "imperfect", "perfect", "pluperfect"
]

TENSE_LABELS_SUBJUNCTIVE = {
    "present": "Presente",
    "imperfect": "Imperfecto",
    "perfect": "Perfecto",
    "pluperfect": "Pluscuamperfecto"
}

# ===== PERSONAS GRAMATICALES =====

PERSONS = ["1", "2", "3"]

PERSON_LABELS = {
    "1": "1ª persona",
    "2": "2ª persona",
    "3": "3ª persona"
}

# ===== NIVELES DE DIFICULTAD =====

LEVELS = list(range(1, 11))  # 1-10

LEVEL_LABELS = {i: f"Nivel {i}" for i in LEVELS}

# ===== XP Y GAMIFICACIÓN =====

XP_PER_LEVEL = 100  # XP requeridos para subir de nivel

XP_REWARDS = {
    "flashcard_again": 1,
    "flashcard_hard": 3,
    "flashcard_good": 5,
    "flashcard_easy": 10,
    "declension_correct": 5,
    "conjugation_correct": 5,
    "analysis_correct": 10,
    "challenge_perfect": 50,
    "challenge_good": 30,
    "challenge_passed": 20
}

# ===== TIPOS DE DESAFÍOS =====

CHALLENGE_TYPES = [
    "declension",
    "conjugation",
    "multiple_choice",
    "translation",
    "syntax",
    "sentence_order",
    "match_pairs"
]

CHALLENGE_TYPE_LABELS = {
    "declension": "Declinación",
    "conjugation": "Conjugación",
    "multiple_choice": "Opción Múltiple",
    "translation": "Traducción",
    "syntax": "Análisis Sintáctico",
    "sentence_order": "Ordenar Palabras",
    "match_pairs": "Emparejar"
}

# ===== CONFIGURACIÓN DE LA APLICACIÓN =====

APP_NAME = "Lingua Latina Viva"
APP_VERSION = "1.0.0"
DEFAULT_LANGUAGE = "es"

# Temas de color (para futuras mejoras)
COLORS = {
    "primary": "#8B4513",  # Sienna (marrón romano)
    "secondary": "#A0522D",  # Sienna oscuro
    "accent": "#CD853F",  # Peru
    "background": "#1E1E1E",  # Gris oscuro
    "text": "#E8E8E8",  # Gris claro
    "success": "#4CAF50",
    "error": "#F44336",
    "warning": "#FF9800",
    "info": "#2196F3"
}

# ===== CONFIGURACIÓN DE SRS (Spaced Repetition System) =====

SRS_QUALITY_LABELS = {
    0: "Nuevamente",
    2: "Difícil",
    4: "Bien",
    5: "Fácil"
}

SRS_MIN_EASE_FACTOR = 1.3
SRS_DEFAULT_EASE_FACTOR = 2.5

# ===== RUTAS DE ARCHIVOS =====

DB_PATH = "lingua_latina.db"
BACKUP_DIR = "backups"
DATA_DIR = "data"
ASSETS_DIR = "assets"
