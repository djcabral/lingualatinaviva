import json
from typing import Dict, List, Optional, Any
from database import Word, SentenceAnalysis

class HintService:
    """
    Servicio para generar pistas contextuales progresivas para ejercicios de traducción.
    """
    
    @staticmethod
    def get_morphological_hint(word_text: str, analysis_data: Dict[str, Any]) -> str:
        """
        Genera una pista morfológica basada en el análisis del token.
        Nivel 1: Identificación básica (Categoría + Rasgos principales)
        """
        # Intentar buscar en el análisis manual primero si existe
        # TODO: Implementar lógica más compleja con spaCy si es necesario
        
        # Por ahora, simulamos lógica basada en terminaciones comunes (heurística simple)
        # En una implementación real, esto usaría los datos de `dependency_json`
        
        lower_word = word_text.lower().strip(".,?!")
        
        if lower_word.endswith("am"):
            return "Sustantivo/Adjetivo en Acusativo Singular (Objeto Directo)"
        elif lower_word.endswith("um"):
            return "Sustantivo/Adjetivo en Nominativo/Acusativo Neutro o Acusativo Masculino"
        elif lower_word.endswith("ae"):
            return "Genitivo/Dativo Singular o Nominativo Plural (1ª Declinación)"
        elif lower_word.endswith("i"):
            return "Genitivo Singular o Nominativo Plural (2ª Declinación)"
        elif lower_word.endswith("t"):
            return "Verbo en 3ª Persona Singular"
        elif lower_word.endswith("nt"):
            return "Verbo en 3ª Persona Plural"
        
        return "Analiza la terminación para deducir el caso o persona."

    @staticmethod
    def get_syntactic_hint(word_text: str, sentence: SentenceAnalysis) -> str:
        """
        Genera una pista sintáctica basada en el rol de la palabra en la oración.
        Nivel 2: Función sintáctica
        """
        try:
            roles = json.loads(sentence.syntax_roles)
            # roles structure example: {"subject": ["puer"], "object": ["rosam"], "verb": ["amat"]}
            # Note: This implies syntax_roles stores lists of words or indices. 
            # Let's assume for now it might store snippets or we need to fuzzy match.
            
            lower_word = word_text.lower().strip(".,?!")
            
            for role, words in roles.items():
                # Check if word is in the list for this role
                # This is a simplification; ideally we use indices from dependency_json
                if any(lower_word in w.lower() for w in words if isinstance(w, str)):
                    role_map = {
                        "subject": "Sujeto (quién realiza la acción)",
                        "object": "Objeto Directo (quién recibe la acción)",
                        "direct_object": "Objeto Directo (quién recibe la acción)",
                        "indirect_object": "Objeto Indirecto (destinatario)",
                        "verb": "Núcleo del Predicado (acción)",
                        "attribute": "Atributo (cualidad del sujeto)",
                        "adverbial": "Circunstancial (contexto)",
                        "adverb": "Adverbio (modifica al verbo)",
                        "prepositional_phrase": "Frase Preposicional (circunstancia)",
                        "agent": "Agente (quién realiza la acción en pasiva)",
                        "ablative_absolute": "Ablativo Absoluto (contexto independiente)",
                        "subject_accusative": "Sujeto de Infinitivo (en oraciones AcI)",
                        "attribute_accusative": "Atributo en Acusativo (en oraciones AcI)",
                        "conjunction": "Conjunción (nexo)",
                        "coordinator": "Coordinante (une elementos)",
                        "negative": "Negación",
                        "infinitive": "Infinitivo (verbo sustantivado)"
                    }
                    return role_map.get(role, f"Cumple la función de {role}")
                    
            return "Observa su relación con el verbo principal."
            
        except Exception as e:
            return "Pista sintáctica no disponible."

    @staticmethod
    def get_dictionary_hint(word_text: str, session) -> str:
        """
        Genera una pista de diccionario (significado base).
        Nivel 3: Significado
        """
        from sqlmodel import select
        # Simple lookup logic
        # In reality, we need lemmatization to find 'rosam' -> 'rosa'
        # For now, we rely on the database having the exact form or we need a lemmatizer.
        # Let's try to find a partial match or use a known lemma if available in analysis.
        
        # Fallback: search exact match first
        word = session.exec(select(Word).where(Word.latin == word_text.lower().strip(".,?!"))).first()
        if word:
            # Preferir traducción en español
            spanish_translation = word.definition_es or word.translation
            return f"Significa: {spanish_translation}"
            
        return "Consulta el vocabulario de la lección."


