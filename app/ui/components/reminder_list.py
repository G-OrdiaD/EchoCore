"""
Component for displaying a list of reminders
"""

from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.core.window import Window


class ReminderList(ScrollView):
    """Scrollable list of reminders with accessibility features"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.do_scroll_x = False
        self.do_scroll_y = True
        self.bar_width = '15dp'
        self.bar_color = (0.7, 0.7, 0.7, 0.6)
        self.bar_inactive_color = (0.7, 0.7, 0.7, 0.2)

        # Create container for reminders
        self.container = GridLayout(
            cols=1,
            size_hint_y=None,
            spacing='10dp',
            padding='10dp'
        )
        self.container.bind(minimum_height=self.container.setter('height'))
        self.add_widget(self.container)

    def update_reminders(self, reminders):
        """Update the list with current reminders"""
        self.container.clear_widgets()

        if not reminders:
            # Show message if no reminders
            no_reminders = Label(
                text="No reminders yet.\nSay 'Remind me to [task] at [time]' to create one.",
                font_size='28sp',
                size_hint_y=None,
                height=120,
                color=(0.8, 0.8, 0.8, 1),
                text_size=(Window.width - 60, None),
                halign='center',
                valign='middle'
            )
            no_reminders.bind(texture_size=no_reminders.setter('size'))
            self.container.add_widget(no_reminders)
            return

        # Add each reminder to the list
        for reminder in reminders:
            reminder_text = f"{reminder.task} at {reminder.time_str}"
            reminder_label = Label(
                text=reminder_text,
                font_size='28sp',
                size_hint_y=None,
                height=80,
                color=(1, 1, 1, 1),
                text_size=(Window.width - 60, None),
                halign='left',
                valign='middle'
            )
            reminder_label.bind(texture_size=reminder_label.setter('size'))
            self.container.add_widget(reminder_label)