"""
Wrapper para PyCollatinus adaptado a latin-python

Este módulo proporciona una interfaz simplificada y en español para PyCollatinus,
el analizador morfológico de latín portado desde Collatinus C++.

Características:
- Resultados traducidos al español
- Interfaz simplificada
- Sistema de caché para optimización
- Compatibilidad con Python 3.11+

Autor: Adaptado para latin-python
Licencia: GNU GPL v3 (mismo que Collatinus/PyCollatinus)
"""

from typing import List, Dict, Optional, Tuple
import os
import pickle
from functools import lru_cache


# Diccionario de traducción de morfología francés → español
MORPH_TRANSLATION = {
    # Números
    "singulier": "singular",
    "pluriel": "plural",
    
    # Personas
    "1ère": "1ª",
    "2ème": "2ª",
    "3ème": "3ª",
    
    # Modos verbales
    "indicatif": "indicativo",
    "subjonctif": "subjuntivo",
    "impératif": "imperativo",
    "infinitif": "infinitivo",
    "participe": "participio",
    "gérondif": "gerundio",
    "supin": "supino",
    
    # Tiempos
    "présent": "presente",
    "imparfait": "imperfecto",
    "futur": "futuro",
    "parfait": "perfecto",
    "plus-que-parfait": "pluscuamperfecto",
    
    # Voces
    "actif": "activo",
    "passif": "pasivo",
    
    # Géneros
    "masculin": "masculino",
    "féminin": "femenino",
    "neutre": "neutro",
    
    # Casos
    "nominatif": "nominativo",
    "vocatif": "vocativo",
    "accusatif": "acusativo",
    "génitif": "genitivo",
    "datif": "dativo",
    "ablatif": "ablativo",
    "locatif": "locativo",
    
    # Grados
    "positif": "positivo",
    "comparatif": "comparativo",
    "superlatif": "superlativo",
}


