# Guía de Contribución - Lingua Latina Viva

## Bienvenido

Esta guía está diseñada para facilitar el desarrollo continuo de Lingua Latina Viva, ya sea que trabajes como desarrollador humano o como asistente de IA.

## Principios de Desarrollo

### 1. Autenticidad del Contenido
**REGLA FUNDAMENTAL**: Todo vocabulario y formas deben provenir de textos clásicos reales.

- ✅ **Correcto**: Importar palabras de Caesar, Cicero, Virgilio, Ørberg
- ❌ **Incorrecto**: Inventar palabras o usar latín medieval/eclesiástico sin indicarlo claramente

### 2. Coherencia con la Metodología Tradicional
El enfoque pedagógico debe seguir los métodos europeos tradicionales:

- Progresión estricta por niveles
- Énfasis en morfología antes de sintaxis compleja
- Práctica intensiva de declinaciones y conjugaciones
- Lectura de textos graduados

### 3. Código Limpio y Mantenible

#### Estilo de Código
- Seguir PEP 8 para Python
- Nombres de variables descriptivos en inglés
- Comentarios en español para lógica compleja
- Docstrings para todas las funciones públicas

#### Ejemplo:
```python
def decline_noun(word: str, declension: str, gender: str, genitive: str) -> Dict[str, str]:
    """
    Genera todas las formas de un sustantivo latino.
    
    Args:
        word: Forma nominativa del sustantivo
        declension: Número de declinación (1-5)
        gender: Género (m, f, n)
        genitive: Forma del genitivo singular
        
    Returns:
        Diccionario con claves como 'nom_sg', 'gen_pl', etc.
    """
    # Implementación...
```

### 4. Base de Datos Consistente

#### Reglas para Modelos
- Siempre importar desde `database.models`
- Nunca crear importaciones relativas como `from ..models`
- Usar `get_session()` con context manager

```python
# ✅ CORRECTO
from database.models import Word, ReviewLog
from database.connection import get_session

with get_session() as session:
    words = session.exec(select(Word)).all()

# ❌ INCORRECTO
from models import Word  # Causa errores de SQLAlchemy
from ..models import Word  # Importación relativa incorrecta
```

### 5. UI/UX Consistente

#### Estética
- Mantener tema clásico romano (fuentes Cinzel, colores tierras)
- Usar emojis consistentes para cada módulo
- Asegurar contraste adecuado para legibilidad

#### Idioma
- Interfaz en español
- Términos gramaticales en español (Nominativo, Acusativo, etc.)
- Títulos de secciones pueden incluir latín

## Estructura de Archivos

### Organización
```
/home/diego/Projects/latin-python/
├── app.py                    # NUNCA modificar la estructura base
├── pages/                    # Módulos de Streamlit
│   └── XX_emoji_Nombre.py   # Numeración secuencial
├── database/
│   ├── models.py            # Definición de modelos SQLModel
│   └── connection.py        # Gestión de sesiones
├── utils/                   # Lógica reutilizable
├── data/                    # Archivos de datos (CSV, JSON)
└── docs/                    # Documentación
```

### Convenciones de Nombres
- **Archivos Python**: snake_case.py
- **Clases**: PascalCase
- **Funciones/variables**: snake_case
- **Constantes**: UPPER_SNAKE_CASE

## Flujo de Trabajo de Desarrollo

### 1. Antes de Comenzar
- Leer `docs/ARCHITECTURE.md` para entender el sistema
- Revisar `docs/enhancement_plan.md` para contexto de mejoras planificadas
- Verificar la estructura actual con `tree` o `ls -la`

### 2. Añadir Nueva Funcionalidad

#### Paso 1: Planificar
```markdown
# Crear un plan en docs/implementation_plan.md
## Objetivo
[Descripción clara]

## Cambios Propuestos
- Archivo X: [cambios]
- Archivo Y: [cambios]

## Verificación
- Test 1: [descripción]
- Test 2: [descripción]
```

#### Paso 2: Implementar
- Hacer cambios atómicos (un archivo a la vez cuando sea posible)
- Probar cada cambio inmediatamente
- No hacer múltiples edits en paralelo al mismo archivo

#### Paso 3: Verificar
- Ejecutar la aplicación: `streamlit run app.py`
- Crear script de verificación si es necesario
- Documentar resultados

#### Paso 4: Documentar
- Actualizar `docs/walkthrough.md` con lo implementado
- Actualizar `README.md` si hay cambios user-facing
- Commit a Git

### 3. Modificar Base de Datos

