"""
Setup script for CommandEcho
Helps with initial setup and dependency checking
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        "models",
        "data/memory", 
        "config",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def download_model_instructions():
    """Provide instructions for downloading the model"""
    print("\n" + "="*60)
    print("📥 MODEL DOWNLOAD INSTRUCTIONS")
    print("="*60)
    print("CommandEcho requires a local LLaMA model to function.")
    print("Please download a GGUF format model and place it in the models/ directory.")
    print()
    print("Recommended models:")
    print("1. Llama-3.2-3B-Instruct (smaller, faster)")
    print("   https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF")
    print()
    print("2. Llama-3.1-8B-Instruct (larger, more capable)")
    print("   https://huggingface.co/bartowski/Llama-3.1-8B-Instruct-GGUF")
    print()
    print("Download the Q4_K_M.gguf version for best balance of size and quality.")
    print("Place the downloaded file as: models/llama-3-8b-instruct.Q4_K_M.gguf")
    print("="*60)

def setup_audio():
    """Setup audio dependencies"""
    print("\n🎤 Setting up audio...")
    
    system = os.name
    if system == 'nt':  # Windows
        print("For Windows, you may need to install:")
        print("- Microsoft Visual C++ Redistributable")
        print("- Windows SDK (for PyAudio)")
    elif system == 'posix':  # Linux/macOS
        print("For Linux, you may need to install:")
        print("- sudo apt-get install portaudio19-dev python3-pyaudio")
        print("- sudo apt-get install espeak espeak-data libespeak1 libespeak-dev")

def main():
    """Main setup function"""
    print("🤖 CommandEcho Setup")
    print("="*30)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        print("Setup failed. Please install dependencies manually.")
        return
    
    # Setup audio
    setup_audio()
    
    # Model download instructions
    download_model_instructions()
    
    print("\n✅ Setup completed!")
    print("\nNext steps:")
    print("1. Download a LLaMA model (see instructions above)")
    print("2. Run: python main.py --text-mode (for testing)")
    print("3. Run: python main.py (for voice mode)")

if __name__ == "__main__":
    main()
