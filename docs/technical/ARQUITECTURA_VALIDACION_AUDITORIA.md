# 🏗️ ARQUITECTURA DEL SISTEMA DE VALIDACIÓN Y AUDITORÍA

## Diagrama de Flujo Completo

```
┌───────────────────────────────────────────────────────────────────┐
│                    PANEL DE ADMINISTRACIÓN                         │
│                 pages/99_⚙️_Administracion.py                      │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
   ┌─────────────┐  ┌──────────────┐  ┌────────────┐
   │  Asistente  │  │  Asistente   │  │ Asistente  │
   │ Vocabulario │  │  Oraciones   │  │   Textos   │
   └─────────────┘  └──────────────┘  └────────────┘
   (VocabularyAssistant, SentenceAssistant, TextAssistant)
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
        ┌──────────────────┴──────────────────┐
        │                                     │
        ▼                                     ▼
   ┌─────────────────────────────────────────────────────┐
   │     VALIDACIÓN + AUDITORÍA (CORE)                   │
   │  utils/admin_validation_audit.py                    │
   │                                                     │
   │  ┌─────────────────────────────────────────────┐   │
   │  │   ComprehensiveValidator                    │   │
   │  │   └─ Orquestador principal                  │   │
   │  │                                             │   │
   │  │  ┌──────────────────────────────────────┐   │   │
   │  │  │  DuplicateValidator                  │   │   │
   │  │  │  ├─ check_vocabulary_duplicate()     │   │   │
   │  │  │  ├─ check_sentence_duplicate()       │   │   │
   │  │  │  └─ check_text_duplicate()           │   │   │
   │  │  └──────────────────────────────────────┘   │   │
   │  │                                             │   │
   │  │  ┌──────────────────────────────────────┐   │   │
   │  │  │  CompletenessValidator               │   │   │
   │  │  │  ├─ validate_vocabulary()            │   │   │
   │  │  │  ├─ validate_sentence()              │   │   │
   │  │  │  └─ validate_text()                  │   │   │
   │  │  └──────────────────────────────────────┘   │   │
   │  │                                             │   │
   │  │  ┌──────────────────────────────────────┐   │   │
   │  │  │  AuditManager                        │   │   │
   │  │  │  ├─ create_vocabulary_audit()        │   │   │
   │  │  │  ├─ create_sentence_audit()          │   │   │
   │  │  │  ├─ create_text_audit()              │   │   │
   │  │  │  └─ export_audit_report()            │   │   │
   │  │  └──────────────────────────────────────┘   │   │
   │  └─────────────────────────────────────────────┘   │
   └─────────────────────────────────────────────────────┘
        │                      │                    │
        ▼                      ▼                    ▼
   ┌──────────┐           ┌──────────┐         ┌──────────┐
   │ValidationResult   │AuditLog   │ValidationLevel
   │ ✅ is_valid     │ timestamp  │🔴 ESTRICTO
   │ ❌ errors       │ action     │🟡 MODERADO
   │ ⚠️  warnings    │ user_id    │🟢 FLEXIBLE
   │ 📊 duplicates   │ data_type  │
   │ 📈 completeness │ validation_status
   │ 💡 suggestions  │ error_message
   │ 🏷️ missing_fields
   └──────────┘           └──────────┘         └──────────┘
        │                      │                    │
        └──────────────────────┼────────────────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼                             ▼
           ┌─────────────────────────────────────────┐
           │  UI COMPONENTS                          │
           │  utils/admin_validation_audit_ui.py     │
           │                                         │
           │  ├─ render_vocabulary_validation()      │
           │  ├─ render_sentence_validation()        │
           │  ├─ render_text_validation()            │
           │  ├─ render_audit_log_table()            │
           │  ├─ render_audit_log_details()          │
           │  ├─ render_audit_report_export()        │
           │  ├─ render_save_confirmation()          │
           │  ├─ render_validation_level_selector()  │
           │  └─ init_validator()                    │
           └──────────────┬──────────────────────────┘
                         │
                         ▼
                ┌─────────────────────┐
                │  STREAMLIT UI       │
                │  Feedback visual    │
                │  ✅ Estados         │
                │  ⚠️  Advertencias   │
                │  ❌ Errores        │
                │  📊 Métricas        │
                │   💾 Botones         │
                └─────────────────────┘
```

---

## Flujo de Datos: Cargar una Palabra

