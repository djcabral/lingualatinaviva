#!/usr/bin/env python3
"""
Aplica las correcciones de la IA al análisis sintáctico en la base de datos.
"""
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import get_session
from database import SentenceAnalysis
from sqlmodel import select

import json
import os

# Todas las correcciones de la IA (7 lotes)
AI_CORRECTIONS = {

    # Lote 1 (1-20) - Solo los errores
    2: {2: "complemento_circunstancial", 3: "cópula"},
    5: {2: "objeto_directo"},
    6: {3: "oración_de_relativo", 5: "sujeto", 6: "modificador_adjetival"},
    7: {2: "complemento_predicativo"},
    8: {2: "complemento_predicativo"},
    12: {0: "sujeto"},
    13: {2: "complemento_predicativo"},
    18: {3: "complemento_predicativo"},
    19: {1: "objeto_indirecto"},
    20: {0: "sujeto", 3: "complemento_predicativo"},
    
    # Lote 2 (21-40)
    21: {1: "objeto_indirecto"},
    22: {3: "complemento_predicativo"},
    23: {1: "objeto_indirecto"},
    24: {3: "complemento_predicativo"},
    25: {1: "objeto_indirecto"},
    27: {0: "sujeto"},
    28: {2: "complemento_circunstancial"},
    34: {2: "sujeto", 4: "complemento_predicativo"},
    
    # Lote 3 (41-60)
    50: {2: "complemento_predicativo", 4: "complemento_predicativo"},
    51: {3: "complemento_predicativo"},
    54: {1: "complemento_circunstancial"},
    56: {3: "complemento_predicativo"},
    57: {3: "complemento_predicativo"},
    
    # Lote 4 (61-80)
    62: {1: "modificador_adjetival"},
    63: {1: "objeto_indirecto"},
    66: {0: "objeto_indirecto", 2: "sujeto"},
    67: {0: "objeto_indirecto"},
    68: {2: "complemento_predicativo"},
    69: {0: "sujeto", 1: "complemento_del_nombre", 3: "complemento_predicativo"},
    70: {2: "complemento_predicativo"},
    71: {0: "sujeto"},
    74: {3: "complemento_predicativo"},
    77: {0: "modificador_adverbial"},
    78: {1: "modificador_adjetival"},
    79: {2: "complemento_predicativo"},
    80: {1: "complemento_predicativo"},
    
    # Lote 5 (81-100)
    82: {2: "complemento_predicativo"},
    83: {1: "complemento_predicativo"},
    84: {0: "modificador_adjetival", 1: "sujeto"},
    85: {1: "complemento_predicativo"},
    86: {3: "complemento_predicativo"},
    89: {3: "complemento_circunstancial"},
    94: {3: "complemento_predicativo"},
    95: {1: "objeto_indirecto", 2: "complemento_predicativo"},
    96: {0: "sujeto", 2: "sujeto", 3: "complemento_predicativo"},
    
    # Lote 6 (101-120)
    102: {3: "complemento_predicativo"},
    104: {2: "complemento_predicativo"},
    106: {0: "sujeto"},
    107: {2: "complemento_predicativo"},
    108: {3: "modificador_adjetival"},
    114: {1: "complemento_predicativo"},
    117: {2: "complemento_predicativo"},
    118: {0: "cópula", 1: "complemento_predicativo"},
    
    # Lote 7 (121-140)
    121: {1: "modificador_adjetival"},
    123: {0: "complemento_predicativo"},
    125: {0: "modificador_adjetival"},
    127: {0: "modificador_adjetival", 1: "sujeto"},
    128: {2: "complemento_predicativo"},
    129: {0: "modificador_adjetival"},
    130: {2: "modificador_adverbial"},
    131: {1: "objeto_directo"},
    132: {1: "complemento_predicativo", 3: "sujeto"},
    133: {0: "sujeto", 1: "complemento_predicativo", 3: "sujeto"},
    134: {2: "complemento_predicativo", 4: "sujeto"},
    135: {2: "complemento_predicativo", 3: "complemento_del_nombre"},
    137: {0: "complemento_predicativo"},
    138: {0: "sujeto", 2: "complemento_predicativo"},
    139: {2: "complemento_predicativo", 3: "complemento_circunstancial"},
    139: {2: "complemento_predicativo", 3: "complemento_circunstancial"},
}

# Cargar correcciones adicionales desde JSON si existe
try:
    json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                            "data", "ai_corrections_batch_541_581.json")
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            batch_corrections = json.load(f)
            # Convertir claves de string a int
            for sent_id_str, corrections in batch_corrections.items():
                sent_id = int(sent_id_str)
                processed_corrections = {int(k): v for k, v in corrections.items()}
                AI_CORRECTIONS[sent_id] = processed_corrections
        print(f"Cargadas {len(batch_corrections)} correcciones del lote 541-581")
