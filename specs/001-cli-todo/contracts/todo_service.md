# TodoService Interface Contract

**Feature**: 001-cli-todo
**Version**: 1.0.0
**Date**: 2026-01-03
**Status**: Complete

## Overview

The `TodoService` class is the core business logic layer for the Todo application. It manages the in-memory task collection and enforces all business rules and validation. This contract defines the public interface that CLI handlers use to interact with task data.

## Class Definition

```python
class TodoService:
    """Manages todo tasks with CRUD operations and validation.

    The service maintains an in-memory list of tasks and provides methods
    for adding, viewing, updating, deleting, and marking tasks complete.
    All validation and business logic is encapsulated in this class.

    Attributes:
        _tasks: Private list of Task objects (in-memory storage)
        _next_id: Private counter for assigning unique task IDs
    """
```

## Constructor

### `__init__(self) -> None`

**Purpose**: Initialize a new TodoService instance with empty task list.

**Parameters**: None

**Returns**: None

**Side Effects**:
- Creates empty task list (`self._tasks = []`)
- Initializes ID counter to 1 (`self._next_id = 1`)

**Example**:
```python
service = TodoService()
assert len(service.get_all_tasks()) == 0
```

## Public Methods

### `add_task(self, description: str) -> Task`

**Purpose**: Create and add a new task to the list.

**Parameters**:
- `description` (str): User-provided task description

**Returns**: `Task` - The newly created task with assigned ID

**Raises**:
- `ValueError`: If description is empty after trimming
- `ValueError`: If description exceeds 500 characters

**Behavior**:
1. Trim whitespace from description
2. Validate description (non-empty, ≤500 chars)
3. Create Task with current `_next_id`
4. Append task to `_tasks` list
5. Increment `_next_id`
6. Return created task

**Validation Rules**:
- Description must not be empty after `strip()`
- Description must be ≤ 500 characters after `strip()`
- Description whitespace is trimmed before storage

**Example**:
```python
task = service.add_task("Buy groceries")
assert task.id == 1
assert task.description == "Buy groceries"
assert task.completed == False

# Whitespace handling
task2 = service.add_task("  Write report  ")
assert task2.description == "Write report"  # Trimmed

# Error cases
try:
    service.add_task("")  # Empty
except ValueError as e:
    print(e)  # "Task description cannot be empty"

try:
    service.add_task("x" * 501)  # Too long
except ValueError as e:
    print(e)  # "Task description too long (501 chars, max 500)"
```

**Postconditions**:
- Task list length increased by 1
- New task has unique ID (previous `_next_id`)
- `_next_id` incremented
- Task is incomplete (`completed=False`)

---

### `get_all_tasks(self) -> list[Task]`

**Purpose**: Retrieve all tasks in the list.

**Parameters**: None

**Returns**: `list[Task]` - Copy of the task list (to prevent external modification)

**Raises**: None

**Behavior**:
1. Return shallow copy of `_tasks` list
2. Preserves insertion order

**Example**:
```python
service.add_task("Task 1")
service.add_task("Task 2")

tasks = service.get_all_tasks()
assert len(tasks) == 2
assert tasks[0].description == "Task 1"
assert tasks[1].description == "Task 2"

# Modifying returned list doesn't affect service
tasks.append(Task(description="Fake", id=999))
assert len(service.get_all_tasks()) == 2  # Still 2
```

