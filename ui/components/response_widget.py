from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor, QPalette

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor, QPalette
from ui.draggable_widget import DraggableWidget

class ResponseWidget(DraggableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Setup Layout / Layout set karein
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # User Text Label (What user said) / User ki baat
        self.user_label = QLabel("")
        self.user_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.user_label.setStyleSheet("""
            QLabel {
                color: #AAAAAA;
                font-family: 'Arial';
                font-size: 24px;
                font-style: italic;
            }
        """)
        
        # Mirror Response Label (What mirror replies) / Mirror ka jawab
        self.mirror_label = QLabel("")
        self.mirror_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mirror_label.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-family: 'Arial';
                font-size: 32px;
                font-weight: bold;
                text-shadow: 0px 0px 10px rgba(0, 255, 255, 0.5);
            }
        """)
        
        layout.addWidget(self.user_label)
        layout.addWidget(self.mirror_label)
        self.setLayout(layout)
        
        # Timer to clear text / Text saaf karne ka timer
        self.clear_timer = QTimer()
        self.clear_timer.timeout.connect(self.clear_text)
        self.clear_timer.setSingleShot(True)
        
        self.hide() # Start hidden / Shuru mein chipa hua
        
    def show_response(self, user_text, mirror_text):
        """Display text with animation effect / Jawab dikhayein"""
        self.user_label.setText(f'"{user_text}"')
        self.mirror_label.setText(mirror_text)
        
        self.show()
        
        # Clear after 5 seconds / 5 second baad saaf karein
        self.clear_timer.start(5000)
        
    def clear_text(self):
        """Clear labels and hide / Text hatayein"""
        self.user_label.setText("")
        self.mirror_label.setText("")
        self.hide()
