"""Modern, professional ANSI color codes for terminal output.

A cohesive color palette designed for excellent readability and
visual hierarchy in CLI applications.
"""

# Reset and styling
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"

# Primary brand colors - Modern blue/cyan palette
PRIMARY = "\033[38;5;39m"       # Vibrant blue (main brand color)
PRIMARY_LIGHT = "\033[38;5;117m"  # Light blue (subtle highlights)
PRIMARY_DARK = "\033[38;5;27m"    # Deep blue (emphasis)

# Accent color for interactive elements
ACCENT = "\033[38;5;214m"       # Warm orange (prompts, highlights)

# Semantic colors with improved contrast
SUCCESS = "\033[38;5;42m"       # Bright green (success, completed)
WARNING = "\033[38;5;220m"      # Amber (warnings, caution)
ERROR = "\033[38;5;196m"        # Bright red (errors, delete)
INFO = "\033[38;5;117m"         # Light blue (informational)

# Neutral hierarchy colors
TITLE = "\033[38;5;39m"         # Vibrant blue (main titles)
SUBTITLE = "\033[38;5;250m"     # Light gray (subtitles)
MUTED = "\033[38;5;243m"        # Medium gray (muted text)
BORDER = "\033[38;5;240m"       # Dark gray (borders, separators)

# Text colors for content
TEXT_PRIMARY = "\033[38;5;255m"   # White (primary text)
TEXT_SECONDARY = "\033[38;5;250m" # Light gray (secondary text)
MENU_NUMBER = "\033[38;5;67m"     # Soft blue-gray (menu numbers)

# Task status colors
TASK_DONE = "\033[38;5;42m"     # Bright green (completed)
TASK_PENDING = "\033[38;5;250m" # Light gray (pending)

# Legacy aliases for backward compatibility
PINK = PRIMARY                   # Map old pink to new primary
SECONDARY = TEXT_SECONDARY       # Map old secondary to text secondary
