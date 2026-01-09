"""Elegant, minimal ANSI color codes for terminal output.

Uses a carefully curated palette that's easy on the eyes while
maintaining good readability and semantic meaning.
"""

# Reset
RESET = "\033[0m"

# Text styling
BOLD = "\033[1m"
DIM = "\033[2m"

# Primary palette - soft, modern colors
# These work well on both light and dark terminals
PRIMARY = "\033[38;5;75m"      # Soft blue-violet (headers, titles)
SECONDARY = "\033[38;5;110m"   # Soft purple (menu options)
ACCENT = "\033[38;5;109m"      # Soft teal (interactive prompts)

# Semantic colors - muted but clear
SUCCESS = "\033[38;5;77m"      # Soft green (success messages)
WARNING = "\033[38;5;214m"     # Warm orange (warnings)
ERROR = "\033[38;5;203m"       # Soft coral (errors)
INFO = "\033[38;5;110m"        # Soft purple (info)

# Neutral colors for hierarchy
TITLE = "\033[38;5;61m"        # Deep blue (main titles)
SUBTITLE = "\033[38;5;243m"    # Medium gray (subtitles)
MUTED = "\033[38;5;249m"       # Light gray (muted text)
BORDER = "\033[38;5;240m"      # Gray (borders, lines)

# Task status colors
TASK_DONE = "\033[38;5;77m"    # Soft green (completed tasks)
TASK_PENDING = "\033[38;5;246m" # Light gray (pending tasks)

# Alternative accent colors for variety
ACCENT_BLUE = "\033[38;5;68m"
ACCENT_PINK = "\033[38;5;175m"
ACCENT_CYAN = "\033[38;5;73m"

# Common aliases for convenience
RED = ERROR
GREEN = SUCCESS
YELLOW = WARNING
BLUE = ACCENT_BLUE
MAGENTA = "\033[38;5;146m"
CYAN = ACCENT_CYAN
WHITE = "\033[38;5;255m"
BLACK = "\033[38;5;16m"

# Background colors (light)
BG_SUCCESS = "\033[48;5;77m"
BG_ERROR = "\033[48;5;203m"
BG_WARNING = "\033[48;5;214m"
