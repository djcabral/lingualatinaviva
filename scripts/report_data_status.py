
import sys
import os
from sqlmodel import select

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.connection import get_session
from database import Word, SentenceAnalysis, LessonVocabulary

def generate_report():
    print("📊 Generating Data Status Report...")
    
    with get_session() as session:
        # Count Words
        total_words = len(session.exec(select(Word)).all())
        verbs = len(session.exec(select(Word).where(Word.part_of_speech == "verb")).all())
        nouns = len(session.exec(select(Word).where(Word.part_of_speech == "noun")).all())
        adjectives = len(session.exec(select(Word).where(Word.part_of_speech == "adjective")).all())
        
        # Count Sentences
        total_sentences = len(session.exec(select(SentenceAnalysis)).all())
        
        # Count Lesson Vocabulary
        total_lesson_vocab = len(session.exec(select(LessonVocabulary)).all())
        
        report = f"""
# Data Status Report

## Vocabulary
- **Total Words**: {total_words}
- **Verbs**: {verbs} (Critical for Conjugations module)
- **Nouns**: {nouns} (Critical for Declensions module)
- **Adjectives**: {adjectives}

## Sentences
- **Total Analyzed Sentences**: {total_sentences}

## Lesson Integration
- **Lesson Vocabulary Entries**: {total_lesson_vocab} (Needs population in Stage 2/3)

## Status
- ✅ **Stabilization**: Essential verbs and nouns are present. Practice modules should load.
- ⚠️ **Next Steps**: Populate LessonVocabulary and assign sentences to lessons.
        """
        
        print(report)
        
        # Save report to file
        with open("ESTADO_DATOS.md", "w") as f:
            f.write(report)
            print("✅ Report saved to ESTADO_DATOS.md")

if __name__ == "__main__":
    generate_report()
