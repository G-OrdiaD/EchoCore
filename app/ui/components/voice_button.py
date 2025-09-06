"""
Custom voice button component with visual feedback
"""

from kivy.uix.button import Button
from kivy.properties import BooleanProperty
from kivy.animation import Animation


class VoiceButton(Button):
    """Custom button for voice control with visual feedback"""

    is_listening = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Press to Speak'
        self.font_size = '36sp'
        self.background_color = (0, 0.6, 0, 1)
        self.color = (1, 1, 1, 1)
        self.bold = True
        self.bind(is_listening=self.on_listening_change)

    def on_listening_change(self, instance, value):
        """Handle listening state change"""
        if value:
            self.text = "Listening..."
            self.background_color = (0.8, 0, 0, 1)

            # Add pulsing animation
            self.anim = Animation(background_color=(0.9, 0.1, 0.1, 1), duration=0.5) + \
                        Animation(background_color=(0.8, 0, 0, 1), duration=0.5)
            self.anim.repeat = True
            self.anim.start(self)
        else:
            self.text = "Press to Speak"
            self.background_color = (0, 0.6, 0, 1)

            # Stop animation
            if hasattr(self, 'anim'):
                self.anim.stop(self)

    def set_listening(self, listening: bool):
        """Set the listening state"""
        self.is_listening = listening