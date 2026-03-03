import json
import traceback

def safe_import():
    try:
        print("Importing simple modules...")
        import os
        import sys
        print("Done.")
    except Exception as e:
        traceback.print_exc()

safe_import()
