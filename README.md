# Lingua Latina Viva 📜

Una aplicación web completa para aprender latín clásico de manera intensiva, progresiva y adictiva, inspirada en la tradición europea más exigente (Ørberg, Wheelock, gymnasia alemanes y jesuitas del siglo XIX).

> **📖 Documentación del Proyecto**: Para desarrolladores y contribuyentes, consulta la documentación completa en el directorio [`docs/`](docs/)

## 🎯 Características

### Tecnologías
- **Framework**: Streamlit (interfaz web moderna y elegante)
- **Base de datos**: SQLite + SQLModel (100% offline)
- **SRS**: Algoritmo SM-2 completo (como Anki)
- **Estilo**: Tipografías clásicas (Cinzel, Cardo, Crimson Text) con estética de manuscrito medieval

### Módulos de Aprendizaje
1. **🏠 Home (Hodie)**: Dashboard con estadísticas, progreso y logros
2. **🎴 Vocabularium**: Flashcards con sistema de repetición espaciada (SRS)
3. **📜 Declinatio**: Práctica intensiva de declinaciones
4. **⚔️ Conjugatio**: Ejercicios de conjugación verbal
5. **🔍 Analysis**: Análisis morfológico de formas latinas
6. **📖 Lectio**: Lectura progresiva de textos auténticos
7. **⚙️ Admin**: Panel de administración para gestionar contenido

### Diseño
- Fondo pergamino con textura sutil
- Modo clásico con colores tierra y dorado
- Glassmorphism en las cajas de estadísticas
- Tipografías serif elegantes
- Animaciones suaves y transiciones fluidas

## 📁 Estructura del Proyecto

```
/home/diego/Projects/latin-python/
├── app.py                      # Punto de entrada principal
├── requirements.txt            # Dependencias Python
├── lingua_latina.db            # Base de datos SQLite (auto-generada)
├── assets/
│   └── style.css               # Estilos personalizados
├── data/
│   ├── words.csv               # Vocabulario (12 palabras de ejemplo)
│   └── texts/                  # Textos latinos auténticos
│       ├── phaedrus_lupus_agnus.txt
│       ├── caesar_gallia.txt
│       └── hyginus_chaos.txt
├── database/
│   ├── __init__.py
│   ├── models.py               # Modelos de datos (Word, ReviewLog, UserProfile)
│   ├── connection.py           # Conexión a la DB
│   └── seed.py                 # Script para poblar la DB
├── pages/                      # Páginas de Streamlit (navegación automática)
│   ├── 01_🏠_Home.py
│   ├── 02_🎴_Vocabularium.py
│   ├── 03_📜_Declinatio.py
│   ├── 04_⚔️_Conjugatio.py
│   ├── 05_🔍_Analysis.py
│   ├── 06_📖_Lectio.py
│   └── 07_⚙️_Admin.py
└── utils/
    ├── __init__.py
    ├── i18n.py                 # Traducciones (ES/EN)
    ├── latin_logic.py          # Lógica morfológica latina
    └── srs.py                  # Algoritmo SM-2

```

## 🚀 Instrucciones de Instalación y Ejecución

### 1. Instalar dependencias
```bash
cd /home/diego/Projects/latin-python
pip install -r requirements.txt
```

### 2. (Opcional) Poblar la base de datos con el script de seed
La base de datos se crea automáticamente al iniciar la app, pero si deseas usar el script de seed:
```bash
python -m database.seed
```

### 3. Ejecutar la aplicación
```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 💡 Uso de la Aplicación

### Primera vez
Al abrir la aplicación por primera vez, verás un pergamino de bienvenida:
> "Ave, discipule. Incipiamus iter per linguam aeternam."

Haz clic en **"Ingredere (Entrar)"** para comenzar.

### Panel de Admin
Usa el módulo **⚙️ Admin** para:
- Añadir nuevas palabras al vocabulario
- Ver estadísticas del sistema
- Agregar textos latinos auténticos
- Gestionar contenido

### Sistema SRS (Spaced Repetition)
El módulo **🎴 Vocabularium** usa un algoritmo de repetición espaciada:
- Cuando veas una palabra, califica qué tan bien la conocías
- El sistema calculará automáticamente cuándo debes repasarla
- Ganas XP con cada respuesta

## 📊 Gamificación

- **Niveles**: Progresa desde el nivel 1 hasta el 10
- **Rachas**: Mantén días consecutivos de práctica
- **PE (Puntos de Experiencia)**: Gana XP con cada ejercicio
- **Logros**: Desbloquea logros como "Primus Gradus", "Septimana Perfecta", etc.

## 🎨 Personalización

El archivo `assets/style.css` contiene todas las variables de diseño:
- Colores de fondo (pergamino)
- Tipografías (Cinzel, Cardo, Crimson Text)
- Estilos de botones y cajas
- Variables CSS para fácil personalización

## 📚 Datos de Ejemplo

La aplicación incluye:
- **12 palabras** de vocabulario básico en `data/words.csv`
- **3 textos** latinos auténticos:
  - Fedro: "Lupus et Agnus"
  - César: "De Bello Gallico I.1"
  - Higinio: "Fabula I: Chaos"

Para expandir el vocabulario, edita `data/words.csv` o usa el panel de Admin.

## 🔧 Desarrollo

### Añadir nuevas páginas
Simplemente crea un nuevo archivo en `pages/` con el formato:
```python
import streamlit as st
# ... tu código
```

Streamlit automáticamente lo agregará al menú lateral.

### Modificar la lógica latina
Edita `utils/latin_logic.py` para mejorar las funciones de declinación y conjugación.

### Cambiar el esquema de la base de datos
Modifica `database/models.py` y reinicia la aplicación.

## 📖 Recursos

- Vocabulario basado en fuentes auténticas
- Textos de autores clásicos (Fedro, César, Higinio, etc.)
- Metodología inspirada en Ørberg y Wheelock

## 📚 Documentación para Desarrolladores

El proyecto incluye documentación completa en el directorio `docs/`:

- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)**: Arquitectura del sistema, modelos de datos, componentes principales y diagramas
- **[CONTRIBUTING.md](docs/CONTRIBUTING.md)**: Guía de contribución con principios de desarrollo, troubleshooting y flujos de trabajo
- **[AI_PROMPTS.md](docs/AI_PROMPTS.md)**: Prompts específicos y plantillas para asistentes de IA
- **[enhancement_plan.md](docs/enhancement_plan.md)**: Plan de mejoras futuras basado en enfoque de corpus

### Para Comenzar a Desarrollar

1. Lee [ARCHITECTURE.md](docs/ARCHITECTURE.md) para entender la estructura del sistema
2. Revisa [CONTRIBUTING.md](docs/CONTRIBUTING.md) para conocer las reglas y convenciones
3. Si eres un asistente de IA, consulta [AI_PROMPTS.md](docs/AI_PROMPTS.md) para prompts específicos

## 🌟 Características Futuras

- Modo nocturno "Scriptorium" completo
- Mapa SVG del Imperio Romano
- Más textos auténticos
- Exportación a Anki
- Generación de ejercicios procedurales
- Sonidos de pluma y laurel

---

**Ave atque vale!** 🏛️
