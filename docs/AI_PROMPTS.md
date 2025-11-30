# AI Prompts - Guía para Asistentes de IA

Este documento contiene prompts y directrices específicas para asistentes de IA que trabajen en el desarrollo de Lingua Latina Viva.

## Prompt de Contexto Inicial

Cuando comiences a trabajar en este proyecto, usa este prompt:

```
Soy un asistente de IA trabajando en Lingua Latina Viva, una aplicación de aprendizaje de latín clásico basada en Python/Streamlit.

INFORMACIÓN DEL PROYECTO:
- Ubicación: /home/diego/Projects/latin-python
- Stack: Python 3.11+, Streamlit, SQLite, SQLModel
- Objetivo: Enseñar latín clásico mediante enfoque basado en corpus
- Metodología: Progresión por niveles + SRS + gamificación

DOCUMENTACIÓN CLAVE:
1. docs/ARCHITECTURE.md - Arquitectura del sistema
2. docs/CONTRIBUTING.md - Guía de contribución
3. docs/enhancement_plan.md - Plan de mejoras futuras

REGLAS FUNDAMENTALES:
1. TODO el vocabulario debe provenir de textos clásicos reales
2. Imports SIEMPRE desde `database.models` (nunca `models` solo)
3. UI en español, con estética romana clásica
4. Código limpio, comentado, siguiendo PEP 8

ANTES DE CUALQUIER CAMBIO:
- Leer ARCHITECTURE.md completo
- Revisar código existente relacionado
- Verificar que el enfoque es coherente con la metodología

¿Entiendes el contexto y estás listo para trabajar?
```

## 🚨 ERRORES CRÍTICOS - RESOLVER PRIMERO (26 NOV 2025 - 00:01h)

**APLICACIÓN COMPLETAMENTE ROTA - PRIORIDAD MÁXIMA**

```
ERROR PRINCIPAL: SQLAlchemy InvalidRequestError
Multiple classes found for path "database.models.Word" in the registry

SÍNTOMAS:
- Todas las páginas fallan al cargar (09_Analizador, 10_Sintaxis, 11_Diccionario, 13_Scriptorium, 99_Admin)
- Dashboard (01_Inicio.py) también afectado
- Error en TODAS las queries: session.exec(select(Word))

CAUSA PROBABLE:
- Modelos SQLModel siendo registrados múltiples veces
- Posible importación circular
- Conflicto entre database.models y database.integration_models

SOLUCIÓN URGENTE:
1. Verificar imports en database/connection.py
2. Buscar imports duplicados de Word en toda la app:
   grep -r "from database.models import Word" pages/
3. Verificar que integration_models.py NO redefine Word
4. Asegurar que solo hay UNA definición de Word en database/models.py
5. Limpiar cache de Python: find . -type d -name __pycache__ -exec rm -rf {} +
6. Reiniciar servidor Streamlit

COMANDO DIAGNÓSTICO:
cd /home/diego/Projects/latin-python
grep -rn "class Word" database/
grep -rn "from.*models import.*Word" .

NOTA: Este error apareció DESPUÉS de modificar Vocabulario con integration_models.
```

## 🐛 OTROS ERRORES DETECTADOS (Resolver después del crítico)

### 1. Error en generate_recommendations()
```
TypeError: generate_recommendations() got an unexpected keyword argument 'limit'
File: pages/01_🏠_Inicio.py, line 125
```
**STATUS:** ✅ CORREGIDO (removido parámetro limit)

### 2. Error en decline_noun() - Homónimos con números
```
Error: "No se pudo generar la declinación para Balbus2"
Palabra: Balbus2 (genitivo: Balbus2i)
Declensión: 2ª, Género: m
```
**CAUSA:** La función decline_noun() no maneja palabras con dígitos (homónimos marcados como word2, word3, etc.)

