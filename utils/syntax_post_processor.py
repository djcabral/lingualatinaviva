"""
Post-procesador para corregir errores sistemáticos de LatinCy.

Basado en análisis comparativo con IA (Claude/Grok), corrige patrones de error conocidos:
1. Oraciones copulativas: distinguir predicado vs complemento_predicativo
2. Verbo "sum": distinguir cópula vs auxiliar_pasivo
3. Dativos: complemento_obligatorio/complemento_del_nombre -> objeto_indirecto
4. Posesivos: determinante -> modificador_adjetival
5. AcI: subordinada completiva correctamente etiquetada
"""
import json
from typing import Dict, List, Any

# Lemas de verbos copulativos (nunca son auxiliar_pasivo sin participio)
COPULATIVE_VERBS = {
    "sum", "esse", "fio", "fieri", "videor", "videri", 
    "maneo", "manere", "appareo", "apparere"
}

# Verbos que rigen DATIVO de persona (objeto indirecto) + acusativo de cosa
# Estos dativos NUNCA son sujeto, complemento_del_nombre, ni complemento_obligatorio
DATIVE_VERBS = {
    # Verbos de dar/entregar
    "do", "dare", "dono", "donare", "trado", "tradere", "reddo", "reddere",
    # Verbos de decir/mostrar
    "dico", "dicere", "narro", "narrare", "ostendo", "ostendere", "monstro", "monstrare",
    # Verbos de enviar
    "mitto", "mittere", "scribo", "scribere", "fero", "ferre",
    # Verbos de ordenar/pedir
    "impero", "imperare", "iubeo", "iubere", "rogo", "rogare",
    # Otros verbos con dativo
    "credo", "credere", "pareo", "parere", "placeo", "placere", 
    "noceo", "nocere", "faveo", "favere", "studeo", "studere"
}

# Posesivos latinos
POSSESSIVES = {"meus", "tuus", "suus", "noster", "vester", "eius", "eorum", "earum"}


