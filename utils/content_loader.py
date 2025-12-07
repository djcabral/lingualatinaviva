
import json
import logging
from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict

# Database
from database.connection import get_session
from database import SentenceAnalysis, Text, TextWordLink, Word
from sqlmodel import select

# NLP tools (lazy loading in __init__)
try:
    import stanza
    STANZA_AVAILABLE = True
except ImportError:
    STANZA_AVAILABLE = False

try:
    from spacy import displacy
    DISPLACY_AVAILABLE = True
except ImportError:
    DISPLACY_AVAILABLE = False

# Logger config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentLoader:
    """
    Unified loader for Latin content.
    Automates the generation of:
    1. Dependency Analysis (Stanza) -> dependency_json
    2. Visual Tree (Displacy) -> tree_diagram_svg
    3. Syntax Roles (UI) -> syntax_roles
    4. Text-Vocabulary Linking -> TextWordLink
    """
    
    # Mapping of Universal Dependencies to UI Syntax Roles
    DEPENDENCY_TO_ROLE = {
        "nsubj": "subject", "csubj": "subject", "nsubj:pass": "subject",
        "root": "predicate", "cop": "predicate", "aux": "predicate", "aux:pass": "predicate",
        "obj": "direct_object", "ccomp": "direct_object",
        "iobj": "indirect_object",
        "obl": "complement", "advmod": "complement", "advcl": "complement",
        "amod": "modifier", "nmod": "modifier", "nummod": "modifier",
        "det": "determiner",
        "appos": "apposition",
        "cc": "conjunction", "mark": "conjunction",
        "case": "preposition"
    }

    def __init__(self, stanza_model_path: str = 'la'):
        self.nlp = None
        if STANZA_AVAILABLE:
            try:
                logger.info("📦 Loading Stanza model...")
                # Download if not present, but usually we expect it to be there
                # stanza.download(stanza_model_path) 
                self.nlp = stanza.Pipeline(stanza_model_path, processors='tokenize,pos,lemma,depparse', verbose=False)
                logger.info("✅ Stanza model loaded.")
            except Exception as e:
                logger.error(f"❌ Failed to load Stanza: {e}")
        else:
            logger.warning("⚠️ Stanza library not installed.")

    def process_sentence(self, latin_text: str, translation: str = "", 
                        source: str = "", lesson: int = 1, complexity: int = 1,
                        constructions: List[str] = None) -> SentenceAnalysis:
        """
        Full pipeline to process a single sentence and return a populated SentenceAnalysis object (not saved yet).
        """
        if not self.nlp:
            logger.error("Cannot process sentence without Stanza NLP.")
            return None

        # 1. NLP Analysis
        try:
            doc = self.nlp(latin_text)
            tokens_data = []
            
            # Extract tokens from Stanza doc
            # Assuming single sentence processing for now
            for sent in doc.sentences:
                for word in sent.words:
                    tokens_data.append({
                        "id": word.id,
                        "text": word.text,
                        "lemma": word.lemma,
                        "pos": word.upos, # Universal POS
                        "dep": word.deprel,
                        "head": word.head,
                        "morph": word.feats if word.feats else ""
                    })
            
            dependency_json = json.dumps(tokens_data)
        except Exception as e:
            logger.error(f"Error during NLP analysis: {e}")
            return None

        # 2. Syntax Roles Mapping
        syntax_roles = self._map_roles(tokens_data)
        syntax_roles_json = json.dumps(syntax_roles)

        # 3. SVG Generation
        svg = self._generate_svg(tokens_data)

        # 4. Create Object
        sentence = SentenceAnalysis(
            latin_text=latin_text,
            spanish_translation=translation,
            source=source,
            lesson_number=lesson,
            complexity_level=complexity,
            sentence_type="simple", # Default, could be inferred
            constructions=json.dumps(constructions or []),
            dependency_json=dependency_json,
            syntax_roles=syntax_roles_json,
            tree_diagram_svg=svg,
            token_annotations=[] # Empty for manual filling later
        )

        return sentence

    def save_sentence(self, sentence: SentenceAnalysis) -> bool:
        """Saves the processed sentence to the database."""
        try:
            with get_session() as session:
                # Check for duplicates based on exact text match
                existing = session.exec(select(SentenceAnalysis).where(SentenceAnalysis.latin_text == sentence.latin_text)).first()
                if existing:
                    logger.info(f"Sentence already exists: {sentence.latin_text[:20]}...")
                    # Update fields? For now, skip or maybe update metadata
                    # valid strategy: update analysis fields if they are better/newer
                    existing.dependency_json = sentence.dependency_json
                    existing.syntax_roles = sentence.syntax_roles
                    existing.tree_diagram_svg = sentence.tree_diagram_svg
                    session.add(existing)
                else:
                    session.add(sentence)
                session.commit()
            return True
        except Exception as e:
            logger.error(f"Error saving sentence: {e}")
            return False

    def _map_roles(self, tokens: List[Dict]) -> Dict[str, List[int]]:
        """Maps token dependencies to UI roles."""
        roles = defaultdict(list)
        for token in tokens:
            dep = token.get("dep", "").lower()
            tid = token.get("id")
            
            # Direct mapping
            role = self.DEPENDENCY_TO_ROLE.get(dep)
            
            # Fallback generalization
            if not role:
                if "subj" in dep: role = "subject"
                elif "obj" in dep: role = "direct_object"
                elif "mod" in dep: role = "modifier"
            
            if role and tid:
                roles[role].append(tid)
        return dict(roles)

    def _generate_svg(self, tokens: List[Dict]) -> Optional[str]:
        """Generates SVG dependency tree using Displacy."""
        if not DISPLACY_AVAILABLE:
            return None
        
        words = []
        arcs = []
        
        for token in tokens:
            words.append({
                "text": token["text"],
                "tag": token["pos"]
            })
            
            if token["head"] > 0:
                head_idx = token["head"] - 1
                dep_idx = token["id"] - 1
                
                if head_idx >= 0 and dep_idx >= 0:
                    start = min(head_idx, dep_idx)
                    end = max(head_idx, dep_idx)
                    direction = "left" if head_idx > dep_idx else "right"
                    
                    arcs.append({
                        "start": start,
                        "end": end,
                        "label": token["dep"],
                        "dir": direction
                    })
        
        manual_data = {
            "words": words,
            "arcs": arcs
        }
        
        try:
            svg = displacy.render(manual_data, style="dep", manual=True, options={
                "compact": False, 
                "bg": "#ffffff", 
                "distance": 100
            })
            return svg
        except Exception as e:
            logger.error(f"Error generating SVG: {e}")
            return None

            if s and self.save_sentence(s):
                count += 1
        return count

    def process_text_content(self, text_id: int) -> Dict[str, int]:
        """
        Process a full Text record from the database.
        Splits into sentences, generates analysis, and creates TextWordLinks.
        """
        results = {"sentences": 0, "links": 0, "errors": 0}
        
        with get_session() as session:
            text_record = session.get(Text, text_id)
            if not text_record:
                logger.error(f"Text with ID {text_id} not found.")
                return results
            
            if not self.nlp:
                logger.error("NLP model not loaded.")
                return results

            logger.info(f"Processing Text {text_id}: {text_record.title}")
            
            try:
                # 1. NLP Analysis of full text
                doc = self.nlp(text_record.content)
                
                # Clear existing links for this text to avoid duplicates? 
                # For now, let's assume we might want to wipe and rebuild or handle appropriately.
                # A safe approach is to delete existing links for this text_id before processing.
                existing_links = session.exec(select(TextWordLink).where(TextWordLink.text_id == text_id)).all()
                for link in existing_links:
                    session.delete(link)
                session.commit() # Commit deletion

                sentence_global_index = 1
                
                for sent_idx, sent in enumerate(doc.sentences, 1):
                    # 2. Create SentenceAnalysis for each sentence
                    # Reconstruct sentence text
                    sent_text = sent.text
                    
                    tokens_data = []
                    for word in sent.words:
                        tokens_data.append({
                            "id": word.id,
                            "text": word.text,
                            "lemma": word.lemma,
                            "pos": word.upos,
                            "dep": word.deprel,
                            "head": word.head,
                            "morph": word.feats if word.feats else ""
                        })
                    
                    # Generate artifacts
                    dependency_json = json.dumps(tokens_data)
                    syntax_roles = self._map_roles(tokens_data)
                    syntax_roles_json = json.dumps(syntax_roles)
                    svg = self._generate_svg(tokens_data)
                    
                    # Create/Update SentenceAnalysis
                    # We try to use the existing `save_sentence` logic but we need to return the ID potentially
                    # Or just create it here directly to link it if we add a Text-Sentence link later.
                    # Currently SentenceAnalysis doesn't link to Text explicitly in the provided model (Lesson number is there).
                    # But the user wants 'dependency_json' which lives in SentenceAnalysis.
                    # For Tooltips (TextWordLink), we populate that separately below.
                    
                    sentence_obj = SentenceAnalysis(
                        latin_text=sent_text,
                        spanish_translation="", # We don't have translation at sentence level automatically
                        source=f"TxID:{text_id} {text_record.title}",
                        lesson_number=None, # explicit linkage or inferred?
                        complexity_level=text_record.difficulty,
                        sentence_type="unknown",
                        dependency_json=dependency_json,
                        syntax_roles=syntax_roles_json,
                        tree_diagram_svg=svg
                    )
                    
                    # Deduplication logic (check exact text + source match usually, but here maybe just text)
                    existing_sa = session.exec(select(SentenceAnalysis).where(SentenceAnalysis.latin_text == sent_text)).first()
                    if existing_sa:
                        existing_sa.dependency_json = dependency_json
                        existing_sa.syntax_roles = syntax_roles_json
                        existing_sa.tree_diagram_svg = svg
                        session.add(existing_sa)
                        results["sentences"] += 1
                        # We might want to use this ID later if we linked Text->Sentence
                    else:
                        session.add(sentence_obj)
                        results["sentences"] += 1
                    
                    # 3. Create TextWordLinks for Tooltips
                    for word_idx, token in enumerate(sent.words, 1):
                        # Attempt to find word in dictionary
                        # Lookup logic: exact match lemma or form
                        # Try lemma first
                        word_match = session.exec(select(Word).where(Word.latin == token.lemma)).first()
                        
                        syntax_role = self._get_single_role(token.deprel)
                        
                        link = TextWordLink(
                            text_id=text_id,
                            word_id=word_match.id if word_match else None,
                            sentence_number=sent_idx,
                            position_in_sentence=word_idx,
                            form=token.text,
                            morphology_json=json.dumps(self._parse_feats(token.feats)),
                            syntax_role=syntax_role,
                            notes=None
                        )
                        session.add(link)
                        results["links"] += 1
                        
                session.commit()
                
            except Exception as e:
                logger.error(f"Error processing text content: {e}")
                results["errors"] += 1
                
        return results

    def _get_single_role(self, dep: str) -> str:
        """Helper to get a single primary role from dependency tag."""
        dep = dep.lower()
        role = self.DEPENDENCY_TO_ROLE.get(dep)
        if not role:
            if "subj" in dep: role = "subject"
            elif "obj" in dep: role = "direct_object"
            elif "mod" in dep: role = "modifier"
        return role or "other"

    def _parse_feats(self, feats_str: str) -> Dict[str, str]:
        """Parses Stanza feats string 'Case=Acc|Gender=Fem' into dict."""
        if not feats_str:
            return {}
        try:
            return dict(item.split("=") for item in feats_str.split("|"))
        except:
            return {}
