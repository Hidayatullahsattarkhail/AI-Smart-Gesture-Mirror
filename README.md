# Smart Mirror - Gesture & Voice Controlled Display

A smart mirror application with gesture and voice control, featuring draggable widgets, virtual cursor, and minimalist design.

## Features

### ✅ Core Functionality
- **Widgets**: Clock, Weather, Calendar, News, Notes
- **Gesture Control**: Index finger cursor tracking within widget window
- **Drag & Drop**: Pinch to drag widgets, release to drop
- **Virtual Cursor**: Visual cursor overlay (not system cursor)
- **Voice Commands**: "Hey Mirror" wake word support
- **Minimalist Design**: Clean, modern UI with dark theme

### 🎯 Gesture Controls
- **Index Finger**: Move cursor within widget area
- **Pinch (Thumb + Index)**: Start dragging widget
- **Unpinch**: Release widget
- **Cursor Boundary**: Only tracks gestures within widget window

### 🎤 Voice Commands
- **Wake Word**: "Hey Mirror" (requires Porcupine API key, or uses continuous mode)
- **Commands**: 
  - "show weather"
  - "show clock"
  - "show calendar"
  - "show news"
  - "show notes"

## Prerequisites

- **Python**: 3.9+
- **OS**: Windows 10/11, Linux (Raspberry Pi OS recommended), macOS
- **Hardware**: 
  - Webcam or OAK-D camera
  - Microphone (for voice commands)
  - Display with two-way mirror (optional)

## Installation

### 1. Clone & Setup
```bash
cd smart_mirror
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

**Note for Raspberry Pi:**
```bash
sudo apt-get update
sudo apt-get install python3-opencv python3-pyaudio libatlas-base-dev portaudio19-dev
```

**Note for Windows:**
- PyAudio might need Visual C++ Build Tools
- Or use pre-built wheels: `pip install pipwin && pipwin install pyaudio`

### 3. Configuration
Edit `config.json` to add your API keys:
- **Weather**: [OpenWeatherMap](https://openweathermap.org/) API key
- **News**: [NewsAPI](https://newsapi.org/) API key
- **AI**: [OpenAI](https://openai.com/) API key (optional)
- **Voice**: Porcupine access key (optional, for wake word detection)

### 4. Run Application
```bash
python main.py
```

**Controls:**
- `F11`: Toggle fullscreen
- `ESC`: Exit application

## Configuration

Edit `config.json`:

```json
{
    "app": {
        "name": "Smart Mirror",
        "fullscreen": true,
        "theme": "dark"
    },
    "weather": {
        "api_key": "YOUR_OPENWEATHERMAP_API_KEY",
        "city": "New York",
        "units": "metric"
    },
    "news": {
        "api_key": "YOUR_NEWSAPI_KEY",
        "source": "bbc-news"
    },
    "camera": {
        "device_id": 0,
        "width": 640,
        "height": 480,
        "use_oakd": false
    },
    "gestures": {
        "enabled": true,
        "sensitivity": 0.7,
        "smoothing": 0.5
    },
    "voice": {
        "enabled": true,
        "wake_word": "hey mirror",
        "porcupine_key": ""
    }
}
```

## Usage

### Gesture Control
1. **Point with index finger** - Cursor follows your finger within the widget area
2. **Pinch (thumb + index)** - Start dragging a widget
3. **Move while pinching** - Drag the widget
4. **Release pinch** - Drop the widget

### Voice Control
1. Say **"Hey Mirror"** followed by a command
2. Example: "Hey Mirror show weather"
3. The system will respond and focus the requested widget

### Widgets
- **Clock**: Shows current time and date
- **Weather**: Displays temperature and conditions
- **Calendar**: Shows upcoming events
- **News**: Scrolls through news headlines
- **Notes**: Text editor for quick notes (auto-saves)

## Architecture

### Technology Stack
- **UI Framework**: PyQt6 (migrated from Tkinter)
- **Hand Tracking**: MediaPipe
- **Computer Vision**: OpenCV
- **Voice Recognition**: SpeechRecognition + Porcupine (optional)
- **Text-to-Speech**: pyttsx3

### Key Components
- `main.py`: Application entry point
- `modules/gesture_controller.py`: Hand tracking and gesture recognition
- `modules/ui_manager.py`: UI management and widget coordination
- `modules/voice_controller.py`: Voice command processing
- `ui/draggable_widget.py`: Base class for draggable widgets
- `ui/virtual_cursor.py`: Virtual cursor overlay

## Autostart on Raspberry Pi

1. Copy the service file:
   ```bash
   sudo cp system/smart_mirror.service /etc/systemd/system/
   ```

2. Edit the service file to set the correct path:
   ```bash
   sudo nano /etc/systemd/system/smart_mirror.service
   ```

3. Reload and enable:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable smart_mirror.service
   sudo systemctl start smart_mirror.service
   ```

## Troubleshooting

### Camera Issues
- Check camera permissions
- Try different `device_id` values (0, 1, 2...)
- For OAK-D, ensure USB connection and drivers

### Gesture Not Working
- Ensure good lighting
- Keep hand within camera view
- Check camera is not blocked
- Adjust `sensitivity` in config.json

### Voice Commands Not Working
- Check microphone permissions
- Test microphone: `python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"`
- For Porcupine, ensure API key is set

### Widgets Not Dragging
- Ensure pinch gesture is detected (check console output)
- Try adjusting `pinch_threshold` in gesture_controller.py
- Ensure cursor is over widget when pinching

## Development

### Project Structure
```
smart_mirror/
├── main.py                 # Application entry
├── config.json             # Configuration
├── modules/                # Core modules
│   ├── gesture_controller.py
│   ├── ui_manager.py
│   ├── voice_controller.py
│   └── [services]
├── ui/                     # UI components
│   ├── virtual_cursor.py
│   ├── draggable_widget.py
│   └── components/
├── gestures/               # Gesture recognition
│   ├── camera.py
│   ├── gesture_recognizer.py
│   └── cursor_controller.py
└── system/                 # System files
```

## License

This project is open source. Feel free to modify and use as needed.

## Credits

- MediaPipe for hand tracking
- PyQt6 for UI framework
- OpenCV for computer vision
