# CommandEcho - Offline AI Voice Assistant

CommandEcho is an intelligent offline AI voice assistant similar to Iron Man's Jarvis. It runs entirely locally without requiring internet connectivity or cloud API calls.

## 🌟 Features

- **Offline AI Brain**: Uses local LLaMA models for intelligent responses
- **Voice Interface**: Speech recognition and text-to-speech capabilities
- **Memory System**: Remembers conversations and user preferences
- **System Control**: Control volume, brightness, launch apps, get system info
- **File Management**: Search and manage files through voice commands
- **Conversational**: Chat naturally like with ChatGPT, not just fixed commands

## 🚀 Quick Start

### 1. Setup
\`\`\`bash
# Clone or download the project
cd CommandEcho

# Run setup script
python setup.py
\`\`\`

### 2. Download AI Model
Download a LLaMA model in GGUF format:
- **Recommended**: [Llama-3.2-3B-Instruct](https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF)
- Place the `.gguf` file in `models/llama-3-8b-instruct.Q4_K_M.gguf`

### 3. Run CommandEcho
\`\`\`bash
# Text mode (for testing)
python main.py --text-mode

# Voice mode
python main.py
\`\`\`

## 📁 Project Structure

\`\`\`
CommandEcho/
├── main.py                 # Entry point
├── core/                   # Core functionality
│   ├── assistant.py        # Main assistant orchestrator
│   ├── config.py          # Configuration management
│   ├── voice_input.py     # Speech recognition
│   ├── voice_output.py    # Text-to-speech
│   └── command_handler.py # Command processing
├── brain/                  # AI and memory
│   ├── llm_brain.py       # LLaMA integration
│   └── memory_system.py   # Long-term memory
├── tools/                  # System control tools
│   ├── system_control.py  # Volume, brightness, etc.
│   ├── file_manager.py    # File operations
│   └── app_launcher.py    # App launching
├── models/                 # Place LLaMA models here
├── data/memory/           # Memory storage
└── config/                # Configuration files
\`\`\`

## 🎯 Usage Examples

### Voice Commands
- "Hello Echo, what's the weather like?" (conversational)
- "Set volume to 50"
- "Open Visual Studio Code"
- "What's my battery level?"
- "Find files containing 'project'"
- "Remember that I prefer dark mode"
- "My name is John"

### Text Mode
\`\`\`
You: Hello, how are you?
CommandEcho: Hello! I'm functioning well and ready to assist you. How can I help you today?

You: Open notepad
CommandEcho: Launched Notepad

You: What time is it?
CommandEcho: The current time is 2:30 PM on Monday, January 15, 2024
\`\`\`

## ⚙️ Configuration

Edit `config/config.json` to customize:

\`\`\`json
{
  "voice": {
    "wake_word": "echo",
    "always_listening": false,
    "speech_rate": 200,
    "speech_volume": 0.9
  },
  "llm": {
    "model_path": "models/llama-3-8b-instruct.Q4_K_M.gguf",
    "context_length": 4096,
    "max_tokens": 512,
    "temperature": 0.7
  }
}
\`\`\`

## 🧠 Memory System

CommandEcho remembers:
- Your name and preferences
- Past conversations
- Important information you tell it
- System usage patterns

Memory is stored locally in:
- SQLite database for structured data
- FAISS vector database for semantic search

## 🛠️ System Requirements

- **Python**: 3.8 or higher
- **RAM**: 8GB minimum (16GB recommended for larger models)
- **Storage**: 5-10GB for models
- **OS**: Windows 10/11, Linux, macOS

## 📦 Dependencies

Core dependencies:
- `llama-cpp-python` - Local LLM inference
- `speech_recognition` - Voice input
- `pyttsx3` - Text-to-speech
- `psutil` - System information
- `sentence-transformers` - Memory embeddings
- `faiss-cpu` - Vector search

## 🔧 Troubleshooting

### Model Issues
- Ensure model file is in correct location
- Check model file isn't corrupted
- Try a smaller model if running out of memory

### Audio Issues
- **Windows**: Install Visual C++ Redistributable
- **Linux**: `sudo apt-get install portaudio19-dev python3-pyaudio`
- **macOS**: `brew install portaudio`

### Performance
- Use Q4_K_M quantized models for best speed/quality balance
- Reduce `context_length` in config for faster responses
- Close other applications to free up RAM

## 🚧 Extending CommandEcho

### Adding New Commands
1. Add patterns to `core/command_handler.py`
2. Implement handler methods
3. Add tool functions in `tools/` directory

### Adding New Tools
1. Create new tool class in `tools/`
2. Import in `command_handler.py`
3. Add command patterns and handlers

### Custom Models
- Replace model path in config
- Ensure model is in GGUF format
- Adjust context length as needed

## 📄 License

This project is open source. Feel free to modify and extend it for your needs.

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional system integrations
- Better natural language understanding
- More efficient memory management
- Cross-platform compatibility improvements

---

**Note**: This is an offline-first assistant. No data is sent to external servers, ensuring complete privacy and security.
