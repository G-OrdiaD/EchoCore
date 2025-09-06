"""
Speech-to-Text implementation using Vosk for offline speech recognition
"""

import threading
import queue
import json
import os
from typing import Optional, Callable

class VoiceRecognizer:
    """Handles offline voice recognition using Vosk"""

    def __init__(self, model_path: str = "model"):
        self.model_path = model_path
        self.is_listening = False
        self.recognizer = None
        self.mic = None
        self.stream = None
        self.audio_queue = queue.Queue()
        self.callback = None

    def initialize(self) -> bool:
        """Initialize the voice recognizer"""
        try:
            from vosk import Model, KaldiRecognizer
            import pyaudio

            if not os.path.exists(self.model_path):
                return False

            self.model = Model(self.model_path)
            self.recognizer = KaldiRecognizer(self.model, 16000)

            self.mic = pyaudio.PyAudio()
            self.stream = self.mic.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=8192
            )
            self.stream.stop_stream()

            return True

        except ImportError:
            return False
        except Exception as e:
            print(f"Error initializing voice recognizer: {e}")
            return False

    def start_listening(self, callback: Callable[[str], None]) -> bool:
        """Start listening for voice commands"""
        if not hasattr(self, 'recognizer') or not self.recognizer:
            return False

        self.callback = callback
        self.is_listening = True
        self.stream.start_stream()
        return True

    def stop_listening(self):
        """Stop listening for voice commands"""
        self.is_listening = False
        if self.stream:
            self.stream.stop_stream()

    def cleanup(self):
        """Clean up resources"""
        self.stop_listening()
        if self.stream:
            self.stream.close()
        if self.mic:
            self.mic.terminate()