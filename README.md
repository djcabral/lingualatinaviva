# 🏛️ Lingua Latina Viva

**Una aplicación moderna para revivir una lengua eterna.**

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)
[![Status](https://img.shields.io/badge/Status-Active-success)]()

> *Non scholae, sed vitae discimus* - No aprendemos para la escuela, sino para la vida.

**Lingua Latina Viva** es una plataforma interactiva completa para el aprendizaje del latín clásico que combina rigor académico con tecnología moderna. Más que una simple aplicación, es un ecosistema educativo integral diseñado para llevarte desde los fundamentos hasta la lectura autónoma de textos clásicos auténticos.

## ✨ ¿Por qué Lingua Latina Viva?

### 🆚 Lo Que Nos Hace Únicos

| Característica | Lingua Latina Viva | Apps Tradicionales |
|----------------|-------------------|-------------------|
| **Curso Estructurado** | 40 lecciones progresivas con infogramas | Lecciones básicas limitadas |
| **Práctica Interactiva** | Declinatio, Conjugatio, Aventura, Desafíos | Ejercicios estáticos |
| **Juegos Didácticos** | Sopa de letras, crucigramas, clasificador | Sin gamificación |
| **Lectura Asistida** | Textos auténticos con análisis morfológico | Textos sin ayuda contextual |
| **SRS Inteligente** | Algoritmo SM-2 adaptativo | Repetición básica o inexistente |
| **Generadores** | Paradigmas completos de cualquier palabra | Tablas estáticas |
| **Análisis Sintáctico** | Descomposición de oraciones | No disponible |
| **Código Abierto** | GPL v3 - gratis y modificable | Cerrado y de pago |

## 🌟 Características Principales

### 📘 Curso Estructurado de 40 Lecciones

Progresión pedagógica desde cero hasta textos clásicos:
- **Lecciones 1-13** (Básico): Declinaciones, conjugaciones, casos fundamentales
- **Lecciones 14-20** (Intermedio): Sistema verbal completo, sintaxis
- **Lecciones 21-30** (Avanzado): Construcciones complejas, subordinadas
- **Lecciones 31-40** (Experto): César, Cicerón, Virgilio, Catulo, y más

Cada lección incluye:
- ✨ Infogramas educativos con estética romana
- 📊 Tablas paradigmáticas estilizadas
- 📐 Diagramas conceptuales interactivos
- 💡 Ejemplos contextualizados auténticos

### 🧠 Sistema de Vocabulario SRS

Sistema de Repetición Espaciada con algoritmo SM-2:
- 📚 +8,000 palabras latinas con traducciones completas
- 🎯 Tarjetas inteligentes que se adaptan a tu ritmo
- 📈 Estadísticas detalladas de progreso
- 🔄 Repaso automatizado basado en curva de olvido

### 💪 Práctica Gramatical Intensiva

Cinco modos de práctica integrados:
- **Declinatio**: Domina las 5 declinaciones con corrección instantánea
- **Conjugatio**: Practica las 4 conjugaciones en todos los tiempos y modos
- **Aventura**: Desafíos progresivos que desbloquean contenido
- **Desafíos**: Puzzles y acertijos gramaticales
- **Práctica Libre**: Explora sin restricciones

### 🎮 Ludus - Juegos Didácticos

Aprende jugando con tres juegos completamente funcionales:
- **🏺 Clasificador de Palabras**: Clasifica sustantivos por género, declinación, parisílabas/imparisílabas
- **🔍 Sopa de Letras**: Encuentra palabras latinas en grids de 8x8 a 12x12
- **🧩 Crucigramas**: Resuelve crucigramas con vocabulario latino

Todas con selección inteligente de vocabulario basada en tu progreso.

### 📖 Lectio - Lectura Asistida

Lee textos clásicos auténticos con ayuda contextual:
- 📜 Obras de César, Fedro, y autores clásicos
- 🔍 Análisis morfológico palabra por palabra
- 📖 Diccionario contextual integrado
- 🎨 Resaltado sintáctico

### 🔧 Generador de Paradigmas

Genera todas las formas de cualquier sustantivo o verbo:
- 📊 Paradigmas completos de declinación
- ⚡ Conjugaciones en todos los tiempos, modos y voces
- 🔄 Particulas, participios, gerundios, gerundivos
- 🎨 Visualización elegante con tablas profesionales

### 🔍 Análisis Sintáctico

Herramientas avanzadas de análisis:
- 🧩 Descomposición de oraciones latinas
- 📝 Identificación de casos y funciones sintácticas
- 🔗 Análisis de subordinación
- 💡 Explicaciones educativas

## 🚀 Inicio Rápido

### ☁️ Opción 1: Usa la App en Línea (Recomendado)

Accede directamente sin instalación:

👉 **[https://lingualatinaviva.streamlit.app](https://lingualatinaviva.streamlit.app)**

### 💻 Opción 2: Instalación Local

```bash
# Clonar el repositorio
git clone https://github.com/djcabral/lingualatinaviva.git
cd lingualatinaviva

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
streamlit run app.py
```

La aplicación se abrirá automáticamente en `http://localhost:8501`

## 📚 Documentación

### Para Usuarios
- 📖 [**Guía de Inicio Rápido**](docs/user-guide/getting-started.md) - Empieza en 5 minutos
- 📘 [**Resumen del Curso**](docs/user-guide/course-overview.md) - Las 40 lecciones explicadas
- 🎮 [**Guía de Juegos**](docs/user-guide/games.md) - Cómo aprovechar Ludus
- 💡 [**Entrenamiento de Vocabulario**](docs/user-guide/vocabulary-training.md) - Maximiza la retención
- 📝 [**Práctica Gramatical**](docs/user-guide/grammar-practice.md) - Domina declinaciones y conjugaciones
- 📖 [**Lectura Asistida**](docs/user-guide/reading-texts.md) - Lee textos clásicos

### Para Administradores
- 💾 [**Respaldo y Restauración**](docs/admin-guide/backup-restore.md) - Protege tu progreso
- 📥 [**Importación de Contenido**](docs/admin-guide/importing-content.md) - Vocabulario y textos personalizados
- 👤 [**Gestión de Usuarios**](docs/admin-guide/user-management.md) - Administra cuentas

### Para Desarrolladores
- 🏗️ [**Arquitectura**](docs/developer-guide/architecture.md) - Estructura técnica
- 🗄️ [**Esquema de Base de Datos**](docs/developer-guide/database-schema.md) - Modelos y relaciones
- 🤝 [**Guía de Contribución**](docs/developer-guide/contributing.md) - Cómo contribuir
- 📡 [**Referencia API**](docs/developer-guide/api-reference.md) - Funciones principales

### Documentación Técnica
- 📊 [**Estado del Proyecto**](docs/technical/project-status.md) - Funcionalidades y roadmap
- 🔍 [**Plan de Análisis Sintáctico**](docs/technical/syntax-parser-plan.md) - Mejoras futuras
- 🚀 [**Guía de Despliegue**](docs/technical/deployment.md) - Deploy en Streamlit Cloud

📋 **[Índice Completo de Documentación](docs/README.md)**

## 🛠️ Stack Tecnológico

- **Frontend**: Streamlit
- **Backend**: Python 3.9+
- **Base de Datos**: SQLite con SQLModel ORM
- **Morfología**: pycollatinus (adaptado de Collatinus)
- **Análisis**: Algoritmos personalizados de parsing
- **Visualización**: Matplotlib, Mermaid

## 📈 Roadmap

### ✅ v1.0 (Actual)
- [x] 40 lecciones completas con infogramas
- [x] Sistema SRS de vocabulario
- [x] Tres juegos didácticos funcionales
- [x] Generador de paradigmas
- [x] Lectura asistida de textos clásicos
- [x] Panel de administración

### 🔮 v1.1 (Próximo)
- [ ] Sistema de logros expandido
- [ ] Tabla de líderes
- [ ] Desafíos diarios automatizados
- [ ] Exportación de progreso a PDF
- [ ] Modo offline (PWA)

### 🚀 v2.0 (Futuro)
- [ ] App móvil nativa
- [ ] Soporte para latín eclesiástico/medieval
- [ ] API pública para integraciones
- [ ] Modo multijugador colaborativo
- [ ] Integración con corpus externos

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Este es un proyecto de código abierto.

1. Haz un fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

Lee nuestra [**Guía de Contribución**](docs/developer-guide/contributing.md) para más detalles.

## 🐛 Reportar Problemas

Encontraste un bug o tienes una sugerencia? [Abre un issue](https://github.com/djcabral/lingualatinaviva/issues/new)

## 📜 Licencia

Este proyecto está bajo la licencia **GNU General Public License v3.0**. Consulta el archivo [LICENSE](LICENSE) para más detalles.

### Atribuciones

- **Collatinus**: Morfología y análisis © Yves Ouvrard & Philippe Verkerk (GPL v3)
- **Diccionario Valbuena (1819)**: Dominio público
- **Código original**: © 2025 Diego J. Cabral (GPL v3)

## 💖 Apoya el Proyecto

Si Lingua Latina Viva te ayudó en tu aprendizaje del latín:
- ⭐ Dale una estrella en GitHub
- 🐦 Comparte con otros estudiantes
- 🤝 Contribuye código o documentación
- 📝 Reporta bugs y sugiere mejoras

## 📞 Contacto

- **GitHub**: [@djcabral](https://github.com/djcabral)
- **Issues**: [GitHub Issues](https://github.com/djcabral/lingualatinaviva/issues)

---

<div align="center">

**Hecho con ❤️ para la comunidad de estudiantes de latín**

*Dum spiro, spero* - Mientras respiro, espero

🏛️ **Lingua Latina Viva** 🏛️

[⬆ Volver arriba](#-lingua-latina-viva)

</div>
