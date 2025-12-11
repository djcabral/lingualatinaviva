# 📝 Registro de Cambios

Todos los cambios notables a este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [Unreleased]

### Added
- Comprehensive refactored architecture with clean separation of concerns
- Library package (`lib/`) containing reusable components
- Docker support with Dockerfile and docker-compose.yml
- Setup script for proper package installation
- Comprehensive documentation for all components
- Recycling bin for deprecated files
- Performance improvements and optimizations

### Changed
- Updated project structure to follow clean architecture principles
- Migrated from Pydantic v1 to v2 (BaseSettings moved to pydantic-settings)
- Improved database connection handling and session management
- Enhanced UI components with better organization
- Refactored services to properly use database sessions

### Fixed
- Pydantic v2 compatibility issues with BaseSettings
- Database session management
- Dependency installation issues
- Circular import issues in models package

### Removed
- Deprecated and one-time use scripts moved to recycling bin
- Technical debt and obsolete code
- Redundant files and directories

## [1.0.0] - 2025-12-08

### Added
- Initial release of the refactored Lingua Latina Viva application
- Clean architecture implementation
- Core services for user and vocabulary management
- Reusable library components
- Containerization support
- Comprehensive documentation

### Changed
- Complete restructuring of the project layout
- Modernization of dependencies and libraries
- Improved code organization and maintainability
- Enhanced performance through better resource management

### Fixed
- Various architectural and performance issues from the original implementation
- Dependency management and installation process
- Code quality and consistency issues

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
