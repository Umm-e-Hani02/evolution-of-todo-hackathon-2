# Technical Research: In-Memory Python Console Todo Application

**Feature**: 001-cli-todo
**Date**: 2026-01-03
**Status**: Complete

## Overview

This document captures research findings for key technical decisions in Phase I of the Evolution of Todo project. All decisions prioritize simplicity, maintainability, and alignment with Phase I constitution constraints (in-memory only, no external dependencies, PEP 8 compliance).

## Research Areas

### 1. Task Data Model: Dict vs Dataclass vs NamedTuple

**Question**: What Python construct should represent a Task entity?

**Options Evaluated**:

| Option | Pros | Cons |
|--------|------|------|
| Dict | Simple, flexible, no imports needed | No type safety, error-prone key access, poor IDE support |
| Dataclass | Type hints, validation hooks, clean syntax | Requires `dataclass` import (stdlib) |
| NamedTuple | Immutable, memory-efficient | Immutability conflicts with `completed` status changes |
| Plain Class | Full control, no learning curve | Verbose boilerplate for simple data |

**Decision**: **Dataclass**

**Rationale**:
- **Type Safety**: `@dataclass` provides compile-time type checking via mypy/IDE
- **Validation**: `__post_init__` hook enables input validation at creation time
- **Readability**: `task.description` vs `task['description']` is clearer
- **Standard Library**: Part of Python 3.7+ (no external dependency)
- **Future-Proof**: Easy to add fields in Phase II (e.g., `created_date`, `priority`)

**Implementation**:
```python
from dataclasses import dataclass

@dataclass
class Task:
    description: str
    completed: bool = False
    id: int = 0

    def __post_init__(self):
        if not self.description or not self.description.strip():
            raise ValueError("Task description cannot be empty")
        if len(self.description) > 500:
            raise ValueError("Task description too long (max 500 characters)")
```

