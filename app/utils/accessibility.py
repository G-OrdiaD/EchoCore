"""
Accessibility utilities for the application
"""

from kivy.core.window import Window


def set_high_contrast_theme():
    """Set high contrast colors for better visibility"""
    # Dark background with light text
    Window.clearcolor = (0.1, 0.1, 0.1, 1)

    # Return color palette for consistency
    return {
        'background': (0.1, 0.1, 0.1, 1),
        'text': (1, 1, 1, 1),
        'primary': (0, 0.6, 0, 1),
        'accent': (0.8, 0, 0, 1),
        'secondary': (0.8, 0.8, 0.8, 1)
    }


def increase_touch_targets(widget, multiplier=1.5):
    """
    Increase touch target size for better accessibility

    Args:
        widget: The widget to modify
        multiplier: Size multiplier for touch targets
    """
    if hasattr(widget, 'height'):
        widget.height = widget.height * multiplier
    if hasattr(widget, 'width') and not hasattr(widget, 'size_hint_x'):
        widget.width = widget.width * multiplier


def get_accessible_font_sizes():
    """Get font sizes optimized for elderly users"""
    return {
        'xlarge': '40sp',
        'large': '36sp',
        'medium': '32sp',
        'small': '28sp'
    }