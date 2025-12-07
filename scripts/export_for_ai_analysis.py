#!/usr/bin/env python3
"""
Exportador de oraciones para análisis por IA.
Genera un archivo JSON con todas las oraciones y un prompt para comparar análisis.
"""
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import get_session
from database import SentenceAnalysis
from sqlmodel import select

def export_sentences_for_ai(output_path: str = "data/sentences_for_ai_analysis.json", limit: int = None, offset: int = 0):
    """Exporta oraciones en formato optimizado para análisis por IA."""
    
    with get_session() as session:
        query = select(SentenceAnalysis).where(SentenceAnalysis.dependency_json != "[]")
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        sentences = session.exec(query).all()
        
        # Filtros de fuente
        filtered_sentences = []
        for sent in sentences:
            # Si queremos solo lecturas, excluimos lo que parezca ejercicio
            # Criterio actual: si source empieza por 'lesson_', es ejercicio
            is_exercise = sent.source and sent.source.startswith("lesson_")
            
            # TODO: Hacer esto configurable por argumento
            # Por ahora, si el script se llama globalmente, exportamos TODO o diferenciamos
            # Para este caso de uso (AI analysis de lecturas), queremos NO ejercicios
            if is_exercise:
                continue
                
            filtered_sentences.append(sent)

        print(f"ℹ️ Filtrado: {len(sentences)} total -> {len(filtered_sentences)} seleccionadas (excluyendo ejercicios)")

        export_data = {
            "metadata": {
                "total_sentences": len(filtered_sentences),
                "format_version": "1.0",
                "description": "Oraciones latinas con análisis sintáctico actual de LatinCy/spaCy"
            },
            "sentences": []
        }
        
        for sent in filtered_sentences:
            deps = json.loads(sent.dependency_json or "[]")
            roles = json.loads(sent.syntax_roles or "{}")
            
            # Crear mapa inverso: token_id -> rol
            token_roles = {}
            for role, ids in roles.items():
                for tid in ids:
                    token_roles[tid] = role
            
            # Formato simplificado para la IA
            tokens = []
            for token in deps:
                tokens.append({
                    "idx": token["id"],
                    "word": token["text"],
                    "lemma": token["lemma"],
                    "pos": token["pos"],
                    "morph": token.get("morph", ""),
                    "dep": token["dep"],
                    "head": token["head"],
                    "current_role": token_roles.get(token["id"], "sin_rol")
                })
            
            export_data["sentences"].append({
                "id": sent.id,
                "latin": sent.latin_text,
                "spanish": sent.spanish_translation,
                "tokens": tokens
            })
        
        # Guardar archivo
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Exportadas {len(sentences)} oraciones a: {output_path}")
        return output_path


