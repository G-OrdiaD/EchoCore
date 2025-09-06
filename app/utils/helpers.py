"""
Helper functions for the application
"""

import re
from typing import Optional, Tuple


def validate_input(text: str, max_length: int = 500) -> str:
    """
    Validate and sanitize user input

    Args:
        text: Input text to validate
        max_length: Maximum allowed length

    Returns:
        Sanitized text
    """
    if not text or not isinstance(text, str):
        return ""

    # Remove potentially dangerous characters
    sanitized = text.strip()
    sanitized = re.sub(r'[;\\/*"\']', '', sanitized)

    # Limit length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]

    return sanitized


def format_time_display(time_str: str) -> str:
    """
    Format time string for consistent display

    Args:
        time_str: Raw time string

    Returns:
        Formatted time string
    """
    time_str = time_str.upper().strip()

    # Handle special cases
    if time_str == "NOON":
        return "12:00 PM"
    elif time_str == "MIDNIGHT":
        return "12:00 AM"

    # Parse numeric times
    time_patterns = [
        r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?",
        r"(\d{1,2})\s*(o'clock|oclock)?\s*(am|pm)?"
    ]

    for pattern in time_patterns:
        match = re.search(pattern, time_str, re.IGNORECASE)
        if match:
            hour = match.group(1)
            minute = match.group(2) or "00"
            period = match.group(3) or ""

            # Convert to consistent format
            hour_int = int(hour)
            if not period:
                period = "AM" if hour_int < 12 else "PM"
                if hour_int > 12:
                    hour_int -= 12

            return f"{hour_int}:{minute} {period.upper()}"

    return time_str  # Return as-is if we can't parse


def parse_voice_command(command: str) -> Optional[Tuple[str, str]]:
    """
    Parse voice command for reminder creation

    Args:
        command: Voice command text

    Returns:
        Tuple of (task, time) or None
    """
    command = command.lower().strip()

    patterns = [
        r"remind me to (.+?) at (.+)",
        r"remember to (.+?) at (.+)",
        r"set reminder for (.+?) at (.+)",
        r"create reminder for (.+?) at (.+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, command, re.IGNORECASE)
        if match:
            task = validate_input(match.group(1).strip(), 200)
            time_str = validate_input(match.group(2).strip(), 50)

            if task and time_str:
                return task, format_time_display(time_str)

    return None