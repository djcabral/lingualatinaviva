"""
Script to integrate Universal Dependencies corpus data with existing analyses
"""

import json
import sys
import os
from pathlib import Path
from typing import List, Dict, Any

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.ud_enhancer import UDEnhancer
from database.connection import get_session
from database.models import SentenceAnalysis


def load_ud_corpus(corpus_file: str) -> List[Dict[Any, Any]]:
    """
    Load Universal Dependencies corpus from CoNLL-U file
    
    Args:
        corpus_file: Path to CoNLL-U file
        
    Returns:
        List of parsed sentences
    """
    enhancer = UDEnhancer()
    
    try:
        with open(corpus_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        sentences = enhancer.parse_conllu_format(content)
        return sentences
    except Exception as e:
        print(f"Error loading corpus: {e}")
        return []


def enhance_database_analyses(limit: int = 100):
    """
    Enhance existing database analyses with UD data
    
    Args:
        limit: Number of sentences to process
    """
    enhancer = UDEnhancer()
    
    if not enhancer.nlp:
        print("Error: LatinCy model not available")
        return
    
    with get_session() as session:
        # Get sentences that need enhancement
        sentences = session.exec(
            "SELECT * FROM sentenceanalysis WHERE ud_enhanced IS NULL OR ud_enhanced = 0 "
            "ORDER BY id LIMIT :limit", 
            {"limit": limit}
        ).all()
        
        print(f"Processing {len(sentences)} sentences...")
        
        for sentence in sentences:
            try:
                # Parse existing dependency analysis
                existing_deps = json.loads(sentence.dependency_json) if sentence.dependency_json else None
                
                # Enhance with UD data
                result = enhancer.enhance_analysis_with_ud(sentence.latin_text, existing_deps)
                
                if "error" not in result:
                    # Update database with enhanced analysis
                    enhanced_deps = json.dumps(result["enhanced_analysis"], ensure_ascii=False)
                    confidence = result["confidence_score"]
                    
                    # Update sentence record
                    session.exec(
                        "UPDATE sentenceanalysis SET "
                        "dependency_json = :deps, "
                        "ud_enhanced = 1, "
                        "ud_confidence = :conf "
                        "WHERE id = :id",
                        {
                            "deps": enhanced_deps,
                            "conf": confidence,
                            "id": sentence.id
                        }
                    )
                    
                    print(f"Enhanced sentence ID {sentence.id} (Confidence: {confidence:.2f})")
                else:
                    print(f"Failed to enhance sentence ID {sentence.id}: {result['error']}")
                
            except Exception as e:
                print(f"Error processing sentence ID {sentence.id}: {e}")
                continue
        
        session.commit()
        print("Database update completed.")


def validate_against_corpus(ud_corpus_file: str, sample_text: str = None):
    """
    Validate analyses against a UD corpus
    
    Args:
        ud_corpus_file: Path to UD corpus in CoNLL-U format
        sample_text: Optional text to validate (otherwise uses database samples)
    """
    enhancer = UDEnhancer()
    
    if sample_text:
        # Validate provided text
        result = enhancer.validate_with_ud_corpus(sample_text, ud_corpus_file)
        print("Validation Results:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        # Validate database samples
        with get_session() as session:
            # Get a few sentences for validation
            sentences = session.exec(
                "SELECT latin_text FROM sentenceanalysis WHERE latin_text IS NOT NULL "
                "LIMIT 5"
            ).all()
            
            for sentence in sentences:
                print(f"\nValidating: {sentence.latin_text}")
                result = enhancer.validate_with_ud_corpus(sentence.latin_text, ud_corpus_file)
                if "error" not in result:
                    print(f"  POS Accuracy: {result['pos_accuracy']:.2f}")
                    print(f"  Dependency Accuracy: {result['dep_accuracy']:.2f}")
                    print(f"  Lemma Accuracy: {result['lemma_accuracy']:.2f}")
                else:
                    print(f"  Error: {result['error']}")


def main():
    """
    Main function to demonstrate UD corpus integration
    """
    print("Universal Dependencies Corpus Integration Tool")
    print("=" * 50)
    
    # Example usage
    enhancer = UDEnhancer()
    
    if not enhancer.nlp:
        print("LatinCy model not available. Please install it:")
        print("pip install https://huggingface.co/latincy/la_core_web_lg/resolve/main/la_core_web_lg-any-py3-none-any.whl")
        return
    
    # Demonstrate CoNLL-U parsing
    sample_conllu = """
# sent_id = 1
# text = Caesar venit Romam
1	Caesar	Caesar	PROPN	n	sing,nom	2	nsubj	_	_
2	venit	venio	VERB	v3spia	_	0	root	_	_
3	Romam	Roma	PROPN	n	sing,acc	2	obj	_	_
""".strip()
    
    parsed = enhancer.parse_conllu_format(sample_conllu)
    print("Parsed CoNLL-U sample:")
    print(json.dumps(parsed, indent=2, ensure_ascii=False))
    
    # Demonstrate enhancement
    sample_text = "Caesar venit Romam"
    result = enhancer.enhance_analysis_with_ud(sample_text)
    
    print(f"\nEnhanced analysis for '{sample_text}':")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()