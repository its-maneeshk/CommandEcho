"""
Main GUI Window for CommandEcho
Modern interface with chat display and controls
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
import time
from datetime import datetime
from pathlib import Path
import json

# Custom styling
class ModernStyle:
    """Modern color scheme and styling"""
    
    # Colors
    BG_DARK = "#1e1e1e"
    BG_LIGHT = "#2d2d2d"
    BG_ACCENT = "#3d3d3d"
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#b0b0b0"
    ACCENT_BLUE = "#0078d4"
    ACCENT_GREEN = "#16c60c"
    ACCENT_RED = "#e74c3c"
    ACCENT_ORANGE = "#ff8c00"
    
    @staticmethod
    def configure_ttk_style():
        """Configure modern TTK styles"""
        style = ttk.Style()
        
        # Configure styles for dark theme
        style.configure("Modern.TFrame", background=ModernStyle.BG_DARK)
        style.configure("Accent.TFrame", background=ModernStyle.BG_ACCENT)
        
        style.configure("Modern.TLabel", 
                       background=ModernStyle.BG_DARK, 
                       foreground=ModernStyle.TEXT_PRIMARY,
                       font=("Segoe UI", 10))
        
        style.configure("Title.TLabel",
                       background=ModernStyle.BG_DARK,
                       foreground=ModernStyle.TEXT_PRIMARY,
                       font=("Segoe UI", 16, "bold"))
        
        style.configure("Status.TLabel",
                       background=ModernStyle.BG_DARK,
                       foreground=ModernStyle.TEXT_SECONDARY,
                       font=("Segoe UI", 9))
        
        style.configure("Modern.TButton",
                       background=ModernStyle.ACCENT_BLUE,
                       foreground=ModernStyle.TEXT_PRIMARY,
                       borderwidth=0,
                       focuscolor="none",
                       font=("Segoe UI", 10))
        
        style.map("Modern.TButton",
                 background=[("active", "#106ebe"),
                           ("pressed", "#005a9e")])

class CommandEchoGUI:
    """Main GUI Application for CommandEcho"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        
        # Communication queues
        self.message_queue = queue.Queue()
        self.command_queue = queue.Queue()
        
        # Assistant state
        self.assistant = None
        self.assistant_thread = None
        self.is_listening = False
        self.is_speaking = False
        
        # GUI components
        self.setup_gui()
        self.setup_styles()
        
        # Start GUI update loop
        self.update_gui()
        
    def setup_window(self):
        """Setup main window properties"""
        self.root.title("CommandEcho - AI Voice Assistant")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Set icon (if available)
        try:
            self.root.iconbitmap("assets/icon.ico")
        except:
            pass
        
        # Configure for dark theme
        self.root.configure(bg=ModernStyle.BG_DARK)
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_styles(self):
        """Setup modern styling"""
        ModernStyle.configure_ttk_style()
    
    def setup_gui(self):
        """Setup GUI components"""
        # Main container
        main_frame = ttk.Frame(self.root, style="Modern.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title bar
        self.setup_title_bar(main_frame)
        
        # Status bar
        self.setup_status_bar(main_frame)
        
        # Main content area
        content_frame = ttk.Frame(main_frame, style="Modern.TFrame")
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Left panel - Chat
        self.setup_chat_panel(content_frame)
        
        # Right panel - Controls
        self.setup_control_panel(content_frame)
    
    def setup_title_bar(self, parent):
        """Setup title bar with logo and title"""
        title_frame = ttk.Frame(parent, style="Modern.TFrame")
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        title_label = ttk.Label(title_frame, text="🤖 CommandEcho", style="Title.TLabel")
        title_label.pack(side=tk.LEFT)
        
        # Version info
        version_label = ttk.Label(title_frame, text="v1.0.0", style="Status.TLabel")
        version_label.pack(side=tk.RIGHT)
    
    def setup_status_bar(self, parent):
        """Setup status bar"""
        status_frame = ttk.Frame(parent, style="Accent.TFrame")
        status_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Status indicator
        self.status_label = ttk.Label(status_frame, text="● Initializing...", style="Status.TLabel")
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Mode indicator
        self.mode_label = ttk.Label(status_frame, text="Mode: GUI", style="Status.TLabel")
        self.mode_label.pack(side=tk.RIGHT, padx=10, pady=5)
    
    def setup_chat_panel(self, parent):
        """Setup chat display panel"""
        # Chat frame
        chat_frame = ttk.Frame(parent, style="Modern.TFrame")
        chat_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Chat title
        chat_title = ttk.Label(chat_frame, text="Conversation", style="Modern.TLabel")
        chat_title.pack(anchor=tk.W, pady=(0, 5))
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            width=50,
            height=25,
            bg=ModernStyle.BG_LIGHT,
            fg=ModernStyle.TEXT_PRIMARY,
            insertbackground=ModernStyle.TEXT_PRIMARY,
            selectbackground=ModernStyle.ACCENT_BLUE,
            font=("Consolas", 10),
            border=0,
            highlightthickness=1,
            highlightcolor=ModernStyle.ACCENT_BLUE
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Input frame
        input_frame = ttk.Frame(chat_frame, style="Modern.TFrame")
        input_frame.pack(fill=tk.X)
        
        # Text input
        self.text_input = tk.Entry(
            input_frame,
            bg=ModernStyle.BG_LIGHT,
            fg=ModernStyle.TEXT_PRIMARY,
            insertbackground=ModernStyle.TEXT_PRIMARY,
            font=("Segoe UI", 10),
            border=0,
            highlightthickness=1,
            highlightcolor=ModernStyle.ACCENT_BLUE
        )
        self.text_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.text_input.bind("<Return>", self.send_text_message)
        
        # Send button
        send_btn = ttk.Button(
            input_frame,
            text="Send",
            style="Modern.TButton",
            command=self.send_text_message
        )
        send_btn.pack(side=tk.RIGHT)
    
    def setup_control_panel(self, parent):
        """Setup control panel"""
        control_frame = ttk.Frame(parent, style="Accent.TFrame")
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 0))
        control_frame.configure(width=250)
        
        # Controls title
        controls_title = ttk.Label(control_frame, text="Controls", style="Modern.TLabel")
        controls_title.pack(pady=10)
        
        # Voice controls
        self.setup_voice_controls(control_frame)
        
        # System info
        self.setup_system_info(control_frame)
        
        # Settings
        self.setup_settings_controls(control_frame)
    
    def setup_voice_controls(self, parent):
        """Setup voice control buttons"""
        voice_frame = ttk.LabelFrame(parent, text="Voice Controls", style="Modern.TFrame")
        voice_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Voice mode toggle
        self.voice_mode_var = tk.BooleanVar(value=False)
        voice_toggle = ttk.Checkbutton(
            voice_frame,
            text="Voice Mode",
            variable=self.voice_mode_var,
            command=self.toggle_voice_mode
        )
        voice_toggle.pack(pady=5)
        
        # Listen button
        self.listen_btn = ttk.Button(
            voice_frame,
            text="🎤 Start Listening",
            style="Modern.TButton",
            command=self.toggle_listening
        )
        self.listen_btn.pack(fill=tk.X, padx=5, pady=2)
        
        # Stop speaking button
        self.stop_btn = ttk.Button(
            voice_frame,
            text="🔇 Stop Speaking",
            style="Modern.TButton",
            command=self.stop_speaking
        )
        self.stop_btn.pack(fill=tk.X, padx=5, pady=2)
        
        # Voice level indicator
        self.voice_level = ttk.Progressbar(
            voice_frame,
            mode='determinate',
            length=200
        )
        self.voice_level.pack(fill=tk.X, padx=5, pady=5)
    
    def setup_system_info(self, parent):
        """Setup system information display"""
        info_frame = ttk.LabelFrame(parent, text="System Info", style="Modern.TFrame")
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # System stats
        self.cpu_label = ttk.Label(info_frame, text="CPU: --", style="Status.TLabel")
        self.cpu_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.memory_label = ttk.Label(info_frame, text="Memory: --", style="Status.TLabel")
        self.memory_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.model_label = ttk.Label(info_frame, text="Model: Loading...", style="Status.TLabel")
        self.model_label.pack(anchor=tk.W, padx=5, pady=2)
        
        # Update system info periodically
        self.update_system_info()
    
    def setup_settings_controls(self, parent):
        """Setup settings controls"""
        settings_frame = ttk.LabelFrame(parent, text="Settings", style="Modern.TFrame")
        settings_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Settings button
        settings_btn = ttk.Button(
            settings_frame,
            text="⚙️ Open Settings",
            style="Modern.TButton",
            command=self.open_settings
        )
        settings_btn.pack(fill=tk.X, padx=5, pady=5)
        
        # Clear chat button
        clear_btn = ttk.Button(
            settings_frame,
            text="🗑️ Clear Chat",
            style="Modern.TButton",
            command=self.clear_chat
        )
        clear_btn.pack(fill=tk.X, padx=5, pady=2)
        
        # Exit button
        exit_btn = ttk.Button(
            settings_frame,
            text="❌ Exit",
            style="Modern.TButton",
            command=self.on_closing
        )
        exit_btn.pack(fill=tk.X, padx=5, pady=2)
    
    def add_message(self, sender: str, message: str, timestamp: str = None):
        """Add message to chat display"""
        if timestamp is None:
            timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Color coding
        if sender.lower() == "you":
            color = ModernStyle.ACCENT_BLUE
            prefix = "👤"
        elif sender.lower() == "commandecho":
            color = ModernStyle.ACCENT_GREEN
            prefix = "🤖"
        else:
            color = ModernStyle.TEXT_SECONDARY
            prefix = "ℹ️"
        
        # Insert message
        self.chat_display.configure(state=tk.NORMAL)
        
        # Add timestamp and sender
        self.chat_display.insert(tk.END, f"[{timestamp}] {prefix} {sender}:\n", "timestamp")
        
        # Add message content
        self.chat_display.insert(tk.END, f"{message}\n\n", "message")
        
        # Configure tags for styling
        self.chat_display.tag_configure("timestamp", foreground=ModernStyle.TEXT_SECONDARY, font=("Consolas", 9))
        self.chat_display.tag_configure("message", foreground=ModernStyle.TEXT_PRIMARY)
        
        # Scroll to bottom
        self.chat_display.see(tk.END)
        self.chat_display.configure(state=tk.DISABLED)
    
    def send_text_message(self, event=None):
        """Send text message"""
        message = self.text_input.get().strip()
        if not message:
            return
        
        # Clear input
        self.text_input.delete(0, tk.END)
        
        # Add to chat
        self.add_message("You", message)
        
        # Send to assistant (if running)
        if self.assistant:
            self.command_queue.put(("text_input", message))
        else:
            self.add_message("System", "Assistant not running. Please start the assistant first.")
    
    def toggle_voice_mode(self):
        """Toggle voice mode"""
        if self.voice_mode_var.get():
            self.add_message("System", "Voice mode enabled. You can now use voice commands.")
            self.update_status("Voice mode active", ModernStyle.ACCENT_GREEN)
        else:
            self.add_message("System", "Voice mode disabled. Using text mode only.")
            self.update_status("Text mode active", ModernStyle.ACCENT_BLUE)
    
    def toggle_listening(self):
        """Toggle listening state"""
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening()
    
    def start_listening(self):
        """Start listening for voice input"""
        if not self.voice_mode_var.get():
            messagebox.showwarning("Voice Mode", "Please enable voice mode first.")
            return
        
        self.is_listening = True
        self.listen_btn.configure(text="🔴 Stop Listening")
        self.update_status("Listening...", ModernStyle.ACCENT_GREEN)
        self.add_message("System", "Listening for voice input... Say 'Echo' to activate.")
        
        # Start voice input thread
        if self.assistant:
            self.command_queue.put(("start_listening", None))
    
    def stop_listening(self):
        """Stop listening for voice input"""
        self.is_listening = False
        self.listen_btn.configure(text="🎤 Start Listening")
        self.update_status("Ready", ModernStyle.ACCENT_BLUE)
        self.add_message("System", "Stopped listening.")
        
        if self.assistant:
            self.command_queue.put(("stop_listening", None))
    
    def stop_speaking(self):
        """Stop current speech"""
        if self.assistant:
            self.command_queue.put(("stop_speaking", None))
        self.add_message("System", "Speech stopped.")
    
    def update_status(self, message: str, color: str = None):
        """Update status bar"""
        if color:
            self.status_label.configure(foreground=color)
        self.status_label.configure(text=f"● {message}")
    
    def update_system_info(self):
        """Update system information display"""
        try:
            import psutil
            
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=None)
            self.cpu_label.configure(text=f"CPU: {cpu_percent:.1f}%")
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            self.memory_label.configure(text=f"Memory: {memory_percent:.1f}%")
            
            # Update voice level (simulate for now)
            if self.is_listening:
                import random
                level = random.randint(10, 90)
                self.voice_level['value'] = level
            else:
                self.voice_level['value'] = 0
            
        except Exception as e:
            pass
        
        # Schedule next update
        self.root.after(2000, self.update_system_info)
    
    def open_settings(self):
        """Open settings window"""
        SettingsWindow(self.root, self)
    
    def clear_chat(self):
        """Clear chat display"""
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.configure(state=tk.DISABLED)
        self.add_message("System", "Chat cleared.")
    
    def start_assistant(self):
        """Start the CommandEcho assistant"""
        try:
            from core.assistant import CommandEcho
            from core.config import Config
            
            # Initialize assistant
            config = Config()
            self.assistant = CommandEcho(config, text_mode=True)  # Start in text mode for GUI
            
            # Start assistant thread
            self.assistant_thread = threading.Thread(target=self.run_assistant, daemon=True)
            self.assistant_thread.start()
            
            self.add_message("System", "CommandEcho assistant started successfully!")
            self.update_status("Assistant ready", ModernStyle.ACCENT_GREEN)
            
        except Exception as e:
            self.add_message("System", f"Failed to start assistant: {str(e)}")
            self.update_status("Assistant failed", ModernStyle.ACCENT_RED)
    
    def run_assistant(self):
        """Run assistant in background thread"""
        # This would integrate with the actual assistant
        # For now, simulate responses
        while True:
            try:
                # Check for commands from GUI
                try:
                    command_type, data = self.command_queue.get_nowait()
                    
                    if command_type == "text_input":
                        # Process text input
                        response = self.process_command(data)
                        self.message_queue.put(("assistant_response", response))
                    
                    elif command_type == "start_listening":
                        # Start voice listening
                        pass
                    
                    elif command_type == "stop_listening":
                        # Stop voice listening
                        pass
                    
                    elif command_type == "stop_speaking":
                        # Stop speaking
                        pass
                        
                except queue.Empty:
                    pass
                
                time.sleep(0.1)
                
            except Exception as e:
                self.message_queue.put(("error", str(e)))
    
    def process_command(self, command: str) -> str:
        """Process command and return response"""
        # This would integrate with the actual CommandEcho brain
        # For now, provide simple responses
        
        command_lower = command.lower()
        
        if any(greeting in command_lower for greeting in ['hello', 'hi', 'hey']):
            return "Hello! I'm CommandEcho, your AI assistant. How can I help you today?"
        
        elif 'time' in command_lower:
            from datetime import datetime
            current_time = datetime.now().strftime("%I:%M %p")
            return f"The current time is {current_time}."
        
        elif 'weather' in command_lower:
            return "I don't have access to current weather data, but you can check your local weather app."
        
        elif any(thanks in command_lower for thanks in ['thank you', 'thanks']):
            return "You're welcome! I'm here to help whenever you need assistance."
        
        else:
            return f"I understand you said: '{command}'. I'm processing your request..."
    
    def update_gui(self):
        """Update GUI with messages from assistant"""
        try:
            # Process messages from assistant
            while True:
                try:
                    message_type, data = self.message_queue.get_nowait()
                    
                    if message_type == "assistant_response":
                        self.add_message("CommandEcho", data)
                    
                    elif message_type == "error":
                        self.add_message("System", f"Error: {data}")
                    
                    elif message_type == "status_update":
                        self.update_status(data)
                        
                except queue.Empty:
                    break
            
        except Exception as e:
            pass
        
        # Schedule next update
        self.root.after(100, self.update_gui)
    
    def on_closing(self):
        """Handle window closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit CommandEcho?"):
            # Stop assistant
            if self.assistant:
                self.command_queue.put(("shutdown", None))
            
            self.root.destroy()
    
    def run(self):
        """Run the GUI application"""
        # Start assistant
        self.start_assistant()
        
        # Add welcome message
        self.add_message("System", "Welcome to CommandEcho! 🤖")
        self.add_message("System", "Wake word: 'Echo' (configurable in settings)")
        self.add_message("System", "You can type messages or enable voice mode for voice commands.")
        
        # Start GUI
        self.root.mainloop()

class SettingsWindow:
    """Settings configuration window"""
    
    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app
        
        # Create settings window
        self.window = tk.Toplevel(parent)
        self.window.title("CommandEcho Settings")
        self.window.geometry("500x600")
        self.window.configure(bg=ModernStyle.BG_DARK)
        self.window.transient(parent)
        self.window.grab_set()
        
        self.setup_settings_gui()
        self.load_current_settings()
    
    def setup_settings_gui(self):
        """Setup settings GUI"""
        # Main frame
        main_frame = ttk.Frame(self.window, style="Modern.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title = ttk.Label(main_frame, text="Settings", style="Title.TLabel")
        title.pack(pady=(0, 20))
        
        # Voice settings
        self.setup_voice_settings(main_frame)
        
        # AI settings
        self.setup_ai_settings(main_frame)
        
        # Memory settings
        self.setup_memory_settings(main_frame)
        
        # Buttons
        self.setup_buttons(main_frame)
    
    def setup_voice_settings(self, parent):
        """Setup voice configuration"""
        voice_frame = ttk.LabelFrame(parent, text="Voice Settings")
        voice_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Wake word
        ttk.Label(voice_frame, text="Wake Word:").pack(anchor=tk.W, padx=5, pady=2)
        self.wake_word_var = tk.StringVar(value="echo")
        wake_word_entry = ttk.Entry(voice_frame, textvariable=self.wake_word_var)
        wake_word_entry.pack(fill=tk.X, padx=5, pady=2)
        
        # Always listening
        self.always_listening_var = tk.BooleanVar()
        always_listening_cb = ttk.Checkbutton(
            voice_frame,
            text="Always Listening (no wake word needed)",
            variable=self.always_listening_var
        )
        always_listening_cb.pack(anchor=tk.W, padx=5, pady=5)
        
        # Speech rate
        ttk.Label(voice_frame, text="Speech Rate:").pack(anchor=tk.W, padx=5, pady=2)
        self.speech_rate_var = tk.IntVar(value=200)
        speech_rate_scale = ttk.Scale(
            voice_frame,
            from_=100,
            to=300,
            variable=self.speech_rate_var,
            orient=tk.HORIZONTAL
        )
        speech_rate_scale.pack(fill=tk.X, padx=5, pady=2)
        
        # Volume
        ttk.Label(voice_frame, text="Speech Volume:").pack(anchor=tk.W, padx=5, pady=2)
        self.speech_volume_var = tk.DoubleVar(value=0.9)
        volume_scale = ttk.Scale(
            voice_frame,
            from_=0.0,
            to=1.0,
            variable=self.speech_volume_var,
            orient=tk.HORIZONTAL
        )
        volume_scale.pack(fill=tk.X, padx=5, pady=2)
    
    def setup_ai_settings(self, parent):
        """Setup AI configuration"""
        ai_frame = ttk.LabelFrame(parent, text="AI Settings")
        ai_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Model path
        ttk.Label(ai_frame, text="Model Path:").pack(anchor=tk.W, padx=5, pady=2)
        self.model_path_var = tk.StringVar(value="models/llama-3-8b-instruct.Q4_K_M.gguf")
        model_path_entry = ttk.Entry(ai_frame, textvariable=self.model_path_var)
        model_path_entry.pack(fill=tk.X, padx=5, pady=2)
        
        # Temperature
        ttk.Label(ai_frame, text="Temperature (Creativity):").pack(anchor=tk.W, padx=5, pady=2)
        self.temperature_var = tk.DoubleVar(value=0.7)
        temp_scale = ttk.Scale(
            ai_frame,
            from_=0.1,
            to=1.0,
            variable=self.temperature_var,
            orient=tk.HORIZONTAL
        )
        temp_scale.pack(fill=tk.X, padx=5, pady=2)
        
        # Max tokens
        ttk.Label(ai_frame, text="Max Response Length:").pack(anchor=tk.W, padx=5, pady=2)
        self.max_tokens_var = tk.IntVar(value=512)
        tokens_scale = ttk.Scale(
            ai_frame,
            from_=128,
            to=2048,
            variable=self.max_tokens_var,
            orient=tk.HORIZONTAL
        )
        tokens_scale.pack(fill=tk.X, padx=5, pady=2)
    
    def setup_memory_settings(self, parent):
        """Setup memory configuration"""
        memory_frame = ttk.LabelFrame(parent, text="Memory Settings")
        memory_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Short-term memory limit
        ttk.Label(memory_frame, text="Short-term Memory Limit:").pack(anchor=tk.W, padx=5, pady=2)
        self.memory_limit_var = tk.IntVar(value=10)
        memory_scale = ttk.Scale(
            memory_frame,
            from_=5,
            to=50,
            variable=self.memory_limit_var,
            orient=tk.HORIZONTAL
        )
        memory_scale.pack(fill=tk.X, padx=5, pady=2)
        
        # Memory stats
        stats_frame = ttk.Frame(memory_frame)
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(stats_frame, text="Total Memories: 0").pack(anchor=tk.W)
        ttk.Label(stats_frame, text="Conversations: 0").pack(anchor=tk.W)
        ttk.Label(stats_frame, text="User Preferences: 0").pack(anchor=tk.W)
    
    def setup_buttons(self, parent):
        """Setup action buttons"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Save button
        save_btn = ttk.Button(
            button_frame,
            text="Save Settings",
            command=self.save_settings
        )
        save_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Cancel button
        cancel_btn = ttk.Button(
            button_frame,
            text="Cancel",
            command=self.window.destroy
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Reset button
        reset_btn = ttk.Button(
            button_frame,
            text="Reset to Defaults",
            command=self.reset_settings
        )
        reset_btn.pack(side=tk.RIGHT)
    
    def load_current_settings(self):
        """Load current settings from config"""
        try:
            config_path = Path("config/config.json")
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                # Load voice settings
                voice_config = config.get('voice', {})
                self.wake_word_var.set(voice_config.get('wake_word', 'echo'))
                self.always_listening_var.set(voice_config.get('always_listening', False))
                self.speech_rate_var.set(voice_config.get('speech_rate', 200))
                self.speech_volume_var.set(voice_config.get('speech_volume', 0.9))
                
                # Load AI settings
                llm_config = config.get('llm', {})
                self.model_path_var.set(llm_config.get('model_path', 'models/llama-3-8b-instruct.Q4_K_M.gguf'))
                self.temperature_var.set(llm_config.get('temperature', 0.7))
                self.max_tokens_var.set(llm_config.get('max_tokens', 512))
                
                # Load memory settings
                memory_config = config.get('memory', {})
                self.memory_limit_var.set(memory_config.get('max_short_term_memory', 10))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load settings: {e}")
    
    def save_settings(self):
        """Save settings to config file"""
        try:
            config = {
                'voice': {
                    'wake_word': self.wake_word_var.get(),
                    'always_listening': self.always_listening_var.get(),
                    'speech_rate': self.speech_rate_var.get(),
                    'speech_volume': self.speech_volume_var.get(),
                    'voice_id': 0
                },
                'llm': {
                    'model_path': self.model_path_var.get(),
                    'context_length': 4096,
                    'max_tokens': self.max_tokens_var.get(),
                    'temperature': self.temperature_var.get(),
                    'top_p': 0.9
                },
                'memory': {
                    'memory_db_path': 'data/memory/memory.db',
                    'vector_db_path': 'data/memory/vectors',
                    'max_short_term_memory': self.memory_limit_var.get(),
                    'embedding_model': 'all-MiniLM-L6-v2'
                }
            }
            
            # Save to file
            config_path = Path("config/config.json")
            config_path.parent.mkdir(exist_ok=True)
            
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            messagebox.showinfo("Success", "Settings saved successfully!")
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")
    
    def reset_settings(self):
        """Reset settings to defaults"""
        if messagebox.askyesno("Reset Settings", "Are you sure you want to reset all settings to defaults?"):
            self.wake_word_var.set("echo")
            self.always_listening_var.set(False)
            self.speech_rate_var.set(200)
            self.speech_volume_var.set(0.9)
            self.model_path_var.set("models/llama-3-8b-instruct.Q4_K_M.gguf")
            self.temperature_var.set(0.7)
            self.max_tokens_var.set(512)
            self.memory_limit_var.set(10)

def main():
    """Run the GUI application"""
    app = CommandEchoGUI()
    app.run()

if __name__ == "__main__":
    main()