```
USUARIO
  │
  └─> Abre "Asistente de Vocabulario"
        │
        ├─> Selecciona Nivel: 🟡 MODERADO
        │
        ├─> Completa datos:
        │   ├─ Palabra: "puella"
        │   ├─ Traducción: "niña"
        │   ├─ POS: "noun"
        │   ├─ Genitivo: "puellae"
        │   ├─ Género: "f"
        │   └─ Declinación: "1ª"
        │
        └─> Hace clic en "Guardar"
              │
              ▼
        ┌─────────────────────────┐
        │ ComprehensiveValidator  │
        │ .validate_vocabulary()  │
        └────────┬────────────────┘
                 │
        ┌────────┴─────────┬─────────────────┐
        │                  │                 │
        ▼                  ▼                 ▼
   ┌──────────────┐  ┌───────────────┐  ┌─────────────┐
   │   DUPLICADOS │  │ COMPLETITUD   │  │ AUDITORÍA   │
   │              │  │               │  │             │
   │ DuplicateVal │  │ CompletenessVal  │ AuditManager│
   │ check_vocab  │  │ validate_vocab   │ create_audit│
   │              │  │                  │             │
   │ Busca en BD: │  │ Valida campos:   │ Registra:   │
   │ "puella"     │  │ ✅ palabra       │ timestamp   │
   │              │  │ ✅ traducción    │ usuario     │
   │ Resultado:   │  │ ✅ pos           │ acción      │
   │ ✅ NO dup    │  │ ✅ genitivo      │ datos       │
   │              │  │ ✅ género        │ validación  │
   │              │  │ ✅ declinación   │ completitud │
   │              │  │                  │             │
   │              │  │ Score: 100%      │             │
   └──────────────┘  └───────────────┘  └─────────────┘
        │                  │                    │
        └──────────────────┴────────────────────┘
                           │
                           ▼
                    ┌──────────────────────┐
                    │ ValidationResult     │
                    │ ✅ is_valid: true    │
                    │ errors: []           │
                    │ warnings: []         │
                    │ duplicates: []       │
                    │ completeness: 1.0    │
                    └────────┬─────────────┘
                             │
                             ▼
                    ┌──────────────────────┐
                    │ UI RENDERS FEEDBACK  │
                    │                      │
                    │ ✅ VÁLIDO            │
                    │ Completitud: 100%    │
                    │ Sin duplicados       │
                    │ Sin errores          │
                    │                      │
                    │ [Guardar] [Cancelar] │
                    └────────┬─────────────┘
                             │
                    Usuario hace clic "Guardar"
                             │
                             ▼
                    ┌──────────────────────┐
                    │ GUARDAR EN BD        │
                    │                      │
                    │ INSERT INTO word     │
                    │ VALUES (...)         │
                    │ ID: 725              │
                    └────────┬─────────────┘
                             │
                             ▼
                    ┌──────────────────────┐
                    │ AUDITORÍA REGISTRA   │
                    │ {                    │
                    │  timestamp: ...,     │
                    │  action: VOCAB_ADD,  │
                    │  user: admin_user,   │
                    │  status: success,    │
                    │  data_id: 725,       │
                    │  completeness: 100%  │
                    │ }                    │
                    └────────┬─────────────┘
                             │
                             ▼
                    ┌──────────────────────┐
                    │ CONFIRMACIÓN VISUAL  │
                    │                      │
                    │ ✅ Guardado!         │
                    │ ID: 725              │
                    │ 🎉 Disponible        │
                    └──────────────────────┘
```

---

## Arquitectura de Base de Datos

```
┌──────────────────────────────────────────┐
│          TABLA: word                     │
├──────────────────────────────────────────┤
│ id | latin | translation | pos | level  │
├──────────────────────────────────────────┤
│ ... | puella | niña | noun | 1 |        │
│ ... | ... | ... | ... | ... |           │
│ 725 | puella | niña | noun | 1 |        │
└──────────────────────────────────────────┘
              ▲
              │ (Validador busca aquí)
              │
         ┌────┴──────────────┐
         │                   │
    ✅ Duplicado?       ✅ Datos válidos?
    (check_vocab_dup)   (validate_vocab)
         │                   │
    ❌ SI → RECHAZA    ✅ SI → GUARDA + LOG
         │                   │
         │ 🟡 MODERADO       │
         │    ADVIERTE        │
         │                   │
         └─────────┬─────────┘
                   │
                   ▼
         ┌─────────────────────┐
         │ AUDITORÍA (en log)  │
         │ - Timestamp         │
         │ - Usuario           │
         │ - Acción            │
         │ - Datos exactos     │
         │ - Validación status │
         │ - Completitud %     │
         └─────────────────────┘
```

