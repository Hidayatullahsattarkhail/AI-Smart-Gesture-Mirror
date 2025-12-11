import cv2
import mediapipe as mp
import threading
import time
import math
from gestures.camera import CameraSystem


class GestureController:
    def __init__(self, screen_width, screen_height, callback, config):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.callback = callback
        self.config = config
        
        # Camera setup / Camera ki settings
        camera_config = config.get('camera', {})
        self.camera = CameraSystem(
            use_oakd=camera_config.get('use_oakd', False),
            width=camera_config.get('width', 640),
            height=camera_config.get('height', 480)
        )
        
        # MediaPipe setup / MediaPipe start karein
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # State management / State sambhalna
        self.running = False
        self.thread = None
        
        # Cursor state / Cursor ki halat
        self.cursor_x = screen_width // 2
        self.cursor_y = screen_height // 2
        self.prev_index_x = 0
        self.prev_index_y = 0
        
        # Pinch state machine / Pinch state machine
        self.pinch_state = 'idle'  # idle, pinching, dragging
        self.pinch_threshold = 50  # pixels distance
        self.dragged_widget = None
        self.drag_start_x = 0
        self.drag_start_y = 0
        
        # Smoothing / Smoothing factor
        self.smoothing_factor = config.get('gestures', {}).get('smoothing', 0.5)
        
        # Window bounds
        self.widget_bounds = {
            'x': 0,
            'y': 0,
            'width': screen_width,
            'height': screen_height
        }
    
    def set_widget_bounds(self, x, y, width, height):
        """Set the bounds of the widget area / Widget area ki hadood set karein"""
        self.widget_bounds = {'x': x, 'y': y, 'width': width, 'height': height}
    
    def _is_point_in_bounds(self, x, y):
        """Check if point is within widget bounds / Check karein kya point hadood mein hai"""
        return (self.widget_bounds['x'] <= x <= self.widget_bounds['x'] + self.widget_bounds['width'] and
                self.widget_bounds['y'] <= y <= self.widget_bounds['y'] + self.widget_bounds['height'])
    
    def _calculate_cursor_position(self, index_x, index_y, frame_width, frame_height):
        """Calculate cursor position from hand landmark / Cursor ki position hisaab karein"""
        # Normalize to 0-1 range
        normalized_x = 1.0 - (index_x / frame_width)
        normalized_y = index_y / frame_height
        
        # Map to screen coordinates
        screen_x = self.widget_bounds['x'] + (normalized_x * self.widget_bounds['width'])
        screen_y = self.widget_bounds['y'] + (normalized_y * self.widget_bounds['height'])
        
        # Apply smoothing
        self.cursor_x = self.cursor_x * (1 - self.smoothing_factor) + screen_x * self.smoothing_factor
        self.cursor_y = self.cursor_y * (1 - self.smoothing_factor) + screen_y * self.smoothing_factor
        
        # Clamp to bounds
        self.cursor_x = max(self.widget_bounds['x'], 
                           min(self.widget_bounds['x'] + self.widget_bounds['width'] - 1, self.cursor_x))
        self.cursor_y = max(self.widget_bounds['y'], 
                           min(self.widget_bounds['y'] + self.widget_bounds['height'] - 1, self.cursor_y))
        
        return self.cursor_x, self.cursor_y
    
    def _detect_pinch(self, hand_landmarks):
        """Detect pinch gesture / Pinch gesture pehchanein"""
        thumb = hand_landmarks.landmark[4]
        index = hand_landmarks.landmark[8]
        
        distance = math.sqrt(
            (thumb.x - index.x) ** 2 + (thumb.y - index.y) ** 2
        )
        
        pixel_distance = distance * 640
        is_pinching = pixel_distance < self.pinch_threshold
        return is_pinching, pixel_distance
    
    def start(self):
        """Start gesture tracking / Tracking shuru karein"""
        self.running = True
        self.thread = threading.Thread(target=self._track_loop, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop gesture tracking / Tracking band karein"""
        self.running = False
        if self.camera:
            self.camera.release()
        if self.thread:
            self.thread.join(timeout=2)
    
    def get_cursor_position(self):
        """Get current cursor position / Cursor ki mojuda jagah lein"""
        return {'x': int(self.cursor_x), 'y': int(self.cursor_y)}
    
    def _track_loop(self):
        """Main tracking loop / Bunyadi tracking loop"""
        while self.running:
            frame = self.camera.get_frame()
            if frame is None:
                # print("⚠️ No frame captured")
                time.sleep(0.01)
                continue
            
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            results = self.hands.process(frame_rgb)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self._process_hand(hand_landmarks, frame.shape)
            else:
                if self.pinch_state != 'idle':
                   self._reset_pinch_state()

            time.sleep(0.01)

    def _process_hand(self, hand_landmarks, frame_shape):
        """Process detected hand / Pakray gaye haath ko process karein"""
        index_tip = hand_landmarks.landmark[8]
        frame_height, frame_width = frame_shape[:2]
        
        cursor_x, cursor_y = self._calculate_cursor_position(
            index_tip.x * frame_width,
            index_tip.y * frame_height,
            frame_width,
            frame_height
        )
        
        if self._is_point_in_bounds(cursor_x, cursor_y):
            self.callback('cursor_move', {'x': int(cursor_x), 'y': int(cursor_y)})
            
            is_pinching, _ = self._detect_pinch(hand_landmarks)
            self._handle_pinch_state(is_pinching, cursor_x, cursor_y)
        else:
            self._reset_pinch_state()

    def _handle_pinch_state(self, is_pinching, cursor_x, cursor_y):
        """Manage pinch state transitions / Pinch state sambhalna"""
        if is_pinching and self.pinch_state == 'idle':
            self.pinch_state = 'pinching'
            self.drag_start_x = cursor_x
            self.drag_start_y = cursor_y
            self.callback('pinch_start', {'x': int(cursor_x), 'y': int(cursor_y)})
            print(f"✋ Pinch detected at ({int(cursor_x)}, {int(cursor_y)})")
            
        elif is_pinching and self.pinch_state == 'pinching':
            move_distance = math.sqrt(
                (cursor_x - self.drag_start_x) ** 2 + 
                (cursor_y - self.drag_start_y) ** 2
            )
            if move_distance > 10:
                self.pinch_state = 'dragging'
                self.callback('drag_start', {
                    'x': int(cursor_x),
                    'y': int(cursor_y),
                    'start_x': int(self.drag_start_x),
                    'start_y': int(self.drag_start_y)
                })
                
        elif is_pinching and self.pinch_state == 'dragging':
            self.callback('drag_move', {
                'x': int(cursor_x),
                'y': int(cursor_y),
                'delta_x': int(cursor_x - self.drag_start_x),
                'delta_y': int(cursor_y - self.drag_start_y)
            })
            
        elif not is_pinching and self.pinch_state != 'idle':
            was_dragging = (self.pinch_state == 'dragging')
            self.pinch_state = 'idle'
            self.dragged_widget = None
            
            if was_dragging:
                self.callback('drag_end', {'x': int(cursor_x), 'y': int(cursor_y)})
                print(f"👆 Pinch released after drag")
            else:
                self.callback('click', {'x': int(cursor_x), 'y': int(cursor_y)})
                print(f"👆 Pinch released (click)")

    def _reset_pinch_state(self):
        """Reset pinch state safely / Pinch state reset karein"""
        if self.pinch_state != 'idle':
            self.pinch_state = 'idle'
            self.dragged_widget = None
            self.callback('drag_end', {'x': int(self.cursor_x), 'y': int(self.cursor_y)})
