"""
Text-to-speech functionality using pyttsx3
"""

import pyttsx3
from typing import Optional

class TextToSpeech:
    """Handles text-to-speech functionality"""

    def __init__(self):
        self.engine = None
        self.initialized = False

    def initialize(self) -> bool:
        """Initialize the TTS engine"""
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 130)
            self.engine.setProperty('volume', 1.0)
            self.initialized = True
            return True

        except Exception as e:
            print(f"Error initializing TTS: {e}")
            return False

    def speak(self, text: str):
        """Speak the given text"""
        if not self.initialized:
            print(f"TTS not available. Would speak: {text}")
            return

        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error speaking text: {e}")

    def cleanup(self):
        """Clean up TTS resources"""
        if self.initialized:
            try:
                self.engine.stop()
            except:
                pass