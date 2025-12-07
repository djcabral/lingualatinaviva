#!/usr/bin/env python3
"""
Exporta vocabulario (tabla Word) para ser curado por IA (Grok).
Genera un archivo Markdown con el prompt y los datos JSON.
"""
import json
import sys
import os
import argparse
from sqlmodel import Session, select, or_, func

# Ensure import path
sys.path.append(os.getcwd())

from database import engine, Word

def export_vocab_for_grok(output_path: str = "data/grok_vocab_prompt.md", limit: int = 50, offset: int = 0, status_filter: str = None):
    """
    Exporta palabras a formato JSON envuelto en Markdown para Grok.
    
    Args:
        output_path: Ruta del archivo de salida.
        limit: Máximo de palabras.
        offset: Desplazamiento.
        status_filter: Filtrar por estado (ej: 'pending', 'review', 'active'). Si es None, trae todo (o prioriza incompletos).
    """
    
    with Session(engine) as session:
        query = select(Word)
        
        # Filtros básicos
        if status_filter:
            query = query.where(Word.status == status_filter)
        else:
            # Default logic: Prioritize words missing definitions or with status 'pending'
            # If no specific filter asked, let's try to find "incomplete" ones first
            # We construct a custom ordering or filter?
            # For simplicity, let's just grab words with NULL definition_es OR status='pending'
            query = query.where(
                or_(
                    Word.definition_es == None,
                    Word.definition_es == "[PENDING]",
                    Word.status == "review"
                )
            )
            
        # Paginación
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
            
        words = session.exec(query).all()
        
        if not words:
            print("⚠️ No words found matching criteria.")
            return

        print(f"Found {len(words)} words to export.")
        
        # Transform to JSON-serializable list
        vocab_list = []
        for w in words:
            vocab_list.append({
                "id": w.id,
                "latin": w.latin,
                "part_of_speech": w.part_of_speech,
                "genitive": w.genitive,
                "definition_es": w.definition_es,
                "status": w.status # Informative, IA implies context
            })
            
        # Load template
        template_path = "data/vocab_analysis_prompt.md"
        if os.path.exists(template_path):
            with open(template_path, "r", encoding="utf-8") as f:
                prompt_content = f.read()
        else:
            prompt_content = "# TAREA: Curation de Vocabulario\n\n[Template not found, using generic header]\n\n"
            
        # Combine
        full_content = prompt_content + json.dumps(vocab_list, indent=2, ensure_ascii=False) + "\n```"
        
        # Write output
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_content)
            
        print(f"✅ Exported to {output_path}")
        print(f"📋 INSTRUCTIONS:")
        print(f"1. Open {output_path}")
        print(f"2. Copy content to Grok")
        print(f"3. Save Grok's JSON response to a file (e.g. data/grok_vocab_response.json)")
        print(f"4. Run import_curated_vocab.py")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export vocabulary for Grok curation")
    parser.add_argument("--limit", type=int, default=50, help="Batch size (default: 50)")
    parser.add_argument("--offset", type=int, default=0, help="Start offset (for manual single batch)")
    parser.add_argument("--output", type=str, default="data/grok_vocab_prompt.md", help="Output file (for single batch)")
    parser.add_argument("--status", type=str, help="Filter by status (active, pending, review)")
    parser.add_argument("--auto-batch", action="store_true", help="Automatically export ALL matching words in batches")
    parser.add_argument("--output-dir", type=str, default="data/grok_batches", help="Directory for batch files")
    
    args = parser.parse_args()
    
    if args.auto_batch:
        # Full export mode
        with Session(engine) as session:
            # Build query count
            query_count = select(func.count()).select_from(Word)
            
            # Reconstruct filter logic (duplicated from main function, ideally refactor)
            if args.status:
                query_count = query_count.where(Word.status == args.status)
            else:
                query_count = query_count.where(
                    or_(
                        Word.definition_es == None,
                        Word.definition_es == "[PENDING]",
                        Word.definition_es == "",
                        Word.status == "review"
                    )
                )
            
            total_words = session.exec(query_count).one()
            
        print(f"📦 Auto-Batch Mode: Found {total_words} words total.")
        
        if total_words == 0:
            print("No words to export.")
            sys.exit(0)
            
        batch_size = args.limit
        total_batches = (total_words + batch_size - 1) // batch_size
        
        print(f"Generating {total_batches} batches of size {batch_size}...")
        
        os.makedirs(args.output_dir, exist_ok=True)
        
        for i in range(total_batches):
            current_offset = i * batch_size
            batch_num = i + 1
            filename = f"batch_{batch_num}_of_{total_batches}.md"
            filepath = os.path.join(args.output_dir, filename)
            
            print(f"  - Generating Batch {batch_num}/{total_batches} (Offset {current_offset})...")
            export_vocab_for_grok(filepath, limit=batch_size, offset=current_offset, status_filter=args.status)
            
        print(f"\n✅ All batches generated in '{args.output_dir}/'")
        
    else:
        # Single manual export
        export_vocab_for_grok(args.output, args.limit, args.offset, args.status)