---

## Validador de Duplicados - Decisión

```
                    ¿Es duplicado?
                          │
            ┌─────────────┼─────────────┐
            │             │             │
            ▼             ▼             ▼
        ✅ EXACTO    ✅ SIMILAR    ❌ NO
        (100%)      (85%+)
            │             │             │
    ┌───────┴─────┐  ┌──────┴────┐  ┌──┴─────────┐
    │ ESTRICTO    │  │ ESTRICTO   │  │ TODOS OK   │
    │ ❌ RECHAZA  │  │ ✅ PERMITE │  │ ✅ PERMITE │
    │             │  │            │  │            │
    │ MODERADO    │  │ MODERADO   │  │            │
    │ ⚠️  ADVIERTE   │  │ ✅ PERMITE │  │            │
    │ ✅ PERMITE  │  │            │  │            │
    │             │  │ FLEXIBLE   │  │            │
    │ FLEXIBLE    │  │ ℹ️  INFORMA   │  │            │
    │ ℹ️  INFORMA    │  │ ✅ PERMITE │  │            │
    │ ✅ PERMITE  │  │            │  │            │
    └─────────────┘  └────────────┘  └────────────┘
```

---

## Validador de Completitud - Scoring

```
                VOCABULARIO
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
    OBLIGATORIOS RECOMENDADOS  OPCIONALES
    (3 campos)   (3-4 campos)   (varían)
        │           │           │
        ├─ Palabra  ├─ Genitivo ├─ Formas irregulares
        ├─ Traduc.  ├─ Género   ├─ Contextos
        ├─ POS      ├─ Declina. ├─ Notas
        │           ├─ Partes   │
        │           │  principales
        │           │
    Score = (Campos presentes / Total esperado)
        │
        ├─ 100% = Perfectamente completo
        ├─ 75%  = Todos obligatorios + algunos recomendados
        ├─ 50%  = Solo obligatorios
        └─ <50% = Incompleto
```

---

## Niveles de Validación - Matriz de Decisión

```
                          ESTRICTO    MODERADO    FLEXIBLE
                          ═════════   ═════════   ════════
¿Es duplicado?
  ├─ Exacto              ❌ RECHAZA   ⚠️  ADVIERTE   ℹ️  INFO
  ├─ Similar (85%+)      ✅ PERMITE   ✅ PERMITE    ℹ️  INFO
  └─ No                  ✅ PERMITE   ✅ PERMITE    ✅ PERMITE

¿Está completo? (score)
  ├─ 100%                ✅ OK        ✅ OK         ✅ OK
  ├─ 75-99%              ❌ RECHAZA   ✅ OK         ✅ OK
  ├─ 50-74%              ❌ RECHAZA   ❌ RECHAZA    ✅ OK
  └─ <50%                ❌ RECHAZA   ❌ RECHAZA    ✅ OK

Conclusión:
  ├─ ✅ VÁLIDO → GUARDA  ✅ PERMITE   ✅ PERMITE    ✅ PERMITE
  ├─ ⚠️  ADVERTENCIA      ❌ RECHAZA   ⚠️  ADVIERTE   ⚠️  ADVIERTE
  └─ ❌ INVÁLIDO          ❌ RECHAZA   ❌ RECHAZA    ⚠️  ADVIERTE
```

---

## Auditoría - Estructura de Log

```
┌─────────────────────────────────────┐
│         AUDIT LOG (JSON)             │
├─────────────────────────────────────┤
│                                     │
│  timestamp:                         │
│  "2025-12-07T14:30:45.123456"      │
│                                     │
│  action: "vocabulary_add"           │
│  ├─ vocabulary_add                  │
│  ├─ vocabulary_update               │
│  ├─ vocabulary_delete               │
│  ├─ sentence_add                    │
│  ├─ text_add                        │
│  ├─ validation_error                │
│  └─ duplicate_detected              │
│                                     │
│  user_id: "admin_user"              │
│                                     │
│  data_type: "vocabulary"            │
│  ├─ vocabulary                      │
│  ├─ sentence                        │
│  └─ text                            │
│                                     │
│  data_id: 725                       │
│  (ID en la BD después de insertar)  │
│                                     │
│  validation_status: "success"       │
│  ├─ success                         │
│  ├─ warning                         │
│  └─ error                           │
│                                     │
│  completeness_score: 0.95           │
│  (0-1, multiplicar por 100 = %)     │
│                                     │
│  duplicates_found: [...]            │
│  (Lista de duplicados detectados)   │
│                                     │
│  new_value: {                       │
│    latin_word: "puella",            │
│    translation: "niña",             │
│    ...                              │
│  }                                  │
│  (Exactamente qué datos se cargaron)│
│                                     │
│  error_message: null                │
│  (Si hay error, el mensaje)         │
│                                     │
│  ip_address: "192.168.1.100"        │
│  (Opcional, para tracking)          │
│                                     │
└─────────────────────────────────────┘
```

