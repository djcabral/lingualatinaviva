#!/usr/bin/env python3
"""
Run Script for Refactored Lingua Latina Viva Application
"""
import subprocess
import sys
import os
from pathlib import Path

def run_streamlit():
    """Run the refactored Streamlit application."""
    # Get the path to the streamlit app
    app_path = Path("ui/streamlit/app.py")
    
    if not app_path.exists():
        print("Error: Streamlit app not found at ui/streamlit/app.py")
        print("Make sure you're running this script from the project root directory")
        sys.exit(1)
    
    # Run the Streamlit app
    try:
        subprocess.run([
            "streamlit", "run", 
            str(app_path),
            "--server.headless=true",
            "--browser.gatherUsageStats=false"
        ])
    except FileNotFoundError:
        print("Error: Streamlit not found. Please install requirements:")
        print("pip install -r requirements-refactored.txt")
        sys.exit(1)

def run_tests():
    """Run the test suite."""
    try:
        subprocess.run(["python", "-m", "pytest", "tests/", "-v"])
    except FileNotFoundError:
        print("Error: pytest not found. Please install requirements:")
        print("pip install -r requirements-refactored.txt")
        sys.exit(1)

def show_help():
    """Show help message."""
    print("Lingua Latina Viva - Refactored Application")
    print("=" * 45)
    print("Usage: python run_refactored.py [command]")
    print()
    print("Commands:")
    print("  streamlit    Run the Streamlit application (default)")
    print("  test         Run the test suite")
    print("  help         Show this help message")
    print()
    print("Examples:")
    print("  python run_refactored.py")
    print("  python run_refactored.py streamlit")
    print("  python run_refactored.py test")

def main():
    """Main entry point."""
    if len(sys.argv) == 1:
        # Default command
        run_streamlit()
    else:
        command = sys.argv[1].lower()
        
        if command == "streamlit":
            run_streamlit()
        elif command == "test":
            run_tests()
        elif command == "help":
            show_help()
        else:
            print(f"Unknown command: {command}")
            show_help()
            sys.exit(1)

if __name__ == "__main__":
    main()