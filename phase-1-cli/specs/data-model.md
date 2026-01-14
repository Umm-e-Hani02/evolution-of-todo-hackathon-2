# Data Model: In-Memory Python Console Todo Application

**Feature**: 001-cli-todo
**Date**: 2026-01-03
**Status**: Complete

## Overview

This document defines the data entities for Phase I of the Todo application. The model is intentionally simple to align with Phase I constitution constraints (in-memory, basic CRUD operations). Future phases will extend this model with persistence, relationships, and additional attributes.

## Entities

### Task

**Purpose**: Represents a single todo item in the user's task list.

**Attributes**:

| Attribute | Type | Required | Default | Validation | Description |
|-----------|------|----------|---------|------------|-------------|
| `id` | `int` | Yes | 0 (assigned by service) | > 0 | Unique identifier for the task within the session |
| `description` | `str` | Yes | None | 1-500 chars, non-empty after trim | User-provided text describing what needs to be done |
| `completed` | `bool` | Yes | `False` | True or False | Whether the task has been marked as complete |

**Invariants**:
- `id` is unique within a TodoService instance (auto-incremented starting from 1)
- `description` is never empty or whitespace-only (enforced at creation and update)
- `description` is stored with leading/trailing whitespace trimmed
- `completed` starts as `False` and can only transition to `True` (no uncomplete operation in Phase I)

**Implementation**:

```python
from dataclasses import dataclass

@dataclass
class Task:
    """Represents a todo item with description and completion status.

    Attributes:
        description: User-provided task description (1-500 chars, trimmed)
        completed: Completion status (False=incomplete, True=complete)
        id: Unique identifier assigned by TodoService (>= 1)
    """
    description: str
    completed: bool = False
    id: int = 0

    def __post_init__(self):
        """Validate task attributes after initialization."""
        # Trim whitespace
        self.description = self.description.strip()

        # Validate non-empty
        if not self.description:
            raise ValueError("Task description cannot be empty")

        # Validate length
        if len(self.description) > 500:
            raise ValueError(f"Task description too long ({len(self.description)} chars, max 500)")

    def __str__(self) -> str:
        """Return human-readable task representation."""
        status = "[✓]" if self.completed else "[ ]"
        return f"{status} {self.description}"

    def mark_complete(self) -> None:
        """Mark this task as completed (idempotent)."""
        self.completed = True
```

**Usage Examples**:

```python
# Creating tasks
task1 = Task(description="Buy groceries", id=1)
task2 = Task(description="  Write report  ", id=2)  # Whitespace trimmed automatically

# Invalid tasks (raise ValueError)
Task(description="")           # Empty description
Task(description="   ")        # Whitespace-only description
Task(description="x" * 501)    # Too long

# Marking complete
task1.mark_complete()
assert task1.completed == True

# Display
print(task1)  # Output: [✓] Buy groceries
print(task2)  # Output: [ ] Write report
```

## Validation Rules

### Description Validation

**Rule**: Task description must be 1-500 characters after trimming whitespace.

**Implementation Location**: `Task.__post_init__()` and `TodoService.add_task()/update_task()`

**Error Messages**:
- Empty: `"Task description cannot be empty"`
- Too long: `"Task description too long ({len} chars, max 500)"`

**Validation Logic**:
```python
def validate_description(desc: str) -> str:
    """Validate and sanitize task description.

    Args:
        desc: Raw user input

    Returns:
        Sanitized description (trimmed)

    Raises:
        ValueError: If description is invalid
    """
    desc = desc.strip()

    if not desc:
        raise ValueError("Task description cannot be empty")

    if len(desc) > 500:
        raise ValueError(f"Task description too long ({len(desc)} chars, max 500)")

    return desc
```

### ID Management

**Rule**: Task IDs are positive integers starting from 1, auto-incremented, unique per service instance.

**Implementation Location**: `TodoService.add_task()`

**Assignment Logic**:
```python
class TodoService:
    def __init__(self):
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def add_task(self, description: str) -> Task:
        task = Task(description=description, id=self._next_id)
        self._tasks.append(task)
        self._next_id += 1
        return task
```

**Notes**:
- IDs are not reused after deletion (gap preservation)
- IDs reset to 1 on application restart (in-memory only)
- User-facing index (1-based) is different from task ID

## State Transitions

### Task Lifecycle

```
[Created] ---> [Incomplete] ---> [Complete]
     |              |                 |
     |              |                 |
   (add)         (update)          (delete)
                  (mark)
```

**States**:
1. **Created**: Task instantiated with validated description, `completed=False`, `id=0` (before service assignment)
2. **Incomplete**: Task in service list with assigned ID, `completed=False` (active work)
3. **Complete**: Task in service list with `completed=True` (finished work)

**Transitions**:
- **add**: Created → Incomplete (service assigns ID, adds to list)
- **update**: Incomplete ↔ Incomplete (description changes, status unchanged)
- **mark**: Incomplete → Complete (idempotent - can be called multiple times)
- **delete**: Any state → Removed (task removed from list entirely)

**Important**: No "uncomplete" operation in Phase I. Once marked complete, a task stays complete until deleted.

## Relationships

**Phase I**: No relationships. Tasks are independent entities in a flat list.

