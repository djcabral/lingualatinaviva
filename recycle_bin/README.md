# Recycle Bin

This directory contains files that have been identified as non-essential for the core operation of the application. These files were previously scattered throughout the project and have been moved here for organizational purposes.

## Categories of Files

1. **Test/Debug Scripts** - Files used for testing specific functionality or debugging issues
2. **Experimental Code** - Proof-of-concept implementations or experimental features
3. **One-time Use Scripts** - Scripts that served a specific purpose and are no longer needed
4. **Old Versions** - Superseded implementations of existing functionality

## Files Moved

- `minimal_test.py` - Minimal test to reproduce database session issues
- `dbg_struct.py` - Debug structure utility
- `investigate_morphology.py` - Tool to investigate word morphology
- `model_test.py` - Test for UserProfile model
- `loader_test_run.py` - Test for content loader
- `practica_module_test.py` - Test for Práctica modules
- `run_diagnostics.py` - Diagnostic checker for imports
- `execution_test.py` - Comprehensive test simulating Streamlit module execution
- `run_refactored.py` - Runner for refactored application (duplicate functionality)

## Policy

Files in this directory:
- Are kept for historical reference only
- Are not actively maintained
- May not work with the current codebase
- Will be periodically reviewed for permanent deletion

If functionality from these files is needed, it should be reimplemented using the current architecture patterns.