def detect_sentence_type(latin_text: str) -> str:
    """
    Detecta el tipo de oración latina.
    
    Args:
        latin_text: Texto de la oración en latín
        
    Returns:
        'simple', 'coordinada', o 'subordinada'
    """
    text_lower = latin_text.lower()
    
    # Palabras subordinantes comunes
    subordinating_words = [
        'qui', 'quae', 'quod',  # Pronombres relativos
        'cum',  # Cuando/con
        'ut', 'ne',  # Para que/que no
        'si', 'nisi',  # Si/si no
        'quia', 'quoniam',  # Porque
        'dum', 'donec',  # Mientras/hasta que
        'antequam', 'priusquam',  # Antes de que
        'postquam',  # Después de que
        'licet', 'quamquam'  # Aunque
    ]
    
    # Conjunciones coordinantes
    coordinating_conj = [' et ', ' sed ', ' aut ', ' vel ', ' neque ', ' atque ']
    
    # Verificar subordinadas (prioridad alta)
    for word in subordinating_words:
        if f' {word} ' in f' {text_lower} ' or text_lower.startswith(f'{word} '):
            return 'subordinada'
    
    # Verificar coordinadas
    for conj in coordinating_conj:
        if conj in f' {text_lower} ':
            return 'coordinada'
    
    # Por defecto, simple
    return 'simple'


def get_translation_guide_path(sentence_type: str) -> str:
    """
    Obtiene la ruta de la infografía según el tipo de oración.
    
    Args:
        sentence_type: Tipo de oración
        
    Returns:
        Ruta relativa a la infografía
    """
    guides = {
        'simple': 'static/images/translation_guides/oraciones_simples_guia.png',
        'coordinada': 'static/images/translation_guides/oraciones_coordinadas_guia.png',
        'subordinada': 'static/images/translation_guides/oraciones_subordinadas_guia.png'
    }
    
    return guides.get(sentence_type, '')


def generate_structure_hints(sentence_type: str) -> List[str]:
    """
    Genera hints de estrategia según el tipo de oración.
    
    Args:
        sentence_type: Tipo de oración ('simple', 'coordinada', 'subordinada')
        
    Returns:
        Lista de pasos recomendados para traducir
    """
    hints = {
        'simple': [
            '1️⃣ Busca el VERBO principal (palabra conjugada)',
            '2️⃣ Identifica el SUJETO (palabra en nominativo)',
            '3️⃣ Busca los COMPLEMENTOS (acusativo, dativo, ablativo)',
            '4️⃣ Ordena en español: Sujeto + Verbo + Complementos'
        ],
        'coordinada': [
            '1️⃣ Identifica la CONJUNCIÓN (et, sed, aut)',
            '2️⃣ Separa las dos PROPOSICIONES',
            '3️⃣ Traduce cada proposición POR SEPARADO',
            '4️⃣ Une con la conjunción en español'
        ],
        'subordinada': [
            '1️⃣ Identifica la PALABRA SUBORDINANTE (qui, cum, ut, si)',
            '2️⃣ Separa la oración PRINCIPAL de la SUBORDINADA',
            '3️⃣ Traduce primero la oración PRINCIPAL',
            '4️⃣ Traduce la subordinada e INTÉGRALA'
        ]
    }
    
    return hints.get(sentence_type, ['Analiza la estructura de la oración'])

