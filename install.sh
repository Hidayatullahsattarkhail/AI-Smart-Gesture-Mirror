INSTALL_SCRIPT = """#!/bin/bash

echo "======================================"
echo "Smart Mirror Installation Script"
echo "======================================"

# Update system
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install Python dependencies
echo "Installing Python and pip..."
sudo apt-get install -y python3 python3-pip python3-tk

# Install OpenCV
echo "Installing OpenCV..."
sudo apt-get install -y python3-opencv

# Install DepthAI (OAK-D)
echo "Installing DepthAI SDK..."
pip3 install depthai

# Install MediaPipe
echo "Installing MediaPipe..."
pip3 install mediapipe

# Install other Python packages
echo "Installing additional packages..."
pip3 install requests anthropic Pillow

# Create project directory
echo "Setting up project directory..."
mkdir -p ~/smart-mirror
cd ~/smart-mirror

# Create config file
echo "Creating config file..."
cat > config.json << 'EOF'
{
    "weather": {
        "api_key": "YOUR_OPENWEATHERMAP_API_KEY",
        "location": {
            "lat": 33.6844,
            "lon": 73.0479,
            "name": "Islamabad"
        }
    },
    "news": {
        "api_key": "YOUR_NEWSAPI_KEY",
        "country": "us",
        "category": "general"
    },
    "calendar": {
        "source": "local",
        "file": "calendar_events.json"
    },
    "ai": {
        "api_key": "YOUR_ANTHROPIC_API_KEY",
        "model": "claude-sonnet-4-20250514"
    },
    "gesture": {
        "click_threshold": 0.05,
        "click_hold_time": 0.8,
        "smoothing_factor": 0.3,
        "enable_oak_d": true
    },
    "display": {
        "fullscreen": true,
        "width": 1920,
        "height": 1080
    }
}
EOF

# Create sample calendar file
cat > calendar_events.json << 'EOF'
{
    "events": [
        {
            "time": "09:00 AM",
            "title": "Morning Meeting",
            "duration": 60
        },
        {
            "time": "02:00 PM",
            "title": "Project Review",
            "duration": 30
        }
    ]
}
EOF

# Create systemd service
echo "Creating systemd service..."
sudo cat > /etc/systemd/system/smart-mirror.service << 'EOF'
[Unit]
Description=Smart Mirror Application
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/smart-mirror
Environment=DISPLAY=:0
ExecStart=/usr/bin/python3 /home/pi/smart-mirror/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Set permissions
sudo chmod 644 /etc/systemd/system/smart-mirror.service

echo "======================================"
echo "Installation complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Edit config.json with your API keys"
echo "2. Copy all Python files to ~/smart-mirror/"
echo "3. Enable service: sudo systemctl enable smart-mirror"
echo "4. Start service: sudo systemctl start smart-mirror"
echo "5. Check status: sudo systemctl status smart-mirror"
echo ""
echo "To start manually: cd ~/smart-mirror && python3 main.py"
echo "======================================"
"""

# Save install script
# with open('install.sh', 'w') as f:
#     f.write(INSTALL_SCRIPT)