**SOLUCIÓN REQUERIDA:**
```python
def decline_noun(word: str, declension: str, gender: str, genitive: str, ...):
    # Limpiar dígitos del final ANTES de procesar
    clean_word = ''.join([c for c in word if not c.isdigit()])
    clean_genitive = ''.join([c for c in genitive if not c.isdigit()])
    
    # Ahora usar clean_word para extraer stem
    if declension == "2":
        if clean_word.endswith("us"):
            stem = clean_word[:-2]
            # ...resto de lógica
```

### 3. Minor: Typo en banner de Vocabulario
```
File: pages/03_🎴_Vocabulario.py
"filtrará automáticamente" tiene error de espacio
```

## Prompt de Continuación - Integración Orgánica (DESPUÉS DE RESOLVER ERRORES)

**📌 TAREA PAUSADA - 26 de Noviembre 2025**

```
⚠️ ATENCIÓN: NO continuar con integración hasta resolver errores críticos arriba.

CONTEXTO:
Estoy trabajando en la Fase 3 del Plan de Integración Orgánica de Módulos para Lingua Latina Viva.
El objetivo es transformar los módulos independientes en un ecosistema cohesivo de aprendizaje.

DOCUMENTOS CLAVE:
1. /home/diego/.gemini/antigravity/brain/4a92856b-82e8-4138-8e90-147be201f198/implementation_plan.md
   → Plan completo de integración (leer primero)
   
2. /home/diego/.gemini/antigravity/brain/c40756f3-f424-4143-b796-727250e87b74/task.md
   → Estado actual y checklist de tareas
   
3. /home/diego/.gemini/antigravity/brain/c40756f3-f424-4143-b796-727250e87b74/vocabulario_integration.md
   → Documentación de último cambio completado

ESTADO ACTUAL:
✅ Fase 1: Fundamentos - COMPLETADO
   - Tablas de integración creadas (LessonVocabulary, UserProgressSummary, etc.)
   - Servicios de integración implementados
   - Datos iniciales poblados

✅ Fase 2: Dashboard Unificado - COMPLETADO
   - Dashboard con recomendaciones personalizadas
   - Mapa visual de 40 lecciones
   - Progreso por módulo

✅ Fase 3: Módulos Individuales - PARCIAL
   - ✅ 02_📘_Curso.py - Sección "Practica esta Lección"
   - ✅ 03_🎴_Vocabulario.py - Filtros por lección + banner + navegación contextual
   - ⏸️ 04_📜_Declinaciones.py - PENDIENTE
   - ⏸️ 05_⚔️_Conjugaciones.py - PENDIENTE
   - ⏸️ 06_📖_Lecturas.py - PENDIENTE
   - ⏸️ 08_🎯_Desafios.py - PENDIENTE
   - ⏸️ 10_📐_Sintaxis.py - PENDIENTE

PRÓXIMA TAREA (cuando errores estén resueltos):
Modificar pages/04_📜_Declinaciones.py para agregar:
1. Banner contextual mostrando lección actual
2. Selector de lección (1-40) con filtro de vocabulario
3. Tracking de ejercicios completados
4. Feedback de progreso
5. Enlaces contextuales a otros módulos

PASOS A SEGUIR:
1. ✅ PRIMERO: Resolver error crítico SQLAlchemy (ver arriba)
2. ✅ SEGUNDO: Corregir decline_noun() para homónimos
3. Leer el implementation_plan.md sección "Fase 3: Declinaciones"
4. Revisar archivo actual pages/04_📜_Declinaciones.py
5. Importar modelos necesarios (LessonVocabulary, UserProgressSummary, ExerciseAttempt)
6. Implementar cambios siguiendo mismo patrón que Vocabulario
7. Actualizar task.md marcando tarea como completada
8. Documentar cambios en nuevo archivo walkthrough

MODELO A SEGUIR:
Ver vocabulario_integration.md para referencia del patrón de integración aplicado.

RESTRICCIONES:
- Mantener funcionalidad SRS existente
- No romper ejercicios actuales
- UI debe seguir estética romana
- Todos los términos en español

¿Listo para resolver errores críticos primero?
```

