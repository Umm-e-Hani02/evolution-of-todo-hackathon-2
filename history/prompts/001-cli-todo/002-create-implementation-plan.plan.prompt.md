---
id: 002
title: Create Implementation Plan
stage: plan
date: 2026-01-03
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-cli-todo
branch: 001-cli-todo
user: admin
command: sp.plan
labels: ["plan", "architecture", "phase-1", "cli-todo", "design-decisions"]
links:
  spec: specs/001-cli-todo/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-cli-todo/plan.md
  - specs/001-cli-todo/research.md
  - specs/001-cli-todo/data-model.md
  - specs/001-cli-todo/quickstart.md
  - specs/001-cli-todo/contracts/todo_service.md
tests:
  - Manual CLI acceptance testing (documented in plan)
---

## Prompt

Create an implementation plan that includes:

Architecture:
- Simple layered structure:
  - models: task representation
  - services: todo operations logic
  - cli: input/output handling
  - main: application entry point and main loop
- In-memory task storage using a list or dataclass instances.

Implementation Phases:
1. Requirements recap.
2. Architecture and data model definition.
3. Feature implementation:
   - Add task
   - View tasks
   - Update task
   - Delete task
   - Mark task as complete
4. Input validation and error handling.
5. Code cleanup and readability review.

Development Approach:
- Iterative, feature-by-feature implementation.
- Implement core CLI loop first.
- Add commands incrementally.
- Refactor continuously to maintain clean code.

Design Decisions to Document:
- Task model: dict vs dataclass.
- Command handling: numeric menu vs text-based commands.
- State management: global list vs manager class.

Testing Strategy:
- Manual CLI acceptance testing:
  - Add -> view -> update -> delete -> complete.
- Edge cases:
  - Invalid task index.
  - Empty task list.
  - Empty or malformed input.
- Ensure no data persists after program exit.

## Response snapshot

Created comprehensive implementation plan for Phase I In-Memory Python Console Todo Application.

**Planning Artifacts Generated**:
1. **plan.md** (555 lines) - Complete implementation roadmap
2. **research.md** - Technical research and design decisions
3. **data-model.md** - Task entity specification
4. **quickstart.md** - User guide for running the application
5. **contracts/todo_service.md** - Service interface contract

**Technical Context Defined**:
- **Language**: Python 3.13+
- **Dependencies**: Python standard library only (no external packages)
- **Storage**: In-memory list (session-only, no persistence)
- **Testing**: Manual CLI acceptance testing
- **Architecture**: Layered (models → services → cli → main)

**Constitution Check**: ✅ **PASSED**
- Scope alignment with Phase I requirements ✓
- No premature features from future phases ✓
- PEP 8 compliance standards defined ✓
- Clear separation of concerns enforced ✓

**Key Design Decisions (Phase 0 Research)**:
1. **Task Model**: Dataclass (chosen over dict for type safety, validation hooks, IDE support)
2. **CLI Pattern**: Numeric menu 1-6 (spec-aligned, beginner-friendly)
3. **State Management**: TodoService class (encapsulation, testability, future-proof)
4. **Indexing**: 1-based for users, 0-based internally (user expectation vs Python convention)
5. **Error Handling**: Exceptions with try/except in CLI (Pythonic, descriptive messages)
6. **Completion Status**: Boolean (simplest for 2-state system in Phase I)
7. **Display Format**: Unicode [✓] with ASCII fallback (visual clarity, compatibility)

**Architecture (Layered)**:
- **Models Layer** (`src/models/task.py`): Task dataclass with validation
- **Services Layer** (`src/services/todo_service.py`): CRUD operations, business logic
- **CLI Layer** (`src/cli/menu.py`, `handlers.py`): User interaction, I/O
- **Main** (`src/main.py`): Application bootstrap, main loop

**Data Model**:
- **Task Entity**: `id` (int, auto-assigned), `description` (str, 1-500 chars), `completed` (bool)
- **Validation**: Non-empty after trim, max 500 chars, whitespace trimmed
- **State Transitions**: Incomplete → Complete (idempotent marking)

**TodoService Interface**:
- `add_task(description: str) -> Task` - Create task with auto-ID
- `get_all_tasks() -> list[Task]` - Return task list copy
- `update_task(index: int, description: str) -> Task` - Modify description
- `delete_task(index: int) -> None` - Remove task, renumber
- `mark_complete(index: int) -> Task` - Set completed=True (idempotent)

**Implementation Phases** (11 phases defined):
1. Foundation - Project structure, UV setup
2. Core Data Model - Task dataclass
3. Service Layer - Basic operations (add, view)
4. Service Layer - Modify operations (update, delete, complete)
5. CLI Layer - Menu system
6. CLI Layer - Command handlers
7. Main Application Loop
8. Input Validation Refinement
9. Code Quality Review (PEP 8, docstrings, type hints)
10. Documentation and Testing

**Testing Strategy**:
- Manual CLI acceptance testing (23 scenarios from spec.md)
- Edge case coverage (empty list, invalid indices, long descriptions, etc.)
- No persistence verification (data lost on exit)

**Error Handling Patterns**:
- ValueError: Invalid descriptions (empty, too long)
- IndexError: Invalid task indices (out of range, empty list)
- User-friendly messages with guidance (e.g., "Valid indices: 1-3")

**Project Structure** (phase-1-cli/):
```
src/
├── models/task.py
├── services/todo_service.py
├── cli/menu.py, handlers.py
└── main.py
tests/acceptance_tests.md
pyproject.toml, .python-version, README.md
```

**Risk Mitigation**:
- Python version availability → UV handles version management
- Terminal encoding issues → UTF-8 explicit, ASCII fallback
- Feature creep → Strict Phase I constitution enforcement
- Over-engineering → Simplest solution principle

## Outcome

- ✅ Impact: Complete implementation plan ready for task breakdown - comprehensive architecture, design decisions, and implementation roadmap
- 🧪 Tests: Manual testing strategy defined with 23 acceptance scenarios
- 📁 Files: Created plan.md (555 lines), research.md, data-model.md, quickstart.md, contracts/todo_service.md
- 🔁 Next prompts: Run `/sp.tasks` to generate detailed task breakdown from implementation plan
- 🧠 Reflection: Plan demonstrates clear layered architecture (models-services-cli-main) with well-researched design decisions. Dataclass chosen for type safety, TodoService class for encapsulation, numeric menu for user-friendliness. All decisions align with Phase I constitution (simplicity, no external deps, PEP 8). 11 implementation phases provide clear progression from setup through testing. Service contract enables independent development of layers.

## Evaluation notes (flywheel)

- Failure modes observed: None - plan created successfully with all required artifacts
- Graders run and results (PASS/FAIL): Constitution Check - PASS (all Phase I requirements met)
- Prompt variant (if applicable): Standard SDD planning workflow with user-specified architecture preferences (layered structure, dataclass, TodoService pattern)
- Next experiment (smallest change to try): Generate tasks.md to validate plan granularity and identify any missing implementation steps
