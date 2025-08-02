import os
import platform

# Mapping of common folders to their absolute paths
FOLDER_MAP = {
    "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
    "documents": os.path.join(os.path.expanduser("~"), "Documents"),
    "desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
    "pictures": os.path.join(os.path.expanduser("~"), "Pictures"),
    # Add more folders if needed
}

# Mapping of applications to their paths
APP_PATHS = {
    "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "vscode": "C:\\Users\\%USERNAME%\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    # Add more apps here
}

def open_application(app_name: str) -> str:
    try:
        if platform.system() != "Windows":
            return "System control currently supports only Windows."

        app_name = app_name.lower().strip()
        path = APP_PATHS.get(app_name)

        if path:
            os.startfile(os.path.expandvars(path))
            return f"{app_name.capitalize()} is opening..."
        else:
            return f"Sorry, I don’t know how to open '{app_name}'."
    except Exception as e:
        return f"Failed to open '{app_name}': {str(e)}"

def open_folder(command: str) -> str:
    command = command.lower().strip()

    for folder_name, path in FOLDER_MAP.items():
        if folder_name in command:
            if os.path.exists(path):
                os.startfile(path)
                return f"{folder_name.capitalize()} folder is now open."
            else:
                return f"{folder_name.capitalize()} folder path does not exist."

    return f"Sorry, I don’t know how to open '{command}'."
