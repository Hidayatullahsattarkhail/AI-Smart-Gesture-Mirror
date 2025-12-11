from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt6.QtGui import QColor
from ui.virtual_cursor import VirtualCursor
from ui.components.clock_widget_qt import ClockWidget
from ui.components.weather_widget_qt import WeatherWidget
from ui.components.calendar_widget_qt import CalendarWidget
from ui.components.news_widget_qt import NewsWidget
from ui.components.notes_widget_qt import NotesWidget
from ui.components.motivational_widget import MotivationalWidget
from ui.components.response_widget import ResponseWidget
import json
import os

class UIManager(QMainWindow):
    def __init__(self, screen_width, screen_height, weather_service, news_service, 
                 calendar_service, ai_assistant, gesture_controller=None):
        super().__init__()
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.weather_service = weather_service
        self.news_service = news_service
        self.calendar_service = calendar_service
        self.ai_assistant = ai_assistant
        self.gesture_controller = gesture_controller
        
        # Widget positions file
        self.positions_file = "widget_positions.json"
        
        # Setup UI
        self.setWindowTitle("Smart Mirror")
        # Set background image (dark camo)
        # We use border-image to stretch/cover the background
        self.setStyleSheet("""
            QMainWindow {
                border-image: url(assets/background.png) 0 0 0 0 stretch stretch;
            }
        """)
        
        # Central widget (widget area)
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("background-color: transparent;")
        self.setCentralWidget(self.central_widget)
        
        # Virtual cursor
        self.cursor = VirtualCursor(self.central_widget)
        self.cursor.setGeometry(0, 0, screen_width, screen_height)
        self.cursor.show()
        
        # Widgets
        self.widgets = {}
        self.dragged_widget = None
        
        # Create widgets
        self._create_widgets()
        self._load_widget_positions()
        
        # Update timer for data refresh
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.refresh_widgets)
        self.update_timer.start(300000)  # 5 minutes
    
    def _create_widgets(self):
        """Create all widgets"""
        # Calculate center positions
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        # Total height of all widgets (approx) + spacing
        # Clock: 180, Weather: 160, Calendar: 200, Notes: 300
        # We'll stack them: Clock, Weather, Calendar, Notes
        
        # Clock widget
        clock = ClockWidget(self.central_widget)
        # Center X, Top of stack
        clock.set_position(center_x - 150, center_y - 400) 
        clock.position_changed.connect(lambda x, y: self._save_widget_position('clock', x, y))
        self.widgets['clock'] = clock
        clock.show()
        
        # Weather widget
        weather = WeatherWidget(self.weather_service, self.central_widget)
        weather.set_position(center_x - 150, center_y - 200)
        weather.position_changed.connect(lambda x, y: self._save_widget_position('weather', x, y))
        self.widgets['weather'] = weather
        weather.show()
        
        # Calendar widget (Restored as per user request)
        calendar = CalendarWidget(self.calendar_service, self.central_widget)
        calendar.set_position(center_x - 150, center_y)
        calendar.position_changed.connect(lambda x, y: self._save_widget_position('calendar', x, y))
        self.widgets['calendar'] = calendar
        calendar.show()
        
        # News widget
        news = NewsWidget(self.news_service, self.central_widget)
        news.set_position(20, 20) # Top-Left
        news.position_changed.connect(lambda x, y: self._save_widget_position('news', x, y))
        self.widgets['news'] = news
        news.show()
        
        # Notes widget
        notes = NotesWidget(self.central_widget)
        notes.set_position(center_x - 175, center_y + 220)
        notes.position_changed.connect(lambda x, y: self._save_widget_position('notes', x, y))
        self.widgets['notes'] = notes
        notes.show()
        
        # Motivational widget (Restored as per user request)
        motivational = MotivationalWidget(self.central_widget)
        motivational.move(self.screen_width // 2 - 200, 100) # Moved down slightly
        motivational.show()

        # Response Widget (New HiMirror feature) / Jawab dikhane wala widget
        self.response_widget = ResponseWidget(self.central_widget)
        # Position at bottom center (Full width)
        self.response_widget.setGeometry(0, self.screen_height - 180, self.screen_width, 150)
        self.widgets['response'] = self.response_widget
    
    def show_response(self, user_text, mirror_text):
        """Show response text on screen / Jawab screen par dikhayein"""
        if hasattr(self, 'response_widget'):
            self.response_widget.show_response(user_text, mirror_text)

    def add_note(self, text):
        """Add note to notes widget / Widget mein note daalien"""
        if 'notes' in self.widgets:
            self.widgets['notes'].add_note(text)
            
    def get_notes(self):
        """Get notes from widget / Widget se notes lein"""
        if 'notes' in self.widgets:
            return self.widgets['notes'].get_notes()
        return "No notes available."
    
    def _save_widget_position(self, widget_name, x, y):
        """Save widget position to file"""
        if os.path.exists(self.positions_file):
            try:
                with open(self.positions_file, 'r') as f:
                    positions = json.load(f)
            except:
                positions = {}
        else:
            positions = {}
        
        positions[widget_name] = {'x': x, 'y': y}
        
        try:
            with open(self.positions_file, 'w') as f:
                json.dump(positions, f)
        except Exception as e:
            print(f"Error saving widget positions: {e}")
    
    def _load_widget_positions(self):
        """Load widget positions from file"""
        if os.path.exists(self.positions_file):
            try:
                with open(self.positions_file, 'r') as f:
                    positions = json.load(f)
                
                for widget_name, pos in positions.items():
                    if widget_name in self.widgets:
                        self.widgets[widget_name].set_position(pos['x'], pos['y'])
            except Exception as e:
                print(f"Error loading widget positions: {e}")
    
    def update_cursor_position(self, x, y):
        """Update virtual cursor position"""
        self.cursor.set_position(x, y)
        self.cursor.show_cursor()
    
    def handle_click(self, x, y):
        """Handle click event"""
        # Check if click is on any widget
        for widget in self.widgets.values():
            if widget.contains_point(x, y):
                # Handle widget-specific click
                if isinstance(widget, NotesWidget):
                    widget.notes_text.setFocus()
                break
    
    def handle_pinch_start(self, x, y):
        """Handle pinch start - check if over a widget"""
        # Show pinch visual feedback
        self.cursor.set_pinching(True)
        
        for widget in self.widgets.values():
            if widget.contains_point(x, y):
                self.dragged_widget = widget
                widget.start_drag(x, y)
                break
    
    def handle_drag_start(self, x, y, start_x, start_y):
        """Handle drag start"""
        if self.dragged_widget:
            self.dragged_widget.start_drag(x, y)
    
    def handle_drag_move(self, x, y, delta_x, delta_y):
        """Handle drag movement"""
        if self.dragged_widget:
            self.dragged_widget.update_drag(x, y)
    
    def handle_drag_end(self, x, y):
        """Handle drag end"""
        # Hide pinch visual feedback
        self.cursor.set_pinching(False)
        
        if self.dragged_widget:
            self.dragged_widget.end_drag()
            self.dragged_widget = None
    
    def refresh_widgets(self):
        """Refresh all widget data"""
        if 'weather' in self.widgets:
            self.widgets['weather'].update_weather()
        if 'calendar' in self.widgets:
            self.widgets['calendar'].update_events()
        if 'news' in self.widgets:
            self.widgets['news'].fetch_news()
    
    def set_gesture_controller(self, gesture_controller):
        """Set gesture controller and update widget bounds"""
        self.gesture_controller = gesture_controller
        if gesture_controller:
            # Set widget bounds to central widget area
            gesture_controller.set_widget_bounds(
                0, 0, self.screen_width, self.screen_height
            )
    
    def show_fullscreen(self):
        """Show in fullscreen mode"""
        self.showFullScreen()
    
    def keyPressEvent(self, event):
        """Handle key presses"""
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        elif event.key() == Qt.Key.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        super().keyPressEvent(event)

