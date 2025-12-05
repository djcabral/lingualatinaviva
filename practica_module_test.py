#!/usr/bin/env python3
"""Test script to check all Práctica modules"""

import sys
import traceback

def test_module(module_name, module_path):
    print(f"\n{'='*60}")
    print(f"Testing: {module_name}")
    print(f"{'='*60}")
    try:
        module = __import__(module_path, fromlist=['render_content'])
        if hasattr(module, 'render_content'):
            print(f"✅ {module_name} imported successfully")
            print(f"   render_content function exists: YES")
        else:
            print(f"❌ {module_name} missing render_content function")
        return True
    except Exception as e:
        print(f"❌ {module_name} import FAILED")
        print(f"Error: {str(e)}")
        print("\nFull traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    modules = [
        ("Declinaciones", "pages.modules.declensions_view"),
        ("Conjugaciones", "pages.modules.conjugations_view"),
        ("Aventura", "pages.modules.adventure_view"),
        ("Desafíos", "pages.modules.challenges_view"),
    ]
    
    results = {}
    for name, path in modules:
        results[name] = test_module(name, path)
    
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for name, success in results.items():
        status = "✅ OK" if success else "❌ FAILED"
        print(f"{name:20} {status}")
