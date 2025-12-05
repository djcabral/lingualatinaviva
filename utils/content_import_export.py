"""
Content Import/Export Handler

This module provides utilities for importing and exporting content (Texts, Sentences)
in CSV and Excel formats, similar to the Vocabulary handler.
"""

import pandas as pd
import io
import json
from typing import List, Tuple, Dict, Optional
from database import Text, SentenceAnalysis

class ContentImporter:
    """Handles importing content from CSV/Excel files"""
    
    TEXT_SCHEMA = {
        'required': ['title', 'content', 'difficulty'],
        'optional': ['author', 'book', 'chapter', 'source'],
        'defaults': {'difficulty': 1}
    }
    
    SYNTAX_SCHEMA = {
        'required': ['latin_text', 'spanish_translation', 'complexity'],
        'optional': ['source', 'notes', 'sentence_type'],
        'defaults': {'complexity': 1, 'sentence_type': 'simple'}
    }

    @staticmethod
    def parse_file(file_bytes: bytes, filename: str) -> pd.DataFrame:
        """Parse CSV or Excel file into DataFrame"""
        try:
            if filename.endswith('.csv'):
                return pd.read_csv(io.BytesIO(file_bytes))
            elif filename.endswith(('.xlsx', '.xls')):
                return pd.read_excel(io.BytesIO(file_bytes))
            else:
                raise ValueError("Formato no soportado. Use .csv, .xlsx o .xls")
        except Exception as e:
            raise ValueError(f"Error al leer archivo: {str(e)}")

    @staticmethod
    def validate_dataframe(df: pd.DataFrame, content_type: str) -> Tuple[bool, List[str]]:
        """Validate DataFrame against schema"""
        errors = []
        
        if content_type == 'text':
            schema = ContentImporter.TEXT_SCHEMA
        elif content_type == 'syntax':
            schema = ContentImporter.SYNTAX_SCHEMA
        else:
            return False, ["Tipo de contenido desconocido"]
            
        # Check required columns
        missing_cols = set(schema['required']) - set(df.columns)
        if missing_cols:
            errors.append(f"Columnas requeridas faltantes: {', '.join(missing_cols)}")
            
        # Check for empty required fields
        for col in schema['required']:
            if col in df.columns:
                empty_count = df[col].isna().sum()
                if empty_count > 0:
                    errors.append(f"Campo '{col}' tiene {empty_count} valores vacíos")
        
        return len(errors) == 0, errors

    @staticmethod
    def dataframe_to_texts(df: pd.DataFrame) -> List[Text]:
        """Convert validated DataFrame to list of Text objects"""
        texts = []
        for _, row in df.iterrows():
            text_data = {
                'title': row['title'],
                'content': row['content'],
                'difficulty': row['difficulty'] if 'difficulty' in row else 1,
                'author': row['author'] if 'author' in row and pd.notna(row['author']) else None,
                'book_number': int(row['book']) if 'book' in row and pd.notna(row['book']) else None,
                'chapter_number': int(row['chapter']) if 'chapter' in row and pd.notna(row['chapter']) else None,
            }
            texts.append(Text(**text_data))
        return texts

    @staticmethod
    def dataframe_to_sentences(df: pd.DataFrame) -> List[SentenceAnalysis]:
        """Convert validated DataFrame to list of SentenceAnalysis objects"""
        sentences = []
        for _, row in df.iterrows():
            sent_data = {
                'latin_text': row['latin_text'],
                'spanish_translation': row['spanish_translation'],
                'complexity_level': row['complexity'] if 'complexity' in row else 1,
                'source': row['source'] if 'source' in row and pd.notna(row['source']) else None,
                'sentence_type': row['sentence_type'] if 'sentence_type' in row and pd.notna(row['sentence_type']) else 'simple',
                # Initialize empty analysis structures
                'dependency_json': '[]',
                'syntax_roles': '{}',
            }
            sentences.append(SentenceAnalysis(**sent_data))
        return sentences

class ContentExporter:
    """Handles exporting content to CSV/Excel files"""
    
    @staticmethod
    def texts_to_dataframe(texts: List[Text]) -> pd.DataFrame:
        data = []
        for t in texts:
            data.append({
                'title': t.title,
                'author': t.author,
                'content': t.content,
                'difficulty': t.difficulty,
                'book': t.book_number,
                'chapter': t.chapter_number
            })
        return pd.DataFrame(data)

    @staticmethod
    def sentences_to_dataframe(sentences: List[SentenceAnalysis]) -> pd.DataFrame:
        data = []
        for s in sentences:
            data.append({
                'latin_text': s.latin_text,
                'spanish_translation': s.spanish_translation,
                'complexity': s.complexity_level,
                'source': s.source,
                'sentence_type': s.sentence_type
            })
        return pd.DataFrame(data)

    @staticmethod
    def to_csv(df: pd.DataFrame) -> bytes:
        return df.to_csv(index=False).encode('utf-8')

    @staticmethod
    def to_excel(df: pd.DataFrame, sheet_name: str = 'Data') -> bytes:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name=sheet_name)
        return output.getvalue()

class ContentTemplateGenerator:
    """Generates template CSV/Excel files"""
    
    @staticmethod
    def generate_text_template() -> pd.DataFrame:
        return pd.DataFrame([
            {
                'title': 'De Bello Gallico (Ejemplo)',
                'author': 'Julio César',
                'content': 'Gallia est omnis divisa in partes tres...',
                'difficulty': 3,
                'book': 1,
                'chapter': 1
            }
        ])

    @staticmethod
    def generate_syntax_template() -> pd.DataFrame:
        return pd.DataFrame([
            {
                'latin_text': 'Puella rosam videt.',
                'spanish_translation': 'La niña ve la rosa.',
                'complexity': 1,
                'source': 'Ejemplo',
                'sentence_type': 'simple'
            }
        ])
