"""
Script para importar muestras de textos clásicos desde archivo local
"""
import sys
import os
from pathlib import Path

# Add project root to path
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_path not in sys.path:
    sys.path.append(root_path)

from database.connection import get_session
from database.syntax_models import SentenceAnalysis

def import_local_samples():
    print("="*60)
    print("IMPORTANDO MUESTRAS CLÁSICAS (LOCAL)")
    print("="*60)
    
    file_path = Path(root_path) / "data" / "texts" / "classical_samples.txt"
    
    if not file_path.exists():
        print(f"❌ No se encontró {file_path}")
        return

    with get_session() as session:
        count = 0
        current_source = ""
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                
                # Parsear [source] text
                if line.startswith("[") and "]" in line:
                    parts = line.split("]", 1)
                    source = parts[0].replace("[", "").strip()
                    text = parts[1].strip()
                else:
                    text = line
                    source = "classical_misc"
                
                # Determinar nivel base
                level = 5
                if "phaedrus" in source: level = 4
                elif "eutropius" in source: level = 5
                elif "caesar" in source: level = 6
                
                # Verificar duplicados
                exists = session.query(SentenceAnalysis).filter(
                    SentenceAnalysis.latin_text == text
                ).first()
                
                if exists:
                    continue
                
                # Crear entrada (sin análisis profundo por ahora)
                analysis = SentenceAnalysis(
                    latin_text=text,
                    spanish_translation="[Traducción pendiente]",
                    source=source,
                    complexity_level=level,
                    sentence_type="complex" if len(text) > 50 else "simple"
                )
                
                session.add(analysis)
                count += 1
                print(f"  Importada ({source}): {text[:40]}...")
        
        session.commit()
        print(f"\n✅ Total importado: {count} oraciones")

if __name__ == "__main__":
    import_local_samples()
