"""
Configuration management for CommandEcho
"""

import json
import os
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, Any

@dataclass
class VoiceConfig:
    """Voice-related configuration"""
    wake_word: str = "echo"
    always_listening: bool = False
    speech_rate: int = 200
    speech_volume: float = 0.9
    voice_id: int = 0  # 0 for default, 1 for female voice typically
    
@dataclass
class LLMConfig:
    """LLM-related configuration"""
    model_path: str = "models/llama-3-8b-instruct.Q4_K_M.gguf"
    context_length: int = 4096
    max_tokens: int = 512
    temperature: float = 0.7
    top_p: float = 0.9
    
@dataclass
class MemoryConfig:
    """Memory system configuration"""
    memory_db_path: str = "data/memory/memory.db"
    vector_db_path: str = "data/memory/vectors"
    max_short_term_memory: int = 10
    embedding_model: str = "all-MiniLM-L6-v2"

class Config:
    """Main configuration class"""
    
    def __init__(self, config_file: str = "config/config.json"):
        self.config_file = Path(config_file)
        self.voice = VoiceConfig()
        self.llm = LLMConfig()
        self.memory = MemoryConfig()
        
        # Create directories
        self._create_directories()
        
        # Load existing config or create default
        self.load()
    
    def _create_directories(self):
        """Create necessary directories"""
        directories = [
            "config",
            "models", 
            "data/memory",
            "logs"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    def load(self):
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                
                # Update configurations
                if 'voice' in data:
                    self.voice = VoiceConfig(**data['voice'])
                if 'llm' in data:
                    self.llm = LLMConfig(**data['llm'])
                if 'memory' in data:
                    self.memory = MemoryConfig(**data['memory'])
                    
            except Exception as e:
                print(f"Error loading config: {e}. Using defaults.")
        else:
            # Save default config
            self.save()
    
    def save(self):
        """Save configuration to file"""
        config_data = {
            'voice': asdict(self.voice),
            'llm': asdict(self.llm),
            'memory': asdict(self.memory)
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config_data, f, indent=2)
    
    def get(self, section: str, key: str, default=None):
        """Get configuration value"""
        section_obj = getattr(self, section, None)
        if section_obj:
            return getattr(section_obj, key, default)
        return default
