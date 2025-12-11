README = """# Smart Mirror Platform

A full-featured smart mirror with AI assistant and gesture control for Raspberry Pi 4.

## Features

- 🕐 **Real-time Clock & Date Display**
- 🌤️ **Live Weather Information**
- 📰 **News Headlines**
- 📅 **Calendar Integration**
- 🤖 **AI Assistant** (powered by Claude)
- 👋 **Hand Gesture Control** (OAK-D + MediaPipe)
- 🖱️ **Touchless Cursor & Click**
- 🎨 **Mirror-Friendly Dark Theme**

## Hardware Requirements

- Raspberry Pi 4 (4GB+ RAM recommended)
- OAK-D Camera (Luxonis)
- HDMI Display
- Two-way mirror glass (optional)
- Micro SD Card (32GB+)

## Software Stack

- **Frontend**: Python 3, Tkinter
- **Gesture Control**: OAK-D DepthAI SDK, MediaPipe Hands, OpenCV
- **Backend**: Python APIs (Weather, News, Calendar)
- **AI**: Anthropic Claude API
- **OS**: Raspberry Pi OS

## Installation

### Quick Install (Raspberry Pi)

```bash
# Download and run installation script
curl -O https://raw.githubusercontent.com/yourrepo/smart-mirror/main/install.sh
chmod +x install.sh
./install.sh
```

### Manual Installation

1. **Install System Dependencies**
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-tk python3-opencv
```

2. **Install Python Packages**
```bash
pip3 install -r requirements.txt
```

3. **Install OAK-D SDK**
```bash
pip3 install depthai
```

4. **Configure API Keys**

Edit `config.json`:
```json
{
    "weather": {
        "api_key": "your-openweathermap-key"
    },
    "news": {
        "api_key": "your-newsapi-key"
    },
    "ai": {
        "api_key": "your-anthropic-key"
    }
}
```

Get API keys from:
- Weather: https://openweathermap.org/api
- News: https://newsapi.org
- AI: https://console.anthropic.com

## Usage

### Run Manually
```bash
python3 main.py
```

### Auto-start on Boot
```bash
# Enable service
sudo systemctl enable smart-mirror

# Start service
sudo systemctl start smart-mirror

# Check status
sudo systemctl status smart-mirror
```

### Gesture Controls

- **Move Hand**: Move cursor
- **Pinch (Thumb + Index)**: Click (hold for 0.8s)
- **Swipe Left/Right**: Navigate screens
- **Swipe Up/Down**: Scroll content

### Keyboard Shortcuts

- `ESC`: Exit application
- `F11`: Toggle fullscreen

## Project Structure

```
smart-mirror/
├── main.py                      # Application entry point
├── modules/
│   ├── ui_manager.py           # Tkinter UI management
│   ├── gesture_controller.py   # OAK-D + MediaPipe gestures
│   ├── weather_service.py      # Weather API integration
│   ├── news_service.py         # News API integration
│   ├── calendar_service.py     # Calendar management
│   └── ai_assistant.py         # AI chatbot integration
├── config.json                  # Configuration file
├── calendar_events.json         # Local calendar data
├── requirements.txt             # Python dependencies
├── install.sh                   # Installation script
└── README.md                    # Documentation
```

## Configuration

### Display Settings
```json
"display": {
    "fullscreen": true,
    "width": 1920,
    "height": 1080
}
```

### Gesture Settings
```json
"gesture": {
    "click_threshold": 0.05,      // Pinch distance for click
    "click_hold_time": 0.8,       // Hold time in seconds
    "smoothing_factor": 0.3,      // Cursor smoothing (0-1)
    "enable_oak_d": true          // Use OAK-D camera
}
```

### Location Settings
```json
"weather": {
    "location": {
        "lat": 33.6844,
        "lon": 73.0479,
        "name": "Islamabad"
    }
}
```

## Customization

### Adding Custom Widgets

1. Create widget function in `ui_manager.py`
2. Add to `create_home_screen()` method
3. Update in `refresh_widgets()` method

### Custom Gestures

1. Add gesture detection in `gesture_controller.py`
2. Handle in `process_hand_landmarks()` method
3. Trigger callback with event type

### Styling

Modify colors in `ui_manager.py`:
```python
self.colors = {
    'bg': '#000000',
    'fg': '#FFFFFF',
    'accent': '#4A90E2',
    'widget_bg': '#1A1A1A'
}
```

## Troubleshooting

### Camera Not Detected
```bash
# Check OAK-D connection
python3 -c "import depthai as dai; print(dai.Device.getAllAvailableDevices())"
```

### Service Won't Start
```bash
# Check logs
sudo journalctl -u smart-mirror -f
```

### Gesture Control Not Working
- Ensure good lighting conditions
- Check camera positioning
- Adjust gesture thresholds in config.json

## Development

### Windows Development
```bash
# Use regular webcam for testing
# OAK-D features will fallback to standard camera
python main.py
```

### Testing Without Camera
Comment out camera initialization in `gesture_controller.py`

## Performance Tips

- Use lightweight widgets
- Reduce API polling frequency
- Optimize image processing resolution
- Enable GPU acceleration (Raspberry Pi 4)

## License

MIT License - See LICENSE file

## Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create pull request

## Support

- GitHub Issues: Report bugs
- Documentation: Full API docs
- Community: Discord server

## Credits

- OAK-D: Luxonis
- MediaPipe: Google
- Claude API: Anthropic
- Weather: OpenWeatherMap
- News: NewsAPI

---

Built with ❤️ for the maker community
"""

# Save README
# with open('README.md', 'w') as f:
#     f.write(README)