**Postconditions**:
- Returns independent copy (mutations don't affect internal list)
- Order matches insertion order
- Empty list if no tasks exist

---

### `update_task(self, index: int, description: str) -> Task`

**Purpose**: Update the description of an existing task.

**Parameters**:
- `index` (int): 0-based list index of task to update
- `description` (str): New task description

**Returns**: `Task` - The updated task

**Raises**:
- `IndexError`: If index is out of range (< 0 or >= len(tasks))
- `ValueError`: If new description is empty after trimming
- `ValueError`: If new description exceeds 500 characters

**Behavior**:
1. Validate index is within bounds
2. Validate new description (same rules as `add_task`)
3. Update task's description in-place
4. Return the updated task

**Validation Rules**:
- Index must be: `0 <= index < len(self._tasks)`
- Description must be non-empty after trimming
- Description must be ≤ 500 characters

**Example**:
```python
task = service.add_task("Buy milk")
assert task.id == 1

# Update with valid index
updated = service.update_task(index=0, description="Buy whole milk")
assert updated.id == 1  # ID unchanged
assert updated.description == "Buy whole milk"
assert updated.completed == False  # Status unchanged

# Invalid index
try:
    service.update_task(index=99, description="Test")
except IndexError as e:
    print(e)  # "Task index out of range (0-0)"

# Invalid description
try:
    service.update_task(index=0, description="")
except ValueError as e:
    print(e)  # "Task description cannot be empty"
```

**Postconditions**:
- Task description changed
- Task ID unchanged
- Task completion status unchanged
- Task list length unchanged

---

### `delete_task(self, index: int) -> None`

**Purpose**: Remove a task from the list.

**Parameters**:
- `index` (int): 0-based list index of task to delete

**Returns**: None

**Raises**:
- `IndexError`: If index is out of range (< 0 or >= len(tasks))

**Behavior**:
1. Validate index is within bounds
2. Remove task at index from `_tasks` list
3. Remaining tasks automatically shift down (Python list behavior)

**Note**: Task IDs are NOT renumbered after deletion. Gaps in IDs are acceptable.

**Example**:
```python
service.add_task("Task 1")  # ID: 1
service.add_task("Task 2")  # ID: 2
service.add_task("Task 3")  # ID: 3

# Delete middle task
service.delete_task(index=1)  # Removes "Task 2"

tasks = service.get_all_tasks()
assert len(tasks) == 2
assert tasks[0].id == 1  # ID preserved
assert tasks[1].id == 3  # ID preserved (gap at ID=2)
# User-facing indices: 1 and 2 (CLI converts to 0 and 1 internally)

# Delete from empty list
service = TodoService()
try:
    service.delete_task(index=0)
except IndexError as e:
    print(e)  # "Task index out of range (empty list)"
```

**Postconditions**:
- Task list length decreased by 1
- Remaining tasks shifted down in list (indices changed)
- Task IDs not renumbered (gaps allowed)
- No impact if task was complete vs incomplete

---

### `mark_complete(self, index: int) -> Task`

**Purpose**: Mark a task as completed.

**Parameters**:
- `index` (int): 0-based list index of task to mark complete

**Returns**: `Task` - The updated task with `completed=True`

**Raises**:
- `IndexError`: If index is out of range (< 0 or >= len(tasks))

**Behavior**:
1. Validate index is within bounds
2. Set task's `completed` attribute to `True`
3. Return the updated task

**Idempotency**: Can be called multiple times on the same task without error. Subsequent calls have no effect (task stays complete).

**Example**:
```python
task = service.add_task("Write report")
assert task.completed == False

# First call: marks complete
completed = service.mark_complete(index=0)
assert completed.completed == True
assert completed.id == task.id  # Same task

# Subsequent calls: idempotent
service.mark_complete(index=0)
service.mark_complete(index=0)
assert service.get_all_tasks()[0].completed == True  # Still just True

# Invalid index
try:
    service.mark_complete(index=99)
except IndexError as e:
    print(e)  # "Task index out of range (0-0)"
```

**Postconditions**:
- Task completion status is `True`
- Task description unchanged
- Task ID unchanged
- Task list length unchanged
- Idempotent (safe to call multiple times)

## Error Handling

### Index Validation

**Private Helper**: `_validate_index(self, index: int) -> None`

```python
def _validate_index(self, index: int) -> None:
    """Validate task index is within bounds.

    Args:
        index: 0-based list index

    Raises:
        IndexError: If index is out of range

    Error Messages:
        - Empty list: "No tasks available. Add a task first."
        - Out of range: "Task index out of range. Valid indices: 0-{max}"
    """
    if not self._tasks:
        raise IndexError("No tasks available. Add a task first.")
    if index < 0 or index >= len(self._tasks):
        raise IndexError(f"Task index out of range. Valid indices: 0-{len(self._tasks)-1}")
```

### Description Validation

**Validation Logic** (used by `add_task` and `update_task`):

```python
description = description.strip()

if not description:
    raise ValueError("Task description cannot be empty. Please enter a valid description.")

if len(description) > 500:
    raise ValueError(f"Task description too long ({len(description)} characters, max 500).")
```

## Usage Example

### Complete Workflow

```python
from models.task import Task
from services.todo_service import TodoService

# Initialize service
service = TodoService()

# Add tasks
task1 = service.add_task("Buy groceries")
task2 = service.add_task("Write report")
task3 = service.add_task("Call dentist")

print(f"Added {len(service.get_all_tasks())} tasks")

# View tasks
for task in service.get_all_tasks():
    print(f"{task.id}. {task}")

# Update task
service.update_task(index=1, description="Write quarterly report")

# Mark task complete
service.mark_complete(index=0)

# View updated tasks
print("\nUpdated tasks:")
for i, task in enumerate(service.get_all_tasks()):
    print(f"Index {i}: {task}")

# Delete task
service.delete_task(index=2)

# Final state
print(f"\nFinal count: {len(service.get_all_tasks())} tasks")
```

**Output**:
```
Added 3 tasks
1. [ ] Buy groceries
2. [ ] Write report
3. [ ] Call dentist

Updated tasks:
Index 0: [✓] Buy groceries
Index 1: [ ] Write quarterly report
Index 2: [ ] Call dentist

Final count: 2 tasks
```

## Design Rationale

### Why TodoService Class?

**Encapsulation**: Hides implementation details (list-based storage) from CLI layer. Phase II can switch to database without changing interface.

**Single Responsibility**: Service handles data management and business rules. CLI handles user interaction. Clear separation of concerns.

**Testability**: Service can be instantiated and tested independently of CLI. Mock service instances for testing CLI handlers.

### Why Return Task Objects?

**Type Safety**: Returning `Task` instead of dict provides IDE autocomplete and type checking.

**Immutability Concerns**: Returned tasks are references to internal objects. Clients can modify them, but this is acceptable for Phase I (single-threaded, no concurrent access).

**Phase II Evolution**: Can add `.copy()` or return DTOs if immutability becomes important.

### Why 0-Based Indexing in Service?

**Python Convention**: Internal code uses Python's 0-based indexing standard.

**Separation of Concerns**: Service doesn't know about user-facing display. CLI layer converts 1-based user input to 0-based service calls.

**Example Conversion**:
```python
# CLI Layer (1-based for users)
user_input = input("Enter task number: ")  # User enters: 1
list_index = int(user_input) - 1           # Convert to: 0

# Service Layer (0-based internally)
service.mark_complete(index=list_index)    # Use 0-based index
```

## Contract Versioning

**Current Version**: 1.0.0

**Breaking Changes** (would require major version bump):
- Changing method signatures (parameters or return types)
- Removing public methods
- Changing exception types

**Non-Breaking Changes** (minor/patch version):
- Adding new public methods
- Adding optional parameters with defaults
- Improving error messages
- Internal implementation changes

**Phase Evolution**:
- Phase I: v1.0.0 (current - in-memory list)
- Phase II: v2.0.0 (add database persistence, new methods)
- Phase III: v3.0.0 (add AI integration methods)

## Testing Contract

All service methods should pass these contract tests:

```python
# Add task validation
assert add_task("Valid") succeeds
assert add_task("") raises ValueError
assert add_task(" ") raises ValueError
assert add_task("x" * 501) raises ValueError

# Get all tasks
service = TodoService()
assert len(service.get_all_tasks()) == 0
service.add_task("Test")
assert len(service.get_all_tasks()) == 1

# Update task validation
assert update_task(0, "New") succeeds
assert update_task(99, "New") raises IndexError
assert update_task(0, "") raises ValueError

# Delete task validation
assert delete_task(0) succeeds when task exists
assert delete_task(0) raises IndexError on empty list
assert delete_task(99) raises IndexError when out of range

# Mark complete validation
assert mark_complete(0) succeeds when task exists
assert mark_complete(0) idempotent (can call multiple times)
assert mark_complete(99) raises IndexError when out of range
```

## Implementation Location

**File**: `phase-1-cli/src/services/todo_service.py`

**Dependencies**:
- `models.task.Task` - Task entity definition

**No External Dependencies**: Uses Python standard library only

## Appendix: Complete Interface Summary

```python
class TodoService:
    """Todo task management service."""

    def __init__(self) -> None:
        """Initialize service with empty task list."""

    def add_task(self, description: str) -> Task:
        """Add new task. Raises ValueError if invalid."""

    def get_all_tasks(self) -> list[Task]:
        """Return copy of all tasks."""

    def update_task(self, index: int, description: str) -> Task:
        """Update task description. Raises IndexError/ValueError."""

    def delete_task(self, index: int) -> None:
        """Remove task. Raises IndexError if invalid index."""

    def mark_complete(self, index: int) -> Task:
        """Mark task complete (idempotent). Raises IndexError."""

    def _validate_index(self, index: int) -> None:
        """Private helper for index validation."""
```
