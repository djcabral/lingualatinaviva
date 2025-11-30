"""
Script para REGENERAR todos los SVGs con etiquetas en español.
"""

import sys
import json
import spacy
from spacy import displacy
from pathlib import Path
from sqlmodel import Session, select
# Añadir directorio raíz al path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from database.connection import engine
from database.syntax_models import SentenceAnalysis

# Mapeo de etiquetas UD a español pedagógico
DEP_LABELS_ES = {
    "nsubj": "Sujeto",
    "obj": "Obj. Directo",
    "iobj": "Obj. Indirecto",
    "obl": "Complemento",
    "advmod": "Modificador",
    "amod": "Adjetivo",
    "root": "Raíz",
    "ROOT": "Raíz",
    "conj": "Coordinado",
    "cc": "Conjunción",
    "case": "Preposición",
    "mark": "Subord.",
    "acl": "Cláus. Adj.",
    "advcl": "Cláus. Adv.",
    "xcomp": "Compl. Pred.",
    "ccomp": "Compl. Orac.",
    "punct": "Puntuación",
    "det": "Determinante",
    "appos": "Aposición",
    "nummod": "Numeral",
    "aux": "Auxiliar",
    "cop": "Cópula",
    "nmod": "Modificador",
    "flat": "Nombre Propio",
    "compound": "Compuesto",
    "vocative": "Vocativo",
    "discourse": "Discurso",
    "expl": "Expletivo",
    "fixed": "Expresión Fija",
    "parataxis": "Parataxis",
    "orphan": "Elipsis",
    "goeswith": "Continúa",
    "reparandum": "Reparación",
    "dep": "Dependencia"
}

def regenerate_all_svgs():
    print("🎨 Regenerando TODOS los SVGs con etiquetas en español...")
    
    with Session(engine) as session:
        # Buscar TODAS las oraciones (no solo las que faltan)
        query = select(SentenceAnalysis).where(SentenceAnalysis.dependency_json != "[]")
        sentences = session.exec(query).all()
        
        count = 0
        for sent in sentences:
            print(f"🔄 Procesando: {sent.latin_text[:40]}...")
            
            try:
                deps = json.loads(sent.dependency_json)
                
                # Construir formato manual para displacy
                words = []
                arcs = []
                
                # Map id -> index (0-based)
                id_to_idx = {t['id']: i for i, t in enumerate(deps)}
                
                for t in deps:
                    words.append({"text": t["text"], "tag": t["pos"]})
                    
                    if t["head"] != 0:  # Skip root self-loop or 0-head
                        head_idx = id_to_idx.get(t["head"])
                        child_idx = id_to_idx.get(t["id"])
                        
                        if head_idx is not None and child_idx is not None:
                            start = min(head_idx, child_idx)
                            end = max(head_idx, child_idx)
                            raw_label = t["dep"]
                            label = DEP_LABELS_ES.get(raw_label, raw_label)  # Traducir a español
                            direction = "left" if child_idx < head_idx else "right"
                            
                            arcs.append({
                                "start": start, 
                                "end": end, 
                                "label": label, 
                                "dir": direction
                            })
                
                manual_data = {
                    "words": words,
                    "arcs": arcs
                }
                
                svg = displacy.render(manual_data, style="dep", manual=True, options={"compact": False, "bg": "#ffffff", "distance": 100})
                
                # Guardar SVG
                sent.tree_diagram_svg = svg
                session.add(sent)
                count += 1
                
            except Exception as e:
                print(f"⚠️ Error generando SVG para '{sent.latin_text}': {e}")
        
        session.commit()
        print(f"✅ Se regeneraron {count} SVGs.")

if __name__ == "__main__":
    regenerate_all_svgs()
