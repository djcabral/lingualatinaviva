
import spacy
import logging
from typing import Dict, List, Optional, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LatinNLP:
    """
    NLP Engine for Latin text analysis using Spacy.
    Singleton pattern to load the model only once.
    """
    _instance = None
    _nlp = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LatinNLP, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._nlp is None:
            self._load_model()

    def _load_model(self):
        """Loads the Spacy Latin model."""
        try:
            logger.info("Loading Spacy Latin model 'la_core_web_lg'...")
            self._nlp = spacy.load("la_core_web_lg")
            logger.info("Model loaded successfully.")
        except OSError:
            logger.error("Failed to load model 'la_core_web_lg'. Is it installed?")
            raise

    def analyze_text(self, text: str) -> Any:
        """Runs the full Spacy pipeline on the text."""
        if not self._nlp:
            self._load_model()
        return self._nlp(text)

    def get_token_details(self, token) -> Dict[str, Any]:
        """
        Extracts structured details from a Spacy token.
        
        Returns:
            dict: {
                "text": str,
                "lemma": str,
                "pos": str, (NOUN, VERB, etc.)
                "tag": str, (noun, verb, etc. - coarser)
                "dep": str, (dependency label)
                "morph": dict (parsed morphology)
            }
        """
        # Parse morphology string (e.g., "Case=Nom|Gender=Fem") into dict
        morph_dict = {}
        if token.morph:
            for feature in str(token.morph).split('|'):
                if '=' in feature:
                    k, v = feature.split('=')
                    morph_dict[k.lower()] = v.lower()
        
        return {
            "text": token.text,
            "lemma": token.lemma_,
            "pos": token.pos_,
            "tag": token.tag_,
            "dep": token.dep_,
            "morph": morph_dict,
            "is_alpha": token.is_alpha,
            "is_stop": token.is_stop,
            "head_text": token.head.text,
            "head_pos": token.head.pos_
        }

    def analyze_sentence(self, sentence: str) -> List[Dict[str, Any]]:
        """
        Analyzes a single sentence and returns a list of token details.
        """
        doc = self.analyze_text(sentence)
        return [self.get_token_details(token) for token in doc]

# Global instance
nlp_engine = LatinNLP()
