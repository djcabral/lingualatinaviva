"""
Popula la tabla InflectedForm con todas las formas inflectadas de las palabras en la BD
Este proceso se ejecuta una vez para pre-generar todas las formas posibles.
"""

import json
import sys
import os

# Add project root to path if needed
if not any('latin-python' in p for p in sys.path):
    sys.path.insert(0, os.getcwd())

from database.connection import get_session
from database.models import Word, InflectedForm
from utils.latin_logic import LatinMorphology
from sqlmodel import select


def parse_form_key_noun(form_key: str) -> dict:
    """
    Convierte una clave de forma nominal (ej: 'nom_sg') a dict morfológico
    Returns: {"case": "nom", "number": "sg"}
    """
    parts = form_key.split("_")
    if len(parts) == 2:
        case_map = {
            "nom": "nom",
            "voc": "voc", 
            "gen": "gen",
            "dat": "dat",
            "acc": "acc",
            "abl": "abl"
        }
        number_map = {"sg": "sg", "pl": "pl"}
        
        return {
            "case": case_map.get(parts[0], parts[0]),
            "number": number_map.get(parts[1], parts[1])
        }
    return {}


def parse_form_key_verb(form_key: str) -> dict:
    """
    Convierte una clave de forma verbal (ej: 'pres_1sg', 'perf_pass_3pl') a dict morfológico
    Returns: {"tense": "pres", "person": "1", "number": "sg", "mood": "ind", "voice": "act"}
    """
    parts = form_key.split("_")
    
    result = {}
    
    # Mapear tiempo
    tense_map = {
        "pres": "pres",
        "imp": "imp",
        "fut": "fut",
        "perf": "perf",
        "plup": "plup",
        "futperf": "futperf"
    }
    
    # Mapear modo
    mood_map = {
        "ind": "ind",
        "subj": "subj",
        "imv": "imv"
    }
    
    # Determinar voz (si contiene "pass" es pasiva)
    voice = "pass" if "pass" in parts else "act"
    result["voice"] = voice
    
    # Extraer tiempo (primera parte)
    if parts[0] in tense_map:
        result["tense"] = tense_map[parts[0]]
    
    # Extraer modo (si está explícito)
    for part in parts:
        if part in mood_map:
            result["mood"] = mood_map[part]
    
    # Si no hay modo explícito, asumir indicativo
    if "mood" not in result:
        # Subjuntivo e imperativo tienen marcadores explícitos
        result["mood"] = "ind"
    
    # Extraer persona y número (último elemento como "1sg", "2pl", etc)
    person_number = parts[-1]
    if len(person_number) >= 2:
        if person_number[0].isdigit():
            result["person"] = person_number[0]
            result["number"] = person_number[1:]
    
    return result


def populate_inflected_forms():
    """Genera todas las formas inflectadas para cada palabra en la DB"""
    
    print("🔄 Iniciando población de formas inflectadas...")
    
    with get_session() as session:
        # Primero, limpiar la tabla existente
        print("🗑️  Limpiando tabla InflectedForm...")
        existing_forms = session.exec(select(InflectedForm)).all()
        for form in existing_forms:
            session.delete(form)
        session.commit()
        
        # Obtener todas las palabras activas
        words = session.exec(select(Word).where(Word.status == "active")).all()
        print(f"📚 Procesando {len(words)} palabras...\n")
        
        total_forms = 0
        processed_words = 0
        
        for word in words:
            forms_added = 0
            
            # SUSTANTIVOS
            if word.part_of_speech == "noun":
                if not word.declension or not word.gender:
                    print(f"⚠️  Saltando {word.latin}: falta declension o gender")
                    continue
                
                forms_dict = LatinMorphology.decline_noun(
                    word.latin, 
                    word.declension, 
                    word.gender, 
                    word.genitive or "",
                    word.irregular_forms,
                    word.parisyllabic
                )
                
                for form_key, form_value in forms_dict.items():
                    if form_value and form_value != "-":
                        morphology = parse_form_key_noun(form_key)
                        
                        inflected = InflectedForm(
                            form=form_value,
                            normalized_form=LatinMorphology.normalize_latin(form_value),
                            word_id=word.id,
                            morphology=json.dumps(morphology)
                        )
                        session.add(inflected)
                        forms_added += 1
            
            # VERBOS
            elif word.part_of_speech == "verb":
                if not word.conjugation or not word.principal_parts:
                    print(f"⚠️  Saltando {word.latin}: falta conjugation o principal_parts")
                    continue
                
                forms_dict = LatinMorphology.conjugate_verb(
                    word.latin,
                    word.conjugation,
                    word.principal_parts,
                    word.irregular_forms
                )
                
                for form_key, form_value in forms_dict.items():
                    if form_value and form_value != "-":
                        morphology = parse_form_key_verb(form_key)
                        
                        inflected = InflectedForm(
                            form=form_value,
                            normalized_form=LatinMorphology.normalize_latin(form_value),
                            word_id=word.id,
                            morphology=json.dumps(morphology)
                        )
                        session.add(inflected)
                        forms_added += 1
            
            # ADJETIVOS
            elif word.part_of_speech == "adjective":
                # Los adjetivos se declinan como sustantivos en sus 3 géneros
                if not word.declension:
                    print(f"⚠️  Saltando {word.latin}: falta declension")
                    continue
                
                for gender in ["m", "f", "n"]:
                    forms_dict = LatinMorphology.decline_noun(
                        word.latin,
                        word.declension,
                        gender,
                        word.genitive or "",
                        word.irregular_forms,
                        word.parisyllabic
                    )
                    
                    for form_key, form_value in forms_dict.items():
                        if form_value and form_value != "-":
                            morphology = parse_form_key_noun(form_key)
                            morphology["gender"] = gender  # Agregar género
                            
                            inflected = InflectedForm(
                                form=form_value,
                                normalized_form=LatinMorphology.normalize_latin(form_value),
                                word_id=word.id,
                                morphology=json.dumps(morphology)
                            )
                            session.add(inflected)
                            forms_added += 1
            
            # PALABRAS INVARIABLES
            elif word.is_invariable:
                # Agregar la forma tal cual
                inflected = InflectedForm(
                    form=word.latin,
                    normalized_form=LatinMorphology.normalize_latin(word.latin),
                    word_id=word.id,
                    morphology=json.dumps({"invariable": True})
                )
                session.add(inflected)
                forms_added += 1
            
            if forms_added > 0:
                processed_words += 1
                total_forms += forms_added
                if processed_words % 50 == 0:
                    print(f"  ✅ {processed_words} palabras procesadas, {total_forms} formas generadas...")
        
        # Commit todos los cambios
        print("\n💾 Guardando en base de datos...")
        session.commit()
        
        print(f"\n✅ ¡Completado!")
        print(f"   📊 Palabras procesadas: {processed_words}")
        print(f"   📝 Formas inflectadas generadas: {total_forms}")
        print(f"   📈 Promedio: {total_forms/processed_words if processed_words > 0 else 0:.1f} formas por palabra")


if __name__ == "__main__":
    try:
        populate_inflected_forms()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
