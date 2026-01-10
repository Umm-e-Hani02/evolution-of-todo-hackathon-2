"""Menu display and input handling for the CLI interface.

This module provides functions for displaying the main menu and
getting validated user input for menu choices.
"""

from .colors import BOLD, PINK, SECONDARY, ACCENT, SUCCESS, ERROR, WARNING, MUTED, BORDER, RESET


def display_menu() -> None:
    """Display the main application menu with numbered options."""
    print(f"\n  {BOLD}{PINK}Menu{RESET}")
    print(f"  {MUTED}{'-' * 20}{RESET}")
    print(f"  {SECONDARY}1){RESET} Add Task")
    print(f"  {ACCENT}2){RESET} View Tasks")
    print(f"  {WARNING}3){RESET} Update Task")
    print(f"  {ERROR}4){RESET} Delete Task")
    print(f"  {ACCENT}5){RESET} Mark Complete")
    print(f"  {MUTED}6){RESET} Exit")
    print(f"  {MUTED}{'-' * 20}{RESET}")
    print()


def get_menu_choice() -> int:
    """Prompt user for menu choice and validate input.

    Returns:
        Valid menu choice (1-6), or -1 if input is invalid

    Note:
        Returns -1 for invalid input to allow caller to re-prompt
        without raising exceptions in the menu loop.
    """
    try:
        choice = int(input(f"  {ACCENT}>{RESET} "))
        if choice < 1 or choice > 6:
            print(f"  {ERROR}Enter a number between 1-6{RESET}")
            return -1
        return choice
    except ValueError:
        print(f"  {ERROR}Enter a valid number{RESET}")
        return -1
    except (EOFError, KeyboardInterrupt):
        print(f"\n  {WARNING}Exiting...{RESET}")
        return 6