## Prompts por Tipo de Tarea

### 1. Añadir Nueva Funcionalidad

```
TAREA: Implementar [nombre de funcionalidad]

PASOS A SEGUIR:
1. Leer docs/ARCHITECTURE.md y docs/enhancement_plan.md
2. Crear plan de implementación en docs/implementation_plan.md
3. Identificar archivos a modificar
4. Implementar cambios de forma atómica (un archivo a la vez)
5. Verificar con pruebas manuales
6. Documentar en docs/walkthrough.md
7. Hacer commit a Git

RESTRICCIONES:
- No modificar estructura base de la aplicación
- Mantener compatibilidad con base de datos existente
- Asegurar que UI mantiene estética romana
- Todos los términos gramaticales en español

VERIFICACIÓN:
- Ejecutar `streamlit run app.py` y verificar que no hay errores
- Navegar a páginas afectadas y probar funcionalidad
- Confirmar que no hay warnings en consola
```

### 2. Corregir Error

```
TAREA: Corregir error [descripción del error]

DIAGNÓSTICO:
1. Leer el stacktrace completo
2. Identificar archivo y línea del error
3. Buscar errores comunes en docs/CONTRIBUTING.md sección "Troubleshooting"

ERRORES COMUNES:
- SQLAlchemyError: Revisar imports (debe ser `from database.models import ...`)
- Streamlit page error: Verificar nombre de archivo en `pages/`
- Database locked: Matar procesos con `pkill -f streamlit`

PROCESO:
1. Diagnosticar causa raíz
2. Revisar código relacionado
3. Aplicar fix mínimo necesario
4. Verificar que fix no rompe otras partes
5. Documentar el fix

VERIFICACIÓN:
- Reiniciar Streamlit
- Reproducir escenario que causaba error
- Confirmar que error está resuelto
```

### 3. Añadir Vocabulario/Contenido

```
TAREA: Importar vocabulario de [fuente]

VALIDACIÓN DE FUENTE:
¿La fuente es un autor clásico reconocido? (Caesar, Cicero, Virgilio, Ovidio, etc.)
- Sí: Continuar
- No: DETENER y consultar con usuario

FORMATO DE DATOS:
- CSV con columnas: latin, translation, part_of_speech, declension/conjugation, etc.
- Validar que todas las palabras tienen traducción
- Verificar formas canónicas (Nominativo para sustantivos, 1ª persona presente para verbos)

PROCESO:
1. Preparar CSV con datos validados
2. Colocar en `data/vocabulary/[autor]_[nivel].csv`
3. Crear script de importación `import_[autor].py`
4. Ejecutar importación
5. Verificar con query SQL
6. Probar en UI (Vocabularium)

SCRIPT TEMPLATE:
```python
import csv
from database.connection import get_session
from database.models import Word

with get_session() as session:
    with open('data/vocabulary/caesar_level1.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            word = Word(
                latin=row['latin'],
                translation=row['translation'],
                part_of_speech=row['part_of_speech'],
                # ... otros campos
                level=1
            )
            session.add(word)
    session.commit()
```
```

### 4. Modificar Base de Datos

