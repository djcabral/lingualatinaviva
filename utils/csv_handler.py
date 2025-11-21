"""
CSV/Excel Handler for Vocabulary Import/Export

This module provides utilities for importing and exporting vocabulary data
in CSV and Excel formats, with validation and template generation.
"""

import pandas as pd
import io
from typing import Dict, List, Optional, Tuple
from database.models import Word


class VocabularyImporter:
    """Handles importing vocabulary from CSV/Excel files"""
    
    # Schema definitions for each word type
    NOUN_SCHEMA = {
        'required': ['latin', 'translation', 'genitive', 'gender', 'declension'],
        'optional': ['level', 'irregular_forms', 'category'],
        'defaults': {'level': 1, 'irregular_forms': None, 'category': 'noun'}
    }
    
    VERB_SCHEMA = {
        'required': ['latin', 'translation', 'principal_parts', 'conjugation'],
        'optional': ['level', 'irregular_forms', 'category'],
        'defaults': {'level': 1, 'irregular_forms': None, 'category': 'verb'}
    }
    
    OTHER_SCHEMA = {
        'required': ['latin', 'translation', 'part_of_speech'],
        'optional': ['level', 'is_invariable', 'category'],
        'defaults': {'level': 1, 'is_invariable': False}
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
    def validate_dataframe(df: pd.DataFrame, word_type: str) -> Tuple[bool, List[str]]:
        """Validate DataFrame against schema for word type"""
        errors = []
        
        # Select schema
        if word_type == 'noun':
            schema = VocabularyImporter.NOUN_SCHEMA
        elif word_type == 'verb':
            schema = VocabularyImporter.VERB_SCHEMA
        else:
            schema = VocabularyImporter.OTHER_SCHEMA
        
        # Check required columns
        missing_cols = set(schema['required']) - set(df.columns)
        if missing_cols:
            errors.append(f"Columnas requeridas faltantes: {', '.join(missing_cols)}")
        
        # Validate data types and values
        if 'gender' in df.columns:
            invalid_genders = df[~df['gender'].isin(['m', 'f', 'n'])]['gender'].unique()
            if len(invalid_genders) > 0:
                errors.append(f"Géneros inválidos: {', '.join(invalid_genders)}. Use: m, f, n")
        
        if 'declension' in df.columns:
            invalid_decl = df[~df['declension'].astype(str).isin(['1', '2', '3', '4', '5'])]['declension'].unique()
            if len(invalid_decl) > 0:
                errors.append(f"Declinaciones inválidas: {', '.join(map(str, invalid_decl))}. Use: 1-5")
        
        if 'conjugation' in df.columns:
            valid_conj = ['1', '2', '3', '4', 'irregular']
            invalid_conj = df[~df['conjugation'].astype(str).isin(valid_conj)]['conjugation'].unique()
            if len(invalid_conj) > 0:
                errors.append(f"Conjugaciones inválidas: {', '.join(map(str, invalid_conj))}")
        
        # Check for empty required fields
        for col in schema['required']:
            if col in df.columns:
                empty_count = df[col].isna().sum()
                if empty_count > 0:
                    errors.append(f"Campo '{col}' tiene {empty_count} valores vacíos")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def dataframe_to_words(df: pd.DataFrame, word_type: str) -> List[Word]:
        """Convert validated DataFrame to list of Word objects"""
        words = []
        
        # Select schema for defaults
        if word_type == 'noun':
            schema = VocabularyImporter.NOUN_SCHEMA
            pos = 'noun'
        elif word_type == 'verb':
            schema = VocabularyImporter.VERB_SCHEMA
            pos = 'verb'
        else:
            schema = VocabularyImporter.OTHER_SCHEMA
            pos = None  # Will come from data
        
        for _, row in df.iterrows():
            word_data = {
                'latin': row['latin'],
                'translation': row['translation'],
                'part_of_speech': pos if pos else row['part_of_speech'],
            }
            
            # Add optional fields with defaults
            for field, default in schema['defaults'].items():
                word_data[field] = row.get(field, default)
                if pd.isna(word_data[field]):
                    word_data[field] = default
            
            # Add schema-specific fields
            if word_type == 'noun':
                word_data['genitive'] = row['genitive']
                word_data['gender'] = row['gender']
                word_data['declension'] = str(row['declension'])
            elif word_type == 'verb':
                word_data['principal_parts'] = row['principal_parts']
                word_data['conjugation'] = str(row['conjugation'])
            elif 'is_invariable' in row:
                word_data['is_invariable'] = bool(row['is_invariable'])
            
            # Ensure category is set
            if 'category' not in word_data or pd.isna(word_data['category']):
                word_data['category'] = word_data['part_of_speech']
            
            words.append(Word(**word_data))
        
        return words


class VocabularyExporter:
    """Handles exporting vocabulary to CSV/Excel files"""
    
    @staticmethod
    def words_to_dataframe(words: List[Word], word_type: str) -> pd.DataFrame:
        """Convert list of Word objects to DataFrame"""
        data = []
        
        for word in words:
            row = {
                'latin': word.latin,
                'translation': word.translation,
                'level': word.level,
            }
            
            if word_type == 'noun':
                row.update({
                    'genitive': word.genitive,
                    'gender': word.gender,
                    'declension': word.declension,
                    'irregular_forms': word.irregular_forms or '',
                })
            elif word_type == 'verb':
                row.update({
                    'principal_parts': word.principal_parts,
                    'conjugation': word.conjugation,
                    'irregular_forms': word.irregular_forms or '',
                })
            else:
                row.update({
                    'part_of_speech': word.part_of_speech,
                    'is_invariable': word.is_invariable,
                })
            
            data.append(row)
        
        return pd.DataFrame(data)
    
    @staticmethod
    def to_csv(df: pd.DataFrame) -> bytes:
        """Convert DataFrame to CSV bytes"""
        return df.to_csv(index=False).encode('utf-8')
    
    @staticmethod
    def to_excel(df: pd.DataFrame) -> bytes:
        """Convert DataFrame to Excel bytes"""
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Vocabulario')
        return output.getvalue()


class TemplateGenerator:
    """Generates template CSV/Excel files for import"""
    
    @staticmethod
    def generate_noun_template() -> pd.DataFrame:
        """Generate noun template with examples"""
        return pd.DataFrame([
            {
                'latin': 'puella',
                'translation': 'girl',
                'genitive': 'puellae',
                'gender': 'f',
                'declension': '1',
                'level': 1,
                'irregular_forms': ''
            },
            {
                'latin': 'filius',
                'translation': 'son',
                'genitive': 'filii',
                'gender': 'm',
                'declension': '2',
                'level': 1,
                'irregular_forms': ''
            },
            {
                'latin': 'rex',
                'translation': 'king',
                'genitive': 'regis',
                'gender': 'm',
                'declension': '3',
                'level': 2,
                'irregular_forms': ''
            }
        ])
    
    @staticmethod
    def generate_verb_template() -> pd.DataFrame:
        """Generate verb template with examples"""
        return pd.DataFrame([
            {
                'latin': 'amo',
                'translation': 'to love',
                'principal_parts': 'amo, amāre, amāvi, amātum',
                'conjugation': '1',
                'level': 1,
                'irregular_forms': ''
            },
            {
                'latin': 'video',
                'translation': 'to see',
                'principal_parts': 'videō, vidēre, vīdī, vīsum',
                'conjugation': '2',
                'level': 1,
                'irregular_forms': ''
            },
            {
                'latin': 'sum',
                'translation': 'to be',
                'principal_parts': 'sum, esse, fuī, futūrus',
                'conjugation': 'irregular',
                'level': 1,
                'irregular_forms': '{"pres_1sg": "sum", "pres_2sg": "es"}'
            }
        ])
    
    @staticmethod
    def generate_other_template() -> pd.DataFrame:
        """Generate other words template with examples"""
        return pd.DataFrame([
            {
                'latin': 'et',
                'translation': 'and',
                'part_of_speech': 'conjunction',
                'level': 1,
                'is_invariable': True
            },
            {
                'latin': 'magnus',
                'translation': 'great/large',
                'part_of_speech': 'adjective',
                'level': 1,
                'is_invariable': False
            },
            {
                'latin': 'bene',
                'translation': 'well',
                'part_of_speech': 'adverb',
                'level': 2,
                'is_invariable': True
            }
        ])
