"""TodoService business logic layer for task management.

This module provides the core CRUD operations for managing todo tasks
in memory with validation and error handling.
"""

from ..models.task import Task


class TodoService:
    """Manages todo tasks with CRUD operations and validation.

    The service maintains an in-memory list of tasks and provides methods
    for adding, viewing, updating, deleting, and marking tasks complete.
    All validation and business logic is encapsulated in this class.

    Attributes:
        _tasks: Private list of Task objects (in-memory storage)
        _next_id: Private counter for assigning unique task IDs
    """

    def __init__(self):
        """Initialize service with empty task list."""
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def add_task(self, description: str) -> Task:
        """Add a new task to the list.

        Args:
            description: User-provided task description

        Returns:
            The newly created task with assigned ID

        Raises:
            ValueError: If description is empty after trimming
            ValueError: If description exceeds 500 characters
        """
        # Validate and create task (Task.__post_init__ handles validation)
        task = Task(description=description, id=self._next_id)
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks in the list.

        Returns:
            Copy of the task list (to prevent external modification)
        """
        return self._tasks.copy()

    def _validate_index(self, index: int) -> None:
        """Validate task index is within bounds.

        Args:
            index: 0-based list index

        Raises:
            IndexError: If index is out of range or list is empty
        """
        if not self._tasks:
            raise IndexError("No tasks available. Add a task first.")
        if index < 0 or index >= len(self._tasks):
            raise IndexError(
                f"Task index out of range. Valid indices: 0-{len(self._tasks)-1}"
            )

    def update_task(self, index: int, description: str) -> Task:
        """Update the description of an existing task.

        Args:
            index: 0-based list index of task to update
            description: New task description

        Returns:
            The updated task

        Raises:
            IndexError: If index is out of range
            ValueError: If new description is empty or too long
        """
        self._validate_index(index)

        # Validate new description by creating a temporary task
        # This reuses Task's validation logic
        temp_task = Task(description=description)

        # Update the existing task's description
        self._tasks[index].description = temp_task.description
        return self._tasks[index]

    def delete_task(self, index: int) -> None:
        """Remove a task from the list.

        Args:
            index: 0-based list index of task to delete

        Raises:
            IndexError: If index is out of range
        """
        self._validate_index(index)
        del self._tasks[index]

    def mark_complete(self, index: int) -> Task:
        """Mark a task as completed.

        Args:
            index: 0-based list index of task to mark complete

        Returns:
            The updated task with completed=True

        Raises:
            IndexError: If index is out of range

        Note:
            This operation is idempotent - calling it multiple times
            on the same task has no additional effect.
        """
        self._validate_index(index)
        self._tasks[index].completed = True
        return self._tasks[index]
