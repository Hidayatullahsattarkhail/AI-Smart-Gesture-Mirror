import webbrowser
import datetime
import os
from PyQt6.QtCore import QObject, pyqtSignal

class CommandProcessor(QObject):
    # Signals to update UI / UI update karne ke liye signals
    response_signal = pyqtSignal(str, str) # (User Text, Assistant Text)
    action_signal = pyqtSignal(str, object) # (Action Name, Data)

    def __init__(self, config, ai_assistant=None):
        super().__init__()
        self.config = config
        self.ai_assistant = ai_assistant
        
    def process(self, text):
        """Process user text and determine action / User ki baat samajhna"""
        text = text.lower().strip()
        print(f"DEBUG: Processing '{text}'")
        
        # 1. Greetings / Salam dua
        if any(word in text for word in ['hello', 'hi', 'hey']):
            self._respond(text, "Hello! How can I help you?", "HiMirror: Hello!")
            return

        # 2. Time & Date / Waqt aur Tareekh
        if 'time' in text:
            now = datetime.datetime.now().strftime("%I:%M %p")
            self._respond(text, f"It is currently {now}", f"Time: {now}")
            self.action_signal.emit('show_clock', None)
            return
            
        if 'date' in text or 'day' in text:
            now = datetime.datetime.now().strftime("%A, %B %d, %Y")
            self._respond(text, f"Today is {now}", f"Date: {now}")
            self.action_signal.emit('show_calendar', None)
            return

        # 3. Weather / Mausam
        if 'weather' in text or 'temperature' in text:
            self.action_signal.emit('show_weather', None)
            self._respond(text, "Checking the weather for you...", "Checking Weather...")
            return

        # 4. Website Commands / Websites kholna
        if 'open' in text:
            if 'youtube' in text:
                self._open_website("https://youtube.com", "Opening YouTube...")
                self._respond(text, "Opening YouTube", "Opening YouTube...")
                return
            elif 'google' in text:
                self._open_website("https://google.com", "Opening Google...")
                self._respond(text, "Opening Google", "Opening Google...")
                return
            elif 'news' in text:
                self.action_signal.emit('show_news', None)
                self._respond(text, "Here is the latest news", "Opening News...")
                return

        # 5. Smart Home (Mock) / Smart Home control
        if 'light' in text or 'lamp' in text:
            if 'on' in text:
                self._respond(text, "Turning on the lights", "Lights: ON")
            elif 'off' in text:
                self._respond(text, "Turning off the lights", "Lights: OFF")
            return

        # 6. Notes / Notes likhna aur parhna
        note_triggers = ['write note', 'add note', 'take note', 'note:']
        for trigger in note_triggers:
            if trigger in text:
                note_content = text.split(trigger, 1)[1].strip()
                if note_content:
                    self.action_signal.emit('add_note', note_content)
                    self._respond(text, "Note saved", "Note Saved")
                    return
                else:
                    self._respond(text, "What should I write?", "Empty Note")
                    return
        
        if 'show notes' in text or 'read notes' in text:
            self.action_signal.emit('read_notes', None)
            return
            
        # 7. Screen Context / Screen par kya hai
        if 'screen' in text or 'display' in text or 'showing' in text:
            context = (
                "The screen currently displays: "
                "1. A large Digital Clock with the current Time and Date. "
                "2. A Weather widget showing the local temperature and conditions. "
                "3. A News ticker at the top showing 'TODAY'S BIG NEWS'. "
                "4. A central area for Assistant interactions. "
            )
            # Ask AI to describe it naturally
            if self.ai_assistant:
                response = self.ai_assistant.process_query(f"User asked: '{text}'. Context: {context}. Answer naturally as Richard.")
                self._respond(text, response, response) # Show actual response, not placeholder
            else:
                self._respond(text, context, "Displaying Clock, Weather, News...")
            return

        # 7. AI Fallback / AI Jawab dega
        if text and self.ai_assistant:
            # Send to AI Assistant
            response = self.ai_assistant.process_query(text)
            self._respond(text, response, response) # Show actual response text
        elif text:
            self._respond(text, "I'm not sure how to help with that yet.", "Unknown Command")
    
    def _respond(self, user_text, speech_text, display_text):
        """Send response to UI and TTS / Jawab dena"""
        self.response_signal.emit(user_text, display_text)
        # We also want to speak it. 
        # The main controller will handle speaking based on 'response_signal' if needed, 
        # but usually we emit a specific speech request. 
        # For simplicty, let's assume the main loop handles speech queueing.
        return speech_text

    def _open_website(self, url, message):
        """Open a URL in default browser / Website kholna"""
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"Error opening website: {e}")