def generate_ai_prompt():
    """Genera el prompt para que una IA analice las oraciones."""
    
    prompt = '''# TAREA: Análisis Sintáctico de Oraciones Latinas

Eres un experto en gramática latina clásica. Tu tarea es analizar las siguientes oraciones latinas y asignar funciones sintácticas a cada palabra.

## FORMATO DE ENTRADA
Recibirás oraciones en este formato JSON:
```json
{
  "id": 1,
  "latin": "Puella rosam videt.",
  "spanish": "La niña ve la rosa.",
  "tokens": [
    {"idx": 0, "word": "Puella", "lemma": "puella", "pos": "NOUN", "morph": "Case=Nom|Gender=Fem|Number=Sing", "dep": "nsubj", "head": 2, "current_role": "sujeto"},
    ...
  ]
}
```

## ROLES SINTÁCTICOS DISPONIBLES
Usa EXACTAMENTE estas etiquetas (en español, con guiones bajos):

### Sujeto y Predicado
- `sujeto` - Nominativo que realiza la acción
- `sujeto_paciente` - Sujeto de voz pasiva
- `predicado` - Verbo principal (ROOT)
- `cópula` - Verbo copulativo (sum, esse)
- `auxiliar` - Verbo auxiliar

### Objetos
- `objeto_directo` - Acusativo, ¿qué?
- `objeto_indirecto` - Dativo, ¿a quién?
- `complemento_predicativo` - Predicativo del sujeto u objeto

### Complementos
- `complemento_circunstancial` - Ablativo/oblicuo: cómo, cuándo, dónde, con qué
- `complemento_del_nombre` - Genitivo que modifica sustantivo

### Modificadores
- `modificador_adjetival` - Adjetivo que modifica sustantivo
- `modificador_adverbial` - Adverbio que modifica verbo

### Oraciones Subordinadas
- `oración_completiva` - Subordinada sustantiva
- `oración_de_relativo` - Con pronombre relativo
- `oración_adverbial` - Subordinada circunstancial

### Conjunciones y Conectores
- `conjunción_coordinante` - et, aut, sed
- `conjunción_subordinante` - ut, cum, si
- `elemento_coordinado` - Elemento unido por conjunción

### Otros
- `preposición` - Introduce complementos
- `determinante` - Determina al sustantivo
- `aposición` - Explicación de otro sustantivo
- `vocativo` - Llamada o invocación
- `puntuación` - Signos de puntuación

## FORMATO DE RESPUESTA
Para CADA oración, devuelve un JSON con tu análisis corregido:

```json
{
  "id": 1,
  "corrections": [
    {"idx": 0, "current_role": "sujeto", "correct_role": "sujeto", "is_correct": true},
    {"idx": 1, "current_role": "objeto_directo", "correct_role": "objeto_directo", "is_correct": true},
    {"idx": 2, "current_role": "predicado", "correct_role": "predicado", "is_correct": true},
    {"idx": 3, "current_role": "puntuación", "correct_role": "puntuación", "is_correct": true}
  ],
  "notes": "Análisis correcto. Oración simple SVO."
}
```

## CRITERIOS DE EVALUACIÓN
1. **Sujeto**: Nominativo que concuerda con el verbo en persona y número
2. **Objeto Directo**: Acusativo que recibe la acción directa
3. **Objeto Indirecto**: Dativo, beneficiario de la acción
4. **Complemento Circunstancial**: Ablativos y sintagmas preposicionales
5. **Predicado**: El verbo principal en forma finita (ROOT)
6. **Cópula**: Específicamente formas de "sum, esse"

## INSTRUCCIONES ADICIONALES
- Si el análisis actual es correcto, marca `is_correct: true`
- Si hay error, indica el rol correcto en `correct_role`
- Presta especial atención a:
  - Distinción entre sujeto activo y pasivo
  - Diferencia entre cópula (sum) y auxiliar
  - Identificación de subordinadas (completivas, relativas, adverbiales)
  - Ablativos absolutos
  - Acusativo + Infinitivo

---

# ORACIONES A ANALIZAR

'''
    return prompt


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Exportar oraciones para análisis por IA")
    parser.add_argument("--limit", type=int, default=None, help="Número máximo de oraciones a exportar")
    parser.add_argument("--offset", type=int, default=0, help="Offset para paginación")
    parser.add_argument("--output", type=str, default="data/sentences_for_ai_analysis.json", help="Archivo de salida")
    
    args = parser.parse_args()
    
    # Exportar oraciones
    output_file = export_sentences_for_ai(output_path=args.output, limit=args.limit, offset=args.offset)
    
    # Generar prompt
    prompt = generate_ai_prompt()
    prompt_file = "data/ai_analysis_prompt.md"
    os.makedirs("data", exist_ok=True)
    with open(prompt_file, "w", encoding="utf-8") as f:
        f.write(prompt)
    
    print(f"✅ Prompt guardado en: {prompt_file}")
    print(f"\n📋 INSTRUCCIONES:")
    print(f"1. Abre {prompt_file} y copia el prompt")
    print(f"2. Adjunta el contenido de {output_file} al final del prompt")
    print(f"3. Envía a Claude/GPT-4 para obtener el análisis comparativo")
