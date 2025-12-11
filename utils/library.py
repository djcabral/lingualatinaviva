"""
Utility Library
===============

A collection of commonly used utility functions and classes extracted from various
single-use scripts in the project. This library aims to provide reusable components
that can be used throughout the application.

Modules:
- benchmark: Performance measurement utilities
- text_utils: Latin text processing and normalization
- ui_helpers: Streamlit UI helper functions
- mermaid_helper: Mermaid diagram renderer
- syntax_analyzer: Latin syntactic analysis using LatinCy
- stanza_spinner: Stanza analyzer initialization with loading spinner
"""

# Import key utilities from various modules

# Benchmark utilities
from .benchmark import benchmark, benchmark_with_stats

# Text utilities
from .text_utils import (
    normalize_latin,
    clean_latin_input,
    is_homograph,
    remove_homograph_digits,
    get_disambiguation_hint,
    display_word_with_disambiguation,
    extract_latin_words,
    compare_latin_words
)

# UI helpers
from .ui_helpers import (
    load_css,
    render_page_header,
    render_stat_box,
    get_session_defaults,
    render_sidebar_footer,
    show_success_with_xp,
    confirm_action,
    show_loading_spinner,
    render_styled_table,
    render_sidebar_config
)

# Mermaid helper
from .mermaid_helper import render_mermaid

# Syntax analyzer
from .syntax_analyzer import LatinSyntaxAnalyzer

# Stanza spinner
from .stanza_spinner import initialize_stanza_with_spinner

__all__ = [
    # Benchmark
    'benchmark',
    'benchmark_with_stats',
    
    # Text utilities
    'normalize_latin',
    'clean_latin_input',
    'is_homograph',
    'remove_homograph_digits',
    'get_disambiguation_hint',
    'display_word_with_disambiguation',
    'extract_latin_words',
    'compare_latin_words',
    
    # UI helpers
    'load_css',
    'render_page_header',
    'render_stat_box',
    'get_session_defaults',
    'render_sidebar_footer',
    'show_success_with_xp',
    'confirm_action',
    'show_loading_spinner',
    'render_styled_table',
    'render_sidebar_config',
    
    # Mermaid helper
    'render_mermaid',
    
    # Syntax analyzer
    'LatinSyntaxAnalyzer',
    
    # Stanza spinner
    'initialize_stanza_with_spinner'
]

__version__ = '1.0.0'
__author__ = 'Lingua Latina Viva Team'