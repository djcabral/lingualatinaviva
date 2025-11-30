#!/usr/bin/env python3
"""
Collatinus Dictionary Importer for Lingua Latina Viva

Imports Latin lemmas and Spanish translations from Collatinus data files
into the application database.

Usage:
    python utils/collatinus_importer.py [--limit N] [--dry-run]

License: GPL v3 (compatible with Collatinus)
Data source: Collatinus © Yves Ouvrard & Philippe Verkerk
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from sqlmodel import Session, create_engine, select

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from database import Word


class CollatinusImporter:
    """Imports Collatinus lexicon data into the database."""
    
    # Mapping of Collatinus models to our declension/conjugation system
    NOUN_MODELS = {
        'rosa': ('1', 'f'),      # 1st declension feminine
        'aqua': ('1', 'f'),
        'terra': ('1', 'f'),
        'lupus': ('2', 'm'),     # 2nd declension masculine
        'dominus': ('2', 'm'),
        'templum': ('2', 'n'),   # 2nd declension neuter
        'puer': ('2', 'm'),      # 2nd dec. masc. (no -us)
        'rex': ('3', 'm'),       # 3rd declension
        'ciuis': ('3', 'm/f'),
        'corpus': ('3', 'n'),
        'manus': ('4', 'f'),     # 4th declension
        'domus': ('4', 'f'),
        'res': ('5', 'f'),       # 5th declension
        'dies': ('5', 'm'),
    }
    
    VERB_MODELS = {
        'amo': '1',       # 1st conjugation
        'moneo': '2',     # 2nd conjugation
        'lego': '3',      # 3rd conjugation
        'capio': '3-io',  # 3rd -io conjugation
        'audio': '4',     # 4th conjugation
        'sum': 'irreg',   # Irregular
        'eo': 'irreg',
        'fero': 'irreg',
        'uolo': 'irreg',
    }
    
    def __init__(self, data_dir: str):
        """
        Initialize importer with Collatinus data directory.
        
        Args:
            data_dir: Path to directory containing lemmes.la and lemmes.es
        """
        self.data_dir = Path(data_dir)
        self.lemmes_la_path = self.data_dir / 'lemmes.la'
        self.lemmes_es_path = self.data_dir / 'lemmes.es'
        
        if not self.lemmes_la_path.exists():
            raise FileNotFoundError(f"Latin lemmas file not found: {self.lemmes_la_path}")
        if not self.lemmes_es_path.exists():
            raise FileNotFoundError(f"Spanish translations file not found: {self.lemmes_es_path}")
    
    def normalize_lemma(self, lemma: str) -> str:
        """
        Normalize a lemma by removing macrons and variants.
        
        Args:
            lemma: Raw lemma string (may contain =variants)
        
        Returns:
            Normalized lemma without macrons
        """
        # Remove variant forms (e.g., "ā=ā,ăb,ābs" -> "a")
        if '=' in lemma:
            lemma = lemma.split('=')[0]
        
        # Remove macrons and breves
        macron_map = str.maketrans(
            'āēīōūȳĂĔĬŎŬĂĕĭŏŭ',  # Characters with diacritics
            'aeiouyAEIOUaeiou'    # Plain ASCII equivalents
        )
        return lemma.translate(macron_map).strip()

    
    def parse_lemmes_es(self) -> Dict[str, str]:
        """
        Parse Spanish translations file.
        
        Returns:
            Dictionary mapping normalized lemmas to Spanish definitions
        """
        translations = {}
        
        with open(self.lemmes_es_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                
                # Skip comments and empty lines
                if not line or line.startswith('!') or line.startswith('Español'):
                    continue
                
                # Format: lemma:translation
                if ':' not in line:
                    continue
                
                lemma, translation = line.split(':', 1)
                lemma_normalized = self.normalize_lemma(lemma.strip())
                translation = translation.strip()
                
                if lemma_normalized and translation:
                    translations[lemma_normalized] = translation
        
        return translations
    
    def parse_morphology(self, morph_str: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Parse morphology string to extract part of speech.
        
        Args:
            morph_str: Morphology field from lemmes.la (e.g., "as, are", "i, m.")
        
        Returns:
            Tuple of (part_of_speech, additional_info)
        """
        if not morph_str:
            return None, None
        
        morph_str = morph_str.lower().strip()
        
        # Verbs: contain "are", "ere", "ire"
        if any(x in morph_str for x in ['are', 'ere', 'ire', 'esse']):
            return 'verb', morph_str
        
        # Nouns: contain gender markers
        if any(x in morph_str for x in [', m.', ', f.', ', n.', ', m/f']):
            return 'noun', morph_str
        
        # Adjectives: typically "a, um" or similar
        if 'a, um' in morph_str or 'is, e' in morph_str:
            return 'adjective', morph_str
        
        # Prepositions
        if 'prép' in morph_str or 'prep' in morph_str:
            return 'preposition', morph_str
        
        # Adverbs
        if 'adv' in morph_str:
            return 'adverb', morph_str
        
        # Conjunctions
        if 'conj' in morph_str:
            return 'conjunction', morph_str
        
        # Interjections
        if 'interj' in morph_str:
            return 'interjection', morph_str
        
        # Invariable marker
        if 'inv' in morph_str:
            return 'invariable', morph_str
        
        return 'unknown', morph_str
    
    def infer_declension_conjugation(self, model: str, pos: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Infer declension or conjugation from model name.
        
        Args:
            model: Model name from Collatinus (e.g., "amo", "lupus")
            pos: Part of speech
        
        Returns:
            Tuple of (declension/conjugation, gender if applicable)
        """
        if pos == 'noun':
            for model_name, (decl, gender) in self.NOUN_MODELS.items():
                if model_name in model.lower():
                    return decl, gender
            return None, None
        
        elif pos == 'verb':
            for model_name, conj in self.VERB_MODELS.items():
                if model_name in model.lower():
                    return conj, None
            return None, None
        
        return None, None
    
    def parse_lemmes_la(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Parse Latin lemmas file with morphological information.
        
        Args:
            limit: Optional limit on number of lemmas to parse
        
        Returns:
            List of dictionaries with lemma data
        """
        lemmas = []
        count = 0
        
        with open(self.lemmes_la_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                
                # Skip comments and empty lines
                if not line or line.startswith('!') or line.startswith('Latin'):
                    continue
                
                # Format: lemma|model|stem1|stem2|morphology|frequency
                parts = line.split('|')
                if len(parts) < 5:
                    continue
                
                lemma_raw = parts[0]
                model = parts[1]
                morphology = parts[4] if len(parts) > 4 else ''
                frequency = int(parts[5]) if len(parts) > 5 and parts[5].isdigit() else 0
                
                # Normalize lemma
                lemma = self.normalize_lemma(lemma_raw)
                
                # Parse morphology
                pos, morph_info = self.parse_morphology(morphology)
                
                # Infer declension/conjugation
                decl_conj, gender = self.infer_declension_conjugation(model, pos)
                
                lemma_data = {
                    'latin': lemma,
                    'collatinus_lemma': lemma_raw,
                    'collatinus_model': model,
                    'part_of_speech': pos or 'unknown',
                    'morphology_info': morph_info,
                    'frequency': frequency,
                }
                
                if pos == 'noun':
                    lemma_data['declension'] = decl_conj
                    lemma_data['gender'] = gender
                elif pos == 'verb':
                    lemma_data['conjugation'] = decl_conj
                
                lemmas.append(lemma_data)
                
                count += 1
                if limit and count >= limit:
                    break
        
        return lemmas
    
    def import_to_database(
        self, 
        db_path: str = 'lingua_latina.db',
        limit: Optional[int] = None,
        dry_run: bool = False,
        overwrite_existing: bool = False
    ) -> Tuple[int, int, int]:
        """
        Import Collatinus data into the database.
        
        Args:
            db_path: Path to SQLite database
            limit: Optional limit on number of words to import
            dry_run: If True, don't actually write to database
            overwrite_existing: If True, update existing words with Collatinus data
        
        Returns:
            Tuple of (words_added, words_updated, words_skipped)
        """
        # Parse data files
        print("📖 Parsing Spanish translations...")
        translations = self.parse_lemmes_es()
        print(f"   Found {len(translations)} Spanish translations")
        
        print("📖 Parsing Latin lemmas...")
        lemmas = self.parse_lemmes_la(limit=limit)
        print(f"   Found {len(lemmas)} Latin lemmas")
        
        if dry_run:
            print("🔍 DRY RUN MODE - No database changes will be made")
            print(f"\nSample data:")
            for i, lemma in enumerate(lemmas[:5]):
                trans = translations.get(lemma['latin'], 'N/A')
                print(f"  {i+1}. {lemma['latin']} ({lemma['part_of_speech']}) = {trans}")
            return 0, 0, 0
        
        # Connect to database
        engine = create_engine(f'sqlite:///{db_path}')
        
        added = 0
        updated = 0
        skipped = 0
        
        with Session(engine) as session:
            for lemma_data in lemmas:
                latin = lemma_data['latin']
                
                # Check if word already exists
                existing_word = session.exec(
                    select(Word).where(Word.latin == latin)
                ).first()
                
                # Get Spanish translation
                definition_es = translations.get(latin)
                
                if existing_word:
                    if overwrite_existing and definition_es:
                        # Update existing word with Collatinus data
                        existing_word.definition_es = definition_es
                        existing_word.collatinus_lemma = lemma_data.get('collatinus_lemma')
                        existing_word.collatinus_model = lemma_data.get('collatinus_model')
                        
                        # Only update if not already set
                        if not existing_word.declension and lemma_data.get('declension'):
                            existing_word.declension = lemma_data['declension']
                        if not existing_word.gender and lemma_data.get('gender'):
                            existing_word.gender = lemma_data['gender']
                        if not existing_word.conjugation and lemma_data.get('conjugation'):
                            existing_word.conjugation = lemma_data['conjugation']
                        
                        session.add(existing_word)
                        updated += 1
                    else:
                        skipped += 1
                else:
                    # Only add if we have a Spanish translation
                    if not definition_es:
                        skipped += 1
                        continue
                    
                    # Create new word
                    new_word = Word(
                        latin=latin,
                        translation=definition_es[:100],  # Short version for compatibility
                        definition_es=definition_es,       # Full definition
                        part_of_speech=lemma_data['part_of_speech'],
                        level=1,  # Default level
                        collatinus_lemma=lemma_data.get('collatinus_lemma'),
                        collatinus_model=lemma_data.get('collatinus_model'),
                        declension=lemma_data.get('declension'),
                        gender=lemma_data.get('gender'),
                        conjugation=lemma_data.get('conjugation'),
                    )
                    
                    session.add(new_word)
                    added += 1
                
                # Commit in batches
                if (added + updated) % 100 == 0:
                    session.commit()
                    print(f"   Progress: {added} added, {updated} updated, {skipped} skipped")
            
            # Final commit
            session.commit()
        
        return added, updated, skipped


def main():
    """Main entry point for the importer script."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Import Collatinus dictionary data into Lingua Latina Viva'
    )
    parser.add_argument(
        '--data-dir',
        default='data/collatinus-repo/bin/data',
        help='Path to Collatinus data directory'
    )
    parser.add_argument(
        '--db',
        default='lingua_latina.db',
        help='Path to database file'
    )
    parser.add_argument(
        '--limit',
        type=int,
        help='Limit number of words to import (for testing)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Parse files but don\'t modify database'
    )
    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Update existing words with Collatinus data'
    )
    
    args = parser.parse_args()
    
    try:
        importer = CollatinusImporter(args.data_dir)
        
        print("=" * 60)
        print("Collatinus Dictionary Importer")
        print("=" * 60)
        print(f"Data directory: {args.data_dir}")
        print(f"Database: {args.db}")
        print(f"Mode: {'DRY RUN' if args.dry_run else 'IMPORT'}")
        print(f"Overwrite existing: {args.overwrite}")
        if args.limit:
            print(f"Limit: {args.limit} words")
        print("=" * 60)
        print()
        
        added, updated, skipped = importer.import_to_database(
            db_path=args.db,
            limit=args.limit,
            dry_run=args.dry_run,
            overwrite_existing=args.overwrite
        )
        
        print()
        print("=" * 60)
        print("✅ Import Complete!")
        print("=" * 60)
        print(f"Words added: {added}")
        print(f"Words updated: {updated}")
        print(f"Words skipped: {skipped}")
        print()
        print("Attribution: Data from Collatinus © Yves Ouvrard & Philippe Verkerk")
        print("License: GPL v3")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
