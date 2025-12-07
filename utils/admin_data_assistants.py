"""
MÓDULO DE ASISTENTES GUIADOS - Panel Admin

Asistentes interactivos para cargar datos en:
- Vocabulario (palabras)
- Oraciones (sentences)
- Textos (readings)

Con dos modos:
1. MANUAL - Ingreso manual de todos los datos
2. AUTOMÁTICO - Usando motores NLP y análisis de Collatinus

Filosofía: Guiar al usuario paso a paso, validando en cada etapa.
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import json
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# ENUMERACIONES
# ============================================================================

class AssistantMode(Enum):
    """Modos de asistencia disponibles"""
    MANUAL = "manual"           # Ingreso completamente manual
    SEMI_AUTO = "semi_auto"     # Manual con sugerencias NLP
    FULL_AUTO = "full_auto"     # Análisis automático completo


class DataType(Enum):
    """Tipos de datos que se pueden cargar"""
    VOCABULARY = "vocabulary"   # Palabras individuales
    SENTENCES = "sentences"     # Oraciones analizadas
    TEXTS = "texts"             # Textos completos


# ============================================================================
# DATACLASSES PARA PASOS DEL ASISTENTE
# ============================================================================

@dataclass
class AssistantStep:
    """Representa un paso en el asistente"""
    step_number: int
    title: str
    description: str
    fields: List[Dict[str, Any]]  # Campo: {name, type, required, help}
    validation_rules: Dict[str, callable] = None
    help_text: str = ""
    examples: List[str] = None


@dataclass
class VocabularyWizardData:
    """Datos recolectados durante el asistente de vocabulario"""
    # Paso 1: Información básica
    latin_word: str = ""
    translation: str = ""
    part_of_speech: str = ""  # noun, verb, adjective, adverb, preposition, etc.
    level: int = 1
    
    # Paso 2: Información morfológica (según POS)
    genitive: str = ""  # Para sustantivos
    gender: str = ""    # Para sustantivos: m, f, n
    declension: str = ""  # Para sustantivos: 1-5
    principal_parts: str = ""  # Para verbos
    conjugation: str = ""  # Para verbos: 1-4, irregular
    
    # Paso 3: Formas irregulares (JSON)
    irregular_forms: str = ""
    
    # Paso 4: Contexto y notas
    contexts: List[str] = None  # Ejemplos de uso en textos
    notes: str = ""
    source: str = ""  # Collatinus, manual, etc.
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario para BD"""
        return {
            'latin': self.latin_word,
            'translation': self.translation,
            'part_of_speech': self.part_of_speech,
            'level': self.level,
            'genitive': self.genitive if self.genitive else None,
            'gender': self.gender if self.gender else None,
            'declension': self.declension if self.declension else None,
            'principal_parts': self.principal_parts if self.principal_parts else None,
            'conjugation': self.conjugation if self.conjugation else None,
            'irregular_forms': self.irregular_forms if self.irregular_forms else None,
        }


@dataclass
class SentenceWizardData:
    """Datos recolectados durante el asistente de oraciones"""
    latin_text: str = ""
    translation: str = ""
    level: int = 1
    source_text_id: Optional[int] = None
    
    # Análisis sintáctico
    syntax_analysis: Dict[str, Any] = None  # Estructura sintáctica
    word_annotations: List[Dict] = None  # Anotaciones por palabra
    
    # Metadata
    tags: List[str] = None
    grammar_focus: List[str] = None  # Temas gramaticales: ablativo, subjuntivo, etc.
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario para BD"""
        return {
            'text': self.latin_text,
            'translation': self.translation,
            'difficulty': self.level,
            'source_text_id': self.source_text_id,
            'syntax_analysis': json.dumps(self.syntax_analysis) if self.syntax_analysis else None,
            'grammar_focus': json.dumps(self.grammar_focus) if self.grammar_focus else None,
        }


@dataclass
class TextWizardData:
    """Datos recolectados durante el asistente de textos"""
    title: str = ""
    author: str = ""
    content: str = ""
    difficulty: int = 1
    
    # Metadata
    book_number: Optional[int] = None
    chapter_number: Optional[int] = None
    source_type: str = ""  # original, adapted, etc.
    
    # Análisis
    vocabulary_coverage: Dict[str, float] = None  # {level: porcentaje}
    estimated_reading_time: Optional[int] = None  # minutos
    grammar_topics: List[str] = None
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario para BD"""
        return {
            'title': self.title,
            'author': self.author,
            'content': self.content,
            'difficulty': self.difficulty,
            'book_number': self.book_number,
            'chapter_number': self.chapter_number,
        }


