# Plan de Mejoras: Streamlit Inspirado en TSX

## Filosofía

> "El líquido es bueno y quita la sed, conservémoslo y mejoremos el envase para mejor presentación"

**Estrategia**: Mantener todo el contenido pedagógico sólido actual (30 lecciones, Collatinus, Stanza) y mejorar la experiencia de usuario adoptando los mejores patrones del proyecto TSX.

---

## Priorización: Mejoras de Alto Impacto

### ⭐⭐⭐⭐⭐ Crítico (Fase 1 - Semana 1)

#### 1. Sistema de Progresión Orgánica

**Inspiración**: `learningEngine.ts` del TSX

**Problema Actual**:

- La navegación es libre pero sin guía clara
- El estudiante puede perderse o saltarse pasos importantes
- No hay flujo pedagógico estructurado

**Solución**:
Implementar ciclo de 5 pasos que se desbloquean secuencialmente:

```
LECCIÓN (Teoría) → VOCABULARIO (50%) → EJERCICIOS (3x) → LECTURA → DESAFÍO
```

**Implementación**:

- Crear `utils/progression_engine.py`
- Tabla `UserLessonProgress` con campos:
  - `lesson_id`
  - `theory_completed` (bool)
  - `vocab_mastery` (float 0-1)
  - `exercises_count` (int)
  - `reading_completed` (bool)
  - `challenge_passed` (bool)
- Función `get_lesson_status(user_id, lesson_id)` → diccionario de estado
- Función `get_next_step_recommendation(user_id, lesson_id)` → mensaje + acción

**Archivos a Modificar**:

- `models/user.py` (nueva tabla)
- `utils/progression_engine.py` (nuevo)
- `pages/01_📚_Curso.py` (mostrar recomendación)
- `pages/modules/course_view.py` (marcar teoría completada)
- `pages/modules/vocab_view.py` (calcular mastery)
- `pages/modules/challenges_view.py` (desbloquear siguiente lección)

**Esfuerzo**: 🕐 6-8 horas

---

#### 2. Dashboard de Progreso Visual

**Inspiración**: `Dashboard.tsx` del TSX

**Problema Actual**:

- No hay un "mapa" visual del progreso
- El estudiante no ve su avance general

**Solución**:
Crear página principal tipo "mapa del tesoro" que muestre:

- Lección actual destacada
- Lecciones completadas (verde con ✓)
- Lecciones bloqueadas (gris con 🔒)
- Barra de progreso por lección (5 pasos)
- XP total y racha de días

**Implementación**:

- Modificar `lingua_latina_viva.py` (página principal)
- Usar `st.columns()` para grid de lecciones
- Cards con estados visuales (CSS personalizado)
- Llamar a `get_lesson_status()` para cada lección

**Mockup**:

```
┌─────────────────────────────────────┐
│  🏛️ LINGUA LATINA VIVA              │
│  Tu Progreso: Lección 5/30          │
│  XP: 2,450 pts | Racha: 7 días 🔥  │
└─────────────────────────────────────┘

┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐
│ L1 │ │ L2 │ │ L3 │ │ L4 │ │ L5 │
│ ✓  │ │ ✓  │ │ ✓  │ │ ✓  │ │ 🔄 │
│100%│ │100%│ │100%│ │100%│ │ 60%│
└────┘ └────┘ └────┘ └────┘ └────┘

┌────┐ ┌────┐ ┌────┐
│ L6 │ │ L7 │ │... │
│ 🔒 │ │ 🔒 │ │ 🔒 │
└────┘ └────┘ └────┘

📍 SIGUIENTE PASO RECOMENDADO:
Paso 3: Completa 3 sesiones de ejercicios (1/3)
[Ir a Ejercicios →]
```

**Archivos**:

- `lingua_latina_viva.py` (reescritura completa)
- `utils/ui_components.py` (funciones para cards)
- `static/custom.css` (estilos para cards)

