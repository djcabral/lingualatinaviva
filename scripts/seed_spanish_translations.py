#!/usr/bin/env python3
"""
Completa las traducciones al español para palabras legacy.
Usa diccionario manual para palabras comunes y fallback.
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.connection import get_session
from database import Word
from sqlmodel import select

# Diccionario manual para palabras comunes legacy que sabemos que faltan
MANUAL_TRANSLATIONS = {
    # Verbos básicos
    "amo": "amar, querer",
    "sum": "ser, estar, existir",
    "do": "dar, conceder",
    "laudo": "alabar, elogiar",
    "habeo": "tener, poseer",
    "porto": "llevar, portar",
    "voco": "llamar, invocar",
    "moneo": "advertir, aconsejar",
    "video": "ver, mirar",
    "timeo": "temer",
    "debeo": "deber",
    "pugno": "luchar, combatir",
    "rego": "gobernar, regir",
    "duco": "conducir, guiar",
    "mitto": "enviar",
    "vinco": "vencer, conquistar",
    "credo": "creer, confiar",
    "paro": "preparar",
    "ago": "hacer, actuar, conducir",
    "dico": "decir",
    "facio": "hacer",
    "capio": "tomar, capturar",
    "fui": "fui (ser/estar)",
    "habui": "tuve",
    "veni": "vine",
    "ero": "seré/estaré",
    "habebo": "tendré",
    "veniam": "vendré",
    
    # Sustantivos
    "rosa": "rosa",
    "puella": "niña, muchacha",
    "femina": "mujer",
    "dominus": "señor, dueño",
    "servus": "esclavo, siervo",
    "puer": "niño",
    "templum": "templo",
    "bellum": "guerra",
    "nauta": "marinero",
    "poeta": "poeta",
    "ager": "campo",
    "rex": "rey",
    "miles": "soldado",
    "corpus": "cuerpo",
    "urbs": "ciudad",
    "victoria": "victoria",
    "gloria": "gloria",
    "fortuna": "fortuna, suerte",
    "memoria": "memoria",
    "lex": "ley",
    "pax": "paz",
    "dux": "líder, guía",
    "lux": "luz",
    "nox": "noche",
    "manus": "mano, grupo",
    "exercitus": "ejército",
    "domus": "casa",
    "fructus": "fruto",
    "res": "cosa, asunto",
    "dies": "día",
    "spes": "esperanza",
    "fides": "fe, lealtad",
    
    # Adjetivos
    "bonus": "bueno",
    "magnus": "grande",
    "pulcher": "hermoso",
    "liber": "libre",
    "tristis": "triste",
    "fortis": "fuerte, valiente",
    "brevis": "breve, corto",
    "acer": "agudo, ardiente",
    "facilis": "fácil",
    
    # Palabras adicionales identificadas en verificación
    "primus": "primero",
    "ubi": "donde",
    "lego": "leer, recoger",
    "audio": "oír, escuchar",
    "venio": "venir",
    "scribo": "escribir",
    "vivo": "vivir",
    "dormio": "dormir",
    "scio": "saber",
    "homo": "hombre, ser humano",
    "mulier": "mujer",
    "pater": "padre",
    "mater": "madre",
    "frater": "hermano",
    "consul": "cónsul",
    "virtus": "virtud, valor",
    "amor": "amor",
    "civis": "ciudadano",
    "mons": "monte, montaña",
    "fons": "fuente",
    "navis": "nave, barco",
    "opus": "obra, trabajo",
    "nomen": "nombre",
    "senatus": "senado",
    "portus": "puerto",
    "cornu": "cuerno",
    "genu": "rodilla",
    "species": "aspecto, especie",
    "omnis": "todo, cada",
    "felix": "feliz, afortunado",
    "sapiens": "sabio",
    "prudens": "prudente",
    "audax": "audaz",
    "sentio": "sentir",
    "pono": "poner, colocar",
    "possum": "poder, ser capaz",
    "scio": "saber",
    "mitto": "enviar",
}

def populate_spanish_translations():
    print("🌱 Completando traducciones al español...")
    
    with get_session() as session:
        # Buscar palabras sin definición en español
        words_without_es = session.exec(
            select(Word).where(Word.definition_es.is_(None))
        ).all()
        
        print(f"ℹ️  Encontradas {len(words_without_es)} palabras sin traducción ES")
        
        updated_count = 0
        
        for word in words_without_es:
            # Normalizar para búsqueda (quitar macrones si los hubiera, aunque en DB suelen estar limpios en 'latin')
            # Aquí asumimos que word.latin está limpio o coincide con las claves
            
            latin_key = word.latin.lower().strip()
            
            if latin_key in MANUAL_TRANSLATIONS:
                word.definition_es = MANUAL_TRANSLATIONS[latin_key]
                session.add(word)
                updated_count += 1
                print(f"   ✅ {word.latin} -> {word.definition_es}")
            else:
                # Si no está en el manual, intentamos usar la traducción en inglés si es simple
                # Esto es un fallback temporal, idealmente usaríamos Collatinus
                pass
        
        session.commit()
        print(f"\n✅ Total palabras actualizadas: {updated_count}")
        
        # Verificar estado final
        total = session.exec(select(Word)).all()
        with_es = [w for w in total if w.definition_es]
        print(f"📊 Estado actual: {len(with_es)}/{len(total)} ({int(len(with_es)/len(total)*100)}%) tienen español")

if __name__ == "__main__":
    populate_spanish_translations()
