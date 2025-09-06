"""
Offline Voice Assistant - Main application entry point
"""

import os
import sys
from kivy.config import Config

# Set accessibility configuration
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '1000')
Config.set('graphics', 'minimum_width', '600')
Config.set('graphics', 'minimum_height', '800')
Config.set('kivy', 'exit_on_escape', '0')

# Add app directory to Python path (utils is inside app)
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Import from app.utils instead of utils
try:
    from app.utils.accessibility import set_high_contrast_theme
    UTILS_AVAILABLE = True
except ImportError as e:
    print(f"Utils module not found: {e}. Using fallback theme settings.")
    UTILS_AVAILABLE = False
    # Fallback function
    def set_high_contrast_theme():
        from kivy.core.window import Window
        Window.clearcolor = (0.1, 0.1, 0.1, 1)
        return {
            'background': (0.1, 0.1, 0.1, 1),
            'text': (1, 1, 1, 1),
            'primary': (0, 0.6, 0, 1),
            'accent': (0.8, 0, 0, 1)
        }

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder

# Load KV file
Builder.load_file('app/ui/main_screen.kv')

from app.ui.main_screen import MainScreen

class VoiceAssistantApp(App):
    """Main application class"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Voice Reminder Assistant"

    def build(self):
        """Build and return the root widget"""
        # Set high contrast theme
        set_high_contrast_theme()
        return MainScreen()

    def on_stop(self):
        """Clean up resources on application exit"""
        if hasattr(self.root, 'cleanup'):
            self.root.cleanup()

if __name__ == '__main__':
    VoiceAssistantApp().run()