**Esfuerzo**: 🕐 4-5 horas

---

### ⭐⭐⭐⭐ Alto Impacto (Fase 2 - Semana 2)

#### 3. Motor de Recomendaciones Inteligente

**Inspiración**: `getRecommendations()` en TSX

**Problema Actual**:

- No hay guía sobre qué hacer a continuación

**Solución**:
Sistema que analiza progreso y recomienda la siguiente acción óptima.

**Implementación**:

```python
# utils/recommendation_engine.py

def get_recommendations(user_id):
    """
    Retorna lista de recomendaciones priorizadas.
    
    Returns:
        List[dict]: [
            {
                'type': 'vocab' | 'exercise' | 'reading' | 'challenge',
                'priority': 'high' | 'medium' | 'low',
                'message': 'Domina el 50% del vocabulario...',
                'action_page': 'Práctica',
                'action_view': 'vocab',
                'lesson_id': 5
            }
        ]
    """
    progress = get_user_progress(user_id)
    current_lesson = progress['current_lesson']
    status = get_lesson_status(user_id, current_lesson)
    
    recs = []
    
    # Lógica de priorización
    if not status['theory_completed']:
        recs.append({
            'priority': 'high',
            'message': f'📖 Lee la teoría de la Lección {current_lesson}',
            'action_page': 'Curso',
            ...
        })
    elif status['vocab_mastery'] < 0.5:
        recs.append({
            'priority': 'high',
            'message': f'🧠 Domina el vocabulario ({status["vocab_mastery"]*100:.0f}% actual)',
            'action_page': 'Práctica',
            'action_view': 'vocab',
            ...
        })
    # ... más lógica
    
    return recs
```

**Integración**:

- Mostrar en dashboard principal
- Banner destacado en todas las páginas
- Botón de acción directa

**Archivos**:

- `utils/recommendation_engine.py` (nuevo)
- `lingua_latina_viva.py` (mostrar recomendación)
- Todas las páginas (banner superior)

**Esfuerzo**: 🕐 3-4 horas

---

#### 4. Sistema de Ayuda Contextual (Sin Costos API)

**Alternativa**: Sistema de ayuda basado en reglas + FAQ interactivo

**Problema Actual**:

- No hay asistencia integrada para dudas comunes
- ~~Tutor IA tendría costos de API continuos~~ ❌

**Solución sin Costos**:
Sistema de ayuda inteligente basado en patrones y contexto del usuario

**Componentes**:

**a) Help System Contextual**

```python
# utils/help_system.py

HELP_PATTERNS = {
    'declension_1': {
        'keywords': ['puella', 'rosa', 'primera declinación', '-ae'],
        'title': '📚 Ayuda: Primera Declinación',
        'content': '''
        La primera declinación se caracteriza por:
        - Genitivo singular en **-ae**
        - Principalmente sustantivos femeninos
        
        Paradigma de "puella" (niña):
        [Tabla visual]
        
        Palabras comunes: puella, rosa, via, terra
        ''',
        'examples': [...],
        'common_errors': [
            'Confundir nominativo plural con genitivo singular (ambos -ae)',
            'Olvidar que algunos masculinos usan esta declinación (poeta, nauta)'
        ]
    },
    # ... más patrones
}

def get_contextual_help(lesson_id, user_query, recent_errors):
    """
    Retorna ayuda relevante basada en:
    - Lección actual
    - Texto de consulta del usuario
    - Errores recientes del usuario
    """
    # Buscar en patrones por keywords
    # Filtrar por lección
    # Priorizar temas con errores recientes
    return help_articles
```

**b) FAQ Interactivo**
Base de conocimiento estructurada con 100+ preguntas frecuentes:

- Organizada por temas (declinaciones, conjugaciones, sintaxis, etc.)
- Búsqueda por palabras clave
- Ejemplos visuales
- Links a lecciones relacionadas

