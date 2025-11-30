# 📝 Registro de Cambios

Todos los cambios notables a este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [1.0.0] - 2025-11-29

### 🎉 Lanzamiento Inicial

Primera versión pública de Lingua Latina Viva con funcionalidades completas.

### ✨ Añadido

#### Curso Estructurado
- 40 lecciones completas de latín clásico (1-13 básicas, 14-20 intermedias, 21-30 avanzadas, 31-40 autores clásicos)
- Más de 30 infogramas educativos con estética romana
- Sistema de progreso con seguimiento de lecciones completadas
- Integración de contenido con tablas estilizadas y diagramas Mermaid

#### Vocabulario
- Sistema de Repetición Espaciada (SRS) con algoritmo SM-2
- Base de datos de +8,000 palabras latinas
- Tarjetas interactivas con pronunciación y ejemplos
- Estadísticas detalladas de progreso por palabra

#### Práctica Gramatical
- **Declinatio**: Ejercicios de declinaciones (5 declinaciones completas)
- **Conjugatio**: Práctica de conjugaciones verbales (4 conjugaciones)
- **Aventura**: Modo de desafíos progresivos
- **Desafíos**: Puzzles y acertijos gramaticales
- **Práctica Libre**: Modo sandbox para explorar

#### Lectura Asistida (Lectio)
- Textos clásicos auténticos (César, Fedro, etc.)
- Análisis morfológico palabra por palabra
- Diccionario contextual integrado
- Resaltado sintáctico

#### Juegos Didácticos (Ludus)
- **Clasificador de Palabras**: Clasifica sustantivos por género, declinación, parisílabas/imparisílabas
- **Sopa de Letras**: Encuentra palabras latinas en grids de 8x8 a 12x12
- **Crucigramas**: Resuelve crucigramas con claves en español
- Sistema de puntuación y precisión
- Selección inteligente de vocabulario basada en progreso

#### Herramientas de Análisis
- **Generador de Paradigmas**: Genera todas las formas de sustantivos y verbos
- **Análisis Sintáctico**: Descompone oraciones latinas
- **Diccionario**: Búsqueda de +8,000 términos con información completa

#### Sistema de Usuario
- Seguimiento de progreso individual
- Sistema de XP y logros
- Estadísticas detalladas de práctica
- Perfiles de usuario

#### Panel de Administración
- Importación de vocabulario desde CSV
- Gestión de textos para lectura
- Creación de desafíos personalizados
- Respaldos de base de datos
- Gestión de usuarios

### 🔧 Técnico
- Arquitectura Streamlit con módulos organizados
- Base de datos SQLite con SQLModel ORM
- Integración con pycollatinus para morfología
- Sistema de caché para rendimiento
- Estructura de datos normalizada

### 📚 Documentación
- README completo con instalación y despliegue
- Guías de usuario (inicio rápido, resumen del curso, juegos)
- Guías de administrador (respaldos, importación)
- Documentación técnica (arquitectura, esquema BD)
- Estructura de docs organizada en subcarpetas

### 🎨 Interfaz
- Diseño responsivo con CSS personalizado
- Tema oscuro/claro
- Iconografía romana consistente
- Animaciones sutiles y transiciones suaves
- Tablas estilizadas profesionales

---

## [Unreleased]

### 🚀 Próximas Funcionalidades
- Sistema de logros expandido
- Tabla de líderes global
- Modo multijugador para desafíos
- Exportación de progreso a PDF
- Integración con API de diccionarios externos
- Soporte para latín eclesiástico/medieval
- App móvil (PWA)

### 🐛 Correcciones Conocidas
- Optimización de rendimiento para grids grandes en Sopa de Letras
- Mejora en detección de participios en análisis sintáctico

---

## Formato de Versiones

### [X.Y.Z] - YYYY-MM-DD

- **X (Major)**: Cambios incompatibles en la API o estructura
- **Y (Minor)**: Nuevas funcionalidades compatibles hacia atrás
- **Z (Patch)**: Correcciones de bugs y mejoras menores

### Categorías de Cambios

- **✨ Añadido**: Nuevas funcionalidades
- **🔧 Cambiado**: Cambios en funcionalidades existentes
- **❌ Deprecado**: Funcionalidades que serán removidas
- **🗑️ Removido**: Funcionalidades eliminadas
- **🐛 Corregido**: Correcciones de bugs
- **🔒 Seguridad**: Correcciones de vulnerabilidades

---

*Semper discentes* (Siempre aprendiendo) 🏛️