---

## Integración en Admin Panel

```
pages/99_⚙️_Administracion.py
            │
            ├─> Importar módulos:
            │   ├─ ComprehensiveValidator
            │   ├─ ValidationLevel
            │   ├─ render_validation_level_selector()
            │   ├─ render_vocabulary_validation()
            │   ├─ render_audit_log_table()
            │   └─ init_validator()
            │
            ├─> Crear sección "🧙 Asistentes":
            │   ├─ Selector: Tipo (Vocab/Sentence/Text)
            │   ├─ Selector: Nivel (ESTRICTO/MODERADO/FLEXIBLE)
            │   ├─ Asistente paso a paso
            │   ├─ Validación en tiempo real
            │   └─ Confirmación antes de guardar
            │
            ├─> Crear sección "📋 Auditoría":
            │   ├─ Tabla de logs
            │   ├─ Detalles expandibles
            │   ├─ Exportar (JSON/CSV)
            │   └─ Filtros por tipo/usuario/fecha
            │
            └─> Integración con BD
                ├─ Insertar en tabla Word
                ├─ Insertar en tabla SentenceAnalysis
                ├─ Insertar en tabla Text
                └─ Auditoría automática en cada insert
```

---

## Stack Técnico

```
FRONTEND (Streamlit)
├─ Componentes UI
├─ Formularios
├─ Tablas
├─ Gráficos de progreso
└─ Descargas (JSON/CSV)
    │
    └──> ValidationResult ──┐
         AuditLog ──────────┤
         ValidationLevel ───┤
                           │
BACKEND (Python)            │
├─ ComprehensiveValidator ◄─┘
├─ DuplicateValidator
├─ CompletenessValidator
├─ AuditManager
└─ Helpers
    │
    └──> BD (SQLite)
         ├─ Tabla: word
         ├─ Tabla: sentence_analysis
         ├─ Tabla: text
         └─ [Opcional] Tabla: audit_log

DEPENDENCIAS
├─ streamlit (UI)
├─ sqlmodel (ORM)
├─ sqlalchemy (DB)
├─ json (serialización)
├─ datetime (timestamps)
└─ python standard library (csv, difflib, etc.)
```

---

## Puntos Clave de Integración

```
1. INICIALIZACIÓN
   validator = init_validator(ValidationLevel.MODERATE)
   
2. VALIDACIÓN VOCABULARY
   result, audit_log = validator.validate_vocabulary_complete(data)
   
3. RENDERIZAR FEEDBACK
   render_vocabulary_validation(data, validator)
   
4. CONFIRMACIÓN
   if render_save_confirmation(result, data, 'vocabulary'):
       # Guardar en BD
       # Auditoría automática
       render_save_success_message('vocabulary', word_id)
   
5. VER AUDITORÍA
   render_audit_log_table(validator)
   render_audit_log_details(validator)
   
6. EXPORTAR
   render_audit_report_export(validator)
```

---

## Seguridad y Trazabilidad

```
CADA CARGA REGISTRA:
├─ WHO: Usuario (admin_user, user_id)
├─ WHAT: Datos exactos (new_value: {})
├─ WHEN: Timestamp ISO (2025-12-07T14:30:45)
├─ WHERE: IP address (192.168.1.100)
├─ HOW: Validación status (success/warning/error)
├─ COMPLETENESS: Score (0-1)
└─ DUPLICATES: Detectados ([] o [dup1, dup2])

BENEFICIOS:
✅ Auditoría completa → Cumplimiento normativo
✅ Trazabilidad → Saber quién hizo qué
✅ Control de calidad → Detectar errores
✅ Recuperación → Ver qué se cargó cuando
✅ Análisis → Métricas de completitud
```

---

**Esta arquitectura garantiza:**
✅ Integridad de datos
✅ Detección de duplicados
✅ Calidad (completitud)
✅ Trazabilidad (auditoría)
✅ Facilidad de uso (UI clara)
