"""
System Control Tools for CommandEcho
Handles system-level operations like volume, brightness, battery info
"""

import logging
import platform
import subprocess
import psutil
from datetime import datetime
from typing import Optional

class SystemControl:
    """Handles system control operations"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.system = platform.system().lower()
        self.logger.info(f"System control initialized for {self.system}")
    
    def set_volume(self, volume: int) -> str:
        """Set system volume (0-100)"""
        volume = max(0, min(100, volume))  # Clamp between 0-100
        
        try:
            if self.system == "windows":
                # Use nircmd for Windows volume control
                subprocess.run([
                    "nircmd.exe", "setsysvolume", str(int(volume * 655.35))
                ], check=True, capture_output=True)
                return f"Volume set to {volume}%"
            
            elif self.system == "linux":
                # Use amixer for Linux
                subprocess.run([
                    "amixer", "set", "Master", f"{volume}%"
                ], check=True, capture_output=True)
                return f"Volume set to {volume}%"
            
            elif self.system == "darwin":  # macOS
                # Use osascript for macOS
                subprocess.run([
                    "osascript", "-e", f"set volume output volume {volume}"
                ], check=True, capture_output=True)
                return f"Volume set to {volume}%"
            
            else:
                return "Volume control not supported on this system"
                
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error setting volume: {e}")
            return f"Failed to set volume. Error: {e}"
        except FileNotFoundError:
            return "Volume control utility not found. Please install required tools."
    
    def adjust_volume(self, change: int) -> str:
        """Adjust volume by a relative amount"""
        try:
            current_volume = self.get_current_volume()
            if current_volume is not None:
                new_volume = current_volume + change
                return self.set_volume(new_volume)
            else:
                return "Could not determine current volume"
        except Exception as e:
            return f"Error adjusting volume: {e}"
    
    def get_current_volume(self) -> Optional[int]:
        """Get current system volume"""
        try:
            if self.system == "windows":
                # This is a simplified approach - in practice you'd need more complex Windows API calls
                return 50  # Placeholder
            
            elif self.system == "linux":
                result = subprocess.run([
                    "amixer", "get", "Master"
                ], capture_output=True, text=True, check=True)
                
                # Parse amixer output to get volume percentage
                import re
                match = re.search(r'\[(\d+)%\]', result.stdout)
                if match:
                    return int(match.group(1))
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting current volume: {e}")
            return None
    
    def set_brightness(self, brightness: int) -> str:
        """Set screen brightness (0-100)"""
        brightness = max(0, min(100, brightness))
        
        try:
            if self.system == "windows":
                # Use powershell for Windows brightness control
                ps_command = f"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{brightness})"
                subprocess.run([
                    "powershell", "-Command", ps_command
                ], check=True, capture_output=True)
                return f"Brightness set to {brightness}%"
            
            elif self.system == "linux":
                # Use xrandr for Linux (requires X11)
                brightness_decimal = brightness / 100.0
                subprocess.run([
                    "xrandr", "--output", "eDP-1", "--brightness", str(brightness_decimal)
                ], check=True, capture_output=True)
                return f"Brightness set to {brightness}%"
            
            else:
                return "Brightness control not implemented for this system"
                
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error setting brightness: {e}")
            return f"Failed to set brightness. Error: {e}"
        except FileNotFoundError:
            return "Brightness control utility not found"
    
    def get_battery_info(self) -> str:
        """Get battery information"""
        try:
            battery = psutil.sensors_battery()
            if battery is None:
                return "No battery found or battery information unavailable"
            
            percent = battery.percent
            plugged = battery.power_plugged
            
            status = "charging" if plugged else "discharging"
            
            if battery.secsleft != psutil.POWER_TIME_UNLIMITED:
                hours, remainder = divmod(battery.secsleft, 3600)
                minutes = remainder // 60
                time_left = f"{int(hours)}h {int(minutes)}m"
                return f"Battery: {percent}% ({status}) - {time_left} remaining"
            else:
                return f"Battery: {percent}% ({status})"
                
        except Exception as e:
            self.logger.error(f"Error getting battery info: {e}")
            return f"Error retrieving battery information: {e}"
    
    def get_current_time(self) -> str:
        """Get current time"""
        now = datetime.now()
        return f"The current time is {now.strftime('%I:%M %p on %A, %B %d, %Y')}"
    
    def get_system_info(self) -> str:
        """Get general system information"""
        try:
            # Get basic system info
            system_info = []
            system_info.append(f"System: {platform.system()} {platform.release()}")
            system_info.append(f"Processor: {platform.processor()}")
            
            # Memory info
            memory = psutil.virtual_memory()
            memory_gb = memory.total / (1024**3)
            memory_used_percent = memory.percent
            system_info.append(f"Memory: {memory_gb:.1f}GB total, {memory_used_percent}% used")
            
            # CPU info
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            system_info.append(f"CPU: {cpu_count} cores, {cpu_percent}% usage")
            
            return "\n".join(system_info)
            
        except Exception as e:
            self.logger.error(f"Error getting system info: {e}")
            return f"Error retrieving system information: {e}"
    
    def get_storage_info(self) -> str:
        """Get storage information"""
        try:
            storage_info = []
            
            # Get disk usage for all mounted drives
            partitions = psutil.disk_partitions()
            
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    total_gb = usage.total / (1024**3)
                    used_gb = usage.used / (1024**3)
                    free_gb = usage.free / (1024**3)
                    percent_used = (usage.used / usage.total) * 100
                    
                    storage_info.append(
                        f"Drive {partition.device}: {used_gb:.1f}GB used / {total_gb:.1f}GB total "
                        f"({percent_used:.1f}% used, {free_gb:.1f}GB free)"
                    )
                except PermissionError:
                    # Skip drives we can't access
                    continue
            
            return "\n".join(storage_info) if storage_info else "No storage information available"
            
        except Exception as e:
            self.logger.error(f"Error getting storage info: {e}")
            return f"Error retrieving storage information: {e}"
