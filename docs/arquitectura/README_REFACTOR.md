# Lingua Latina Viva - Refactored Architecture

## New Project Structure

```
lingua-latina-viva/
├── app/                     # Core application package
│   ├── __init__.py
│   ├── main.py             # Application entry point
│   ├── config/             # Configuration files
│   │   ├── __init__.py
│   │   ├── settings.py     # Application settings
│   │   └── logging_config.py
│   ├── models/             # Data models
│   │   ├── __init__.py
│   │   ├── core.py         # Core domain models
│   │   └── database.py     # Database models
│   ├── services/           # Business logic services
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── vocabulary_service.py
│   │   ├── lesson_service.py
│   │   ├── exercise_service.py
│   │   └── progress_service.py
│   ├── repositories/        # Data access layer
│   │   ├── __init__.py
│   │   ├── base.py         # Base repository class
│   │   ├── user_repo.py
│   │   ├── vocabulary_repo.py
│   │   └── lesson_repo.py
│   ├── api/                # API endpoints (if needed)
│   │   ├── __init__.py
│   │   └── routes.py
│   └── utils/              # Utility functions
│       ├── __init__.py
│       ├── helpers.py
│       └── exceptions.py
├── ui/                     # User interface components
│   ├── __init__.py
│   ├── streamlit/          # Streamlit UI
│   │   ├── __init__.py
│   │   ├── pages/          # Streamlit pages
│   │   ├── components/     # Reusable UI components
│   │   └── app.py          # Streamlit application
│   └── textual/            # Textual TUI (if still needed)
├── migrations/             # Database migrations
├── tests/                  # Test suite
├── scripts/                # Utility scripts
├── data/                   # Data files
├── docs/                   # Documentation
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Key Improvements

1. **Clear Separation of Concerns**:
   - Core business logic separated from UI
   - Data access abstracted through repositories
   - Services encapsulate business operations

2. **Better Performance**:
   - Optimized database queries
   - Caching strategies
   - Asynchronous operations where applicable

3. **Enhanced Maintainability**:
   - Modular structure with clear responsibilities
   - Consistent naming conventions
   - Comprehensive documentation

4. **Scalability**:
   - Easy to extend with new features
   - Support for multiple UI frameworks
   - Clean API design for future integrations