"""Elegant, minimal ANSI color codes for terminal output.

Uses a carefully curated palette that's easy on the eyes while
maintaining good readability and semantic meaning.
"""

# Reset
RESET = "\033[0m"

# Text styling
BOLD = "\033[1m"
DIM = "\033[2m"

# Soft pink theme for minimal professional CLI
PINK = "\033[38;5;205m"        # Soft pink (headers, titles, accents)
PINK_LIGHT = "\033[38;5;218m"  # Light pink (subtle highlights)
PINK_DARK = "\033[38;5;162m"   # Dark pink (emphasis)

# Secondary colors for balance
SECONDARY = "\033[38;5;252m"    # Light gray (menu options)
ACCENT = "\033[38;5;226m"       # Yellow (interactive prompts)

# Semantic colors for meaningful feedback
SUCCESS = "\033[38;5;46m"      # Green (success messages)
WARNING = "\033[38;5;220m"     # Orange-yellow (warnings)
ERROR = "\033[38;5;196m"       # Red (errors)
INFO = "\033[38;5;252m"        # Light gray (info)

# Neutral colors for hierarchy
TITLE = "\033[38;5;205m"       # Soft pink (main titles)
SUBTITLE = "\033[38;5;242m"    # Medium gray (subtitles)
MUTED = "\033[38;5;244m"       # Gray (muted text)
BORDER = "\033[38;5;240m"      # Dark gray (borders, lines)

# Task status colors
TASK_DONE = "\033[38;5;46m"    # Green (completed tasks)
TASK_PENDING = "\033[38;5;252m" # Light gray (pending tasks)

# Alternative accent colors
ACCENT_BLUE = "\033[38;5;33m"
ACCENT_CYAN = "\033[38;5;51m"
WHITE = "\033[38;5;255m"
BLACK = "\033[38;5;16m"

# Alternative accent colors for variety
ACCENT_BLUE = "\033[38;5;33m"  # Strong blue
ACCENT_PINK = "\033[38;5;205m" # Bright pink
ACCENT_CYAN = "\033[38;5;51m"  # Bright cyan

# Common aliases for convenience
RED = "\033[38;5;196m"         # Bright red
GREEN = "\033[38;5;46m"        # Bright green
YELLOW = "\033[38;5;226m"      # Bright yellow
BLUE = "\033[38;5;33m"         # Strong blue
MAGENTA = "\033[38;5;201m"     # Bright magenta
CYAN = "\033[38;5;51m"         # Bright cyan
WHITE = "\033[38;5;255m"       # Bright white
BLACK = "\033[38;5;16m"        # Black

# Background simulation using indentation and color blocks
BG_HEADER = "\033[38;5;22m"    # Dark green background simulation
BG_MENU = "\033[38;5;235m"     # Dark gray background simulation
