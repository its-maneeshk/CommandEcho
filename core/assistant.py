"""
Main CommandEcho Assistant Class
Orchestrates all components of the voice assistant
"""

import logging
import threading
import time
from typing import Optional

from core.config import Config
from core.voice_input import VoiceInput
from core.voice_output import VoiceOutput
from core.command_handler import CommandHandler
from brain.llm_brain import LLMBrain
from brain.memory_system import MemorySystem

class CommandEcho:
    """Main CommandEcho Assistant"""
    
    def __init__(self, config: Config, text_mode: bool = False):
        self.config = config
        self.text_mode = text_mode
        self.logger = logging.getLogger(__name__)
        self.running = False
        
        # Initialize components
        self.logger.info("Initializing CommandEcho components...")
        
        # Memory system (initialize first)
        self.memory = MemorySystem(config.memory)
        
        # LLM Brain
        self.brain = LLMBrain(config.llm, self.memory)
        
        # Voice components (only if not in text mode)
        if not text_mode:
            self.voice_input = VoiceInput(config.voice)
            self.voice_output = VoiceOutput(config.voice)
        else:
            self.voice_input = None
            self.voice_output = None
        
        # Command handler
        self.command_handler = CommandHandler(self.brain, self.memory)
        
        self.logger.info("CommandEcho initialized successfully!")
    
    def start(self):
        """Start the assistant"""
        self.running = True
        self.logger.info("CommandEcho is now active!")
        
        # Greet the user
        greeting = self._get_greeting()
        self._respond(greeting)
        
        if self.text_mode:
            self._text_mode_loop()
        else:
            self._voice_mode_loop()
    
    def stop(self):
        """Stop the assistant"""
        self.running = False
        self.logger.info("CommandEcho stopped")
    
    def _get_greeting(self) -> str:
        """Get personalized greeting"""
        user_name = self.memory.get_user_preference("name")
        if user_name:
            return f"Hello {user_name}, CommandEcho is ready. How can I assist you today?"
        else:
            return "Hello! I'm CommandEcho, your personal AI assistant. How can I help you today?"
    
    def _text_mode_loop(self):
        """Main loop for text mode"""
        print("\n" + "="*50)
        print("CommandEcho - Text Mode")
        print("Type 'quit' or 'exit' to stop")
        print("="*50 + "\n")
        
        while self.running:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    self._respond("Goodbye! Have a great day!")
                    break
                
                if user_input:
                    response = self._process_input(user_input)
                    print(f"\nCommandEcho: {response}")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.logger.error(f"Error in text mode loop: {e}")
    
    def _voice_mode_loop(self):
        """Main loop for voice mode"""
        if not self.voice_input or not self.voice_output:
            self.logger.error("Voice components not initialized")
            return
        
        self.logger.info("Listening for wake word or voice commands...")
        
        while self.running:
            try:
                # Listen for input
                user_input = self.voice_input.listen()
                
                if user_input:
                    self.logger.info(f"User said: {user_input}")
                    
                    # Check for exit commands
                    if any(phrase in user_input.lower() for phrase in ['goodbye', 'bye bye', 'stop listening']):
                        self._respond("Goodbye! Have a great day!")
                        break
                    
                    # Process the input
                    response = self._process_input(user_input)
                    self._respond(response)
                
                time.sleep(0.1)  # Small delay to prevent excessive CPU usage
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.logger.error(f"Error in voice mode loop: {e}")
                time.sleep(1)  # Wait before retrying
    
    def _process_input(self, user_input: str) -> str:
        """Process user input and generate response"""
        try:
            # Store the user input in short-term memory
            self.memory.add_to_conversation("user", user_input)
            
            # Check if this is a system command
            if self.command_handler.is_system_command(user_input):
                response = self.command_handler.handle_command(user_input)
            else:
                # Generate AI response
                response = self.brain.generate_response(user_input)
            
            # Store the response in memory
            self.memory.add_to_conversation("assistant", response)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error processing input: {e}")
            return "I'm sorry, I encountered an error processing your request. Please try again."
    
    def _respond(self, text: str):
        """Send response to user"""
        if self.text_mode:
            # In text mode, response is printed in the main loop
            pass
        else:
            if self.voice_output:
                self.voice_output.speak(text)
            else:
                print(f"CommandEcho: {text}")
