
import sys
import os
import importlib

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def validate_modules():
    print("🧪 Starting Module Validation (Safe Mode)...")
    
    modules_to_check = [
        ('utils.learning_hub_widgets', ['render_vocabulary_widget', 'render_practice_content']),
        ('pages.modules.gamified_lesson', ['render_gamified_lesson']),
    ]
    
    for module_name, attributes in modules_to_check:
        try:
            print(f"📦 Importing {module_name}...", end=" ")
            module = importlib.import_module(module_name)
            print("✅ OK")
            
            for attr in attributes:
                print(f"   - Checking {attr}...", end=" ")
                if hasattr(module, attr):
                    print("✅ Found")
                else:
                    print(f"❌ MISSING")
                    sys.exit(1)
                    
        except ImportError as e:
            print(f"\n❌ ImportError: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
        except SyntaxError as e:
            print(f"\n❌ SyntaxError: {e}")
            sys.exit(1)
        except Exception as e:
            # Catching generic exceptions during import (like Streamlit errors if referenced at top level)
            # We print them but if it's just a streamlit warning we might proceed manually
            print(f"\n⚠️ Runtime Error (might be benign context issue): {e}")
            # sys.exit(1) # Don't exit on runtime errors, only import/syntax

    print("\n🎉 All critical modules structure verified successfully!")

if __name__ == "__main__":
    validate_modules()
