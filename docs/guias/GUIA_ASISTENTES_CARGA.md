# 🧙 Asistentes Guiados para Carga de Datos

## Visión General

Se han creado **asistentes interactivos paso a paso** para guiar a los usuarios en la carga de datos de Vocabulario, Oraciones y Textos. Los asistentes validan en cada etapa y ofrecen tres modos de operación.

---

## 📚 Asistente de Vocabulario

### 4 Pasos

```
Paso 1: Información Básica
├─ Palabra en latín *
├─ Traducción *
├─ Categoría gramatical (noun, verb, adj, etc.) *
└─ Nivel de dificultad (1-10) *

Paso 2: Información Morfológica
├─ Genitivo (sustantivos)
├─ Género (m, f, n) - sustantivos
├─ Declinación (1-5) - sustantivos
├─ Partes principales - verbos
└─ Conjugación (1-4, irregular) - verbos

Paso 3: Formas Irregulares (Optional)
└─ JSON con formas especiales

Paso 4: Contexto y Fuente
├─ Fuente (manual, collatinus, dictionary)
└─ Notas adicionales
```

### Características
- ✅ Campos dinámicos según POS (Part of Speech)
- ✅ Solo muestra campos relevantes
- ✅ Validación de datos requeridos
- ✅ Ejemplos en cada paso
- ✅ Ayuda contextual

---

## 📝 Asistente de Oraciones

### 3 Pasos

```
Paso 1: Oración en Latín
├─ Texto latino *
├─ Traducción *
└─ Nivel de dificultad *

Paso 2: Análisis Sintáctico
├─ Tipo de cláusula principal
└─ Construcciones especiales (accusative infinitive, ablative absolute, etc.)

Paso 3: Anotaciones Gramaticales
└─ Temas gramaticales principales (casos, tiempos, modos, etc.)
```

### Características
- ✅ Soporta modo automático con NLP (Future)
- ✅ Multiselect para marcar múltiples temas
- ✅ Análisis sintáctico opcional
- ✅ Integración con motor NLP del sistema

---

## 📖 Asistente de Textos

### 4 Pasos

```
Paso 1: Información del Texto
├─ Título *
├─ Autor *
└─ Nivel de dificultad (1-10) *

Paso 2: Contenido del Texto
└─ Texto latino completo *

Paso 3: Análisis de Contenido
├─ Tipo (original, adapted, simplified, excerpt)
├─ Número de libro
└─ Número de capítulo

Paso 4: Revisión Final
└─ Confirmación de datos
```

### Características
- ✅ Validación de macrones en latín (Future)
- ✅ Análisis de cobertura de vocabulario (Future)
- ✅ Estimación de tiempo de lectura (Future)
- ✅ Revisión final antes de guardar

---

## 🤖 Modos de Operación

### 1. MANUAL (✍️ Manual completo)
- **Descripción:** El usuario ingresa TODOS los datos manualmente
- **Uso:** Cuando el usuario conoce los detalles gramaticales
- **Validación:** Estricta en todos los campos requeridos
- **Ejemplo:** Profesor cargando vocabulario que prepara

### 2. SEMI_AUTO (🤝 Semi-automático)
- **Descripción:** Usuario ingresa datos + Motor NLP sugiere análisis
- **Uso:** Balance entre velocidad y control
- **Validación:** Datos base requeridos + opciones sugeridas
- **Ejemplo:** Cargar oración y dejar que NLP sugiera análisis sintáctico

### 3. FULL_AUTO (🤖 Automático completo)
- **Descripción:** Motor NLP analiza y carga automáticamente
- **Uso:** Procesamiento rápido de lotes (batch)
- **Validación:** Solo verificación final
- **Ejemplo:** Importar 100 palabras de un texto ya analizado

---

## 🔧 Integración en Admin Panel

### Ubicación propuesta

```
pages/99_⚙️_Administracion.py
└─ Nueva sección: "🧙 Asistentes de Carga"
   ├─ Selector de modo y tipo de datos
   ├─ Vocabulario → render_vocabulary_assistant()
   ├─ Oraciones → render_sentence_assistant()
   └─ Textos → render_text_assistant()
```

### Ejemplo de uso

```python
from utils.admin_data_assistants_ui import (
    render_assistant_mode_selector,
    render_vocabulary_assistant,
    render_sentence_assistant,
    render_text_assistant
)

if section == "🧙 Asistentes de Carga":
    st.markdown("## 🧙 Asistentes Guiados de Carga")
    
    data_type, mode = render_assistant_mode_selector()
    
    if data_type == DataType.VOCABULARY:
        result = render_vocabulary_assistant(mode)
        if result:
            # Guardar en BD
            save_to_database(result)
    
    elif data_type == DataType.SENTENCES:
        result = render_sentence_assistant(mode)
        if result:
            save_to_database(result)
    
    elif data_type == DataType.TEXTS:
        result = render_text_assistant(mode)
        if result:
            save_to_database(result)
```

---

## 📊 Validación Step-by-Step

Cada paso valida:

1. **Campos requeridos** - No puede avanzar sin completarlos
2. **Tipos de datos** - Valida formato (número, email, etc.)
3. **Reglas personalizadas** - Validadores específicos por campo
4. **Consistencia** - Valida que los datos sean coherentes

