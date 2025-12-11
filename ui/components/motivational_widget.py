from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
import random

class MotivationalWidget(QLabel):
    """Immovable motivational message widget at top center"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Motivational messages
        self.messages = [
            "You're doing amazing! 🌟",
            "Believe in yourself! 💪",
            "Today is your day! ✨",
            "Stay positive! 😊",
            "You've got this! 🚀",
            "Keep smiling! 😄",
            "Be awesome today! ⭐",
            "You are unstoppable! 🔥",
            "Make it happen! 💫",
            "Dream big! 🌈",
            "Stay focused! 🎯",
            "You're a star! ⭐",
            "Shine bright! ✨",
            "Be kind to yourself! 💖",
            "You're incredible! 🌟"
        ]
        
        # Style - Red text, no background block
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                background-color: transparent;
                color: white;
                padding: 10px 20px;
                font-size: 28px;
                font-weight: bold;
                border: none;
            }
        """)
        
        font = QFont("Arial", 28, QFont.Weight.Bold)
        self.setFont(font)
        
        # Set initial message
        self.update_message()
        
        # Change message every 10 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_message)
        self.timer.start(10000)  # 10 seconds
    
    def update_message(self):
        """Update to a random motivational message"""
        message = random.choice(self.messages)
        self.setText(message)
        self.adjustSize()
