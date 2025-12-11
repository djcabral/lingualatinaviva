# Migration Guide: Old Structure to Refactored Structure

## Overview

This guide explains how to migrate from the legacy code structure to the new, more robust and maintainable structure.

## Key Changes

### 1. Directory Structure

**Old Structure:**
```
.
├── app.py
├── pages/
├── database/
├── utils/
├── src/
└── ...
```

**New Structure:**
```
.
├── app/                 # Core application logic
│   ├── models/          # Domain and database models
│   ├── services/        # Business logic
│   ├── repositories/     # Data access layer
│   └── config/          # Configuration
├── ui/                  # User interfaces
│   ├── streamlit/       # Streamlit UI
│   └── textual/         # Textual TUI
├── data/
├── scripts/
└── tests/
```

### 2. Separation of Concerns

The new structure follows clean architecture principles:
- **Models**: Data structures and domain entities
- **Repositories**: Data access layer
- **Services**: Business logic
- **UI**: Presentation layer

### 3. Dependency Management

Dependencies are now managed more explicitly:
- Core dependencies in [requirements.txt](file:///home/diego/Projects/latin-python/requirements-refactored.txt)
- Development dependencies in `requirements-dev.txt`

## Migration Steps

### Step 1: Create New Structure

Copy the new directory structure to your project.

### Step 2: Move Models

Move database models from `database/models.py` to `app/models/database.py`.

### Step 3: Extract Business Logic

Extract business logic from Streamlit pages and put it in service classes.

Example transformation:

**Old (in page):**
```python
# In pages/some_page.py
def calculate_user_level(xp):
    return xp // 100 + 1
```

**New (in service):**
```python
# In app/services/user_service.py
class UserService:
    def calculate_user_level(self, xp: int) -> int:
        return xp // 100 + 1
```

### Step 4: Create Repositories

Create repository classes for data access operations.

### Step 5: Update UI Layer

Update Streamlit pages to use services instead of direct database access.

### Step 6: Configuration

Move configuration to `app/config/settings.py` using Pydantic.

## Benefits of the New Structure

1. **Maintainability**: Clear separation of concerns makes code easier to understand and modify
2. **Testability**: Services and repositories can be tested independently
3. **Scalability**: Easy to add new features without affecting existing code
4. **Performance**: Better organization enables targeted optimizations
5. **Collaboration**: Team members can work on different layers simultaneously

## Performance Improvements

1. **Caching**: Added `cachetools` for strategic caching
2. **Database**: Improved connection pooling
3. **Modularity**: Smaller, focused modules load faster
4. **Lazy Loading**: Components loaded only when needed

## Testing Strategy

1. Unit tests for services
2. Integration tests for repositories
3. UI tests for Streamlit components
4. End-to-end tests for critical user flows
