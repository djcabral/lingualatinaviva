
import json
import logging
from typing import List, Dict, Optional, Tuple
from sqlmodel import select

from database.connection import get_session
from database import Text, Word, TextWordLink, InflectedForm, Author, SentenceAnalysis
from utils.nlp_engine import nlp_engine, LatinNLP
from utils.latin_logic import LatinMorphology

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentImporter:
    """
    Handles the import of raw Latin text into the database structure.
    Uses NLP Engine to auto-discover words and generate links.
    """
    
    def __init__(self):
        self.nlp = nlp_engine

    def import_text(self, title: str, content: str, level: int = 1, author_name: str = "Unknown") -> int:
        """
        Imports a text.
        
        Args:
            title: Title of the text/reading.
            content: Raw Latin text.
            level: Difficulty level (1-10).
            author_name: Name of the author.
            
        Returns:
            text_id: The ID of the created/updated Text record.
        """
        logger.info(f"Importing text '{title}'...")
        
        with get_session() as session:
            # 1. Get or Create Author
            author = session.exec(select(Author).where(Author.name == author_name)).first()
            if not author:
                author = Author(name=author_name, difficulty_level=level)
                session.add(author)
                session.commit()
                session.refresh(author)
            
            # 2. Create Text Record
            # Check if exists to update or create new? For now, create new or overwrite if title matches?
            # Let's assume title is unique for simplicity here.
            text_record = session.exec(select(Text).where(Text.title == title)).first()
            if not text_record:
                text_record = Text(
                    title=title,
                    content=content,
                    level=level,
                    author_id=author.id
                )
                session.add(text_record)
                session.commit()
                session.refresh(text_record)
            else:
                # Update content if exists
                text_record.content = content
                text_record.level = level
                session.add(text_record)
                session.commit()
                session.refresh(text_record)
                
                # specific cleanup: delete old links if re-importing
                # In a real app we might want to be more careful, but for this tool, full refresh is safer.
                # links = session.exec(select(TextWordLink).where(TextWordLink.text_id == text_record.id)).all()
                # for link in links: session.delete(link)
                # session.commit()
                # (Skipping delete for now to avoid complexity, assuming additive or fresh DB)

            # 3. Process Content via NLP
            doc = self.nlp.analyze_text(content)
            
            sentence_num = 1
            word_pos = 1
            
            for token in doc:
                # Handle punctuation / spacing logic if needed, but Spacy handles basic tokenization.
                # If token is a sentence terminator, increment sentence_num
                if token.is_sent_start:
                    # Spacy sentence detection
                    pass 
                
                # We can adhere to Spacy's sentence iteration:
                pass
            
            # Better approach: Iterate by sentences
            for sent in doc.sents:
                word_pos = 1
                for token in sent:
                    if not token.is_alpha:
                        # Save punctuation link? Yes, allows reconstruction.
                        # But TextWordLink usually links to specific Words. 
                        # If punctuation, word_id is None.
                        self._create_link(session, text_record.id, None, token.text, sentence_num, word_pos, None)
                    else:
                        # Analyze Word
                        details = self.nlp.get_token_details(token)
                        lemma = details["lemma"]
                        pos = details["pos"]
                        
                        # Find or Create Word
                        word = self._get_or_create_word(session, detail=details)
                        
                        # Create Link with Analysis
                        self._create_link(session, text_record.id, word.id, token.text, sentence_num, word_pos, details["morph"])
                        
                        # Ensure InflectedForm exists
                        self._ensure_inflected_form(session, word, token.text, details["morph"])
                        
                    word_pos += 1
                sentence_num += 1
                
            session.commit()
            logger.info(f"Import complete for '{title}'. Text ID: {text_record.id}")
            return text_record.id

    def _get_or_create_word(self, session, detail: Dict) -> Word:
        """Finds a word by Lemma/POS or creates a 'review_pending' one."""
        lemma = detail["lemma"]
        pos_map = {"NOUN": "noun", "VERB": "verb", "ADJ": "adjective", "ADP": "preposition", "ADV": "adverb", "SCONJ": "conjunction", "CCONJ": "conjunction", "PRON": "pronoun", "PROPN": "noun"}
        
        # Simple mapping
        db_pos = pos_map.get(detail["pos"], "other")
        
        # Try finding exact match
        word = session.exec(select(Word).where(Word.latin == lemma)).first()
        
        # Fallback: specific lookup for critical words (like sum) if lemma is different
        # if not word and lemma == 'sum': ...
        
        if not word:
            # Create new Review Pending word
            word = Word(
                latin=lemma,
                translation="[PENDING]", # Needs human review or translation API
                part_of_speech=db_pos,
                level=1,
                status="review" # Status flag to find pending words
            )
            
            # Attempt to set properties based on POS
            if db_pos == "noun":
                 # Guess gender/declension? Hard without more data.
                 # Leave for review.
                 pass
            elif db_pos == "preposition":
                word.is_invariable = True
                
            session.add(word)
            session.commit()
            session.refresh(word)
            logger.info(f"Created new pending word: {lemma} ({db_pos})")
            
        return word

    def _create_link(self, session, text_id, word_id, form, sent_num, pos_num, morph):
        link = TextWordLink(
            text_id=text_id,
            word_id=word_id,
            sentence_number=sent_num,
            position_in_sentence=pos_num,
            form=form,
            morphology_json=json.dumps(morph) if morph else None
        )
        session.add(link)

    def _ensure_inflected_form(self, session, word, form, morph):
        """Adds to InflectedForm if missing."""
        norm = LatinMorphology.normalize_latin(form)
        existing = session.exec(select(InflectedForm).where(InflectedForm.normalized_form == norm).where(InflectedForm.word_id == word.id)).first()
        
        if not existing:
            inf_form = InflectedForm(
                word_id=word.id,
                form=form,
                normalized_form=norm,
                morphology=json.dumps(morph)
            )
            session.add(inf_form)

    def reanalyze_text(self, text_id: int):
        """
        Re-analyzes an existing text, updating its links and analysis.
        Use this when the NLP engine logic improves.
        """
        logger.info(f"Re-analyzing Text {text_id}...")
        
        with get_session() as session:
            text = session.get(Text, text_id)
            if not text:
                logger.error(f"Text {text_id} not found.")
                return

            # DELETE existing links
            existing_links = session.exec(select(TextWordLink).where(TextWordLink.text_id == text_id)).all()
            for link in existing_links:
                session.delete(link)
            
            # Re-process content
            doc = self.nlp.analyze_text(text.content)
            
            sentence_num = 1
            word_pos = 1
            
            # Simple sentence iterator logic matches import_text
            for sent in doc.sents:
                word_pos = 1
                for token in sent:
                    if not token.is_alpha:
                        self._create_link(session, text.id, None, token.text, sentence_num, word_pos, None)
                    else:
                        details = self.nlp.get_token_details(token)
                        word = self._get_or_create_word(session, detail=details)
                        self._create_link(session, text.id, word.id, token.text, sentence_num, word_pos, details["morph"])
                        self._ensure_inflected_form(session, word, token.text, details["morph"])
                    
                    word_pos += 1
                sentence_num += 1
            
            session.commit()
            logger.info(f"Text {text_id} re-analysis complete.")

    def reanalyze_sentence(self, sentence_id: int):
        """
        Re-analyzes a SentenceAnalysis record, updating dependency_json.
        """
        logger.info(f"Re-analyzing Sentence {sentence_id}...")
        
        with get_session() as session:
            sentence = session.get(SentenceAnalysis, sentence_id)
            if not sentence:
                return

            # Run NLP
            doc = self.nlp.analyze_text(sentence.latin_text)
            
            # Build dependency JSON structure for displaCy or internal usage
            # [{id, text, lemma, pos, dep, head, morph}, ...]
            # Note: Spacy tokens are 0-indexed.
            
            dep_data = []
            syntax_roles = {"subject": [], "predicate": [], "object": []}
            
            for token in doc:
                token_data = {
                    "id": token.i,
                    "text": token.text,
                    "lemma": token.lemma_,
                    "pos": token.pos_,
                    "tag": token.tag_,
                    "dep": token.dep_,
                    "head": token.head.i,
                    "morph": str(token.morph)
                }
                dep_data.append(token_data)
                
                # Naive syntax tagging for now
                if token.dep_ == "nsubj":
                    syntax_roles["subject"].append(token.i)
                elif token.dep_ == "obj" or token.dep_ == "dobj":
                     syntax_roles["object"].append(token.i)
                elif token.pos_ == "VERB":
                     syntax_roles["predicate"].append(token.i)

            sentence.dependency_json = json.dumps(dep_data)
            sentence.syntax_roles = json.dumps(syntax_roles)
            
            session.add(sentence)
            session.commit()
            logger.info(f"Sentence {sentence_id} re-analysis updated.")


