"""
Helper functions for CommandEcho
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any

def setup_logging(log_level: str = "INFO", log_file: str = "commandecho.log"):
    """Setup logging configuration"""
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Create logs directory if it doesn't exist
    Path("logs").mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f"logs/{log_file}"),
            logging.StreamHandler(sys.stdout)
        ]
    )

def check_dependencies() -> Dict[str, bool]:
    """Check if all required dependencies are available"""
    dependencies = {
        'speech_recognition': False,
        'pyttsx3': False,
        'psutil': False,
        'llama_cpp': False,
        'sentence_transformers': False,
        'faiss': False,
        'numpy': False
    }
    
    for dep in dependencies:
        try:
            if dep == 'llama_cpp':
                import llama_cpp
            elif dep == 'sentence_transformers':
                import sentence_transformers
            elif dep == 'faiss':
                import faiss
            else:
                __import__(dep)
            dependencies[dep] = True
        except ImportError:
            dependencies[dep] = False
    
    return dependencies

def get_system_info() -> Dict[str, Any]:
    """Get basic system information"""
    import platform
    import psutil
    
    return {
        'platform': platform.system(),
        'platform_version': platform.version(),
        'architecture': platform.architecture()[0],
        'processor': platform.processor(),
        'python_version': platform.python_version(),
        'cpu_count': psutil.cpu_count(),
        'memory_total': psutil.virtual_memory().total,
        'disk_usage': psutil.disk_usage('/').total if os.name != 'nt' else psutil.disk_usage('C:').total
    }

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def validate_model_file(model_path: str) -> bool:
    """Validate if model file exists and is accessible"""
    path = Path(model_path)
    
    if not path.exists():
        return False
    
    if not path.is_file():
        return False
    
    # Check if it's a GGUF file
    if not path.suffix.lower() in ['.gguf', '.bin']:
        return False
    
    # Check if file is readable
    try:
        with open(path, 'rb') as f:
            # Read first few bytes to check if it's a valid file
            header = f.read(4)
            return len(header) == 4
    except (IOError, OSError):
        return False

def clean_text_for_speech(text: str) -> str:
    """Clean text for better speech synthesis"""
    import re
    
    # Remove markdown formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)      # Italic
    text = re.sub(r'`(.*?)`', r'\1', text)        # Code
    
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\$$\$$,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', 'link', text)
    
    # Clean up extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def get_available_voices():
    """Get list of available TTS voices"""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        voice_list = []
        for i, voice in enumerate(voices):
            voice_list.append({
                'id': i,
                'name': voice.name,
                'language': getattr(voice, 'languages', ['unknown'])[0] if hasattr(voice, 'languages') else 'unknown'
            })
        
        engine.stop()
        return voice_list
    except Exception:
        return []