except Exception as e:
    print(f"Error cargando correcciones JSON: {e}")



def apply_corrections():
    """Aplica las correcciones de la IA a la base de datos."""
    
    with get_session() as session:
        corrected_count = 0
        
        for sent_id, corrections in AI_CORRECTIONS.items():
            sent = session.exec(
                select(SentenceAnalysis).where(SentenceAnalysis.id == sent_id)
            ).first()
            
            if not sent:
                print(f"⚠️ Oración {sent_id} no encontrada")
                continue
            
            # Cargar roles actuales
            try:
                roles = json.loads(sent.syntax_roles or "{}")
                deps = json.loads(sent.dependency_json or "[]")
            except:
                print(f"⚠️ Error parseando oración {sent_id}")
                continue
            
            # Crear mapa inverso: token_id -> rol_actual
            id_to_role = {}
            for role, ids in roles.items():
                for tid in ids:
                    id_to_role[tid] = role
            
            # Aplicar correcciones
            for token_idx, new_role in corrections.items():
                old_role = id_to_role.get(token_idx)
                
                # Remover del rol anterior
                if old_role and old_role in roles:
                    if token_idx in roles[old_role]:
                        roles[old_role].remove(token_idx)
                    if not roles[old_role]:
                        del roles[old_role]
                
                # Añadir al nuevo rol
                if new_role not in roles:
                    roles[new_role] = []
                if token_idx not in roles[new_role]:
                    roles[new_role].append(token_idx)
                
                id_to_role[token_idx] = new_role
            
            # Guardar
            sent.syntax_roles = json.dumps(roles, ensure_ascii=False)
            session.add(sent)
            corrected_count += 1
        
        session.commit()
        print(f"✅ {corrected_count} oraciones corregidas con análisis de IA")


def apply_corrections_from_file(file_path: str):
    """Aplica correcciones desde un archivo JSON con el nuevo format (lista de objetos)."""
    
    if not os.path.exists(file_path):
        print(f"❌ Archivo no encontrado: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📄 Procesando {len(data)} oraciones de: {file_path}")
    
    with get_session() as session:
        corrected_count = 0
        verified_count = 0
        
        for item in data:
            sent_id = item["id"]
            corrections_list = item.get("corrections", [])
            
            sent = session.exec(
                select(SentenceAnalysis).where(SentenceAnalysis.id == sent_id)
            ).first()
            
            if not sent:
                print(f"⚠️ Oración {sent_id} no encontrada")
                continue
            
            # Cargar roles actuales
            try:
                roles = json.loads(sent.syntax_roles or "{}")
            except:
                print(f"⚠️ Error parseando roles de oración {sent_id}")
                continue
            
            # Crear mapa inverso: token_id -> rol_actual
            id_to_role = {}
            for role, ids in roles.items():
                for tid in ids:
                    id_to_role[tid] = role
            
            has_changes = False
            
            for corr in corrections_list:
                # Solo aplicamos si está marcado como incorrecto O si los roles difieren (robustez)
                # A veces la IA marca is_correct: false pero pone el rol correcto
                should_fix = not corr.get("is_correct", True)
                
                # Check explícito de diferencia
                current_role = corr.get("current_role")
                correct_role = corr.get("correct_role")
                
                if current_role != correct_role:
                    should_fix = True
                
                if should_fix and correct_role:
                    t_idx = corr["idx"]
                    
                    # Lógica de actualización
                    old_role = id_to_role.get(t_idx)
                    
                    # Remover del rol anterior
                    if old_role and old_role in roles:
                        if t_idx in roles[old_role]:
                            roles[old_role].remove(t_idx)
                        if not roles[old_role]:
                            del roles[old_role]
                    
                    # Añadir al nuevo rol
                    if correct_role not in roles:
                        roles[correct_role] = []
                    if t_idx not in roles[correct_role]:
                        roles[correct_role].append(t_idx)
                    
                    id_to_role[t_idx] = correct_role
                    has_changes = True
            
            # Siempre marcamos como verificada porque la IA la revisó
            sent.verified = True
            
            if has_changes:
                sent.syntax_roles = json.dumps(roles, ensure_ascii=False)
                session.add(sent)
                corrected_count += 1
            else:
                # Si no hubo cambios pero se verificó, guardamos el flag verified
                session.add(sent)
                verified_count += 1
        
        session.commit()
        print(f"✅ {corrected_count} oraciones corregidas.")
        print(f"✅ {verified_count} oraciones verificadas sin cambios.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?", help="Archivo JSON con correcciones")
    args = parser.parse_args()
    
    if args.file:
        apply_corrections_from_file(args.file)
    else:
        # Comportamiento legacy
        apply_corrections()
