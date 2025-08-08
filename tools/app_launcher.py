"""
App Launcher Tools for CommandEcho
Handles launching and closing applications
"""

import logging
import subprocess
import platform
import psutil
import os
from typing import Dict, List, Optional

class AppLauncher:
    """Handles application launching and management"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.system = platform.system().lower()
        
        # Common application mappings
        self.app_mappings = {
            # Text editors
            'notepad': {'windows': 'notepad.exe', 'linux': 'gedit', 'darwin': 'TextEdit'},
            'code': {'windows': 'code', 'linux': 'code', 'darwin': 'code'},
            'vscode': {'windows': 'code', 'linux': 'code', 'darwin': 'code'},
            'vs code': {'windows': 'code', 'linux': 'code', 'darwin': 'code'},
            'visual studio code': {'windows': 'code', 'linux': 'code', 'darwin': 'code'},
            
            # Browsers
            'chrome': {'windows': 'chrome', 'linux': 'google-chrome', 'darwin': 'Google Chrome'},
            'google chrome': {'windows': 'chrome', 'linux': 'google-chrome', 'darwin': 'Google Chrome'},
            'firefox': {'windows': 'firefox', 'linux': 'firefox', 'darwin': 'Firefox'},
            'edge': {'windows': 'msedge', 'linux': 'microsoft-edge', 'darwin': 'Microsoft Edge'},
            'safari': {'darwin': 'Safari'},
            
            # System apps
            'calculator': {'windows': 'calc', 'linux': 'gnome-calculator', 'darwin': 'Calculator'},
            'file explorer': {'windows': 'explorer'},
            'explorer': {'windows': 'explorer'},
            'finder': {'darwin': 'Finder'},
            'terminal': {'windows': 'cmd', 'linux': 'gnome-terminal', 'darwin': 'Terminal'},
            'command prompt': {'windows': 'cmd'},
            'cmd': {'windows': 'cmd'},
            
            # Media
            'vlc': {'windows': 'vlc', 'linux': 'vlc', 'darwin': 'VLC'},
            'spotify': {'windows': 'spotify', 'linux': 'spotify', 'darwin': 'Spotify'},
            
            # Office
            'word': {'windows': 'winword', 'darwin': 'Microsoft Word'},
            'excel': {'windows': 'excel', 'darwin': 'Microsoft Excel'},
            'powerpoint': {'windows': 'powerpnt', 'darwin': 'Microsoft PowerPoint'},
        }
        
        self.logger.info(f"App launcher initialized for {self.system}")
    
    def launch_app(self, app_name: str) -> str:
        """Launch an application by name"""
        app_name_lower = app_name.lower().strip()
        
        try:
            # Check if it's a mapped application
            if app_name_lower in self.app_mappings:
                app_info = self.app_mappings[app_name_lower]
                
                if self.system in app_info:
                    executable = app_info[self.system]
                    return self._launch_executable(executable, app_name)
                else:
                    return f"'{app_name}' is not available on {self.system}"
            
            # Try to launch directly by name
            else:
                return self._launch_executable(app_name_lower, app_name)
                
        except Exception as e:
            self.logger.error(f"Error launching app {app_name}: {e}")
            return f"Failed to launch {app_name}: {e}"
    
    def _launch_executable(self, executable: str, display_name: str) -> str:
        """Launch an executable"""
        try:
            if self.system == "windows":
                # Try different methods for Windows
                try:
                    # First try with shell=True for built-in commands
                    subprocess.Popen(executable, shell=True)
                    return f"Launched {display_name}"
                except:
                    # Try without shell for regular executables
                    subprocess.Popen([executable])
                    return f"Launched {display_name}"
            
            elif self.system == "linux":
                # Use subprocess for Linux
                subprocess.Popen([executable], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return f"Launched {display_name}"
            
            elif self.system == "darwin":  # macOS
                # Use 'open' command for macOS
                subprocess.Popen(['open', '-a', executable], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return f"Launched {display_name}"
            
            else:
                return f"App launching not supported on {self.system}"
                
        except FileNotFoundError:
            return f"Application '{display_name}' not found. Please check if it's installed."
        except Exception as e:
            self.logger.error(f"Error launching {executable}: {e}")
            return f"Failed to launch {display_name}: {e}"
    
    def close_app(self, app_name: str) -> str:
        """Close an application by name"""
        app_name_lower = app_name.lower().strip()
        
        try:
            # Find running processes that match the app name
            matching_processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    proc_name = proc.info['name'].lower() if proc.info['name'] else ""
                    proc_exe = proc.info['exe'].lower() if proc.info['exe'] else ""
                    
                    # Check if the app name matches the process name or executable
                    if (app_name_lower in proc_name or 
                        app_name_lower in proc_exe or
                        any(app_name_lower in alias for alias in self._get_app_aliases(app_name_lower))):
                        matching_processes.append(proc)
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            if not matching_processes:
                return f"No running processes found for '{app_name}'"
            
            # Terminate the processes
            terminated_count = 0
            for proc in matching_processes:
                try:
                    proc.terminate()
                    terminated_count += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if terminated_count > 0:
                return f"Closed {terminated_count} instance(s) of {app_name}"
            else:
                return f"Could not close {app_name} - access denied or process not found"
                
        except Exception as e:
            self.logger.error(f"Error closing app {app_name}: {e}")
            return f"Failed to close {app_name}: {e}"
    
    def _get_app_aliases(self, app_name: str) -> List[str]:
        """Get possible aliases for an app name"""
        aliases = []
        
        # Check our mappings
        if app_name in self.app_mappings:
            app_info = self.app_mappings[app_name]
            if self.system in app_info:
                aliases.append(app_info[self.system].lower())
        
        # Add common variations
        if 'chrome' in app_name:
            aliases.extend(['chrome.exe', 'google-chrome', 'googlechrome'])
        elif 'firefox' in app_name:
            aliases.extend(['firefox.exe', 'firefox'])
        elif 'code' in app_name:
            aliases.extend(['code.exe', 'vscode'])
        elif 'notepad' in app_name:
            aliases.extend(['notepad.exe'])
        
        return aliases
    
    def list_running_apps(self) -> str:
        """List currently running applications"""
        try:
            running_apps = set()
            
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name']:
                        # Filter out system processes and focus on user applications
                        proc_name = proc.info['name']
                        if not proc_name.startswith(('System', 'svchost', 'dwm', 'winlogon')):
                            running_apps.add(proc_name)
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            if running_apps:
                sorted_apps = sorted(running_apps)
                result = "Currently running applications:\n"
                for i, app in enumerate(sorted_apps[:15], 1):  # Limit to 15 apps
                    result += f"{i}. {app}\n"
                
                if len(sorted_apps) > 15:
                    result += f"... and {len(sorted_apps) - 15} more applications"
                
                return result.strip()
            else:
                return "No user applications currently running"
                
        except Exception as e:
            self.logger.error(f"Error listing running apps: {e}")
            return f"Error listing running applications: {e}"
