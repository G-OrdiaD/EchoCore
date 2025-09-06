"""
Reminder data model
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Reminder:
    """Represents a reminder task"""
    task: str
    time_str: str
    id: Optional[int] = None
    created_at: Optional[str] = None

    def __str__(self):
        return f"{self.task} at {self.time_str}"