class LatinMorphologyAnalyzer:
    """
    Analizador morfológico de latín usando PyCollatinus
    
    Esta clase proporciona una interfaz en español para el análisis morfológico
    de textos en latín, incluyendo lematización y análisis gramatical completo.
    """
    
    def __init__(self, use_compiled: bool = True, auto_fix_compatibility: bool = True):
        """
        Inicializa el analizador morfológico
        
        Args:
            use_compiled: Si True, intenta usar versión compilada (más rápido)
            auto_fix_compatibility: Si True, aplica parche automático para Python 3.11+
        """
        self._analyzer = None
        self._use_compiled = use_compiled
        
        # Aplicar parche de compatibilidad si es necesario
        if auto_fix_compatibility:
            self._apply_compatibility_patch()
        
        # Inicializar PyCollatinus
        self._initialize_analyzer()
    
    def _apply_compatibility_patch(self):
        """
        Aplica parche de compatibilidad para Python 3.11+
        Corrige el import de Callable en PyCollatinus
        """
        try:
            import pycollatinus
            import sys
            
            # Solo aplicar en Python 3.9+
            if sys.version_info >= (3, 9):
                util_path = os.path.join(
                    os.path.dirname(pycollatinus.__file__),
                    'util.py'
                )
                
                if os.path.exists(util_path):
                    with open(util_path, 'r') as f:
                        content = f.read()
                    
                    # Verificar si necesita parche
                    if 'from collections import OrderedDict, Callable' in content:
                        # Aplicar parche
                        content = content.replace(
                            'from collections import OrderedDict, Callable',
                            'from collections import OrderedDict\nfrom collections.abc import Callable'
                        )
                        
                        with open(util_path, 'w') as f:
                            f.write(content)
                        
                        print("✓ Parche de compatibilidad Python 3.11+ aplicado")
        except Exception as e:
            print(f"⚠ Error aplicando parche de compatibilidad: {e}")
    
    def _initialize_analyzer(self):
        """Inicializa el lemmatizador de PyCollatinus"""
        try:
            from pycollatinus import Lemmatiseur
            
            if self._use_compiled:
                try:
                    # Intentar cargar versión compilada
                    self._analyzer = Lemmatiseur.load()
                    print("✓ Analizador morfológico cargado (compilado)")
                except:
                    # Si falla, usar versión normal y compilar
                    self._analyzer = Lemmatiseur()
                    try:
                        self._analyzer.compile()
                        print("✓ Analizador morfológico compilado para futuro uso")
                    except:
                        pass
                    print("✓ Analizador morfológico cargado (normal)")
            else:
                self._analyzer = Lemmatiseur()
                print("✓ Analizador morfológico cargado")
                
        except ImportError:
            raise ImportError(
                "PyCollatinus no está instalado. "
                "Instálalo con: pip install pycollatinus"
            )
    
    def translate_morphology(self, morph_fr: str) -> str:
        """
        Traduce la morfología del francés al español
        
        Args:
            morph_fr: Descripción morfológica en francés
            
        Returns:
            Descripción morfológica en español
        """
        morph_es = morph_fr
        
        # Aplicar traducciones
        for fr, es in MORPH_TRANSLATION.items():
            morph_es = morph_es.replace(fr, es)
        
        return morph_es
    
    @lru_cache(maxsize=1000)
    def analyze_word(self, word: str) -> List[Dict[str, str]]:
        """
        Analiza una palabra individual
        
        Args:
            word: Palabra en latín a analizar
            
        Returns:
            Lista de posibles análisis, cada uno con:
            - lemma: Lema (forma base)
            - morph: Descripción morfológica (en español)
            - morph_original: Descripción original (en francés)
            - radical: Raíz de la palabra
            - desinence: Desinencia
            - form: Forma analizada
        """
        if not self._analyzer:
            return []
        
        results = self._analyzer.lemmatise(word)
        
        if not results:
            return []
        
        # Traducir y formatear resultados
        translated_results = []
        for result in results:
            morph_fr = result.get('morph', '')
            translated_results.append({
                'lemma': result.get('lemma', ''),
                'morph': self.translate_morphology(morph_fr),
                'morph_original': morph_fr,
                'radical': result.get('radical', ''),
                'desinence': result.get('desinence', ''),
                'form': result.get('form', word)
            })
        
        return translated_results
    
    def analyze_text(self, text: str) -> List[Tuple[str, List[Dict[str, str]]]]:
        """
        Analiza un texto completo
        
        Args:
            text: Texto en latín (puede contener múltiples palabras)
            
        Returns:
            Lista de tuplas (palabra, análisis) para cada palabra del texto
        """
        if not self._analyzer:
            return []
        
        results = self._analyzer.lemmatise_multiple(text)
        words = text.split()
        
        analyzed = []
        for word, word_results in zip(words, results):
            if word_results:
                # Traducir resultados
                translated = [
                    {
                        'lemma': r.get('lemma', ''),
                        'morph': self.translate_morphology(r.get('morph', '')),
                        'morph_original': r.get('morph', ''),
                        'radical': r.get('radical', ''),
                        'desinence': r.get('desinence', ''),
                        'form': r.get('form', word)
                    }
                    for r in word_results
                ]
                analyzed.append((word, translated))
            else:
                analyzed.append((word, []))
        
        return analyzed
    
    def get_lemma(self, word: str) -> Optional[str]:
        """
        Obtiene el lema principal de una palabra
        
        Args:
            word: Palabra en latín
            
        Returns:
            El lema más probable, o None si no se encuentra
        """
        results = self.analyze_word(word)
        return results[0]['lemma'] if results else None
    
    def get_all_lemmas(self, word: str) -> List[str]:
        """
        Obtiene todos los posibles lemas de una palabra
        
        Args:
            word: Palabra en latín
            
        Returns:
            Lista de todos los posibles lemas
        """
        results = self.analyze_word(word)
        return list(set(r['lemma'] for r in results))
    
    def is_verb_form(self, word: str, lemma: Optional[str] = None) -> bool:
        """
        Verifica si una palabra es una forma verbal
        
        Args:
            word: Palabra a verificar
            lemma: Opcionalmente, verificar para un lema específico
            
        Returns:
            True si es forma verbal
        """
        results = self.analyze_word(word)
        
        for result in results:
            if lemma and result['lemma'] != lemma:
                continue
            
            morph = result['morph'].lower()
            verb_indicators = ['indicativo', 'subjuntivo', 'imperativo', 'infinitivo', 'gerundio']
            
            if any(indicator in morph for indicator in verb_indicators):
                return True
        
        return False
    
    def get_verb_info(self, word: str, lemma: Optional[str] = None) -> Optional[Dict[str, str]]:
        """
        Obtiene información verbal específica
        
        Args:
            word: Forma verbal
            lemma: Opcionalmente, analizar para un lema específico
            
        Returns:
            Diccionario con información verbal o None
        """
        results = self.analyze_word(word)
        
        for result in results:
            if lemma and result['lemma'] != lemma:
                continue
            
            if self.is_verb_form(word, result['lemma']):
                # Parsear la morfología
                morph = result['morph'].lower()
                
                info = {
                    'lemma': result['lemma'],
                    'form': result['form'],
                    'radical': result['radical'],
                    'desinence': result['desinence'],
                    'morph_full': result['morph'],
                }
                
                # Extraer información específica
                for person in ['1ª', '2ª', '3ª']:
                    if person in morph:
                        info['person'] = person
                
                for number in ['singular', 'plural']:
                    if number in morph:
                        info['number'] = number
                
                for mood in ['indicativo', 'subjuntivo', 'imperativo', 'infinitivo']:
                    if mood in morph:
                        info['mood'] = mood
                
                for tense in ['presente', 'imperfecto', 'futuro', 'perfecto', 'pluscuamperfecto']:
                    if tense in morph:
                        info['tense'] = tense
                
                for voice in ['activo', 'pasivo']:
                    if voice in morph:
                        info['voice'] = voice
                
                return info
        
        return None
    
    def format_analysis(self, word: str, detailed: bool = False) -> str:
        """
        Formatea el análisis de una palabra para mostrar al usuario
        
        Args:
            word: Palabra a analizar
            detailed: Si True, incluye detalles completos
            
        Returns:
            Texto formateado con el análisis
        """
        results = self.analyze_word(word)
        
        if not results:
            return f"'{word}': No se encontró análisis"
        
        output = [f"'{word}':"]
        
        for i, result in enumerate(results, 1):
            if detailed:
                output.append(f"  {i}. Lema: {result['lemma']}")
                output.append(f"     Morfología: {result['morph']}")
                output.append(f"     Radical: {result['radical']}, Desinencia: {result['desinence']}")
            else:
                output.append(f"  {i}. {result['lemma']} - {result['morph']}")
        
        return "\n".join(output)


