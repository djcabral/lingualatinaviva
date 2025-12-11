
import sys
import os
import traceback

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

print("Starting diagnostic check...")

modules_to_check = [
    "pages.modules.declensions_view",
    "pages.modules.conjugations_view",
    "pages.modules.adventure_view",
    "pages.modules.challenges_view",
    "utils.challenge_engine"
]

for module in modules_to_check:
    print(f"\nChecking import: {module}")
    try:
        __import__(module)
        print(f"✅ Successfully imported {module}")
    except Exception as e:
        print(f"❌ Failed to import {module}")
        print(f"Error: {str(e)}")
        traceback.print_exc()

print("\nDiagnostic check complete.")
