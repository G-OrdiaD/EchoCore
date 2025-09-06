"""
Audio recording utilities for voice input
"""

import threading
import queue
import time
from typing import Optional, Callable


class AudioRecorder:
    """Handles audio recording for voice input"""

    def __init__(self):
        self.is_recording = False
        self.audio_queue = queue.Queue()
        self.callback = None
        self.recording_thread = None

    def start_recording(self, callback: Callable[[bytes], None]) -> bool:
        """Start audio recording"""
        try:
            import pyaudio

            self.callback = callback
            self.is_recording = True

            # Initialize audio recording
            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=1024,
                stream_callback=self._audio_callback
            )

            self.stream.start_stream()
            return True

        except ImportError:
            print("PyAudio not available for audio recording")
            return False
        except Exception as e:
            print(f"Error starting audio recording: {e}")
            return False

    def _audio_callback(self, in_data, frame_count, time_info, status):
        """Audio callback for recording"""
        if self.is_recording:
            self.audio_queue.put(in_data)
        return (in_data, self.audio.paContinue)

    def stop_recording(self):
        """Stop audio recording"""
        self.is_recording = False
        if hasattr(self, 'stream') and self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if hasattr(self, 'audio') and self.audio:
            self.audio.terminate()

    def cleanup(self):
        """Clean up recording resources"""
        self.stop_recording()