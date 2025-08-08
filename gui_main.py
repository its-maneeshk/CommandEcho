"""
GUI Launcher for CommandEcho
Launch the graphical interface
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Launch CommandEcho GUI"""
    try:
        from gui.main_window import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"Error importing GUI components: {e}")
        print("Please ensure all dependencies are installed:")
        print("pip install -r requirements.txt")
    except Exception as e:
        print(f"Error starting GUI: {e}")

if __name__ == "__main__":
    main()
