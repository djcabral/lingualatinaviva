#!/usr/bin/env python3
"""
Script to process all existing Texts in the database.
Generates:
1. Linked Vocabulary (TextWordLink) for Tooltips
2. Syntax Analysis (SentenceAnalysis) for Trees/Charts
"""

import sys
import os
import logging
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

from utils.content_loader import ContentLoader
from database.connection import get_session
from database import Text
from sqlmodel import select

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    print("="*60)
    print("📚 PROCESADOR DE TEXTOS MASIVO")
    print("="*60)
    print("Iniciando carga de modelos NLP (esto puede tardar un poco)...")
    
    start_time = time.time()
    
    try:
        loader = ContentLoader()
        if not loader.nlp:
            print("❌ Error: No se pudo cargar Stanza. Abortando.")
            return
    except Exception as e:
        print(f"❌ Error fatal inicializando loader: {e}")
        return
        
    print("✅ Modelos cargados correctamente.")
    
    with get_session() as session:
        texts = session.exec(select(Text)).all()
        total_texts = len(texts)
        print(f"\nEncontrados {total_texts} textos para procesar.\n")
        
        total_sents = 0
        total_links = 0
        errors = 0
        
        for i, text in enumerate(texts, 1):
            print(f"[{i}/{total_texts}] Procesando: {text.title} (ID: {text.id})... ", end="", flush=True)
            
            try:
                result = loader.process_text_content(text.id)
                
                s_count = result.get("sentences", 0)
                l_count = result.get("links", 0)
                e_count = result.get("errors", 0)
                
                total_sents += s_count
                total_links += l_count
                errors += e_count
                
                if e_count > 0:
                    print(f"⚠️  Completado con {e_count} errores.")
                else:
                    print(f"✅ OK ({s_count} oraciones, {l_count} links)")
                    
            except Exception as e:
                print(f"❌ FALLÓ: {e}")
                errors += 1
                
    duration = time.time() - start_time
    print("\n" + "="*60)
    print("RESUMEN DE EJECUCIÓN")
    print("="*60)
    print(f"Tiempo total: {duration:.2f} segundos")
    print(f"Textos procesados: {total_texts}")
    print(f"Oraciones analizadas: {total_sents}")
    print(f"Enlaces creados (Tooltips): {total_links}")
    print(f"Errores: {errors}")
    print("="*60)

if __name__ == "__main__":
    main()
