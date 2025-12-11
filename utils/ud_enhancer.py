"""
Universal Dependencies Enhancer for Latin Text Analysis

This module enhances automatic Latin text analysis by integrating with 
Universal Dependencies corpora to validate and enrich syntactic analyses.
"""

import json
from typing import Dict, List, Any, Optional
from spacy.lang.la import Latin
import spacy

class UDEnhancer:
    """
    Enhances Latin text analysis using Universal Dependencies corpora
    """
    
    def __init__(self):
        """
        Initialize the UD Enhancer with LatinCy model
        """
        try:
            # Load LatinCy model (should be installed as per requirements)
            self.nlp = spacy.load("la_core_web_lg")
        except OSError:
            print("Warning: LatinCy model not found. Please install it from https://huggingface.co/latincy/la_core_web_lg")
            self.nlp = None
            
        # Load dependency to role mappings from existing code
        self.ud_roles = self._load_ud_roles()
    
    def _load_ud_roles(self) -> Dict[str, str]:
        """
        Load Universal Dependencies to pedagogical roles mapping
        Based on existing vocab_roles_mapper.py
        """
        return {
            # === SUBJECT ===
            "nsubj": "sujeto",
            "csubj": "sujeto",
            "nsubj:pass": "sujeto_paciente",
            
            # === PREDICATE AND VERBS ===
            "root": "predicado",
            "cop": "cópula",
            "aux": "auxiliar",
            "aux:pass": "auxiliar_pasivo",
            
            # === OBJECTS ===
            "obj": "objeto_directo",
            "ccomp": "oración_completiva",
            "xcomp": "complemento_predicativo",
            "iobj": "objeto_indirecto",
            
            # === CIRCUMSTANTIAL COMPLEMENTS ===
            "obl": "complemento_circunstancial",
            "obl:tmod": "complemento_temporal",
            "obl:arg": "complemento_obligatorio",
            "advmod": "modificador_adverbial",
            "advcl": "oración_adverbial",
            
            # === MODIFIERS ===
            "amod": "modificador_adjetival",
            "nmod": "complemento_del_nombre",
            "nummod": "modificador_numeral",
            "acl": "oración_adjetiva",
            "acl:relcl": "oración_de_relativo",
            "relcl": "oración_de_relativo",
            
            # === DETERMINERS ===
            "det": "determinante",
            
            # === APPOSITION ===
            "appos": "aposición",
            
            # === CONJUNCTIONS ===
            "cc": "conjunción_coordinante",
            "conj": "elemento_coordinado",
            "mark": "conjunción_subordinante",
            
            # === PREPOSITIONS ===
            "case": "preposición",
            
            # === PUNCTUATION ===
            "punct": "puntuación",
        }
    
    def parse_conllu_format(self, conllu_text: str) -> List[Dict[str, Any]]:
        """
        Parse CoNLL-U formatted text into structured data
        
        Args:
            conllu_text: Text in CoNLL-U format
            
        Returns:
            List of sentences, each containing list of token dictionaries
        """
        sentences = []
        current_sentence = []
        
        for line in conllu_text.strip().split('\n'):
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                if current_sentence:
                    sentences.append(current_sentence)
                    current_sentence = []
                continue
            
            # Parse token line (CoNLL-U format: ID, FORM, LEMMA, UPOS, XPOS, FEATS, HEAD, DEPREL, DEPS, MISC)
            parts = line.split('\t')
            if len(parts) >= 8:
                token = {
                    "id": int(parts[0]) if parts[0].isdigit() else parts[0],
                    "text": parts[1],
                    "lemma": parts[2],
                    "upos": parts[3],
                    "xpos": parts[4] if parts[4] != '_' else None,
                    "feats": parts[5] if parts[5] != '_' else {},
                    "head": int(parts[6]) if parts[6].isdigit() else None,
                    "deprel": parts[7],
                    "deps": parts[8] if len(parts) > 8 and parts[8] != '_' else None,
                    "misc": parts[9] if len(parts) > 9 and parts[9] != '_' else None
                }
                
                # Parse features if present
                if isinstance(token["feats"], str):
                    feats = {}
                    for feat in token["feats"].split('|'):
                        if '=' in feat:
                            k, v = feat.split('=', 1)
                            feats[k] = v
                    token["feats"] = feats
                
                current_sentence.append(token)
        
        # Add last sentence if exists
        if current_sentence:
            sentences.append(current_sentence)
            
        return sentences
    
    def enhance_analysis_with_ud(self, text: str, existing_analysis: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Enhance existing analysis with Universal Dependencies data
        
        Args:
            text: Latin text to analyze
            existing_analysis: Existing analysis to enhance (optional)
            
        Returns:
            Enhanced analysis with validation scores and enriched data
        """
        if not self.nlp:
            return {
                "error": "LatinCy model not available",
                "enhanced_analysis": existing_analysis or []
            }
        
        # Perform analysis with LatinCy
        doc = self.nlp(text)
        
        # Convert to dependency structure similar to existing system
        enhanced_tokens = []
        validation_issues = []
        
        for sent_idx, sent in enumerate(doc.sents):
            for token in sent:
                token_data = {
                    "id": token.i + 1,  # 1-indexed
                    "text": token.text,
                    "lemma": token.lemma_,
                    "pos": token.pos_,
                    "tag": token.tag_,
                    "dep": token.dep_,
                    "head": token.head.i + 1 if token.head.i >= 0 else 0,
                    "pedagogical_role": self.ud_roles.get(token.dep_, "desconocido"),
                    "morph": str(token.morph) if token.morph else "",
                    "is_oov": token.is_oov,  # Out of vocabulary
                    "is_sent_start": token.is_sent_start,
                    "sentence_id": sent_idx + 1
                }
                
                enhanced_tokens.append(token_data)
                
                # Validate against existing analysis if provided
                if existing_analysis:
                    # Find corresponding token in existing analysis
                    existing_token = next(
                        (t for t in existing_analysis if t.get("text", "").lower() == token.text.lower()), 
                        None
                    )
                    
                    if existing_token:
                        # Check for discrepancies
                        mismatches = []
                        for field in ["pos", "dep", "lemma"]:
                            existing_val = existing_token.get(field, "")
                            new_val = token_data.get(field, "")
                            if existing_val and new_val and existing_val.lower() != new_val.lower():
                                mismatches.append({
                                    "field": field,
                                    "existing": existing_val,
                                    "ud": new_val
                                })
                        
                        if mismatches:
                            validation_issues.append({
                                "token": token.text,
                                "mismatches": mismatches
                            })
        
        # Calculate confidence score based on validation
        total_tokens = len(enhanced_tokens)
        mismatched_tokens = len(validation_issues)
        confidence_score = 1.0 - (mismatched_tokens / total_tokens) if total_tokens > 0 else 1.0
        
        return {
            "enhanced_analysis": enhanced_tokens,
            "validation_issues": validation_issues,
            "confidence_score": confidence_score,
            "total_tokens": total_tokens,
            "mismatched_tokens": mismatched_tokens
        }
    
    def validate_with_ud_corpus(self, text: str, ud_corpus_path: str) -> Dict[str, Any]:
        """
        Validate text analysis against a UD corpus file
        
        Args:
            text: Latin text to validate
            ud_corpus_path: Path to UD corpus file in CoNLL-U format
            
        Returns:
            Validation report with discrepancies and suggestions
        """
        try:
            with open(ud_corpus_path, 'r', encoding='utf-8') as f:
                corpus_content = f.read()
            
            # Parse the corpus
            corpus_sentences = self.parse_conllu_format(corpus_content)
            
            # Analyze the text
            enhanced_result = self.enhance_analysis_with_ud(text)
            
            if "error" in enhanced_result:
                return enhanced_result
            
            # Compare with first sentence in corpus (simplified validation)
            if corpus_sentences:
                corpus_tokens = corpus_sentences[0]
                analyzed_tokens = enhanced_result["enhanced_analysis"]
                
                comparison = []
                for i, (corpus_token, analyzed_token) in enumerate(zip(corpus_tokens, analyzed_tokens)):
                    if i >= len(corpus_tokens) or i >= len(analyzed_tokens):
                        break
                        
                    token_comparison = {
                        "text": corpus_token["text"],
                        "corpus_pos": corpus_token["upos"],
                        "analyzed_pos": analyzed_token["pos"],
                        "pos_match": corpus_token["upos"] == analyzed_token["pos"],
                        "corpus_dep": corpus_token["deprel"],
                        "analyzed_dep": analyzed_token["dep"],
                        "dep_match": corpus_token["deprel"] == analyzed_token["dep"],
                        "corpus_lemma": corpus_token["lemma"],
                        "analyzed_lemma": analyzed_token["lemma"],
                        "lemma_match": corpus_token["lemma"] == analyzed_token["lemma"]
                    }
                    comparison.append(token_comparison)
                
                # Calculate accuracy
                pos_matches = sum(1 for c in comparison if c["pos_match"])
                dep_matches = sum(1 for c in comparison if c["dep_match"])
                lemma_matches = sum(1 for c in comparison if c["lemma_match"])
                total = len(comparison)
                
                return {
                    "comparison": comparison,
                    "pos_accuracy": pos_matches / total if total > 0 else 0,
                    "dep_accuracy": dep_matches / total if total > 0 else 0,
                    "lemma_accuracy": lemma_matches / total if total > 0 else 0,
                    "total_compared": total
                }
            
            return {
                "error": "No sentences found in corpus for comparison"
            }
            
        except FileNotFoundError:
            return {
                "error": f"Corpus file not found: {ud_corpus_path}"
            }
        except Exception as e:
            return {
                "error": f"Error validating with corpus: {str(e)}"
            }


def enhance_latin_analysis(text: str, existing_analysis: Optional[List[Dict]] = None) -> Dict[str, Any]:
    """
    Convenience function to enhance Latin text analysis with UD data
    
    Args:
        text: Latin text to analyze
        existing_analysis: Optional existing analysis to enhance
        
    Returns:
        Enhanced analysis with validation data
    """
    enhancer = UDEnhancer()
    return enhancer.enhance_analysis_with_ud(text, existing_analysis)


# Example usage
if __name__ == "__main__":
    # Example of how to use the UDEnhancer
    enhancer = UDEnhancer()
    
    sample_text = "Caesar venit Romam"
    
    if enhancer.nlp:
        result = enhancer.enhance_analysis_with_ud(sample_text)
        print("Enhanced Analysis:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Cannot perform analysis - LatinCy model not available")