**c) Glosario de Términos**
Diccionario de términos gramaticales con explicaciones simples:

- "Nominativo", "Acusativo", "Ablativo", etc.
- "Perifrástica", "Deponente", "Supino"
- Ejemplos en cada definición

**d) Tips Contextuales**
Hints automáticos basados en el progreso:

```python
def get_lesson_tips(lesson_id, user_progress):
    """
    Retorna 3-5 tips relevantes para la lección actual
    """
    TIPS = {
        1: [
            "💡 Tip: En latín, el orden de palabras es más flexible que en español",
            "💡 Memoriza 'puella' como palabra clave para la 1ª declinación",
            "💡 El nominativo responde a '¿quién?' y el acusativo a '¿qué?'"
        ],
        # ...
    }
    return TIPS.get(lesson_id, [])
```

**e) Asistente de Análisis Morfológico**
Herramienta offline que analiza palabras sin API:

```python
def analyze_word_offline(word):
    """
    Análisis básico usando:
    1. Collatinus (base de datos local)
    2. Heurísticas por terminaciones
    3. Diccionario local
    
    Returns:
        {
            'lemma': 'puella',
            'forms': ['puellae (gen sg)', 'puellae (nom pl)'],
            'definitions': ['niña', 'muchacha'],
            'declension': '1ª',
            'gender': 'fem'
        }
    """
```

**Implementación**:

- Nueva página: `pages/07_❓_Ayuda.py`
- Buscador de FAQ
- Glosario navegable
- Analizador de palabras (Collatinus)
- Tips de la lección actual

**UI**:

```
┌────────────────────────────────────┐
│  ❓ Centro de Ayuda                │
├────────────────────────────────────┤
│  🔍 Buscar: [___________________] │
│                                    │
│  📚 Temas Frecuentes:              │
│  ├─ Declinaciones                 │
│  ├─ Conjugaciones                 │
│  ├─ Sintaxis                      │
│  └─ Vocabulario                   │
│                                    │
│  🔤 Analizador de Palabras:       │
│  Ingresa una palabra: [________]  │
│  [Analizar]                       │
│                                    │
│  💡 Tips para Lección 5:          │
│  • Memoriza el paradigma de bonus │
│  • Los adjetivos concuerdan en... │
└────────────────────────────────────┘
```

**Archivos**:

- `pages/07_❓_Ayuda.py` (nuevo)
- `utils/help_system.py` (nuevo)
- `data/faq.json` (base de conocimiento)
- `data/glossary.json` (glosario)
- Integrar análisis Collatinus existente

**Ventajas vs AI Tutor**:

- ✅ **Costo cero** (todo local)
- ✅ **Respuestas instantáneas** (sin latencia de API)
- ✅ **Siempre disponible** (offline)
- ✅ **Respuestas consistentes** y verificadas
- ✅ **Integración con Collatinus** (análisis preciso)

**Limitaciones vs AI Tutor**:

- ❌ No conversacional
- ❌ No genera ejercicios dinámicos
- ❌ Requiere actualización manual del contenido

**Esfuerzo**: 🕐 6-8 horas (pero valor permanente)

---

#### 5. Sistema SRS Mejorado

**Inspiración**: `SRS.tsx` (flashcards 3D y algoritmo de repetición)

**Problema Actual**:

- Sistema de vocabulario muy básico
- Sin algoritmo de repetición espaciada real

**Solución**:
Implementar algoritmo **SM-2** (SuperMemo 2) simplificado

**Algoritmo SM-2 Simplificado**:

