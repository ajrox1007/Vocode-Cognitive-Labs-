# VoCode - Voice-Activated Coding Assistant

A Python-based voice-activated coding assistant that listens to your commands and generates Python code using AI, with text-to-speech feedback powered by ElevenLabs.

## Features

- **Voice Command Recognition**: Uses Google Speech Recognition to capture your coding requests
- **AI Code Generation**: Processes commands through a local API to generate Python code
- **Text-to-Speech Feedback**: Provides audio feedback using ElevenLabs' Rachel voice
- **System Tray Integration**: Runs quietly in the background with a system tray icon
- **VS Code Integration**: Automatically opens generated files in Visual Studio Code
- **Smart File Management**: Creates new Python files or continues existing ones
- **Context-Aware Coding**: Reads existing code to provide contextual continuations

## Prerequisites

### Software Requirements
- Python 3.7+
- Visual Studio Code
- Microphone for voice input
- Internet connection for speech recognition and TTS

### Python Dependencies
Install the required packages using pip:

```bash
pip install speech_recognition
pip install pystray
pip install Pillow
pip install elevenlabs
pip install requests
pip install playsound
```

### System Dependencies
- **macOS/Linux**: Install `portaudio` for microphone support:
  ```bash
  # macOS
  brew install portaudio
  
  # Ubuntu/Debian
  sudo apt-get install portaudio19-dev
  ```

## Setup Instructions

### 1. ElevenLabs API Configuration
1. Sign up for an [ElevenLabs account](https://elevenlabs.io)
2. Get your API key from the ElevenLabs dashboard
3. Replace the API key in the code:
   ```python
   client = ElevenLabs(
       api_key="your_elevenlabs_api_key_here"
   )
   ```

### 2. Local API Server
This application expects a local API server running on `http://localhost:8000/command` that processes coding prompts. You'll need to set up a server that:
- Accepts POST requests with JSON payload: `{"prompt": "your_command", "max_tokens": 7000}`
- Returns JSON response with: `{"code": "generated_code"}`

### 3. System Tray Icon
1. Create or obtain an icon image file (PNG format recommended)
2. Update the icon path in the code:
   ```python
   icon_image_path = "/path/to/your/icon.png"
   ```

### 4. Directory Configuration
Set your preferred working directory:
```python
directory_to_watch = "/path/to/your/projects"
```

## Usage

### Starting the Assistant
1. Run the application:
   ```bash
   python vocode_ver_3.py
   ```
2. The application will start in the system tray
3. Right-click the tray icon and select "Activate Voice Assistant"
4. Speak your coding command when you hear "Listening..."

### Voice Commands
The assistant responds to natural language coding requests:
- "Create a function to calculate fibonacci numbers"
- "Add error handling to the existing code"
- "Create a class for managing user data"
- "Add a method to save data to JSON file"

### Workflow
1. **First Command**: Creates a new Python file with generated code
2. **Subsequent Commands**: Continues coding in the same file, reading existing code for context
3. **File Management**: Automatically opens files in VS Code and provides audio feedback

## File Structure

```
vocode_ver_3.py          # Main application file
temp_rachel.mp3          # Temporary audio file (auto-deleted)
untitled.py              # Generated Python files
untitled_1.py            # Additional files if needed
...
```

## Configuration Options

### Voice Settings
Customize the ElevenLabs voice parameters:
```python
voice_settings=VoiceSettings(
    stability=0.1,      # Voice stability (0.0-1.0)
    similarity_boost=0.3, # Voice similarity (0.0-1.0)
    style=0.2,          # Voice style (0.0-1.0)
)
```

### Code Context
Adjust how much existing code to consider:
```python
def get_existing_code(filepath, max_lines=50):  # Modify max_lines as needed
```

## Troubleshooting

### Common Issues

**Microphone not working**:
- Check microphone permissions in system settings
- Ensure `portaudio` is installed
- Test microphone with other applications

**ElevenLabs API errors**:
- Verify API key is correct and has sufficient credits
- Check internet connection
- Ensure API key has proper permissions

**VS Code not opening**:
- Verify VS Code is installed and `code` command is available in PATH
- Try running `code --version` in terminal

**Speech recognition fails**:
- Speak clearly and at moderate pace
- Reduce background noise
- Check internet connection (Google Speech Recognition requires internet)

### Error Messages
- `"Error with ElevenLabs TTS"`: Check API key and internet connection
- `"Failed to open in VS Code"`: Verify VS Code installation and PATH
- `"An error occurred while processing your command"`: Check local API server status

## Limitations

- Requires active internet connection for speech recognition and TTS
- Depends on local API server for code generation
- Currently supports Python file generation only
- macOS-specific file paths in the example

## Security Notes

- Store API keys securely and consider using environment variables
- Be cautious with generated code - review before execution
- The application has file system access to the configured directory

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Test your changes thoroughly
4. Submit a pull request with detailed description

