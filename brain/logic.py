# brain/logic.py

import datetime
import os
from system.control import open_application
from brain.ai_response import get_ai_response
from brain.memory import remember, recall
from system.monitor import system_status
from system.control import open_application, open_folder

def process_command(text):
    command = text.lower()
    command = command.replace("’", "'")  # Normalize smart quotes

    if "open" in command:
        if "folder" in command or "directory" in command:
            return open_folder(command)
        else:
            app_name = command.replace("open", "").strip()
            return open_application(app_name)

    elif "time" in command:
        now = datetime.datetime.now().strftime("%H:%M")
        return f"The current time is {now}."

    elif "date" in command:
        today = datetime.date.today().strftime("%B %d, %Y")
        return f"Today's date is {today}."

    elif "hello" in command:
        return "Hello Manish, how can I assist you today?"

    elif "joke" in command:
        return "Why don't programmers like nature? Too many bugs."

    elif "exit" in command or "quit" in command:
        return "exit"

    elif "remember that" in command:
        try:
            _, memory = command.split("remember that", 1)
            key = memory.strip().split(" is ")[0].strip()
            value = memory.strip().split(" is ")[1].strip()
            remember(key, value)
            return f"I will remember that {key} is {value}."
        except:
            return "I didn't catch what to remember."

    elif "do you remember" in command:
        try:
            key = command.split("do you remember", 1)[1].strip()
            value = recall(key)
            return f"Yes, {key} is {value}." if value else "I don't remember that yet."
        except:
            return "I couldn't understand what you asked me to recall."

    elif "system status" in command or "how is my pc" in command:
        return system_status()

    elif "diagnose system" in command or "full system report" in command:
        return system_status(verbose=True)

    else:
        return get_ai_response(command)  # Fallback to smart AI    