```python
def update_card_sm2(card, quality):
    """
    quality: 0-5 (0=total olvido, 5=perfecto)
    
    Actualiza:
    - easiness_factor (EF): facilidad de la tarjeta
    - interval: días hasta próxima revisión
    - repetitions: contador de repeticiones correctas
    """
    if quality < 3:  # Respuesta incorrecta
        card.repetitions = 0
        card.interval = 1
    else:
        card.repetitions += 1
        if card.repetitions == 1:
            card.interval = 1
        elif card.repetitions == 2:
            card.interval = 6
        else:
            card.interval = round(card.interval * card.easiness_factor)
    
    # Ajustar EF
    card.easiness_factor += (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    card.easiness_factor = max(1.3, card.easiness_factor)
    
    # Próxima revisión
    card.next_review = datetime.now() + timedelta(days=card.interval)
    
    return card
```

**UI Mejorada**:

- Animación de volteo (CSS)
- Botones de calificación: "Otra vez", "Difícil", "Bien", "Fácil"
- Estadísticas: "Nuevas", "Por repasar", "Dominadas"
- Filtro por lección

**Tabla Nueva**:

```sql
CREATE TABLE flashcard_progress (
    user_id INT,
    word_id INT,
    easiness_factor REAL DEFAULT 2.5,
    interval INT DEFAULT 0,
    repetitions INT DEFAULT 0,
    next_review TIMESTAMP,
    last_quality INT,
    PRIMARY KEY (user_id, word_id)
);
```

**Archivos**:

- `models/flashcard.py` (nueva tabla)
- `utils/srs_algorithm.py` (nuevo - algoritmo SM-2)
- `pages/modules/vocab_view.py` (reescribir con nuevo sistema)
- `static/flashcard.css` (animaciones)

**Esfuerzo**: 🕐 6-7 horas

---

### ⭐⭐⭐ Impacto Medio (Fase 3 - Semana 3)

#### 6. Mejoras de UI/UX

**a) CSS Personalizado Premium**

Crear `static/premium.css` con:

- Paleta de colores romana (terracota, oro, ocre)
- Tipografía mejorada (Cinzel para títulos, Merriweather para textos)
- Animaciones suaves (hover, transiciones)
- Cards con sombras y bordes estilizados
- Botones con efectos premium

**b) Componentes Visuales Reutilizables**

Crear en `utils/ui_components.py`:

```python
def lesson_card(lesson_id, status, title):
    """Card visual para lección con estado"""
    
def progress_bar(percentage, label):
    """Barra de progreso estilizada"""
    
def stat_badge(value, label, icon):
    """Badge para estadísticas (XP, racha, etc.)"""
    
def recommendation_banner(message, action_button):
    """Banner destacado para recomendaciones"""
```

**c) Responsive Design Mejorado**

- Usar `st.container()` con max-width
- Grid adaptativo con `st.columns()`
- Ocultar sidebar en móvil por defecto

**Archivos**:

- `static/premium.css` (nuevo)
- `utils/ui_components.py` (ampliar)
- Todas las páginas (aplicar componentes)

**Esfuerzo**: 🕐 5-6 horas

---

#### 7. Gamificación Expandida

**Sistema de XP y Niveles**:

```python
XP_REWARDS = {
    'lesson_theory': 100,
    'vocab_word_learned': 10,
    'exercise_perfect': 50,
    'exercise_good': 30,
    'reading_completed': 75,
    'challenge_passed': 200,
    'daily_streak': 25
}

LEVELS = [
    (0, "Tiro", "🎓"),          # Principiante
    (500, "Discipulus", "📚"),   # Estudiante
    (1500, "Scholasticus", "🏛️"), # Académico
    (3000, "Magister", "👨‍🏫"),    # Maestro
    (5000, "Grammaticus", "📖"),  # Gramático
    (8000, "Rhetor", "🎭")        # Retórico
]
```

**Logros**:

- "Primera Lección": Completa L1
- "Políglota": Domina 100 palabras
- "Marathonista": 7 días de racha
- "Perfeccionista": 10 ejercicios perfectos
- "Lector Ávido": 5 lecturas completadas

**Visualización**:

- Badge de nivel en header
- Progreso a siguiente nivel (barra)
- Galería de logros desbloqueados
- Animación al subir de nivel (confetti con `streamlit-extras`)

