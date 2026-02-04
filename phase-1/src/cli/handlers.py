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
            print(f"  {ERROR}Error:{RESET} Please enter a positive number.")
            return None
        return value
    except ValueError:
        print(f"  {ERROR}Error:{RESET} Invalid input. Please enter a valid number.")
        return None
    except (EOFError, KeyboardInterrupt):
        print(f"\n  {WARNING}Operation cancelled.{RESET}")
        return None


def handle_add_task(service: TodoService) -> None:
    """Handle adding a new task.

    Args:
        service: TodoService instance to add task to
    """
    try:
        description = input(f"  {ACCENT}Enter task description: {RESET}")
        if not description.strip():
            print(f"  {ERROR}Error:{RESET} Task description cannot be empty.")
            return
        task = service.add_task(description)
        print(f"  {SUCCESS}✔ Task '{task.description}' added successfully!{RESET}")
    except ValueError as e:
        print(f"  {ERROR}Error: {e}{RESET}")


def handle_view_tasks(service: TodoService) -> None:
    """Handle viewing all tasks.

    Args:
        service: TodoService instance to get tasks from
    """
    tasks = service.get_all_tasks()

    if not tasks:
        print(f"\n  {MUTED}No tasks yet. Select 'Add Task' to get started!{RESET}")
        return

    print(f"\n  {BOLD}{PINK}┌────────────────── Your Tasks ──────────────────┐{RESET}")
    
    completed_count = sum(1 for task in tasks if task.completed)
    pending_count = len(tasks) - completed_count

    for index, task in enumerate(tasks, start=1):
        status_icon = f"{TASK_DONE}●{RESET}" if task.completed else f"{TASK_PENDING}○{RESET}"
        description_style = f"{MUTED}{task.description}{RESET}" if task.completed else f"{RESET}{task.description}"
        num_str = f"{SECONDARY}{index:2d}){RESET}"
        
        # Basic padding to align content
        line = f"  {num_str} {status_icon} {description_style}"
        print(f"  {BOLD}{PINK}│{RESET}{line.ljust(50)}{BOLD}{PINK}│{RESET}")


    print(f"  {BOLD}{PINK}├──────────────────────────────────────────────┤{RESET}")
    summary = f"  Total: {len(tasks)} | {TASK_DONE}Done: {completed_count}{RESET} | {TASK_PENDING}Pending: {pending_count}{RESET}"
    print(f"  {BOLD}{PINK}│{RESET}{summary.ljust(50)}{BOLD}{PINK}│{RESET}")
    print(f"  {BOLD}{PINK}└──────────────────────────────────────────────┘{RESET}")


def handle_update_task(service: TodoService) -> None:
    """Handle updating a task's description.

    Args:
        service: TodoService instance to update task in
    """
    tasks = service.get_all_tasks()
    if not tasks:
        print(f"  {MUTED}No tasks to update. Please add a task first.{RESET}")
        return

    handle_view_tasks(service) # Show tasks to the user first
    print()

    task_num = get_positive_int(f"{ACCENT}Enter task number to update: {RESET}")
    if task_num is None:
        return

    index = task_num - 1

    try:
        current_task = tasks[index]
        print(f"  {MUTED}Current description: {current_task.description}{RESET}")

        new_description = input(f"  {ACCENT}Enter new description: {RESET}")
        if not new_description.strip():
            print(f"  {ERROR}Error:{RESET} Task description cannot be empty.")
            return

        updated_task = service.update_task(index, new_description)
        print(f"  {SUCCESS}✔ Task {task_num} updated successfully to '{updated_task.description}'!{RESET}")
    except IndexError:
        print(f"  {ERROR}Error:{RESET} Task number {task_num} does not exist. Please enter a number between 1 and {len(tasks)}.")
    except ValueError as e:
        print(f"  {ERROR}Error: {e}{RESET}")


def handle_delete_task(service: TodoService) -> None:
    """Handle deleting a task.

    Args:
        service: TodoService instance to delete task from
    """
    tasks = service.get_all_tasks()
    if not tasks:
        print(f"  {MUTED}No tasks to delete. The list is already empty.{RESET}")
        return
        
    handle_view_tasks(service) # Show tasks to the user first
    print()

    task_num = get_positive_int(f"{ERROR}Enter task number to delete: {RESET}")
    if task_num is None:
        return

    index = task_num - 1

    try:
        task_description = tasks[index].description
        service.delete_task(index)
        print(f"  {SUCCESS}✔ Task '{task_description}' deleted successfully.{RESET}")
    except IndexError:
        print(f"  {ERROR}Error:{RESET} Task number {task_num} does not exist. Please enter a number between 1 and {len(tasks)}.")


def handle_mark_complete(service: TodoService) -> None:
    """Handle marking a task as complete.

    Args:
        service: TodoService instance to mark task in
    """
    tasks = service.get_all_tasks()
    if not tasks:
        print(f"  {MUTED}No tasks to complete. Please add a task first.{RESET}")
        return

    handle_view_tasks(service) # Show tasks to the user first
    print()

    task_num = get_positive_int(f"{ACCENT}Enter task number to mark as complete: {RESET}")
    if task_num is None:
        return

    index = task_num - 1

    try:
        if tasks[index].completed:
            print(f"  {WARNING}Note:{RESET} Task {task_num} is already marked as complete.")
            return

        completed_task = service.mark_complete(index)
        print(f"  {SUCCESS}✔ Task '{completed_task.description}' marked as complete!{RESET}")
    except IndexError:
        print(f"  {ERROR}Error:{RESET} Task number {task_num} does not exist. Please enter a number between 1 and {len(tasks)}.")
