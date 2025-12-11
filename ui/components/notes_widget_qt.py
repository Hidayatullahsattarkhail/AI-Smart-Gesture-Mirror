from PyQt6.QtWidgets import QLabel, QVBoxLayout, QTextEdit, QPushButton
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from ui.draggable_widget import DraggableWidget
import json
import os

class NotesWidget(DraggableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(350, 300)
        self.notes_file = "notes.json"
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Title
        title = QLabel("Notes")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        font = QFont("Montserrat", 16, QFont.Weight.Bold)
        title.setFont(font)
        title.setStyleSheet("color: white; background: transparent;")
        layout.addWidget(title)
        
        # Notes text area
        self.notes_text = QTextEdit()
        self.notes_text.setStyleSheet("""
            QTextEdit {
                background-color: rgba(20, 20, 20, 200);
                color: white;
                border: 1px solid rgba(255, 255, 255, 50);
                border-radius: 5px;
                padding: 10px;
                font-family: 'Montserrat';
                font-size: 14px;
            }
        """)
        self.notes_text.setPlaceholderText("Tap to add notes...")
        layout.addWidget(self.notes_text)
        
        # Save button (minimalist)
        self.save_btn = QPushButton("Save")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 30);
                color: white;
                border: 1px solid rgba(255, 255, 255, 50);
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 50);
            }
        """)
        self.save_btn.clicked.connect(self.save_notes)
        layout.addWidget(self.save_btn)
        
        self.setLayout(layout)
        
        # Load notes
        self.load_notes()
        
        # Auto-save timer
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.save_notes)
        self.auto_save_timer.start(30000)  # Auto-save every 30 seconds
    
    def load_notes(self):
        """Load notes from file"""
        if os.path.exists(self.notes_file):
            try:
                with open(self.notes_file, 'r') as f:
                    data = json.load(f)
                    self.notes_text.setPlainText(data.get('notes', ''))
            except Exception as e:
                print(f"Error loading notes: {e}")
    
    def save_notes(self):
        """Save notes to file"""
        try:
            data = {'notes': self.notes_text.toPlainText()}
            with open(self.notes_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving notes: {e}")

    def add_note(self, text):
        """Add a new note programmatically / Naya note shamil karein"""
        current_text = self.notes_text.toPlainText()
        if current_text:
            new_text = f"{current_text}\n- {text}"
        else:
            new_text = f"- {text}"
        self.notes_text.setPlainText(new_text)
        self.save_notes()
        print(f"DEBUG: Note added: {text}")

    def get_notes(self):
        """Get all notes / Tamam notes wapis layein"""
        return self.notes_text.toPlainText()
