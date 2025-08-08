"""
Test script to verify CommandEcho installation
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.helpers import check_dependencies, get_system_info, validate_model_file

def test_dependencies():
    """Test if all dependencies are installed"""
    print("🔍 Checking Dependencies...")
    print("-" * 40)
    
    deps = check_dependencies()
    all_good = True
    
    for dep, available in deps.items():
        status = "✅" if available else "❌"
        print(f"{status} {dep}")
        if not available:
            all_good = False
    
    print("-" * 40)
    if all_good:
        print("✅ All dependencies are installed!")
    else:
        print("❌ Some dependencies are missing. Run: pip install -r requirements.txt")
    
    return all_good

def test_directories():
    """Test if all required directories exist"""
    print("\n📁 Checking Directories...")
    print("-" * 40)
    
    required_dirs = [
        "models",
        "data/memory",
        "config",
        "logs",
        "core",
        "brain", 
        "tools",
        "utils"
    ]
    
    all_good = True
    for directory in required_dirs:
        path = Path(directory)
        if path.exists():
            print(f"✅ {directory}")
        else:
            print(f"❌ {directory} (missing)")
            all_good = False
    
    print("-" * 40)
    if all_good:
        print("✅ All directories exist!")
    else:
        print("❌ Some directories are missing. Run setup.py")
    
    return all_good

def test_model():
    """Test if model file exists"""
    print("\n🤖 Checking AI Model...")
    print("-" * 40)
    
    model_path = "models/llama-3-8b-instruct.Q4_K_M.gguf"
    
    if validate_model_file(model_path):
        print(f"✅ Model found: {model_path}")
        return True
    else:
        print(f"❌ Model not found: {model_path}")
        print("Please download a LLaMA model in GGUF format")
        return False

def test_voice_system():
    """Test voice input/output system"""
    print("\n🎤 Testing Voice System...")
    print("-" * 40)
    
    # Test TTS
    try:
        import pyttsx3
        engine = pyttsx3.init()
        print("✅ Text-to-Speech engine initialized")
        engine.stop()
    except Exception as e:
        print(f"❌ Text-to-Speech failed: {e}")
        return False
    
    # Test Speech Recognition
    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        print("✅ Speech Recognition initialized")
    except Exception as e:
        print(f"❌ Speech Recognition failed: {e}")
        return False
    
    # Test Microphone
    try:
        import speech_recognition as sr
        mic = sr.Microphone()
        print("✅ Microphone access available")
    except Exception as e:
        print(f"❌ Microphone access failed: {e}")
        return False
    
    return True

def test_system_info():
    """Display system information"""
    print("\n💻 System Information...")
    print("-" * 40)
    
    info = get_system_info()
    
    print(f"Platform: {info['platform']} {info['platform_version']}")
    print(f"Architecture: {info['architecture']}")
    print(f"Python: {info['python_version']}")
    print(f"CPU Cores: {info['cpu_count']}")
    print(f"Memory: {info['memory_total'] / (1024**3):.1f} GB")
    print(f"Disk Space: {info['disk_usage'] / (1024**3):.1f} GB")

def main():
    """Run all tests"""
    print("🤖 CommandEcho Installation Test")
    print("=" * 50)
    
    # Run tests
    deps_ok = test_dependencies()
    dirs_ok = test_directories()
    model_ok = test_model()
    voice_ok = test_voice_system()
    
    # System info
    test_system_info()
    
    # Final result
    print("\n" + "=" * 50)
    if deps_ok and dirs_ok and voice_ok:
        if model_ok:
            print("🎉 CommandEcho is ready to use!")
            print("Run: python main.py --text-mode")
        else:
            print("⚠️  CommandEcho is almost ready!")
            print("Please download a LLaMA model to complete setup")
    else:
        print("❌ CommandEcho setup incomplete")
        print("Please fix the issues above and try again")

if __name__ == "__main__":
    main()
