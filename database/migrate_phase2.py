"""
Script de Migración Fase 2: Vocabulario y Excepciones

1. Añade columna 'irregular_forms' a la tabla Word
2. Inserta palabras con irregularidades (dea, filia, domus, etc.)
3. Expande el vocabulario general
"""

from database.connection import get_session
from database import Word, Author
from sqlmodel import select
import sqlite3
import json

def add_column_if_not_exists():
    """Añade la columna irregular_forms si no existe"""
    print("1. Verificando esquema de base de datos...")
    conn = sqlite3.connect("lingua_latina.db")
    cursor = conn.cursor()
    
    # Verificar si existe la columna
    cursor.execute("PRAGMA table_info(word)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if "irregular_forms" not in columns:
        print("   -> Añadiendo columna 'irregular_forms'...")
        try:
            cursor.execute("ALTER TABLE word ADD COLUMN irregular_forms VARCHAR")
            conn.commit()
            print("   ✅ Columna añadida exitosamente.")
        except Exception as e:
            print(f"   ❌ Error añadiendo columna: {e}")
    else:
        print("   ✓ La columna 'irregular_forms' ya existe.")
    
    conn.close()

def migrate_phase2():
    """Ejecuta la migración de datos"""
    print("\n2. Insertando vocabulario con excepciones...")
    
    # Datos de palabras irregulares
    # dea, deae (f) - dat/abl pl: deabus
    # filia, filiae (f) - dat/abl pl: filiabus
    # domus, domus (f) - 4th/2nd mixed
    # locus, loci (m) - pl: loca (n)
    
    irregular_words = [
        {
            "latin": "dea",
            "translation": "diosa",
            "part_of_speech": "noun",
            "genitive": "deae",
            "gender": "f",
            "declension": "1",
            "level": 1,
            "irregular_forms": json.dumps({
                "dat_pl": "deābus",
                "abl_pl": "deābus"
            }),
            "category": "noun"
        },
        {
            "latin": "filia",
            "translation": "hija",
            "part_of_speech": "noun",
            "genitive": "filiae",
            "gender": "f",
            "declension": "1",
            "level": 1,
            "irregular_forms": json.dumps({
                "dat_pl": "filiābus",
                "abl_pl": "filiābus"
            }),
            "category": "noun"
        },
        {
            "latin": "domus",
            "translation": "casa, hogar",
            "part_of_speech": "noun",
            "genitive": "domūs",
            "gender": "f",
            "declension": "4", # Mixed 4th/2nd
            "level": 2,
            "irregular_forms": json.dumps({
                "abl_sg": "domō",       # 2nd decl ending
                "acc_pl": "domōs",      # or domūs
                "gen_pl": "domuum",     # or domōrum
                "loc_sg": "domī"        # Locative!
            }),
            "category": "noun"
        },
        {
            "latin": "locus",
            "translation": "lugar",
            "part_of_speech": "noun",
            "genitive": "locī",
            "gender": "m",
            "declension": "2",
            "level": 2,
            "irregular_forms": json.dumps({
                "nom_pl": "loca",       # Neuter plural
                "acc_pl": "loca"
            }),
            "category": "noun"
        },
        {
            "latin": "vis",
            "translation": "fuerza, violencia",
            "part_of_speech": "noun",
            "genitive": "—", # Defective in sg
            "gender": "f",
            "declension": "3", # Irregular
            "level": 3,
            "irregular_forms": json.dumps({
                "nom_sg": "vīs",
                "acc_sg": "vim",
                "abl_sg": "vī",
                "nom_pl": "vīrēs",
                "gen_pl": "vīrium",
                "dat_pl": "vīribus",
                "acc_pl": "vīrēs",
                "abl_pl": "vīribus"
            }),
            "category": "noun"
        }
    ]
    
    # Vocabulario general expandido (selección)
    new_vocab = [
        # 1st Declension
        {"latin": "aqua", "translation": "agua", "genitive": "aquae", "gender": "f", "declension": "1", "level": 1},
        {"latin": "via", "translation": "camino, calle", "genitive": "viae", "gender": "f", "declension": "1", "level": 1},
        {"latin": "fama", "translation": "fama, rumor", "genitive": "famae", "gender": "f", "declension": "1", "level": 1},
        {"latin": "fortuna", "translation": "fortuna, suerte", "genitive": "fortunae", "gender": "f", "declension": "1", "level": 1},
        {"latin": "nauta", "translation": "marinero", "genitive": "nautae", "gender": "m", "declension": "1", "level": 1}, # Masc 1st decl
        {"latin": "poeta", "translation": "poeta", "genitive": "poetae", "gender": "m", "declension": "1", "level": 1}, # Masc 1st decl
        
        # 2nd Declension
        {"latin": "amicus", "translation": "amigo", "genitive": "amici", "gender": "m", "declension": "2", "level": 1},
        {"latin": "equus", "translation": "caballo", "genitive": "equi", "gender": "m", "declension": "2", "level": 1},
        {"latin": "bellum", "translation": "guerra", "genitive": "belli", "gender": "n", "declension": "2", "level": 1},
        {"latin": "caelum", "translation": "cielo", "genitive": "caeli", "gender": "n", "declension": "2", "level": 1},
        {"latin": "vir", "translation": "hombre", "genitive": "viri", "gender": "m", "declension": "2", "level": 1},
        
        # 3rd Declension
        {"latin": "homo", "translation": "ser humano", "genitive": "hominis", "gender": "m", "declension": "3", "level": 2},
        {"latin": "corpus", "translation": "cuerpo", "genitive": "corporis", "gender": "n", "declension": "3", "level": 2},
        {"latin": "urbs", "translation": "ciudad", "genitive": "urbis", "gender": "f", "declension": "3", "level": 2},
        {"latin": "mare", "translation": "mar", "genitive": "maris", "gender": "n", "declension": "3", "level": 2}, # i-stem
        {"latin": "pater", "translation": "padre", "genitive": "patris", "gender": "m", "declension": "3", "level": 1},
        {"latin": "mater", "translation": "madre", "genitive": "matris", "gender": "f", "declension": "3", "level": 1},
        {"latin": "frater", "translation": "hermano", "genitive": "fratris", "gender": "m", "declension": "3", "level": 1},
        {"latin": "soror", "translation": "hermana", "genitive": "sororis", "gender": "f", "declension": "3", "level": 1},
        
        # 4th Declension
        {"latin": "exercitus", "translation": "ejército", "genitive": "exercitūs", "gender": "m", "declension": "4", "level": 3},
        {"latin": "cornu", "translation": "cuerno, ala (ejército)", "genitive": "cornūs", "gender": "n", "declension": "4", "level": 3},
        
        # 5th Declension
        {"latin": "res", "translation": "cosa, asunto", "genitive": "rei", "gender": "f", "declension": "5", "level": 3},
        {"latin": "spes", "translation": "esperanza", "genitive": "spei", "gender": "f", "declension": "5", "level": 3}
    ]

    with get_session() as session:
        # Insert irregular words
        count_irr = 0
        for data in irregular_words:
            # Check if exists
            existing = session.exec(select(Word).where(Word.latin == data["latin"])).first()
            if not existing:
                word = Word(**data)
                session.add(word)
                count_irr += 1
                print(f"   + Insertado irregular: {data['latin']}")
            else:
                # Update existing with irregular forms if needed
                if not existing.irregular_forms and "irregular_forms" in data:
                    existing.irregular_forms = data["irregular_forms"]
                    session.add(existing)
                    print(f"   ~ Actualizado irregular: {data['latin']}")

        # Insert new vocabulary
        count_new = 0
        for data in new_vocab:
            existing = session.exec(select(Word).where(Word.latin == data["latin"])).first()
            if not existing:
                word = Word(
                    latin=data["latin"],
                    translation=data["translation"],
                    part_of_speech="noun",
                    genitive=data["genitive"],
                    gender=data["gender"],
                    declension=data["declension"],
                    level=data["level"],
                    category="noun"
                )
                session.add(word)
                count_new += 1
        
        session.commit()
        print(f"\n✅ Migración completada.")
        print(f"   - Palabras irregulares nuevas: {count_irr}")
        print(f"   - Vocabulario general nuevo: {count_new}")

if __name__ == "__main__":
    add_column_if_not_exists()
    migrate_phase2()
