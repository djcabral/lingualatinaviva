#!/usr/bin/env python3
"""
Importa vocabulario curado por IA (JSON) a la base de datos.
Actualiza Words existentes basándose en ID.
"""
import json
import sys
import os
import argparse
from sqlmodel import Session
from typing import List, Dict, Any

# Ensure import path
sys.path.append(os.getcwd())

from database import engine, Word

def import_curated_vocab(input_path: str):
    """
    Importa archivo JSON con vocabulario curado.
    """
    if not os.path.exists(input_path):
        print(f"❌ File not found: {input_path}")
        return

    print(f"📖 Reading {input_path}...")
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            
        # 1. Strip Markdown code blocks
        if "```" in content:
            print("🧹 Detected Markdown code blocks. Cleaning...")
            import re
            # Extract content inside ```json ... ``` or just ``` ... ```
            # Find all json blocks and concatenate them? 
            # Or just remove the fences. 
            # Simple approach: Remove lines starting with ```
            content = re.sub(r'^```\w*\s*$', '', content, flags=re.MULTILINE)
            content = content.replace('```', '')  # Remove any remaining backticks
            
        # 2. Handle concatenated lists like [...][...] by replacing ][ with ,
        if '][' in content:
             print("🔗 Detected concatenated lists. Merging...")
             content = content.replace('][', ',')

        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            # Fallback: maybe it's not a list but multiple objects?
            # Or maybe just try to wrap in [] if not list?
            print("⚠️ JSON decode failed. Trying to wrap content in [...]")
            try:
                data = json.loads(f"[{content}]")
            except:
                print("❌ Failed to parse JSON. Please check formatting.")
                return

        if not isinstance(data, list):
            print("❌ Invalid format. Expected a list of objects.")
            return
            
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return

    updated_count = 0
    errors = 0
    
    with Session(engine) as session:
        for item in data:
            word_id = item.get("id")
            if not word_id:
                print(f"⚠️ Skipping item without ID: {item}")
                continue
                
            word = session.get(Word, word_id)
            if not word:
                print(f"⚠️ Word ID {word_id} not found in database. Skipping.")
                continue
                
            # Update fields
            changes = []
            
            # Latin (Lemma)
            new_latin = item.get("latin")
            if new_latin and new_latin != word.latin:
                changes.append(f"latin: {word.latin} -> {new_latin}")
                word.latin = new_latin
                
            # POS
            new_pos = item.get("part_of_speech")
            if new_pos and new_pos != word.part_of_speech:
                changes.append(f"pos: {word.part_of_speech} -> {new_pos}")
                word.part_of_speech = new_pos
                
            # Genitive
            new_gen = item.get("genitive")
            if new_gen is not None and new_gen != word.genitive:
                 changes.append(f"gen: {word.genitive} -> {new_gen}")
                 word.genitive = new_gen
                 
            # Definition
            new_def = item.get("definition_es")
            if new_def and new_def != word.definition_es:
                changes.append(f"def: {word.definition_es} -> {new_def}")
                word.definition_es = new_def
                # If we update definition, move to active if it was pending/review?
                if word.status in ["pending", "review"]:
                    word.status = "active"
                    changes.append("status: active")

            if changes:
                updated_count += 1
                session.add(word)
                # print(f"📝 Updated Word {word_id}: {', '.join(changes)}")
            
        try:
            session.commit()
            print(f"\n✅ Successfully updated {updated_count} words.")
            if errors > 0:
                print(f"⚠️ Encountered {errors} errors.")
                
        except Exception as e:
            session.rollback()
            print(f"❌ Database error during commit: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import curated vocabulary")
    parser.add_argument("input_file", help="Path to JSON file with curated vocab")
    
    args = parser.parse_args()
    
    import_curated_vocab(args.input_file)
