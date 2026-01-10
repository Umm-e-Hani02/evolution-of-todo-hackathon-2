"""Command handlers for CLI operations.

This module implements handler functions for each menu operation,
coordinating between user input and the TodoService.
"""

from ..services.todo_service import TodoService
from .colors import BOLD, ACCENT, SUCCESS, ERROR, WARNING, TASK_DONE, TASK_PENDING, MUTED, SECONDARY, PINK, RESET


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
            print(f"  {ERROR}Enter a positive number{RESET}")
            return None
        return value
    except ValueError:
        print(f"  {ERROR}Enter a valid number{RESET}")
        return None
    except (EOFError, KeyboardInterrupt):
        print(f"\n  {WARNING}Operation cancelled{RESET}")
        return None


def handle_add_task(service: TodoService) -> None:
    """Handle adding a new task.

    Args:
        service: TodoService instance to add task to
    """
    try:
        description = input(f"  {ACCENT}Task description: {RESET}")
        task = service.add_task(description)
        print(f"  {SUCCESS}✔ {task.description} added successfully{RESET}")
    except ValueError as e:
        print(f"  {ERROR}{e}{RESET}")


def handle_view_tasks(service: TodoService) -> None:
    """Handle viewing all tasks.

    Args:
        service: TodoService instance to get tasks from
    """
    tasks = service.get_all_tasks()

    if not tasks:
        print(f"\n  {MUTED}No tasks yet. Add your first task!{RESET}")
        return

    print(f"\n  {BOLD}{PINK}Your Tasks{RESET}")
    print(f"  {MUTED}{'-' * 45}{RESET}")

    completed_count = sum(1 for task in tasks if task.completed)
    pending_count = len(tasks) - completed_count

    for index, task in enumerate(tasks, start=1):
        status = f"{TASK_DONE}●{RESET}" if task.completed else f"{TASK_PENDING}○{RESET}"
        desc = f"{TASK_DONE}{task.description}{RESET}" if task.completed else f"{TASK_PENDING}{task.description}{RESET}"
        num_str = f"{SUCCESS}{index:2d}{RESET}"
        print(f"  {num_str}) {status} {desc}")

    print(f"  {MUTED}{'-' * 45}{RESET}")
    print(f"  {BOLD}Total:{RESET} {len(tasks)}  {TASK_DONE}{completed_count} done{RESET}  {TASK_PENDING}{pending_count} pending{RESET}")


def handle_update_task(service: TodoService) -> None:
    """Handle updating a task's description.

    Args:
        service: TodoService instance to update task in
    """
    # First show tasks so user knows valid indices
    tasks = service.get_all_tasks()
    if not tasks:
        print(f"  {ERROR}No tasks available. Add a task first.{RESET}")
        return

    task_num = get_positive_int(f"{ACCENT}Task number to update: {RESET}")
    if task_num is None:
        return

    # Convert 1-based user input to 0-based list index
    index = task_num - 1

    try:
        # Show current description
        current_task = tasks[index]
        print(f"  {MUTED}Current: {current_task.description}{RESET}")

        new_description = input(f"  {ACCENT}New description: {RESET}")
        updated_task = service.update_task(index, new_description)
        print(f"  {SUCCESS}✔ {updated_task.description} updated successfully{RESET}")
    except IndexError as e:
        print(f"  {ERROR}{e}{RESET}")
        print(f"  {MUTED}Enter 1-{len(tasks)}{RESET}")
    except ValueError as e:
        print(f"  {ERROR}{e}{RESET}")


def handle_delete_task(service: TodoService) -> None:
    """Handle deleting a task.

    Args:
        service: TodoService instance to delete task from
    """
    tasks = service.get_all_tasks()
    if not tasks:
        print(f"  {ERROR}No tasks available. Add a task first.{RESET}")
        return

    task_num = get_positive_int(f"{ERROR}Task number to delete: {RESET}")
    if task_num is None:
        return

    # Convert 1-based user input to 0-based list index
    index = task_num - 1

    try:
        task_description = tasks[index].description
        service.delete_task(index)
        print(f"  {SUCCESS}✔ {task_description} deleted successfully{RESET}")
        print(f"  {MUTED}Remaining tasks renumbered{RESET}")
    except IndexError as e:
        print(f"  {ERROR}{e}{RESET}")
        print(f"  {MUTED}Enter 1-{len(tasks)}{RESET}")


def handle_mark_complete(service: TodoService) -> None:
    """Handle marking a task as complete.

    Args:
        service: TodoService instance to mark task in
    """
    tasks = service.get_all_tasks()
    if not tasks:
        print(f"  {ERROR}No tasks available. Add a task first.{RESET}")
        return

    task_num = get_positive_int(f"{ACCENT}Task number to complete: {RESET}")
    if task_num is None:
        return

    # Convert 1-based user input to 0-based list index
    index = task_num - 1

    try:
        completed_task = service.mark_complete(index)
        print(f"  {SUCCESS}✔ {completed_task.description} marked complete{RESET}")
        print(f"  {MUTED}View tasks to see updated status{RESET}")
    except IndexError as e:
        print(f"  {ERROR}{e}{RESET}")
        print(f"  {MUTED}Enter 1-{len(tasks)}{RESET}")
