from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
import json


class SentenceAnalysis(SQLModel, table=True):
    """Análisis sintáctico completo de una oración latina"""
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Contenido
    latin_text: str = Field(index=True)
    spanish_translation: str
    
    # Clasificación
    complexity_level: int = Field(default=1)  # 1-10
    sentence_type: str = Field(default="simple")  # "simple", "compound", "complex"
    source: str = Field(default="")  # "familia_romana_cap1", "caesar_gallia", etc.
    lesson_number: Optional[int] = None
    
    # Análisis LatinCy (JSON)
    # Árbol de dependencias completo: [{id, text, lemma, pos, dep, head, morph}, ...]
    dependency_json: str = Field(default="[]")
    
    # Funciones identificadas (JSON)
    # {"subject": [1,2], "predicate": [3], "object": [4,5], ...}
    syntax_roles: str = Field(default="{}")
    
    # Construcciones especiales detectadas (JSON array)
    # ["ablative_absolute", "accusative_infinitive", ...]
    constructions: Optional[str] = None
    
    # Diagrama SVG (pre-renderizado por displaCy)
    tree_diagram_svg: Optional[str] = None
    
    # Metadatos
    created_at: datetime = Field(default_factory=datetime.utcnow)
    verified: bool = Field(default=False)  # Revisión manual
    
    # Relaciones
    category_links: List["SentenceCategoryLink"] = Relationship(back_populates="sentence")
    token_annotations: List["TokenAnnotation"] = Relationship(back_populates="sentence")
    structures: List["SentenceStructure"] = Relationship(back_populates="sentence")


class SyntaxCategory(SQLModel, table=True):
    """Categorías para organizar el tesauro sintáctico"""
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)  # "Oraciones Simples", "Ablativo Absoluto", etc.
    parent_id: Optional[int] = None  # Para jerarquía de categorías
    complexity_level: int = Field(default=1)
    description: str = Field(default="")
    
    # Relaciones
    sentence_links: list["SentenceCategoryLink"] = Relationship(back_populates="category")


class SentenceCategoryLink(SQLModel, table=True):
    """Relación many-to-many entre oraciones y categorías"""
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    sentence_id: int = Field(foreign_key="sentenceanalysis.id", index=True)
    category_id: int = Field(foreign_key="syntaxcategory.id", index=True)
    
    # Relaciones
    sentence: Optional["SentenceAnalysis"] = Relationship(back_populates="category_links")
    category: Optional["SyntaxCategory"] = Relationship(back_populates="sentence_links")


class TokenAnnotation(SQLModel, table=True):
    """Anotación manual para una palabra específica en una oración."""
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    sentence_id: int = Field(foreign_key="sentenceanalysis.id", index=True)
    token_index: int  # Índice de la palabra en la oración (0-based)
    token_text: str   # Texto de la palabra (para verificación)
    
    # Análisis Pedagógico
    pedagogical_role: str  # Ej: "Sujeto", "Objeto Directo", "Núcleo del Predicado"
    case_function: Optional[str] = None  # Ej: "Ablativo de Instrumento", "Dativo Posesivo"
    explanation: Optional[str] = None  # Explicación en lenguaje natural
    
    # Relación
    sentence: Optional["SentenceAnalysis"] = Relationship(back_populates="token_annotations")


class SentenceStructure(SQLModel, table=True):
    """Estructura de alto nivel de la oración (cláusulas)."""
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    sentence_id: int = Field(foreign_key="sentenceanalysis.id", index=True)
    
    clause_type: str  # "Principal", "Subordinada Adverbial", "Subordinada Sustantiva"
    construction_type: Optional[str] = None  # "Ablativo Absoluto", "AcI", "Cum Histórico"
    notes: Optional[str] = None
    
    # Relación
    sentence: Optional["SentenceAnalysis"] = Relationship(back_populates="structures")
