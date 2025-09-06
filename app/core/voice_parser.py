"""
Voice command parsing and processing
"""

import re
from typing import Optional, Tuple, List

class VoiceCommandParser:
    """Parses voice commands from STT output"""

    def __init__(self):
        self.command_patterns = [
            r"remind me to (.+?) at (.+)",
            r"remember to (.+?) at (.+)",
            r"set reminder for (.+?) at (.+)",
            r"create reminder for (.+?) at (.+)"
        ]

    def parse_reminder_command(self, command: str) -> Optional[Tuple[str, str]]:
        """
        Parse a voice command to extract task and time

        Args:
            command: Raw text from STT

        Returns:
            Tuple of (task, time) or None if parsing failed
        """
        command = command.lower().strip()

        for pattern in self.command_patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                task = match.group(1).strip()
                time_str = match.group(2).strip()
                return task, time_str

        return None

    def get_help_examples(self) -> List[str]:
        """Get example voice commands for user guidance"""
        return [
            "Remind me to take medicine at 10 AM",
            "Remember to call doctor at 3 PM",
            "Set reminder for watering plants at 9 AM",
            "Create reminder to take walk at 5 PM"
        ]