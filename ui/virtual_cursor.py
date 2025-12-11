from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush

class VirtualCursor(QWidget):
    """Virtual cursor overlay that displays within the widget window"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        
        self.x = 0
        self.y = 0
        self.visible = True
        self.cursor_size = 40 
        self.cursor_color = QColor(0, 255, 255, 200)  # Cyan
        self.cursor_outline = QColor(255, 255, 255, 255)  # White
        self.is_pinching = False
        
    def set_position(self, x, y):
        """Update cursor position"""
        self.x = x
        self.y = y
        self.update()
    
    def set_pinching(self, pinching):
        """Set pinch state for visual feedback"""
        self.is_pinching = pinching
        self.update()
    
    def show_cursor(self):
        """Show the cursor"""
        self.visible = True
        self.update()
    
    def hide_cursor(self):
        """Hide the cursor"""
        self.visible = False
        self.update()
    
    def paintEvent(self, event):
        """Draw the cursor"""
        if not self.visible:
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # If pinching, make it bigger and change color
        if self.is_pinching:
            size = int(self.cursor_size * 1.5)  # 50% bigger when pinching
            outline_color = QColor(255, 0, 0, 255)  # Bright red when pinching
            fill_color = QColor(255, 100, 100, 255)  # Light red fill
        else:
            size = self.cursor_size
            outline_color = self.cursor_outline
            fill_color = self.cursor_color
        
        # Draw outer circle (outline) - thicker for visibility
        pen = QPen(outline_color, 4)
        painter.setPen(pen)
        painter.setBrush(QBrush(outline_color))
        painter.drawEllipse(
            int(self.x - size // 2),
            int(self.y - size // 2),
            size,
            size
        )
        
        # Draw inner circle (cursor)
        pen = QPen(fill_color, 2)
        painter.setPen(pen)
        painter.setBrush(QBrush(fill_color))
        inner_size = size - 8
        painter.drawEllipse(
            int(self.x - inner_size // 2),
            int(self.y - inner_size // 2),
            inner_size,
            inner_size
        )
        
        # Draw center dot - bigger for visibility
        painter.setBrush(QBrush(outline_color))
        dot_size = 8 if self.is_pinching else 6
        painter.drawEllipse(
            int(self.x - dot_size // 2),
            int(self.y - dot_size // 2),
            dot_size,
            dot_size
        )
        
        # Draw crosshair lines for better visibility
        if not self.is_pinching:
            pen = QPen(self.cursor_outline, 2)
            painter.setPen(pen)
            line_length = 15
            # Horizontal line
            painter.drawLine(
                int(self.x - line_length), int(self.y),
                int(self.x + line_length), int(self.y)
            )
            # Vertical line
            painter.drawLine(
                int(self.x), int(self.y - line_length),
                int(self.x), int(self.y + line_length)
            )

