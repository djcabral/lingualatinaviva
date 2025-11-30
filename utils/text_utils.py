"""
Text Utilities
Funciones para procesamiento y normalización de texto latino.
"""
import unicodedata
import re
from typing import Optional


def normalize_latin(text: str) -> str:
    """
    Remueve macrones y diacríticos del texto latino para permitir comparación
    insensible a acentos.
    
    Args:
        text: Texto latino con posibles macrones
        
    Returns:
        Texto normalizado sin macrones
        
    Examples:
        >>> normalize_latin("puella")
        'puella'
        >>> normalize_latin("puellā")
        'puella'
    """
    if not text:
        return text
    
    # Normalizar a NFD (forma descompuesta)
    normalized = unicodedata.normalize('NFD', text)
    
    # Remover caracteres de combinación (macrones, etc.)
    return ''.join(char for char in normalized if unicodedata.category(char) != 'Mn')


def clean_latin_input(text: str) -> str:
    """
    Limpia y normaliza la entrada del usuario.
    
    Args:
        text: Texto ingresado por el usuario
        
    Returns:
        Texto limpio y normalizado
    """
    if not text:
        return ""
    
    # Remover espacios extras al inicio y final
    text = text.strip()
    
    # Normalizar macrones
    text = normalize_latin(text)
    
    # Convertir a minúsculas para comparación
    text = text.lower()
    
    return text


def is_homograph(word: str) -> bool:
    """
    Detecta si una palabra es un homógrafo (contiene dígitos para desambiguación).
    
    Args:
        word: Palabra latina
        
    Returns:
        True si contiene dígitos, False en caso contrario
        
    Examples:
        >>> is_homograph("dico")
        False
        >>> is_homograph("dico1")
        True
    """
    return any(char.isdigit() for char in word)


def remove_homograph_digits(word: str) -> str:
    """
    Remueve dígitos de desambiguación de homógrafos.
    
    Args:
        word: Palabra latina con posibles dígitos
        
    Returns:
        Palabra sin dígitos
        
    Examples:
        >>> remove_homograph_digits("dico1")
        'dico'
        >>> remove_homograph_digits("amo")
        'amo'
    """
    return ''.join(char for char in word if not char.isdigit())


def get_disambiguation_hint(word_data: dict) -> str:
    """
    Genera un hint de desambiguación para homógrafos basado en la información morfológica.
    
    Args:
        word_data: Diccionario con datos de la palabra (part_of_speech, conjugation, genitive, etc.)
        
    Returns:
        String con el hint de desambiguación o vacío si no aplica
        
    Examples:
        >>> get_disambiguation_hint({'part_of_speech': 'verb', 'conjugation': '1'})
        '(1ª conj.)'
        >>> get_disambiguation_hint({'part_of_speech': 'noun', 'genitive': 'regis'})
        '(Gen: regis)'
    """
    pos = word_data.get('part_of_speech', '')
    
    if pos == 'verb':
        conjugation = word_data.get('conjugation')
        if conjugation:
            return f"({conjugation}ª conj.)"
        
        principal_parts = word_data.get('principal_parts', '')
        if principal_parts:
            parts = principal_parts.split(', ')
            if len(parts) >= 2:
                return f"({parts[1]})"
            return f"({principal_parts})"
    
    elif pos == 'noun':
        genitive = word_data.get('genitive')
        if genitive:
            return f"(Gen: {genitive})"
        
        declension = word_data.get('declension')
        if declension:
            return f"({declension}ª decl.)"
    
    elif pos == 'adjective':
        genitive = word_data.get('genitive')
        if genitive:
            return f"({genitive})"
    
    return ""


def display_word_with_disambiguation(word: str, word_data: dict = None) -> tuple[str, str]:
    """
    Prepara una palabra para mostrar, manejando homógrafos.
    
    Args:
        word: Palabra latina (puede contener dígitos)
        word_data: Datos morfológicos de la palabra (opcional)
        
    Returns:
        Tupla (palabra_limpia, hint_desambiguacion)
        
    Examples:
        >>> display_word_with_disambiguation("puella")
        ('puella', '')
        >>> display_word_with_disambiguation("dico1", {'part_of_speech': 'verb', 'conjugation': '1'})
        ('dico', '(1ª conj.)')
    """
    if is_homograph(word):
        clean_word = remove_homograph_digits(word)
        hint = ""
        
        if word_data:
            hint = get_disambiguation_hint(word_data)
        
        return clean_word, hint
    
    return word, ""


def extract_latin_words(text: str) -> list[str]:
    """
    Extrae palabras latinas de un texto.
    
    Args:
        text: Texto que puede contener palabras latinas y puntuación
        
    Returns:
        Lista de palabras latinas (sin puntuación)
    """
    # Patrón para palabras latinas (incluye macrones)
    pattern = r'[a-zA-ZāēīōūĀĒĪŌŪ]+'
    words = re.findall(pattern, text)
    return [w for w in words if w]


def compare_latin_words(word1: str, word2: str, case_sensitive: bool = False) -> bool:
    """
    Compara dos palabras latinas, normalizando macrones.
    
    Args:
        word1: Primera palabra
        word2: Segunda palabra
        case_sensitive: Si True, la comparación es sensible a mayúsculas
        
    Returns:
        True si las palabras son iguales (ignorando macrones)
    """
    w1 = normalize_latin(word1)
    w2 = normalize_latin(word2)
    
    if not case_sensitive:
        w1 = w1.lower()
        w2 = w2.lower()
    
    return w1 == w2
