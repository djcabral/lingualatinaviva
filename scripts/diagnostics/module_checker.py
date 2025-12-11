import sys
import os
import traceback

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

modules_to_check = [
    "pages.modules.conjugations_view",
    "pages.modules.adventure_view",
    "pages.modules.challenges_view"
]

print("Checking modules...")

for module_name in modules_to_check:
    print(f"\n--------------------------------------------------")
    print(f"Testing import: {module_name}")
    try:
        __import__(module_name)
        print(f"✅ Successfully imported {module_name}")
    except Exception as e:
        print(f"❌ Failed to import {module_name}")
        print(f"Error: {str(e)}")
        traceback.print_exc()
