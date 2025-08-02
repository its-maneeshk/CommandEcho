# voice/speaker.py

import os
import uuid
import pygame
from TTS.api import TTS

class VoiceSpeaker:
    def __init__(self):
        print("🗣️ Loading Coqui TTS...")
        self.tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)
        pygame.mixer.init()

    def speak(self, text):
        file_path = f"temp_{uuid.uuid4()}.wav"
        self.tts.tts_to_file(text=text, file_path=file_path)
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        pygame.mixer.music.unload()
        os.remove(file_path)
