"""
Utility functions and helpers for the application
"""

from .accessibility import set_high_contrast_theme, increase_touch_targets
from .helpers import validate_input, parse_voice_command
from .audio_recorder import AudioRecorder

__all__ = [
    'set_high_contrast_theme',
    'increase_touch_targets',
    'validate_input',
    'parse_voice_command',
    'AudioRecorder'
]