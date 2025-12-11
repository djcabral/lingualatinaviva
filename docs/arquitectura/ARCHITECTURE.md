# Refactored Architecture

## Overview
This document describes the refactored architecture for the Latin learning application. The new structure follows clean architecture principles with clear separation of concerns.

## Directory Structure
```
src/
├── core/                 # Core business logic and domain models
│   ├── entities/         # Domain entities
│   ├── interfaces/       # Abstract interfaces for services
│   ├── services/         # Business logic services
│   └── exceptions/       # Custom exceptions
├── infrastructure/       # Technical implementations
│   ├── database/         # Database implementations
│   ├── external/         # External service adapters
│   └── config/           # Configuration management
├── application/          # Application layer
│   ├── use_cases/        # Application use cases
│   └── dtos/             # Data transfer objects
├── presentation/         # Presentation layer
│   ├── streamlit/        # Streamlit UI components and pages
│   │   ├── components/   # Reusable UI components
│   │   ├── pages/        # Application pages
│   │   └── utils/        # Streamlit-specific utilities
│   └── cli/              # Command-line interface (if applicable)
├── shared/               # Shared utilities and helpers
│   ├── constants/        # Application constants
│   ├── enums/            # Enumerations
│   └── utils/            # Generic utility functions
└── tests/                # Test suite
    ├── unit/             # Unit tests
    ├── integration/      # Integration tests
    └── fixtures/         # Test data and mocks
```

## Key Improvements

1. **Clean Architecture**: Clear separation between business logic and technical implementation
2. **Single Responsibility**: Each module has a well-defined purpose
3. **Dependency Injection**: Components depend on abstractions, not concrete implementations
4. **Testability**: Easy to unit test business logic without database or UI dependencies
5. **Maintainability**: Changes in one layer don't affect others
6. **Scalability**: Easy to add new features or modify existing ones