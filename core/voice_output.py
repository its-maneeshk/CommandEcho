"""
Voice Output Handler for CommandEcho
Handles text-to-speech functionality
"""

import logging
import pyttsx3
import threading
from queue import Queue

class VoiceOutput:
    """Handles text-to-speech output"""
    
    def __init__(self, voice_config):
        self.config = voice_config
        self.logger = logging.getLogger(__name__)
        
        # Initialize TTS engine
        try:
            self.engine = pyttsx3.init()
            self._configure_voice()
            self.logger.info("Voice output initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize TTS engine: {e}")
            self.engine = None
        
        # Speech queue for handling multiple requests
        self.speech_queue = Queue()
        self.speech_thread = threading.Thread(target=self._speech_worker, daemon=True)
        self.speech_thread.start()
    
    def _configure_voice(self):
        """Configure voice properties"""
        if not self.engine:
            return
        
        try:
            # Set speech rate
            self.engine.setProperty('rate', self.config.speech_rate)
            
            # Set volume
            self.engine.setProperty('volume', self.config.speech_volume)
            
            # Set voice (if available)
            voices = self.engine.getProperty('voices')
            if voices and len(voices) > self.config.voice_id:
                self.engine.setProperty('voice', voices[self.config.voice_id].id)
                self.logger.info(f"Voice set to: {voices[self.config.voice_id].name}")
            
        except Exception as e:
            self.logger.error(f"Error configuring voice: {e}")
    
    def speak(self, text: str, priority: bool = False):
        """Add text to speech queue"""
        if not text.strip():
            return
        
        if priority:
            # Clear queue and speak immediately
            while not self.speech_queue.empty():
                try:
                    self.speech_queue.get_nowait()
                except:
                    break
        
        self.speech_queue.put(text)
    
    def _speech_worker(self):
        """Worker thread for handling speech queue"""
        while True:
            try:
                text = self.speech_queue.get()
                if text is None:  # Shutdown signal
                    break
                
                self._speak_now(text)
                self.speech_queue.task_done()
                
            except Exception as e:
                self.logger.error(f"Error in speech worker: {e}")
    
    def _speak_now(self, text: str):
        """Immediately speak the given text"""
        if not self.engine:
            # Fallback to print if TTS not available
            print(f"CommandEcho: {text}")
            return
        
        try:
            self.logger.debug(f"Speaking: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            self.logger.error(f"Error speaking text: {e}")
            print(f"CommandEcho: {text}")  # Fallback
    
    def stop_speaking(self):
        """Stop current speech"""
        if self.engine:
            try:
                self.engine.stop()
            except Exception as e:
                self.logger.error(f"Error stopping speech: {e}")
    
    def shutdown(self):
        """Shutdown the voice output system"""
        self.speech_queue.put(None)  # Signal shutdown
        if self.speech_thread.is_alive():
            self.speech_thread.join(timeout=2)
