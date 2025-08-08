"""
LLM Brain for CommandEcho
Handles AI response generation using local LLaMA model
"""

import logging
import os
from typing import List, Dict, Optional
from pathlib import Path

# Check if llama-cpp-python is available
try:
    from llama_cpp import Llama
    LLAMA_AVAILABLE = True
except ImportError:
    LLAMA_AVAILABLE = False
    print("⚠️  llama-cpp-python not installed. Install with: pip install llama-cpp-python")

class LLMBrain:
    """AI Brain using local LLaMA model"""
    
    def __init__(self, llm_config, memory_system):
        self.config = llm_config
        self.memory = memory_system
        self.logger = logging.getLogger(__name__)
        self.llm = None
        
        if LLAMA_AVAILABLE:
            self._initialize_llm()
        else:
            self.logger.warning("LLaMA not available, using fallback responses")
    
    def _initialize_llm(self):
        """Initialize the LLaMA model"""
        model_path = Path(self.config.model_path)
        
        if not model_path.exists():
            self.logger.error(f"Model file not found: {model_path}")
            print(f"Please place your LLaMA model here: {model_path}")
            return
        
        try:
            self.logger.info("Loading LLaMA model... This may take a moment.")
            self.llm = Llama(
                model_path=str(model_path),
                n_ctx=self.config.context_length,
                verbose=False,
                n_threads=os.cpu_count() // 2  # Use half of available CPU cores
            )
            self.logger.info("LLaMA model loaded successfully!")
            
        except Exception as e:
            self.logger.error(f"Failed to load LLaMA model: {e}")
            self.llm = None
    
    def generate_response(self, user_input: str) -> str:
        """Generate AI response to user input"""
        if not self.llm:
            return self._fallback_response(user_input)
        
        try:
            # Get conversation context
            context = self._build_context(user_input)
            
            # Generate response
            response = self.llm(
                context,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                top_p=self.config.top_p,
                stop=["User:", "Human:", "\n\n"],
                echo=False
            )
            
            # Extract the response text
            response_text = response['choices'][0]['text'].strip()
            
            # Clean up the response
            response_text = self._clean_response(response_text)
            
            return response_text
            
        except Exception as e:
            self.logger.error(f"Error generating LLM response: {e}")
            return self._fallback_response(user_input)
    
    def _build_context(self, user_input: str) -> str:
        """Build conversation context for the LLM"""
        # Get user preferences and relevant memories
        user_name = self.memory.get_user_preference('name', 'User')
        relevant_memories = self.memory.search_memories(user_input, limit=3)
        
        # Get recent conversation history
        conversation_history = self.memory.get_recent_conversation(limit=5)
        
        # Build the context
        context_parts = []
        
        # System prompt
        context_parts.append(
            "You are CommandEcho, an intelligent AI assistant similar to Jarvis from Iron Man. "
            "You are helpful, conversational, and have a slightly sophisticated personality. "
            "You can control computer systems and remember information about the user. "
            f"The user's name is {user_name}. "
            "Keep responses concise but friendly."
        )
        
        # Add relevant memories if any
        if relevant_memories:
            context_parts.append("\nRelevant information I remember:")
            for memory in relevant_memories:
                context_parts.append(f"- {memory}")
        
        # Add conversation history
        if conversation_history:
            context_parts.append("\nRecent conversation:")
            for entry in conversation_history:
                role = entry['role'].title()
                content = entry['content']
                context_parts.append(f"{role}: {content}")
        
        # Add current user input
        context_parts.append(f"\nUser: {user_input}")
        context_parts.append("CommandEcho:")
        
        return "\n".join(context_parts)
    
    def _clean_response(self, response: str) -> str:
        """Clean up the LLM response"""
        # Remove any unwanted prefixes
        prefixes_to_remove = ["CommandEcho:", "Assistant:", "AI:"]
        for prefix in prefixes_to_remove:
            if response.startswith(prefix):
                response = response[len(prefix):].strip()
        
        # Remove any trailing incomplete sentences
        sentences = response.split('.')
        if len(sentences) > 1 and len(sentences[-1].strip()) < 10:
            response = '.'.join(sentences[:-1]) + '.'
        
        return response.strip()
    
    def _fallback_response(self, user_input: str) -> str:
        """Provide fallback responses when LLM is not available"""
        user_input_lower = user_input.lower()
        
        # Simple pattern matching for common queries
        if any(greeting in user_input_lower for greeting in ['hello', 'hi', 'hey']):
            return "Hello! I'm CommandEcho, your AI assistant. How can I help you today?"
        
        elif any(question in user_input_lower for question in ['how are you', 'how do you do']):
            return "I'm functioning well, thank you! Ready to assist you with any tasks."
        
        elif any(thanks in user_input_lower for thanks in ['thank you', 'thanks']):
            return "You're welcome! I'm here whenever you need assistance."
        
        elif 'weather' in user_input_lower:
            return "I don't have access to current weather data, but you can check your local weather app or website."
        
        elif 'time' in user_input_lower:
            from datetime import datetime
            current_time = datetime.now().strftime("%I:%M %p")
            return f"The current time is {current_time}."
        
        else:
            return ("I understand you're asking about something, but I need my full AI model to provide a proper response. "
                   "Please ensure the LLaMA model is properly installed.")