**Archivos**:

- `models/user.py` (campos xp, level, logros)
- `utils/gamification.py` (nuevo)
- `lingua_latina_viva.py` (mostrar nivel/XP)

**Esfuerzo**: 🕐 4-5 horas

---

### ⭐⭐ Nice to Have (Fase 4 - Semana 4)

#### 8. Análisis y Estadísticas

Dashboard personal de aprendizaje:

- Gráfico de progreso temporal (palabras aprendidas/semana)
- Mapa de calor de actividad (estilo GitHub)
- Tiempo dedicado por categoría
- Palabras más difíciles
- Recomendaciones de repaso

**Herramienta**: `plotly` o `altair` para gráficos interactivos

**Esfuerzo**: 🕐 3-4 horas

---

#### 9. Modo Offline Parcial

Inspirado en el fallback de TSX:

- Detectar si Gemini API está disponible
- Fallback a ejercicios estáticos JSON
- Mensaje claro: "Modo Offline - Funcionalidad limitada"
- Análisis morfológico básico con heurísticas

**Esfuerzo**: 🕐 2-3 horas

---

## Cronograma de Implementación

### **Semana 1: Fundamentos** (16-18 horas)

- ✅ Día 1-2: Sistema de progresión orgánica (6-8h)
- ✅ Día 3-4: Dashboard visual (4-5h)
- ✅ Día 5: Motor de recomendaciones (3-4h)

**Entregable**: App con flujo pedagógico guiado y mapa de progreso

---

### **Semana 2: Herramientas de Aprendizaje** (16-20 horas)

- ✅ Día 1-3: Sistema de Ayuda Contextual **sin costos** (6-8h)
  - FAQ interactivo
  - Glosario de términos
  - Tips contextuales
  - Analizador morfológico (Collatinus)
- ✅ Día 4-6: Sistema SRS mejorado (6-7h)
  - Algoritmo SM-2
  - UI con flip cards
  - Estadísticas de repaso
- ✅ Día 7: Gamificación básica (4-5h)
  - Sistema XP
  - Niveles
  - Logros básicos

**Entregable**: App con sistema de ayuda completo, SRS funcional, y motivación (XP/niveles)

---

### **Semana 3: Pulido** (10-12 horas)

- ✅ Día 1-3: CSS premium y componentes UI (5-6h)
- ✅ Día 4-5: Gamificación expandida (logros, niveles) (4-5h)
- ✅ Día 6: Testing y ajustes

**Entregable**: App con diseño premium y gamificación completa

---

### **Semana 4: Extras** (Opcional, 5-7 horas)

- ✅ Estadísticas y análisis
- ✅ Modo offline parcial
- ✅ Documentación de usuario

---

## Criterios de Éxito

Al finalizar, la aplicación deberá:

1. ✅ Guiar al estudiante paso a paso (sin perderse)
2. ✅ Mostrar progreso visual claro
3. ✅ Recomendar siguiente acción siempre
4. ✅ Tener asistente IA funcional
5. ✅ SRS con algoritmo real de repetición espaciada
6. ✅ Diseño visualmente atractivo (dentro de Streamlit)
7. ✅ Sistema de motivación (XP, niveles, logros)

---

## Ventajas de Esta Estrategia

✅ **Bajo Riesgo**: No tocamos contenido existente  
✅ **Incremental**: Cada semana hay mejora visible  
✅ **Reversible**: Cambios no destructivos  
✅ **Probado**: Patrones del TSX ya validados  
✅ **Pragmático**: Enfoque en impacto/esfuerzo  

---

## Próximos Pasos Inmediatos

### Esta Semana

1. **Crear estructura de base de datos** (`UserLessonProgress`)
2. **Implementar `progression_engine.py`**
3. **Modificar `lingua_latina_viva.py`** (dashboard)
4. **Probar flujo completo** con Lección 1

¿Comenzamos con la Fase 1?
