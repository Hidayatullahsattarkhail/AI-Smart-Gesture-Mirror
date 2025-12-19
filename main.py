import sys
import json
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QObject, pyqtSignal
# Modules import / Modules ko import karein
from modules.ui_manager import UIManager
from modules.gesture_controller import GestureController
from modules.voice_controller import VoiceController
from modules.weather_service import WeatherService
from modules.news_service import NewsService
from modules.calendar_service import CalendarService
from modules.ai_assistant import AIAssistant
from modules.command_processor import CommandProcessor # Import CommandProcessor

class SmartMirror(QObject):
    gesture_signal = pyqtSignal(str, object)
    voice_signal = pyqtSignal(str, object) # Signal for voice events

    def __init__(self):
        super().__init__()
        
        # Load configuration / Config file load karein
        try:
            with open('config.json', 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            print("Error: config.json not found!")
            sys.exit(1)
        
        # Initialize Qt Application / Qt Application shuru karein
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Smart Mirror")
        
        # Connect signal to handler for thread safety
        self.gesture_signal.connect(self.on_gesture_event)
        self.voice_signal.connect(self.on_voice_event) # Connect voice signal
        
        screen = self.app.primaryScreen().geometry()
        self.screen_width = screen.width()
        self.screen_height = screen.height()
        
        # Initialize Services / Services shuru karein
        print("Initializing services...")
        self.weather_service = WeatherService(self.config)
        self.news_service = NewsService(self.config)
        self.calendar_service = CalendarService(self.config)
        self.ai_assistant = AIAssistant(self.config)
        
        # Initialize Command Processor / Command Processor shuru karein
        self.command_processor = CommandProcessor(self.config, self.ai_assistant, self.weather_service)
        self.command_processor.response_signal.connect(self.on_command_response)
        self.command_processor.action_signal.connect(self.on_command_action)
        
        # Initialize Gesture Control / Gesture control shuru karein
        print("Initializing gesture control...")
        self.gesture_controller = GestureController(
            self.screen_width,
            self.screen_height,
            self.gesture_signal.emit,
            self.config
        )
        
        # Initialize Voice Control / Awaaz control shuru karein
        print("Initializing voice control...")
        self.voice_controller = VoiceController(
            self.voice_signal.emit, # Use voice_signal.emit
            self.config
        )
        
        
        print("Initializing UI...")
        self.ui_manager = UIManager(
            self.screen_width,
            self.screen_height,
            self.weather_service,
            self.news_service,
            self.calendar_service,
            self.ai_assistant,
            self.gesture_controller
        )
        
        
        self.ui_manager.set_gesture_controller(self.gesture_controller)
        
        
        self.gesture_controller.start()
        
        
        self.voice_controller.start()
        
        
        if self.config.get('app', {}).get('fullscreen', True):
            self.ui_manager.show_fullscreen()
        else:
            self.ui_manager.show()
        
        print("Smart Mirror initialized successfully!")
        print("Press F11 to toggle fullscreen, ESC to exit")
    
    def on_gesture_event(self, event_type, data):
        """Handle gesture events from the gesture controller"""
        if event_type == 'cursor_move':
            self.ui_manager.update_cursor_position(data['x'], data['y'])
        
        elif event_type == 'pinch_start':
            self.ui_manager.handle_pinch_start(data['x'], data['y'])
        
        elif event_type == 'drag_start':
            self.ui_manager.handle_drag_start(
                data['x'], data['y'],
                data['start_x'], data['start_y']
            )
        
        elif event_type == 'drag_move':
            self.ui_manager.handle_drag_move(
                data['x'], data['y'],
                data['delta_x'], data['delta_y']
            )
        
        elif event_type == 'drag_end':
            self.ui_manager.handle_drag_end(data['x'], data['y'])
        
        elif event_type == 'click':
            self.ui_manager.handle_click(data['x'], data['y'])
        
        elif event_type == 'voice_command':
            action = data.get('action')
            if action == 'show_weather':
                # Focus weather widget
                if 'weather' in self.ui_manager.widgets:
                    self.ui_manager.widgets['weather'].raise_()
            elif action == 'show_clock':
                if 'clock' in self.ui_manager.widgets:
                    self.ui_manager.widgets['clock'].raise_()
            elif action == 'show_calendar':
                if 'calendar' in self.ui_manager.widgets:
                    self.ui_manager.widgets['calendar'].raise_()
            elif action == 'show_news':
                if 'news' in self.ui_manager.widgets:
                    self.ui_manager.widgets['news'].raise_()
            elif action == 'show_notes':
                if 'notes' in self.ui_manager.widgets:
                    self.ui_manager.widgets['notes'].raise_()
                    self.ui_manager.widgets['notes'].notes_text.setFocus()
    
    def run(self):
        """Start the application"""
        try:
            sys.exit(self.app.exec())
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            self.cleanup()
    
    def on_voice_event(self, event_type, data):
        """Handle voice events safely on main thread / Voice commands sambhalein"""
        if event_type == 'voice_command':
            text = data.get('text', '')
            if text:
                print(f"Processing command: {text}")
                self.command_processor.process(text)
    
    def on_command_response(self, user_text, mirror_text):
        """Handle response from command processor / Jawab dikhayein aur bolein"""
        self.ui_manager.show_response(user_text, mirror_text)
        self.voice_controller.speak(mirror_text)
    
    def on_command_action(self, action, data):
        """Handle metadata actions from command processor / Actions karein"""
        if action == 'show_weather':
             self.ui_manager.refresh_widgets()
        elif action == 'show_clock':
             pass # Already visible
        elif action == 'show_calendar':
             self.ui_manager.refresh_widgets()
        elif action == 'show_news':
             self.ui_manager.refresh_widgets()
        elif action == 'add_note':
             self.ui_manager.add_note(data)
        elif action == 'read_notes':
             notes = self.ui_manager.get_notes()
             self.voice_controller.speak(f"Here are your notes: {notes}")

    def cleanup(self):
        """Cleanup resources on exit"""
        if self.gesture_controller:
            self.gesture_controller.stop()
        if self.voice_controller:
            self.voice_controller.stop()
        print("Cleanup complete")

if __name__ == "__main__":
    try:
        app = SmartMirror()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
