"""
Main screen UI for the voice assistant application
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty, BooleanProperty, ListProperty
from kivy.clock import Clock

from app.core.voice_recognizer import VoiceRecognizer
from app.core.text_to_speech import TextToSpeech
from app.core.database import DatabaseManager
from app.core.voice_parser import VoiceCommandParser
from app.ui.components.voice_button import VoiceButton
from app.ui.components.reminder_list import ReminderList
from app.utils.helpers import validate_input, parse_voice_command
from app.utils.accessibility import increase_touch_targets

class MainScreen(BoxLayout):
    """Main screen of the application"""

    status_text = StringProperty("Ready to listen")
    is_listening = BooleanProperty(False)
    reminders = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 20
        self.padding = 30

        # Initialize services
        self.voice_recognizer = VoiceRecognizer()
        self.tts = TextToSpeech()
        self.db = DatabaseManager()
        self.parser = VoiceCommandParser()

        # Create UI
        self._create_ui()

        # Initialize components
        self.initialize_services()

        # Load existing reminders
        Clock.schedule_once(lambda dt: self.load_reminders(), 0.1)

    def _create_ui(self):
        """Create the user interface with components"""
        # Title
        title = Label(
            text="Voice Reminder Assistant",
            font_size='40sp',
            size_hint_y=0.15,
            color=(1, 1, 1, 1),
            bold=True
        )
        self.add_widget(title)

        # Use VoiceButton component
        self.voice_button = VoiceButton(
            size_hint_y=0.2
        )
        self.voice_button.bind(on_press=self.toggle_listening)
        increase_touch_targets(self.voice_button, 1.3)
        self.add_widget(self.voice_button)

        # Status label
        self.status_label = Label(
            text=self.status_text,
            font_size='32sp',
            size_hint_y=0.1,
            color=(1, 1, 1, 1),
            halign='center'
        )
        self.add_widget(self.status_label)

        # Reminders list title
        reminders_title = Label(
            text='Your Reminders:',
            font_size='36sp',
            size_hint_y=0.1,
            color=(1, 1, 1, 1),
            bold=True
        )
        self.add_widget(reminders_title)

        # Use ReminderList component
        self.reminder_list = ReminderList(
            size_hint_y=0.45
        )
        self.add_widget(self.reminder_list)

    def initialize_services(self):
        """Initialize all services with error handling"""
        # Initialize TTS first for audio feedback
        if not self.tts.initialize():
            self.status_text = "Text-to-speech not available"
            self.tts.speak("Text to speech is not available. Please check your installation.")

        # Initialize voice recognition
        if not self.voice_recognizer.initialize():
            self.status_text = "Voice recognition not available"
            self.voice_button.disabled = True
            self.tts.speak("Voice recognition is not available. Please install Vosk and ensure the model is downloaded.")

    def toggle_listening(self):
        """Toggle voice listening state"""
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening()

    def start_listening(self):
        """Start listening for voice commands"""
        self.is_listening = True
        self.voice_button.set_listening(True)
        self.status_label.text = "Listening... Speak now"

        # Start voice recognition
        success = self.voice_recognizer.start_listening(self.process_voice_command)

        if success:
            self.tts.speak("I'm listening. Please say your reminder.")
        else:
            self.status_text = "Failed to start listening"
            self.is_listening = False
            self.voice_button.set_listening(False)

    def stop_listening(self):
        """Stop listening for voice commands"""
        self.is_listening = False
        self.voice_button.set_listening(False)
        self.status_text = "Ready to listen"
        self.voice_recognizer.stop_listening()

    def process_voice_command(self, command: str):
        """Process voice command in UI thread"""
        Clock.schedule_once(lambda dt: self._process_command_ui(command))

    def _process_command_ui(self, command: str):
        """Process voice command with full pipeline"""
        self.status_text = f"Heard: {command}"

        # Parse the command using helper function
        result = parse_voice_command(command)
        if not result:
            # Fallback to the voice parser
            result = self.parser.parse_reminder_command(command)

        if result:
            task, time_str = result

            # Validate inputs
            task = validate_input(task, 200)
            time_str = validate_input(time_str, 50)

            if not task or not time_str:
                error_msg = "Please provide a valid task and time"
                self.tts.speak(error_msg)
                self.status_text = error_msg
                self.stop_listening()
                return

            # Add to database
            reminder_id = self.db.add_reminder(task, time_str)

            if reminder_id:
                confirmation = f"Okay, I'll remind you to {task} at {time_str}"
                self.tts.speak(confirmation)
                self.status_text = confirmation
                self.load_reminders()
            else:
                error_msg = "Sorry, I couldn't save that reminder"
                self.tts.speak(error_msg)
                self.status_text = error_msg
        else:
            error_msg = "I didn't understand. Please say something like: Remind me to take medicine at 10 AM"
            self.tts.speak(error_msg)
            self.status_text = "Please try again"

        self.stop_listening()

    def load_reminders(self):
        """Load and display reminders from database"""
        self.reminders = self.db.get_all_reminders()
        self._update_reminders_display()

    def _update_reminders_display(self):
        """Update the reminders display using the ReminderList component"""
        self.reminder_list.update_reminders(self.reminders)

    def cleanup(self):
        """Clean up all resources"""
        self.voice_recognizer.cleanup()
        self.tts.cleanup()