"""
Adaptador para PyCollatinus (Motor de morfología latina)

Este módulo proporciona una interfaz de alto nivel para PyCollatinus,
manejando la carga eficiente del modelo (Singleton), la traducción
de etiquetas del francés al español y la simplificación de la salida.
"""

import os
import pickle
import sys
from typing import List, Dict, Optional, Any

# Intentar importar pycollatinus, manejar error si no está instalado
# Intentar importar pycollatinus, manejar error si no está instalado
try:
    # Parche para compatibilidad con Python 3.10+ (pycollatinus usa collections.Callable)
    import collections
    import collections.abc
    if not hasattr(collections, 'Callable'):
        collections.Callable = collections.abc.Callable

    from pycollatinus import Lemmatiseur
    PYCOLLATINUS_AVAILABLE = True
except ImportError:
    PYCOLLATINUS_AVAILABLE = False

class LatinMorphAnalyzer:
    """
    Wrapper para el lemmatizador de Collatinus.
    Implementa patrón Singleton para cargar los datos una sola vez.
    """
    _instance = None
    _analyzer = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LatinMorphAnalyzer, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Evitar re-inicialización si ya existe
        if self._analyzer is not None:
            return

        if not PYCOLLATINUS_AVAILABLE:
            print("⚠️ PyCollatinus no está instalado. Funcionalidad limitada.")
            return

        try:
            # Intentar cargar versión compilada primero (más rápido ~3s vs ~5s)
            compiled_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'collatinus_compiled.pickle')
            
            if os.path.exists(compiled_path):
                print(f"📦 Cargando PyCollatinus compilado desde {compiled_path}...")
                try:
                    self._analyzer = Lemmatiseur.load(compiled_path)
                    print("✅ PyCollatinus compilado cargado exitosamente")
                except Exception as e:
                    print(f"⚠️ Error cargando versión compilada: {e}")
                    print("Cargando versión estándar...")
                    self._analyzer = Lemmatiseur()
            else:
                print("📚 Cargando PyCollatinus (primera vez, puede tardar unos segundos)...")
                self._analyzer = Lemmatiseur()
                
                # Compilar para futuras cargas
                print("🔧 Compilando PyCollatinus para futuras cargas...")
                try:
                    os.makedirs(os.path.dirname(compiled_path), exist_ok=True)
                    # compile() no acepta argumentos, guarda en su propia ubicación
                    self._analyzer.compile()
                    # Intentar copiar el archivo compilado a nuestra ubicación
                    import shutil
                    default_compiled = self._analyzer.path('compiled.pickle')
                    if os.path.exists(default_compiled):
                        shutil.copy(default_compiled, compiled_path)
                        print(f"✅ PyCollatinus compilado guardado en {compiled_path}")
                except Exception as e:
                    print(f"⚠️ No se pudo compilar: {e}")

            
            # Mapeo de traducción Francés -> Español
            self.translations = {
                # Casos
                'nominatif': 'Nominativo',
                'vocatif': 'Vocativo',
                'accusatif': 'Acusativo',
                'génitif': 'Genitivo',
                'datif': 'Dativo',
                'ablatif': 'Ablativo',
                'locatif': 'Locativo',
                
                # Números
                'singulier': 'Singular',
                'pluriel': 'Plural',
                
                # Géneros
                'masculin': 'Masculino',
                'féminin': 'Femenino',
                'neutre': 'Neutro',
                
                # Personas
                '1ère': '1ª Persona',
                '2ème': '2ª Persona',
                '3ème': '3ª Persona',
                
                # Tiempos
                'présent': 'Presente',
                'imparfait': 'Imperfecto',
                'futur': 'Futuro',
                'parfait': 'Perfecto',
                'plus-que-parfait': 'Pluscuamperfecto',
                'futur antérieur': 'Futuro Perfecto',
                
                # Modos
                'indicatif': 'Indicativo',
                'subjonctif': 'Subjuntivo',
                'impératif': 'Imperativo',
                'infinitif': 'Infinitivo',
                'participe': 'Participio',
                'gérondif': 'Gerundio',
                'supin': 'Supino',
                
                # Voces
                'actif': 'Activa',
                'passif': 'Pasiva',
                'déponent': 'Deponente',
                
                # Grados
                'positif': 'Positivo',
                'comparatif': 'Comparativo',
                'superlatif': 'Superlativo',
                
                # Otros
                'adjectif': 'Adjetivo',
                'adverbe': 'Adverbio',
                'préposition': 'Preposición',
                'conjonction': 'Conjunción',
                'interjection': 'Interjección',
                'numéral': 'Numeral',
                'pronom': 'Pronombre',
            }
            
        except Exception as e:
            print(f"❌ Error inicializando PyCollatinus: {e}")
            self._analyzer = None

    def is_ready(self) -> bool:
        """Verifica si el analizador está listo para usarse"""
        return self._analyzer is not None

    def _translate_morph(self, morph_str: str) -> str:
        """Traduce la cadena de morfología del francés al español"""
        if not morph_str:
            return ""
            
        words = morph_str.split()
        translated_words = []
        
        for word in words:
            # Limpiar puntuación si es necesario, aunque Collatinus suele dar limpio
            clean_word = word.lower()
            if clean_word in self.translations:
                translated_words.append(self.translations[clean_word])
            else:
                # Mantener palabra original si no hay traducción (ej. palabras desconocidas)
                translated_words.append(word)
                
        return " ".join(translated_words)

    def analyze_word(self, word: str) -> List[Dict[str, Any]]:
        """
        Analiza una palabra latina y devuelve todas sus posibles formas.
        
        Args:
            word: Palabra en latín
            
        Returns:
            Lista de diccionarios con lema, morfología (traducida) y detalles
        """
        if not self.is_ready():
            return []
            
        try:
            raw_results = self._analyzer.lemmatise(word)
            processed_results = []
            
            for res in raw_results:
                processed_results.append({
                    'lemma': res.get('lemma', ''),
                    'morph_raw': res.get('morph', ''),
                    'morph': self._translate_morph(res.get('morph', '')),
                    'radical': res.get('radical', ''),
                    'desinence': res.get('desinence', '')
                })
                
            return processed_results
            
        except Exception as e:
            print(f"Error analizando '{word}': {e}")
            return []

    def analyze_phrase(self, phrase: str) -> List[Dict[str, Any]]:
        """
        Analiza una frase completa token por token.
        
        Args:
            phrase: Frase en latín
            
        Returns:
            Lista de resultados por palabra
        """
        if not self.is_ready():
            return []
            
        try:
            # Collatinus tiene lemmatise_multiple para frases
            raw_results_list = self._analyzer.lemmatise_multiple(phrase)
            words = phrase.split() # Tokenización simple de Collatinus
            
            final_output = []
            
            for i, word_results in enumerate(raw_results_list):
                word_text = words[i] if i < len(words) else "?"
                
                word_analyses = []
                for res in word_results:
                    word_analyses.append({
                        'lemma': res.get('lemma', ''),
                        'morph': self._translate_morph(res.get('morph', '')),
                        'raw': res
                    })
                
                final_output.append({
                    'word': word_text,
                    'analyses': word_analyses
                })
                
            return final_output
            
        except Exception as e:
            print(f"Error analizando frase: {e}")
            return []

    def generate_paradigm(self, word: str) -> Dict[str, Any]:
        """
        Genera el paradigma completo (tabla de conjugación/declinación) para una palabra.
        
        Args:
            word: Palabra en latín (lema)
            
        Returns:
            Diccionario con:
                - lemma: el lema
                - model: nombre del modelo de flexión
                - forms: lista de todas las formas con morfología traducida
        """
        if not self.is_ready():
            return {}
            
        try:
            # Obtener el objeto Lemme
            lemma_obj = self._analyzer.lemme(word)
            if not lemma_obj:
                return {'error': f"Lema '{word}' no encontrado"}
            
            # Obtener el modelo de flexión
            model = lemma_obj.modele()
            
            # Obtener todas las desinencias
            desinences = model.desinences()
            
            forms = []
            
            for d in desinences:
                # Obtener el sufijo
                suffix = d.gr()
                
                # Obtener el índice del radical
                rad_idx = d.numRad()
                
                # Obtener el ID de morfología
                morph_id = d.morphoNum()
                
                # Obtener el radical
                radicals = lemma_obj.radical(rad_idx)
                if radicals:
                    stem = radicals[0].gr()
                else:
                    stem = ""
                
                # Construir la forma completa
                full_form = stem + suffix
                
                # Obtener y traducir la morfología
                morph_raw = self._analyzer.morpho(morph_id)
                morph_translated = self._translate_morph(morph_raw)
                
                forms.append({
                    'form': full_form,
                    'morph': morph_translated,
                    'morph_raw': morph_raw,
                    'stem': stem,
                    'suffix': suffix
                })
            
            return {
                'lemma': word,
                'model': str(model),
                'total_forms': len(forms),
                'forms': forms
            }
            
        except Exception as e:
            print(f"Error generando paradigma para '{word}': {e}")
            return {'error': str(e)}

# Instancia global para uso fácil
analyzer = LatinMorphAnalyzer()
