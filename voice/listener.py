# voice/listener.py

import os
import queue
import sounddevice as sd
import vosk
import json

class VoiceListener:
    def __init__(self, model_path="models/vosk-model-small-en-us-0.15"):
        print("🎙️ Loading Vosk model...")
        if not os.path.exists(model_path):
            raise FileNotFoundError("Vosk model not found. Please check your path.")
        self.model = vosk.Model(model_path)
        self.q = queue.Queue()

    def listen(self):
        def callback(indata, frames, time, status):
            if status:
                print("⚠️ Status:", status)
            self.q.put(bytes(indata))

        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=callback):
            print("🎤 Listening (Vosk)... Say something!")
            rec = vosk.KaldiRecognizer(self.model, 16000)

            while True:
                data = self.q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    return result.get("text", "")