**References**:
- [PEP 557 - Data Classes](https://peps.python.org/pep-0557/)
- [Real Python: Data Classes in Python 3.7+](https://realpython.com/python-data-classes/)

### 2. CLI Interface Pattern: Numeric Menu vs Text Commands

**Question**: How should users interact with the application?

**Options Evaluated**:

| Option | Pros | Cons |
|--------|------|------|
| Numeric Menu (1-6) | Spec-aligned, simple validation, beginner-friendly | Less flexible, requires menu display |
| Text Commands ("add", "list") | Professional feel, shell-like | Complex parsing, more error cases, not in spec |
| Single-Letter ("a", "l", "d") | Fast for power users | Not discoverable, conflicts (delete/done) |

**Decision**: **Numeric Menu**

**Rationale**:
- **Specification Requirement**: FR-001 explicitly requires "menu-driven CLI interface with numbered options"
- **Target Audience**: Beginners prefer visual menus over memorizing commands
- **Error Handling**: Simple range validation (1-6) vs string matching
- **Discoverability**: Menu always shows available options
- **Validation Simplicity**: `choice.isdigit() and 1 <= int(choice) <= 6`

**Menu Structure**:
```
=== Todo Application ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Exit

Enter your choice (1-6): _
```

**References**:
- spec.md FR-001: "System MUST provide a menu-driven CLI interface with numbered options"
- [Python CLI Best Practices](https://docs.python.org/3/library/cmd.html)

### 3. State Management: Global List vs Manager Class

**Question**: How should task data be stored and accessed?

**Options Evaluated**:

| Option | Pros | Cons |
|--------|------|------|
| Global list variable | Simplest, direct access | Violates encapsulation, hard to test, global state |
| TodoService class | Encapsulation, testable, single responsibility | Slightly more complex |
| Singleton pattern | Global access + encapsulation | Overkill for single-user app, testing complexity |

**Decision**: **TodoService Manager Class**

**Rationale**:
- **Encapsulation**: Implementation (list) hidden behind interface
- **Testability**: Can create isolated service instances for testing
- **Validation**: Centralized index/description validation in one place
- **Single Responsibility**: Service manages data, CLI handles I/O
- **Evolution Ready**: Phase II can add database layer without changing interface

**Service Interface**:
```python
class TodoService:
    def __init__(self):
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def add_task(self, description: str) -> Task:
        """Add a new task with validated description."""

    def get_all_tasks(self) -> List[Task]:
        """Return copy of all tasks."""

    def update_task(self, index: int, description: str) -> Task:
        """Update task at index with new description."""

    def delete_task(self, index: int) -> None:
        """Remove task at index and renumber remaining."""

    def mark_complete(self, index: int) -> Task:
        """Mark task at index as completed (idempotent)."""
```

**References**:
- [SOLID Principles: Single Responsibility](https://en.wikipedia.org/wiki/Single-responsibility_principle)
- [Python Design Patterns: Service Layer](https://www.cosmicpython.com/book/chapter_04_service_layer.html)

### 4. Index Handling: 0-Based vs 1-Based

**Question**: Should task indices start at 0 or 1?

**Options Evaluated**:

| Option | Pros | Cons |
|--------|------|------|
| 0-based (internal) | Python standard, list access | Confusing for non-programmers |
| 1-based (user-facing) | Natural counting, spec alignment | Requires conversion layer |
| UUID/Hash-based | Avoids renumbering issues | Overkill, not in spec, harder for users |

**Decision**: **1-based for users, 0-based internally**

**Rationale**:
- **Specification**: User Story 1 states "unique index number starting from 1"
- **User Expectation**: Non-technical users expect lists to start at 1
- **Conversion Layer**: CLI converts user input (`1`) to list index (`0`)
- **Python Standard**: Internal code uses 0-based (idiomatic)

**Conversion Logic**:
```python
# User Input → CLI Handler
user_input = input("Enter task number: ")  # User enters: 1
list_index = int(user_input) - 1           # Convert to: 0

# Service Layer → CLI Display
for index, task in enumerate(tasks):
    print(f"{index + 1}. {task}")          # Display as: 1. Task
```

**References**:
- spec.md User Story 1: "each task receives a unique index number starting from 1"
- [Why Arrays Start at 0](https://www.cs.utexas.edu/users/EWD/transcriptions/EWD08xx/EWD831.html)

### 5. Error Handling: Exceptions vs Return Codes

**Question**: How should errors be communicated between layers?

**Options Evaluated**:

| Option | Pros | Cons |
|--------|------|------|
| Exceptions (ValueError, IndexError) | Pythonic, clear error types, stack traces | Can crash if unhandled |
| Return codes (-1, None) | Simple, no exception handling | Ambiguous, easy to ignore |
| Result type (success/error) | Explicit error handling | Not idiomatic Python |

**Decision**: **Exceptions with try/except in CLI layer**

**Rationale**:
- **Pythonic**: Exceptions are standard Python error handling
- **Type Clarity**: `ValueError` for validation, `IndexError` for bounds
- **Separation**: Service raises exceptions, CLI catches and displays
- **Spec Alignment**: FR-013 requires "specific error messages" - exceptions carry messages
- **Fail-Fast**: Invalid data detected immediately, not propagated

**Exception Handling Pattern**:
```python
# Service Layer
def add_task(self, description: str) -> Task:
    desc = description.strip()
    if not desc:
        raise ValueError("Task description cannot be empty")
    if len(desc) > 500:
        raise ValueError("Task description too long (max 500 characters)")
    # ... create task

# CLI Layer
def handle_add_task(service: TodoService):
    try:
        description = input("Enter task description: ")
        task = service.add_task(description)
        print(f"✓ Task added: {task.description}")
    except ValueError as e:
        print(f"✗ Error: {e}")
```

**References**:
- [PEP 3134 - Exception Chaining](https://peps.python.org/pep-3134/)
- [Python Exceptions Best Practices](https://realpython.com/python-exceptions/)

### 6. Task Completion: Boolean vs Enum

**Question**: How should task completion status be represented?

**Options Evaluated**:

| Option | Pros | Cons |
|--------|------|------|
| Boolean (`completed`) | Simple, clear True/False | Not extensible (no "in progress") |
| Enum (INCOMPLETE, COMPLETE) | Explicit states, extensible | Overkill for 2 states |
| String ("done", "pending") | Human-readable | Error-prone, no type safety |

**Decision**: **Boolean (`completed: bool`)**

**Rationale**:
- **Specification**: Phase I only has "complete" vs "incomplete" (2 states)
- **Simplicity**: `if task.completed` is clearer than `if task.status == Status.COMPLETE`
- **Memory Efficient**: bool is 1 byte vs enum overhead
- **Progressive Complexity**: Phase I should use simplest solution
- **Future-Proof**: Phase II can migrate to enum if needed (non-breaking)

**Implementation**:
```python
@dataclass
class Task:
    description: str
    completed: bool = False  # Default to incomplete
    id: int = 0

# Usage
task.completed = True  # Mark complete
if task.completed:     # Check status
    print("[✓]")
```

**References**:
- spec.md FR-006: "System MUST support marking tasks as complete by index number"
- Constitution: Progressive Complexity - "Phase I: basics"

### 7. Display Formatting: ASCII vs Unicode

**Question**: Should completion status use ASCII [ ] [X] or Unicode [✓]?

**Options Evaluated**:

| Option | Pros | Cons |
|--------|------|------|
| Unicode [✓] [✗] | Visually clear, modern | May not render on old terminals |
| ASCII [X] [ ] | Universal compatibility | Less visually distinct |
| Emoji ✅ ❌ | Colorful, fun | Inconsistent rendering, unprofessional |

**Decision**: **Unicode [✓] with ASCII fallback**

**Rationale**:
- **Visual Clarity**: ✓ is universally recognized checkmark
- **Modern Terminals**: UTF-8 supported on Windows 10+, macOS, Linux
- **Fallback Strategy**: Detect encoding, use `[X]` if UTF-8 unavailable
- **Spec Alignment**: FR-003 requires "clearly indicates" completion status

**Implementation**:
```python
import sys

def get_status_symbol(completed: bool) -> str:
    """Return completion symbol with UTF-8 fallback."""
    if sys.stdout.encoding.lower() in ('utf-8', 'utf8'):
        return "[✓]" if completed else "[ ]"
    else:
        return "[X]" if completed else "[ ]"

# Display
print(f"{index + 1}. {get_status_symbol(task.completed)} {task.description}")
```

**References**:
- [Unicode Checkmark (U+2713)](https://unicode-table.com/en/2713/)
- [Python UTF-8 Encoding](https://docs.python.org/3/howto/unicode.html)

## Best Practices Adopted

### Python 3.13+ Features

**Typing Enhancements**: Use modern type hints
```python
from typing import List  # Python 3.9+
from collections.abc import Sequence  # Python 3.10+

def get_tasks(self) -> list[Task]:  # Python 3.9+ lowercase list
    return self._tasks.copy()
```

**Dataclass Features**: Leverage `__post_init__` for validation
```python
@dataclass
class Task:
    description: str
    completed: bool = False

    def __post_init__(self):
        self.description = self.description.strip()
        if not self.description:
            raise ValueError("Empty description")
```

### PEP 8 Compliance

- **Function Names**: `snake_case` (e.g., `add_task`, `get_all_tasks`)
- **Class Names**: `PascalCase` (e.g., `Task`, `TodoService`)
- **Constants**: `UPPER_CASE` (e.g., `MAX_DESCRIPTION_LENGTH = 500`)
- **Private Members**: `_underscore_prefix` (e.g., `self._tasks`)
- **Line Length**: Max 88 characters (Black formatter default)
- **Imports**: Standard library, third-party, local (Phase I has no third-party)

**References**:
- [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [Black Code Formatter](https://black.readthedocs.io/)

### Dependency Management with UV

**Why UV over venv/pip**:
- **Faster**: Rust-based, 10-100x faster than pip
- **Deterministic**: Lock file ensures reproducible environments
- **Modern**: Active development, Python 3.13+ support
- **Simple**: `uv run` executes scripts in isolated environment

**Project Setup**:
```toml
# pyproject.toml
[project]
name = "phase-1-cli-todo"
version = "0.1.0"
description = "Phase I: In-Memory Python Console Todo Application"
requires-python = ">=3.13"
dependencies = []  # No external dependencies in Phase I

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**References**:
- [UV Documentation](https://github.com/astral-sh/uv)
- [PEP 621 - pyproject.toml](https://peps.python.org/pep-0621/)

## Technology Stack Summary

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Language | Python 3.13+ | Spec requirement, modern features |
| Data Model | Dataclass | Type safety, validation, readability |
| State Management | TodoService class | Encapsulation, testability |
| CLI Pattern | Numeric menu | Spec requirement, beginner-friendly |
| Error Handling | Exceptions | Pythonic, clear error types |
| Completion Status | Boolean | Simple, sufficient for Phase I |
| Display Symbols | Unicode [✓] with ASCII fallback | Visual clarity, compatibility |
| Dependency Management | UV | Fast, modern, deterministic |
| Code Style | PEP 8 (Black formatter) | Standard, automated |

## Validation Checklist

- [x] No external dependencies (Python stdlib only)
- [x] In-memory storage only (no files, databases)
- [x] PEP 8 compliant patterns
- [x] Type hints for all public APIs
- [x] Validation at data layer (Task, TodoService)
- [x] User-friendly error messages
- [x] 1-based indexing for users
- [x] Cross-platform compatibility (Windows, macOS, Linux)
- [x] Graceful error handling (no crashes)
- [x] Clear separation of concerns (models, services, cli)

## References

1. [Python Data Classes (PEP 557)](https://peps.python.org/pep-0557/)
2. [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
3. [UV - Fast Python Package Manager](https://github.com/astral-sh/uv)
4. [Real Python: Python Type Checking](https://realpython.com/python-type-checking/)
5. [SOLID Principles in Python](https://realpython.com/solid-principles-python/)
6. [Python CLI Best Practices](https://docs.python-guide.org/writing/structure/)

## Conclusion

All technical research complete. Decisions align with Phase I constitution (simplicity, no external dependencies, PEP 8 compliance) and specification requirements (menu-driven, 1-based indexing, 500-char limit, error handling). Ready to proceed with data model definition and implementation.
