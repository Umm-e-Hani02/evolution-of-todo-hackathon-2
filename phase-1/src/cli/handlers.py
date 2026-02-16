"""Command handlers for CLI operations.

This module implements handler functions for each menu operation,
coordinating between user input and the TodoService.
"""

from ..services.todo_service import TodoService
from .colors import (
    BOLD, PRIMARY, ACCENT, SUCCESS, ERROR, WARNING,
    TASK_DONE, TASK_PENDING, MUTED, MENU_NUMBER, RESET
)


def get_positive_int(prompt: str) -> int | None:
    """Get a positive integer from user input.

    Args:
        prompt: The prompt message to display

    Returns:
        Positive integer if valid, None if invalid

    Note:
        This helper is used for getting task indices from the user.
    """
    try:
        value = int(input(f"  {prompt}"))
        if value <= 0:
            print(f"  {ERROR}[x] Error:{RESET} Please enter a positive number.")
            return None
        return value
    except ValueError:
        print(f"  {ERROR}[x] Error:{RESET} Invalid input. Please enter a valid number.")
        return None
    except (EOFError, KeyboardInterrupt):
        print(f"\n  {WARNING}[!] Operation cancelled.{RESET}")
        return None


def handle_add_task(service: TodoService) -> None:
    """Handle adding a new task.

    Args:
        service: TodoService instance to add task to
    """
    try:
        description = input(f"\n  {ACCENT}>{RESET} Enter task description: ")
        if not description.strip():
            print(f"  {ERROR}[x] Error:{RESET} Task description cannot be empty.")
            return
        task = service.add_task(description)
        print(f"  {SUCCESS}[+] Task added:{RESET} {BOLD}{task.description}{RESET}")
    except ValueError as e:
        print(f"  {ERROR}[x] Error: {e}{RESET}")


def handle_view_tasks(service: TodoService) -> None:
    """Handle viewing all tasks.

    Args:
        service: TodoService instance to get tasks from
    """
    tasks = service.get_all_tasks()

    if not tasks:
        print(f"\n  {MUTED}No tasks yet. Add your first task to get started!{RESET}")
        return

    print(f"\n  {BOLD}{PRIMARY}+-------------------------------------------------------+{RESET}")
    print(f"  {BOLD}{PRIMARY}|{RESET}                   {BOLD}YOUR TASKS{RESET}                        {BOLD}{PRIMARY}|{RESET}")
    print(f"  {BOLD}{PRIMARY}+-------------------------------------------------------+{RESET}")

    completed_count = sum(1 for task in tasks if task.completed)
    pending_count = len(tasks) - completed_count

    for index, task in enumerate(tasks, start=1):
        # Truncate long descriptions to fit (max 38 chars for description)
        max_desc_len = 38
        display_desc = task.description
        if len(task.description) > max_desc_len:
            display_desc = task.description[:max_desc_len-3] + "..."

        # Build plain text line to calculate width
        status_char = "*" if task.completed else "o"
        plain_line = f" {index:2d}. {status_char} {display_desc}"

        # Now apply colors
        if task.completed:
            colored_line = f" {MENU_NUMBER}{index:2d}.{RESET} {TASK_DONE}{status_char}{RESET} {MUTED}{display_desc}{RESET}"
        else:
            colored_line = f" {MENU_NUMBER}{index:2d}.{RESET} {TASK_PENDING}{status_char}{RESET} {display_desc}"

        # Add padding spaces (calculate based on plain text)
        padding_needed = 50 - len(plain_line)
        padding = " " * padding_needed if padding_needed > 0 else ""

        print(f"  {BOLD}{PRIMARY}|{RESET}{colored_line}{padding} {BOLD}{PRIMARY}|{RESET}")

    print(f"  {BOLD}{PRIMARY}+-------------------------------------------------------+{RESET}")

    # Build summary line
    plain_summary = f" Total: {len(tasks)}  * Done: {completed_count}  o Pending: {pending_count}"
    padding_needed = 50 - len(plain_summary)
    padding = " " * padding_needed if padding_needed > 0 else ""

    colored_summary = f" {BOLD}Total:{RESET} {len(tasks)}  {TASK_DONE}*{RESET} {BOLD}Done:{RESET} {completed_count}  {TASK_PENDING}o{RESET} {BOLD}Pending:{RESET} {pending_count}"

    print(f"  {BOLD}{PRIMARY}|{RESET}{colored_summary}{padding} {BOLD}{PRIMARY}|{RESET}")
    print(f"  {BOLD}{PRIMARY}+-------------------------------------------------------+{RESET}")


def handle_update_task(service: TodoService) -> None:
    """Handle updating a task's description.

    Args:
        service: TodoService instance to update task in
    """
    tasks = service.get_all_tasks()
    if not tasks:
        print(f"\n  {MUTED}No tasks to update. Please add a task first.{RESET}")
        return

    handle_view_tasks(service)
    print()

    task_num = get_positive_int(f"{ACCENT}>{RESET} Enter task number to update: ")
    if task_num is None:
        return

    index = task_num - 1

    try:
        current_task = tasks[index]
        print(f"  {MUTED}Current: {current_task.description}{RESET}")

        new_description = input(f"  {ACCENT}>{RESET} Enter new description: ")
        if not new_description.strip():
            print(f"  {ERROR}[x] Error:{RESET} Task description cannot be empty.")
            return

        updated_task = service.update_task(index, new_description)
        print(f"  {SUCCESS}[+] Task {task_num} updated:{RESET} {BOLD}{updated_task.description}{RESET}")
    except IndexError:
        print(f"  {ERROR}[x] Error:{RESET} Task #{task_num} does not exist. Choose 1-{len(tasks)}.")
    except ValueError as e:
        print(f"  {ERROR}[x] Error: {e}{RESET}")


def handle_delete_task(service: TodoService) -> None:
    """Handle deleting a task.

    Args:
        service: TodoService instance to delete task from
    """
    tasks = service.get_all_tasks()
    if not tasks:
        print(f"\n  {MUTED}No tasks to delete. The list is already empty.{RESET}")
        return

    handle_view_tasks(service)
    print()

    task_num = get_positive_int(f"{ERROR}>{RESET} Enter task number to delete: ")
    if task_num is None:
        return

    index = task_num - 1

    try:
        task_description = tasks[index].description
        service.delete_task(index)
        print(f"  {SUCCESS}[-] Task deleted:{RESET} {MUTED}{task_description}{RESET}")
    except IndexError:
        print(f"  {ERROR}[x] Error:{RESET} Task #{task_num} does not exist. Choose 1-{len(tasks)}.")


def handle_mark_complete(service: TodoService) -> None:
    """Handle marking a task as complete.

    Args:
        service: TodoService instance to mark task in
    """
    tasks = service.get_all_tasks()
    if not tasks:
        print(f"\n  {MUTED}No tasks to complete. Please add a task first.{RESET}")
        return

    handle_view_tasks(service)
    print()

    task_num = get_positive_int(f"{SUCCESS}>{RESET} Enter task number to mark complete: ")
    if task_num is None:
        return

    index = task_num - 1

    try:
        if tasks[index].completed:
            print(f"  {WARNING}[!] Note:{RESET} Task #{task_num} is already complete.")
            return

        completed_task = service.mark_complete(index)
        print(f"  {SUCCESS}[+] Task completed:{RESET} {BOLD}{completed_task.description}{RESET}")
    except IndexError:
        print(f"  {ERROR}[x] Error:{RESET} Task #{task_num} does not exist. Choose 1-{len(tasks)}.")
