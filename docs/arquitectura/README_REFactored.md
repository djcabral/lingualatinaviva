# Lingua Latina Viva - Refactored Architecture

This document describes the refactored architecture of the Lingua Latina Viva application, designed to be more robust, maintainable, and performant.

## Architecture Overview

The refactored application follows a clean architecture pattern with clear separation of concerns:

```
lingua-latina-viva/
├── app/                  # Application core
│   ├── __init__.py
│   ├── config.py         # Application configuration
│   ├── core/             # Business logic and domain models
│   │   ├── entities/     # Domain entities
│   │   ├── services/     # Business services
│   │   └── exceptions.py # Custom exceptions
│   ├── infrastructure/   # Technical implementations
│   │   ├── persistence/  # Database implementations
│   │   ├── logging/      # Logging configuration
│   └── presentation/     # User interface layers
│       ├── streamlit/    # Streamlit interface
│       ├── textual/      # Textual interface
├── tests/                # Test suite
├── scripts/              # Utility scripts
├── data/                 # Data files
├── docs/                 # Documentation
├── refactored_requirements.txt  # Dependencies
└── README_REFactored.md
```

## Key Improvements

### 1. Separation of Concerns
- **Domain Entities**: Pure data structures representing core concepts
- **Services**: Business logic separated from presentation
- **Repositories**: Data access patterns abstracted from implementation
- **Presentation**: UI layers focused solely on user interaction

### 2. Performance Enhancements
- Caching strategies can be easily implemented at the service layer
- Database queries optimized through repository pattern
- Reduced coupling enables better optimization opportunities

### 3. Maintainability
- Clear module boundaries make code easier to understand
- Dependency injection enables easier testing
- Consistent patterns throughout the codebase

### 4. Testability
- Business logic separated from UI makes unit testing straightforward
- Repositories can be easily mocked for testing
- Services have well-defined interfaces

## Getting Started

1. Install dependencies:
```bash
pip install -r refactored_requirements.txt
```

2. Run the Streamlit application:
```bash
streamlit run app/presentation/streamlit/app.py
```

## Directory Structure Details

### `app/core/entities/`
Contains the domain entities that represent the core concepts of the application:
- Word: Represents a Latin word with all its properties
- User: Represents a user profile and progress
- ReviewLog: Represents a vocabulary review session

### `app/core/services/`
Contains business logic organized into services:
- VocabularyService: Handles vocabulary learning and SRS algorithms
- UserService: Manages user profiles and progress tracking

### `app/infrastructure/persistence/`
Implements the repository pattern for data access:
- Repositories for each entity type
- Abstract base classes for consistent interface

### `app/presentation/streamlit/`
Contains the Streamlit UI implementation:
- Main application entry point
- Page components
- UI utilities

## Migration Path

To migrate from the legacy structure to this refactored architecture:

1. Begin by implementing the core entities and services
2. Create repository implementations for data access
3. Gradually replace direct database calls with repository methods
4. Refactor UI components to use services instead of direct data access
5. Implement proper error handling and logging throughout

## Future Enhancements

This architecture supports several future enhancements:
- REST API layer for mobile applications
- Advanced analytics and reporting
- Machine learning integration for personalized learning paths
- Multi-user support with authentication
- Enhanced caching mechanisms