# Instancia global (lazy loading)
_global_analyzer: Optional[LatinMorphologyAnalyzer] = None


def get_analyzer() -> LatinMorphologyAnalyzer:
    """
    Obtiene la instancia global del analizador (patrón Singleton)
    
    Returns:
        Instancia del analizador morfológico
    """
    global _global_analyzer
    
    if _global_analyzer is None:
        _global_analyzer = LatinMorphologyAnalyzer()
    
    return _global_analyzer


# Funciones de conveniencia
def analyze(word: str) -> List[Dict[str, str]]:
    """Analiza una palabra (función de conveniencia)"""
    return get_analyzer().analyze_word(word)


def lemmatize(word: str) -> Optional[str]:
    """Obtiene el lema de una palabra (función de conveniencia)"""
    return get_analyzer().get_lemma(word)


def analyze_text(text: str) -> List[Tuple[str, List[Dict[str, str]]]]:
    """Analiza un texto (función de conveniencia)"""
    return get_analyzer().analyze_text(text)


if __name__ == "__main__":
    # Demo
    print("=" * 60)
    print("DEMO: Latin Morphology Analyzer")
    print("=" * 60)
    
    analyzer = LatinMorphologyAnalyzer()
    
    # Test palabras simples
    test_words = ["rosa", "amo", "cogito", "sum", "veni"]
    
    for word in test_words:
        print(f"\n{analyzer.format_analysis(word, detailed=True)}")
    
    # Test texto
    print("\n" + "=" * 60)
    print("Análisis de texto: 'Cogito ergo sum'")
    print("=" * 60)
    
    text_results = analyzer.analyze_text("Cogito ergo sum")
    for word, analyses in text_results:
        print(f"\n{word}:")
        for analysis in analyses[:2]:  # Mostrar solo primeras 2
            print(f"  - {analysis['lemma']}: {analysis['morph']}")