#### Añadir Nueva Tabla
1. Definir modelo en `database/models.py`
2. Importar en `database/connection.py`
3. Ejecutar para crear tabla (SQLModel lo hace automáticamente)
4. Verificar con `sqlite3 lingua_latina.db ".schema"`

#### Ejemplo:
```python
# En database/models.py
class Author(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    difficulty_level: int  # 1-4
    description: Optional[str]
    
    # Relación
    texts: List["Text"] = Relationship(back_populates="author")
```

### 4. Añadir Nuevo Módulo de Práctica

#### Template Base
```python
# pages/XX_emoji_Nombre.py
import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.connection import get_session
from database.models import Word  # Importar modelos necesarios

# Configuración de página
st.set_page_config(page_title="Nombre", page_icon="emoji", layout="wide")

# Cargar CSS
def load_css():
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Título
st.markdown(
    """
    <h1 style='text-align: center; font-family: "Cinzel", serif; color: #8b4513;'>
        emoji Nombre - Descripción en Español
    </h1>
    """,
    unsafe_allow_html=True
)

# Lógica del módulo
# ...
```

## Testing

### Manual Testing
Antes de cada commit:
1. Ejecutar `streamlit run app.py`
2. Navegar a cada página afectada
3. Verificar que no hay errores en consola
4. Probar interacciones principales

### Automated Testing (Futuro)
```bash
pytest tests/
```

## Git Workflow

### Commits
```bash
# Antes de commit
git status
git diff

# Añadir archivos
git add [archivos específicos]

# Commit con mensaje descriptivo
git commit -m "feat: descripción clara del cambio"

# Tipos de commits:
# feat: nueva funcionalidad
# fix: corrección de bug
# docs: cambios en documentación
# refactor: refactorización de código
# test: añadir tests
```

### Mensajes de Commit
```
feat: añadir módulo de análisis morfológico
fix: corregir validación de sincretismo en Analysis
docs: actualizar ARCHITECTURE.md con nuevos modelos
refactor: normalizar imports de database.models
```

## Troubleshooting Común

### Error: SQLAlchemy InvalidRequestError
**Causa**: Múltiples imports de modelos desde rutas diferentes

**Solución**: 
```python
# ✅ Siempre usar:
from database.models import Word, ReviewLog

# ❌ NUNCA usar:
from models import Word
from ..models import Word
```

### Error: Streamlit no encuentra página
**Causa**: Nombre de archivo incorrecto en `pages/`

**Solución**: 
- Asegurar formato: `XX_emoji_Nombre.py`
- Verificar que hay al menos un emoji en el nombre

### Error: Base de datos bloqueada
**Causa**: Múltiples procesos de Streamlit corriendo

**Solución**:
```bash
pkill -f "streamlit run"
streamlit run app.py
```

## Recursos de Referencia

### Latín
- **Gramática**: Allen & Greenough's New Latin Grammar
- **Diccionario**: Lewis & Short Latin Dictionary
- **Frecuencias**: Dickinson College Core Vocabulary

### Desarrollo
- **Streamlit**: https://docs.streamlit.io
- **SQLModel**: https://sqlmodel.tiangolo.com
- **Python**: https://docs.python.org/3/

## Checklist de Calidad

Antes de considerar un cambio completo:

- [ ] Código sigue PEP 8
- [ ] Imports son correctos (`database.models`)
- [ ] UI mantiene estética romana
- [ ] Términos están en español
- [ ] No hay errores en consola
- [ ] Funcionalidad probada manualmente
- [ ] Documentación actualizada
- [ ] Commit hecho con mensaje descriptivo

## Preguntas Frecuentes

### ¿Puedo cambiar la estructura de la base de datos?
Sí, pero con cuidado. Añade nuevos campos como `Optional` primero para mantener compatibilidad.

### ¿Cómo añado nuevo vocabulario?
1. Preparar CSV con formato correcto
2. Crear script de importación en raíz del proyecto
3. Ejecutar script
4. Verificar con query SQL

### ¿Puedo usar librerías adicionales?
Sí, pero primero:
1. Verificar que es realmente necesaria
2. Añadir a `requirements.txt`
3. Documentar su propósito

### ¿Cómo manejo migraciones de base de datos?
Actualmente: recrear base de datos si es necesario (proyecto en desarrollo)
Futuro: usar Alembic para migraciones

## Contacto y Soporte

Para dudas sobre el desarrollo:
1. Revisar `docs/ARCHITECTURE.md`
2. Revisar `docs/AI_PROMPTS.md` (si eres IA)
3. Consultar código existente como referencia

---

**Recuerda**: El objetivo es crear una herramienta que permita a los usuarios disfrutar de los clásicos latinos. Cada línea de código debe servir a ese propósito.
