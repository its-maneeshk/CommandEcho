# main.py

from voice.listener import VoiceListener
from voice.speaker import VoiceSpeaker
from brain.memory import init_memory
from brain.logic import process_command

def main():
    init_memory()  # ← Initializes memory on startup
    listener = VoiceListener()
    speaker = VoiceSpeaker()

    while True:
        print("🕒 Waiting for your voice input...")
        command = listener.listen()

        if command:
            print(f"🗣️ You said: {command}")
            response = process_command(command)
            
            if response == "exit":
                speaker.speak("Goodbye Manish.")
                break

            speaker.speak(response)

if __name__ == "__main__":
    main()