Ejemplo de validación para Vocabulario Paso 1:
```
❌ latin_word vacío → "Campo requerido: latin_word"
❌ translation vacío → "Campo requerido: translation"
❌ part_of_speech vacío → "Campo requerido: part_of_speech"
✅ Todos completos → Puede avanzar
```

---

## 🔌 Integración con Motores NLP (Future)

### Para Semi-Auto y Full-Auto

```python
# Uso futuro del motor NLP
from utils.nlp_engine import nlp_engine

# Análisis automático de oración
syntax = nlp_engine.analyze_syntax("Magister discipulos docet.")
# → {"main_verb": "docet", "direct_object": "discipulos", ...}

# Análisis de palabra
morphology = nlp_engine.analyze_word("discipulos")
# → {"root": "discipulus", "case": "accusative", "number": "plural", ...}

# Extracción de vocabulario desde texto
words = nlp_engine.extract_vocabulary("Lorem ipsum dolor sit amet...")
# → [{"word": "Lorem", "lemma": "Lorum", "pos": "noun", ...}, ...]
```

---

## 💾 Flujo de Datos

```
Usuario selecciona modo
    ↓
Asistente inicializa (session_state)
    ↓
Paso 1: Renderizar + Recolectar datos
    ↓
Validar Step 1
    ├─ ❌ Errores → Mostrar errores
    └─ ✅ Ok → Siguiente
    ↓
Paso 2, 3, 4... (repetir)
    ↓
Último paso completado
    ↓
VocabularyWizardData / SentenceWizardData / TextWizardData
    ↓
Convertir a formato BD (to_dict())
    ↓
Guardar en base de datos
    ↓
✅ Éxito / ❌ Error
```

---

## 🎯 Próximos Pasos

### Corto plazo (Sprint actual)
- [ ] Integrar asistentes en admin panel (nueva sección)
- [ ] Crear funciones `save_to_database()` para cada tipo
- [ ] Pruebas manuales de cada asistente
- [ ] Documentación de usuario

### Mediano plazo
- [ ] Integración con motor NLP para SEMI_AUTO
- [ ] Análisis automático de sintaxis (FULL_AUTO para oraciones)
- [ ] Validación de macrones latinos
- [ ] Estimación de tiempo de lectura

### Largo plazo
- [ ] Bulk import desde archivos (CSV, JSON)
- [ ] Historial de carga y rollback
- [ ] Sistema de sugerencias basado en contenido existente
- [ ] Exportación de data para auditoría

---

## 📚 Referencia de Módulos

### `utils/admin_data_assistants.py` (~500 líneas)

**Clases principales:**
- `AssistantStep` - Representa un paso del asistente
- `VocabularyWizardData` - Recolección de datos de vocabulario
- `SentenceWizardData` - Recolección de datos de oraciones
- `TextWizardData` - Recolección de datos de textos
- `BaseAssistant` - Clase base con lógica común
- `VocabularyAssistant` - Asistente de vocabulario
- `SentenceAssistant` - Asistente de oraciones
- `TextAssistant` - Asistente de textos
- `AssistantManager` - Gestor central

**Factory:**
```python
from utils.admin_data_assistants import create_assistant, DataType, AssistantMode

assistant = create_assistant(DataType.VOCABULARY, AssistantMode.MANUAL)
```

### `utils/admin_data_assistants_ui.py` (~400 líneas)

**Funciones principales:**
- `render_vocabulary_assistant(mode)` → VocabularyWizardData o None
- `render_sentence_assistant(mode)` → SentenceWizardData o None
- `render_text_assistant(mode)` → TextWizardData o None
- `render_assistant_mode_selector()` → (DataType, AssistantMode)
- `render_progress_bar(current, total)` → None (renderiza)
- `render_step_navigation(assistant)` → (prev_clicked, next_clicked)
- `render_field(field, key_prefix)` → valor del campo

**Uso típico:**
```python
from utils.admin_data_assistants_ui import render_vocabulary_assistant
from utils.admin_data_assistants import AssistantMode

result = render_vocabulary_assistant(AssistantMode.MANUAL)
if result:
    print(result.to_dict())  # Guardar en BD
```

---

## 🎓 Filosofía del Diseño

### 1. **No Abrumador**
- Un paso a la vez
- Solo campos relevantes visibles
- Ayuda contextual disponible

### 2. **Guiado**
- Indicadores de progreso claros
- Ejemplos en cada paso
- Validación inmediata

### 3. **Flexible**
- 3 modos: manual, semi-auto, automático
- Usuarios pueden cambiar de modo si lo necesitan
- Datos parciales se guardan en session_state

### 4. **Robusto**
- Validación en múltiples niveles
- Mensajes de error claros
- Nunca pierde datos del usuario

---

## 🚀 Estado Actual

**Creado:** 2025-12-07  
**Commit:** d7ac394  
**Estado:** ✅ Pronto para integración en Admin Panel

**Archivos:**
- ✅ `utils/admin_data_assistants.py` - Lógica base
- ✅ `utils/admin_data_assistants_ui.py` - Componentes UI
- ⏳ Integración en admin panel (pendiente)

---

**Próximo paso:** Integrar asistentes en `pages/99_⚙️_Administracion.py` como nueva sección.
