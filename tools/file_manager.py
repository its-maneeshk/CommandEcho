"""
File Manager Tools for CommandEcho
Handles file operations and searches
"""

import logging
import os
import glob
from pathlib import Path
from typing import List, Optional

class FileManager:
    """Handles file operations and searches"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Common search locations
        self.search_paths = [
            Path.home() / "Desktop",
            Path.home() / "Documents", 
            Path.home() / "Downloads",
            Path.home() / "Pictures",
            Path.home() / "Videos",
            Path.home() / "Music"
        ]
        
        self.logger.info("File manager initialized")
    
    def search_files(self, search_term: str, max_results: int = 10) -> str:
        """Search for files containing the search term"""
        try:
            found_files = []
            search_term_lower = search_term.lower()
            
            # Search in common directories
            for search_path in self.search_paths:
                if not search_path.exists():
                    continue
                
                try:
                    # Search for files with matching names
                    for file_path in search_path.rglob("*"):
                        if len(found_files) >= max_results:
                            break
                        
                        if file_path.is_file() and search_term_lower in file_path.name.lower():
                            found_files.append(str(file_path))
                
                except PermissionError:
                    # Skip directories we can't access
                    continue
                except Exception as e:
                    self.logger.error(f"Error searching in {search_path}: {e}")
                    continue
            
            if found_files:
                result = f"Found {len(found_files)} files matching '{search_term}':\n"
                for i, file_path in enumerate(found_files[:max_results], 1):
                    result += f"{i}. {file_path}\n"
                return result.strip()
            else:
                return f"No files found matching '{search_term}'"
                
        except Exception as e:
            self.logger.error(f"Error searching files: {e}")
            return f"Error searching for files: {e}"
    
    def get_file_info(self, file_path: str) -> str:
        """Get information about a specific file"""
        try:
            path = Path(file_path)
            
            if not path.exists():
                return f"File not found: {file_path}"
            
            if path.is_file():
                stat = path.stat()
                size_mb = stat.st_size / (1024 * 1024)
                modified_time = stat.st_mtime
                
                from datetime import datetime
                modified_date = datetime.fromtimestamp(modified_time).strftime("%Y-%m-%d %H:%M:%S")
                
                return (f"File: {path.name}\n"
                       f"Location: {path.parent}\n"
                       f"Size: {size_mb:.2f} MB\n"
                       f"Modified: {modified_date}")
            
            elif path.is_dir():
                # Count files in directory
                try:
                    file_count = len([f for f in path.iterdir() if f.is_file()])
                    dir_count = len([f for f in path.iterdir() if f.is_dir()])
                    
                    return (f"Directory: {path.name}\n"
                           f"Location: {path.parent}\n"
                           f"Contains: {file_count} files, {dir_count} directories")
                except PermissionError:
                    return f"Directory: {path.name}\nLocation: {path.parent}\nAccess denied"
            
        except Exception as e:
            self.logger.error(f"Error getting file info: {e}")
            return f"Error getting file information: {e}"
    
    def list_directory(self, directory_path: str = None) -> str:
        """List contents of a directory"""
        try:
            if directory_path is None:
                directory_path = str(Path.home())
            
            path = Path(directory_path)
            
            if not path.exists():
                return f"Directory not found: {directory_path}"
            
            if not path.is_dir():
                return f"Not a directory: {directory_path}"
            
            try:
                items = list(path.iterdir())
                
                if not items:
                    return f"Directory is empty: {directory_path}"
                
                # Separate files and directories
                directories = [item for item in items if item.is_dir()]
                files = [item for item in items if item.is_file()]
                
                result = f"Contents of {directory_path}:\n\n"
                
                if directories:
                    result += "Directories:\n"
                    for directory in sorted(directories)[:10]:  # Limit to 10
                        result += f"  📁 {directory.name}\n"
                    
                    if len(directories) > 10:
                        result += f"  ... and {len(directories) - 10} more directories\n"
                    result += "\n"
                
                if files:
                    result += "Files:\n"
                    for file in sorted(files)[:10]:  # Limit to 10
                        size_kb = file.stat().st_size / 1024
                        result += f"  📄 {file.name} ({size_kb:.1f} KB)\n"
                    
                    if len(files) > 10:
                        result += f"  ... and {len(files) - 10} more files\n"
                
                return result.strip()
                
            except PermissionError:
                return f"Access denied to directory: {directory_path}"
            
        except Exception as e:
            self.logger.error(f"Error listing directory: {e}")
            return f"Error listing directory: {e}"
    
    def create_directory(self, directory_path: str) -> str:
        """Create a new directory"""
        try:
            path = Path(directory_path)
            path.mkdir(parents=True, exist_ok=True)
            return f"Directory created: {directory_path}"
            
        except Exception as e:
            self.logger.error(f"Error creating directory: {e}")
            return f"Error creating directory: {e}"
    
    def delete_file(self, file_path: str) -> str:
        """Delete a file (with confirmation)"""
        try:
            path = Path(file_path)
            
            if not path.exists():
                return f"File not found: {file_path}"
            
            # For safety, we'll just return a message instead of actually deleting
            # In a real implementation, you might want to add confirmation
            return (f"File deletion requested: {file_path}\n"
                   "For safety, file deletion is not implemented in this demo. "
                   "You can manually delete the file if needed.")
            
        except Exception as e:
            self.logger.error(f"Error deleting file: {e}")
            return f"Error deleting file: {e}"