# ============================================================================
# ASISTENTE BASE
# ============================================================================

class BaseAssistant:
    """Clase base para asistentes de carga de datos"""
    
    def __init__(self, mode: AssistantMode = AssistantMode.MANUAL):
        self.mode = mode
        self.current_step = 0
        self.steps: List[AssistantStep] = []
        self.data = {}
    
    def get_current_step(self) -> Optional[AssistantStep]:
        """Obtiene el paso actual del asistente"""
        if 0 <= self.current_step < len(self.steps):
            return self.steps[self.current_step]
        return None
    
    def has_next_step(self) -> bool:
        """Verifica si hay más pasos"""
        return self.current_step < len(self.steps) - 1
    
    def has_previous_step(self) -> bool:
        """Verifica si hay pasos anteriores"""
        return self.current_step > 0
    
    def next_step(self) -> bool:
        """Avanza al siguiente paso"""
        if self.has_next_step():
            self.current_step += 1
            return True
        return False
    
    def previous_step(self) -> bool:
        """Retrocede al paso anterior"""
        if self.has_previous_step():
            self.current_step -= 1
            return True
        return False
    
    def validate_step(self, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Valida los datos del paso actual
        
        Returns:
            (es_válido, lista_de_errores)
        """
        step = self.get_current_step()
        if not step:
            return False, ["No hay paso actual"]
        
        errors = []
        
        # Validar campos requeridos
        for field in step.fields:
            if field.get('required', False):
                if field['name'] not in data or not data[field['name']]:
                    errors.append(f"Campo requerido: {field['name']}")
        
        # Aplicar reglas de validación personalizadas
        if step.validation_rules:
            for field_name, validator in step.validation_rules.items():
                if field_name in data:
                    try:
                        if not validator(data[field_name]):
                            errors.append(f"Validación fallida para: {field_name}")
                    except Exception as e:
                        errors.append(f"Error validando {field_name}: {str(e)}")
        
        return len(errors) == 0, errors
    
    def save_step_data(self, data: Dict[str, Any]) -> None:
        """Guarda los datos del paso actual"""
        step = self.get_current_step()
        if step:
            self.data[f'step_{step.step_number}'] = data


# ============================================================================
# ASISTENTE DE VOCABULARIO
# ============================================================================

class VocabularyAssistant(BaseAssistant):
    """Asistente paso a paso para cargar vocabulario"""
    
    def __init__(self, mode: AssistantMode = AssistantMode.MANUAL):
        super().__init__(mode)
        self.wizard_data = VocabularyWizardData()
        self._setup_steps()
    
    def _setup_steps(self) -> None:
        """Configura los pasos del asistente"""
        
        # PASO 1: Información básica
        self.steps.append(AssistantStep(
            step_number=1,
            title="Información Básica de la Palabra",
            description="Ingresa los datos fundamentales de la palabra latina",
            fields=[
                {
                    'name': 'latin_word',
                    'type': 'text',
                    'required': True,
                    'help': 'Palabra en latín (forma diccionario)',
                    'placeholder': 'ej: puella, amare, magnus'
                },
                {
                    'name': 'translation',
                    'type': 'text',
                    'required': True,
                    'help': 'Traducción al español',
                    'placeholder': 'ej: niña, amar, grande'
                },
                {
                    'name': 'part_of_speech',
                    'type': 'select',
                    'required': True,
                    'options': ['noun', 'verb', 'adjective', 'adverb', 'preposition', 'pronoun', 'conjunction'],
                    'help': 'Categoría gramatical'
                },
                {
                    'name': 'level',
                    'type': 'number',
                    'required': True,
                    'min': 1,
                    'max': 10,
                    'value': 1,
                    'help': 'Nivel de dificultad (1-10)'
                }
            ],
            help_text="Los datos básicos son fundamentales. El programa usará esta información para categorizar la palabra.",
            examples=['puella, puellae (niña)', 'amare (amar)', 'magnus (grande)']
        ))
        
        # PASO 2: Información morfológica
        self.steps.append(AssistantStep(
            step_number=2,
            title="Información Morfológica",
            description="Detalles según la categoría gramatical",
            fields=[
                {
                    'name': 'genitive',
                    'type': 'text',
                    'required': False,
                    'help': 'Genitivo singular (para sustantivos)',
                    'visible_for_pos': ['noun']
                },
                {
                    'name': 'gender',
                    'type': 'select',
                    'required': False,
                    'options': ['m', 'f', 'n'],
                    'help': 'Género (para sustantivos)',
                    'visible_for_pos': ['noun']
                },
                {
                    'name': 'declension',
                    'type': 'select',
                    'required': False,
                    'options': ['1', '2', '3', '4', '5'],
                    'help': 'Declinación (para sustantivos)',
                    'visible_for_pos': ['noun']
                },
                {
                    'name': 'principal_parts',
                    'type': 'text',
                    'required': False,
                    'help': 'Partes principales (para verbos)',
                    'placeholder': 'ej: amo, amare, amavi, amatum',
                    'visible_for_pos': ['verb']
                },
                {
                    'name': 'conjugation',
                    'type': 'select',
                    'required': False,
                    'options': ['1', '2', '3', '4', 'irregular'],
                    'help': 'Conjugación (para verbos)',
                    'visible_for_pos': ['verb']
                }
            ],
            help_text="Esta información varía según la categoría gramatical. Solo completa los campos relevantes.",
        ))
        
        # PASO 3: Formas irregulares
        self.steps.append(AssistantStep(
            step_number=3,
            title="Formas Irregulares (Opcional)",
            description="Especifica formas irregulares o anómalas",
            fields=[
                {
                    'name': 'irregular_forms',
                    'type': 'textarea',
                    'required': False,
                    'help': 'JSON con formas irregulares',
                    'placeholder': '{"dat_pl": "filiābus", "abl_pl": "filiābus"}'
                }
            ],
            help_text="Usa JSON para especificar formas que no siguen la regla normal. Deja en blanco si no hay irregularidades.",
        ))
        
        # PASO 4: Contexto y fuente
        self.steps.append(AssistantStep(
            step_number=4,
            title="Contexto y Fuente",
            description="Información adicional sobre la palabra",
            fields=[
                {
                    'name': 'source',
                    'type': 'select',
                    'required': False,
                    'options': ['manual', 'collatinus', 'dictionary', 'text_context'],
                    'help': 'Fuente de la información'
                },
                {
                    'name': 'notes',
                    'type': 'textarea',
                    'required': False,
                    'help': 'Notas adicionales (etimología, usos comunes, etc.)'
                }
            ],
            help_text="Información extra para enriquecer la base de datos.",
        ))
    
    def get_visible_fields(self, pos: str) -> List[Dict]:
        """Obtiene solo los campos visibles para una categoría gramatical"""
        step = self.get_current_step()
        if not step:
            return []
        
        visible = []
        for field in step.fields:
            if 'visible_for_pos' not in field or pos in field.get('visible_for_pos', []):
                visible.append(field)
        return visible


# ============================================================================
# ASISTENTE DE ORACIONES
# ============================================================================

class SentenceAssistant(BaseAssistant):
    """Asistente paso a paso para cargar oraciones analizadas"""
    
    def __init__(self, mode: AssistantMode = AssistantMode.MANUAL):
        super().__init__(mode)
        self.wizard_data = SentenceWizardData()
        self._setup_steps()
    
    def _setup_steps(self) -> None:
        """Configura los pasos del asistente"""
        
        # PASO 1: Texto básico
        self.steps.append(AssistantStep(
            step_number=1,
            title="Oración en Latín",
            description="Ingresa la oración latina y su traducción",
            fields=[
                {
                    'name': 'latin_text',
                    'type': 'textarea',
                    'required': True,
                    'help': 'Oración en latín',
                    'placeholder': 'Magister discipulos in schola docet.'
                },
                {
                    'name': 'translation',
                    'type': 'textarea',
                    'required': True,
                    'help': 'Traducción al español',
                    'placeholder': 'El maestro enseña a los discípulos en la escuela.'
                },
                {
                    'name': 'level',
                    'type': 'number',
                    'required': True,
                    'min': 1,
                    'max': 10,
                    'value': 1,
                    'help': 'Nivel de dificultad'
                }
            ],
            help_text="Ingresa la oración exacta como aparece en el texto, sin modificaciones.",
        ))
        
        # PASO 2: Análisis sintáctico (automático o manual)
        self.steps.append(AssistantStep(
            step_number=2,
            title="Análisis Sintáctico",
            description="Estructura sintáctica de la oración",
            fields=[
                {
                    'name': 'main_clause_type',
                    'type': 'select',
                    'required': False,
                    'options': ['independent', 'main_with_subordinate', 'complex'],
                    'help': 'Tipo de cláusula principal'
                },
                {
                    'name': 'special_constructions',
                    'type': 'multiselect',
                    'required': False,
                    'options': ['accusative_infinitive', 'ablative_absolute', 'ut_clause', 'ablative_of_agent', 'dative_of_indirect_object'],
                    'help': 'Construcciones especiales presentes'
                }
            ],
            help_text="En modo automático, el programa analizará esto. En modo manual, especifica lo que reconozcas.",
        ))
        
        # PASO 3: Anotaciones de palabras
        self.steps.append(AssistantStep(
            step_number=3,
            title="Anotaciones Gramaticales",
            description="Etiquetas gramaticales por palabra",
            fields=[
                {
                    'name': 'grammar_focus',
                    'type': 'multiselect',
                    'required': False,
                    'options': [
                        'nominative', 'genitive', 'dative', 'accusative', 'ablative', 'vocative',
                        'present', 'imperfect', 'perfect', 'pluperfect', 'future',
                        'subjunctive', 'imperative', 'infinitive', 'participle',
                        'agreement', 'word_order', 'agreement_disagreement'
                    ],
                    'help': 'Temas gramaticales principales'
                }
            ],
            help_text="Marca los conceptos gramaticales que ilustra esta oración.",
        ))
    
    def analyze_with_nlp(self) -> Dict[str, Any]:
        """
        Usa el motor NLP para analizar la oración automáticamente
        (Requiere importar nlp_engine)
        """
        # Esto se integraría con el motor NLP del sistema
        # Por ahora es un stub
        return {
            'syntax': 'pending',
            'words': [],
            'grammar': []
        }


# ============================================================================
# ASISTENTE DE TEXTOS
# ============================================================================

class TextAssistant(BaseAssistant):
    """Asistente paso a paso para cargar textos completos"""
    
    def __init__(self, mode: AssistantMode = AssistantMode.MANUAL):
        super().__init__(mode)
        self.wizard_data = TextWizardData()
        self._setup_steps()
    
    def _setup_steps(self) -> None:
        """Configura los pasos del asistente"""
        
        # PASO 1: Metadatos básicos
        self.steps.append(AssistantStep(
            step_number=1,
            title="Información del Texto",
            description="Datos básicos del texto latino",
            fields=[
                {
                    'name': 'title',
                    'type': 'text',
                    'required': True,
                    'help': 'Título del texto',
                    'placeholder': 'ej: Fábula de la Hormiga y la Cigarra'
                },
                {
                    'name': 'author',
                    'type': 'text',
                    'required': True,
                    'help': 'Autor (si se conoce)',
                    'placeholder': 'ej: Fedro, Tito Livio'
                },
                {
                    'name': 'difficulty',
                    'type': 'number',
                    'required': True,
                    'min': 1,
                    'max': 10,
                    'value': 1,
                    'help': 'Nivel de dificultad (1-10)'
                }
            ],
            help_text="Información bibliográfica básica del texto.",
        ))
        
        # PASO 2: Contenido
        self.steps.append(AssistantStep(
            step_number=2,
            title="Contenido del Texto",
            description="El texto latino completo",
            fields=[
                {
                    'name': 'content',
                    'type': 'textarea',
                    'required': True,
                    'help': 'Texto latino completo',
                    'placeholder': 'Pega el texto aquí...'
                }
            ],
            help_text="El texto debe estar correctamente acentuado con macrones cuando sea necesario.",
        ))
        
        # PASO 3: Análisis de contenido
        self.steps.append(AssistantStep(
            step_number=3,
            title="Análisis de Contenido",
            description="Información sobre el contenido del texto",
            fields=[
                {
                    'name': 'source_type',
                    'type': 'select',
                    'required': False,
                    'options': ['original', 'adapted', 'simplified', 'excerpt'],
                    'help': 'Tipo de texto'
                },
                {
                    'name': 'book_number',
                    'type': 'number',
                    'required': False,
                    'help': 'Número de libro (si aplica)'
                },
                {
                    'name': 'chapter_number',
                    'type': 'number',
                    'required': False,
                    'help': 'Número de capítulo (si aplica)'
                }
            ],
            help_text="Información estructural del texto.",
        ))
        
        # PASO 4: Revisión y estadísticas
        self.steps.append(AssistantStep(
            step_number=4,
            title="Revisión Final",
            description="Verifica los datos antes de guardar",
            fields=[
                {
                    'name': 'confirm',
                    'type': 'checkbox',
                    'required': True,
                    'help': 'Confirmo que los datos son correctos'
                }
            ],
            help_text="Última oportunidad para revisar los datos antes de guardar.",
        ))
    
    def analyze_vocabulary_coverage(self) -> Dict[str, float]:
        """
        Analiza qué porcentaje del texto está cubierto por cada nivel
        (Requiere BD de vocabulario)
        """
        # Esto se integraría con el análisis del texto
        return {
            'level_1': 0.75,
            'level_2': 0.15,
            'level_3': 0.05,
            'unknown': 0.05
        }


# ============================================================================
# GESTOR DE ASISTENTES
# ============================================================================

class AssistantManager:
    """Gestor central para todos los asistentes"""
    
    def __init__(self):
        self.vocabulary_assistant: Optional[VocabularyAssistant] = None
        self.sentence_assistant: Optional[SentenceAssistant] = None
        self.text_assistant: Optional[TextAssistant] = None
    
    def create_vocabulary_assistant(self, mode: AssistantMode = AssistantMode.MANUAL) -> VocabularyAssistant:
        """Crea un nuevo asistente de vocabulario"""
        self.vocabulary_assistant = VocabularyAssistant(mode)
        return self.vocabulary_assistant
    
    def create_sentence_assistant(self, mode: AssistantMode = AssistantMode.MANUAL) -> SentenceAssistant:
        """Crea un nuevo asistente de oraciones"""
        self.sentence_assistant = SentenceAssistant(mode)
        return self.sentence_assistant
    
    def create_text_assistant(self, mode: AssistantMode = AssistantMode.MANUAL) -> TextAssistant:
        """Crea un nuevo asistente de textos"""
        self.text_assistant = TextAssistant(mode)
        return self.text_assistant


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def create_assistant(data_type: DataType, mode: AssistantMode = AssistantMode.MANUAL) -> BaseAssistant:
    """
    Factory para crear asistentes
    
    Args:
        data_type: Tipo de datos a cargar
        mode: Modo de asistencia
    
    Returns:
        Asistente configurado
    """
    if data_type == DataType.VOCABULARY:
        return VocabularyAssistant(mode)
    elif data_type == DataType.SENTENCES:
        return SentenceAssistant(mode)
    elif data_type == DataType.TEXTS:
        return TextAssistant(mode)
    else:
        raise ValueError(f"Tipo de datos desconocido: {data_type}")


__all__ = [
    'AssistantMode',
    'DataType',
    'VocabularyAssistant',
    'SentenceAssistant',
    'TextAssistant',
    'AssistantManager',
    'VocabularyWizardData',
    'SentenceWizardData',
    'TextWizardData',
    'create_assistant',
]
