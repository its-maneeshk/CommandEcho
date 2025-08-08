"""
Voice Input Handler for CommandEcho
Handles speech recognition and wake word detection
"""

import logging
import speech_recognition as sr
import threading
import time
from typing import Optional

class VoiceInput:
    """Handles voice input and speech recognition"""
    
    def __init__(self, voice_config):
        self.config = voice_config
        self.logger = logging.getLogger(__name__)
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        self.logger.info("Adjusting for ambient noise...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        
        self.logger.info("Voice input initialized")
    
    def listen(self) -> Optional[str]:
        """Listen for voice input"""
        try:
            with self.microphone as source:
                # Listen for audio
                self.logger.debug("Listening...")
                
                if self.config.always_listening:
                    # Always listening mode
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                else:
                    # Wake word mode - listen for wake word first
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                    
                    # Quick recognition for wake word
                    try:
                        text = self.recognizer.recognize_google(audio, language='en-US')
                        if self.config.wake_word.lower() not in text.lower():
                            return None  # Wake word not detected
                        
                        # Wake word detected, listen for actual command
                        self.logger.info("Wake word detected, listening for command...")
                        audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                        
                    except sr.UnknownValueError:
                        return None  # Couldn't understand wake word
            
            # Recognize the speech
            text = self.recognizer.recognize_google(audio, language='en-US')
            return text.strip()
            
        except sr.WaitTimeoutError:
            # Timeout - normal in listening mode
            return None
        except sr.UnknownValueError:
            self.logger.debug("Could not understand audio")
            return None
        except sr.RequestError as e:
            self.logger.error(f"Error with speech recognition service: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error in voice input: {e}")
            return None
    
    def listen_once(self, timeout: int = 5) -> Optional[str]:
        """Listen for a single command with timeout"""
        try:
            with self.microphone as source:
                self.logger.info("Listening for command...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            
            text = self.recognizer.recognize_google(audio, language='en-US')
            return text.strip()
            
        except sr.WaitTimeoutError:
            self.logger.info("Listening timeout")
            return None
        except sr.UnknownValueError:
            self.logger.info("Could not understand audio")
            return None
        except Exception as e:
            self.logger.error(f"Error in listen_once: {e}")
            return None
