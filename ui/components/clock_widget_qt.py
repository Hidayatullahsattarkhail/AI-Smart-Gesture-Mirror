from PyQt6.QtWidgets import QLabel, QVBoxLayout
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont
from datetime import datetime
from ui.draggable_widget import DraggableWidget

class ClockWidget(DraggableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(300, 180)
       
        self.setStyleSheet("background-color: rgba(0, 0, 0, 100); border-radius: 15px;")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20) 
        
       
        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        font = QFont("Montserrat", 60, QFont.Weight.Light)  
        self.time_label.setFont(font)
        self.time_label.setStyleSheet("color: white; background: transparent;")
        layout.addWidget(self.time_label)
        
        
        self.date_label = QLabel()
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        font = QFont("Montserrat", 20) 
        self.date_label.setFont(font)
        self.date_label.setStyleSheet("color: rgba(255, 255, 255, 180); background: transparent;")
        layout.addWidget(self.date_label)
        
        self.setLayout(layout)
        
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)  
        
        self.update_clock()
    
    def update_clock(self):
        """Update clock display"""
        now = datetime.now()
        time_str = now.strftime("%H:%M")
        date_str = now.strftime("%A, %B %d, %Y")
        
        self.time_label.setText(time_str)
        self.date_label.setText(date_str)

