# Utility Library Documentation

This directory contains reusable utility functions and classes that are essential for the application's operation. These utilities have been extracted from various single-use scripts and organized into a coherent library structure.

## Modules

### benchmark.py
Provides decorators for measuring function performance and execution time.

Functions:
- `benchmark(func)`: Basic decorator to measure execution time
- `benchmark_with_stats(func)`: Advanced decorator with statistical analysis

### text_utils.py
Utilities for processing and normalizing Latin text.

Functions:
- `normalize_latin(text)`: Removes macrons and diacritics from Latin text
- `clean_latin_input(text)`: Cleans and normalizes user input
- `is_homograph(word)`: Checks if a word is a homograph (contains digits)
- `remove_homograph_digits(word)`: Removes disambiguation digits from homographs
- `get_disambiguation_hint(word_data)`: Generates disambiguation hints for homographs
- `display_word_with_disambiguation(word, word_data)`: Prepares words for display with disambiguation
- `extract_latin_words(text)`: Extracts Latin words from text
- `compare_latin_words(word1, word2, case_sensitive)`: Compares Latin words ignoring macrons

### ui_helpers.py
Streamlit UI helper functions for consistent interface elements.

Functions:
- `load_css()`: Loads custom CSS styles
- `render_page_header(title, icon)`: Renders consistent page headers
- `render_stat_box(label, value, help_text)`: Displays styled statistic boxes
- `get_session_defaults()`: Initializes default session state values
- `render_sidebar_footer()`: Renders sidebar footer with project info
- `show_success_with_xp(message, xp_gained)`: Shows success messages with XP gains
- `confirm_action(action_name, warning_message)`: Requests user confirmation
- `show_loading_spinner(message)`: Context manager for loading spinners
- `render_styled_table(headers, rows)`: Renders styled HTML tables
- `render_sidebar_config()`: Renders sidebar configuration controls

### mermaid_helper.py
Helper for rendering Mermaid diagrams in Streamlit.

Functions:
- `render_mermaid(diagram_code, height)`: Renders Mermaid diagrams

### syntax_analyzer.py
Latin syntactic analysis using LatinCy.

Classes:
- `LatinSyntaxAnalyzer`: Analyzes Latin sentences and extracts syntactic functions

Methods:
- `analyze_sentence(latin_text, translation, source, level, lesson_number)`: Analyzes a Latin sentence
- `_extract_dependencies(doc)`: Extracts dependency tree
- `_extract_syntax_roles(doc)`: Maps spaCy dependencies to traditional syntactic functions
- `_detect_constructions(doc)`: Detects special Latin constructions
- `_classify_sentence(doc)`: Classifies sentence type
- `_generate_tree_diagram(doc)`: Generates dependency tree SVG diagram
- `batch_analyze(sentences)`: Analyzes multiple sentences

### stanza_spinner.py
Utility for showing a spinner while initializing the Stanza analyzer.

Functions:
- `initialize_stanza_with_spinner()`: Initializes Stanza analyzer with loading spinner

## Usage

Import utilities from the specific modules as needed:

```python
from utils.text_utils import normalize_latin
from utils.ui_helpers import render_page_header
from utils.syntax_analyzer import LatinSyntaxAnalyzer
```