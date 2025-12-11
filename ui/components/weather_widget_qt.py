from PyQt6.QtWidgets import QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from ui.draggable_widget import DraggableWidget

class WeatherWidget(DraggableWidget):
    def __init__(self, weather_service, parent=None):
        super().__init__(parent)
        self.weather_service = weather_service
        self.setFixedSize(300, 160)  # Increased size for better visibility
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)  # Increased spacing
        
        # Header
        header = QLabel("WEATHER")
        header.setAlignment(Qt.AlignmentFlag.AlignRight)
        header.setStyleSheet("color: #FFD700; font-size: 10pt; font-weight: bold; letter-spacing: 2px;")
        layout.addWidget(header)

        # Temperature label
        self.temp_label = QLabel("--°C")
        self.temp_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        font = QFont("Montserrat", 48, QFont.Weight.Bold) # Bigger font
        self.temp_label.setFont(font)
        self.temp_label.setStyleSheet("color: white; background: transparent;")
        layout.addWidget(self.temp_label)
        
        # Description label
        self.desc_label = QLabel("Loading...")
        self.desc_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        font = QFont("Montserrat", 16)
        self.desc_label.setFont(font)
        self.desc_label.setStyleSheet("color: #E0E0E0; background: transparent;")
        layout.addWidget(self.desc_label)
        
        self.setLayout(layout)
        
        self.update_weather()
    
    def update_weather(self):
        """Update weather display"""
        data = self.weather_service.get_current_weather()
        if data:
            self.temp_label.setText(f"{data['temp']}°C")
            self.desc_label.setText(f"{data['city']} - {data['condition']}")

