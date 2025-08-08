"""
Simple launcher script for CommandEcho
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Launch CommandEcho with options"""
    print("🤖 CommandEcho Launcher")
    print("=" * 30)
    print("1. GUI Mode (Graphical Interface)")
    print("2. Text Mode (Terminal)")
    print("3. Voice Mode (Full Voice)")
    print("4. Run Tests")
    print("5. Setup")
    print("6. Exit")
    
    while True:
        try:
            choice = input("\nSelect option (1-6): ").strip()
            
            if choice == "1":
                print("Starting CommandEcho GUI...")
                subprocess.run([sys.executable, "gui_main.py"])
                break
            
            elif choice == "2":
                print("Starting CommandEcho in text mode...")
                subprocess.run([sys.executable, "main.py", "--text-mode"])
                break
            
            elif choice == "3":
                print("Starting CommandEcho in voice mode...")
                subprocess.run([sys.executable, "main.py"])
                break
            
            elif choice == "4":
                print("Running installation tests...")
                subprocess.run([sys.executable, "test_installation.py"])
                break
            
            elif choice == "5":
                print("Running setup...")
                subprocess.run([sys.executable, "setup.py"])
                break
            
            elif choice == "6":
                print("Goodbye!")
                break
            
            else:
                print("Invalid choice. Please select 1-6.")
        
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
