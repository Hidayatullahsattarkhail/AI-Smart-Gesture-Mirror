from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from ui.draggable_widget import DraggableWidget

class CalendarWidget(DraggableWidget):
    def __init__(self, calendar_service, parent=None):
        super().__init__(parent)
        self.calendar_service = calendar_service
        self.setFixedSize(300, 200)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Title
        title = QLabel("Upcoming Events")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        font = QFont("Montserrat", 16, QFont.Weight.Bold)
        title.setFont(font)
        title.setStyleSheet("color: white; background: transparent;")
        layout.addWidget(title)
        
        # Events container
        self.events_container = QWidget()
        events_layout = QVBoxLayout()
        events_layout.setContentsMargins(0, 0, 0, 0)
        events_layout.setSpacing(5)
        self.events_container.setLayout(events_layout)
        layout.addWidget(self.events_container)
        
        self.setLayout(layout)
        
        self.update_events()
    
    def update_events(self):
        """Update calendar events"""
        events = self.calendar_service.get_events()
        
        # Clear existing events
        layout = self.events_container.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Add events
        font = QFont("Montserrat", 12)
        for event in events:
            event_label = QLabel(f"• {event['time']} - {event['title']}")
            event_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            event_label.setFont(font)
            event_label.setStyleSheet("color: rgba(255, 255, 255, 200); background: transparent;")
            layout.addWidget(event_label)

