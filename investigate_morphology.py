import sys
import os
from sqlmodel import Session, select
from database import engine, Word, InflectedForm
from utils.collatinus_analyzer import LatinMorphAnalyzer
from utils.stanza_analyzer import StanzaAnalyzer

def check_word(word_form):
    print(f"\n--- Checking '{word_form}' ---")
    
    with Session(engine) as session:
        # 1. Check InflectedForm
        print("1. Database InflectedForm matches:")
        forms = session.exec(select(InflectedForm).where(InflectedForm.form == word_form)).all()
        for f in forms:
            word = session.get(Word, f.word_id)
            if word:
                print(f"   - Form: {f.form}, Lemma: {word.latin}, POS: {word.part_of_speech}, Morph: {f.morphology}")
            else:
                print(f"   - Form: {f.form}, Lemma: [MISSING WORD ID {f.word_id}], Morph: {f.morphology}")

        # 2. Check Word (exact match)
        print("2. Database Word matches:")
        words = session.exec(select(Word).where(Word.latin == word_form)).all()
        for w in words:
            print(f"   - Word: {w.latin}, POS: {w.part_of_speech}")

    # 3. Check Collatinus
    print("3. Collatinus Analysis:")
    analyzer = LatinMorphAnalyzer()
    if analyzer.is_ready():
        results = analyzer.analyze_word(word_form)
        for r in results:
            print(f"   - Lemma: {r['lemma']}, Morph: {r['morph']}")
    else:
        print("   Collatinus not ready.")

    # 4. Check Stanza
    print("4. Stanza Analysis:")
    stanza = StanzaAnalyzer()
    if stanza.is_available():
        try:
            results = stanza.analyze_text(word_form)
            for r in results:
                print(f"   - Lemma: {r['lemma']}, POS: {r['pos']}, Morph: {r['morphology']}")
        except Exception as e:
            print(f"   Error: {e}")
    else:
        print("   Stanza not available.")

if __name__ == "__main__":
    check_word("Romae")
    check_word("Romani")