def post_process_syntax_roles(dependency_json: str, syntax_roles: str) -> str:
    """
    Aplica correcciones post-proceso a los roles sintácticos de LatinCy.
    
    Args:
        dependency_json: JSON con datos de dependencias de spaCy
        syntax_roles: JSON con roles sintácticos actuales
        
    Returns:
        JSON corregido de syntax_roles
    """
    try:
        tokens = json.loads(dependency_json)
        roles = json.loads(syntax_roles)
    except:
        return syntax_roles
    
    if not tokens or not roles:
        return syntax_roles
    
    # Crear mapa de token_id -> token_data
    token_map = {t["id"]: t for t in tokens}
    
    # Crear mapa inverso: token_id -> rol_actual
    id_to_role = {}
    for role, ids in roles.items():
        for tid in ids:
            id_to_role[tid] = role
    
    corrections = []
    
    # === REGLA 1: Oraciones copulativas ===
    # Si hay cópula, el ROOT que es adjetivo/sustantivo es complemento_predicativo, no predicado
    copula_ids = roles.get("cópula", [])
    if copula_ids:
        for tid, role in id_to_role.items():
            token = token_map.get(tid)
            if not token:
                continue
            
            # Si está marcado como predicado pero es ADJ o NOUN, es complemento_predicativo
            if role == "predicado" and token.get("pos") in ["ADJ", "NOUN"]:
                # Verificar que el verbo principal sea copulativo
                head_id = token.get("head")
                head_token = token_map.get(head_id)
                if head_token and head_token.get("lemma", "").lower() in COPULATIVE_VERBS:
                    corrections.append((tid, "predicado", "complemento_predicativo"))
    
    # === REGLA 2: sum como cópula vs auxiliar_pasivo ===
    # Si no hay participio pasado, sum es cópula, no auxiliar_pasivo
    aux_pasivo_ids = roles.get("auxiliar_pasivo", [])
    for tid in aux_pasivo_ids:
        token = token_map.get(tid)
        if not token:
            continue
        
        lemma = token.get("lemma", "").lower()
        if lemma in COPULATIVE_VERBS:
            # Buscar si hay participio pasado en la oración
            has_participle = False
            for t in tokens:
                morph = t.get("morph", "")
                if "VerbForm=Part" in morph and "Voice=Pass" in morph:
                    has_participle = True
                    break
            
            if not has_participle:
                corrections.append((tid, "auxiliar_pasivo", "cópula"))
    
    # === REGLA 3: Dativos con verbos de transferencia ===
    # complemento_obligatorio -> objeto_indirecto para verbos que rigen dativo
    comp_oblig_ids = roles.get("complemento_obligatorio", [])
    for tid in comp_oblig_ids:
        token = token_map.get(tid)
        if not token:
            continue
        
        morph = token.get("morph", "")
        if "Case=Dat" in morph:
            # Verificar si el verbo principal rige dativo
            head_id = token.get("head")
            head_token = token_map.get(head_id)
            if head_token and head_token.get("lemma", "").lower() in DATIVE_VERBS:
                corrections.append((tid, "complemento_obligatorio", "objeto_indirecto"))
    
    # === REGLA 4: Posesivos como modificadores ===
    # determinante -> modificador_adjetival para posesivos
    det_ids = roles.get("determinante", [])
    for tid in det_ids:
        token = token_map.get(tid)
        if not token:
            continue
        
        lemma = token.get("lemma", "").lower()
        if lemma in POSSESSIVES:
            corrections.append((tid, "determinante", "modificador_adjetival"))
    
    # === REGLA 5: Nominativos mal clasificados ===
    # Si tiene Case=Nom y no es sujeto, probablemente debería serlo
    for tid, token in token_map.items():
        morph = token.get("morph", "")
        current_role = id_to_role.get(tid, "")
        
        if "Case=Nom" in morph and token.get("pos") in ["NOUN", "PROPN"]:
            if current_role in ["complemento_del_nombre", "modificador_adjetival"]:
                # Verificar que no haya otro sujeto ya
                if not roles.get("sujeto"):
                    corrections.append((tid, current_role, "sujeto"))
    
    # === REGLA 6: ergo, igitur, itaque son adverbios circunstanciales ===
    DISCOURSE_TO_CIRCUNSTANCIAL = {"ergo", "igitur", "itaque", "tamen", "autem", "enim"}
    disc_ids = roles.get("marcador_discursivo", [])
    for tid in disc_ids:
        token = token_map.get(tid)
        if not token:
            continue
        
        lemma = token.get("lemma", "").lower()
        if lemma in DISCOURSE_TO_CIRCUNSTANCIAL:
            corrections.append((tid, "marcador_discursivo", "modificador_adverbial"))
    
    # === REGLA 7: Dativos mal clasificados como sujeto o complemento_del_nombre ===
    # Con verbos que rigen dativo, el dativo es SIEMPRE objeto_indirecto
    for role_name in ["sujeto", "complemento_del_nombre"]:
        role_ids = roles.get(role_name, [])
        for tid in role_ids:
            token = token_map.get(tid)
            if not token:
                continue
            
            morph = token.get("morph", "")
            if "Case=Dat" in morph:
                # Buscar el verbo principal
                head_id = token.get("head")
                head_token = token_map.get(head_id)
                
                # Si el head directo no es verbo, buscar el ROOT
                if head_token and head_token.get("pos") != "VERB":
                    for t in tokens:
                        if t.get("dep") == "ROOT" and t.get("pos") == "VERB":
                            head_token = t
                            break
                
                if head_token and head_token.get("lemma", "").lower() in DATIVE_VERBS:
                    corrections.append((tid, role_name, "objeto_indirecto"))
    
    # === REGLA 8: Cualquier dativo con verbo de transferencia es objeto_indirecto ===
    # Buscar dativos que estén en complemento_circunstancial pero deberían ser objeto_indirecto
    cc_ids = roles.get("complemento_circunstancial", [])
    for tid in cc_ids:
        token = token_map.get(tid)
        if not token:
            continue
        
        morph = token.get("morph", "")
        if "Case=Dat" in morph:
            head_id = token.get("head")
            head_token = token_map.get(head_id)
            if head_token and head_token.get("lemma", "").lower() in DATIVE_VERBS:
                corrections.append((tid, "complemento_circunstancial", "objeto_indirecto"))

    # === REGLA 9: AcI - Oración completiva de infinitivo ===
    # Si 'ccomp' o 'xcomp' es VERBO en infinitivo, es 'oración_completiva'
    # LatinCy a veces lo marca como objeto_directo
    for tid, unique_role in id_to_role.items():
        token = token_map.get(tid)
        if not token: continue
        
        dep = token.get("dep", "")
        if dep in ["ccomp", "xcomp"]:
            # Verificar si es infinitivo
            is_infinitive = "VerbForm=Inf" in token.get("morph", "")
            if is_infinitive:
                # Si está marcado como objeto_directo, cambiar a oración_completiva
                if unique_role == "objeto_directo":
                    corrections.append((tid, "objeto_directo", "oración_completiva"))
                # O si no tiene rol específico (token podría no estar en roles, pero aquí iteramos roles)
                elif unique_role == "complemento_predicativo": # A veces pasa
                     corrections.append((tid, "complemento_predicativo", "oración_completiva"))

    # === REGLA 10: Ablativo Absoluto ===
    # Buscar participio en ablativo que tenga un sujeto (nsubj) en ablativo
    # Si se encuentra, marcar el participio como 'abl_absoluto'
    for tid, role in id_to_role.items():
        token = token_map.get(tid)
        if not token: continue
        
        if token.get("pos") == "VERB":
            morph = token.get("morph", "")
            if "VerbForm=Part" in morph and "Case=Abl" in morph:
                # Verificar dependientes
                has_abl_subject = False
                for other_id, other_token in token_map.items():
                    if other_token.get("head") == tid:
                        other_morph = other_token.get("morph", "")
                        # Sujeto o nominal en ablativo
                        if ("nsubj" in other_token.get("dep", "") or "nmod" in other_token.get("dep", "")) and "Case=Abl" in other_morph:
                            has_abl_subject = True
                            break
                
                if has_abl_subject and role != "ablativo_absoluto":
                     corrections.append((tid, role, "ablativo_absoluto"))

    # === REGLA 11: Gerundivo con SUM ===
    # Si hay un Gerundivo (VerbForm=Gdv) y su head es SUM, SUM es cópula
    # Y el gerundivo suele ser predicado o complemento_predicativo
    for tid, role in id_to_role.items():
        token = token_map.get(tid)
        if not token: continue
        
        morph = token.get("morph", "")
        if "VerbForm=Gdv" in morph: 
             # Chequear head
             head_id = token.get("head")
             head_token = token_map.get(head_id)
             if head_token and head_token.get("lemma", "").lower() in COPULATIVE_VERBS:
                 # Asegurar que SUM esté marcado como cópula, no auxiliar_pasivo
                 head_role = id_to_role.get(head_id)
                 if head_role != "cópula":
                     corrections.append((head_id, head_role or "predicado", "cópula"))
                 
                 # El gerundivo en esta construcción perifrástica suele actuar como predicado principal semántico
                 # Si está como complemento_predicativo, lo dejamos, pero a veces está como sujeto_paciente (error)
                     if role == "sujeto_paciente":
                         corrections.append((tid, "sujeto_paciente", "complemento_predicativo"))

    # === REGLA 12: Complemento Predicativo en AcI (affirmavit se esse amicum) ===
    # Si hay una oración completiva (infinitive) y un adjetivo/sustantivo depende de ese infinitivo copulativo
    # Ese dependiente es complemento_predicativo
    for tid, role in id_to_role.items():
        token = token_map.get(tid)
        if not token: continue
        
        # Debe ser adjetivo o sustantivo
        if token.get("pos") not in ["ADJ", "NOUN"]: continue

        head_id = token.get("head")
        head_token = token_map.get(head_id)
        
        # El head debe ser infinitivo (oración_completiva)
        if head_token and "VerbForm=Inf" in head_token.get("morph", ""):
            head_role = id_to_role.get(head_id)
            if head_role == "oración_completiva" or head_role == "cópula": # A veces el infinitivo es la cópula de la completiva
                 # Si el token actual es 'modificador_adjetival' (ej. amicum), cambiar a predicativo
                 if role == "modificador_adjetival":
                     corrections.append((tid, "modificador_adjetival", "complemento_predicativo"))

    # === REGLA 13: Verbos de movimiento con destino (Acc sin prep) ===
    # Ciudades/lugares en acusativo con verbos de movimiento son CC, no Obj
    # Ej: Romam veniebant
    MOVEMENT_VERBS = {"venio", "uenio", "eo", "adeo", "proficiscor", "curro", "fugio"}
    for tid, role in id_to_role.items():
        token = token_map.get(tid)
        if not token: continue
        
        if role == "objeto_directo" and token.get("pos") in ["PROPN", "NOUN"]:
             # Check lema del verbo
             head_id = token.get("head")
             head_token = token_map.get(head_id)
             if head_token and head_token.get("lemma", "").lower() in MOVEMENT_VERBS:
                 # Si es Propn (ciudad) o Noun (domum, rus)
                 lemma = token.get("lemma", "").lower()
                 if token.get("pos") == "PROPN" or lemma in ["domus", "rus"]:
                     corrections.append((tid, "objeto_directo", "complemento_circunstancial"))


    
    # Aplicar correcciones
    for tid, old_role, new_role in corrections:
        # Remover del rol anterior
        if old_role in roles and tid in roles[old_role]:
            roles[old_role].remove(tid)
            if not roles[old_role]:
                del roles[old_role]
        
        # Añadir al nuevo rol
        if new_role not in roles:
            roles[new_role] = []
        if tid not in roles[new_role]:
            roles[new_role].append(tid)
    
    return json.dumps(roles, ensure_ascii=False)


def apply_corrections_to_database():
    """Aplica las correcciones a todas las oraciones en la base de datos."""
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from database.connection import get_session
    from database import SentenceAnalysis
    from sqlmodel import select
    
    with get_session() as session:
        sentences = session.exec(select(SentenceAnalysis)).all()
        
        corrected = 0
        for sent in sentences:
            if not sent.dependency_json or sent.dependency_json == "[]":
                continue
            
            original_roles = sent.syntax_roles
            corrected_roles = post_process_syntax_roles(sent.dependency_json, original_roles)
            
            if corrected_roles != original_roles:
                sent.syntax_roles = corrected_roles
                session.add(sent)
                corrected += 1
        
        session.commit()
        print(f"✅ {corrected} oraciones corregidas con post-procesamiento.")


if __name__ == "__main__":
    apply_corrections_to_database()
