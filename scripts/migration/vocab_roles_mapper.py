#!/usr/bin/env python3
"""
Script para generar automáticamente los roles sintácticos (syntax_roles)
basándose en el análisis de dependencias (dependency_json) existente.
"""

import sys
import os
import json
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.connection import get_session
from database import SentenceAnalysis
from sqlmodel import select

# Mapeo COMPLETO de UD tags a Roles UI (etiquetas en ESPAÑOL)
# Cubre todas las dependencias de Universal Dependencies usadas por LatinCy
DEPENDENCY_TO_ROLE = {
    # === SUJETO ===
    "nsubj": "sujeto",
    "csubj": "sujeto",
    "nsubj:pass": "sujeto_paciente",
    
    # === PREDICADO Y VERBOS ===
    "root": "predicado",
    "cop": "cópula",
    "aux": "auxiliar",
    "aux:pass": "auxiliar_pasivo",
    
    # === OBJETOS ===
    "obj": "objeto_directo",
    "ccomp": "oración_completiva",
    "xcomp": "complemento_predicativo",
    "iobj": "objeto_indirecto",
    
    # === COMPLEMENTOS CIRCUNSTANCIALES ===
    "obl": "complemento_circunstancial",
    "obl:tmod": "complemento_temporal",
    "obl:arg": "complemento_obligatorio",
    "advmod": "modificador_adverbial",
    "advcl": "oración_adverbial",
    
    # === MODIFICADORES ===
    "amod": "modificador_adjetival",
    "nmod": "complemento_del_nombre",
    "nummod": "modificador_numeral",
    "acl": "oración_adjetiva",
    "acl:relcl": "oración_de_relativo",
    "relcl": "oración_de_relativo",
    
    # === DETERMINANTES ===
    "det": "determinante",
    
    # === APOSICIÓN ===
    "appos": "aposición",
    
    # === CONJUNCIONES ===
    "cc": "conjunción_coordinante",
    "conj": "elemento_coordinado",
    "mark": "conjunción_subordinante",
    
    # === PREPOSICIONES ===
    "case": "preposición",
    
    # === VOCATIVO ===
    "vocative": "vocativo",
    
    # === PUNTUACIÓN ===
    "punct": "puntuación",
    
    # === ESTRUCTURAS ESPECIALES ===
    "flat": "nombre_compuesto",
    "flat:name": "nombre_compuesto",
    "compound": "compuesto",
    "fixed": "expresión_fija",
    "discourse": "marcador_discursivo",
    "orphan": "huérfano",
    "dep": "dependencia",
    "expl": "expletivo",
    "parataxis": "parataxis",
    "list": "elemento_de_lista",
    "dislocated": "dislocado",
    "reparandum": "reparación",
    "goeswith": "fragmento"
}

def map_roles(dependency_json_str):
    try:
        tokens = json.loads(dependency_json_str)
    except:
        return {}
    
    roles = defaultdict(list)
    
    for token in tokens:
        dep = token.get("dep", "").lower()
        tid = token.get("id")
        
        role = DEPENDENCY_TO_ROLE.get(dep)
        
        # Fallback heurístico para casos no mapeados
        if not role:
            if "subj" in dep: role = "sujeto"
            elif "obj" in dep: role = "objeto_directo"
            elif "mod" in dep: role = "modificador"
            else: role = "otro"  # Siempre asignar algo
        
        if tid is not None:
            roles[role].append(tid)
            
    return dict(roles)

def main():
    with get_session() as session:
        sentences = session.exec(select(SentenceAnalysis)).all()
        updated = 0
        for sent in sentences:
            if not sent.dependency_json or sent.dependency_json == "[]": continue
            new_roles = map_roles(sent.dependency_json)
            if new_roles:
                sent.syntax_roles = json.dumps(new_roles)
                session.add(sent)
                updated += 1
        session.commit()
        print(f"✅ {updated} oraciones actualizadas con roles sintácticos.")

if __name__ == "__main__":
    main()