```
TAREA: [Añadir tabla/campo/relación]

PLANIFICACIÓN:
1. Dibujar diagrama ER de cambio propuesto
2. Identificar impacto en código existente
3. Planificar migración de datos si es necesario

PROCESO:
1. Añadir/modificar modelo en `database/models.py`
2. Siempre usar `Optional[]` para campos nuevos (compatibilidad)
3. Añadir relaciones con `Relationship(back_populates=...)`
4. Actualizar imports en `database/connection.py`

EJEMPLO - AÑADIR TABLA:
```python
# En database/models.py
class Author(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    difficulty_level: int
    description: Optional[str] = None
    
    # Relaciones
    words: List["Word"] = Relationship(back_populates="author")
    texts: List["Text"] = Relationship(back_populates="author")

# En Word, añadir:
author_id: Optional[int] = Field(default=None, foreign_key="author.id")
author: Optional["Author"] = Relationship(back_populates="words")
```

VERIFICACIÓN:
- Reiniciar app (SQLModel crea tablas automáticamente)
- Verificar esquema: `sqlite3 lingua_latina.db ".schema"`
- Probar creación de registros
```

### 5. Mejorar UI/UX

```
TAREA: Mejorar [aspecto de UI]

PRINCIPIOS DE DISEÑO:
- Estética romana clásica (fuentes Cinzel, Trajan)
- Paleta de colores tierra (#8b4513 marrón, #d2b48c beige, #f5f5dc crema)
- Contraste adecuado para legibilidad
- Emojis consistentes por módulo

COMPONENTES HTML/CSS:
- Usar clases CSS existentes en `assets/style.css`
- Si añades nuevas clases, documentarlas
- Mantener responsive design

EJEMPLO - TARJETA DE VOCABULARIO:
```python
st.markdown(
    f'''
    <div class="vocab-card">
        <div class="vocab-latin">{word.latin}</div>
        <div class="vocab-translation">{word.translation}</div>
        <div class="vocab-pos">{translate_pos(word.part_of_speech)}</div>
    </div>
    ''',
    unsafe_allow_html=True
)
```

VERIFICACIÓN:
- Probar en diferentes tamaños de pantalla
- Verificar contraste con herramienta online
- Confirmar que términos están en español
```

### 6. Refactorizar Código

```
TAREA: Refactorizar [componente/módulo]

OBJETIVOS:
- Mejorar legibilidad
- Eliminar duplicación
- Optimizar rendimiento
- Mantener funcionalidad existente

PROCESO:
1. Entender código actual completamente
2. Identificar patrones duplicados
3. Extraer funciones/clases reutilizables
4. Mover a `utils/` si es genérico
5. Actualizar imports en archivos afectados

REGLAS:
- NO cambiar funcionalidad visible al usuario
- Mantener nombres de función públicas (breaking changes)
- Añadir docstrings si no existen
- Mantener tests pasando (cuando existan)

VERIFICACIÓN:
- Ejecutar app completa
- Probar todas las funcionalidades afectadas
- Confirmar que no hay regresiones
```

## Prompts de Verificación

### Checklist Pre-Commit

```
Antes de hacer commit, verifica:

CÓDIGO:
- [ ] Imports correctos (`from database.models import ...`)
- [ ] Nombres de variables descriptivos
- [ ] Código sigue PEP 8
- [ ] Funciones tienen docstrings
- [ ] No hay código comentado sin necesidad

UI/UX:
- [ ] Términos en español
- [ ] Estética romana mantenida
- [ ] Emojis consistentes
- [ ] Contraste adecuado

FUNCIONALIDAD:
- [ ] App corre sin errores (`streamlit run app.py`)
- [ ] Funcionalidad probada manualmente
- [ ] No hay warnings en consola
- [ ] Session state manejado correctamente

DOCUMENTACIÓN:
- [ ] ARCHITECTURE.md actualizado (si aplica)
- [ ] CONTRIBUTING.md actualizado (si aplica)
- [ ] walkthrough.md creado/actualizado
- [ ] Comentarios en código complejo

GIT:
- [ ] .gitignore excluye archivos temporales
- [ ] Commit message descriptivo
- [ ] Solo archivos relevantes en commit
```

### Prompt de Debug

```
PROBLEMA: [Descripción del error]
ERROR: [Mensaje de error completo]

PASOS DE DEBUG:
1. ¿Es un error conocido? Revisar docs/CONTRIBUTING.md "Troubleshooting"
2. ¿Stacktrace apunta a código nuestro o librería externa?
   - Nuestro: Revisar lógica
   - Externo: Revisar uso de API

3. ERRORES COMUNES:
   - InvalidRequestError → Revisar imports de modelos
   - Streamlit rerun loop → Revisar session_state
   - Database locked → Matar procesos duplicados
   - Import error → Verificar sys.path y estructura

4. TÉCNICAS:
   - Añadir print() temporales
   - Ejecutar en REPL interactivo
   - Revisar logs de Streamlit
   - Verificar versiones de dependencias

5. SOLUCIÓN:
   - Aplicar fix mínimo
   - Verificar que no rompe otras cosas
   - Documentar causa y solución
```

## Prompts de Comunicación con Usuario

### Solicitar Clarificación

```
Necesito clarificación sobre [aspecto]:

CONTEXTO:
- [Explicar situación actual]
- [Explicar ambigüedad o duda]

OPCIONES:
A) [Opción 1 con pros/contras]
B) [Opción 2 con pros/contras]

RECOMENDACIÓN:
[Tu recomendación basada en principios del proyecto]

¿Qué prefieres?
```

### Reportar Progreso

```
PROGRESO: [Tarea]

COMPLETADO:
✅ [Ítem 1]
✅ [Ítem 2]

EN PROGRESO:
🔄 [Ítem actual]

PENDIENTE:
⏸️ [Ítem futuro]

BLOQUEADORES:
❌ [Si aplica]

Siguiente paso: [Describir]
```

### Solicitar Revisión

```
He completado [funcionalidad]. Por favor revisa:

ARCHIVOS MODIFICADOS:
- [Archivo 1]: [Cambios]
- [Archivo 2]: [Cambios]

VERIFICACIÓN:
✅ [Test manual 1]
✅ [Test manual 2]

DOCUMENTACIÓN:
- docs/walkthrough.md actualizado
- Código comentado donde necesario

¿Apruebas para hacer commit?
```

## Plantillas de Código

### Nueva Página de Streamlit

```python
import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.connection import get_session
from database.models import Word, ReviewLog

st.set_page_config(page_title="[Nombre]", page_icon="[emoji]", layout="wide")

def load_css():
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.markdown(
    """
    <h1 style='text-align: center; font-family: "Cinzel", serif; color: #8b4513;'>
        [emoji] [Título] - [Subtítulo en Español]
    </h1>
    """,
    unsafe_allow_html=True
)

# --- LÓGICA PRINCIPAL ---

with get_session() as session:
    # Tu código aquí
    pass
```

### Nuevo Modelo SQLModel

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class [NombreModelo](SQLModel, table=True):
    """[Descripción del modelo]"""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Campos básicos
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    
    # Relaciones
    related_items: List["[OtroModelo]"] = Relationship(back_populates="[este_modelo]")
```

### Función de Utilidad

```python
def [nombre_funcion]([parametros]) -> [tipo_retorno]:
    """
    [Descripción breve de qué hace la función]
    
    Args:
        [param1]: [Descripción]
        [param2]: [Descripción]
        
    Returns:
        [Descripción del valor de retorno]
        
    Example:
        >>> [ejemplo de uso]
        [resultado esperado]
    """
    # Implementación
    pass
```

## Recordatorios Finales

### SIEMPRE:
- ✅ Leer documentación antes de cambios mayores
- ✅ Verificar imports desde `database.models`
- ✅ Probar manualmente antes de commit
- ✅ Mantener UI en español con estética romana
- ✅ Documentar cambios significativos

### NUNCA:
- ❌ Inventar vocabulario (debe ser de corpus real)
- ❌ Usar imports relativos para modelos
- ❌ Hacer múltiples edits en paralelo al mismo archivo
- ❌ Commitear sin probar
- ❌ Cambiar estructura base sin documentar

### EN CASO DE DUDA:
1. Consultar docs/ARCHITECTURE.md
2. Revisar código existente similar
3. Buscar en docs/CONTRIBUTING.md
4. Preguntar al usuario

---

**Objetivo Final**: Facilitar que usuarios desarrollen habilidades para traducir latín clásico y disfruten de los autores originales.