**Future Phases**:
- Phase II: Tasks may have `user_id` (multi-user), `created_at`, `updated_at` (timestamps)
- Phase III: Tasks may have `parent_task_id` (subtasks), `tags` (categorization)
- Phase IV: Tasks may be distributed across microservices (event sourcing)

## Storage

**Phase I Implementation**: Python list in `TodoService`

```python
class TodoService:
    def __init__(self):
        self._tasks: list[Task] = []  # In-memory storage
        self._next_id: int = 1

    def get_all_tasks(self) -> list[Task]:
        """Return copy of task list to prevent external modification."""
        return self._tasks.copy()
```

**Characteristics**:
- **Volatility**: Data lost on application exit (session-only)
- **Capacity**: Limited by available RAM (~1GB = ~10M tasks with 100-char descriptions)
- **Performance**: O(1) append, O(n) search/delete, O(1) access by index
- **Concurrency**: Single-threaded, no locking needed

**Phase II Evolution**: Replace `list` with database repository pattern:
```python
# Phase II (future)
class TodoService:
    def __init__(self, repository: TaskRepository):
        self._repo = repository  # Database-backed storage
```

## Data Integrity

### Guarantees

**Phase I Guarantees**:
1. ✅ No duplicate IDs within a session
2. ✅ No empty or whitespace-only descriptions
3. ✅ No descriptions exceeding 500 characters
4. ✅ Completion status is always boolean (never null/undefined)
5. ✅ Task list order is stable (insertion order preserved)

**Non-Guarantees** (acceptable for Phase I):
1. ❌ No persistence across sessions (by design)
2. ❌ No transaction rollback (stateful operations)
3. ❌ No concurrent access safety (single-threaded)
4. ❌ No backup or recovery

### Constraints

**Hard Constraints** (enforced by validation):
- Description: 1 ≤ length ≤ 500 characters (after trim)
- ID: integer ≥ 1
- Completed: boolean (True or False)

**Soft Constraints** (conventions, not enforced):
- Task descriptions should be concise action items (recommendation)
- Tasks should represent single units of work (best practice)
- Completed tasks can be deleted to keep list manageable (user choice)

## Examples

### Complete Task Lifecycle

```python
# Initialize service
service = TodoService()

# Add task
task = service.add_task("Buy groceries")
assert task.id == 1
assert task.description == "Buy groceries"
assert task.completed == False

# View tasks
tasks = service.get_all_tasks()
assert len(tasks) == 1
print(tasks[0])  # Output: [ ] Buy groceries

# Update task
updated = service.update_task(index=0, description="Buy groceries and milk")
assert updated.description == "Buy groceries and milk"
assert updated.id == 1  # ID unchanged
assert updated.completed == False  # Status unchanged

# Mark complete
completed = service.mark_complete(index=0)
assert completed.completed == True
print(completed)  # Output: [✓] Buy groceries and milk

# Delete task
service.delete_task(index=0)
tasks = service.get_all_tasks()
assert len(tasks) == 0
```

### Edge Cases

```python
# Empty list operations
service = TodoService()

# Attempt to update non-existent task
try:
    service.update_task(index=0, description="Test")
except IndexError as e:
    print(f"Error: {e}")  # "No tasks available"

# Add multiple tasks
service.add_task("Task 1")  # ID: 1
service.add_task("Task 2")  # ID: 2
service.add_task("Task 3")  # ID: 3

# Delete middle task
service.delete_task(index=1)  # Removes "Task 2" (ID 2)

# Remaining tasks
tasks = service.get_all_tasks()
assert len(tasks) == 2
assert tasks[0].id == 1  # IDs not renumbered
assert tasks[1].id == 3
# But user sees indices 1 and 2 (user-facing is renumbered)

# Idempotent complete
task = service.add_task("Test")
service.mark_complete(index=0)
service.mark_complete(index=0)  # Second call does nothing
service.mark_complete(index=0)  # Third call does nothing
assert task.completed == True  # Still just True

# Whitespace handling
task = service.add_task("  Clean room  ")
assert task.description == "Clean room"  # Trimmed
```

## Migration Path (Future Phases)

### Phase I → Phase II (Add Persistence)

```python
# Phase I (current)
@dataclass
class Task:
    description: str
    completed: bool = False
    id: int = 0

# Phase II (future)
@dataclass
class Task:
    description: str
    completed: bool = False
    id: int = 0
    created_at: datetime = None  # NEW
    updated_at: datetime = None  # NEW
    user_id: int = None          # NEW (multi-user)
```

**Migration Strategy**: Add optional fields with defaults to maintain backward compatibility.

### Phase II → Phase III (Add AI Features)

```python
# Phase III (future)
@dataclass
class Task:
    # ... existing fields ...
    priority: str = "medium"     # NEW: low, medium, high
    tags: list[str] = None       # NEW: categorization
    ai_generated: bool = False   # NEW: track AI-created tasks
```

### Phase III → Phase IV (Add Kubernetes Metadata)

```python
# Phase IV (future)
@dataclass
class Task:
    # ... existing fields ...
    namespace: str = "default"   # NEW: K8s namespace
    pod_id: str = None           # NEW: processing pod identifier
```

## Appendix: Complete Implementation

See `phase-1-cli/src/models/task.py` for the full implementation of the Task entity.

**File Location**: `phase-1-cli/src/models/task.py`

**Dependencies**: None (Python standard library only)

**Testing**: Manual REPL testing per acceptance scenarios in `specs/spec.md`
