"""Main application entry point for the Todo CLI.

This module contains the main loop and application initialization logic,
coordinating the menu system, user input, and command handlers.
"""

import signal
import sys

from .services.todo_service import TodoService
from .cli.menu import display_menu, get_menu_choice
from .cli.handlers import (
    handle_add_task,
    handle_view_tasks,
    handle_update_task,
    handle_delete_task,
    handle_mark_complete,
)
from .cli.colors import BOLD, PINK, SUCCESS, WARNING, MUTED, SUBTITLE, RESET


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully.

    Args:
        sig: Signal number
        frame: Current stack frame

    Note:
        This ensures the application exits cleanly when interrupted.
    """
    print(f"\n\n{SUCCESS}Thank you for using Todo Application!{RESET}")
    print(f"  {WARNING}Data will be lost when the program exits.{RESET}")
    print(f"\n  {SUBTITLE}Goodbye!{RESET}")
    print()
    sys.exit(0)


def main() -> None:
    """Main application loop.

    Initializes the TodoService, displays welcome message, and runs
    the main menu loop handling user commands until exit is chosen.
    """
    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Display welcome message
    print(f"\n  {BOLD}{PINK}Todo Application{RESET}  {SUBTITLE}In-Memory Todo Manager{RESET}")
    print(f"  {MUTED}{'-' * 45}{RESET}")
    print(f"  {BOLD}Welcome!{RESET}")
    print(f"  {MUTED}Tasks are stored in memory only and will be lost on exit.{RESET}")
    print()

    # Initialize service
    service = TodoService()

    # Main application loop
    while True:
        display_menu()
        choice = get_menu_choice()

        # Handle invalid input - re-prompt
        if choice == -1:
            continue

        # Dispatch to appropriate handler
        if choice == 1:
            handle_add_task(service)
        elif choice == 2:
            handle_view_tasks(service)
        elif choice == 3:
            handle_update_task(service)
        elif choice == 4:
            handle_delete_task(service)
        elif choice == 5:
            handle_mark_complete(service)
        elif choice == 6:
            # Exit
            print(f"\n  {SUCCESS}Thank you for using Todo Application!{RESET}")
            print(f"  {WARNING}Data will be lost when the program exits.{RESET}")
            print(f"\n  {SUBTITLE}Goodbye!{RESET}")
            print()
            break


if __name__ == "__main__":
    main()
