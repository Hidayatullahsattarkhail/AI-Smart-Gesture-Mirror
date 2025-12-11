from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QPen

class DraggableWidget(QWidget):
    """Base class for draggable widgets"""
    
    
    position_changed = pyqtSignal(int, int)  
    drag_started = pyqtSignal()
    drag_ended = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        self.setMouseTracking(True)  
        
        
        self.is_dragging = False
        self.drag_offset = QPoint(0, 0)
        self.original_position = QPoint(0, 0)
        
        
        self.is_resizing = False
        self.resize_edge = None  
        self.resize_margin = 20  
        self.min_width = 200
        self.min_height = 100
        self.drag_start_pos = QPoint()
        
        
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 180);
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 30);
            }
            QWidget:hover {
                border: 1px solid rgba(255, 255, 255, 100);
            }
        """)

    def mousePressEvent(self, event):
        """Handle mouse press for resizing"""
        if event.button() == Qt.MouseButton.LeftButton:
            if self._is_on_resize_edge(event.pos()):
                self.is_resizing = True
                self.drag_start_pos = event.globalPosition().toPoint()
                self.original_size = self.size()
                event.accept()
            else:
                super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Handle mouse move for resizing and cursor updates"""
        pos = event.pos()
        
        if self.is_resizing:
            delta = event.globalPosition().toPoint() - self.drag_start_pos
            
            new_width = self.width()
            new_height = self.height()
            
            if self.resize_edge in ['right', 'bottom_right']:
                new_width = max(self.min_width, self.original_size.width() + delta.x())
            
            if self.resize_edge in ['bottom', 'bottom_right']:
                new_height = max(self.min_height, self.original_size.height() + delta.y())
            
            self.resize(new_width, new_height)
            event.accept()
            
        elif not self.is_dragging:
            # Update cursor based on position
            edge = self._get_resize_edge(pos)
            if edge == 'bottom_right':
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            elif edge == 'right':
                self.setCursor(Qt.CursorShape.SizeHorCursor)
            elif edge == 'bottom':
                self.setCursor(Qt.CursorShape.SizeVerCursor)
            else:
                self.setCursor(Qt.CursorShape.ArrowCursor)
            
            self.resize_edge = edge
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if self.is_resizing:
            self.is_resizing = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    def _get_resize_edge(self, pos):
        """Determine which edge the mouse is on"""
        w, h = self.width(), self.height()
        m = self.resize_margin
        
        on_right = w - m <= pos.x() <= w
        on_bottom = h - m <= pos.y() <= h
        
        if on_right and on_bottom:
            return 'bottom_right'
        elif on_right:
            return 'right'
        elif on_bottom:
            return 'bottom'
        return None

    def _is_on_resize_edge(self, pos):
        """Check if mouse is on a resize edge"""
        return self._get_resize_edge(pos) is not None

    def set_position(self, x, y):
        """Set widget position"""
        self.move(x, y)
        self.original_position = QPoint(x, y)
    
    def get_position(self):
        """Get widget position"""
        return self.pos()
    
    def start_drag(self, cursor_x, cursor_y):
        """Start dragging the widget"""
        if not self.is_dragging:
            self.is_dragging = True
            widget_pos = self.pos()
            self.drag_offset = QPoint(cursor_x - widget_pos.x(), cursor_y - widget_pos.y())
            self.drag_started.emit()
    
    def update_drag(self, cursor_x, cursor_y):
        """Update drag position"""
        if self.is_dragging:
            new_x = cursor_x - self.drag_offset.x()
            new_y = cursor_y - self.drag_offset.y()
            
            # Keep within parent bounds
            parent = self.parent()
            if parent:
                max_x = parent.width() - self.width()
                max_y = parent.height() - self.height()
                new_x = max(0, min(new_x, max_x))
                new_y = max(0, min(new_y, max_y))
            
            self.move(new_x, new_y)
            self.position_changed.emit(new_x, new_y)
    
    def end_drag(self):
        """End dragging"""
        if self.is_dragging:
            self.is_dragging = False
            self.drag_ended.emit()
    
    def contains_point(self, x, y):
        """Check if point is within widget bounds"""
        widget_pos = self.pos()
        return (widget_pos.x() <= x <= widget_pos.x() + self.width() and
                widget_pos.y() <= y <= widget_pos.y() + self.height())

    def paintEvent(self, event):
        """Custom paint for minimalist look"""
        super().paintEvent(event)
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw resize handle
        pen = QPen(QColor(255, 255, 255, 100), 2)
        painter.setPen(pen)
        w, h = self.width(), self.height()
        painter.drawLine(w - 15, h - 5, w - 5, h - 15)
        painter.drawLine(w - 10, h - 5, w - 5, h - 10)
        painter.drawLine(w - 5, h - 5, w - 5, h - 5)
        
        # Optional: Add subtle glow when dragging
        if self.is_dragging:
            pen = QPen(QColor(255, 255, 255, 100), 2)
            painter.setPen(pen)
            painter.drawRoundedRect(1, 1, self.width() - 2, self.height() - 2, 10, 10)

