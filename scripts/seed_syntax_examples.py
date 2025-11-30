"""
Script para poblar la base de datos con ejemplos de análisis sintáctico pedagógico.
Inserta oraciones de 'Familia Romana' con anotaciones detalladas.
"""

import sys
import os
from pathlib import Path

# Añadir directorio raíz al path
sys.path.append(str(Path(__file__).parent.parent))

from sqlmodel import Session, select
from database.connection import engine
from database import Word
from database.syntax_models import SentenceAnalysis, TokenAnnotation, SentenceStructure

def seed_syntax_examples():
    print("🌱 Sembrando ejemplos de análisis sintáctico pedagógico...")
    
    with Session(engine) as session:
        # Limpiar ejemplos previos para evitar duplicados
        texts_to_remove = [
            "Puella rosam videt.",
            "Aemilia Iulium baculo pulsat."
        ]
        
        for text in texts_to_remove:
            statement = select(SentenceAnalysis).where(SentenceAnalysis.latin_text == text)
            results = session.exec(statement).all()
            for s in results:
                print(f"🗑️ Eliminando versión anterior de: {text}")
                # Manual cascade delete
                for ann in s.token_annotations:
                    session.delete(ann)
                for struct in s.structures:
                    session.delete(struct)
                session.delete(s)
        
        session.commit()
        
        # Ejemplo 1: Oración simple con caso especial
        # "Puella rosam videt."
        
        # 1. Crear SentenceAnalysis (base)
        sentence1 = SentenceAnalysis(
            latin_text="Puella rosam videt.",
            spanish_translation="La niña ve la rosa.",
            complexity_level=1,
            sentence_type="simple",
            source="familia_romana_cap1",
            syntax_roles='{"subject": [1], "direct_object": [2], "predicate": [3]}',
            dependency_json='[{"id": 1, "text": "Puella", "lemma": "puella", "pos": "NOUN", "dep": "nsubj", "head": 3, "morph": "Case=Nom|Gender=Fem|Number=Sing"}, {"id": 2, "text": "rosam", "lemma": "rosa", "pos": "NOUN", "dep": "obj", "head": 3, "morph": "Case=Acc|Gender=Fem|Number=Sing"}, {"id": 3, "text": "videt", "lemma": "video", "pos": "VERB", "dep": "ROOT", "head": 0, "morph": "Aspect=Imp|Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act"}, {"id": 4, "text": ".", "lemma": ".", "pos": "PUNCT", "dep": "punct", "head": 3, "morph": ""}]'
        )
        session.add(sentence1)
        session.commit()
        session.refresh(sentence1)
        
        # 2. Añadir TokenAnnotations (pedagógico) - 100% COBERTURA
        annotations1 = [
            TokenAnnotation(
                sentence_id=sentence1.id,
                token_index=0,
                token_text="Puella",
                pedagogical_role="Sujeto",
                case_function="Nominativo Sujeto",
                explanation="El sujeto realiza la acción del verbo. 'Puella' está en nominativo singular."
            ),
            TokenAnnotation(
                sentence_id=sentence1.id,
                token_index=1,
                token_text="rosam",
                pedagogical_role="Objeto Directo",
                case_function="Acusativo de Objeto Directo",
                explanation="El objeto directo recibe la acción. 'Rosam' está en acusativo singular (terminación -am)."
            ),
            TokenAnnotation(
                sentence_id=sentence1.id,
                token_index=2,
                token_text="videt",
                pedagogical_role="Núcleo del Predicado",
                case_function="Verbo Transitivo",
                explanation="Verbo en 3ª persona singular del presente indicativo. Requiere un objeto directo."
            ),
            TokenAnnotation(
                sentence_id=sentence1.id,
                token_index=3,
                token_text=".",
                pedagogical_role="Puntuación",
                case_function="Signo de Puntuación",
                explanation="Marca el final de la oración declarativa."
            )
        ]
        
        for ann in annotations1:
            session.add(ann)
            
        # 3. Añadir SentenceStructure
        struct1 = SentenceStructure(
            sentence_id=sentence1.id,
            clause_type="Principal",
            notes="Oración simple transitiva con orden SOV (Sujeto-Objeto-Verbo)."
        )
        session.add(struct1)
        
        # Ejemplo 2: Ablativo de Instrumento
        # "Aemilia Iulium baculo pulsat."
        
        sentence2 = SentenceAnalysis(
            latin_text="Aemilia Iulium baculo pulsat.",
            spanish_translation="Aemilia golpea a Julio con un bastón.",
            complexity_level=2,
            sentence_type="simple",
            source="familia_romana_cap3",
            syntax_roles='{"subject": [1], "direct_object": [2], "complement": [3], "predicate": [4]}',
            dependency_json='[{"id": 1, "text": "Aemilia", "lemma": "Aemilia", "pos": "PROPN", "dep": "nsubj", "head": 4, "morph": "Case=Nom|Gender=Fem|Number=Sing"}, {"id": 2, "text": "Iulium", "lemma": "Iulius", "pos": "PROPN", "dep": "obj", "head": 4, "morph": "Case=Acc|Gender=Masc|Number=Sing"}, {"id": 3, "text": "baculo", "lemma": "baculum", "pos": "NOUN", "dep": "obl", "head": 4, "morph": "Case=Abl|Gender=Neut|Number=Sing"}, {"id": 4, "text": "pulsat", "lemma": "pulso", "pos": "VERB", "dep": "ROOT", "head": 0, "morph": "Aspect=Imp|Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act"}, {"id": 5, "text": ".", "lemma": ".", "pos": "PUNCT", "dep": "punct", "head": 4, "morph": ""}]'
        )
        session.add(sentence2)
        session.commit()
        session.refresh(sentence2)
        
        annotations2 = [
            TokenAnnotation(
                sentence_id=sentence2.id,
                token_index=0,
                token_text="Aemilia",
                pedagogical_role="Sujeto",
                case_function="Nominativo Sujeto"
            ),
            TokenAnnotation(
                sentence_id=sentence2.id,
                token_index=1,
                token_text="Iulium",
                pedagogical_role="Objeto Directo",
                case_function="Acusativo"
            ),
            TokenAnnotation(
                sentence_id=sentence2.id,
                token_index=2,
                token_text="baculo",
                pedagogical_role="Complemento Circunstancial",
                case_function="Ablativo de Instrumento",
                explanation="Indica el medio o instrumento con el que se realiza la acción. Se traduce 'con...' o 'por medio de...'."
            ),
            TokenAnnotation(
                sentence_id=sentence2.id,
                token_index=3,
                token_text="pulsat",
                pedagogical_role="Núcleo del Predicado",
                case_function="Verbo Transitivo"
            ),
            TokenAnnotation(
                sentence_id=sentence2.id,
                token_index=4,
                token_text=".",
                pedagogical_role="Puntuación",
                case_function="Signo de Puntuación"
            )
        ]
        
        for ann in annotations2:
            session.add(ann)
            
        struct2 = SentenceStructure(
            sentence_id=sentence2.id,
            clause_type="Principal",
            notes="Uso clásico del ablativo instrumental sin preposición."
        )
        session.add(struct2)
        
        session.commit()
        print("✅ Ejemplos insertados correctamente (100% cobertura).")

if __name__ == "__main__":
    # Crear tablas si no existen (esto actualizará el esquema)
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)
    
    seed_syntax_examples()
