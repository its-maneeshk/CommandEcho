"""
Command Handler for CommandEcho
Handles system commands and integrates with tools
"""

import logging
import re
from typing import Optional, Dict, Any

from tools.system_control import SystemControl
from tools.file_manager import FileManager
from tools.app_launcher import AppLauncher

class CommandHandler:
    """Handles system commands and tool integration"""
    
    def __init__(self, brain, memory):
        self.brain = brain
        self.memory = memory
        self.logger = logging.getLogger(__name__)
        
        # Initialize tools
        self.system_control = SystemControl()
        self.file_manager = FileManager()
        self.app_launcher = AppLauncher()
        
        # Command patterns
        self.command_patterns = {
            'volume': [r'set volume to (\d+)', r'volume (\d+)', r'turn volume (up|down)'],
            'brightness': [r'set brightness to (\d+)', r'brightness (\d+)'],
            'open_app': [r'open (.+)', r'launch (.+)', r'start (.+)'],
            'close_app': [r'close (.+)', r'quit (.+)', r'exit (.+)'],
            'system_info': [r'battery', r'what time', r'current time', r'system info', r'storage'],
            'file_search': [r'find file (.+)', r'search for (.+)', r'locate (.+)'],
            'memory_command': [r'remember (.+)', r'my name is (.+)', r'save (.+)']
        }
    
    def is_system_command(self, text: str) -> bool:
        """Check if the input is a system command"""
        text_lower = text.lower()
        
        # Check against all command patterns
        for command_type, patterns in self.command_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return True
        
        return False
    
    def handle_command(self, text: str) -> str:
        """Handle system command and return response"""
        text_lower = text.lower()
        
        try:
            # Volume control
            for pattern in self.command_patterns['volume']:
                match = re.search(pattern, text_lower)
                if match:
                    return self._handle_volume_command(match, text_lower)
            
            # Brightness control
            for pattern in self.command_patterns['brightness']:
                match = re.search(pattern, text_lower)
                if match:
                    return self._handle_brightness_command(match)
            
            # App launching
            for pattern in self.command_patterns['open_app']:
                match = re.search(pattern, text_lower)
                if match:
                    return self._handle_open_app_command(match)
            
            # App closing
            for pattern in self.command_patterns['close_app']:
                match = re.search(pattern, text_lower)
                if match:
                    return self._handle_close_app_command(match)
            
            # System info
            for pattern in self.command_patterns['system_info']:
                if re.search(pattern, text_lower):
                    return self._handle_system_info_command(text_lower)
            
            # File search
            for pattern in self.command_patterns['file_search']:
                match = re.search(pattern, text_lower)
                if match:
                    return self._handle_file_search_command(match)
            
            # Memory commands
            for pattern in self.command_patterns['memory_command']:
                match = re.search(pattern, text_lower)
                if match:
                    return self._handle_memory_command(match, text)
            
            # If no specific command matched, let the AI handle it
            return self.brain.generate_response(text)
            
        except Exception as e:
            self.logger.error(f"Error handling command: {e}")
            return f"I encountered an error while executing that command: {str(e)}"
    
    def _handle_volume_command(self, match, text_lower: str) -> str:
        """Handle volume control commands"""
        if 'up' in text_lower:
            result = self.system_control.adjust_volume(10)
        elif 'down' in text_lower:
            result = self.system_control.adjust_volume(-10)
        else:
            volume = int(match.group(1))
            result = self.system_control.set_volume(volume)
        
        return result
    
    def _handle_brightness_command(self, match) -> str:
        """Handle brightness control commands"""
        brightness = int(match.group(1))
        return self.system_control.set_brightness(brightness)
    
    def _handle_open_app_command(self, match) -> str:
        """Handle app opening commands"""
        app_name = match.group(1).strip()
        return self.app_launcher.launch_app(app_name)
    
    def _handle_close_app_command(self, match) -> str:
        """Handle app closing commands"""
        app_name = match.group(1).strip()
        return self.app_launcher.close_app(app_name)
    
    def _handle_system_info_command(self, text_lower: str) -> str:
        """Handle system information commands"""
        if 'battery' in text_lower:
            return self.system_control.get_battery_info()
        elif 'time' in text_lower:
            return self.system_control.get_current_time()
        elif 'storage' in text_lower:
            return self.system_control.get_storage_info()
        else:
            return self.system_control.get_system_info()
    
    def _handle_file_search_command(self, match) -> str:
        """Handle file search commands"""
        search_term = match.group(1).strip()
        return self.file_manager.search_files(search_term)
    
    def _handle_memory_command(self, match, original_text: str) -> str:
        """Handle memory-related commands"""
        content = match.group(1).strip()
        
        # Check if it's a name introduction
        if 'my name is' in original_text.lower():
            name = content
            self.memory.store_user_preference('name', name)
            return f"Nice to meet you, {name}! I'll remember your name."
        else:
            # General memory storage
            self.memory.store_memory(content, 'user_preference')
            return f"I've remembered that: {content}"
