import threading
import time
import json
import os
import queue
import sys
import zipfile
import requests
from pathlib import Path
import pyaudio

try:
    from vosk import Model, KaldiRecognizer
    VOSK_AVAILABLE = True
except ImportError:
    VOSK_AVAILABLE = False

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

class VoiceController:
    def __init__(self, callback, config):
        self.callback = callback
        self.config = config
        
        # Audio configuration / Audio ki settings
        self.sample_rate = 16000
        self.chunk_size = 8096
        self.audio_queue = queue.Queue()
        
        # Initialize VOSK Model / VOSK model initialize karein
        self.model = None
        self.recognizer = None
        self.microphone_stream = None
        
        if VOSK_AVAILABLE:
            self._initialize_vosk()
        else:
            print("VOSK not installed. Voice control disabled.")
            print("VOSK install nahi hai. Awaaz control band hai.")

        # Initialize TTS / TTS start karein
        self.tts_engine = None
        if TTS_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                self.tts_engine.setProperty('rate', 150)
            except Exception as e:
                print(f"TTS initialization failed: {e}")
        
        # State management / State sambhalna
        self.running = False
        self.thread = None
        self.listening = False

    def _initialize_vosk(self):
        """Initialize VOSK model, downloading if necessary / VOSK model tayyar karein"""
        model_name = "vosk-model-small-en-us-0.15"
        model_path = Path(model_name)
        
        # Check if model exists / Check karein agar model majood hai
        if not model_path.exists():
            print(f"Downloading {model_name}...")
            print(f"{model_name} download ho raha hai...")
            self._download_model(model_name)
        
        try:
            print("Loading VOSK model... (Please wait)")
            print("VOSK model load ho raha hai... (Baraye meherbani intezaar karein)")
            self.model = Model(str(model_path))
            self.recognizer = KaldiRecognizer(self.model, self.sample_rate)
            print("✅ VOSK Model Loaded Successfully")
        except Exception as e:
            print(f"Failed to load VOSK model: {e}")
            print(f"VOSK model load karne mein nakami: {e}")

    def _download_model(self, model_name):
        """Download VOSK model from official server / VOSK model server se download karein"""
        url = f"https://alphacephei.com/vosk/models/{model_name}.zip"
        zip_path = f"{model_name}.zip"
        
        try:
            response = requests.get(url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            
            with open(zip_path, 'wb') as f:
                for data in response.iter_content(chunk_size=4096):
                    f.write(data)
            
            print("Extracting model...")
            print("Model unzip ho raha hai...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(".")
            
            os.remove(zip_path) # Clean up zip file
        except Exception as e:
            print(f"Error downloading model: {e}")

    def start(self):
        """Start voice listening thread / Awaaz sunne wala thread shuru karein"""
        if not self.model:
            print("No model loaded, voice disabled")
            return
            
        self.running = True
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop voice listening / Awaaz sunna band karein"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
    
    def speak(self, text):
        """Speak text using TTS / TTS ke zariye text bolein"""
        if self.tts_engine:
            try:
                # Run in separate thread to avoid blocking / Alag thread mein chalayein
                threading.Thread(target=self._speak_thread, args=(text,), daemon=True).start()
            except Exception as e:
                print(f"TTS error: {e}")
    
    def _speak_thread(self, text):
        """Thread implementation for speaking / Bolne ke liye thread implementation"""
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def _listen_loop(self):
        """Main listening loop using PyAudio and VOSK / PyAudio aur VOSK ka main loop"""
        p = pyaudio.PyAudio()
        
        try:
            stream = p.open(format=pyaudio.paInt16,
                          channels=1,
                          rate=self.sample_rate,
                          input=True,
                          frames_per_buffer=self.chunk_size)
        except Exception as e:
            print(f"Could not open microphone: {e}")
            print(f"Microphone khul nahi saka: {e}")
            return

        print("🎤 Voice listening active... (Use 'Hey Mirror')")
        print("🎤 Awaaz sunna shuru... ('Hey Mirror' bolein)")

        while self.running:
            try:
                data = stream.read(self.chunk_size, exception_on_overflow=False)
                
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get('text', '').lower()
                    
                    if text:
                        print(f"Heard: {text}") # Log sunii hui baat
                        self._process_command(text)
            
            except Exception as e:
                print(f"Error in listen loop: {e}")
                time.sleep(1)

        stream.stop_stream()
        stream.close()
        p.terminate()

    def _process_command(self, text):
        """Process detected voice commands / Awaaz se mile commands ko process karein"""
        
        # 1. Check if we are waiting for a command / Kya hum command ka intezaar kar rahe hain?
        if getattr(self, 'waiting_for_command', False):
            print(f"DEBUG: Context command received: '{text}'")
            self.waiting_for_command = False # Reset state
            self.callback('voice_command', {'text': text})
            return

        # 2. Wake word detection / Wake word pehchan
        wake_words = ['hi mirror', 'high mirror', 'hey mirror', 'hello mirror', 'mirror', 'himirror']
        
        identified_wake_word = None
        for ww in wake_words:
            if ww in text:
                identified_wake_word = ww
                break
        
        if identified_wake_word:
            # Wake word detected / Jaag gaya
            command = text.replace(identified_wake_word, '').strip()
            
            print(f"DEBUG: Wake Word '{identified_wake_word}' detected. Command part: '{command}'")
            
            if not command:
                # Wake word ONLY -> Enter conversation mode
                print("DEBUG: Standalone wake word. Asking for input.")
                self.speak("Yes, what can I help you?")
                self.waiting_for_command = True
                return

            # Wake word + Command -> Execute immediately
            self.callback('voice_command', {'text': command})
