"""Menu display and input handling for the CLI interface.

This module provides functions for displaying the main menu and
getting validated user input for menu choices.
"""

from .colors import BOLD, PRIMARY, MENU_NUMBER, ACCENT, SUCCESS, ERROR, WARNING, MUTED, RESET


def display_menu() -> None:
    """Display the main application menu with numbered options."""
    print(f"\n  {BOLD}{PRIMARY}+----------------------------------+{RESET}")
    print(f"  {BOLD}{PRIMARY}|{RESET}              {BOLD}MENU{RESET}                {BOLD}{PRIMARY}|{RESET}")
    print(f"  {BOLD}{PRIMARY}+----------------------------------+{RESET}")
    print(f"  {BOLD}{PRIMARY}|{RESET}                                  {BOLD}{PRIMARY}|{RESET}")
    print(f"  {BOLD}{PRIMARY}|{RESET}    {MENU_NUMBER}1.{RESET}  {SUCCESS}Add Task{RESET}                 {BOLD}{PRIMARY}|{RESET}")
    print(f"  {BOLD}{PRIMARY}|{RESET}    {MENU_NUMBER}2.{RESET}  {PRIMARY}View Tasks{RESET}               {BOLD}{PRIMARY}|{RESET}")
    print(f"  {BOLD}{PRIMARY}|{RESET}    {MENU_NUMBER}3.{RESET}  {ACCENT}Update Task{RESET}              {BOLD}{PRIMARY}|{RESET}")
    print(f"  {BOLD}{PRIMARY}|{RESET}    {MENU_NUMBER}4.{RESET}  {ERROR}Delete Task{RESET}              {BOLD}{PRIMARY}|{RESET}")
    print(f"  {BOLD}{PRIMARY}|{RESET}    {MENU_NUMBER}5.{RESET}  {SUCCESS}Mark Complete{RESET}            {BOLD}{PRIMARY}|{RESET}")
    print(f"  {BOLD}{PRIMARY}|{RESET}    {MENU_NUMBER}6.{RESET}  {MUTED}Exit{RESET}                     {BOLD}{PRIMARY}|{RESET}")
    print(f"  {BOLD}{PRIMARY}|{RESET}                                  {BOLD}{PRIMARY}|{RESET}")
    print(f"  {BOLD}{PRIMARY}+----------------------------------+{RESET}")
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
        choice = int(input(f"  {BOLD}{ACCENT}>>>{RESET} {MUTED}Enter your choice: {RESET}"))
        if choice < 1 or choice > 6:
            print(f"  {ERROR}Error:{RESET} Please enter a number between 1 and 6.")
            return -1
        return choice
    except ValueError:
        print(f"  {ERROR}Error:{RESET} Invalid input. Please enter a valid number.")
        return -1
    except (EOFError, KeyboardInterrupt):
        print(f"\n  {WARNING}Exiting application...{RESET}")
        return 6
