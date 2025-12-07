"""
Diagnóstico de alineación de tokens vs TextWordLinks
"""
import sys
import os
sys.path.append(os.getcwd())

from database.connection import get_session
from database import Text, TextWordLink
from sqlmodel import select
import re
import unicodedata

def normalize(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.lower()

def diagnose_alignment(text_id=4):
    with get_session() as session:
        text = session.exec(select(Text).where(Text.id == text_id)).first()
        if not text:
            print(f"Text ID {text_id} not found")
            return
            
        content = text.content
        
        sentences = re.split(r"(?<=[.!?])\s+", content)
        
        print(f"📖 Text: {text.title}")
        print(f"📝 Content: {content}")
        print()
        print("Tokenized by sentence:")
        print("=" * 80)
        
        all_tokens = []
        for s_idx, sentence in enumerate(sentences, 1):
            tokens = re.findall(r"[\w'āēīōūĀĒĪŌŪ]+|[.,!?;:]", sentence)
            print(f"Sentence {s_idx}: {tokens}")
            for t_idx, token in enumerate(tokens, 1):
                all_tokens.append((s_idx, t_idx, token))
        
        print()
        print("Comparison with TextWordLinks:")
        print("=" * 80)
        
        links = session.exec(
            select(TextWordLink)
            .where(TextWordLink.text_id == text_id)
            .order_by(TextWordLink.sentence_number, TextWordLink.position_in_sentence)
        ).all()
        
        print(f"  # | Content Token             | Link.form       | Lemma          | Match")
        print("-" * 90)
        
        for i, ((s, p, token), link) in enumerate(zip(all_tokens, links)):
            token_norm = normalize(token)
            link_form = link.form if link.form else "(none)"
            link_norm = normalize(link_form)
            
            match = "OK" if token_norm == link_norm else "MISMATCH"
            
            lemma = ""
            if link.word_id and link.word:
                lemma = link.word.latin
            
            print(f"{i+1:>3} | {token:>25} | {link_form:>15} | {lemma:>14} | {match}")
        
        if len(all_tokens) != len(links):
            print(f"\n⚠️ Token count ({len(all_tokens)}) differs from link count ({len(links)})")
        else:
            print(f"\n✅ Token count matches link count: {len(all_tokens)}")


if __name__ == "__main__":
    text_id = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    diagnose_alignment(text_id)
