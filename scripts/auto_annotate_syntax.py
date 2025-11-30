"""
Script para generar automáticamente anotaciones pedagógicas preliminares
basadas en el análisis de LatinCy.
Esto permite mover oraciones de la "Zona de Espera" al "Corpus Verificado"
para su posterior revisión manual.
"""

import sys
import json
from pathlib import Path
# Añadir directorio raíz al path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from sqlmodel import Session, select
from database.connection import engine
from database.syntax_models import SentenceAnalysis, TokenAnnotation, SentenceStructure

# Mapeo de dependencias de LatinCy a roles pedagógicos
DEP_TO_ROLE = {
    "nsubj": "Sujeto",
    "obj": "Objeto Directo",
    "iobj": "Objeto Indirecto",
    "obl": "Complemento Circunstancial",
    "advmod": "Adverbio / Modificador",
    "amod": "Adjetivo / Modificador",
    "root": "Núcleo del Predicado",
    "ROOT": "Núcleo del Predicado",
    "conj": "Coordinado",
    "cc": "Conjunción",
    "case": "Preposición",
    "mark": "Conjunción Subordinante",
    "acl": "Cláusula Adjetiva",
    "advcl": "Cláusula Adverbial",
    "xcomp": "Complemento Predicativo",
    "ccomp": "Complemento Oracional",
    "punct": "Puntuación",
    "det": "Determinante",
    "appos": "Aposición",
    "nummod": "Numeral"
}

# Mapeo de casos a funciones básicas
CASE_FUNCTIONS = {
    "Nom": "Nominativo Sujeto",
    "Acc": "Acusativo",
    "Dat": "Dativo",
    "Gen": "Genitivo",
    "Abl": "Ablativo",
    "Voc": "Vocativo"
}

def auto_annotate_sentences():
    print("🤖 Iniciando auto-anotación de oraciones...")
    
    with Session(engine) as session:
        # Buscar oraciones sin anotaciones (o incompletas)
        # Por simplicidad, buscamos las que tienen 0 anotaciones primero
        query = select(SentenceAnalysis)
        sentences = session.exec(query).all()
        
        count = 0
        for sent in sentences:
            # Verificar si ya está completa
            try:
                deps = json.loads(sent.dependency_json)
                if not deps:
                    continue
                    
                if len(sent.token_annotations) == len(deps):
                    continue # Ya está completa
                
                print(f"📝 Anotando: {sent.latin_text[:50]}...")
                
                # Limpiar anotaciones parciales si existen (para regenerar limpio)
                for ann in sent.token_annotations:
                    session.delete(ann)
                
                # Generar nuevas anotaciones
                for i, token in enumerate(deps):
                    dep = token.get("dep", "")
                    pos = token.get("pos", "")
                    morph_str = token.get("morph", "")
                    
                    # Determinar Rol
                    role = DEP_TO_ROLE.get(dep, "Elemento Sintáctico")
                    
                    # Determinar Función de Caso (si aplica)
                    case_func = None
                    explanation = "Generado automáticamente."
                    
                    if "Case=" in morph_str:
                        for part in morph_str.split('|'):
                            if part.startswith("Case="):
                                case = part.split('=')[1]
                                case_func = CASE_FUNCTIONS.get(case, f"Caso {case}")
                                break
                    
                    if pos == "VERB":
                        case_func = "Verbo"
                    
                    annotation = TokenAnnotation(
                        sentence_id=sent.id,
                        token_index=i,
                        token_text=token["text"],
                        pedagogical_role=role,
                        case_function=case_func,
                        explanation=explanation
                    )
                    session.add(annotation)
                
                # Generar estructura básica si no existe
                if not sent.structures:
                    struct = SentenceStructure(
                        sentence_id=sent.id,
                        clause_type="Principal (Auto)",
                        notes="Estructura generada automáticamente."
                    )
                    session.add(struct)
                
                count += 1
                
            except Exception as e:
                print(f"❌ Error en oración {sent.id}: {e}")
                continue
        
        session.commit()
        print(f"✅ Se han auto-anotado {count} oraciones.")

if __name__ == "__main__":
    auto_annotate_sentences()
