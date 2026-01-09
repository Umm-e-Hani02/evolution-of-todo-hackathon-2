"""Task data model for the todo application.

This module defines the Task entity representing a single todo item with
description, completion status, and unique identifier.
"""

from dataclasses import dataclass


@dataclass
class Task:
    """Represents a todo item with description and completion status.

    Attributes:
        description: User-provided task description (1-500 chars, trimmed)
        completed: Completion status (False=incomplete, True=complete)
        id: Unique identifier assigned by TodoService (>= 1)

    Raises:
        ValueError: If description is empty or exceeds 500 characters
    """

    description: str
    completed: bool = False
    id: int = 0

    def __post_init__(self):
        """Validate task attributes after initialization.

        Raises:
            ValueError: If description is empty after trimming
            ValueError: If description exceeds 500 characters
        """
        # Trim whitespace
        self.description = self.description.strip()

        # Validate non-empty
        if not self.description:
            raise ValueError("Task description cannot be empty")

        # Validate length
        if len(self.description) > 500:
            raise ValueError(
                f"Task description too long ({len(self.description)} chars, max 500)"
            )

    def __str__(self) -> str:
        """Return human-readable task representation.

        Returns:
            Formatted string with completion status and description
        """
        status = "[X]" if self.completed else "[ ]"
        return f"{status} {self.description}"

    def mark_complete(self) -> None:
        """Mark this task as completed (idempotent).

        This method can be called multiple times without error.
        """
        self.completed = True
