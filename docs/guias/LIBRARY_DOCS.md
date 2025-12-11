# Lingua Latina Viva Library Documentation

## Overview

This library contains the core reusable components of the Lingua Latina Viva application. These components have been identified as stable, well-tested, and suitable for reuse across different parts of the application or in other projects.

## Modules

### 1. UI (`lib/ui.py`)

Reusable UI components and helper functions for Streamlit applications.

#### Components:
- `render_stat_box`: Display statistics in styled boxes
- `render_progress_bar`: Custom progress bar component
- `render_page_header`: Consistent page header rendering
- `load_css`: Load custom CSS styles
- `render_sidebar_config`: Font size configuration in sidebar
- `render_breadcrumbs`: Navigation breadcrumbs
- `render_lesson_context`: Lesson context widget
- `render_quick_links`: Contextual quick links
- `render_recommendation_card`: Recommendation cards
- `render_unlock_message`: Locked content messages

#### Usage Example:
```python
from lib.ui import render_stat_box, render_page_header

render_page_header("My Dashboard", "📊")
col1, col2 = st.columns(2)
with col1:
    render_stat_box("Users", 120)
with col2:
    render_stat_box("Revenue", "$1,200")
```

### 2. Text (`lib/text.py`)

Utilities for processing and normalizing Latin text.

#### Functions:
- `normalize_latin`: Remove macrons and diacritics from Latin text
- `clean_latin_input`: Clean and normalize user input
- `is_homograph`: Detect if a word is a homograph
- `remove_homograph_digits`: Remove disambiguation digits from homographs
- `get_disambiguation_hint`: Generate disambiguation hint for homographs
- `display_word_with_disambiguation`: Prepare word for display with disambiguation
- `extract_latin_words`: Extract Latin words from text
- `compare_latin_words`: Compare two Latin words ignoring macrons

#### Usage Example:
```python
from lib.text import normalize_latin, compare_latin_words

# Normalize text with macrons
normalized = normalize_latin("puellārum")
print(normalized)  # Output: puellarum

# Compare words ignoring macrons
result = compare_latin_words("puellā", "puella")
print(result)  # Output: True
```

### 3. SRS (`lib/srs.py`)

Implementation of the SM-2 algorithm for spaced repetition learning.

#### Functions:
- `calculate_next_review`: Calculate next review date based on quality rating

#### Usage Example:
```python
from lib.srs import calculate_next_review

# First review
result = calculate_next_review(quality=4)
print(result['interval'])  # Output: 1

# Subsequent review with previous data
previous_review = {
    'ease_factor': 2.5,
    'interval': 1,
    'repetitions': 1
}
result = calculate_next_review(quality=4, previous_review=previous_review)
print(result['interval'])  # Output: 6
```

### 4. Gamification (`lib/gamification.py`)

Gamification system including XP calculation and level progression.

#### Functions:
- `calculate_level`: Calculate user level based on XP
- `process_xp_gain`: Add XP to user and update level if necessary
- `get_xp_for_level`: Calculate total XP required to reach a specific level
- `get_level_progress`: Calculate progress towards the next level

#### Usage Example:
```python
from lib.gamification import calculate_level, process_xp_gain

# Calculate level based on XP
level = calculate_level(400)
print(level)  # Output: 3

# Process XP gain
new_level, leveled_up = process_xp_gain(session, user, 50)
```

### 5. i18n (`lib/i18n.py`)

Internationalization support for the application.

#### Functions:
- `get_text`: Get translated text for a given key and language

#### Usage Example:
```python
from lib.i18n import get_text

# Get English translation
text = get_text("dashboard", "en")
print(text)  # Output: Dashboard

# Get Spanish translation (default)
text = get_text("dashboard")
print(text)  # Output: Tablero
```

## Creating the Recycling Bin

Let's create a directory to store unused scripts and files:

```bash
mkdir -p recycling_bin/scripts
mkdir -p recycling_bin/utils
mkdir -p recycling_bin/data
```

Files that are moved to the recycling bin include:
1. One-time use scripts that have served their purpose
2. Experimental code that is no longer needed
3. Old versions of files that have been superseded
4. Backup files and temporary data

This keeps the main project directory clean while preserving potentially useful code for future reference.